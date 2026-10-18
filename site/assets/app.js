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

// Cache chapter boundaries on layout changes. Scroll reads only scrollY;
// it never measures boxes, rewrites history, moves focus or announces a section.
function initSectionIndex() {
  const index = document.querySelector('.section-index');
  if (!index) return;
  const root = document.documentElement;
  const header = document.querySelector('.site-header');
  const track = index.querySelector('.chapter-links');
  const links = [...track.querySelectorAll('a')];
  const sections = links.map(link => document.getElementById(link.hash.slice(1)));
  let boundaries = [];
  let readingLine = 0;
  let pageHeight = 0;
  let viewportHeight = 0;
  let current = -1;
  let layoutTask = 0;
  let scrollTask = 0;

  const showCurrentLink = () => {
    if (current < 0 || track.contains(document.activeElement)) return;
    const link = links[current];
    track.scrollLeft = link.offsetLeft - track.offsetLeft - (track.clientWidth - link.offsetWidth) / 2;
  };

  const sync = () => {
    scrollTask = 0;
    let next = 0;
    boundaries.forEach((top, i) => { if (top <= window.scrollY + readingLine + 1) next = i; });
    if (window.scrollY + viewportHeight >= pageHeight - 2) next = links.length - 1;
    if (next === current) return;
    current = next;
    links.forEach((link, i) => {
      if (i === next) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    // Only a chapter change reads the link's horizontal geometry. Scroll the
    // native strip itself; scrollIntoView would also move the reading page.
    showCurrentLink();
  };
  const layout = () => {
    layoutTask = 0;
    const headerHeight = getComputedStyle(header).position === 'sticky' ? header.offsetHeight : 0;
    const indexHeight = index.offsetHeight;
    viewportHeight = window.innerHeight;
    // Very short or heavily enlarged views keep the index in normal flow.
    const staticIndex = indexHeight > viewportHeight * .28;
    const nextReadingLine = headerHeight + (staticIndex ? 0 : indexHeight) + 24;
    boundaries = sections.map(section => section.getBoundingClientRect().top + window.scrollY);
    pageHeight = root.scrollHeight;
    readingLine = nextReadingLine;
    root.toggleAttribute('data-index-static', staticIndex);
    root.style.setProperty('--sticky-header-height', `${headerHeight}px`);
    root.style.setProperty('--sticky-index-height', `${staticIndex ? 0 : indexHeight}px`);
    sync();
  };
  const scheduleLayout = () => {
    if (!layoutTask) layoutTask = requestAnimationFrame(layout);
  };
  index.dataset.ready = 'true';
  root.setAttribute('data-section-navigation', '');
  window.addEventListener('scroll', () => {
    if (!scrollTask) scrollTask = requestAnimationFrame(sync);
  }, { passive: true });
  window.addEventListener('resize', scheduleLayout, { passive: true });
  window.addEventListener('hashchange', () => requestAnimationFrame(sync));
  window.addEventListener('pageshow', scheduleLayout);
  track.addEventListener('focusout', () => requestAnimationFrame(showCurrentLink));
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(scheduleLayout);
    [header, index, document.querySelector('main')].forEach(element => observer.observe(element));
  }
  layout();
  // Native anchor positioning can precede JS's measured offsets on first load.
  // Correct that destination once; later Back/Forward retain native restoration.
  if (location.hash) requestAnimationFrame(() => {
    document.getElementById(location.hash.slice(1))?.scrollIntoView({ block: 'start' });
  });
}
initSectionIndex();

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
    const header = document.querySelector('.site-header');
    const globalIndex = document.querySelector('.section-index');
    const nav = guide.querySelector('.reading-guide');
    const headerHeight = header && getComputedStyle(header).position === 'sticky' ? header.offsetHeight : 0;
    const globalHeight = globalIndex && getComputedStyle(globalIndex).position === 'sticky' ? globalIndex.offsetHeight : 0;
    const navHeight = window.innerWidth <= 720 && getComputedStyle(nav).position === 'sticky' ? nav.offsetHeight : 0;
    readingLine = Math.min(window.innerHeight - 1, Math.max(window.innerHeight * .35, headerHeight + globalHeight + navHeight + 24));
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
