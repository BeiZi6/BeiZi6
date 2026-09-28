"""Render assets/fetch.png, the terminal card on the profile.  Run: python assets/fetch.py"""
import html
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent

LOGO = """\
██╗  ██╗██╗   ██╗
╚██╗██╔╝╚██╗ ██╔╝
 ╚███╔╝  ╚████╔╝
 ██╔██╗   ╚██╔╝
██╔╝ ██╗   ██║
╚═╝  ╚═╝   ╚═╝"""

INFO = [
    ('Name', 'Xu Yuanshan (徐元山)'),
    ('Edu', 'HIT Weihai (B.Eng.) → HIT (M.Eng., 2026–)'),
    ('Major', 'Electronic Information · Info & Comm. Engineering'),
    ('Focus', 'AI engineering · forward-deployed engineering'),
    ('Ship', 'LLM gateways · agent plugins · desktop apps · CLIs'),
    ('Delivery', 'API → app → release → docs, end to end'),
    ('Research', 'synthetic multimodal data (visible / IR / SAR), UE5'),
    ('Perf', 'RaySAR ported to Rust, 7.8× faster end to end'),
    ('Stack', 'Python · Rust · TypeScript · Claude Code · MCP'),
]
PALETTE = ['#484f58', '#ff7b72', '#3fb950', '#d29922', '#58a6ff', '#bc8cff', '#39c5cf', '#b1bac4']

logo = re.sub(r'(█+)', r'<b>\1</b>', html.escape(LOGO))
rows = '\n'.join(f'<span class="k">{k:<10}</span>{html.escape(v)}' for k, v in INFO)
palette = ''.join(f'<i style="background:{c}"></i>' for c in PALETTE)
prompt = '<span class="u">xu@hit</span>:<span class="p">~</span>$ '

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
  html, body {{ margin:0; background:transparent; }}
  .term {{ display:inline-block; background:#0d1117; border:1px solid #30363d; border-radius:12px; overflow:hidden;
          font:15px/1.65 'Cascadia Mono', 'Microsoft YaHei', monospace; color:#c9d1d9; }}
  .bar {{ position:relative; height:40px; background:#161b22; border-bottom:1px solid #30363d; }}
  .dots {{ position:absolute; left:16px; top:14px; display:flex; gap:8px; }}
  .dots i {{ width:12px; height:12px; border-radius:50%; }}
  .title {{ text-align:center; line-height:40px; font-size:13px; color:#8b949e; }}
  .body {{ padding:22px 36px 26px; }}
  pre {{ margin:0; font:inherit; white-space:pre; }}
  .fetch {{ display:flex; align-items:center; gap:44px; margin:18px 0 20px 6px; }}
  .logo {{ font-size:22px; line-height:1; color:#30363d; }}
  .logo b {{ font-weight:normal; color:#39c5cf; }}
  .k {{ color:#39c5cf; font-weight:bold; }}
  .u {{ color:#3fb950; }} .p {{ color:#58a6ff; }} .m {{ color:#8b949e; }}
  .pal {{ display:flex; margin-top:12px; }}
  .pal i {{ width:28px; height:14px; }}
  .cur {{ display:inline-block; width:.6em; height:1.15em; background:#8b949e; vertical-align:-.22em; }}
</style></head><body><div class="term">
  <div class="bar"><div class="dots"><i style="background:#ff5f56"></i><i style="background:#ffbd2e"></i><i style="background:#27c93f"></i></div>
    <div class="title">xu@hit: ~</div></div>
  <div class="body">
    <pre>{prompt}neofetch</pre>
    <div class="fetch">
      <pre class="logo">{logo}</pre>
      <div><pre><span class="k">xu</span>@<span class="k">hit</span>
<span class="m">------</span>
{rows}</pre><div class="pal">{palette}</div></div>
    </div>
    <pre>{prompt}<span class="cur"></span></pre>
  </div>
</div></body></html>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1400, 'height': 900}, device_scale_factor=2)
    page.set_content(HTML)
    page.evaluate('document.fonts.ready.then(() => true)')
    page.locator('.term').screenshot(path=HERE / 'fetch.png', omit_background=True)
    browser.close()
