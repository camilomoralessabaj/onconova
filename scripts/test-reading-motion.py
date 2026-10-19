#!/usr/bin/env python3
"""Check visible continuity at reading milestones, not just final card selection.

Requires local Playwright/Chromium. Outputs measurements only; no dependencies
are added to the site. Run alongside test-reading-guide.py for the full journey.
"""
import argparse
import json
import shutil
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='http://127.0.0.1:4173')
parser.add_argument('--output', type=Path, default=Path('work/qa-reading-motion'))
args = parser.parse_args()
url = urlsplit(args.base_url)
if (url.scheme not in ('http', 'https') or url.hostname not in ('127.0.0.1', 'localhost', '::1')
        or url.username or url.password or url.query or url.fragment):
    parser.error('Use a local test server URL without credentials, query or fragment')
args.output.mkdir(parents=True, exist_ok=True)
results = []


def settled(page):
    page.wait_for_function('''() => {
      const panel = document.querySelector('.reading-panel');
      return panel.getAnimations({subtree:true}).length === 0 &&
        [...panel.querySelectorAll('[data-reading-stage]')].every(e => !e.inert || e.hidden);
    }''')


def choose(page, index):
    page.locator('[data-reading-select]').nth(index).click()
    settled(page)


def cross(page, target):
    # Observe the first committed visual state in the same frame as the card
    # change. Subtract native scrolling: only the layout jump must be bridged.
    return page.evaluate('''target => new Promise(resolve => {
      const panel = document.querySelector('.reading-panel');
      let start = panel.getBoundingClientRect().top;
      let scroll = scrollY;
      // Read again in the upcoming animation frame, before the scroll render:
      // an in-flight transition may legitimately advance while input is queued.
      requestAnimationFrame(() => {
        start = panel.getBoundingClientRect().top;
        scroll = scrollY;
      });
      const observer = new MutationObserver(() => {
        observer.disconnect();
        const content = panel.querySelector('[data-reading-stage]:not([inert])');
        resolve({
          expected: start - (scrollY - scroll), actual: panel.getBoundingClientRect().top,
          scroll: scrollY, target, selected: content.id,
          panelAnimations: panel.getAnimations().length,
          contentAnimations: content.getAnimations().map(a => a.transitionProperty)
        });
      });
      observer.observe(panel, {subtree:true, attributes:true, attributeFilter:['data-depth']});
      document.dispatchEvent(new WheelEvent('wheel', {deltaY:target-scroll}));
      scrollTo({top:target, behavior:'instant'});
    })''', target)


def choreography(page, source, destination):
    choose(page, source)
    # Inspect effective CSS timelines, not elapsed wall-clock guesses. Keeping
    # transforms and depth on the same curve lets opaque cards exchange order
    # at their spatial crossing, including direct non-adjacent selections.
    data = page.locator('[data-reading-select]').nth(destination).evaluate('''button => {
      const panel = button.closest('.reading-panel');
      const cards = [...panel.querySelectorAll('[data-reading-card]')];
      const stages = cards.map(c => c.querySelector('[data-reading-stage]'));
      const snapshot = () => cards.map((c, i) => {
        const style = getComputedStyle(c), matrix = new DOMMatrix(style.transform);
        return {y:matrix.m42, z:Number(style.zIndex), height:parseFloat(style.height), opacity:Number(getComputedStyle(stages[i]).opacity),
          hidden:stages[i].hidden, inert:stages[i].inert, aria:stages[i].getAttribute('aria-hidden')};
      });
      const before = snapshot();
      button.dispatchEvent(new MouseEvent('click', {bubbles:true, detail:1}));
      const animations = panel.getAnimations({subtree:true});
      animations.forEach(a => a.pause());
      const timing = animations.map(a => ({property:a.transitionProperty,
        duration:a.effect.getTiming().duration, easing:a.effect.getTiming().easing,
        target:a.effect.target.className}));
      const samples = [0,100,300,450].map(time => {
        animations.forEach(a => { a.currentTime = time; });
        return {time, cards:snapshot()};
      });
      animations.forEach(a => a.play());
      return {before, timing, samples};
    }''')
    start, early, _, late = [sample['cards'] for sample in data['samples']]
    for a, b in zip(data['before'], start):
        assert abs(a['y'] - b['y']) < .1 and a['z'] == b['z'] and abs(a['height']-b['height']) < .1, data
    assert not start[source]['hidden'] and start[source]['inert'] and start[source]['aria'] == 'true', data
    assert not start[destination]['inert'] and start[destination]['opacity'] < .1, data
    assert early[source]['z'] > early[destination]['z'], data
    assert late[source]['z'] < late[destination]['z'], data
    assert 0 < early[source]['opacity'] < 1, data
    assert abs(early[source]['y'] - start[source]['y']) > 1, data
    assert abs(early[destination]['y'] - start[destination]['y']) > 1, data
    for sample in data['samples']:
        for card in sample['cards']:
            assert abs(card['z'] - card['y'] * 200 / 128) < 1, data
    spatial = [a for a in data['timing'] if a['property'] in ('transform','z-index','height')]
    assert spatial and all(a['duration'] == 600 and a['easing'] == 'cubic-bezier(0.4, 0, 0.2, 1)' for a in spatial), data
    arrival = [a for a in data['timing'] if a['property'] == 'opacity' and a['duration'] == 200]
    assert arrival and all(a['easing'] == 'cubic-bezier(0.23, 1, 0.32, 1)' for a in arrival), data
    # The measured card surfaces resize continuously, then hide departing text
    # without a late collapse. The test deliberately covers unequal heights.
    assert any(a['property']=='height' for a in spatial), data
    for a,b in zip(early,late):
        assert abs(a['height']-b['height'])>1, data
    page.locator('.reading-panel').evaluate('''p=>{
      const animations=p.getAnimations({subtree:true});
      animations.forEach(a=>{a.pause();a.currentTime=599});
    }''')
    before_end=page.locator('[data-reading-card]').evaluate_all('els=>els.map(e=>parseFloat(getComputedStyle(e).height))')
    page.locator('.reading-panel').evaluate('p=>p.getAnimations({subtree:true}).forEach(a=>a.finish())')
    settled(page)
    after_end=page.locator('[data-reading-card]').evaluate_all('els=>els.map(e=>parseFloat(getComputedStyle(e).height))')
    assert all(abs(a-b)<1 for a,b in zip(before_end,after_end)), (before_end,after_end)
    assert page.locator('[data-reading-stage]:not([hidden])').count() == 1
    assert page.locator('[data-reading-card][data-depth="2"]').evaluate('''card => {
      const stage=card.querySelector('[data-reading-stage]');
      return card.scrollHeight<=card.clientHeight+1 &&
        stage.getBoundingClientRect().bottom<=card.getBoundingClientRect().bottom+1;
    }'''), 'Measured card clips active content'


def activate(page, index):
    page.locator('[data-reading-select]').nth(index).evaluate('''b => b.dispatchEvent(
      new MouseEvent('click', {bubbles:true, detail:1}))''')


def underway(page):
    page.wait_for_function('''() => document.querySelector('.reading-panel').getAnimations({subtree:true})
      .some(a => a.currentTime > 40 && a.currentTime < 350)''')


def no_temporary_motion(page):
    settled(page)
    assert page.locator('.reading-panel').evaluate('e => getComputedStyle(e).transform') == 'none'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
    assert page.evaluate('!document.activeElement.closest("[inert],[hidden]")')


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    for width in (1440, 390, 768, 1024):
        for reduced in (False, True):
            context = browser.new_context(viewport={'width':width, 'height':900 if width == 1440 else 1024 if width == 768 else 768 if width == 1024 else 800},
                reduced_motion='reduce' if reduced else 'no-preference', is_mobile=width <= 1024, has_touch=width <= 1024)
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
            page.goto(args.base_url.rstrip('/') + '/#lectura-aprendizajes', wait_until='networkidle')
            choose(page, 1)
            boundary = page.evaluate('scrollY')
            choose(page, 0)
            page.evaluate('y => scrollTo({top:y, behavior:"instant"})', boundary - 8)
            page.wait_for_timeout(50)
            forward = cross(page, boundary + 4)
            assert forward['selected'] == 'lectura-brechas', forward
            assert abs(forward['scroll'] - forward['target']) < 1, forward
            if reduced:
                assert not forward['panelAnimations'] and not forward['contentAnimations'], forward
            else:
                assert forward['panelAnimations'] == 1, forward
                assert abs(forward['actual'] - forward['expected']) < 2, forward
                assert set(forward['contentAnimations']) == {'opacity'}, forward
            # Reverse while the panel is still moving. The first frame must use
            # its current presentation position instead of restarting at rest.
            page.wait_for_timeout(75)
            backward = cross(page, boundary - 8)
            assert backward['selected'] == 'lectura-aprendizajes', backward
            if not reduced:
                assert backward['panelAnimations'] == 1, backward
                assert abs(backward['actual'] - backward['expected']) < 2, backward
            settled(page)
            # The deck's larger internal depth range must stay below sticky
            # navigation, including after FLIP's temporary transform is gone.
            assert page.locator('.chapter-links a[aria-current]').evaluate('''e=>{
              const r=e.getBoundingClientRect();
              return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));
            }'''), 'Card covers the chapter index'
            assert abs(page.evaluate('scrollY') - (boundary - 8)) < 1, 'Animation moved document scroll'
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Overflow'
            # Direct selection at a canonical stop must also reveal the body
            # progressively, while leaving document/selection in agreement.
            choose(page, 0)
            direct = page.locator('[data-reading-select]').nth(2).evaluate('''button => {
              const panel = button.closest('.reading-panel');
              const before = panel.getBoundingClientRect().top;
              button.dispatchEvent(new MouseEvent('click', {bubbles:true, detail:1}));
              const content = document.getElementById('proximos-pasos');
              return {before, after:panel.getBoundingClientRect().top,
                opacity:getComputedStyle(content).opacity,
                properties:content.getAnimations().map(a => a.transitionProperty)};
            }''')
            assert abs(direct['before'] - direct['after']) < 2, direct
            if reduced:
                assert direct['opacity'] == '1' and not direct['properties'], direct
            else:
                assert float(direct['opacity']) < .1 and set(direct['properties']) == {'opacity'}, direct
            # Keyboard input cancels both the deck displacement and text entry.
            page.keyboard.press('Tab')
            assert page.locator('.reading-panel').evaluate('e => e.getAnimations({subtree:true}).length') == 0
            assert page.locator('#proximos-pasos').evaluate('e => getComputedStyle(e).opacity') == '1'
            if not reduced:
                choose(page, 0)
                page.evaluate('y => scrollTo({top:y, behavior:"instant"})', boundary - 8)
                page.wait_for_timeout(50)
                cross(page, boundary + 4)
                page.emulate_media(reduced_motion='reduce')
                settled(page)
                assert page.locator('.reading-panel').evaluate('e => getComputedStyle(e).transform') == 'none'
                page.emulate_media(reduced_motion='no-preference')
                cross(page, boundary - 8)
                # Reflow during a transition must clear all presentation offsets.
                page.set_viewport_size({'width':320, 'height':800})
                page.wait_for_function('!document.querySelector(".reading-enhanced")')
                settled(page)
                assert page.locator('[data-reading-stage]').evaluate_all('els => els.every(e => !e.hidden && !e.inert)')
                assert page.locator('.reading-panel').evaluate('e => getComputedStyle(e).transform') == 'none'
            # Fresh layout after the narrow-screen cancellation above.
            if not reduced:
                page.set_viewport_size({'width':width, 'height':900 if width == 1440 else 1024 if width == 768 else 768 if width == 1024 else 800})
                page.wait_for_function('document.querySelector(".reading-enhanced")')
                for source, destination in ((0,1),(1,2),(2,1),(1,0),(0,2),(2,0)):
                    choreography(page, source, destination)
                # A tall departing card must leave the new footer clickable.
                choose(page,2)
                activate(page,0)
                footer = page.locator('[data-reading-next]').evaluate('''button => {
                  const panel=button.closest('.reading-panel');
                  panel.getAnimations({subtree:true}).forEach(a=>a.pause());
                  let r=button.getBoundingClientRect();
                  scrollBy({top:Math.max(0,r.bottom-innerHeight+24),behavior:'instant'});
                  r=button.getBoundingClientRect();
                  const x=r.x+r.width/2,y=r.y+r.height/2;
                  return {x,y,accessible:button.contains(document.elementFromPoint(x,y))};
                }''')
                assert footer['accessible'], footer
                page.mouse.click(footer['x'],footer['y'])
                page.locator('.reading-panel').evaluate('p=>p.getAnimations({subtree:true}).forEach(a=>a.play())')
                settled(page)
                assert page.locator('[data-reading-select][aria-pressed="true"]').get_attribute('aria-controls') == 'lectura-brechas'
                # Reverse visible content before its exit has finished. Neither
                # card transforms, depth nor text may restart from a rest pose.
                choose(page, 0)
                activate(page, 1)
                underway(page)
                reversal = page.locator('[data-reading-select]').nth(0).evaluate('''b => {
                  const panel=b.closest('.reading-panel');
                  const snap=()=>[...panel.querySelectorAll('[data-reading-card]')].map(c=>({
                    matrix:getComputedStyle(c).transform,z:getComputedStyle(c).zIndex,height:getComputedStyle(c).height,
                    opacity:Number(getComputedStyle(c.querySelector('section')).opacity)}));
                  const before=snap();
                  b.dispatchEvent(new MouseEvent('click',{bubbles:true,detail:1}));
                  return {before,after:snap()};
                }''')
                for before, after in zip(reversal['before'],reversal['after']):
                    assert before['matrix'] == after['matrix'] and before['z'] == after['z'] and before['height'] == after['height'], reversal
                    assert abs(before['opacity'] - after['opacity']) < .02, reversal
                settled(page)
                # Repeated scroll changes resolve from real document position.
                stops=[]
                for i in range(3):
                    choose(page,i)
                    stops.append(page.evaluate('scrollY'))
                for i in (0,2,1,0,2):
                    page.evaluate('''y=>{document.dispatchEvent(new WheelEvent('wheel'));scrollTo({top:y,behavior:'instant'})}''',stops[i]+4)
                    page.wait_for_function('(i)=>document.querySelectorAll("[data-reading-select]")[i].getAttribute("aria-pressed")==="true"',arg=i)
                settled(page)
                assert page.locator('[data-reading-select][aria-pressed="true"]').get_attribute('aria-controls') == 'proximos-pasos'
                assert abs(page.evaluate('scrollY')-stops[2]-4)<1
                # Moving a focused link out of the active chapter has a safe,
                # persistent button destination before hidden/inert is applied.
                choose(page,0)
                page.locator('#lectura-aprendizajes a').first.evaluate('e=>e.focus({preventScroll:true})')
                page.evaluate('''y=>{document.dispatchEvent(new WheelEvent('wheel'));scrollTo({top:y,behavior:'instant'})}''',stops[1]+4)
                page.wait_for_function('document.activeElement.getAttribute("aria-controls")==="lectura-brechas"')
                no_temporary_motion(page)
                # Orientation, text enlargement, reduced preference in both
                # directions, and print cancel presentation offsets mid-flight.
                activate(page,0)
                underway(page)
                page.set_viewport_size({'width':768 if width!=768 else 1024,'height':1024 if width!=768 else 768})
                no_temporary_motion(page)
                activate(page,1)
                underway(page)
                page.locator('.text-size').evaluate('b=>b.click()')
                page.wait_for_function('!document.querySelector(".reading-enhanced")')
                no_temporary_motion(page)
                assert page.locator('[data-reading-stage]').evaluate_all('els=>els.every(e=>!e.hidden&&!e.inert&&!e.hasAttribute("aria-hidden"))')
                page.locator('.text-size').evaluate('b=>b.click()')
                page.wait_for_function('document.querySelector(".reading-enhanced")')
                activate(page,2)
                underway(page)
                page.emulate_media(reduced_motion='reduce')
                no_temporary_motion(page)
                page.emulate_media(reduced_motion='no-preference')
                no_temporary_motion(page)
                activate(page,0)
                underway(page)
                page.evaluate('dispatchEvent(new Event("beforeprint"))')
                no_temporary_motion(page)
                page.emulate_media(media='print')
                assert page.locator('[data-reading-stage]').evaluate_all('els=>els.every(e=>!e.hidden&&!e.inert&&!e.hasAttribute("aria-hidden"))')
                assert page.locator('[data-reading-stage]').evaluate_all('els=>els.every(e=>e.getBoundingClientRect().height>0&&getComputedStyle(e).opacity==="1")')
                page.emulate_media(media='screen')
                page.evaluate('dispatchEvent(new Event("afterprint"))')
                no_temporary_motion(page)
            assert not errors, errors
            result = {'width':width, 'reduced_motion':reduced, 'forward':forward,
                'interrupted_reverse':backward, 'direct':direct, 'status':'passed'}
            results.append(result)
            print(json.dumps({'width':width, 'reduced_motion':reduced, 'status':'passed'}), flush=True)
            context.close()
    # Starting-style is optional: content must remain visible if unsupported.
    context = browser.new_context()
    page = context.new_page()
    css = Path('site/assets/styles.css').read_text().replace('@starting-style', '@unsupported-starting-style')
    page.route('**/assets/styles.css', lambda route: route.fulfill(body=css, content_type='text/css'))
    page.goto(args.base_url.rstrip('/') + '/#lectura-aprendizajes', wait_until='networkidle')
    choose(page, 1)
    assert page.locator('#lectura-brechas').evaluate('e => getComputedStyle(e).opacity') == '1'
    results.append({'case':'unsupported starting-style', 'status':'passed'})
    browser.close()

(args.output / 'report.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
print(f'{len(results)} casos de continuidad aprobados.')
