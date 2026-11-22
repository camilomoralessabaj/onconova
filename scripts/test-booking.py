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

def visible_screen(page, screen, focused=False):
    heading = page.locator(f'[data-screen="{screen}"] h3')
    check(heading.is_visible(), f'Screen {screen} missing')
    if focused:
        check(heading.evaluate('el => el === document.activeElement'), f'Focus not moved to {screen}')


def enter_account(page, insurance='Fonasa'):
    visible_screen(page, 'account')
    check(page.locator('[data-example-name]').inner_text() == NAME, 'Wrong sample identity')
    check(page.locator('[data-example-email]').inner_text() == CONTACTS['Correo'], 'Wrong sample email')
    page.get_by_role('radio', name=insurance, exact=False).check()
    enter = page.get_by_role('button', name='Entrar con cuenta de ejemplo')
    enter.press('Enter')
    visible_screen(page, 'start', focused=True)
    # A repeated submit from the previous screen cannot change state.
    page.locator('[data-account-form]').evaluate('form => form.requestSubmit()')
    visible_screen(page, 'start', focused=True)


def submit_request(page, channel='WhatsApp', modality='Videollamada', insurance='Fonasa'):
    if page.locator('[data-screen="account"]').is_visible():
        enter_account(page, insurance)
    page.locator(f'input[name="channel"][value="{channel}"]').check()
    page.locator(f'input[name="modality"][value="{modality}"]').check()
    page.locator('input[name="demo-consent"]').check()
    page.get_by_role('button', name='Simular mi solicitud', exact=False).click()
    visible_screen(page, 'message')
    check(f'{channel} para {CONTACTS[channel]}' == page.locator('[data-message-channel]').inner_text(), 'Wrong message channel/contact')
    check(page.locator('[data-message-name]').inner_text() == NAME, 'Wrong message name')
    no_receipt(page)
    page.get_by_role('button', name='Ver horarios de ejemplo', exact=False).click()


def sample_session(page, insurance, key, *, cancel_start=False):
    appointment = page.locator('[data-appointment-date]').inner_text()
    start = page.locator('[data-action=start-session]')
    page.locator('[data-screen=confirmed] h3').focus()
    page.keyboard.press('Tab')
    check(start.evaluate('el => el === document.activeElement && el.matches(":focus-visible")'), 'Start session keyboard order')
    page.keyboard.press('Enter')
    visible_screen(page, 'payment', focused=True)
    start.dispatch_event('click')
    check(page.locator('[data-payment-date]').inner_text() == appointment, 'Payment linked to wrong booking')
    check(page.locator('[data-payment-amount]').inner_text() == '$20.000 CLP', 'Incorrect illustrative amount')
    check(page.locator('[data-screen=payment] input').count() == 0, 'Unexpected payment inputs')
    no_session_document(page)
    if cancel_start:
        page.locator('[data-action=return-to-booking]').press('Enter')
        visible_screen(page, 'confirmed', focused=True)
        check(page.locator('[data-appointment-date]').inner_text() == appointment, 'Returning from payment lost reservation')
        no_session_document(page)
        start.press('Enter')
    pay = page.locator('[data-action=pay]')
    page.keyboard.press('Tab')
    check(pay.evaluate('el => el === document.activeElement && el.matches(":focus-visible")'), 'Pay keyboard order')
    fits(page)
    page.screenshot(path=str(args.output / f'payment-{key}.png'))
    page.keyboard.press('Space')
    visible_screen(page, 'paid', focused=True)
    pay.dispatch_event('click')
    ref = page.locator('[data-bill-reference]').inner_text()
    check(ref.startswith('EJ-') and page.locator('[data-bill-date]').inner_text() == appointment, 'Boleta linked to wrong appointment')
    check(page.locator('[data-bill-amount]').inner_text() == '$20.000 CLP', 'Incorrect boleta amount')
    check(page.locator('.sample-bill .bill-validity').inner_text() == 'Sin validez tributaria', 'Boleta validity warning missing')
    check(page.locator('.sample-bill').count() == 1 and page.locator('[data-action=download]').is_hidden(), 'Duplicate boleta or booking PDF exposed')
    check(page.locator('[data-isapre-draft]').is_hidden(), 'Draft before completion')
    page.screenshot(path=str(args.output / f'boleta-{key}.png'))
    end = page.locator('[data-action=end-session]')
    page.keyboard.press('Tab')
    check(end.evaluate('el => el === document.activeElement'), 'End session keyboard order')
    page.keyboard.press('Enter')
    visible_screen(page, 'documents', focused=True)
    end.dispatch_event('click')
    draft = page.locator('[data-isapre-draft]')
    guidance = page.locator('[data-fonasa-guidance]')
    if insurance == 'Isapre':
        check(draft.is_visible() and guidance.is_hidden(), 'Wrong Isapre closing')
        for field, expected in {
            'name': NAME, 'email': CONTACTS['Correo'], 'insurance': 'Isapre',
            'reference': ref, 'amount': '$20.000 CLP'
        }.items():
            check(page.locator(f'[data-draft-{field}]').inner_text() == expected, f'Wrong prefill {field}')
        check(appointment in page.locator('[data-draft-date]').inner_text(), 'Draft linked to wrong date')
        check('ficticio' in page.locator('[data-draft-plan]').inner_text(), 'Plan should be marked fictitious')
        check('sin envío' in draft.inner_text() and draft.get_by_role('button').count() == 0, 'Draft exposes sending')
    else:
        check(guidance.is_visible() and draft.is_hidden(), 'Wrong Fonasa closing')
        check('Libre Elección' in guidance.inner_text() and 'bonos' in guidance.inner_text(), 'Fonasa orientation missing')
        check(all(value == '' for value in draft.locator('dd').all_text_contents()), 'Fonasa populated Isapre draft')
    fits(page)
    page.screenshot(path=str(args.output / f'documents-{key}.png'))
    page.locator('[data-action=review-bill]').press('Enter')
    visible_screen(page, 'paid', focused=True)
    check(page.locator('[data-bill-reference]').inner_text() == ref, 'Reopening changed bill reference')
    check('Volver a la orientación' in end.inner_text(), 'Repeated completion offered again')
    end.press('Enter')
    visible_screen(page, 'documents', focused=True)
    return ref


def no_session_document(page):
    check(page.locator('.sample-bill, [data-isapre-draft], [data-fonasa-guidance]').evaluate_all(
        'els => els.every(el => el.closest("[hidden]"))'), 'Session document exposed before payment or completion')
    check(all(value == '' for value in page.locator('.sample-bill dd[data-bill-reference], .sample-bill dd[data-bill-date], .sample-bill dd[data-bill-amount], [data-isapre-draft] dd').all_text_contents()),
          'Old session data retained')


def proposal_slots(page):
    return list(zip(page.locator('.slot>span').all_text_contents(), page.locator('.slot>strong').all_text_contents()))


def no_receipt(page):
    check(page.locator('[data-action="download"]').is_hidden(), 'Download exposed without confirmation')
    before = page.evaluate('window.receiptQA.created.length')
    page.locator('[data-action="download"]').dispatch_event('click')
    check(page.evaluate('window.receiptQA.created.length') == before, 'Unconfirmed receipt generated')
    check(all(page.locator(f'[data-appointment-{key}]').inner_text() == '' for key in ('name', 'date', 'modality', 'channel')), 'Stale confirmation')
    check(page.locator('[data-booking-status]').inner_text() == '', 'Stale download status')
    page.locator('[data-action=pay]').dispatch_event('click')
    page.locator('[data-action=end-session]').dispatch_event('click')
    no_session_document(page)

def download_pdf(page, channel, modality, name, key='Enter', render=False):
    global pdf_downloads
    date = page.locator('[data-appointment-date]').inner_text()
    button = page.get_by_role('button', name='Descargar comprobante PDF', exact=True)
    # Each confirmation focuses its heading; the session action comes before PDF.
    page.keyboard.press('Tab')
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
    check(page.locator('[data-appointment-name]').inner_text() not in text and CONTACTS[channel] not in text, 'Contact/name included in PDF')
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
            context = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce', accept_downloads=True, is_mobile=width != 1440, has_touch=width != 1440, timezone_id='Pacific/Kiritimati' if width == 1440 else 'America/Los_Angeles')
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
                # The public page loads without a session. Only the account opens booking.
                visible_screen(page, 'account')
                check(page.locator('[data-account-actions]').is_hidden(), 'Account actions shown when logged out')
                check(page.locator('[data-account-form] input').evaluate_all('els => els.every(el => el.type === "radio")'), 'Account asks for credentials')
                page.locator('[data-request-form]').evaluate('form => form.requestSubmit()')
                visible_screen(page, 'account')
                enter_account(page)
                request_button = page.get_by_role('button', name='Simular mi solicitud')
                request_button.press('Enter')
                visible_screen(page, 'start')
                check(page.locator('#consent-error').is_visible(), 'Consent bypass')
                check(page.locator('[name=demo-consent]').evaluate('el => el === document.activeElement'), 'Consent error focus')
                # Postponing or declining clears the active sample account.
                for label in ('Prefiero pensarlo', 'Ahora no lo necesito'):
                    page.get_by_role('button', name=label, exact=True).click()
                    visible_screen(page, 'paused', focused=True)
                    check(page.locator('[data-account-actions]').is_hidden(), 'Decision retained account')
                    no_receipt(page)
                    page.get_by_role('button', name='Volver al inicio de la demostración').click()
                    enter_account(page)
                page.locator('[data-account-actions] [data-action=reset]').click()
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
                # Reject the initial proposal, validate both groups, and fill them using the keyboard.
                submit_request(page, 'Correo', 'Videollamada', insurance='Isapre')
                original_slots = proposal_slots(page)
                page.locator('[name=slot]').first.check()
                page.locator('[data-action=unavailable]').press('Enter')
                check(page.locator('[data-screen=waiting] h3').evaluate('el => el === document.activeElement'), 'Availability heading focus')
                no_receipt(page)
                check(page.locator('[name=slot]:checked').count() == 0, 'Rejected selection retained')
                check(page.locator('[name=alternative-modality]:checked').input_value() == 'Videollamada', 'Alternative modality not preserved')
                search = page.locator('[data-wait-form] [type=submit]')
                search.press('Enter')
                days = page.locator('[name=preferred-day]')
                bands = page.locator('[name=preferred-band]')
                check(page.locator('#preferred-day-error').is_visible() and page.locator('#preferred-band-error').is_visible(), 'Missing empty-group errors')
                check(days.first.evaluate('el => el === document.activeElement && el.matches(":focus-visible")'), 'Day error focus')
                page.keyboard.press('Tab')
                page.keyboard.press('Space')
                page.keyboard.press('Tab')
                page.keyboard.press('Tab')
                page.keyboard.press('Space')
                check(page.locator('[name=preferred-day]:checked').evaluate_all('els => els.map(el => el.value)') == ['2', '4'], 'Keyboard selected wrong weekdays')
                check(page.locator('#preferred-day-error').is_hidden(), 'Day error does not clear immediately')
                search.press('Enter')
                check(bands.first.evaluate('el => el === document.activeElement && el.matches(":focus-visible")'), 'Band error focus')
                page.keyboard.press('Space')
                page.keyboard.press('Tab')
                page.keyboard.press('Space')
                check(page.locator('#preferred-band-error').is_hidden(), 'Band error does not clear immediately')
                page.keyboard.press('Tab')
                page.keyboard.press('Tab')
                page.keyboard.press('ArrowRight')
                check(page.locator('[name=alternative-modality]:checked').input_value() == 'Presencial', 'Keyboard modality selection')
                page.locator('.text-size').click()
                fits(page)
                check(all(el['height'] >= 44 for el in page.locator('.availability-grid .option').evaluate_all('els => els.map(el => ({height: el.getBoundingClientRect().height}))')), 'Availability target smaller than 44px')
                search.press('Enter')
                new_slots = proposal_slots(page)
                check(new_slots == [
                    ('jueves, 31 de diciembre de 2026', '11:15 h'),
                    ('jueves, 31 de diciembre de 2026', '14:15 h'),
                    ('martes, 5 de enero de 2027', '11:15 h'),
                ], 'Availability did not match multiple days/bands, modality, full duration or Santiago calendar')
                check(set(original_slots).isdisjoint(new_slots), 'Rejected initial time repeated')
                check('Presencial' in page.locator('[data-proposal-note]').inner_text(), 'Preference summary mismatch')
                no_receipt(page)
                fits(page)
                page.locator('[name=slot]').last.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo').press('Enter')
                page.locator('[data-schedule-form]').evaluate('form => form.requestSubmit()')
                visible_screen(page, 'confirmed', focused=True)
                check(page.locator('[data-appointment-date]').inner_text() == 'martes, 5 de enero de 2027, 11:15 h (Santiago de Chile)', 'Wrong alternative confirmed')
                key = f'{route.strip("/") or "home"}-{width}'
                pdf_text = download_pdf(page, 'Correo', 'Presencial', f'alt-{key}', render=True)
                check('jueves, 31 de diciembre de 2026' not in pdf_text and '14:15 h' not in pdf_text, 'Unconfirmed alternative in PDF')
                check(all(date not in pdf_text for date, _ in original_slots), 'Rejected date in alternative PDF')
                page.locator('.text-size').click()

                old_reference = sample_session(page, 'Isapre', f'isapre-{key}', cancel_start=True)

                # Reprogramming after payment invalidates documents and restores the current proposal.
                page.locator('[data-screen=documents] [data-action=reschedule]').press('Enter')
                check(page.locator('[name=slot]:checked').count() == 0, 'Reschedule retained selection')
                no_receipt(page)
                page.locator('[name=slot]').first.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo').press('Enter')
                page.locator('[data-action=start-session]').press('Enter')
                page.locator('[data-action=pay]').press('Enter')
                check(page.locator('[data-bill-reference]').inner_text() != old_reference, 'Rebooked appointment reused document reference')
                check('jueves, 31 de diciembre de 2026' in page.locator('[data-bill-date]').inner_text(), 'New bill retained old date')
                page.locator('[data-action=end-session]').press('Enter')
                check(page.locator('[data-draft-reference]').inner_text() == page.locator('[data-bill-reference]').inner_text(), 'Rebooked draft linked to wrong bill')
                page.locator('[data-screen=documents] [data-action=reschedule]').press('Enter')
                no_receipt(page)
                page.locator('[name=slot]').first.check()
                page.locator('[data-action=adjust-availability]').click()
                page.locator('[name=alternative-modality][value=Videollamada]').check()
                page.get_by_role('button', name='Volver a la propuesta anterior').press('Enter')
                check(proposal_slots(page) == new_slots and 'Presencial' in page.locator('[data-proposal-note]').inner_text(), 'Draft modality changed previous proposal')
                check(page.locator('[name=slot]:checked').count() == 0, 'Return retained selection')
                no_receipt(page)

                # Reject again, then preserve the filters and exclude all rejected date+time pairs.
                page.locator('[name=slot]').first.check()
                page.locator('[data-action=unavailable]').press('Enter')
                check(page.locator('[data-screen=pending]').is_visible(), 'Second rejection should explain pending state')
                check(page.locator('[name=slot]:checked').count() == 0, 'Second rejection retained selection')
                no_receipt(page)
                page.locator('[data-action=review-alternatives]').press('Enter')
                check(page.locator('[name=preferred-day]:checked').count() == 2 and page.locator('[name=preferred-band]:checked').count() == 2, 'Review lost availability')
                page.locator('[name=alternative-modality][value=Presencial]').check()
                search.press('Enter')
                check(set(proposal_slots(page)).isdisjoint(original_slots + new_slots), 'Regeneration reused a rejected date+time')
                page.locator('[data-action=adjust-availability]').press('Enter')
                for day in (days.nth(1), days.nth(3)):
                    day.uncheck()
                check(page.locator('#preferred-day-error').is_visible() and page.locator('#preferred-band-error').is_hidden(), 'Missing-day error targets wrong group')
                days.last.check()
                bands.nth(0).uncheck()
                bands.nth(1).uncheck()
                bands.nth(2).check()
                search.press('Enter')
                check(proposal_slots(page) == [('viernes, 8 de enero de 2027', '15:30 h')], 'Rejected Friday time or a 17:30 start slipped into a shorter proposal')
                page.locator('[data-action=unavailable]').press('Enter')
                page.locator('[data-action=review-alternatives]').press('Enter')
                search.press('Enter')
                check(page.locator('[data-pending-reason]').inner_text().startswith('No quedan horarios'), 'Empty calendar missing')
                check(page.locator('[data-screen=pending] h3').evaluate('el => el === document.activeElement'), 'Empty calendar heading focus')
                no_receipt(page)
                page.locator('[data-action=review-alternatives]').press('Enter')
                page.locator('[name=alternative-modality][value=Videollamada]').check()
                search.press('Enter')
                check(proposal_slots(page) == [
                    ('viernes, 1 de enero de 2027', '15:00 h'),
                    ('viernes, 1 de enero de 2027', '17:15 h'),
                    ('viernes, 8 de enero de 2027', '15:00 h'),
                ], 'Changing modality should recover an empty calendar, including an exact 18:00 finish')
                page.locator('[data-action=adjust-availability]').press('Enter')
                page.locator('[name=alternative-modality][value=Presencial]').check()
                search.press('Enter')
                check(page.locator('[data-pending-reason]').inner_text().startswith('No quedan horarios'), 'Return to exhausted calendar')
                page.locator('[data-screen=pending] [data-action=leave-pending]').press('Enter')
                check(page.locator('[data-screen=paused]').is_visible(), 'Pending exit missing')
                check(page.locator('[data-account-actions]').is_hidden(), 'Pending exit retained account')
                check(page.locator('[name=preferred-day]:checked, [name=preferred-band]:checked').count() == 0, 'Pending exit retained availability')
                no_receipt(page)
                page.get_by_role('button', name='Volver al inicio de la demostración').press('Enter')
                # An early voluntary return leaves the original proposal and permits a fresh selection.
                submit_request(page, 'WhatsApp', 'Videollamada')
                page.locator('[data-action=unavailable]').press('Enter')
                page.locator('[data-screen=waiting] h3').focus()
                page.keyboard.press('Tab')
                check(days.first.evaluate('el => el === document.activeElement && el.matches(":focus-visible")'), 'First availability checkbox missing from tab order')
                page.screenshot(path=str(args.output / f'availability-focus-{key}.png'))
                page.get_by_role('button', name='Volver a la propuesta anterior').press('Enter')
                check(proposal_slots(page) == original_slots and page.locator('[name=slot]:checked').count() == 0, 'Initial return changed proposal or restored selection')
                no_receipt(page)
                page.locator('[data-action=reset]').first.press('Enter')
                # Edit confirmed details, change channel, invalidate summaries and generate a fresh PDF.
                submit_request(page, 'WhatsApp', 'Presencial')
                page.locator('[name=slot]').first.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                page.get_by_role('button', name='Editar preferencias de reserva').click()
                no_receipt(page)
                check(page.locator('[data-message-name]').inner_text() == '' and page.locator('[data-message-channel]').inner_text() == '', 'Old message retained on edit')
                page.locator('.text-size').click()
                submit_request(page, 'Correo', 'Videollamada')
                page.get_by_role('button', name='Volver al mensaje').click()
                check(page.locator('[data-message-name]').inner_text() == NAME, 'Fixed account name changed')
                page.screenshot(path=str(args.output / f'message-{width}-{route.strip("/") or "home"}.png'))
                fits(page)
                page.get_by_role('button', name='Ver horarios de ejemplo').click()
                page.locator('[name=slot]').last.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo', exact=True).click()
                check(CONTACTS['Correo'] in page.locator('[data-appointment-channel]').inner_text(), 'Selected account contact stale')
                check(CONTACTS['WhatsApp'] not in page.locator('[data-screen=confirmed]').inner_text(), 'Previous channel in confirmation')
                download_pdf(page, 'Correo', 'Videollamada', f'edited-{width}-{route.strip("/") or "home"}', render=True)
                fits(page)
                sample_session(page, 'Fonasa', f'fonasa-{key}')
                page.locator('[data-screen=documents] [data-action=cancel-booking]').press('Enter')
                visible_screen(page, 'paused', focused=True)
                check('Cancelaste' in page.locator('[data-pause-title]').inner_text(), 'Cancellation not explained')
                no_receipt(page)
                page.get_by_role('button', name='Volver al inicio de la demostración').press('Enter')
                submit_request(page, insurance='Isapre')
                page.locator('[name=slot]').first.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo').press('Enter')
                page.locator('[data-action=start-session]').press('Enter')
                page.locator('[data-action=pay]').press('Enter')
                page.locator('[data-action=end-session]').press('Enter')
                visible_screen(page, 'documents')
                check(page.evaluate('sessionStorage.length') == 0 and page.evaluate('Object.keys(localStorage).every(k => k === "onconova-large-text")'), 'Contact persisted during flow')
                check(page.evaluate('document.cookie') == '', 'Unexpected cookies')
                check(page.evaluate('async () => (await indexedDB.databases()).length') == 0, 'Unexpected IndexedDB')
                check(all(NAME not in message and not any(value in message for value in CONTACTS.values()) for message in console_messages), 'Personal data in console')
                # Reload clears active Isapre documents and resets the account choice.
                page.reload(wait_until='networkidle')
                visible_screen(page, 'account')
                no_receipt(page)
                check(page.locator('[name=insurance]:checked').input_value() == 'Fonasa', 'Reload retained account choice')
                check(page.locator('[data-account-actions]').is_hidden(), 'Reload retained session')
                submit_request(page, insurance='Isapre')
                page.locator('[name=slot]').first.check()
                page.get_by_role('button', name='Confirmar hora de ejemplo').press('Enter')
                page.locator('[data-action=start-session]').press('Enter')
                page.locator('[data-action=pay]').press('Enter')
                page.get_by_role('button', name='Cerrar sesión de ejemplo').press('Enter')
                visible_screen(page, 'account', focused=True)
                no_receipt(page)
                check(page.locator('[name=insurance]:checked').input_value() == 'Fonasa', 'Logout retained insurance')
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
    for source in ('S10', 'S15', 'S16', 'S17'):
        page.goto(args.base_url.rstrip('/') + '/#fuente-' + source)
        check(page.locator('#fuente-' + source).is_visible(), 'Source deep link hidden')
    results.append({'case':'source deep link','status':'passed'})
    browser.close()
(args.output/'report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
raise SystemExit(1 if any(r['status']=='failed' for r in results) else 0)
