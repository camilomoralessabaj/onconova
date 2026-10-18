#!/usr/bin/env python3
"""Local regression checks for the shared reading panel. Requires Playwright/Chromium."""
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


def selected(page):
    return page.locator('[data-reading-stage]:not([hidden])').get_attribute('id')


def settled(page, index):
    page.wait_for_timeout(350)
    check(selected(page) == STOPS[index], f'Wrong panel: {selected(page)}, expected {STOPS[index]}')
    check(page.locator('.reading-panel').count() == 1, 'Shared panel was duplicated')
    check(page.locator('.reading-guide [aria-current="step"]').get_attribute('href') == '#' + STOPS[index], 'Wrong current link')
    check(page.locator('.reading-panel').evaluate('el => !el.inert && !el.hasAttribute("data-phase") && el.getAnimations().length === 0'), 'Panel did not settle')
    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Horizontal overflow')


def geometry(page):
    return page.locator('.reading-panel').evaluate('''el => ({
      top:el.offsetTop, height:el.offsetHeight, origin:el.parentElement.getBoundingClientRect().top+scrollY,
      clearance:el.getBoundingClientRect().top, scroll:scrollY
    })''')


def phase(page, name, direction, reduced):
    if reduced:
        check(page.locator('.reading-panel').evaluate('el => el.getAnimations().length === 0'), 'Reduced motion animated')
        return
    page.wait_for_function('(phase) => document.querySelector(".reading-panel").dataset.phase === phase', arg=name)
    state = page.locator('.reading-panel').evaluate('''el => ({
      transform:el.style.transform,
      animations:el.getAnimations().map(a=>({property:a.transitionProperty, duration:a.effect.getTiming().duration, easing:a.effect.getTiming().easing}))
    })''')
    if name == 'exit':
        check(state['transform'] == f'translateX({direction * 24}px)', f'Wrong exit direction: {state}')
    check(state['animations'] and all(a['property'] in ('transform', 'opacity') and abs(a['duration'] - (100 if name == 'exit' else 150)) < .5
          and a['easing'] == 'cubic-bezier(0.23, 1, 0.32, 1)' for a in state['animations']), f'Wrong transition: {state}')
    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Overflow during transition')


def touch(page, dx, dy=0):
    box = page.locator('.reading-panel').bounding_box()
    x, y = box['x'] + (60 if dx >= 0 else box['width'] - 60), max(220, box['y'] + 125)
    cdp = page.context.new_cdp_session(page)
    cdp.send('Input.dispatchTouchEvent', {'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
    for fraction in (.25,.5,.75,1):
        cdp.send('Input.dispatchTouchEvent', {'type':'touchMove','touchPoints':[{'x':x+dx*fraction,'y':y+dy*fraction}]})
        page.wait_for_timeout(20)
    cdp.send('Input.dispatchTouchEvent', {'type':'touchEnd','touchPoints':[]})
    cdp.detach()


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
            check(page.locator('.reading-enhanced').count() == 1, 'Progressive enhancement failed')
            positions = []
            for index in range(3):
                links.nth(index).click()
                if index:
                    phase(page, 'exit', 1, reduced)
                    if not reduced:
                        phase(page, 'enter', 1, False)
                settled(page, index)
                g = geometry(page)
                check(g['clearance'] >= page.locator('.site-header').bounding_box()['height'], 'Heading behind header')
                if width < 500:
                    nav = page.locator('.reading-guide').bounding_box()
                    check(g['clearance'] >= nav['y'] + nav['height'], 'Heading behind mobile guide')
                positions.append(g)
            page.screenshot(path=str(args.output/f'panel-{width}-{"reduce" if reduced else "normal"}.png'))
            links.nth(0).click()
            phase(page, 'exit', -1, reduced)
            settled(page, 0)
            # Natural document scroll exposes the end before crossing each boundary.
            # It must not be cancelled, force scrollY, or create a nested scroller.
            for index in (1, 2):
                boundary = positions[index]['origin'] + positions[index]['top'] - positions[index]['clearance']
                page.evaluate('y => scrollTo(0,y)', boundary - 4)
                page.wait_for_timeout(80)
                check(selected(page) == STOPS[index-1], 'Advanced before reading the complete panel')
                bottom = page.locator('.reading-panel').bounding_box()
                check(bottom['y'] + bottom['height'] <= page.viewport_size['height'] - 40, 'End not fully readable before advance')
                page.mouse.wheel(0, 12)
                page.wait_for_timeout(90)
                scroll = page.evaluate('scrollY')
                settled(page, index)
                check(abs(page.evaluate('scrollY') - scroll) < 1, 'Automatic change moved scrollY')
                check(page.locator('.reading-panel').evaluate('e=>getComputedStyle(e).overflowY === "visible"'), 'Nested scroll introduced')
            # Reversing native scroll revisits the preceding complete chapter.
            boundary = positions[2]['origin'] + positions[2]['top'] - positions[2]['clearance']
            page.evaluate('y => scrollTo(0,y)', boundary - 4)
            settled(page, 1)
            # Last action wins, whether interruption happens during exit or entry.
            for delay in (35, 130):
                links.nth(2).click()
                page.wait_for_timeout(delay)
                links.nth(0).click()
                settled(page, 0)
            # Keyboard activation and cancellation have no remaining motion.
            links.nth(2).focus()
            page.keyboard.press('Enter')
            check(page.locator('.reading-panel').evaluate('e=>e.getAnimations().length===0'), 'Keyboard animation')
            settled(page, 2)
            check(page.locator('#'+STOPS[2]).evaluate('el=>document.activeElement===el && getComputedStyle(el).outlineStyle==="solid"'), 'Keyboard target focus missing')
            links.nth(0).click()
            page.keyboard.press('Tab')
            settled(page, 0)
            if not reduced:
                links.nth(1).click()
                page.emulate_media(reduced_motion='reduce')
                check(page.locator('.reading-panel').evaluate('e=>e.getAnimations().length===0'), 'Preference change failed to cancel')
                settled(page, 1)
                page.emulate_media(reduced_motion='no-preference')
            # Recompute heights on enlarged text; all final actions must be reachable.
            page.locator('.text-size').click()
            links.nth(2).click()
            settled(page, 2)
            next_button = page.locator('[data-reading-next]')
            next_button.scroll_into_view_if_needed()
            check(next_button.is_visible() and next_button.is_disabled(), 'Last actions clipped')
            check(page.locator('.reading-actions').evaluate('''el=>{
              const box=el.getBoundingClientRect();
              return [...el.querySelectorAll('button')].every(button=>{
                const r=button.getBoundingClientRect();
                return r.left>=box.left-1 && r.right<=box.right+1;
              });
            }'''),'Enlarged-text controls are clipped by the panel')
            check(page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), 'Large text overflow')
            page.screenshot(path=str(args.output/f'large-{width}-{"reduce" if reduced else "normal"}.png'))
            # Native browser history and hash changes reveal hidden targets.
            page.evaluate('location.hash="lectura-brechas"')
            settled(page, 1)
            page.go_back()
            settled(page, 2)
            page.set_viewport_size({'width':720 if width == 1440 else 1000,'height':900})
            settled(page, 2)
            # Print shows every chapter despite their screen-only hidden state.
            page.emulate_media(media='print')
            check(page.locator('[data-reading-stage]').evaluate_all('els=>els.every(el=>el.getBoundingClientRect().height>0)'), 'Print loses chapters')
            check(page.locator('.reading-guide').is_hidden(), 'Print guide remains')
            check(not errors, '; '.join(errors))
            result = {'width':width,'reduced_motion':reduced,'status':'passed'}
            results.append(result)
            print(json.dumps(result), flush=True)
            context.close()
    # Actual Chromium touch events: horizontal navigation, natural vertical scroll,
    # no wrap at either end. This is emulation, not a physical-device assertion.
    for width in (390, 320):
        context = browser.new_context(viewport={'width':width,'height':800},is_mobile=True,has_touch=True)
        page=context.new_page()
        page.goto(BASE+'/#lectura-aprendizajes',wait_until='networkidle')
        settled(page,0)
        touch(page,130)
        settled(page,1)
        touch(page,-130)
        settled(page,0)
        touch(page,-130)
        settled(page,0)
        scroll=page.evaluate('scrollY')
        touch(page,0,-75)
        page.wait_for_timeout(150)
        check(page.evaluate('scrollY')>scroll,'Vertical touch scroll blocked')
        settled(page,0)
        # Synthetic cancellation and short/diagonal gestures must not navigate.
        for kind in ('short','diagonal','cancel'):
            page.locator('.reading-panel').evaluate('''(el,kind)=>{
              const event=(type,x,y)=>el.dispatchEvent(new PointerEvent(type,{bubbles:true,pointerType:'touch',isPrimary:true,pointerId:9,clientX:x,clientY:y}));
              event('pointerdown',80,250);
              event(kind==='cancel'?'pointercancel':'pointerup',kind==='short'?100:180,kind==='diagonal'?380:250);
            }''',kind)
            settled(page,0)
        page.locator('.reading-guide a').nth(2).click()
        settled(page,2)
        touch(page,130)
        settled(page,2)
        page.locator('.reading-guide a').first.click()
        settled(page,0)
        page.locator('.reading-guide a').first.focus()
        for key in ['Tab'] * 10 + ['Shift+Tab'] * 10:
            page.keyboard.press(key)
            check(page.evaluate('''() => {
              const el=document.activeElement;
              if(!el.closest('.reading-panel')) return true;
              const r=el.getBoundingClientRect(), nav=document.querySelector('.reading-guide').getBoundingClientRect();
              return r.top>=nav.bottom-1 && r.bottom<=innerHeight+1;
            }'''),'Sticky guide obscures keyboard focus')
        results.append({'case':'touch navigation, vertical scroll and cancellation','width':width,'status':'passed'})
        context.close()
    for fallback in ('no-js','no-observer','no-resize-observer'):
        context=browser.new_context(viewport={'width':320,'height':800},java_script_enabled=fallback!='no-js')
        if fallback=='no-observer': context.add_init_script('delete window.IntersectionObserver')
        if fallback=='no-resize-observer': context.add_init_script('delete window.ResizeObserver')
        page=context.new_page()
        page.goto(BASE,wait_until='networkidle')
        check(page.locator('[data-reading-stage]').evaluate_all('els=>els.every(e=>!e.hidden && e.getBoundingClientRect().height>0)'), 'Fallback loses content')
        for index in range(3):
            page.locator('.reading-guide a').nth(index).click()
            check(page.url.endswith('#'+STOPS[index]),'Fallback anchor failed')
        check(page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Fallback overflow')
        results.append({'fallback':fallback,'status':'passed'})
        context.close()
    page=browser.new_page(viewport={'width':390,'height':800})
    for stop in STOPS:
        page.goto(BASE+'/#'+stop,wait_until='networkidle')
        settled(page,STOPS.index(stop))
        check(page.locator('#'+stop).bounding_box()['y']>=150,'Deep link hidden by navigation')
    results.append({'case':'direct links to all chapters','status':'passed'})
    browser.close()
(args.output/'report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
