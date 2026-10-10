const decisions = [...document.querySelectorAll('input[name="decision"]')];
const support = document.querySelector('#support');
const actionButtons = [...document.querySelectorAll('[data-event]')];
const feedback = document.querySelector('.decision-feedback');
const status = document.querySelector('.tracking-status');
const description = document.querySelector('.tracking-description');
let state = 'inicial';

const messages = {
  inicial: ['Por activar', 'En este escenario falta que el responsable active la solicitud y confirme su recepción.'],
  recibida: ['Solicitud recibida · Simulación', 'La recepción no confirma una hora ni una atención. El responsable debe coordinar el siguiente contacto.'],
  'sin-cupo': ['Espera sin cupo · Simulación', 'La derivación sigue abierta. El responsable registra la falta de disponibilidad y solicita coordinación; no la cierra como una atención recibida.'],
  atendida: ['Atención confirmada · Simulación', 'En este escenario se comprobó la atención y puede cerrarse el seguimiento por ese motivo. Esto no representa una atención real.']
};
const copy = {
  acepta: 'En este escenario, la usuaria acepta orientación y puede acordar un apoyo prioritario.',
  posterga: 'En este escenario se respeta su tiempo. Solo se acuerda un contacto posterior si ella lo desea; no se activa una derivación.',
  rechaza: 'En este escenario no se activa una derivación. Se respeta la decisión y puede ofrecerse información si la desea.'
};

function render(updateURL = true) {
  const decision = decisions.find(input => input.checked)?.value || 'acepta';
  feedback.textContent = copy[decision];
  const agreed = decision === 'acepta';
  support.disabled = !agreed;
  actionButtons.forEach(button => { button.disabled = !agreed && button.dataset.event !== 'reiniciar'; });
  document.querySelectorAll('[data-support]').forEach(element => {
    element.textContent = agreed ? support.value : 'Sin derivación activada';
  });
  const stages = [...document.querySelectorAll('[data-stage]')];
  stages.forEach(item => item.classList.remove('is-done', 'is-waiting'));
  stages[0].querySelector('p').textContent = agreed ? 'La usuaria acepta orientación.' : 'La decisión de la usuaria se respeta.';
  stages[1].querySelector('p').textContent = 'Falta confirmar recepción.';
  stages[2].querySelector('p').textContent = 'No hay hora confirmada.';
  stages[3].querySelector('p').textContent = 'Todavía no se confirma una atención.';
  if (agreed) {
    stages[0].classList.add('is-done');
    if (state !== 'inicial') { stages[1].classList.add('is-done'); stages[1].querySelector('p').textContent = 'Recepción representada en el ensayo.'; }
    if (state === 'sin-cupo') { stages[2].classList.add('is-waiting'); stages[2].querySelector('p').textContent = 'Falta disponibilidad. Requiere coordinación.'; }
    if (state === 'atendida') {
      stages[2].classList.add('is-done'); stages[2].querySelector('p').textContent = 'Coordinación completada en el escenario.';
      stages[3].classList.add('is-done'); stages[3].querySelector('p').textContent = 'Atención confirmada solo en la simulación.';
    }
    [status.textContent, description.textContent] = messages[state];
  } else {
    status.textContent = decision === 'posterga' ? 'Postergada por decisión · Simulación' : 'Sin solicitud por decisión · Simulación';
    description.textContent = copy[decision] + ' Este cierre no equivale a haber recibido atención.';
  }
  if (updateURL) {
    const url = new URL(location.href);
    url.searchParams.set('decision', decision);
    url.searchParams.set('apoyo', String(support.selectedIndex));
    url.searchParams.set('estado', state);
    history.replaceState(null, '', url);
  }
}
function restoreURL() {
  const url = new URL(location.href);
  const decision = url.searchParams.get('decision');
  decisions.forEach(input => { input.checked = input.value === (Object.hasOwn(copy, decision) ? decision : 'acepta'); });
  const index = Number(url.searchParams.get('apoyo') || 0);
  support.selectedIndex = Number.isInteger(index) && index >= 0 && index < support.options.length ? index : 0;
  const candidate = url.searchParams.get('estado');
  state = Object.hasOwn(messages, candidate) ? candidate : 'inicial';
  render(false);
}
decisions.forEach(input => input.addEventListener('change', () => { state = 'inicial'; render(); }));
support.addEventListener('change', () => { state = 'inicial'; render(); });
actionButtons.forEach(button => button.addEventListener('click', () => {
  if (button.dataset.event === 'reiniciar') {
    decisions.forEach(input => { input.checked = input.value === 'acepta'; });
    support.selectedIndex = 0;
    state = 'inicial';
  } else state = button.dataset.event;
  render();
}));
window.addEventListener('popstate', restoreURL);
restoreURL();
const printButton = document.querySelector('#print-prototype');
printButton.hidden = false;
printButton.addEventListener('click', () => window.print());
