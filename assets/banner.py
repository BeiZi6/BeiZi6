"""Render assets/banner-light.png and assets/banner-dark.png.  Run: python assets/banner.py"""
import math
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
W, H = 1280, 360
CX, CY = 1090, 172  # centre of the rings and of the sinc main lobe

rings = ''.join(f'<circle cx="{CX}" cy="{CY}" r="{r}"/>' for r in (118, 172, 226, 280, 334))
sinc = ' '.join(
    f'{x},{336 - 30 * (math.sin(math.pi * t) / (math.pi * t) if t else 1):.2f}'
    for x in range(0, W + 1, 4) for t in [(x - CX) / 36]
)

HTML = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,500&display=block">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@600&text=%E5%BE%90%E5%85%83%E5%B1%B1&display=block">
<style>
  :root {{ --bg1:#F8F2E7; --bg2:#EFE5D3; --ink:#1E1915; --muted:#6F665C; --accent:#B3301C;
          --edge:rgba(30,25,21,.10); --ring:rgba(179,48,28,.15); }}
  .dark {{ --bg1:#161A21; --bg2:#0D0F13; --ink:#EFE7D8; --muted:#A1978A; --accent:#C9A45C;
          --edge:rgba(201,164,92,.24); --ring:rgba(201,164,92,.17); }}
  html, body {{ margin:0; background:transparent; }}
  .card {{ position:relative; width:{W}px; height:{H}px; box-sizing:border-box; overflow:hidden;
          border-radius:20px; border:1px solid var(--edge); background:linear-gradient(160deg, var(--bg1), var(--bg2)); }}
  .deco {{ position:absolute; inset:0; fill:none; stroke:var(--ring); stroke-width:1.2;
          -webkit-mask-image:radial-gradient(circle at {CX}px {CY}px, #000 35%, transparent 78%); }}
  .text {{ position:absolute; left:84px; top:58px; }}
  .kicker {{ font:600 15px/1 'Cormorant Garamond'; letter-spacing:.34em; text-transform:uppercase; color:var(--accent); }}
  .name {{ font:600 104px/1 'Cormorant Garamond'; letter-spacing:-.01em; color:var(--ink); margin-top:24px; }}
  .cn {{ font:600 28px/1 'Noto Serif SC'; letter-spacing:.6em; color:var(--muted); margin-top:14px; }}
  .bar {{ width:56px; height:2px; background:var(--accent); margin:26px 0 20px; }}
  .tag {{ font:italic 500 26px/1 'Cormorant Garamond'; color:var(--muted); }}
  .tag b {{ font-weight:500; font-style:normal; color:var(--accent); padding:0 .4em; }}
</style></head><body><div class="card">
  <svg class="deco" width="{W}" height="{H}">{rings}<polyline points="{sinc}"/></svg>
  <div class="text">
    <div class="kicker">Harbin Institute of Technology</div>
    <div class="name">Xu Yuanshan</div>
    <div class="cn">徐元山</div>
    <div class="bar"></div>
    <div class="tag">Multimodal sensor simulation<b>·</b>Rust &amp; Python<b>·</b>Tools for AI coding agents</div>
  </div>
</div></body></html>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
    page.set_content(HTML, wait_until='networkidle')
    page.evaluate('document.fonts.ready.then(() => true)')
    print('loaded fonts:', [f"{f['family']} {f['weight']}" for f in page.evaluate(
        '[...document.fonts].map(f => ({family: f.family, weight: f.weight, status: f.status}))') if f['status'] == 'loaded'])
    for theme in ('light', 'dark'):
        page.evaluate(f"document.body.className = '{theme}'")
        page.locator('.card').screenshot(path=HERE / f'banner-{theme}.png', omit_background=True)
    browser.close()
