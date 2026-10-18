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

// One shared surface, three reading chapters. Scroll never gets cancelled or set
// by an automatic chapter change. Cached ranges allow tall chapters to be read
// to the end before the next one enters at the top of the reading area.
function initReadingGuide() {
  const guide = document.querySelector('[data-reading-guide]');
  if (!guide || !('IntersectionObserver' in window) || !('ResizeObserver' in window)) return;
  const stages = [...guide.querySelectorAll('[data-reading-stage]')];
  const ids = stages.map(stage => stage.id);
  const links = [...guide.querySelectorAll('.reading-guide a')];
  const track = guide.querySelector('.reading-stages');
  const panel = guide.querySelector('.reading-panel');
  const actions = guide.querySelector('.reading-actions');
  const prev = actions.querySelector('[data-reading-prev]');
  const next = actions.querySelector('[data-reading-next]');
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = Math.max(0, ids.indexOf(location.hash.slice(1)));
  let destination = current;
  let offsets = [0, 0, 0];
  let origin = 0;
  let clearance = 0;
  let geometryTask = 0;
  let scrollTask = 0;
  let generation = 0;
  let phaseTimer = 0;
  let phaseFrame = 0;
  let allowMotion = false;
  let pointer = null;
  let printing = false;
  let pendingNavigation = null;

  const resetMotion = () => {
    generation++;
    clearTimeout(phaseTimer);
    cancelAnimationFrame(phaseFrame);
    panel.removeAttribute('data-phase');
    panel.style.transform = '';
    panel.style.opacity = '';
    stages.forEach(stage => { stage.inert = false; });
  };
  const render = index => {
    current = index;
    stages.forEach((stage, i) => { stage.hidden = i !== index; });
    links.forEach((link, i) => {
      if (i === index) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    });
    prev.disabled = index === 0;
    next.disabled = index === stages.length - 1;
    panel.style.top = `${offsets[index]}px`;
  };
  const reveal = (index, focus) => {
    // Only deliberate navigation follows an anchor. Automatic scrolling never
    // calls this function, changes the hash, or relocates the user's focus.
    window.scrollTo({ top: origin + offsets[index] - clearance, behavior: 'instant' });
    if (focus) stages[index].focus({ preventScroll: true });
  };
  const select = (index, { motion = false, follow = false, focus = false } = {}) => {
    if (index < 0 || index >= stages.length) return;
    const interrupted = panel.hasAttribute('data-phase');
    const direction = Math.sign(index - current) || Math.sign(index - destination) || 1;
    // Move focus to a persistent title before hiding the departing chapter.
    if (panel.contains(document.activeElement)) links[index].focus({ preventScroll: true });
    destination = index;
    resetMotion();
    pendingNavigation = { follow, focus };
    const finish = () => {
      render(index);
      if (follow) reveal(index, focus);
    };
    if (!motion || preference.matches || interrupted || index === current) {
      finish();
      return;
    }
    const token = generation;
    // Keep shared controls and swipe recognition available during the exit.
    stages[current].inert = true;
    panel.dataset.phase = 'exit';
    panel.style.transform = `translateX(${direction * 24}px)`;
    panel.style.opacity = '0';
    phaseTimer = setTimeout(() => {
      if (token !== generation) return;
      panel.removeAttribute('data-phase');
      finish();
      panel.style.transform = `translateX(${-direction * 24}px)`;
      // Flush only at the phase boundary, not during scrolling or per frame.
      panel.getBoundingClientRect();
      phaseFrame = requestAnimationFrame(() => {
        if (token !== generation) return;
        panel.dataset.phase = 'enter';
        panel.style.transform = 'translateX(0)';
        panel.style.opacity = '1';
        // Focus is placed once the arriving chapter is no longer inert.
        stages[index].inert = false;
        if (focus) stages[index].focus({ preventScroll: true });
        phaseTimer = setTimeout(() => {
          if (token === generation) {
            resetMotion();
            scheduleScroll();
          }
        }, 150);
      });
    }, 100);
  };
  const syncScroll = () => {
    scrollTask = 0;
    if (printing || panel.hasAttribute('data-phase') || panel.contains(document.activeElement) ||
        (window.getSelection()?.toString() && panel.contains(window.getSelection().anchorNode))) return;
    const position = window.scrollY + clearance - origin;
    let index = 0;
    offsets.forEach((offset, i) => { if (position + 1 >= offset) index = i; });
    if (index !== current) select(index, { motion: allowMotion });
  };
  const scheduleScroll = () => {
    if (!scrollTask) scrollTask = requestAnimationFrame(syncScroll);
  };
  const layout = () => {
    geometryTask = 0;
    if (printing) return;
    const focused = document.activeElement;
    const wasNavigating = panel.hasAttribute('data-phase') && pendingNavigation?.follow;
    resetMotion();
    const nav = guide.querySelector('.reading-guide');
    const header = document.querySelector('.site-header');
    const navStyle = getComputedStyle(nav);
    const globalIndex = document.querySelector('.section-index');
    const headerHeight = header && getComputedStyle(header).position === 'sticky' ? header.offsetHeight : 0;
    const indexHeight = globalIndex && getComputedStyle(globalIndex).position === 'sticky' ? globalIndex.offsetHeight : 0;
    clearance = headerHeight + indexHeight + 24;
    if (navStyle.position === 'sticky' && window.innerWidth <= 720) {
      clearance = Math.max(clearance, parseFloat(navStyle.top) + nav.offsetHeight + 24);
    }
    panel.style.setProperty('--reading-clearance', `${clearance}px`);
    // Measure at the actual content width, with all inactive chapters remaining
    // visually hidden and outside the accessibility tree. No cloned text/IDs.
    panel.classList.add('reading-measure');
    const style = getComputedStyle(panel);
    const chrome = parseFloat(style.paddingTop) + parseFloat(style.paddingBottom) + 2 + actions.offsetHeight + 28;
    const heights = stages.map(stage => stage.offsetHeight + chrome);
    panel.classList.remove('reading-measure');
    const viewport = Math.max(160, window.innerHeight - clearance - 24);
    offsets = [0];
    // The 96px reading margin leaves the end visible before advancing. Short
    // chapters also require a deliberate amount of native scroll to advance.
    heights.slice(0, -1).forEach((height, i) => offsets.push(offsets[i] + Math.max(96, height - viewport + 96)));
    track.style.height = `${Math.max(...heights.map((height, i) => height + offsets[i]))}px`;
    origin = track.getBoundingClientRect().top + window.scrollY;
    render(destination);
    if (wasNavigating) reveal(destination, pendingNavigation.focus);
    if (focused && panel.contains(focused)) focused.focus({ preventScroll: true });
  };
  const scheduleLayout = () => {
    if (!geometryTask) geometryTask = requestAnimationFrame(layout);
  };
  const navigate = (index, keyboard = false, updateHash = true) => {
    if (index < 0 || index >= stages.length) return;
    if (updateHash && location.hash !== '#' + ids[index]) history.pushState(null, '', '#' + ids[index]);
    select(index, { motion: !keyboard, follow: true, focus: keyboard });
  };
  const stopMotion = () => {
    allowMotion = false;
    if (panel.hasAttribute('data-phase')) select(destination, pendingNavigation || {});
  };
  guide.classList.add('reading-enhanced');
  actions.hidden = false;
  guide.querySelector('.reading-hint').hidden = false;
  layout();

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    const index = link ? ids.indexOf(link.hash.slice(1)) : -1;
    if (index === -1 || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    navigate(index, event.detail === 0);
  });
  prev.addEventListener('click', event => navigate(destination - 1, event.detail === 0));
  next.addEventListener('click', event => navigate(destination + 1, event.detail === 0));
  const onHash = () => {
    const index = ids.indexOf(location.hash.slice(1));
    if (index !== -1) navigate(index, true, false);
  };
  window.addEventListener('hashchange', onHash);
  if (ids.includes(location.hash.slice(1))) requestAnimationFrame(onHash);
  window.addEventListener('load', () => {
    layout();
    if (ids.includes(location.hash.slice(1))) onHash();
  }, { once: true });

  document.addEventListener('keydown', stopMotion);
  document.addEventListener('wheel', () => { allowMotion = true; }, { passive: true });
  document.addEventListener('pointerdown', () => { allowMotion = true; }, { passive: true });
  window.addEventListener('scroll', scheduleScroll, { passive: true });
  window.addEventListener('resize', scheduleLayout, { passive: true });
  preference.addEventListener('change', stopMotion);
  // Track content width and reading preferences, not the height we assign.
  let lastWidth = track.clientWidth;
  new ResizeObserver(() => {
    if (track.clientWidth !== lastWidth) {
      lastWidth = track.clientWidth;
      scheduleLayout();
    }
  }).observe(track);
  // The demonstration above can change height after this module initializes,
  // or when a visitor uses it. Keep the cached document origin in sync too.
  new ResizeObserver(scheduleLayout).observe(document.body);
  new MutationObserver(scheduleLayout).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  document.fonts?.ready.then(scheduleLayout);

  panel.addEventListener('pointerdown', event => {
    pointer = null;
    if (!event.isPrimary || event.pointerType !== 'touch' || event.target.closest('a,button,input,select,textarea') || window.getSelection()?.toString()) return;
    pointer = { id: event.pointerId, x: event.clientX, y: event.clientY };
  });
  panel.addEventListener('pointerup', event => {
    const start = pointer;
    pointer = null;
    if (!start || event.pointerId !== start.id || window.getSelection()?.toString()) return;
    const dx = event.clientX - start.x;
    const dy = event.clientY - start.y;
    if (Math.abs(dx) >= 48 && Math.abs(dx) >= Math.abs(dy) * 1.5) navigate(destination + (dx > 0 ? 1 : -1));
  });
  panel.addEventListener('pointercancel', () => { pointer = null; });
  window.addEventListener('beforeprint', () => { printing = true; stopMotion(); });
  window.addEventListener('afterprint', () => { printing = false; scheduleLayout(); });
}
initReadingGuide();
