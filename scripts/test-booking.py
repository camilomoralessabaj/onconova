#!/usr/bin/env python3
"""Local browser checks for the academic booking flow. Requires Playwright/Chromium."""
import argparse
import json
import shutil
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='http://127.0.0.1:4173')
parser.add_argument('--output', type=Path, default=Path('work/qa'))
parser.add_argument('--auxiliary-only', action='store_true', help='Repeat static/no-JS checks using an existing main-flow report')
args = parser.parse_args()
if urlparse(args.base_url).hostname not in ('127.0.0.1', 'localhost', '::1'):
    parser.error('Use a local test server')
args.output.mkdir(parents=True, exist_ok=True)
results = json.loads((args.output/'report.json').read_text()) if args.auxiliary_only else []

def check(condition, message):
    if not condition:
        raise AssertionError(message)

def fits(page):
    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Horizontal overflow')

def submit_request(page, channel='WhatsApp', modality='Videollamada'):
    page.locator(f'input[name="channel"][value="{channel}"]').check()
    page.locator(f'input[name="modality"][value="{modality}"]').check()
    page.locator('input[name="demo-consent"]').check()
    page.get_by_role('button', name='Simular mi solicitud', exact=False).click()
    check(page.locator('[data-screen="message"]').is_visible(), 'Message must follow request')
    check(channel in page.locator('[data-message-channel]').inner_text(), 'Wrong message channel')
    page.get_by_role('button', name='Ver horarios de ejemplo', exact=False).click()

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    for route in (() if args.auxiliary_only else ('/', '/prototipo/')):
        for width in (1440, 390, 320):
            context = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce', accept_downloads=True)
            page = context.new_page()
            errors = []
            requests = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
            page.on('response', lambda response: errors.append(f'HTTP {response.status} {response.url}') if response.status >= 400 else None)
            page.on('request', lambda request: requests.append((request.method, request.url)))
            try:
                response = page.goto(args.base_url.rstrip('/') + route, wait_until='networkidle')
                check(response.status == 200, 'Page failed')
                fits(page)
                check(page.locator('h1').count() == 1, 'Heading hierarchy')
                page.keyboard.press('Tab')
                check(page.locator('.skip-link').evaluate('(el) => el === document.activeElement'), 'Skip link must be first focus')
                page.keyboard.press('Enter')
                page.locator('.text-size').click()
                fits(page)
                check(page.locator('.text-size').get_attribute('aria-pressed') == 'true', 'Text resize')
                page.locator('.text-size').click()
                # Required acknowledgement blocks request.
                page.get_by_role('button', name='Simular mi solicitud', exact=False).click()
                check(page.locator('[data-screen="start"]').is_visible(), 'Consent bypass')
                # Postpone and decline never create requests.
                for label in ('Prefiero pensarlo', 'Ahora no lo necesito'):
                    page.get_by_role('button', name=label, exact=True).click()
                    check(page.locator('[data-screen="paused"]').is_visible(), 'Decision ignored')
                    page.get_by_role('button', name='Volver al inicio de la demostración').click()
                # All channel/modality combinations and download consistency.
                for channel in ('WhatsApp', 'Correo'):
                    for modality in ('Videollamada', 'Presencial'):
                        submit_request(page, channel, modality)
                        page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                        check(page.locator('[data-slot-error]').is_visible(), 'Missing selection error')
                        check(page.locator('input[name="slot"]').first.evaluate('(el) => el === document.activeElement'), 'Error focus')
                        page.locator('input[name="slot"]').nth(1).check()
                        page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                        check(page.locator('[data-screen="confirmed"]').is_visible(), 'Confirmation missing')
                        check(modality.lower() in page.locator('[data-appointment-modality]').inner_text().lower(), 'Modality mismatch')
                        check(channel in page.locator('[data-appointment-channel]').inner_text(), 'Channel mismatch')
                        fits(page)
                        with page.expect_download() as download:
                            page.get_by_role('button', name='Descargar comprobante de ejemplo').click()
                        file = args.output / 'comprobante-test.txt'
                        download.value.save_as(file)
                        text = file.read_text()
                        check('NO ES UNA RESERVA REAL' in text and modality in text and channel in text, 'Download mismatch')
                        # Changing slot removes prior confirmation.
                        page.get_by_role('button', name='Cambiar horario', exact=True).click()
                        check(page.locator('input[name="slot"]:checked').count() == 0, 'Stale slot after reschedule')
                        page.locator('input[name="slot"]').last.check()
                        page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                        page.get_by_role('button', name='Volver a empezar', exact=True).click()
                        check(not page.locator('input[name="demo-consent"]').is_checked(), 'Reset consent')
                # Unavailable branch: preferences must be explicitly registered again after edit.
                submit_request(page, 'Correo', 'Presencial')
                page.get_by_role('button', name='Ninguno me acomoda', exact=True).click()
                page.locator('input[value="la tarde"]').check()
                page.get_by_role('button', name='Simular solicitud de otro horario').click()
                check('la tarde' in page.locator('[data-wait-copy]').inner_text(), 'Waiting preference mismatch')
                check('Correo' in page.locator('[data-wait-copy]').inner_text(), 'Waiting channel mismatch')
                page.locator('input[value="la mañana"]').check()
                check(page.locator('[data-wait-result]').is_hidden(), 'Stale waiting result')
                page.get_by_role('button', name='Simular solicitud de otro horario').click()
                page.screenshot(path=str(args.output / f'waiting-{width}-{route.strip("/") or "home"}.png'), full_page=True)
                fits(page)
                # Reload clears the academic booking; only reading preference persists.
                page.reload(wait_until='networkidle')
                check(page.locator('[data-screen="start"]').is_visible(), 'Reload retains booking')
                check(page.evaluate('sessionStorage.length') == 0, 'Booking stored in session')
                check(page.evaluate('Object.keys(localStorage).every(k => k === "onconova-large-text")'), 'Unexpected local storage')
                check(all(method == 'GET' and url.startswith(args.base_url) for method, url in requests), 'External request or submission')
                page.screenshot(path=str(args.output / f'{route.strip("/") or "home"}-{width}.png'), full_page=True)
                # Text enlargement plus halved desktop viewport as reflow approximation.
                page.locator('.text-size').click()
                fits(page)
                if width == 1440:
                    page.set_viewport_size({'width':720,'height':900})
                    fits(page)
                check(not errors, '; '.join(errors))
                results.append({'route': route, 'width': width, 'status':'passed'})
            except Exception as error:
                page.screenshot(path=str(args.output / f'failure-{width}-{route.strip("/") or "home"}.png'), full_page=True)
                results.append({'route':route,'width':width,'status':'failed','error':str(error)})
            print(json.dumps(results[-1],ensure_ascii=False), flush=True)
            (args.output/'report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
            context.close()
    # No JS: clear simulation limitation and all static content remains readable.
    context = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':900})
    for route in ('/', '/prototipo/'):
        page = context.new_page()
        page.goto(args.base_url.rstrip('/')+route)
        page.screenshot(path=str(args.output / ('nojs-'+(route.strip('/') or 'home')+'.png')),full_page=True)
        check(page.locator('noscript h3').is_visible(), 'Missing noscript guidance')
        fits(page)
        page.close()
    results.append({'case':'no JavaScript, both routes','status':'passed'})
    context.close()
    # Source anchors open their containing details, including on direct page load.
    page=browser.new_page(viewport={'width':390,'height':900})
    page.goto(args.base_url.rstrip('/')+'/#fuente-S10')
    check(page.locator('#fuente-S10').is_visible(), 'Source deep link hidden')
    results.append({'case':'source deep link','status':'passed'})
    browser.close()
(args.output/'report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
raise SystemExit(1 if any(r['status']=='failed' for r in results) else 0)
