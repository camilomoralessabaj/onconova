#!/usr/bin/env python3
"""Local regression checks for the floating reading cards. Requires Playwright/Chromium."""
import argparse
import base64
import json
import math
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


def enhanced(page):
    return page.locator('.reading-enhanced').count() == 1


def selected(page):
    return page.locator('[data-reading-select][aria-pressed="true"]').get_attribute('aria-controls')


def obstruction(page):
    return page.evaluate('Math.max(0,...[...document.querySelectorAll(".site-header,.section-index")].filter(e=>getComputedStyle(e).position==="sticky").map(e=>e.getBoundingClientRect().bottom))')


def settled(page, index):
    page.wait_for_timeout(360)
    if enhanced(page):
        check(selected(page) == STOPS[index], f'Wrong card: {selected(page)}, expected {STOPS[index]}')
        check(page.locator('[data-reading-stage]:not([hidden])').get_attribute('id') == STOPS[index], 'Visible content differs from selection')
        check(page.locator('[data-reading-card][data-depth="2"]').count() == 1, 'Deck has no unique front card')
        check(page.locator('[data-reading-stage]').evaluate_all('els=>els.every(el=>el.hidden===el.inert)'), 'Inactive content is focusable')
    else:
        check(page.locator('[data-reading-stage]').evaluate_all('els=>els.every(el=>!el.hidden&&!el.inert&&el.getBoundingClientRect().height>0)'), 'Linear layout loses content')
    check(page.locator('.reading-panel').count() == 1, 'Deck was duplicated')
    check(page.locator('[data-reading-card]').evaluate_all('els=>els.every(el=>el.getAnimations().length===0&&getComputedStyle(el).opacity==="1")'), 'Cards did not settle')
    check(page.locator('[data-reading-stage]').evaluate_all('els=>els.map(e=>e.id).join("|")==="lectura-aprendizajes|lectura-brechas|proximos-pasos"'), 'Canonical DOM order changed')
    check(page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), 'Horizontal overflow')


def choose(page, index):
    if enhanced(page):
        page.locator('[data-reading-select]').nth(index).click()
    else:
        page.locator('.reading-guide a').nth(index).click()
    settled(page, index)


def geometry(page):
    return page.locator('.reading-panel').evaluate('''el=>({
      top:el.offsetTop,height:el.offsetHeight,origin:el.parentElement.getBoundingClientRect().top+scrollY,
      clearance:el.getBoundingClientRect().top,scroll:scrollY
    })''')


def motion(page, index, reduced):
    # Dispatch pointer activation synchronously to sample the transition before a
    # Playwright locator waits for moving buttons to become stable.
    state = page.locator('[data-reading-select]').nth(index).evaluate('''el=>{
      const before=[...document.querySelectorAll('[data-reading-card]')].map(e=>getComputedStyle(e).transform);
      el.dispatchEvent(new MouseEvent('click',{bubbles:true,detail:1}));
      const cards=[...document.querySelectorAll('[data-reading-card]')];
      return {before,after:cards.map(e=>getComputedStyle(e).transform),animations:cards.flatMap(e=>e.getAnimations().map(a=>({property:a.transitionProperty,duration:a.effect.getTiming().duration,easing:a.effect.getTiming().easing}))) };
    }''')
    if reduced:
        check(not state['animations'], 'Reduced motion animated')
    else:
        check(state['animations'] and all(a['property']=='transform' and 0<a['duration']<=300 and a['easing']=='cubic-bezier(0.23, 1, 0.32, 1)' for a in state['animations']), f'Wrong deck transition: {state}')
        check(state['before']==state['after'], 'Motion jumped instead of starting at the presentation value')
    check(page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), 'Overflow during motion')


def capture(page, width, index):
    # Capture the entire selected card (including content below the viewport)
    # without scrolling it into view, which would advance the reading narrative.
    box=page.locator('.reading-panel' if enhanced(page) else '#'+STOPS[index]).bounding_box()
    y=page.evaluate('scrollY')+box['y']
    cdp=page.context.new_cdp_session(page)
    screenshot=cdp.send('Page.captureScreenshot',{'format':'png','fromSurface':True,'captureBeyondViewport':True,
        'clip':{'x':max(0,box['x']-12),'y':max(0,y-12),'width':min(width,box['width']+24),'height':box['height']+24,'scale':1}})
    cdp.detach()
    data=base64.b64decode(screenshot['data'])
    check(len(data)>10000,'Screenshot contains no card content')
    (args.output/f'card-{width}-{index+1}.png').write_bytes(data)


def touch(page, dx, dy=0):
    box=page.locator('.reading-panel').bounding_box()
    x,y=box['x']+(60 if dx>=0 else box['width']-60),max(250,box['y']+220)
    cdp=page.context.new_cdp_session(page)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
    for fraction in (.25,.5,.75,1):
        cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+dx*fraction,'y':y+dy*fraction}]})
        page.wait_for_timeout(20)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    cdp.detach()


with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    for width in (1440,390,320):
        for reduced in (False,True):
            context=browser.new_context(viewport={'width':width,'height':900 if width==1440 else 800},
                reduced_motion='reduce' if reduced else 'no-preference',is_mobile=width<500,has_touch=width<500)
            page=context.new_page()
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
            page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
            page.goto(BASE+'/#aprendizajes',wait_until='networkidle')
            settled(page,0)
            check(enhanced(page)==(width>=360),'Wrong responsive reading mode')
            check(page.locator('#aprendizajes-title').inner_text()=='Aprendizajes, Brechas y Próximos Pasos','Heading changed')
            check(page.locator('.learning-heading').evaluate('el=>getComputedStyle(el).textAlign==="center"'),'Heading is not centered')
            check('Se mantiene el enfoque conceptual. Las próximas iteraciones buscarán' not in page.locator('.learning-section').inner_text(),'Removed introduction remains')
            if not reduced:
                page.screenshot(path=str(args.output/f'heading-{width}.png'))
            positions=[]
            for index in range(3):
                choose(page,index)
                check(page.url.endswith('#'+STOPS[index]),'Selection hash mismatch')
                if enhanced(page):
                    g=geometry(page)
                    positions.append(g)
                    check(g['clearance']>=obstruction(page)+14,'Deck behind global navigation')
                    # Exposed background titles have a real 44px-high hit area.
                    check(page.locator('[data-reading-select]').evaluate_all('''els=>els.every(el=>{
                      const r=el.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+32;
                      return r.height>=44&&[-21,0,21].every(d=>el.contains(document.elementFromPoint(x,y+d)));
                    })'''),'A background title cannot be selected directly')
                    # The immediately following wheel event stays at this stop.
                    page.mouse.wheel(0,12)
                    settled(page,index)
                    # Re-select to capture the exact milestone rather than +12.
                    choose(page,index)
                else:
                    check(page.locator('#'+STOPS[index]).bounding_box()['y']>=obstruction(page)+20,'Linear anchor hidden')
                if not reduced:
                    capture(page,width,index)
            if enhanced(page):
                choose(page,0)
                # Every selection preserves canonical forward/backward boundaries.
                for start in (0,1,2):
                    choose(page,start)
                    for index in range(start+1,3):
                        boundary=positions[index]['scroll']
                        page.evaluate('y=>scrollTo(0,y)',boundary-4)
                        page.wait_for_timeout(80)
                        check(selected(page)==STOPS[index-1],'Advanced before the complete card was readable')
                        box=page.locator('.reading-panel').bounding_box()
                        check(box['y']+box['height']<=page.viewport_size['height']-40,'End of card not readable before advance')
                        page.mouse.wheel(0,12)
                        page.wait_for_timeout(90)
                        scroll=page.evaluate('scrollY')
                        settled(page,index)
                        check(abs(page.evaluate('scrollY')-scroll)<1,'Automatic card change moved the document')
                    choose(page,start)
                    for index in range(start,0,-1):
                        page.evaluate('y=>scrollTo(0,y)',positions[index]['scroll']-4)
                        settled(page,index-1)
                check(page.locator('.reading-panel').evaluate('e=>getComputedStyle(e).overflowY==="visible"'),'Nested scroll introduced')
                # Exit the section naturally; reversing revisits the last card.
                choose(page,2)
                page.locator('#fuentes-title').scroll_into_view_if_needed()
                check(page.locator('#fuentes-title').bounding_box()['y']>=obstruction(page),'Section exit obscured')
                choose(page,2)
                # Forward/reverse transitions and last-input-wins interruptions.
                motion(page,0,reduced)
                settled(page,0)
                motion(page,2,reduced)
                settled(page,2)
                for delay in (35,130):
                    motion(page,0,reduced)
                    page.wait_for_timeout(delay)
                    motion(page,1,reduced)
                    page.wait_for_timeout(25)
                    motion(page,2,reduced)
                    settled(page,2)
                buttons=page.locator('[data-reading-select]')
                for index,key in ((0,'Enter'),(1,'Space'),(2,'Enter')):
                    buttons.nth(index).focus()
                    page.keyboard.press(key)
                    settled(page,index)
                    check(page.locator('#'+STOPS[index]).evaluate('el=>document.activeElement===el&&getComputedStyle(el).outlineStyle==="solid"'),'Keyboard target/focus missing')
                motion(page,0,reduced)
                page.keyboard.press('Tab')
                settled(page,0)
                if not reduced:
                    motion(page,1,False)
                    page.emulate_media(reduced_motion='reduce')
                    settled(page,1)
                    page.emulate_media(reduced_motion='no-preference')
                choose(page,0)
                buttons.first.focus()
                for key in ['Tab']*10+['Shift+Tab']*10:
                    page.keyboard.press(key)
                    check(page.evaluate('''()=>{
                      const el=document.activeElement;
                      if(!el.closest('.reading-panel'))return true;
                      const r=el.getBoundingClientRect();
                      const obstruction=Math.max(0,...[...document.querySelectorAll('.site-header,.section-index')].filter(e=>getComputedStyle(e).position==='sticky').map(e=>e.getBoundingClientRect().bottom));
                      return !el.inert&&!el.closest('[hidden],[inert]')&&r.top>=obstruction-1&&r.bottom<=innerHeight+1;
                    }'''),'Navigation obscures keyboard focus or exposes hidden content')
            # Source links still open their evidence, and the demo return stays native.
            choose(page,0)
            page.locator('#lectura-aprendizajes a[href="#fuente-S01"]').click()
            check(page.locator('.source-details').get_attribute('open') is not None,'Source link did not open evidence')
            check(page.locator('#fuente-S01').bounding_box()['y']>=obstruction(page),'Source anchor obscured')
            choose(page,2)
            page.locator('#proximos-pasos>.button').click()
            check(page.url.endswith('#prototipo'),'Return to demonstration failed')
            # Enlarged text returns all content to flow; final actions stay usable.
            page.locator('.text-size').click()
            page.wait_for_timeout(100)
            check(not enhanced(page),'Enlarged text did not reflow')
            choose(page,2)
            if width<500:
                check(page.locator('.iteration-table tbody tr').first.evaluate('el=>{const s=getComputedStyle(el);return Math.abs(el.clientWidth-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight)-el.querySelector("th").getBoundingClientRect().width)<2}'),'Mobile action is restricted to a table column')
            last=page.locator('#proximos-pasos>.button')
            last.scroll_into_view_if_needed()
            check(last.is_visible(),'Final link clipped')
            check(page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Large text overflow')
            page.screenshot(path=str(args.output/f'large-{width}-{"reduce" if reduced else "normal"}.png'))
            # History, reload and resizing retain target content in both modes.
            page.evaluate('location.hash="lectura-brechas"')
            settled(page,1)
            page.go_back()
            settled(page,2)
            page.reload(wait_until='networkidle')
            settled(page,2)
            page.set_viewport_size({'width':720 if width==1440 else 1000,'height':900})
            settled(page,2)
            # Browser-independent text enlargement to 200%, in addition to AA.
            page.add_style_tag(content=':root{font-size:200%!important}')
            page.wait_for_timeout(120)
            check(not enhanced(page),'200% text did not reflow')
            check(page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'200% text overflow')
            page.emulate_media(media='print')
            check(page.locator('[data-reading-stage]').evaluate_all('els=>els.every(e=>e.getBoundingClientRect().height>0)'),'Print loses content')
            check(page.locator('.reading-guide').is_hidden(),'Print guide remains')
            check(not errors,'; '.join(errors))
            result={'width':width,'reduced_motion':reduced,'status':'passed'}
            results.append(result)
            print(json.dumps(result),flush=True)
            context.close()
    # Real Chromium touch events, including the existing optional swipe shortcut.
    context=browser.new_context(viewport={'width':390,'height':800},is_mobile=True,has_touch=True)
    page=context.new_page()
    page.goto(BASE+'/#lectura-aprendizajes',wait_until='networkidle')
    for index in (1,2,0):
        page.locator('[data-reading-select]').nth(index).tap()
        settled(page,index)
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
    for kind in ('short','diagonal','cancel'):
        page.locator('.reading-panel').evaluate('''(el,kind)=>{
          const event=(type,x,y)=>el.dispatchEvent(new PointerEvent(type,{bubbles:true,pointerType:'touch',isPrimary:true,pointerId:9,clientX:x,clientY:y}));
          event('pointerdown',80,250);event(kind==='cancel'?'pointercancel':'pointerup',kind==='short'?100:180,kind==='diagonal'?380:250);
        }''',kind)
        settled(page,0)
    choose(page,2)
    touch(page,130)
    settled(page,2)
    results.append({'case':'touch selection, swipe, vertical scroll and cancellation','status':'passed'})
    context.close()
    for fallback in ('no-js','no-observer','no-resize-observer'):
        context=browser.new_context(viewport={'width':390,'height':800},java_script_enabled=fallback!='no-js')
        if fallback=='no-observer':context.add_init_script('delete window.IntersectionObserver')
        if fallback=='no-resize-observer':context.add_init_script('delete window.ResizeObserver')
        page=context.new_page()
        page.goto(BASE,wait_until='networkidle')
        check(not enhanced(page),'Fallback enhanced unexpectedly')
        check(page.locator('[data-reading-stage]').evaluate_all('els=>els.every(e=>!e.hidden&&e.getBoundingClientRect().height>0)'),'Fallback loses content')
        for index in range(3):
            choose(page,index)
            check(page.url.endswith('#'+STOPS[index]),'Fallback anchor failed')
        results.append({'fallback':fallback,'status':'passed'})
        context.close()
    for width in (1440,390,320):
        page=browser.new_page(viewport={'width':width,'height':900 if width==1440 else 800})
        for index,stop in enumerate(STOPS):
            page.goto(BASE+'/#'+stop,wait_until='networkidle')
            settled(page,index)
            page.reload(wait_until='networkidle')
            settled(page,index)
            target=page.locator('[data-reading-select][aria-pressed="true"]' if enhanced(page) else '#'+stop)
            check(target.bounding_box()['y']>=obstruction(page)+20,'Deep link hidden by navigation')
        # Print from an enhanced state also exposes previously hidden content.
        page.emulate_media(media='print')
        check(page.locator('[data-reading-stage]').evaluate_all('els=>els.every(e=>e.getBoundingClientRect().height>0)'),'Enhanced print loses chapters')
        if width==1440:page.pdf(path=str(args.output/'print.pdf'),format='A4')
        results.append({'case':'direct links, reload and print','width':width,'status':'passed'})
        page.close()
    browser.close()
    # Native browser zoom, not CSS zoom or device-scale emulation.
    profile=args.output/'zoom-profile'
    (profile/'Default').mkdir(parents=True,exist_ok=True)
    (profile/'Default'/'Preferences').write_text(json.dumps({'partition':{'default_zoom_level':{'x':math.log(2)/math.log(1.2)}}}))
    context=p.chromium.launch_persistent_context(str(profile),executable_path=shutil.which('chromium'),headless=True,no_viewport=True,args=['--no-sandbox','--window-size=1440,1000'])
    page=context.pages[0]
    page.goto(BASE+'/#aprendizajes',wait_until='networkidle')
    metrics=page.evaluate('({inner:innerWidth,outer:outerWidth,dpr:devicePixelRatio})')
    check(metrics['dpr']>=1.99 and metrics['inner']<=metrics['outer']/1.9,'Native zoom is not 200%')
    for index in range(3):
        choose(page,index)
        check(page.locator('#'+STOPS[index]).bounding_box()['y']>=obstruction(page),'Zoom anchor obscured')
    screenshot=context.new_cdp_session(page).send('Page.captureScreenshot',{'format':'png','fromSurface':True})
    (args.output/'native-zoom-200.png').write_bytes(base64.b64decode(screenshot['data']))
    results.append({'case':'native browser zoom 200%','status':'passed','metrics':metrics})
    context.close()
(args.output/'report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
