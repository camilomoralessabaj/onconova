import { appointmentDate, createReceiptPdf, sessionInstructions } from './receipt-pdf.js';

// Academic simulation. No requests, personal fields, URL state or persistent booking data.
const booking = document.querySelector('[data-booking]');
if (booking) {
  const find = selector => booking.querySelector(selector);
  const requestForm = find('[data-request-form]');
  const scheduleForm = find('[data-schedule-form]');
  const waitForm = find('[data-wait-form]');
  const steps = { start: 0, message: 1, schedule: 2, waiting: 2, confirmed: 3, paused: 0 };
  let current = 'start';
  let channel = 'WhatsApp';
  let modality = 'Videollamada';
  let selected = null;
  let slots = [];
  const dayFormat = new Intl.DateTimeFormat('en-CA', { year: 'numeric', month: '2-digit', day: '2-digit', timeZone: 'America/Santiago' });

  function show(screen) {
    find('[data-booking-status]').textContent = '';
    current = screen;
    booking.querySelectorAll('[data-screen]').forEach(element => { element.hidden = element.dataset.screen !== screen; });
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
  function updatePreferences() {
    channel = requestForm.elements.channel.value;
    modality = requestForm.elements.modality.value;
    booking.querySelectorAll('[data-modality-copy]').forEach(element => {
      element.textContent = modality === 'Videollamada' ? 'por videollamada' : 'de forma presencial';
    });
    find('[data-message-channel]').textContent = channel === 'Correo' ? 'Correo para usuaria@example.com' : 'Conversación de WhatsApp de ejemplo';
    find('[data-message-subject]').textContent = channel === 'Correo' ? 'Asunto: elige tu primera hora de apoyo psicológico' : 'Tu solicitud tiene un siguiente paso';
  }
  function createSlots() {
    // Use Santiago's calendar day, then operate at UTC noon to avoid local/DST shifts.
    const parts = Object.fromEntries(dayFormat.formatToParts(new Date()).map(part => [part.type, part.value]));
    const day = new Date(Date.UTC(Number(parts.year), Number(parts.month) - 1, Number(parts.day), 12));
    slots = [];
    while (slots.length < 3) {
      day.setUTCDate(day.getUTCDate() + 1);
      if (![0, 6].includes(day.getUTCDay())) {
        slots.push({ year: day.getUTCFullYear(), month: day.getUTCMonth() + 1, day: day.getUTCDate(), time: ['10:00', '15:30', '11:00'][slots.length] });
      }
    }
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
  function clearConfirmation() {
    selected = null;
    ['date', 'modality', 'channel'].forEach(key => { find(`[data-appointment-${key}]`).textContent = ''; });
    find('[data-before-session]').textContent = '';
  }
  function reset() {
    requestForm.reset(); scheduleForm.reset(); waitForm.reset();
    clearConfirmation();
    find('[data-slot-error]').hidden = true;
    find('[data-wait-result]').hidden = true;
    find('[data-wait-copy]').textContent = '';
    find('[data-booking-status]').textContent = '';
    createSlots(); updatePreferences(); show('start');
  }
  requestForm.addEventListener('submit', event => {
    event.preventDefault();
    if (current !== 'start' || !requestForm.reportValidity()) return;
    clearConfirmation(); scheduleForm.reset(); updatePreferences(); show('message');
  });
  scheduleForm.addEventListener('submit', event => {
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
    find('[data-appointment-date]').textContent = `${appointmentDate(selected)}, ${selected.time} h (Santiago de Chile)`;
    find('[data-appointment-modality]').textContent = modality === 'Videollamada' ? 'Videollamada de ejemplo' : 'Consulta presencial de ejemplo';
    find('[data-appointment-channel]').textContent = `${channel} · Mensaje no enviado`;
    find('[data-before-session]').textContent = sessionInstructions(modality).join(' ');
    show('confirmed');
  });
  scheduleForm.addEventListener('change', () => { find('[data-slot-error]').hidden = true; });
  waitForm.addEventListener('submit', event => {
    event.preventDefault();
    if (current !== 'waiting') return;
    find('[data-wait-copy]').textContent = `Prefieres ${waitForm.elements['preferred-time'].value} y el contacto por ${channel}. Esta preferencia solo existe en esta página; no se envió.`;
    find('[data-wait-result]').hidden = false;
  });
  waitForm.addEventListener('change', () => { find('[data-wait-result]').hidden = true; });
  booking.addEventListener('click', event => {
    const action = event.target.closest('[data-action]')?.dataset.action;
    if (!action) return;
    if (action === 'reset') reset();
    if (action === 'edit' && current === 'message') { clearConfirmation(); show('start'); }
    if (action === 'message' && current === 'schedule') show('message');
    if (action === 'schedules' && ['message', 'waiting'].includes(current)) show('schedule');
    if (action === 'reschedule' && current === 'confirmed') { clearConfirmation(); scheduleForm.reset(); show('schedule'); }
    if (action === 'unavailable' && current === 'schedule') { clearConfirmation(); scheduleForm.reset(); find('[data-wait-result]').hidden = true; show('waiting'); }
    if (['later', 'decline'].includes(action) && current === 'start') {
      find('[data-pause-title]').textContent = action === 'later' ? 'Puedes darte un tiempo.' : 'Tu decisión también cuenta.';
      find('[data-pause-copy]').textContent = action === 'later' ? 'No se ha iniciado una solicitud, ni siquiera dentro de la simulación. Puedes conocer la propuesta y volver cuando quieras.' : 'No se inicia una solicitud ni un contacto de seguimiento. Puedes volver a explorar el recorrido si cambias de opinión.';
      show('paused');
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
  find('[data-screen="start"]').hidden = false;
  createSlots(); updatePreferences();
}
