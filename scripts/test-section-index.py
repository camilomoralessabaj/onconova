#!/usr/bin/env python3
"""Regression checks for the native chapter index; requires Playwright/Chromium."""
import argparse,json,shutil,math,base64
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--base-url',default='http://127.0.0.1:4173')
p.add_argument('--output',type=Path,default=Path('.local/section-index'))
a=p.parse_args();url=urlsplit(a.base_url)
if url.scheme not in ('http','https') or url.hostname not in ('localhost','127.0.0.1','::1') or url.username or url.password or url.query or url.fragment:p.error('Use a local test server URL')
a.output.mkdir(parents=True,exist_ok=True);base=a.base_url.rstrip('/')
ids=['inicio','desafio','historia','propuesta','iteracion','prototipo','preguntas','validacion','aprendizajes','fuentes']
results=[]
def active(page,id):
 page.wait_for_function('(id)=>document.querySelector(".section-index [aria-current=location]")?.hash==="#"+id',arg=id)
 assert page.locator('.section-index [aria-current]').count()==1
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Document overflow'
def visible_target(page,id):
 box=page.locator('#'+id).bounding_box()
 bottom=page.evaluate('''Math.max(0,...[...document.querySelectorAll('.site-header,.section-index')].filter(e=>getComputedStyle(e).position==='sticky').map(e=>e.getBoundingClientRect().bottom))''')
 assert box['y']>=bottom-1,(id,'Target obscured',box,bottom)
def screenshot(page,name):page.screenshot(path=str(a.output/(name+'.png')))
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 for width,height in [(1440,900),(390,800),(320,800),(844,390),(320,256)]:
  context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
  page.goto(base+'/#historia',wait_until='networkidle');active(page,'historia');visible_target(page,'historia')
  # Forward and backward reading, including fast jumps and bottom of document.
  for id in ids+list(reversed(ids)):
   page.locator('#'+id).evaluate('e=>e.scrollIntoView({block:"start"})');active(page,id)
  # Native links and native Back/Forward preserve meaningful destinations.
  for id in ['historia','propuesta','validacion']:
   page.locator(f'.chapter-links a[href="#{id}"]').click();active(page,id);visible_target(page,id)
  page.go_back();active(page,'propuesta');page.go_forward();active(page,'validacion')
  for id,parent in [('resultados','validacion'),('proximos-pasos','aprendizajes'),('fuente-S01','fuentes')]:
   page.goto(base+'/#'+id,wait_until='networkidle');active(page,parent);visible_target(page,id)
  # Scroll changes must not steal focus, announce every chapter or create history.
  page.locator('.text-size').focus();focus=page.evaluate('document.activeElement.className');history=page.evaluate('history.length')
  page.locator('#desafio').evaluate('e=>e.scrollIntoView()');active(page,'desafio')
  assert page.evaluate('document.activeElement.className')==focus
  assert page.evaluate('history.length')==history
  assert page.locator('.section-index [aria-live],.section-index[aria-live]').count()==0
  # Tab/Shift+Tab/Enter; the browser scrolls only the native strip as necessary.
  link=page.locator('.chapter-links a[href="#historia"]');link.focus();page.keyboard.press('Tab');page.keyboard.press('Shift+Tab')
  assert link.evaluate('e=>document.activeElement===e && getComputedStyle(e).outlineStyle!=="none"')
  assert link.bounding_box()['y']>=0
  page.keyboard.press('Enter');active(page,'historia');visible_target(page,'historia')
  assert page.locator('.chapter-links a').evaluate_all('els=>els.every(e=>e.getBoundingClientRect().height>=44 && e.getBoundingClientRect().width>=44)')
  page.locator('.text-size').click();page.wait_for_timeout(120)
  page.locator('.chapter-links a[href="#propuesta"]').click();active(page,'propuesta');visible_target(page,'propuesta')
  screenshot(page,f'index-{width}x{height}-large')
  page.set_viewport_size({'width':height,'height':width});page.wait_for_timeout(150)
  page.locator('#historia').evaluate('e=>e.scrollIntoView()');active(page,'historia');visible_target(page,'historia')
  assert not errors,errors
  results.append({'viewport':[width,height],'status':'passed','cases':['bidirectional','deep-link','aliases','back-forward','keyboard','no-focus-steal','large-text','orientation'],'errors':errors})
  context.close()
 # No JavaScript: essential links and narrative, no fictitious active chapter.
 context=browser.new_context(java_script_enabled=False,viewport={'width':320,'height':800});page=context.new_page();page.goto(base)
 assert page.locator('.chapter-links a').count()==10
 assert page.locator('.chapter-links [aria-current]').count()==0
 assert page.locator('.section-index').evaluate('e=>getComputedStyle(e).position')=='static'
 page.locator('.chapter-links a[href="#historia"]').click();assert page.url.endswith('#historia')
 assert page.locator('#desafio .study-problem').is_visible()
 results.append({'case':'no-js','status':'passed'});context.close()
 # Exact reduced-motion policy: new index never animates, existing guide retains its token.
 page=browser.new_page();page.goto(base+'/#prototipo');page.wait_for_timeout(100)
 page.evaluate('''() => {window.boxReads=0;const original=Element.prototype.getBoundingClientRect;Element.prototype.getBoundingClientRect=function(){window.boxReads++;return original.call(this)};}''')
 for _ in range(4):page.mouse.wheel(0,12);page.wait_for_timeout(40)
 assert page.evaluate('window.boxReads')==0,'Continuous scroll measures boxes'
 page.emulate_media(reduced_motion='reduce');page.locator('#historia').evaluate('e=>e.scrollIntoView()');active(page,'historia')
 assert page.locator('.section-index').evaluate('e=>e.getAnimations({subtree:true}).length')==0
 results.append({'case':'no-continuous-layout-and-reduced-motion','status':'passed'});page.close();browser.close()
 # Chromium's native page zoom preference (not CSS zoom or device scale emulation).
 profile=a.output/'zoom-profile';(profile/'Default').mkdir(parents=True,exist_ok=True)
 (profile/'Default'/'Preferences').write_text(json.dumps({'partition':{'default_zoom_level':{'x':math.log(2)/math.log(1.2)}}}))
 context=pw.chromium.launch_persistent_context(str(profile),executable_path=shutil.which('chromium'),headless=True,no_viewport=True,args=['--no-sandbox','--window-size=1440,1000'])
 page=context.pages[0];page.goto(base+'/#propuesta',wait_until='networkidle');active(page,'propuesta');visible_target(page,'propuesta')
 metrics=page.evaluate('({inner:innerWidth,outer:outerWidth,dpr:devicePixelRatio,scale:visualViewport.scale})')
 assert metrics['dpr']>=1.99 and metrics['inner']<=metrics['outer']/1.9,metrics
 # Capture compositor pixels directly: Playwright's no-viewport helper resets
 # screenshot metrics at native zoom and can return a blank CSS-size surface.
 capture=context.new_cdp_session(page).send('Page.captureScreenshot',{'format':'png','fromSurface':True})
 (a.output/'native-zoom-200.png').write_bytes(base64.b64decode(capture['data']))
 results.append({'case':'native-zoom-200','status':'passed','metrics':metrics});context.close()
(a.output/'report.json').write_text(json.dumps({'status':'passed','results':results},ensure_ascii=False,indent=2))
print(json.dumps({'status':'passed','cases':len(results)},ensure_ascii=False))
