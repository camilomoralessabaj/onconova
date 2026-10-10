const textSize = document.querySelector('.text-size');
if (textSize) {
  textSize.hidden = false;
  textSize.setAttribute('aria-label', 'Texto más grande');
  let larger = false;
  try { larger = localStorage.getItem('onconova-large-text') === 'true'; } catch { /* Preferencia opcional. */ }
  const applySize = () => {
    document.documentElement.classList.toggle('large-text', larger);
    textSize.setAttribute('aria-pressed', String(larger));
    textSize.setAttribute('aria-label', larger ? 'Volver al tamaño de texto original' : 'Texto más grande');
    const label = textSize.querySelector('.text-size-label');
    if (label) label.textContent = larger ? 'Tamaño original' : 'Texto más grande';
  };
  applySize();
  textSize.addEventListener('click', () => {
    larger = !larger;
    applySize();
    try { localStorage.setItem('onconova-large-text', String(larger)); } catch { /* La lectura sigue disponible. */ }
  });
}

function openReferencedSource(hash = location.hash) {
  if (!hash.startsWith('#fuente-')) return;
  const source = document.getElementById(hash.slice(1));
  const details = source?.closest('details');
  if (details) details.open = true;
  if (source) requestAnimationFrame(() => source.scrollIntoView({ block: 'start', behavior: 'instant' }));
}
document.addEventListener('click', event => {
  const anchor = event.target.closest('a[href^="#fuente-"]');
  if (anchor) {
    const source = document.getElementById(anchor.getAttribute('href').slice(1));
    if (source?.closest('details')) source.closest('details').open = true;
  }
});
window.addEventListener('hashchange', () => openReferencedSource());
openReferencedSource();

const navigation = [...document.querySelectorAll('.chapter-nav a')];
if ('IntersectionObserver' in window && navigation.length) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      for (const link of navigation) {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      }
    }
  }, { rootMargin: '-22% 0px -55% 0px', threshold: 0 });
  document.querySelectorAll('[data-chapter]').forEach(chapter => observer.observe(chapter));
}

const choiceButtons = [...document.querySelectorAll('[data-choice]')];
if (choiceButtons.length) {
  let choices;
  try {
    const response = await fetch(new URL('../content/project.json', import.meta.url));
    if (!response.ok) throw new Error('Contenido no disponible');
    choices = (await response.json()).choices;
  } catch {
    document.querySelector('[data-choice-result]').textContent = 'Puedes explorar estas decisiones en la maqueta completa. Recarga la página para volver a intentar esta vista.';
    choiceButtons.forEach(button => { button.disabled = true; });
  }
  if (choices) {
    const selectChoice = (id, updateURL = true) => {
      const choice = choices.find(item => item.id === id);
      if (!choice) return;
      choiceButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.choice === id)));
      document.querySelector('[data-choice-result]').textContent = choice.explanation;
      if (updateURL) {
        const url = new URL(location.href);
        url.searchParams.set('eleccion', id);
        history.replaceState(null, '', url);
      }
    };
    choiceButtons.forEach(button => button.addEventListener('click', () => selectChoice(button.dataset.choice)));
    selectChoice(new URL(location.href).searchParams.get('eleccion'), false);
    window.addEventListener('popstate', () => selectChoice(new URL(location.href).searchParams.get('eleccion'), false));
  }
}
