"""Responsive QA: load each page at 1920/1440/1024/768/390/360, scroll to load
lazy images, report horizontal overflow and small tap targets, save screenshots.
Usage: python3 tools/check_pages.py page1.html [page2.html ...] [--shots DIR] [--full]
"""
import asyncio, sys, os, json
from playwright.async_api import async_playwright
WIDTHS = [1920, 1440, 1024, 768, 430, 390, 375, 360]
JS = """() => {
  const W = document.documentElement.clientWidth;
  const over = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || getComputedStyle(el).position === 'fixed') continue;
    if (r.right > W + 1 && !el.closest('[class*=hscroll],.hscroll,.scroll,.ticker,.foot-word,.word,.lb,.labnav,iframe,.strip,.ftr-word,.h-word,.compare-wrap,.xp-bar,[style*="overflow"]')) {
      let p = el.parentElement, clipped = false;
      while (p) { const s = getComputedStyle(p); if (['hidden','clip','auto','scroll'].includes(s.overflowX)) { clipped = true; break; } p = p.parentElement; }
      if (!clipped) over.push((el.className || el.tagName).toString().slice(0, 40) + ' ' + Math.round(r.right - W) + 'px');
    }
  }
  const small = [...document.querySelectorAll('a,button,input,select')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.height < 32 && getComputedStyle(e).display !== 'inline' && !e.closest('nav p, footer, .foot-cols, figcaption, .xlist, .labnav'); }).length;
  return { scrollW: document.documentElement.scrollWidth, W, over: [...new Set(over)].slice(0, 6), small };
}"""
async def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    shots = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
    if shots: args = [a for a in args if a != shots]; os.makedirs(shots, exist_ok=True)
    full = '--full' in sys.argv
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for page_path in args:
            for w in WIDTHS:
                pg = await b.new_page(viewport={'width': w, 'height': 900})
                await pg.goto('http://localhost:8765/' + page_path)
                h = await pg.evaluate('document.body.scrollHeight')
                for y in range(0, h, 700):
                    await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(60)
                await pg.evaluate('document.querySelectorAll(".reveal,.reveal-mask,.rv,.rv-mask,.sp,[data-reveal],[data-stagger],[data-layered]").forEach(e=>e.classList.add("is-in","in"))')
                await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(700)
                r = await pg.evaluate(JS)
                res[f'{page_path}@{w}'] = r
                if shots and w in (1440, 390):
                    name = page_path.replace('/', '_').replace('.html', '') + f'_{w}.png'
                    await pg.screenshot(path=os.path.join(shots, name), full_page=full)
                await pg.close()
        await b.close()
    bad = {k: v for k, v in res.items() if v['scrollW'] > v['W'] or v['over']}
    for k, v in res.items():
        flag = 'OVERFLOW' if k in bad else 'ok'
        print(f"{flag:8} {k}  scrollW={v['scrollW']} W={v['W']} small-targets={v['small']} {v['over'] if v['over'] else ''}")
asyncio.run(main())
