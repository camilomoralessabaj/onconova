#!/usr/bin/env python3
"""Local interaction checks for step entry motion. Requires Playwright/Chromium."""
import argparse
import json
import shutil
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='http://127.0.0.1:4173')
parser.add_argument('--output', type=Path, default=Path('work/qa-step-motion'))
args = parser.parse_args()
url = urlsplit(args.base_url)
if (url.scheme not in ('http', 'https') or url.hostname not in ('127.0.0.1', 'localhost', '::1')
        or url.username or url.password or url.query or url.fragment):
    parser.error('Use a local test server URL without credentials, query or fragment')
OUT = args.output
OUT.mkdir(parents=True, exist_ok=True)
BASE = args.base_url.rstrip('/')
results = []

OBSERVER = """() => {
  window.motionQA = [];
  const record = () => {
    const screens = [...document.querySelectorAll('[data-screen]:not([hidden])')];
    const el = screens[0];
    const animations = el.getAnimations().map(animation => ({
      timing: animation.effect.getTiming(),
      frames: animation.effect.getKeyframes(),
      property: animation.transitionProperty
    }));
    motionQA.push({screen: el.dataset.screen, count: screens.length,
      focused: document.activeElement === el.querySelector('h3'), animations});
  };
  document.addEventListener('submit', record);
  document.addEventListener('click', event => {
    if (event.target.closest('[data-action]')) record();
  });
}"""

def check(condition, message):
    assert condition, message

def snapshot(page, screen, animated, focused=True):
    data = page.evaluate('motionQA.at(-1)')
    check(data['screen'] == screen and data['count'] == 1, f'Wrong active screen: {data}')
    if focused:
        check(data['focused'], f'Heading not focused immediately: {data}')
    animations = data['animations']
    check(len(animations) == int(animated), f'Unexpected animation: {data}')
    if animated:
        animation = animations[0]
        check(animation['property'] == 'opacity', f'Unexpected property: {animation}')
        check(animation['timing']['duration'] == 150, f'Wrong duration: {animation}')
        check(animation['timing']['easing'] == 'cubic-bezier(0.23, 1, 0.32, 1)', f'Wrong easing: {animation}')
        check(animation['frames'][0]['opacity'] == '0' and animation['frames'][-1]['opacity'] == '1', f'Wrong opacity endpoints: {animation}')
    return data

def settled(page):
    page.wait_for_function("[...document.querySelectorAll('[data-screen]:not([hidden])')].every(el => el.getAnimations().length === 0 && getComputedStyle(el).opacity === '1')")

def fits(page):
    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Horizontal overflow')

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    browser_version = browser.version
    for route in ('/', '/prototipo/'):
        for width in (1440, 390, 320):
            for reduced in (False, True):
                context = browser.new_context(viewport={'width': width, 'height': 900},
                    has_touch=width < 500, is_mobile=width < 500,
                    reduced_motion='reduce' if reduced else 'no-preference')
                page = context.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
                page.on('response', lambda response: errors.append(f'HTTP {response.status}') if response.status >= 400 else None)
                check(page.goto(BASE+route).status == 200, 'Page failed')
                page.evaluate(OBSERVER)
                settled(page)
                check(page.locator('[data-screen]:not([hidden])').get_attribute('data-screen') == 'start', 'Initial state')
                check(page.locator('[data-step-entry]').count() == 0, 'Initial animation')
                def activate(locator):
                    if width < 500: locator.tap()
                    else: locator.click()
                request = page.get_by_role('button', name='Simular mi solicitud')
                activate(request)
                check(page.locator('[data-screen="start"]').is_visible(), 'Consent bypass')
                page.locator('[name="demo-consent"]').check()
                activate(request)
                event = snapshot(page, 'message', not reduced)
                # Tab must immediately cancel any entry, while preserving native focus navigation.
                page.keyboard.press('Tab')
                check(page.evaluate("document.querySelector('[data-screen=message]').getAnimations().length") == 0, 'Tab did not cancel entry')
                check(page.locator('[data-screen="message"]').evaluate("el => getComputedStyle(el).opacity === '1'"), 'Transparent keyboard content')
                check(page.evaluate('document.activeElement.matches("[data-action=schedules]")'), 'Tab order changed')
                page.get_by_role('button', name='Ver horarios de ejemplo').press('Enter')
                snapshot(page, 'schedule', False)
                activate(page.get_by_role('button', name='Confirmar hora de ejemplo'))
                snapshot(page, 'schedule', False, focused=False)
                check(page.locator('[data-slot-error]').is_visible(), 'Missing slot error')
                check(page.locator('[name=slot]').first.evaluate('el => el === document.activeElement'), 'Slot error focus')
                page.locator('[name=slot]').first.check()
                activate(page.get_by_role('button', name='Confirmar hora de ejemplo'))
                snapshot(page, 'confirmed', not reduced)
                check(page.locator('.booking-progress [aria-current=step]').get_attribute('data-progress') == '3', 'Progress delayed')
                activate(page.get_by_role('button', name='Cambiar horario', exact=True))
                snapshot(page, 'schedule', not reduced)
                activate(page.get_by_role('button', name='Ninguno me acomoda', exact=True))
                snapshot(page, 'waiting', not reduced)
                settled(page)
                activate(page.get_by_role('button', name='Simular solicitud de otro horario'))
                snapshot(page, 'waiting', False, focused=False)
                check(page.locator('[data-wait-result]').is_visible(), 'Waiting result missing')
                activate(page.get_by_role('button', name='Volver a los horarios de ejemplo'))
                snapshot(page, 'schedule', not reduced)
                activate(page.get_by_role('button', name='Volver al mensaje'))
                snapshot(page, 'message', not reduced)
                activate(page.get_by_role('button', name='Cambiar preferencias'))
                snapshot(page, 'start', not reduced)
                # Keyboard submit must remain instant after an actual pointer interaction.
                page.get_by_role('button', name='Simular mi solicitud').press('Enter')
                snapshot(page, 'message', False)
                activate(page.get_by_role('button', name='Volver a empezar', exact=True))
                snapshot(page, 'start', not reduced)
                for decision in ('Prefiero pensarlo', 'Ahora no lo necesito'):
                    activate(page.get_by_role('button', name=decision, exact=True))
                    snapshot(page, 'paused', not reduced)
                    activate(page.get_by_role('button', name='Volver al inicio de la demostración'))
                    snapshot(page, 'start', not reduced)
                # Space, synthesized clicks and programmatic submits have no pointer entry.
                page.get_by_role('button', name='Prefiero pensarlo').press('Space')
                snapshot(page, 'paused', False)
                page.get_by_role('button', name='Volver al inicio de la demostración').dispatch_event('click', {'detail': 1})
                snapshot(page, 'start', False)
                page.locator('[name="demo-consent"]').check()
                page.evaluate("document.querySelector('[data-request-form]').requestSubmit(document.querySelector('[data-request-form] button[type=submit]'))")
                snapshot(page, 'message', False)
                # Repeated direct transitions must not leave hidden animations or old screens active.
                for _ in range(3):
                    activate(page.get_by_role('button', name='Cambiar preferencias'))
                    snapshot(page, 'start', not reduced)
                    activate(page.get_by_role('button', name='Simular mi solicitud'))
                    snapshot(page, 'message', not reduced)
                if not reduced:
                    page.emulate_media(reduced_motion='reduce')
                    settled(page)
                    check(page.locator('[data-screen="message"]').evaluate('el => el.getAnimations().length') == 0, 'Live reduced motion failed')
                    page.emulate_media(reduced_motion='no-preference')
                settled(page)
                page.locator('.text-size').click()
                fits(page)
                activate(page.get_by_role('button', name='Ver horarios de ejemplo'))
                snapshot(page, 'schedule', not reduced)
                settled(page)
                fits(page)
                key = f'{route.strip("/") or "home"}-{width}-{"reduce" if reduced else "normal"}'
                if not reduced and width in (1440, 390):
                    page.screenshot(path=str(OUT/f'{key}.png'))
                check(not errors, '; '.join(errors))
                results.append({'route':route,'width':width,'reduced_motion':reduced,'status':'passed','events':len(page.evaluate('motionQA')),'sample':event})
                context.close()
    # Old-browser fallback: an ignored starting-style rule leaves the screen visible.
    context = browser.new_context(reduced_motion='no-preference')
    page = context.new_page()
    css = Path('site/assets/prototype.css').read_text().replace('@starting-style', '@unsupported-starting-style')
    page.route('**/assets/prototype.css', lambda route: route.fulfill(body=css, content_type='text/css'))
    page.goto(BASE+'/prototipo/')
    page.evaluate(OBSERVER)
    page.locator('[name=demo-consent]').check()
    page.get_by_role('button', name='Simular mi solicitud').click()
    snapshot(page, 'message', False)
    settled(page)
    results.append({'case':'unsupported-starting-style','status':'passed'})
    browser.close()

(OUT/'report.json').write_text(json.dumps({'browser':f'Chromium {browser_version}','cases':results}, ensure_ascii=False, indent=2))
print(f'{len(results)} casos aprobados, escritorio, toque emulado, teclado, movimiento reducido e interrupciones.')
