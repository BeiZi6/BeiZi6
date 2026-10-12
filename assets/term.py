"""Render the profile from otty-rs's live state: assets/term.svg (animated terminal) and README.md.
Run: python assets/term.py <otty-rs checkout>, e.g. python assets/term.py E:/study_serve/otty-re"""
import re
import subprocess
import sys
import unicodedata
from html import escape
from pathlib import Path
from xml.etree import ElementTree

HERE = Path(__file__).parent
REPO = Path(sys.argv[1])

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
    ('Now', 'otty-rs: the Otty terminal rebuilt from scratch in Rust'),
]
SHIP = [
    ('otty-rs', 'Rust', 'Otty terminal rebuilt from scratch: Rust engine, Electron UI'),
    ('CSwitch', 'TypeScript', 'local Anthropic-compatible gateway for third-party LLM APIs'),
    ('claude-3p-setup', 'PowerShell', 'one-command Claude Desktop setup for third-party gateways'),
    ('Ai-Report-Formatter', 'Python', 'LLM Markdown to submission-ready Word: equations, citations'),
    ('easy-cc', 'Markdown', 'field guide to Claude Code for Chinese developers'),
    ('dsh-opencodego-usage', 'JavaScript', 'LLM quota monitor plugin for the DeepSeek Harness web GUI'),
    ('dsh-theme-plugin', 'JavaScript', 'theme studio plugin for the DeepSeek Harness web GUI'),
]
PALETTE = ['#484f58', '#ff7b72', '#3fb950', '#d29922', '#58a6ff', '#bc8cff', '#39c5cf', '#b1bac4']
LOGO = ('##....##  ##....##',
        '##....##  ##....##',
        '.##..##.  .##..##.',
        '.##..##.  .##..##.',
        '..####..  ..####..',
        '.##..##.  ...##...',
        '.##..##.  ...##...',
        '##....##  ...##...',
        '##....##  ...##...')
DOMAINS = {'K': 'resources', 'S': 'app shell', 'T': 'engine', 'C': 'config',     # GAP-K01, GAP-S01, ... in the ledger
           'A': 'agent', 'W': 'workflow', 'I': 'cli / ipc', 'P': 'packaging'}


def git(*args):
    return subprocess.run(['git', '-C', REPO, *args], capture_output=True, encoding='utf-8', check=True).stdout.strip()


# --- otty-rs: the gap ledger, the last commits, the size of the tree ---
head, date = git('log', '-1', '--format=%h %cs').split()
branch = git('branch', '--show-current') or 'HEAD'
commits = git('rev-list', '--count', 'HEAD')
log = [line.split('\t', 1) for line in git('log', '-8', '--format=%h%x09%s').splitlines()]
rust = sum(p.read_bytes().count(b'\n') for p in (REPO / 'otty/packages').rglob('*.rs') if 'target' not in p.parts)
cargo = (REPO / 'otty/Cargo.toml').read_text(encoding='utf-8')
crates = cargo.split('members = [')[1].split(']')[0].count('"packages/')
version = re.search(r'^version = "(.+?)"', cargo, re.M)[1]
gaps = {d: {'done': 0, 'partial': 0, 'open': 0} for d in DOMAINS}
ledger = (REPO / 'otty/docs/GAPS.md').read_text(encoding='utf-8')
for d, status in re.findall(r'^\| GAP-(\w)\d+ \|[^|]*\|[^|]*\| (\w+) \|', ledger, re.M):
    if status != 'skip':    # skip: the original has no such feature either
        gaps[d]['open' if status == 'blocked' else status] += 1
done, partial, todo = (sum(g[s] for g in gaps.values()) for s in ('done', 'partial', 'open'))
tracked = done + partial + todo

# --- the SVG: text sits on a cell grid, and every animation ends in the static picture ---
W, CW, LH, PAD, SPLIT = 920, 8.4, 22, 24, 360     # width, cell (0.6em of 14px), line height, padding, pane split
CSS = '''
text{font:14px ui-monospace,'Cascadia Mono','SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace;fill:#c9d1d9}
.k{fill:#39c5cf;font-weight:bold}.c{fill:#39c5cf}.d{fill:#8b949e}.g{fill:#3fb950}.b{fill:#58a6ff}.y{fill:#d29922}
.inv{fill:#0d1117;font-weight:bold}
.ty{animation:in .01s backwards}
.ln{animation:rise .35s ease-out backwards}
.bar{transform-box:fill-box;transform-origin:left;animation:grow .7s cubic-bezier(.2,.8,.2,1) backwards}
.px{fill:#39c5cf;transform-box:fill-box;transform-origin:center;animation:pop .4s cubic-bezier(.3,1.5,.5,1) backwards,glint 8s linear infinite}
.tc{fill:#8b949e;opacity:0}
.cur{fill:#8b949e;animation:blink 1.1s steps(1) infinite}
.pulse{animation:pulse 2s ease-in-out infinite}
@keyframes in{from{opacity:0}}
@keyframes rise{from{opacity:0;transform:translateY(6px)}}
@keyframes grow{from{transform:scaleX(0)}}
@keyframes pop{from{opacity:0;transform:scale(.2)}}
@keyframes glint{0%,8%,to{fill:#39c5cf}4%{fill:#d5fbff}}
@keyframes on{from,to{opacity:1}}
@keyframes blink{50%{opacity:0}}
@keyframes pulse{50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
'''
svg, moves = [], []
add = svg.append


def cells(s):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)


def text(x, y, s, cls='', delay=None):
    """One run of text, its row's top at y. textLength pins the width, so any monospace font keeps the grid."""
    n = cells(s)
    add(f'<text x="{x:.1f}" y="{y + 15}"'
        + (f' textLength="{n * CW:.1f}"' if n > 1 else '')
        + (f' class="{cls}"' if cls else '')
        + (f' style="animation-delay:{delay:.2f}s"' if delay is not None else '')
        + f'>{escape(s)}</text>')
    return x + n * CW


def prompt(x, y, path):
    x = text(text(text(x, y, 'xu@hit', 'g'), y, ':'), y, path, 'b')
    return text(x, y, '$') + CW


def typed(x, y, cmd, start, dt):
    """Type cmd behind a block cursor, one cell per dt. Returns the time it is entered."""
    enter = start + len(cmd) * dt + .25
    moves.append(f'@keyframes mv{len(moves)}{{to{{transform:translateX({len(cmd) * CW:.1f}px)}}}}')
    for i, ch in enumerate(cmd):
        if ch != ' ':
            text(x + i * CW, y, ch, 'ty', start + (i + 1) * dt)
    add(f'<rect class="tc" x="{x:.1f}" y="{y + 3}" width="{CW}" height="17" style="animation:on {enter:.2f}s linear,'
        f'mv{len(moves) - 1} {len(cmd) * dt:.2f}s steps({len(cmd)}) {start:.2f}s forwards"/>')
    return enter


def reveal(delay):
    add(f'<g class="ln" style="animation-delay:{delay:.2f}s">')


# title bar: traffic lights, the active tab, a tab with work in progress
for i, colour in enumerate(('#ff5f56', '#ffbd2e', '#27c93f')):
    add(f'<circle cx="{22 + 20 * i}" cy="20" r="6" fill="{colour}"/>')
add('<rect x="90" y="8" width="62" height="40" rx="8" fill="#0d1117"/><path d="M99 9H143" stroke="#39c5cf" stroke-width="2"/>')
text(104, 13, '~')
text(129, 13, '×', 'd')
text(174, 13, 'otty-rs', 'd')
add('<circle class="pulse" cx="247" cy="23.5" r="3.5" fill="#3fb950"/>')
text(W - PAD - 6 * CW, 13, 'xu@hit', 'd')

# top pane: neofetch
y = 54
t = typed(prompt(PAD, y, '~'), y, 'neofetch', .25, .06)
top, IX = y + LH + 12, 308
block, PX = (len(INFO) + 2) * LH + 22, 13
lx, ly = 34, top + (block - len(LOGO) * PX) / 2
dots = [(lx + c * PX, ly + r * PX, c + r) for r, row in enumerate(LOGO) for c, ch in enumerate(row) if ch == '#']
shadow = ''.join(f'M{x + 4} {y + 4:.1f}h11v11h-11z' for x, y, _ in dots)
add(f'<path class="ln" d="{shadow}" fill="#163238" style="animation-delay:{t:.2f}s"/>')
for x, y, k in dots:
    add(f'<rect class="px" x="{x}" y="{y:.1f}" width="11" height="11" rx="2" '
        f'style="animation-delay:{t + .03 * k:.2f}s,{t + 2 + .08 * k:.2f}s"/>')
reveal(t)
text(text(text(IX, top, 'xu', 'k'), top, '@'), top, 'hit', 'k')
add('</g>')
reveal(t + .07)
text(IX, top + LH, '------', 'd')
add('</g>')
for i, (key, value) in enumerate(INFO, 2):
    reveal(t + .07 * i)
    text(IX, top + i * LH, key, 'g' if key == 'Now' else 'k')
    text(IX + 10 * CW, top + i * LH, value)
    add('</g>')
for i, colour in enumerate(PALETTE):
    add(f'<rect class="ln" x="{IX + 28 * i}" y="{top + block - 14}" width="28" height="14" fill="{colour}" '
        f'style="animation-delay:{t + 1 + .04 * i:.2f}s"/>')

# bottom left: the gap ledger as a file pane
mid = top + block + 16
by = mid + 13
bot = by + 10 * LH + 11
add(f'<path d="M0 {mid}.5H{W}M{SPLIT}.5 {mid}V{bot}" stroke="#30363d"/>')
g0 = t + .9
reveal(g0)
text(text(PAD, by, 'docs/GAPS.md', 'b') + CW, by, f'parity with Otty {version}', 'd')
add('</g>')
BX, BW = PAD + 10 * CW + 4, 164
for i, (d, name) in enumerate(DOMAINS.items(), 1):
    g, y, at = gaps[d], by + i * LH, g0 + .09 * i
    n = sum(g.values())
    reveal(at)
    text(PAD, y, name)
    add(f'<rect x="{BX}" y="{y + 6}" width="{BW}" height="10" rx="2" fill="#30363d"/>')
    x = BX
    for status, colour, wait in (('done', '#3fb950', 0), ('partial', '#d29922', .45)):
        w = BW * g[status] / n
        if w:
            add(f'<rect class="bar" x="{x:.1f}" y="{y + 6}" width="{w:.1f}" height="10" rx="2" fill="{colour}" '
                f'style="animation-delay:{at + wait:.2f}s"/>')
        x += w
    count = f'{g["done"]}/{n}'
    text(BX + BW + 10 + (5 - len(count)) * CW, y, count, 'd')
    add('</g>')
reveal(g0 + 1)
x, y = PAD, by + 9 * LH
for n, label, colour in ((done, 'done', '#3fb950'), (partial, 'partial', '#d29922'), (todo, 'open', '#30363d')):
    add(f'<rect x="{x:.1f}" y="{y + 6}" width="10" height="10" rx="2" fill="{colour}"/>')
    x = text(x + 16, y, f'{n} {label}', 'd') + 18
add('</g>')

# bottom right: git log
rx = SPLIT + 21
t = typed(prompt(rx, by, '~/otty-rs'), by, f'git log --oneline -{len(log)}', t + 1.2, .04)
room = int((W - PAD - rx) / CW) - 8
for i, (sha, subject) in enumerate(log, 1):
    ids, rest = re.match(r'((?:GAP-\w+ )*)(.*)', ' '.join(subject.split())).groups()
    if len(rest) > room - len(ids):
        rest = rest[:room - len(ids) - 1].rstrip(' ,;:') + '…'
    reveal(t + .08 * i)
    x = text(rx, by + i * LH, sha, 'y') + CW
    if ids:
        x = text(x, by + i * LH, ids.strip(), 'c') + CW
    text(x, by + i * LH, rest)
    add('</g>')
reveal(t + .08 * len(log) + .4)
x = prompt(rx, by + 9 * LH, '~/otty-rs')
add(f'<rect class="cur" x="{x:.1f}" y="{by + 9 * LH + 3}" width="{CW}" height="17"/></g>')

# status line: where the numbers above were read
H = bot + 28
add(f'<rect y="{bot}" width="{W}" height="28" fill="#161b22"/><path d="M0 {bot}.5H{W}" stroke="#30363d"/>')
x = (len(branch) + 2) * CW + 18
add(f'<rect y="{bot + 1}" width="{x:.1f}" height="27" fill="#39c5cf"/>'
    f'<g fill="none" stroke="#0d1117" stroke-width="1.4"><circle cx="13" cy="{bot + 9}" r="1.8"/>'
    f'<circle cx="13" cy="{bot + 19}" r="1.8"/><circle cx="19" cy="{bot + 11}" r="1.8"/>'
    f'<path d="M13 {bot + 10.8}V{bot + 17.2}M19 {bot + 12.8}c0 3-6 2-6 4.4"/></g>')
text(CW + 18, bot + 3, branch, 'inv')
x = text(x + CW, bot + 3, head, 'y')
for part in (f'{commits} commits', f'{crates} crates', f'{rust / 1000:.1f}k lines of Rust'):
    x = text(text(x + CW, bot + 3, '·', 'd') + CW, bot + 3, part, 'd')
text(W - PAD - len(date) * CW, bot + 3, date, 'd')

doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<title>xu@hit: neofetch, the otty-rs gap ledger, git log</title><style>{CSS}{"".join(moves)}</style>'
       f'<clipPath id="w"><rect width="{W}" height="{H}" rx="12"/></clipPath><g clip-path="url(#w)">'
       f'<rect width="{W}" height="{H}" fill="#0d1117"/><rect width="{W}" height="40" fill="#161b22"/>'
       f'<path d="M0 40.5H{W}" stroke="#30363d"/>{"".join(svg)}</g>'
       f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="11.5" fill="none" stroke="#30363d"/></svg>')
ElementTree.fromstring(doc)     # the check: malformed markup stops here, before anything is written
(HERE / 'term.svg').write_text(doc, encoding='utf-8', newline='\n')

# --- README.md: the same facts as text, with links (GitHub keeps <a> inside <pre>) ---
alt = ('Animated terminal. neofetch: ' + ' '.join(f'{k}: {v}.' for k, v in INFO)
       + f' docs/GAPS.md, parity with Otty {version}: {done} of {tracked} tracked capabilities done, {partial} partial,'
       f' {todo} open. git log: ' + '; '.join(subject for _, subject in log)
       + f'. {branch} at {head}, {date}: {commits} commits, {crates} crates, {rust / 1000:.1f}k lines of Rust.')
ship = '\n'.join(f'<a href="https://github.com/BeiZi6/{name}">{name}</a>{" " * (22 - len(name))}{lang:<12}{escape(what)}'
                 for name, lang, what in SHIP)
(HERE.parent / 'README.md').write_text(f'''<!-- Generated by assets/term.py from an otty-rs checkout. Edit the script, not this file. -->
<img alt="{escape(alt)}" src="assets/term.svg">

`$ whoami` Xu Yuanshan (徐元山), M.Eng. student at Harbin Institute of Technology. AI engineering and forward-deployed engineering: I ship LLM gateways, agent plugins and desktop apps end to end. Research: synthetic multimodal data (visible / IR / SAR) in UE5. Stack: Python, Rust, TypeScript.

<pre>
$ ls ship/
{ship}
</pre>

`$ cat now` [otty-rs](https://github.com/BeiZi6/otty-rs), the Otty terminal rebuilt from scratch: a Rust engine (VT, PTY, fonts, rasteriser) behind an Electron frontend. {done} of {tracked} tracked capabilities done, {partial} partial, {todo} open, as of `{head}` ({date}). Design notes: [引擎报事件，应用做决定](https://blog.xyucode.top/p/2026-10-06-otty-rs-怎么分层)
''', encoding='utf-8', newline='\n')
print(f'{head} {date}: {done}/{tracked} done, {partial} partial, {todo} open | term.svg {len(doc) / 1024:.1f} KB, {W}x{H}')
