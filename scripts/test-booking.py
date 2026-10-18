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
pdf_downloads = 0
NAME = 'María José O’Neill'
CONTACTS = {'WhatsApp': '+56 9 0000 0000', 'Correo': 'maria.jose@example.com'}
results = json.loads((args.output/'report.json').read_text()) if args.auxiliary_only else []

def check(condition, message):
    if not condition:
        raise AssertionError(message)

def fits(page):
    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Horizontal overflow')

def submit_request(page, channel='WhatsApp', modality='Videollamada', name=NAME, contact=None):
    page.locator(f'input[name="channel"][value="{channel}"]').check()
    page.locator(f'input[name="modality"][value="{modality}"]').check()
    page.get_by_label('Nombre preferido').fill(name)
    page.locator('#contact-email' if channel == 'Correo' else '#contact-phone').fill(contact or CONTACTS[channel])
    page.locator('input[name="demo-consent"]').check()
    page.get_by_role('button', name='Simular mi solicitud', exact=False).click()
    check(page.locator('[data-screen="message"]').is_visible(), 'Message must follow request')
    check(channel in page.locator('[data-message-channel]').inner_text(), 'Wrong message channel')
    check((contact or CONTACTS[channel]) in page.locator('[data-message-channel]').inner_text(), 'Wrong message contact')
    check(page.locator('[data-message-name]').inner_text() == name.strip(), 'Wrong message name')
    no_receipt(page)
    page.get_by_role('button', name='Ver horarios de ejemplo', exact=False).click()

def no_receipt(page):
    check(page.locator('[data-action="download"]').is_hidden(), 'Download exposed without confirmation')
    before = page.evaluate('window.receiptQA.created.length')
    page.locator('[data-action="download"]').dispatch_event('click')
    check(page.evaluate('window.receiptQA.created.length') == before, 'Unconfirmed receipt generated')
    check(all(page.locator(f'[data-appointment-{key}]').inner_text() == '' for key in ('name', 'date', 'modality', 'channel')), 'Stale confirmation')
    check(page.locator('[data-booking-status]').inner_text() == '', 'Stale download status')

def download_pdf(page, channel, modality, name, key='Enter', render=False):
    global pdf_downloads
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
    pdf_downloads += 1
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
    for value in ('OncoNova', 'Comprobante de agendamiento', 'Demostración sin nombre ni contacto en el PDF',
                  'Primera sesión de apoyo psicológico', '45 minutos', modality,
                  'Profesional de ejemplo, sin identidad asignada', channel,
                  'No se envió ningún mensaje.', 'Cita simulada; atención aún no realizada.',
                  'Prototipo académico de OncoNova.',
                  'Cita simulada: no constituye una reserva real, no acredita atención, cobertura ni pago.'):
        check(value in text, f'Missing PDF content: {value}')
    check(page.locator('[data-appointment-name]').inner_text() not in text and CONTACTS[channel] not in text and page.locator('#contact-email' if channel == 'Correo' else '#contact-phone').input_value() not in text, 'Contact/name included in PDF')
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
            pdf_downloads = 0
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
            console_messages = []
            page.on('console', lambda message: console_messages.append(message.text))
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
                # Empty, whitespace, malformed contacts and channel changes stay on the form.
                request_button = page.get_by_role('button', name='Simular mi solicitud')
                request_button.click()
                check(page.locator('#preferred-name').evaluate('el => el === document.activeElement'), 'Name error focus')
                check(page.locator('#name-error').is_visible(), 'Name error missing')
                page.locator('#preferred-name').fill('   ')
                request_button.click()
                check(page.locator('[data-screen="start"]').is_visible(), 'Whitespace name accepted')
                page.locator('#preferred-name').fill(NAME)
                check(page.locator('#name-error').is_hidden(), 'Name error does not clear immediately')
                for value in ('', '123', 'abcdefgh', '++56 9 0000 0000', '1234567890123456'):
                    page.locator('#contact-phone').fill(value)
                    request_button.click()
                    check(page.locator('#phone-error').is_visible(), 'Invalid telephone accepted')
                    check(page.locator('#contact-phone').evaluate('el => el === document.activeElement'), 'Telephone error focus')
                page.locator('[name=channel][value=Correo]').check()
                check(page.locator('#contact-phone').is_disabled() and page.locator('#contact-phone').input_value() == '', 'Inactive phone retained')
                check(page.locator('#phone-error').is_hidden() and page.locator('#contact-phone').is_hidden(), 'Inactive phone error/focus target')
                for value in ('', 'sin-arroba', 'nombre@', 'nombre con espacios@example.com'):
                    page.locator('#contact-email').fill(value)
                    request_button.click()
                    check(page.locator('#email-error').is_visible(), 'Invalid email accepted')
                    check(page.locator('#contact-email').evaluate('el => el === document.activeElement'), 'Email error focus')
                page.locator('#contact-email').fill(CONTACTS['Correo'])
                check(page.locator('#email-error').is_hidden(), 'Email error does not clear immediately')
                page.locator('[name=channel][value=WhatsApp]').check()
                check(page.locator('#contact-email').is_disabled() and page.locator('#contact-email').input_value() == '', 'Inactive email retained')
                check(not page.locator('#contact-email').evaluate('el => el.required'), 'Inactive channel required')
                page.locator('#contact-phone').fill(CONTACTS['WhatsApp'])
                # Required acknowledgement blocks request.
                page.get_by_role('button', name='Simular mi solicitud', exact=False).click()
                check(page.locator('[data-screen="start"]').is_visible(), 'Consent bypass')
                check(page.locator('[name=demo-consent]').evaluate('el => el === document.activeElement'), 'Consent error focus')
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
                        check(CONTACTS[channel] in page.locator('[data-appointment-channel]').inner_text(), 'Confirmation contact mismatch')
                        check(page.locator('[data-appointment-name]').inner_text() == NAME, 'Confirmation name mismatch')
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
                # Each preference and modality produces a new proposal, not the rejected dates.
                for channel in ('WhatsApp', 'Correo'):
                    for initial_modality in ('Videollamada', 'Presencial'):
                        for period in ('la mañana', 'la tarde'):
                            submit_request(page, channel, initial_modality)
                            rejected = page.locator('.slot>span').all_text_contents()
                            page.locator('[name=slot]').first.check()
                            page.get_by_role('button', name='Ninguno me acomoda', exact=True).click()
                            no_receipt(page)
                            check(page.locator('[name=slot]:checked').count() == 0, 'Rejected selection retained')
                            check(page.locator('[name=alternative-modality]:checked').input_value() == initial_modality, 'Alternative modality not preserved')
                            page.locator(f'[name=preferred-time][value="{period}"]').check()
                            modality = 'Presencial' if initial_modality == 'Videollamada' else 'Videollamada'
                            page.locator(f'[name=alternative-modality][value="{modality}"]').check()
                            page.get_by_role('button', name='Ver nuevos horarios de ejemplo').click()
                            check(page.locator('[data-screen=schedule]').is_visible(), 'Alternatives do not continue')
                            new_dates = page.locator('.slot>span').all_text_contents()
                            check(len(new_dates) == 3 and not set(new_dates) & set(rejected), 'Rejected dates repeated')
                            check(new_dates == ['martes, 5 de enero de 2027', 'miércoles, 6 de enero de 2027', 'jueves, 7 de enero de 2027'], 'Alternative dates/calendar mismatch')
                            hours = [int(value.split(':')[0]) for value in page.locator('.slot>strong').all_text_contents()]
                            check(all((h < 12 if period == 'la mañana' else h >= 12) for h in hours), 'Wrong period')
                            check(modality.lower() in page.locator('[data-proposal-note]').inner_text() and period in page.locator('[data-proposal-note]').inner_text(), 'Preference summary mismatch')
                            check(page.locator('[name=slot]:checked').count() == 0, 'Stale alternative selection')
                            page.locator('[name=slot]').last.check()
                            page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                            check(modality.lower() in page.locator('[data-appointment-modality]').inner_text().lower(), 'Alternative modality mismatch')
                            alt_key = f'alt-{route.strip("/") or "home"}-{width}-{channel}-{modality}-{period}'
                            pdf_text = download_pdf(page, channel, modality, alt_key, render=channel == 'Correo' and period == 'la tarde')
                            check(all(value not in pdf_text for value in rejected), 'Rejected date in PDF')
                            # Reprogram, reject again, review preferences and regenerate beyond that proposal.
                            page.get_by_role('button', name='Cambiar horario', exact=True).click()
                            no_receipt(page)
                            page.get_by_role('button', name='Ninguno me acomoda', exact=True).click()
                            check(page.locator('[data-screen=pending]').is_visible(), 'Second rejection should explain pending state')
                            no_receipt(page)
                            page.get_by_role('button', name='Revisar preferencias de horarios').click()
                            # Return is voluntary, and never restores a selected or confirmed slot.
                            page.get_by_role('button', name='Volver a la propuesta anterior').click()
                            check(page.locator('[name=slot]:checked').count() == 0, 'Back restored selection')
                            page.get_by_role('button', name='Ninguno me acomoda', exact=True).click()
                            page.get_by_role('button', name='Revisar preferencias de horarios').click()
                            page.get_by_role('button', name='Ver nuevos horarios de ejemplo').click()
                            check(modality.lower() in page.locator('[data-proposal-note]').inner_text(), 'Maintained modality lost')
                            check(not set(page.locator('.slot>span').all_text_contents()) & set(rejected + new_dates), 'Regenerated proposal reused rejected dates')
                            page.get_by_role('button', name='Ninguno me acomoda', exact=True).click()
                            page.get_by_role('button', name='Dejar pendiente y salir').click()
                            check(page.locator('[data-screen=paused]').is_visible(), 'Pending exit missing')
                            check(page.locator('#preferred-name').input_value() == '', 'Pending exit retained contact')
                            no_receipt(page)
                            page.get_by_role('button', name='Volver al inicio de la demostración').click()
                # Edit confirmed details, change channel, invalidate summaries and generate a fresh PDF.
                submit_request(page, 'WhatsApp', 'Presencial')
                page.locator('[name=slot]').first.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                page.get_by_role('button', name='Editar datos y preferencias').click()
                no_receipt(page)
                check(page.locator('[data-message-name]').inner_text() == '' and page.locator('[data-message-channel]').inner_text() == '', 'Old message retained on edit')
                page.locator('.text-size').click()
                submit_request(page, 'Correo', 'Videollamada', name="Ana Isabel O'Connor de la Cruz", contact='ana.isabel.de.la.cruz+demostracion@ejemplo-academico.example.com')
                page.get_by_role('button', name='Volver al mensaje').click()
                check(page.locator('[data-message-name]').inner_text() == "Ana Isabel O'Connor de la Cruz", 'Edited message name stale')
                page.screenshot(path=str(args.output / f'message-{width}-{route.strip("/") or "home"}.png'))
                fits(page)
                page.get_by_role('button', name='Ver horarios de ejemplo').click()
                page.locator('[name=slot]').last.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                check('ana.isabel.de.la.cruz+' in page.locator('[data-appointment-channel]').inner_text(), 'Edited contact stale')
                check(NAME not in page.locator('[data-booking]').inner_text() and CONTACTS['WhatsApp'] not in page.locator('[data-booking]').inner_text(), 'Previous identity in rendered output')
                download_pdf(page, 'Correo', 'Videollamada', f'edited-{width}-{route.strip("/") or "home"}', render=True)
                fits(page)
                check(page.evaluate('sessionStorage.length') == 0 and page.evaluate('Object.keys(localStorage).every(k => k === "onconova-large-text")'), 'Contact persisted during flow')
                check(page.evaluate('document.cookie') == '', 'Unexpected cookies')
                check(page.evaluate('async () => (await indexedDB.databases()).length') == 0, 'Unexpected IndexedDB')
                check(all(NAME not in message and not any(value in message for value in CONTACTS.values()) for message in console_messages), 'Personal data in console')
                # Reload clears the academic booking; only reading preference persists.
                page.reload(wait_until='networkidle')
                check(page.locator('[data-screen="start"]').is_visible(), 'Reload retains booking')
                no_receipt(page)
                check(all(page.locator(selector).input_value() == '' for selector in ('#preferred-name', '#contact-phone', '#contact-email')), 'Reload retains contact fields')
                check(not page.locator('[name=demo-consent]').is_checked(), 'Reload retains consent')
                check(page.evaluate('sessionStorage.length') == 0, 'Booking stored in session')
                check(page.evaluate('Object.keys(localStorage).every(k => k === "onconova-large-text")'), 'Unexpected local storage')
                check(all(method == 'GET' and url.startswith(args.base_url) and not urlparse(url).query for method, url in requests), 'External request, data in URL or submission')
                page.screenshot(path=str(args.output / f'{route.strip("/") or "home"}-{width}.png'), full_page=True)
                # Text enlargement plus halved desktop viewport as reflow approximation.
                page.locator('.text-size').click()
                fits(page)
                if width == 1440:
                    page.set_viewport_size({'width':720,'height':900})
                    fits(page)
                check(not errors, '; '.join(errors))
                results.append({'route': route, 'width': width, 'status':'passed', 'pdfDownloads':pdf_downloads, 'combinations':4, 'failureCases': ['blob', 'url', 'click']})
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
        check(page.get_by_role('link', name='Ver el proyecto en GitHub', exact=False).is_visible(), 'Essential no-JS repository link missing')
        check(page.locator('#preguntas').is_visible(), 'No-JS FAQs missing')
        if route == '/':
            check(all(page.locator('#'+id).count() == 1 for id in ('desafio', 'historia', 'propuesta', 'validacion', 'proximos-pasos')), 'No-JS narrative missing')
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
