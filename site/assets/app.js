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

// Fixed canonical milestones, independent of the deck's visual depth. Automatic
// changes only render: wheel/touch scrolling and document position stay native.
function initReadingGuide() {
  const guide = document.querySelector('[data-reading-guide]');
  if (!guide || !('IntersectionObserver' in window) || !('ResizeObserver' in window)) return;
  const stages = [...guide.querySelectorAll('[data-reading-stage]')];
  const cards = [...guide.querySelectorAll('[data-reading-card]')];
  const buttons = [...guide.querySelectorAll('[data-reading-select]')];
  const ids = stages.map(stage => stage.id);
  const track = guide.querySelector('.reading-stages');
  const panel = guide.querySelector('.reading-panel');
  const actions = guide.querySelector('.reading-actions');
  const prev = actions.querySelector('[data-reading-prev]');
  const next = actions.querySelector('[data-reading-next]');
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = Math.max(0, ids.indexOf(location.hash.slice(1)));
  let offsets = [];
  let heights = [];
  let origin = 0;
  let clearance = 0;
  let geometryTask = 0;
  let scrollTask = 0;
  let enhanced = false;
  let printing = false;
  let allowMotion = false;
  let tabNavigation = false;
  let pointer = null;
  let panelMotion = null;

  const settleMotion = () => {
    panelMotion?.cancel();
    panelMotion = null;
    panel.getAnimations({ subtree: true }).forEach(animation => animation.finish());
  };
  const render = (index, motion = false, follow = false, focus = false) => {
    const animate = motion && !preference.matches && index !== current;
    // Read the presentation position, including any interrupted movement, before
    // changing the canonical layout. This also accounts for native scrolling.
    const before = animate ? panel.getBoundingClientRect() : null;
    const direction = index > current ? 1 : -1;
    // A focused link must never become hidden/inert. The persistent card button
    // is a safe destination, also when native scrolling changes the chapter.
    if (index !== current && stages[current].contains(document.activeElement)) {
      buttons[index].focus({ preventScroll: true });
    }
    current = index;
    panel.dataset.direction = direction > 0 ? 'forward' : 'backward';
    const behind = cards.map((_, i) => i).filter(i => i !== index);
    cards.forEach((card, i) => {
      card.dataset.depth = String(i === index ? 2 : behind.indexOf(i));
      stages[i].hidden = i !== index;
      stages[i].inert = i !== index;
      buttons[i].setAttribute('aria-pressed', String(i === index));
      buttons[i].querySelector('.reading-card-state').textContent = i === index ? 'Leyendo' : 'Abrir';
    });
    prev.disabled = index === 0;
    next.disabled = index === stages.length - 1;
    panel.style.top = `${offsets[index]}px`;
    panel.style.setProperty('--reading-card-height', `${heights[index]}px`);
    actions.style.top = `${128 + heights[index] + 24}px`;
    panel.style.height = `${128 + heights[index] + 24 + actions.offsetHeight}px`;
    if (follow) reveal(index, focus);
    panelMotion?.cancel();
    panelMotion = null;
    if (animate) {
      const after = panel.getBoundingClientRect();
      const delta = before.top - after.top;
      // FLIP bridges the layout jump with a compositor transform. A deliberate
      // selection rebases document scroll first, so the two offsets cancel.
      // Only animate a deck that was on screen; distant anchors land directly.
      if (Math.abs(delta) > 1 && before.bottom > clearance && before.top < innerHeight) {
        const styles = getComputedStyle(panel);
        const animation = panel.animate([
          { transform: `translateY(${delta}px)` },
          { transform: 'translateY(0)' }
        ], {
          duration: parseFloat(styles.getPropertyValue('--motion-story')),
          easing: styles.getPropertyValue('--ease-out').trim()
        });
        panelMotion = animation;
        animation.onfinish = () => {
          if (panelMotion === animation) panelMotion = null;
        };
      }
    }
    // CSS transitions retarget from their current presentation value, with no
    // queues, timers or disabled controls. Keyboard and reduced motion settle.
    if (!animate) settleMotion();
  };
  const reveal = (index, focus) => {
    window.scrollTo({ top: origin + offsets[index] - clearance, behavior: 'instant' });
    if (focus) stages[index].focus({ preventScroll: true });
  };
  const navigate = (index, keyboard = false, updateHash = true) => {
    if (index < 0 || index >= stages.length) return;
    if (updateHash && location.hash !== '#' + ids[index]) history.pushState(null, '', '#' + ids[index]);
    if (enhanced) {
      // This explicit selection moves the document to the same canonical stop
      // that scroll uses. The next wheel event cannot restore the previous card.
      render(index, !keyboard, true, keyboard);
    } else {
      current = index;
      stages[index].scrollIntoView({ block: 'start', behavior: 'instant' });
      if (keyboard) stages[index].focus({ preventScroll: true });
    }
  };
  const syncScroll = () => {
    scrollTask = 0;
    if (!enhanced || printing || (tabNavigation && panel.contains(document.activeElement))) return;
    const selection = window.getSelection();
    if (selection?.toString() && panel.contains(selection.anchorNode)) return;
    const position = window.scrollY + clearance - origin;
    let index = 0;
    offsets.forEach((offset, i) => { if (position + 1 >= offset) index = i; });
    if (index !== current) render(index, allowMotion);
  };
  const scheduleScroll = () => {
    if (!scrollTask) scrollTask = requestAnimationFrame(syncScroll);
  };
  const layout = () => {
    geometryTask = 0;
    if (printing) return;
    const wasEnhanced = enhanced;
    const focused = document.activeElement;
    const header = document.querySelector('.site-header');
    const globalIndex = document.querySelector('.section-index');
    const headerHeight = header && getComputedStyle(header).position === 'sticky' ? header.offsetHeight : 0;
    const indexHeight = globalIndex && getComputedStyle(globalIndex).position === 'sticky' ? globalIndex.offsetHeight : 0;
    clearance = headerHeight + indexHeight + 24;
    const viewport = window.innerHeight - clearance - 24;
    // Reflow takes priority over the metaphor when type or viewport leave too
    // little space. All content and native anchor links then return to flow.
    enhanced = window.innerWidth >= 360 && parseFloat(getComputedStyle(document.documentElement).fontSize) <= 18 && viewport >= 360;
    guide.classList.toggle('reading-enhanced', enhanced);
    guide.querySelector('.reading-hint').hidden = !enhanced;
    actions.hidden = !enhanced;
    buttons.forEach(button => { button.hidden = !enhanced; });
    if (!enhanced) {
      settleMotion();
      stages.forEach(stage => { stage.hidden = false; stage.inert = false; });
      if (buttons.includes(focused) || actions.contains(focused)) stages[current].focus({ preventScroll: true });
      cards.forEach(card => card.removeAttribute('data-depth'));
      track.style.height = '';
      panel.style.height = '';
      panel.style.top = '';
      if (wasEnhanced) stages[current].scrollIntoView({ block: 'start', behavior: 'instant' });
      return;
    }
    // Measure the actual nodes, including the planning table, at their final
    // width. Hidden content remains invisible and inaccessible during layout.
    panel.classList.add('reading-measure');
    heights = cards.map(card => card.offsetHeight);
    panel.classList.remove('reading-measure');
    offsets = [0];
    // Include exposed tabs and footer controls. A 96px margin shows the whole
    // end before the next card arrives, even when a card exceeds the viewport.
    const totals = heights.map(height => 128 + height + 24 + actions.offsetHeight);
    totals.slice(0, -1).forEach((height, i) => offsets.push(offsets[i] + Math.max(96, height - viewport + 96)));
    track.style.height = `${Math.max(...totals.map((height, i) => height + offsets[i]))}px`;
    origin = track.getBoundingClientRect().top + window.scrollY;
    render(current);
    // Keep a deliberate reading selection when returning from linear mode.
    if (!wasEnhanced && ids.includes(location.hash.slice(1))) reveal(current, false);
  };
  const scheduleLayout = () => {
    if (!geometryTask) geometryTask = requestAnimationFrame(layout);
  };
  const onHash = () => {
    const index = ids.indexOf(location.hash.slice(1));
    if (index !== -1) navigate(index, true, false);
  };
  layout();
  buttons.forEach((button, index) => button.addEventListener('click', event => navigate(index, event.detail === 0)));
  prev.addEventListener('click', event => navigate(current - 1, event.detail === 0));
  next.addEventListener('click', event => navigate(current + 1, event.detail === 0));
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    const index = link ? ids.indexOf(link.hash.slice(1)) : -1;
    if (index === -1 || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    navigate(index, event.detail === 0);
  });
  window.addEventListener('hashchange', onHash);
  if (ids.includes(location.hash.slice(1))) requestAnimationFrame(onHash);
  window.addEventListener('load', () => {
    layout();
    if (ids.includes(location.hash.slice(1))) onHash();
  }, { once: true });
  document.addEventListener('keydown', event => {
    allowMotion = false;
    // Tab's native focus reveal must not switch/hide the content being visited.
    // Wheel, vertical touch and keyboard scrolling resume canonical milestones.
    tabNavigation = event.key === 'Tab';
    settleMotion();
  });
  document.addEventListener('wheel', () => { allowMotion = true; tabNavigation = false; }, { passive: true });
  document.addEventListener('pointerdown', () => { allowMotion = true; tabNavigation = false; }, { passive: true });
  panel.addEventListener('focusin', () => {
    if (!tabNavigation) return;
    requestAnimationFrame(() => {
      const focused = document.activeElement;
      if (!enhanced || !panel.contains(focused)) return;
      const rect = focused.getBoundingClientRect();
      // Rotated background titles can project a few pixels above the browser's
      // native focus box. Keep the entire visible ring below the global index.
      if (rect.top < clearance) window.scrollBy({ top: rect.top - clearance, behavior: 'instant' });
      else if (rect.bottom > innerHeight - 8) window.scrollBy({ top: rect.bottom - innerHeight + 8, behavior: 'instant' });
    });
  });
  panel.addEventListener('focusout', scheduleScroll);
  window.addEventListener('scroll', scheduleScroll, { passive: true });
  window.addEventListener('resize', scheduleLayout, { passive: true });
  preference.addEventListener('change', settleMotion);
  let lastWidth = track.clientWidth;
  new ResizeObserver(() => {
    if (track.clientWidth !== lastWidth) {
      lastWidth = track.clientWidth;
      scheduleLayout();
    }
  }).observe(track);
  new ResizeObserver(scheduleLayout).observe(document.body);
  new MutationObserver(scheduleLayout).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  document.fonts?.ready.then(scheduleLayout);
  // Preserve the existing optional horizontal touch shortcut without cancelling
  // pointer events: vertical pans, text selection and pinch zoom stay native.
  panel.addEventListener('pointerdown', event => {
    pointer = null;
    if (!enhanced || !event.isPrimary || event.pointerType !== 'touch' || event.target.closest('a,button,input,select,textarea') || window.getSelection()?.toString()) return;
    pointer = { id: event.pointerId, x: event.clientX, y: event.clientY };
  });
  panel.addEventListener('pointerup', event => {
    const start = pointer;
    pointer = null;
    if (!enhanced || !start || event.pointerId !== start.id || window.getSelection()?.toString()) return;
    const dx = event.clientX - start.x;
    const dy = event.clientY - start.y;
    if (Math.abs(dx) >= 48 && Math.abs(dx) >= Math.abs(dy) * 1.5) navigate(current + (dx > 0 ? 1 : -1));
  });
  panel.addEventListener('pointercancel', () => { pointer = null; });
  window.addEventListener('beforeprint', () => { printing = true; settleMotion(); });
  window.addEventListener('afterprint', () => { printing = false; scheduleLayout(); });
}
initReadingGuide();
