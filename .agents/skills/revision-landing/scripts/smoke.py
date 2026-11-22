#!/usr/bin/env python3
"""Smoke test local de Onconova. Requiere Playwright y Chromium; no instala nada."""
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def visible_screen(booking, name):
    screen = booking.locator(f'[data-screen="{name}"]')
    require(screen.is_visible(), f"No se muestra la pantalla {name}")
    return screen


def enter_account(booking, insurance):
    account = visible_screen(booking, "account")
    account.locator(f'input[name="insurance"][value="{insurance}"]').check()
    account.get_by_role("button", name="Entrar con cuenta de ejemplo", exact=True).press("Enter")
    return visible_screen(booking, "start")


def require_no_appointment(booking):
    require(booking.locator('[data-action="download"]').is_hidden()
            and not booking.locator("[data-appointment-date]").text_content().strip(),
            "Hay una cita o un comprobante sin confirmar un horario")


def check_pauses(booking):
    for label, heading in [("Prefiero pensarlo", "Puedes darte un tiempo."),
                           ("Ahora no lo necesito", "Tu decisión también cuenta.")]:
        start = enter_account(booking, "Fonasa")
        start.get_by_role("button", name=label, exact=True).click()
        paused = visible_screen(booking, "paused")
        require(paused.get_by_role("heading", name=heading, exact=True).is_visible(),
                f"La pausa no refleja la decisión: {label}")
        require(start.is_hidden() and booking.locator("[data-account-actions]").is_hidden()
                and not booking.locator("[data-message-channel]").text_content().strip(),
                f"La solicitud permanece activa tras elegir: {label}")
        require_no_appointment(booking)
        paused.get_by_role("button", name="Volver al inicio de la demostración", exact=True).click()
        visible_screen(booking, "account")


def check_pending(booking, schedule):
    schedule.get_by_role("button", name="Ninguno me acomoda", exact=True).click()
    waiting = visible_screen(booking, "waiting")
    waiting.get_by_role("checkbox", name="Lunes", exact=True).check()
    waiting.locator('input[name="preferred-band"][value="morning"]').check()
    waiting.get_by_role("button", name="Ver nuevos horarios de ejemplo", exact=True).click()
    schedule = visible_screen(booking, "schedule")
    require("según tus preferencias" in schedule.locator("[data-proposal-note]").inner_text()
            and schedule.get_by_role("radio").first.is_visible(),
            "No se muestran horarios alternativos según las preferencias")
    schedule.get_by_role("button", name="Ninguno me acomoda", exact=True).click()
    pending = visible_screen(booking, "pending")
    require("horarios" in pending.locator("[data-pending-reason]").inner_text(),
            "El estado pendiente no explica qué ocurrió con los horarios")
    require_no_appointment(booking)
    pending.get_by_role("button", name="Revisar preferencias de horarios", exact=True).click()
    waiting = visible_screen(booking, "waiting")
    waiting.get_by_role("button", name="Volver a la propuesta anterior", exact=True).click()
    return visible_screen(booking, "schedule")


def check_session(booking, confirmed, insurance, appointment):
    confirmed.get_by_role("button", name="Simular inicio de la sesión", exact=True).click()
    payment = visible_screen(booking, "payment")
    require(payment.locator("[data-payment-date]").inner_text() == appointment,
            "El pago simulado no corresponde al horario confirmado")
    payment.get_by_role("button", name="Simular pago", exact=True).click()
    paid = visible_screen(booking, "paid")
    reference = paid.locator("[data-bill-reference]").inner_text()
    require(reference.startswith("EJ-") and paid.locator("[data-bill-date]").inner_text() == appointment
            and paid.get_by_text("Sin validez tributaria", exact=True).is_visible(),
            "La boleta no refleja el pago de la cita simulada")
    paid.get_by_role("button", name="Simular término de la atención", exact=True).click()
    documents = visible_screen(booking, "documents")
    guidance = documents.locator("[data-fonasa-guidance]")
    draft = documents.locator("[data-isapre-draft]")
    if insurance == "Fonasa":
        require(guidance.is_visible() and "Libre Elección" in guidance.inner_text() and draft.is_hidden(),
                "Falta la orientación de Fonasa o aparece el borrador de Isapre")
    else:
        require(draft.is_visible() and guidance.is_hidden()
                and draft.locator("[data-draft-reference]").inner_text() == reference
                and "sin envío" in draft.inner_text(),
                "El borrador de Isapre no refleja la boleta de ejemplo o falta su aviso")


def check_booking(booking):
    account = visible_screen(booking, "account")
    require(bool(account.locator(".screen-intro p").inner_text().strip()),
            "La entrada no explica la simulación con cuenta de ejemplo")
    name = account.locator("[data-example-name]").inner_text().strip()
    require(bool(name), "Falta el nombre de la cuenta de ejemplo")
    check_pauses(booking)
    for insurance, channel, modality in [("Fonasa", "Correo", "Presencial"),
                                         ("Isapre", "WhatsApp", "Videollamada")]:
        start = enter_account(booking, insurance)
        start.locator(f'input[name="channel"][value="{channel}"]').check()
        start.locator(f'input[name="modality"][value="{modality}"]').check()
        contact = start.locator(f'[data-contact-example="{channel}"]').inner_text().strip()
        consent = start.locator('input[name="demo-consent"]')
        submit = start.get_by_role("button", name="Simular mi solicitud", exact=True)
        submit.click()
        require(start.locator("#consent-error").is_visible(), "La solicitud no exige consentimiento")
        consent.check()
        submit.click()
        message = visible_screen(booking, "message")
        require(bool(contact) and message.locator("[data-message-channel]").inner_text() == f"{channel} para {contact}"
                and message.locator("[data-message-name]").inner_text() == name,
                "El mensaje de solicitud recibida no refleja el canal y la cuenta seleccionados")
        require_no_appointment(booking)
        message.get_by_role("button", name="Ver horarios de ejemplo", exact=True).click()
        schedule = visible_screen(booking, "schedule")
        if insurance == "Fonasa":
            schedule = check_pending(booking, schedule)
        slot = schedule.locator(".slot").first
        date = slot.locator("span").inner_text()
        time = slot.locator("strong").inner_text()
        slot.get_by_role("radio").check()
        schedule.get_by_role("button", name="Confirmar hora de ejemplo", exact=True).click()
        confirmed = visible_screen(booking, "confirmed")
        appointment = f"{date}, {time} (Santiago de Chile)"
        require(confirmed.get_by_role("heading", name="Primera sesión de apoyo psicológico", exact=True).is_visible()
                and modality.lower() in confirmed.locator("[data-appointment-modality]").inner_text().lower()
                and confirmed.locator("[data-appointment-date]").inner_text() == appointment,
                "La cita confirmada no refleja el apoyo, la modalidad o el horario elegidos")
        require(confirmed.locator('[data-action="download"]').is_visible(),
                "La cita confirmada no ofrece el comprobante")
        check_session(booking, confirmed, insurance, appointment)
        booking.get_by_role("button", name="Volver a empezar", exact=True).click()
        account = visible_screen(booking, "account")
        require(account.locator('input[name="insurance"][value="Fonasa"]').is_checked()
                and start.locator('input[name="channel"][value="WhatsApp"]').is_checked()
                and start.locator('input[name="modality"][value="Videollamada"]').is_checked()
                and not consent.is_checked(), "El reinicio no restaura las preferencias iniciales")
        require_no_appointment(booking)
        require(not booking.locator("[data-bill-reference]").text_content().strip()
                and not booking.locator("[data-draft-reference]").text_content().strip(),
                "El reinicio conserva documentación de la sesión anterior")


def check_page(page, base_url, route):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("console", lambda message: errors.append(message.text)
            if message.type == "error" else None)
    page.on("response", lambda response: errors.append(
        f"HTTP {response.status}: {response.url}") if response.status >= 400 else None)
    page.on("requestfailed", lambda request: errors.append(
        f"Carga fallida: {request.url}") if request.failure != "net::ERR_ABORTED" else None)
    response = page.goto(base_url + route, wait_until="networkidle")
    require(response is not None and response.status == 200, "La página no devuelve HTTP 200")
    require(page.locator("h1").count() == 1, "Falta el encabezado principal único")
    require(page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"),
            "El documento desborda el ancho")
    page.keyboard.press("Tab")
    skip = page.locator(".skip-link")
    require(skip.evaluate("el => el === document.activeElement"),
            "Tab no enfoca primero el enlace para saltar al contenido")
    page.keyboard.press("Enter")
    size = page.locator(".text-size")
    before = size.get_attribute("aria-pressed")
    size.click()
    require(size.get_attribute("aria-pressed") != before, "El control de tamaño no cambia de estado")
    require(page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"),
            "El documento desborda con texto ampliado")
    if not route:
        page.get_by_role("link", name="Probar mi primera hora", exact=True).click()
        require(urlsplit(page.url).fragment == "prototipo", "La portada no enlaza con la demostración")
    check_booking(page.locator("[data-booking]"))
    require(page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"),
            "El documento desborda tras la interacción")
    require(not errors, "; ".join(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:4173")
    parser.add_argument("--width", type=int, action="append")
    parser.add_argument("--browser", help="Ruta del ejecutable Chromium")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--screenshots", type=Path)
    args = parser.parse_args()
    url = urlsplit(args.base_url)
    if url.scheme not in {"http", "https"} or url.hostname not in {"localhost", "127.0.0.1", "::1"}:
        parser.error("La URL debe apuntar a un servidor local de desarrollo")
    if url.username or url.password or url.query or url.fragment:
        parser.error("No se admiten credenciales, query ni fragmento en la URL base")
    base_url = args.base_url.rstrip("/") + "/"
    widths = list(dict.fromkeys(args.width or [1440, 390, 320]))
    if any(width < 280 or width > 7680 for width in widths):
        parser.error("Los anchos deben estar entre 280 y 7680 px")
    started = datetime.now(timezone.utc).isoformat()

    def save_report(data):
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps({"started_at": started, "base_url": base_url,
                                              **data}, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")

    save_report({"status": "running", "cases": []})
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        save_report({"status": "not_run", "error": "Falta Playwright Python", "cases": []})
        print("No se ejecutaron pruebas: falta Playwright Python en este entorno", file=sys.stderr)
        return 2
    results = []
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        executable = args.browser or shutil.which("chromium") or shutil.which("chromium-browser")
        try:
            browser = playwright.chromium.launch(executable_path=executable, args=["--no-sandbox"])
        except Exception as error:
            save_report({"status": "not_run", "error": str(error), "cases": []})
            print(f"No se ejecutaron pruebas: no pudo iniciar Chromium: {error}", file=sys.stderr)
            return 2
        try:
            for width in widths:
                for route in ["", "prototipo/"]:
                    context = browser.new_context(viewport={"width": width, "height": 900},
                                                  reduced_motion="reduce")
                    page = context.new_page()
                    result = {"width": width, "route": "/" + route, "status": "passed"}
                    try:
                        check_page(page, base_url, route)
                        if args.screenshots:
                            name = "prototipo" if route else "portada"
                            page.screenshot(path=str(args.screenshots / f"{name}-{width}.png"),
                                            full_page=True)
                    except Exception as error:
                        result.update(status="failed", error=str(error))
                        if args.screenshots:
                            name = "prototipo" if route else "portada"
                            try:
                                path = args.screenshots / f"fallo-{name}-{width}.png"
                                page.screenshot(path=str(path), full_page=True)
                                result["screenshot"] = str(path)
                            except Exception as capture_error:
                                result["capture_error"] = str(capture_error)
                    finally:
                        context.close()
                    results.append(result)
                    print(json.dumps(result, ensure_ascii=False))
        finally:
            browser.close()
    report = {"status": "completed", "finished_at": datetime.now(timezone.utc).isoformat(),
              "passed": sum(r["status"] == "passed" for r in results),
              "failed": sum(r["status"] == "failed" for r in results), "cases": results}
    save_report(report)
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"Smoke test interrumpido: {error}", file=sys.stderr)
        sys.exit(2)
