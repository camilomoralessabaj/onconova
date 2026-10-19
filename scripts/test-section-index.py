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
def aligned(page):
 page.wait_for_function(r'''() => {
  const indicator=document.querySelector('.chapter-indicator');
  const link=document.querySelector('.chapter-links [aria-current="location"]');
  if(!indicator || !link || indicator.getAnimations().some(a=>a.playState==='running')) return false;
  const values=getComputedStyle(indicator).clipPath.match(/inset\((.*?) round/)[1].split(' ').map(parseFloat);
  const [t,r=t,b=t,l=r]=values;
  const i=indicator.getBoundingClientRect(), a=link.getBoundingClientRect();
  return Math.abs(i.left+l-a.left)<=1 && Math.abs(i.top+t-a.top)<=1 &&
   Math.abs(i.width-l-r-a.width)<=1 && Math.abs(i.height-t-b-a.height)<=1;
 }''')
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
  aligned(page)
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
  aligned(page)
  screenshot(page,f'index-{width}x{height}-large')
  page.set_viewport_size({'width':height,'height':width});page.wait_for_timeout(150)
  page.locator('#historia').evaluate('e=>e.scrollIntoView()');active(page,'historia');visible_target(page,'historia')
  aligned(page)
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
 # Scroll geometry stays cached; reduced motion settles the capsule immediately.
 page=browser.new_page();page.goto(base+'/#prototipo');page.wait_for_timeout(100)
 page.evaluate('''() => {window.boxReads=0;const original=Element.prototype.getBoundingClientRect;Element.prototype.getBoundingClientRect=function(){window.boxReads++;return original.call(this)};}''')
 for _ in range(4):page.mouse.wheel(0,12);page.wait_for_timeout(40)
 assert page.evaluate('window.boxReads')==0,'Continuous scroll measures boxes'
 page.emulate_media(reduced_motion='reduce');page.locator('#historia').evaluate('e=>e.scrollIntoView()');active(page,'historia')
 assert page.locator('.section-index').evaluate('e=>e.getAnimations({subtree:true}).length')==0
 results.append({'case':'no-continuous-layout-and-reduced-motion','status':'passed'});page.close()
 # Normal motion, deterministic interruption from its presentation position,
 # then real rapid clicks in both directions (no disabled controls or queue).
 page=browser.new_page(viewport={'width':1440,'height':900});page.goto(base,wait_until='networkidle');aligned(page)
 assert page.locator('.chapter-indicator').count()==1
 assert page.locator('.chapter-indicator').get_attribute('aria-hidden')=='true'
 assert page.locator('.chapter-indicator').evaluate('e=>e.inert && getComputedStyle(e).pointerEvents==="none"')
 assert page.locator('.chapter-indicator a,.chapter-indicator [id],.chapter-indicator [tabindex]').count()==0
 assert page.locator('.chapter-links [role="tab"],.chapter-links [aria-selected]').count()==0
 motion=page.evaluate('''async () => {
  const indicator=document.querySelector('.chapter-indicator');
  const link=id=>document.querySelector(`.chapter-links a[href="#${id}"]`);
  const frame=()=>new Promise(requestAnimationFrame);
  link('propuesta').click();
  while(!indicator.getAnimations().length) await frame();
  const first=indicator.getAnimations()[0];
  first.pause(); first.currentTime=70;
  const before=getComputedStyle(indicator).clipPath;
  const timing=first.effect.getTiming();
  link('desafio').click();
  while(document.querySelector('.chapter-links [aria-current]').hash!=='#desafio') await frame();
  const second=indicator.getAnimations()[0];
  return {before,from:second.effect.getKeyframes()[0].clipPath,duration:timing.duration,easing:timing.easing};
 }''')
 assert motion['before']==motion['from'],motion
 assert abs(motion['duration']-200)<.001 and motion['easing']=='cubic-bezier(0.23, 1, 0.32, 1)',motion
 for id in ['iteracion','historia','preguntas','propuesta']:
  page.locator(f'.chapter-links a[href="#{id}"]').click();page.wait_for_timeout(35)
 active(page,'propuesta');aligned(page)
 assert page.locator('.chapter-indicator').evaluate('e=>e.getAnimations().filter(a=>a.playState==="running").length')==0
 # Changing the preference while moving must cancel motion, not just prevent
 # the next animation. Returning to normal must allow subsequent movement.
 page.locator('.chapter-links a[href="#historia"]').click()
 page.wait_for_function('document.querySelector(".chapter-indicator").getAnimations().some(a=>a.playState==="running")')
 page.emulate_media(reduced_motion='reduce');aligned(page)
 assert page.locator('.chapter-indicator').evaluate('e=>e.getAnimations().length')==0
 page.emulate_media(reduced_motion='no-preference')
 page.locator('.chapter-links a[href="#propuesta"]').click()
 page.wait_for_function('document.querySelector(".chapter-indicator").getAnimations().some(a=>a.playState==="running")')
 # Resize mid-flight and then enlarge text without changing chapter.
 page.set_viewport_size({'width':390,'height':800});aligned(page)
 page.locator('.text-size').click();page.wait_for_timeout(100);aligned(page)
 page.locator('.chapter-links a[href="#historia"]').focus();page.keyboard.press('Enter');active(page,'historia')
 assert page.locator('.chapter-indicator').evaluate('e=>e.getAnimations().length')==0
 aligned(page)
 # Full focus outline fits inside the scroller; focused link beats auto-centering.
 page.locator('.chapter-links a[href="#historia"]').focus()
 page.keyboard.press('Tab')
 page.evaluate('()=>new Promise(requestAnimationFrame)')
 focus=page.evaluate('''() => {const t=document.querySelector('.chapter-links').getBoundingClientRect(), f=document.activeElement.getBoundingClientRect();return {left:f.left-t.left,right:t.right-f.right,top:f.top-t.top,bottom:t.bottom-f.bottom}}''')
 assert min(focus.values())>=5,focus
 # Modified navigation keys (Ctrl+Home, browser history shortcuts) are keyboard
 # input too: they must settle a pointer-triggered transition immediately.
 page.locator('.chapter-links a[href="#propuesta"]').click()
 page.keyboard.press('Control+Home');page.wait_for_timeout(100)
 assert page.locator('.chapter-indicator').evaluate('e=>e.getAnimations().length')==0
 results.append({'case':'capsule-interruption-preference-resize-keyboard','status':'passed','motion':motion});page.close()
 context=browser.new_context(viewport={'width':390,'height':800},is_mobile=True,has_touch=True)
 page=context.new_page();page.goto(base+'/#historia',wait_until='networkidle');aligned(page)
 track=page.locator('.chapter-links');track.evaluate('e=>e.scrollLeft=0')
 box=track.bounding_box();x=box['x']+box['width']-30;y=box['y']+box['height']/2
 scroll=page.evaluate('scrollY');cdp=context.new_cdp_session(page)
 cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
 for distance in [40,80,120,160,220]:
  cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-distance,'y':y}]});page.wait_for_timeout(25)
 cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});page.wait_for_timeout(500)
 position=track.evaluate('e=>e.scrollLeft')
 assert position>100 and abs(page.evaluate('scrollY')-scroll)<1,(position,scroll)
 page.locator('#propuesta').evaluate('e=>e.scrollIntoView()');active(page,'propuesta');aligned(page)
 assert abs(track.evaluate('e=>e.scrollLeft')-position)<1,'Scroll following fought strip exploration'
 results.append({'case':'touch-strip-keeps-user-position','status':'passed','scrollLeft':position})
 context.close();browser.close()
 # Chromium's native page zoom preference (not CSS zoom or device scale emulation).
 profile=a.output/'zoom-profile';(profile/'Default').mkdir(parents=True,exist_ok=True)
 (profile/'Default'/'Preferences').write_text(json.dumps({'partition':{'default_zoom_level':{'x':math.log(2)/math.log(1.2)}}}))
 context=pw.chromium.launch_persistent_context(str(profile),executable_path=shutil.which('chromium'),headless=True,no_viewport=True,args=['--no-sandbox','--window-size=1440,1000'])
 page=context.pages[0];page.goto(base+'/#propuesta',wait_until='networkidle');active(page,'propuesta');visible_target(page,'propuesta')
 aligned(page)
 metrics=page.evaluate('({inner:innerWidth,outer:outerWidth,dpr:devicePixelRatio,scale:visualViewport.scale})')
 assert metrics['dpr']>=1.99 and metrics['inner']<=metrics['outer']/1.9,metrics
 # Capture compositor pixels directly: Playwright's no-viewport helper resets
 # screenshot metrics at native zoom and can return a blank CSS-size surface.
 capture=context.new_cdp_session(page).send('Page.captureScreenshot',{'format':'png','fromSurface':True})
 (a.output/'native-zoom-200.png').write_bytes(base64.b64decode(capture['data']))
 results.append({'case':'native-zoom-200','status':'passed','metrics':metrics});context.close()
(a.output/'report.json').write_text(json.dumps({'status':'passed','results':results},ensure_ascii=False,indent=2))
print(json.dumps({'status':'passed','cases':len(results)},ensure_ascii=False))
