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
