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


def check_page(page, base_url, route, width):
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
    require(page.evaluate("document.activeElement !== document.body"),
            "Tab no alcanza un elemento enfocable")
    size = page.locator(".text-size")
    before = size.get_attribute("aria-pressed")
    size.click()
    require(size.get_attribute("aria-pressed") != before, "El control de tamaño no cambia de estado")
    require(page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"),
            "El documento desborda con texto ampliado")
    if route == "prototipo/":
        page.locator("#support").select_option(index=1)
        require("rehabilitación" in page.locator("[data-support]").first.inner_text(),
                "La ficha no refleja el apoyo seleccionado")
        for decision in ["posterga", "rechaza"]:
            page.locator(f'input[value="{decision}"]').check()
            require(page.locator('[data-event="recibida"]').is_disabled(),
                    f"La solicitud permanece activa tras {decision}")
        page.locator('input[value="acepta"]').check()
        for state, expected in [("recibida", "recibida"), ("sin-cupo", "cupo"),
                                ("atendida", "confirmada")]:
            page.locator(f'[data-event="{state}"]').click()
            require(expected in page.locator(".tracking-status").inner_text().lower(),
                    f"Estado de seguimiento incorrecto: {state}")
        page.locator('[data-event="reiniciar"]').click()
        require(page.locator('input[value="acepta"]').is_checked(), "El reinicio no restaura aceptación")
        require(page.locator("#support").input_value() == "Apoyo emocional",
                "El reinicio no restaura el apoyo inicial")
    else:
        choice = page.locator("[data-choice]").last
        choice.click()
        require(choice.get_attribute("aria-pressed") == "true", "La elección no se activa")
        require(bool(page.locator("[data-choice-result]").inner_text().strip()),
                "La elección no muestra una explicación")
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
                        check_page(page, base_url, route, width)
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
