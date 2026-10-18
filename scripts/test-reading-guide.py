#!/usr/bin/env python3
"""Local browser regression checks for the shared reading frame. Requires Playwright/Chromium."""
import argparse
import json
import shutil
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='http://127.0.0.1:4173')
parser.add_argument('--output', type=Path, default=Path('work/qa-reading-guide'))
args = parser.parse_args()
url = urlsplit(args.base_url)
if (url.scheme not in ('http', 'https') or url.hostname not in ('127.0.0.1', 'localhost', '::1')
        or url.username or url.password or url.query or url.fragment):
    parser.error('Use a local test server URL without credentials, query or fragment')
args.output.mkdir(parents=True, exist_ok=True)
BASE = args.base_url.rstrip('/')
STOPS = ['lectura-aprendizajes', 'lectura-brechas', 'proximos-pasos']
results = []


def check(condition, message):
    assert condition, message


def settled(page, index=None):
    page.wait_for_timeout(300)
    check(page.locator('.reading-guide [aria-current="step"]').count() == 1, 'Missing or duplicate current stop')
    if index is not None:
        check(page.locator('.reading-guide [aria-current="step"]').get_attribute('href') == '#' + STOPS[index], 'Wrong reading stop')
    delta = page.locator('.reading-frame').evaluate('''(frame) => {
      const target = document.querySelector('.reading-guide [aria-current]').getBoundingClientRect();
      const box = frame.getBoundingClientRect();
      return ['x','y','width','height'].map(key => Math.abs(box[key] - target[key]));
    }''')
    check(max(delta) < 2, f'Frame does not surround current link: {delta}')
    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Horizontal overflow')
    check(page.locator('[data-reading-stage]').evaluate_all('els => els.every(el => getComputedStyle(el).transform === "none" && getComputedStyle(el).opacity === "1")'), 'Reading text moves or fades')


def frame_motion(page, expected):
    animations = page.locator('.reading-frame').evaluate('''el => el.getAnimations().map(a => ({
      property:a.transitionProperty, duration:a.effect.getTiming().duration,
      easing:a.effect.getTiming().easing
    }))''')
    check(bool(animations) == expected, f'Unexpected frame animation: {animations}')
    if expected:
        check(all(a == {'property':'transform','duration':250,'easing':'cubic-bezier(0.23, 1, 0.32, 1)'} for a in animations), f'Wrong motion: {animations}')
    return animations


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    for width in (1440, 390, 320):
        for reduced in (False, True):
            context = browser.new_context(viewport={'width':width,'height':900 if width == 1440 else 800},
                reduced_motion='reduce' if reduced else 'no-preference', is_mobile=width < 500, has_touch=width < 500)
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
            page.goto(BASE + '/#aprendizajes', wait_until='networkidle')
            links = page.locator('.reading-guide a')
            page.locator('#' + STOPS[0]).evaluate('el => el.scrollIntoView({block:"start"})')
            settled(page, 0)
            # Native anchors, pointer/touch input, and the single shared frame.
            for index in (1, 2, 0):
                if width < 500:
                    links.nth(index).tap()
                else:
                    links.nth(index).click()
                frame_motion(page, not reduced)
                settled(page, index)
                check(page.locator('.reading-frame').count() == 1, 'Frame was duplicated')
                check(page.locator('#' + STOPS[index]).evaluate('el => el.getBoundingClientRect().top') > page.locator('.site-header').evaluate('el => el.getBoundingClientRect().bottom'), 'Target hidden behind header')
            # Native wheel crossing a section boundary updates the frame without auto-scrolling.
            target_y = page.locator('#' + STOPS[1]).evaluate('el => el.getBoundingClientRect().top + scrollY - innerHeight * .35 + 50')
            page.evaluate('y => scrollTo(0,y)', target_y)
            page.wait_for_timeout(100)
            page.mouse.wheel(0, 130)
            page.wait_for_function('document.querySelector(".reading-guide [aria-current]").hash === "#lectura-brechas"')
            frame_motion(page, not reduced)
            settled(page, 1)
            scroll = page.evaluate('scrollY')
            page.wait_for_timeout(100)
            check(page.evaluate('scrollY') == scroll, 'Guide moved the scroll position')
            nav = page.locator('.reading-guide').bounding_box()
            if page.locator('.reading-guide').evaluate('el => getComputedStyle(el).position') == 'sticky':
                check(nav['y'] >= 0 and nav['y'] + nav['height'] < page.viewport_size['height'], 'Sticky guide disappeared')
            else:
                check(width <= 720, 'Unexpected nonpersistent desktop guide')
                check(page.locator('.section-index').evaluate('el => getComputedStyle(el).position') == 'sticky', 'Global location missing while local guide is in flow')
            page.screenshot(path=str(args.output / f'guide-{width}-{"reduce" if reduced else "normal"}.png'))
            # Rapid reversal must finish at the latest stop, not queue animations.
            links.nth(2).click()
            links.nth(0).click()
            settled(page, 0)
            # Keyboard activation and Tab during an entry must settle immediately.
            links.nth(1).focus()
            page.keyboard.press('Tab')
            check(links.nth(2).evaluate('el => document.activeElement === el && getComputedStyle(el).outlineStyle === "solid"'), 'Keyboard link focus missing')
            page.keyboard.press('Enter')
            frame_motion(page, False)
            settled(page, 2)
            check(page.locator('#'+STOPS[2]).evaluate('el => document.activeElement === el && getComputedStyle(el).outlineStyle === "solid"'), 'Keyboard target focus missing')
            links.nth(0).click()
            page.keyboard.press('Tab')
            frame_motion(page, False)
            settled(page, 0)
            # System preference changing during an entrance cancels it immediately.
            if not reduced:
                links.nth(1).click()
                frame_motion(page, True)
                page.emulate_media(reduced_motion='reduce')
                frame_motion(page, False)
                settled(page, 1)
                page.emulate_media(reduced_motion='no-preference')
                frame_motion(page, False)
            # Larger type and a breakpoint change must resize/reposition the same frame.
            page.locator('.text-size').click()
            settled(page)
            links.nth(2).click()
            settled(page, 2)
            if width < 500:
                check(page.locator('.reading-guide').evaluate('el => getComputedStyle(el).position') == 'static', 'Large type guide obscures content')
                check(page.locator('.iteration-table tbody tr').first.evaluate('el => { const style=getComputedStyle(el); return Math.abs(el.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight) - el.querySelector("th").getBoundingClientRect().width) < 2; }'), 'Mobile action text is restricted to a table column')
            page.screenshot(path=str(args.output / f'large-{width}-{"reduce" if reduced else "normal"}.png'))
            page.set_viewport_size({'width':720 if width == 1440 else 1000,'height':900})
            page.wait_for_timeout(100)
            settled(page)
            check(page.locator('.reading-frame').count() == 1, 'Resize duplicated the frame')
            check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Resize overflow')
            page.emulate_media(media='print')
            check(page.locator('.reading-guide').is_hidden(), 'Print guide obscures text')
            check(page.locator('[data-reading-stage]').evaluate_all('els=>els.every(el => el.getBoundingClientRect().height > 0)'), 'Print hides narrative')
            check(not errors, '; '.join(errors))
            results.append({'width':width,'reduced_motion':reduced,'status':'passed'})
            print(json.dumps(results[-1]), flush=True)
            context.close()
    # Reverse Tab can bring an action close to the sticky bar: it must stay clear.
    for width in (390, 320):
        context = browser.new_context(viewport={'width':width,'height':800})
        page = context.new_page()
        page.goto(BASE+'/#lectura-aprendizajes', wait_until='networkidle')
        page.locator('.reading-guide a').first.focus()
        for key in ['Tab'] * 12 + ['Shift+Tab'] * 12:
            page.keyboard.press(key)
            check(page.evaluate('''() => {
                const el = document.activeElement;
                if (!el.closest('.reading-stage')) return true;
                const rect = el.getBoundingClientRect();
                const nav = document.querySelector('.reading-guide').getBoundingClientRect();
                return rect.top >= nav.bottom - 1 && rect.bottom <= innerHeight + 1;
            }'''), 'Mobile guide obscures keyboard focus')
        results.append({'case':'Tab and Shift+Tab below sticky guide','width':width,'status':'passed'})
        context.close()
    for fallback in ('no-js','no-observer'):
        context = browser.new_context(viewport={'width':320,'height':800}, java_script_enabled=fallback != 'no-js')
        if fallback == 'no-observer':
            context.add_init_script('delete window.IntersectionObserver')
        page = context.new_page()
        page.goto(BASE, wait_until='networkidle')
        check(page.locator('[data-reading-stage]').count() == 3, 'Fallback loses stages')
        check(page.locator('.reading-frame').is_hidden(), 'Fallback has an unpositioned frame')
        for index in range(3):
            page.locator('.reading-guide a').nth(index).click()
            check(page.url.endswith('#'+STOPS[index]), 'Fallback link failed')
            check(page.locator('#'+STOPS[index]).is_visible(), 'Fallback content hidden')
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Fallback overflow')
        results.append({'fallback':fallback,'status':'passed'})
        context.close()
    page = browser.new_page(viewport={'width':390,'height':800})
    for stop in STOPS:
        page.goto(BASE+'/#'+stop,wait_until='networkidle')
        settled(page, STOPS.index(stop))
    results.append({'case':'direct links to all three stops','status':'passed'})
    browser.close()
(args.output/'report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
