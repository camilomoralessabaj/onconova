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

// A single shared frame follows the reading position; links remain native anchors.
function initReadingGuide() {
  const guide = document.querySelector('[data-reading-guide]');
  if (!guide || !('IntersectionObserver' in window)) return;
  const stages = [...guide.querySelectorAll('[data-reading-stage]')];
  const track = guide.querySelector('.reading-guide-track');
  const links = [...track.querySelectorAll('a')];
  const frame = track.querySelector('.reading-frame');
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = -1;
  let allowMotion = false;
  let observer;
  let readingLine = 0;
  let resizeTask = 0;

  const select = (index, instant = false) => {
    if (current === index && !instant) return;
    current = index;
    const link = links[index];
    // Geometry is read only at a section boundary or resize, never per scroll frame.
    const { offsetLeft: x, offsetTop: y, offsetWidth: width, offsetHeight: height } = link;
    links.forEach((item, i) => {
      if (i === index) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
    });
    frame.classList.toggle('reading-frame-instant', instant || !allowMotion || preference.matches);
    frame.style.width = `${width}px`;
    frame.style.height = `${height}px`;
    frame.style.transform = `translate(${x}px, ${y}px)`;
    frame.hidden = false;
  };
  const sync = (instant = false) => {
    const tops = stages.map(stage => stage.getBoundingClientRect().top);
    let index = 0;
    tops.forEach((top, i) => { if (top <= readingLine + 1) index = i; });
    select(index, instant);
  };
  const layout = () => {
    resizeTask = 0;
    const headerHeight = document.querySelector('.site-header')?.offsetHeight || 0;
    const navHeight = window.innerWidth <= 720 ? guide.querySelector('.reading-guide').offsetHeight : 0;
    readingLine = Math.min(window.innerHeight - 1, Math.max(window.innerHeight * .35, headerHeight + navHeight + 24));
    observer?.disconnect();
    observer = new IntersectionObserver(() => sync(), {
      rootMargin: `-${readingLine}px 0px -${window.innerHeight - readingLine - 1}px 0px`,
      threshold: 0
    });
    stages.forEach(stage => observer.observe(stage));
    sync(true);
  };
  const scheduleLayout = () => {
    if (!resizeTask) resizeTask = requestAnimationFrame(layout);
  };
  const stopMotion = () => {
    allowMotion = false;
    frame.classList.add('reading-frame-instant');
  };
  const pointerInput = () => { allowMotion = true; };
  document.addEventListener('keydown', stopMotion);
  document.addEventListener('pointerdown', pointerInput, { passive: true });
  document.addEventListener('touchstart', pointerInput, { passive: true });
  document.addEventListener('wheel', pointerInput, { passive: true });
  track.addEventListener('click', event => {
    const index = links.indexOf(event.target.closest('a'));
    if (index !== -1) {
      allowMotion = event.detail > 0;
      select(index, !allowMotion);
    }
  });
  // Focus remains on the native link or target. No live announcements on scroll.
  preference.addEventListener('change', () => { stopMotion(); sync(true); });
  window.addEventListener('resize', scheduleLayout, { passive: true });
  window.addEventListener('hashchange', () => sync(!allowMotion));
  window.addEventListener('beforeprint', stopMotion);
  if ('ResizeObserver' in window) new ResizeObserver(scheduleLayout).observe(guide);
  layout();
}
initReadingGuide();
