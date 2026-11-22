import { appointmentDate, createReceiptPdf, sessionInstructions, SESSION_MINUTES } from './receipt-pdf.js';

const bands = {
  morning: [9 * 60, 12 * 60],
  midday: [12 * 60, 15 * 60],
  afternoon: [15 * 60, 18 * 60]
};
// Some starts straddle band boundaries and only appear if the full session fits.
const exampleStarts = {
  Videollamada: ['09:00', '11:30', '12:00', '14:30', '15:00', '17:15'],
  Presencial: ['11:15', '11:30', '14:15', '14:30', '15:30', '17:30']
};
const searchDays = 14;
const maxSlots = 3;
const slotKey = ({ year, month, day, time }) => [year, month, day, time].join('/');
const dayFormat = new Intl.DateTimeFormat('en-CA', { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'America/Santiago' });

function* upcomingDays() {
  // UTC noon represents a civil date in Santiago without device timezone or DST arithmetic.
  const parts = Object.fromEntries(dayFormat.formatToParts(new Date()).map(part => [part.type, part.value]));
  const date = new Date(Date.UTC(Number(parts.year), Number(parts.month) - 1, Number(parts.day), 12));
  for (let offset = 0; offset < searchDays; offset++) {
    date.setUTCDate(date.getUTCDate() + 1);
    const weekday = date.getUTCDay();
    if (weekday === 0 || weekday === 6) continue;
    yield { weekday, year: date.getUTCFullYear(), month: date.getUTCMonth() + 1, day: date.getUTCDate() };
  }
}

function fitsBand(time, [start, end]) {
  const [hour, minute] = time.split(':').map(Number);
  const startsAt = hour * 60 + minute;
  return startsAt >= start && startsAt + SESSION_MINUTES <= end;
}

// Academic simulation. Contact fields stay in memory/DOM; no requests, URL state or storage.
const booking = document.querySelector('[data-booking]');
if (booking) {
  const find = selector => booking.querySelector(selector);
  const requestForm = find('[data-request-form]');
  const scheduleForm = find('[data-schedule-form]');
  const waitForm = find('[data-wait-form]');
  const steps = { start: 0, message: 1, schedule: 2, waiting: 2, pending: 2, confirmed: 3, paused: 0 };
  let current = 'start';
  let channel = 'WhatsApp';
  let modality = 'Videollamada';
  let selected = null;
  let slots = [];
  let proposal = 'initial';
  const rejectedSlots = new Set();
  let attempted = false;
  let attemptedAvailability = false;
  const availabilityGroups = [
    ['preferred-day', 'preferred-day-error', 'Marca al menos un día de la semana.'],
    ['preferred-band', 'preferred-band-error', 'Marca al menos una franja horaria.']
  ];

  let pointerSubmitActivation = null;
  const isPointerClick = event => event.isTrusted && event.detail > 0;
  // A submit event has no click detail; remember only its native pointer activation.
  document.addEventListener('click', event => {
    pointerSubmitActivation = null;
    const button = event.target instanceof Element ? event.target.closest('button') : null;
    if (!isPointerClick(event) || !button || !booking.contains(button) || button.type !== 'submit') return;
    const activation = { submitter: button };
    pointerSubmitActivation = activation;
    // Expire even when native validation prevents a submit event.
    setTimeout(() => {
      if (pointerSubmitActivation === activation) pointerSubmitActivation = null;
    }, 0);
  }, true);
  document.addEventListener('keydown', () => {
    pointerSubmitActivation = null;
    booking.querySelectorAll('[data-step-entry]').forEach(element => element.removeAttribute('data-step-entry'));
  }, true);
  function consumePointerSubmit(event) {
    const activation = pointerSubmitActivation;
    pointerSubmitActivation = null;
    return Boolean(event.isTrusted && activation && event.submitter === activation.submitter);
  }

  function show(screen, { animate = false } = {}) {
    const shouldAnimate = animate && screen !== current &&
      window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
    find('[data-booking-status]').textContent = '';
    current = screen;
    booking.querySelectorAll('[data-screen]').forEach(element => {
      const visible = element.dataset.screen === screen;
      element.toggleAttribute('data-step-entry', visible && shouldAnimate);
      element.hidden = !visible;
    });
    booking.querySelectorAll('[data-progress]').forEach(element => {
      const step = Number(element.dataset.progress);
      element.classList.toggle('complete', step < steps[screen]);
      if (step === steps[screen]) element.setAttribute('aria-current', 'step');
      else element.removeAttribute('aria-current');
    });
    find('[data-action="reset"]').hidden = screen === 'start';
    const heading = find(`[data-screen="${screen}"] h3`);
    heading.focus({ preventScroll: true });
    heading.scrollIntoView({ block: 'start', behavior: 'instant' });
  }
  function clearMessage() {
    ['name', 'channel', 'subject'].forEach(key => { find(`[data-message-${key}]`).textContent = ''; });
  }
  function contactValue() {
    return requestForm.elements[channel === 'Correo' ? 'contact-email' : 'contact-phone'].value.trim();
  }
  function updatePreferences() {
    channel = requestForm.elements.channel.value;
    modality = requestForm.elements.modality.value;
    booking.querySelectorAll('[data-modality-copy]').forEach(element => {
      element.textContent = modality === 'Videollamada' ? 'por videollamada' : 'de forma presencial';
    });
    find('[data-proposal-note]').textContent = proposal === 'initial'
      ? 'Primera propuesta de horarios ficticios.'
      : `Horarios de ejemplo según tus preferencias · ${modality}`;
    find('[data-action="adjust-availability"]').hidden = proposal === 'initial';
    find('[data-message-name]').textContent = requestForm.elements['preferred-name'].value.trim();
    find('[data-message-channel]').textContent = `${channel} para ${contactValue()}`;
    find('[data-message-subject]').textContent = channel === 'Correo' ? 'Asunto: elige tu primera hora de apoyo psicológico' : 'Tu solicitud tiene un siguiente paso';
  }
  function setError(input, id, message) {
    const error = find(`#${id}`);
    // Avoid repeating the same live-region announcement on every keystroke.
    if (error.textContent !== message) error.textContent = message;
    error.hidden = !message;
    if (message) input.setAttribute('aria-invalid', 'true');
    else input.removeAttribute('aria-invalid');
  }
  function checkedValues(name) {
    return Array.from(waitForm.elements[name]).filter(input => input.checked).map(input => input.value);
  }
  function validateAvailability() {
    let firstInvalid;
    for (const [name, id, message] of availabilityGroups) {
      const firstInput = waitForm.elements[name][0];
      const missing = !checkedValues(name).length;
      setError(firstInput, id, missing ? message : '');
      if (missing) firstInvalid ??= firstInput;
    }
    return firstInvalid;
  }
  function validateRequest({ focus = false } = {}) {
    const name = requestForm.elements['preferred-name'];
    const phone = requestForm.elements['contact-phone'];
    const email = requestForm.elements['contact-email'];
    const consent = requestForm.elements['demo-consent'];
    const phoneValue = phone.value.trim();
    const digits = phoneValue.replace(/\D/g, '').length;
    const errors = [
      [name, 'name-error', !name.value.trim() ? 'Escribe un nombre ficticio para continuar.' : name.value.length > 80 ? 'Usa un nombre de hasta 80 caracteres.' : ''],
      [phone, 'phone-error', phone.disabled ? '' : !phoneValue ? 'Escribe un teléfono ficticio para WhatsApp.' : !/^\+?[\d ()-]+$/.test(phoneValue) || digits < 8 || digits > 15 || phone.value.length > 30 ? 'Revisa el formato: usa de 8 a 15 dígitos, con +, espacios, guiones o paréntesis si lo necesitas.' : ''],
      [email, 'email-error', email.disabled ? '' : !email.value.trim() ? 'Escribe un correo ficticio para continuar.' : email.validity.typeMismatch || email.value.length > 254 ? 'Revisa el formato del correo, por ejemplo nombre@example.com (hasta 254 caracteres).' : ''],
      [consent, 'consent-error', !consent.checked ? 'Marca que entiendes la simulación antes de continuar.' : '']
    ];
    errors.forEach(([input, id, message]) => setError(input, id, message));
    const first = errors.find(([, , message]) => message);
    if (first && focus) {
      find('[data-screen="start"]').removeAttribute('data-step-entry');
      first[0].focus();
    }
    return !first;
  }
  function syncContactFields() {
    channel = requestForm.elements.channel.value;
    booking.querySelectorAll('[data-contact-field]').forEach(field => {
      const active = field.dataset.contactField === channel;
      const input = field.querySelector('input');
      field.hidden = !active;
      input.disabled = !active;
      input.required = active;
      if (!active) input.value = '';
    });
  }
  function clearConfirmation() {
    selected = null;
    ['name', 'date', 'modality', 'channel'].forEach(key => { find(`[data-appointment-${key}]`).textContent = ''; });
    find('[data-before-session]').textContent = '';
    find('[data-booking-status]').textContent = '';
  }
  function invalidate() {
    clearConfirmation(); clearMessage(); scheduleForm.reset();
    find('[data-slot-error]').hidden = true;
  }
  function initialSlots() {
    return [...upcomingDays()].slice(0, maxSlots).map((day, index) => ({
      ...day, time: ['10:00', '15:30', '11:00'][index]
    }));
  }
  function alternativeSlots(days, preferredBands, preferredModality) {
    const times = exampleStarts[preferredModality].filter(time => preferredBands.some(band => fitsBand(time, band)));
    const matches = [];
    for (const day of upcomingDays()) {
      if (!days.includes(day.weekday)) continue;
      for (const time of times) {
        const slot = { ...day, time };
        if (rejectedSlots.has(slotKey(slot))) continue;
        matches.push(slot);
        if (matches.length === maxSlots) return matches;
      }
    }
    return matches;
  }
  function setProposal(kind, nextSlots) {
    invalidate();
    proposal = kind;
    slots = nextSlots;
    find('[data-slots]').replaceChildren(...slots.map((slot, index) => {
      const label = document.createElement('label');
      label.className = 'slot';
      const radio = document.createElement('input');
      radio.type = 'radio'; radio.name = 'slot'; radio.value = String(index);
      const date = document.createElement('span'); date.textContent = appointmentDate(slot);
      const time = document.createElement('strong'); time.textContent = `${slot.time} h`;
      const note = document.createElement('small'); note.textContent = 'Horario de ejemplo';
      label.append(radio, date, time, note);
      return label;
    }));
  }
  function showPending(reason, animate) {
    find('[data-pending-reason]').textContent = reason;
    show('pending', { animate });
  }
  function clearJourney() {
    requestForm.reset(); scheduleForm.reset(); waitForm.reset();
    attempted = false;
    attemptedAvailability = false;
    rejectedSlots.clear();
    for (const [name, id] of availabilityGroups) setError(waitForm.elements[name][0], id, '');
    syncContactFields();
    requestForm.querySelectorAll('[aria-invalid]').forEach(input => input.removeAttribute('aria-invalid'));
    requestForm.querySelectorAll('.field-error').forEach(error => { error.hidden = true; error.textContent = ''; });
    channel = requestForm.elements.channel.value;
    modality = requestForm.elements.modality.value;
    setProposal('initial', initialSlots()); updatePreferences(); clearMessage();
  }
  function reset({ animate = false } = {}) {
    clearJourney(); show('start', { animate });
  }
  requestForm.addEventListener('input', () => {
    invalidate(); syncContactFields();
    if (attempted) validateRequest();
  });
  requestForm.addEventListener('change', () => {
    invalidate(); syncContactFields();
    if (attempted) validateRequest();
  });
  requestForm.addEventListener('submit', event => {
    const animate = consumePointerSubmit(event);
    event.preventDefault();
    if (current !== 'start') return;
    attempted = true;
    if (!validateRequest({ focus: true })) return;
    waitForm.elements['alternative-modality'].value = requestForm.elements.modality.value;
    setProposal('initial', initialSlots()); updatePreferences(); show('message', { animate });
  });
  scheduleForm.addEventListener('submit', event => {
    const animate = consumePointerSubmit(event);
    event.preventDefault();
    if (current !== 'schedule') return;
    const input = scheduleForm.querySelector('input[name="slot"]:checked');
    if (!input || !slots[Number(input.value)]) {
      find('[data-slot-error]').hidden = false;
      scheduleForm.querySelector('input[name="slot"]').focus();
      return;
    }
    selected = slots[Number(input.value)];
    find('[data-slot-error]').hidden = true;
    find('[data-appointment-name]').textContent = requestForm.elements['preferred-name'].value.trim();
    find('[data-appointment-date]').textContent = `${appointmentDate(selected)}, ${selected.time} h (Santiago de Chile)`;
    find('[data-appointment-modality]').textContent = modality === 'Videollamada' ? 'Videollamada de ejemplo' : 'Consulta presencial de ejemplo';
    find('[data-appointment-channel]').textContent = `${channel} para ${contactValue()} · Mensaje no enviado`;
    find('[data-before-session]').textContent = sessionInstructions(modality).join(' ');
    show('confirmed', { animate });
  });
  scheduleForm.addEventListener('change', () => { find('[data-slot-error]').hidden = true; });
  waitForm.addEventListener('submit', event => {
    const animate = consumePointerSubmit(event);
    event.preventDefault();
    if (current !== 'waiting') return;
    attemptedAvailability = true;
    const firstInvalid = validateAvailability();
    if (firstInvalid) {
      find('[data-screen="waiting"]').removeAttribute('data-step-entry');
      firstInvalid.focus();
      return;
    }
    const days = checkedValues('preferred-day').map(Number);
    const preferredBands = checkedValues('preferred-band').map(value => bands[value]);
    const preferredModality = waitForm.elements['alternative-modality'].value;
    const matches = alternativeSlots(days, preferredBands, preferredModality);
    if (!matches.length) {
      invalidate();
      showPending('No quedan horarios ficticios que coincidan con los días, las franjas y la modalidad que elegiste.', animate);
      return;
    }
    requestForm.elements.modality.value = preferredModality;
    setProposal('alternative', matches);
    updatePreferences(); show('schedule', { animate });
  });
  waitForm.addEventListener('change', () => {
    if (attemptedAvailability) validateAvailability();
  });
  booking.addEventListener('click', event => {
    const action = event.target.closest('[data-action]')?.dataset.action;
    if (!action) return;
    const animate = isPointerClick(event);
    if (action === 'reset') reset({ animate });
    if (action === 'edit' && ['message', 'confirmed', 'pending'].includes(current)) { invalidate(); show('start', { animate }); }
    if (action === 'message' && current === 'schedule') { invalidate(); updatePreferences(); show('message', { animate }); }
    if (action === 'schedules' && ['message', 'waiting'].includes(current)) { updatePreferences(); show('schedule', { animate }); }
    if (action === 'reschedule' && current === 'confirmed') { clearConfirmation(); scheduleForm.reset(); show('schedule', { animate }); }
    if (action === 'unavailable' && current === 'schedule') {
      invalidate();
      slots.forEach(slot => rejectedSlots.add(slotKey(slot)));
      if (proposal === 'initial') show('waiting', { animate });
      else showPending('Tampoco te acomodaron los horarios de la nueva propuesta.', animate);
    }
    if (action === 'adjust-availability' && current === 'schedule') { invalidate(); show('waiting', { animate }); }
    if (action === 'review-alternatives' && current === 'pending') show('waiting', { animate });
    if (action === 'leave-pending' && ['waiting', 'pending'].includes(current)) {
      clearJourney();
      find('[data-pause-title]').textContent = 'Tu recorrido quedó pendiente.';
      find('[data-pause-copy]').textContent = 'Saliste sin confirmar una hora. Se eliminaron los datos de la demostración; no se envió una solicitud ni habrá un contacto real. Puedes volver al inicio si deseas explorar de nuevo.';
      show('paused', { animate });
    }
    if (['later', 'decline'].includes(action) && current === 'start') {
      find('[data-pause-title]').textContent = action === 'later' ? 'Puedes darte un tiempo.' : 'Tu decisión también cuenta.';
      find('[data-pause-copy]').textContent = action === 'later' ? 'No se ha iniciado una solicitud, ni siquiera dentro de la simulación. Puedes conocer la propuesta y volver cuando quieras.' : 'No se inicia una solicitud ni un contacto de seguimiento. Puedes volver a explorar el recorrido si cambias de opinión.';
      show('paused', { animate });
    }
    if (action === 'download' && current === 'confirmed' && selected) {
      const status = find('[data-booking-status]');
      let url;
      let link;
      status.textContent = '';
      try {
        const pdf = createReceiptPdf({ slot: selected, modality, channel });
        url = URL.createObjectURL(pdf);
        link = document.createElement('a');
        link.href = url;
        link.download = 'onconova-comprobante-simulado.pdf';
        document.body.append(link);
        link.click();
        // Announce initiation: the browser owns the final save/cancel decision.
        status.textContent = 'Descarga del comprobante PDF iniciada. Es una cita simulada.';
      } catch {
        status.textContent = 'No se pudo preparar el comprobante PDF. Intenta descargarlo de nuevo.';
      } finally {
        link?.remove();
        // Leave time for the browser to consume the URL, including repeated downloads.
        if (url) setTimeout(() => URL.revokeObjectURL(url), 1000);
      }
    }
  });
  // Explicitly clear browser-restored fields on load, reload and back/forward cache.
  clearJourney();
  find('[data-screen="start"]').hidden = false;
  window.addEventListener('pageshow', event => { if (event.persisted) reset(); });
}
