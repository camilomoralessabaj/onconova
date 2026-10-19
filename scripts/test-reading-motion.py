#!/usr/bin/env python3
"""Check visible continuity at reading milestones, not just final card selection.

Requires local Playwright/Chromium. Outputs measurements only; no dependencies
are added to the site. Run alongside test-reading-guide.py for the full journey.
"""
import argparse
import json
import shutil
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='http://127.0.0.1:4173')
parser.add_argument('--output', type=Path, default=Path('work/qa-reading-motion'))
args = parser.parse_args()
url = urlsplit(args.base_url)
if (url.scheme not in ('http', 'https') or url.hostname not in ('127.0.0.1', 'localhost', '::1')
        or url.username or url.password or url.query or url.fragment):
    parser.error('Use a local test server URL without credentials, query or fragment')
args.output.mkdir(parents=True, exist_ok=True)
results = []


def settled(page):
    page.wait_for_function('''() => {
      const panel = document.querySelector('.reading-panel');
      return panel.getAnimations({subtree:true}).length === 0;
    }''')


def choose(page, index):
    page.locator('[data-reading-select]').nth(index).click()
    settled(page)


def cross(page, target):
    # Observe the first committed visual state in the same frame as the card
    # change. Subtract native scrolling: only the layout jump must be bridged.
    return page.evaluate('''target => new Promise(resolve => {
      const panel = document.querySelector('.reading-panel');
      let start = panel.getBoundingClientRect().top;
      let scroll = scrollY;
      // Read again in the upcoming animation frame, before the scroll render:
      // an in-flight transition may legitimately advance while input is queued.
      requestAnimationFrame(() => {
        start = panel.getBoundingClientRect().top;
        scroll = scrollY;
      });
      const observer = new MutationObserver(() => {
        observer.disconnect();
        const content = panel.querySelector('[data-reading-stage]:not([hidden])');
        resolve({
          expected: start - (scrollY - scroll), actual: panel.getBoundingClientRect().top,
          scroll: scrollY, target, selected: content.id,
          panelAnimations: panel.getAnimations().length,
          contentAnimations: content.getAnimations().map(a => a.transitionProperty)
        });
      });
      observer.observe(panel, {subtree:true, attributes:true, attributeFilter:['data-depth']});
      document.dispatchEvent(new WheelEvent('wheel', {deltaY:target-scroll}));
      scrollTo({top:target, behavior:'instant'});
    })''', target)


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    for width in (1440, 390):
        for reduced in (False, True):
            context = browser.new_context(viewport={'width':width, 'height':900 if width == 1440 else 800},
                reduced_motion='reduce' if reduced else 'no-preference', is_mobile=width < 500, has_touch=width < 500)
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
            page.goto(args.base_url.rstrip('/') + '/#lectura-aprendizajes', wait_until='networkidle')
            choose(page, 1)
            boundary = page.evaluate('scrollY')
            choose(page, 0)
            page.evaluate('y => scrollTo({top:y, behavior:"instant"})', boundary - 8)
            page.wait_for_timeout(50)
            forward = cross(page, boundary + 4)
            assert forward['selected'] == 'lectura-brechas', forward
            assert abs(forward['scroll'] - forward['target']) < 1, forward
            if reduced:
                assert not forward['panelAnimations'] and not forward['contentAnimations'], forward
            else:
                assert forward['panelAnimations'] == 1, forward
                assert abs(forward['actual'] - forward['expected']) < 2, forward
                assert set(forward['contentAnimations']) == {'opacity', 'transform'}, forward
            # Reverse while the panel is still moving. The first frame must use
            # its current presentation position instead of restarting at rest.
            page.wait_for_timeout(75)
            backward = cross(page, boundary - 8)
            assert backward['selected'] == 'lectura-aprendizajes', backward
            if not reduced:
                assert backward['panelAnimations'] == 1, backward
                assert abs(backward['actual'] - backward['expected']) < 2, backward
            settled(page)
            assert abs(page.evaluate('scrollY') - (boundary - 8)) < 1, 'Animation moved document scroll'
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Overflow'
            # Direct selection at a canonical stop must also reveal the body
            # progressively, while leaving document/selection in agreement.
            choose(page, 0)
            direct = page.locator('[data-reading-select]').nth(2).evaluate('''button => {
              const panel = button.closest('.reading-panel');
              const before = panel.getBoundingClientRect().top;
              button.dispatchEvent(new MouseEvent('click', {bubbles:true, detail:1}));
              const content = document.getElementById('proximos-pasos');
              return {before, after:panel.getBoundingClientRect().top,
                opacity:getComputedStyle(content).opacity,
                properties:content.getAnimations().map(a => a.transitionProperty)};
            }''')
            assert abs(direct['before'] - direct['after']) < 2, direct
            if reduced:
                assert direct['opacity'] == '1' and not direct['properties'], direct
            else:
                assert float(direct['opacity']) < .1 and set(direct['properties']) == {'opacity', 'transform'}, direct
            # Keyboard input cancels both the deck displacement and text entry.
            page.keyboard.press('Tab')
            assert page.locator('.reading-panel').evaluate('e => e.getAnimations({subtree:true}).length') == 0
            assert page.locator('#proximos-pasos').evaluate('e => getComputedStyle(e).opacity') == '1'
            if not reduced:
                choose(page, 0)
                page.evaluate('y => scrollTo({top:y, behavior:"instant"})', boundary - 8)
                page.wait_for_timeout(50)
                cross(page, boundary + 4)
                page.emulate_media(reduced_motion='reduce')
                settled(page)
                assert page.locator('.reading-panel').evaluate('e => getComputedStyle(e).transform') == 'none'
                page.emulate_media(reduced_motion='no-preference')
                cross(page, boundary - 8)
                # Reflow during a transition must clear all presentation offsets.
                page.set_viewport_size({'width':320, 'height':800})
                page.wait_for_function('!document.querySelector(".reading-enhanced")')
                settled(page)
                assert page.locator('[data-reading-stage]').evaluate_all('els => els.every(e => !e.hidden && !e.inert)')
                assert page.locator('.reading-panel').evaluate('e => getComputedStyle(e).transform') == 'none'
            assert not errors, errors
            result = {'width':width, 'reduced_motion':reduced, 'forward':forward,
                'interrupted_reverse':backward, 'direct':direct, 'status':'passed'}
            results.append(result)
            print(json.dumps({'width':width, 'reduced_motion':reduced, 'status':'passed'}), flush=True)
            context.close()
    # Starting-style is optional: content must remain visible if unsupported.
    context = browser.new_context()
    page = context.new_page()
    css = Path('site/assets/styles.css').read_text().replace('@starting-style', '@unsupported-starting-style')
    page.route('**/assets/styles.css', lambda route: route.fulfill(body=css, content_type='text/css'))
    page.goto(args.base_url.rstrip('/') + '/#lectura-aprendizajes', wait_until='networkidle')
    choose(page, 1)
    assert page.locator('#lectura-brechas').evaluate('e => getComputedStyle(e).opacity') == '1'
    results.append({'case':'unsupported starting-style', 'status':'passed'})
    browser.close()

(args.output / 'report.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
print(f'{len(results)} casos de continuidad aprobados.')
