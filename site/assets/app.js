const textSize = document.querySelector('.text-size');
if (textSize) {
  textSize.hidden = false;
  let larger = false;
  try { larger = localStorage.getItem('onconova-large-text') === 'true'; } catch { /* Optional reading preference. */ }
  const applySize = () => {
    document.documentElement.classList.toggle('large-text', larger);
    textSize.setAttribute('aria-pressed', String(larger));
    textSize.setAttribute('aria-label', larger ? 'Volver al tamaño de texto original' : 'Texto más grande');
  };
  applySize();
  textSize.addEventListener('click', () => {
    larger = !larger;
    applySize();
    try { localStorage.setItem('onconova-large-text', String(larger)); } catch { /* Reading remains available. */ }
  });
}
function openSource() {
  if (!location.hash.startsWith('#fuente-')) return;
  const source = document.getElementById(location.hash.slice(1));
  if (source?.closest('details')) source.closest('details').open = true;
  if (source) requestAnimationFrame(() => source.scrollIntoView({ block: 'start' }));
}
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#fuente-"]');
  const source = link && document.getElementById(link.hash.slice(1));
  if (source?.closest('details')) source.closest('details').open = true;
});
window.addEventListener('hashchange', openSource);
openSource();

// Optional, one-time entrances. Reading and interaction never depend on motion.
function initScrollMotion() {
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (preference.matches || location.hash || !('IntersectionObserver' in window)) return;

  const targets = [...document.querySelectorAll('[data-scroll-motion]')];
  if (!targets.length) return;

  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('motion-play');
      observer.unobserve(entry.target);
    }
  }, { rootMargin: '0px 0px -32px 0px', threshold: 0 });

  // Leave the initial viewport still, including restored scroll positions.
  const belowViewport = targets.filter(target => target.getBoundingClientRect().top >= window.innerHeight);
  belowViewport.forEach(target => observer.observe(target));

  // Keyboard navigation, anchors and preference changes settle immediately.
  // Once stopped, this visit stays still rather than replaying earlier entrances.
  const stop = () => {
    observer.disconnect();
    targets.forEach(target => target.classList.remove('motion-play'));
    document.removeEventListener('keydown', onKeydown);
    document.removeEventListener('click', onAnchor);
    window.removeEventListener('hashchange', stop);
    window.removeEventListener('beforeprint', stop);
    preference.removeEventListener('change', stop);
  };
  const onKeydown = event => {
    if (['Tab', 'Home', 'End', 'PageUp', 'PageDown', 'ArrowUp', 'ArrowDown', ' '].includes(event.key)) stop();
  };
  const onAnchor = event => {
    if (event.target.closest('a[href^="#"]')) stop();
  };
  document.addEventListener('keydown', onKeydown);
  document.addEventListener('click', onAnchor);
  window.addEventListener('hashchange', stop);
  window.addEventListener('beforeprint', stop);
  preference.addEventListener('change', stop);
}
initScrollMotion();
