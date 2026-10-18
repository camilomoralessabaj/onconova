#!/usr/bin/env python3
"""Local browser checks for the academic booking flow. Requires Playwright/Chromium, PyMuPDF and pdftotext (QA only)."""
import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import fitz
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='http://127.0.0.1:4173')
parser.add_argument('--output', type=Path, default=Path('work/qa'))
parser.add_argument('--auxiliary-only', action='store_true', help='Repeat static/no-JS checks using an existing main-flow report')
args = parser.parse_args()
if urlparse(args.base_url).hostname not in ('127.0.0.1', 'localhost', '::1'):
    parser.error('Use a local test server')
if not shutil.which('pdftotext'):
    parser.error('pdftotext is required to validate PDF content independently')
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
    no_receipt(page)
    page.get_by_role('button', name='Ver horarios de ejemplo', exact=False).click()

def no_receipt(page):
    check(page.locator('[data-action="download"]').is_hidden(), 'Download exposed without confirmation')
    before = page.evaluate('window.receiptQA.created.length')
    page.locator('[data-action="download"]').dispatch_event('click')
    check(page.evaluate('window.receiptQA.created.length') == before, 'Unconfirmed receipt generated')
    check(page.locator('[data-appointment-date]').inner_text() == '', 'Stale confirmation')
    check(page.locator('[data-booking-status]').inner_text() == '', 'Stale download status')

def download_pdf(page, channel, modality, name, key='Enter', render=False):
    date = page.locator('[data-appointment-date]').inner_text()
    button = page.get_by_role('button', name='Descargar comprobante PDF', exact=True)
    # Each confirmation focuses its heading; Tab must reach the download button.
    page.keyboard.press('Tab')
    check(button.evaluate('(el) => el === document.activeElement'), 'Download keyboard order')
    check(button.evaluate('(el) => getComputedStyle(el).outlineStyle != "none" && parseFloat(getComputedStyle(el).outlineWidth) >= 3'), 'Download focus outline')
    check(button.bounding_box()['height'] >= 44, 'Download target smaller than 44px')
    if render:
        page.screenshot(path=str(args.output / f'focus-{name}.png'))
    with page.expect_download() as event:
        page.keyboard.press(key)
    download = event.value
    check(download.suggested_filename == 'onconova-comprobante-simulado.pdf', 'Wrong filename')
    check(download.failure() is None, 'Download failed')
    file = args.output / f'{name}.pdf'
    download.save_as(file)
    check(page.evaluate('window.receiptQA.created.at(-1).type') == 'application/pdf', 'Wrong MIME')
    check('PDF iniciada' in page.locator('[data-booking-status]').inner_text(), 'Missing download announcement')
    check(page.locator('[data-booking-status]').is_visible(), 'Download status hidden')
    fits(page)
    if render:
        page.locator('[data-booking-status]').scroll_into_view_if_needed()
        page.screenshot(path=str(args.output / f'status-{name}.png'))
    check(page.locator('[data-booking-status]').get_attribute('role') == 'status' and page.locator('[data-booking-status]').get_attribute('aria-live') == 'polite', 'Missing live region')
    # Parse the actual file, extract independently with Poppler and rasterize with MuPDF.
    extracted = subprocess.run(['pdftotext', '-layout', str(file), '-'], capture_output=True, text=True, check=True)
    check(not extracted.stderr, 'PDF reader warnings: ' + extracted.stderr)
    text = ' '.join(extracted.stdout.split())
    file.with_suffix('.txt').write_text(extracted.stdout)
    fitz.TOOLS.mupdf_warnings(reset=True)
    with fitz.open(file) as pdf:
        check(not pdf.is_repaired and not pdf.is_encrypted, 'PDF requires repair or password')
        check(len(pdf) == 1, 'Receipt must have one page')
        sheet = pdf[0]
        check(abs(sheet.rect.width - 595.28) < .1 and abs(sheet.rect.height - 841.89) < .1, 'Not A4')
        check(not sheet.get_images(), 'Receipt must use text/vector content')
        check('Comprobante de agendamiento' in sheet.get_text(), 'No selectable receipt text')
        spans = []
        for block in sheet.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    check(sheet.rect.contains(fitz.Rect(span['bbox'])), 'Text outside page')
                    spans.append(fitz.Rect(span['bbox']))
        for index, span in enumerate(spans):
            for other in spans[index + 1:]:
                intersection = span & other
                check(intersection.is_empty or intersection.get_area() < .5, 'Overlapping PDF text')
        pixels = sheet.get_pixmap(matrix=fitz.Matrix(1.25, 1.25))
        if render:
            pixels.save(args.output / f'{name}.png')
    check(not fitz.TOOLS.mupdf_warnings(reset=True), 'MuPDF reader warnings')
    for value in ('OncoNova', 'Comprobante de agendamiento', 'Usuaria de ejemplo',
                  'Primera sesión de apoyo psicológico', '45 minutos', modality,
                  'Profesional de ejemplo, sin identidad asignada', channel,
                  'No se envió ningún mensaje.', 'Cita simulada; atención aún no realizada.',
                  'Prototipo académico de OncoNova.',
                  'Cita simulada: no constituye una reserva real, no acredita atención, cobertura ni pago.'):
        check(value in text, f'Missing PDF content: {value}')
    expected_date, time = date.rsplit(', ', 1)
    check(expected_date in text and time.replace(' (Santiago de Chile)', '') + ' · Hora de Santiago de Chile' in text, 'PDF/screen date or time mismatch')
    check(('dirección real asignada' if modality == 'Presencial' else 'sala real de atención') in text, 'Missing modality limitation')
    check(('WhatsApp' if channel == 'Correo' else 'Correo') not in text, 'Wrong extra channel')
    check(('Presencial' if modality == 'Videollamada' else 'Videollamada') not in text, 'Wrong extra modality')
    return text

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    for route in (() if args.auxiliary_only else ('/', '/prototipo/')):
        for width in (1440, 390, 320):
            context = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce', accept_downloads=True, timezone_id='Pacific/Kiritimati' if width == 1440 else 'America/Los_Angeles')
            context.add_init_script("""
                window.receiptQA = {created: [], revoked: [], fail: ''};
                window.Blob = new Proxy(Blob, {construct(target, args) {
                    if (receiptQA.fail === 'blob') throw new Error('QA: PDF Blob failure');
                    return Reflect.construct(target, args);
                }});
                const create = URL.createObjectURL.bind(URL);
                const revoke = URL.revokeObjectURL.bind(URL);
                URL.createObjectURL = blob => {
                    if (receiptQA.fail === 'url') throw new Error('QA: URL failure');
                    const url = create(blob);
                    receiptQA.created.push({url, type: blob.type});
                    return url;
                };
                URL.revokeObjectURL = url => { receiptQA.revoked.push(url); revoke(url); };
                const click = HTMLAnchorElement.prototype.click;
                HTMLAnchorElement.prototype.click = function () {
                    if (receiptQA.fail === 'click') throw new Error('QA: anchor failure');
                    return click.call(this);
                };
            """)
            page = context.new_page()
            # Santiago is still Dec 30; next slots must cross the year regardless of device zone.
            page.clock.install(time=datetime(2026, 12, 31, 1, tzinfo=timezone.utc))
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
                no_receipt(page)
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
                    no_receipt(page)
                    page.get_by_role('button', name='Volver al inicio de la demostración').click()
                # All channel/modality combinations and download consistency.
                for channel in ('WhatsApp', 'Correo'):
                    for modality in ('Videollamada', 'Presencial'):
                        submit_request(page, channel, modality)
                        no_receipt(page)
                        check(page.locator('.slot>span').all_text_contents() == ['jueves, 31 de diciembre de 2026', 'viernes, 1 de enero de 2027', 'lunes, 4 de enero de 2027'], 'Santiago calendar/year mismatch')
                        page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                        check(page.locator('[data-slot-error]').is_visible(), 'Missing selection error')
                        check(page.locator('input[name="slot"]').first.evaluate('(el) => el === document.activeElement'), 'Error focus')
                        page.locator('input[name="slot"]').nth(1).check()
                        page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                        check(page.locator('[data-screen="confirmed"]').is_visible(), 'Confirmation missing')
                        check(modality.lower() in page.locator('[data-appointment-modality]').inner_text().lower(), 'Modality mismatch')
                        check(channel in page.locator('[data-appointment-channel]').inner_text(), 'Channel mismatch')
                        fits(page)
                        date = page.locator('[data-appointment-date]').inner_text()
                        check(date == 'viernes, 1 de enero de 2027, 15:30 h (Santiago de Chile)', 'Wrong selected date')
                        name = f'{route.strip("/") or "home"}-{width}-{channel}-{modality}'
                        original = download_pdf(page, channel, modality, name, render=channel == 'Correo')
                        # Changing slot removes prior confirmation.
                        page.get_by_role('button', name='Cambiar horario', exact=True).click()
                        check(page.locator('input[name="slot"]:checked').count() == 0, 'Stale slot after reschedule')
                        no_receipt(page)
                        page.locator('input[name="slot"]').last.check()
                        page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                        updated = download_pdf(page, channel, modality, name + '-reprogramado', key='Space')
                        check('lunes, 4 de enero de 2027' in updated and '11:00 h' in updated, 'Reschedule PDF mismatch')
                        check('viernes, 1 de enero de 2027' not in updated and '15:30 h' not in updated and original != updated, 'Stale PDF after reschedule')
                        # Forced creation and click failures must never announce success or leak anchors.
                        for failure in ('blob', 'url', 'click'):
                            page.evaluate('(failure) => { receiptQA.fail = failure; }', failure)
                            page.locator('[data-action="download"]').click()
                            check('No se pudo preparar' in page.locator('[data-booking-status]').inner_text(), 'False success on error')
                            check(page.locator('a[download]').count() == 0, 'Temporary anchor leaked')
                        page.evaluate('receiptQA.fail = ""')
                        # Retry succeeds after failures, even for the same confirmation.
                        page.locator('[data-screen="confirmed"] h3').focus()
                        download_pdf(page, channel, modality, name + '-reintento')
                        page.clock.run_for(1100)
                        check(page.evaluate('receiptQA.created.every(item => receiptQA.revoked.includes(item.url))'), 'Object URL leaked')
                        page.get_by_role('button', name='Volver a empezar', exact=True).click()
                        no_receipt(page)
                        check(not page.locator('input[name="demo-consent"]').is_checked(), 'Reset consent')
                # The changed confirmation, button and status also reflow with enlarged text.
                page.locator('.text-size').click()
                submit_request(page, 'Correo', 'Videollamada')
                page.locator('input[name="slot"]').first.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                download_pdf(page, 'Correo', 'Videollamada', f'large-{route.strip("/") or "home"}-{width}', render=True)
                page.get_by_role('button', name='Volver a empezar', exact=True).click()
                page.locator('.text-size').click()
                # Unavailable branch: preferences must be explicitly registered again after edit.
                submit_request(page, 'Correo', 'Presencial')
                page.get_by_role('button', name='Ninguno me acomoda', exact=True).click()
                no_receipt(page)
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
                no_receipt(page)
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
                results.append({'route': route, 'width': width, 'status':'passed', 'pdfDownloads':13, 'combinations':4, 'failureCases': ['blob', 'url', 'click']})
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
