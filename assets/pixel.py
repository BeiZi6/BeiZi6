"""Render the profile: assets/pixel.svg (a pixel-art card whose animations all loop) and README.md.
Run: python assets/pixel.py <otty-rs checkout>, e.g. python assets/pixel.py E:/study_serve/otty-re"""
import re
import subprocess
import sys
from html import escape
from pathlib import Path
from xml.etree import ElementTree

HERE = Path(__file__).parent
REPO = Path(sys.argv[1])

NAME, SCHOOL, AGE = 'XU YUANSHAN', '哈工大', 23
TAGLINES = ['AI ENGINEERING', 'FORWARD-DEPLOYED ENGINEERING', 'NOW BUILDING OTTY-RS']
STACK = ['RUST', 'TS', 'PYTHON', 'C', 'GO']
SKILLS = ['LLM GATEWAYS', 'AGENT TOOLING: MCP + SKILLS', 'DESKTOP APPS', 'CLI TOOLS']
SHIP = [
    ('otty-rs', 'Rust', 'Otty terminal rebuilt from scratch: Rust engine, Electron UI'),
    ('CSwitch', 'TypeScript', 'local Anthropic-compatible gateway for third-party LLM APIs'),
    ('claude-3p-setup', 'PowerShell', 'one-command Claude Desktop setup for third-party gateways'),
    ('Ai-Report-Formatter', 'Python', 'LLM Markdown to submission-ready Word: equations, citations'),
    ('easy-cc', 'Markdown', 'field guide to Claude Code for Chinese developers'),
    ('dsh-opencodego-usage', 'JavaScript', 'LLM quota monitor plugin for the DeepSeek Harness web GUI'),
    ('dsh-theme-plugin', 'JavaScript', 'theme studio plugin for the DeepSeek Harness web GUI'),
]

# --- otty-rs: how far the gap ledger has got ---
head, date = subprocess.run(['git', '-C', REPO, 'log', '-1', '--format=%h %cs'],
                            capture_output=True, encoding='utf-8', check=True).stdout.split()
status = re.findall(r'^\| GAP-\w+ \|[^|]*\|[^|]*\| (\w+) \|', (REPO / 'otty/docs/GAPS.md').read_text(encoding='utf-8'), re.M)
done, partial = status.count('done'), status.count('partial')
tracked = len(status) - status.count('skip')    # skip: the original has no such feature either
todo = tracked - done - partial

# --- pixels: a 5x7 face, three 12x12 hanzi, a 16x16 sprite, three frames of a spinning star ---
PAPER, CARD, TILE, RULE = '#F0EEE6', '#FAF9F5', '#E8E6DC', '#D1CFC5'
INK, BODY, MUTE = '#141413', '#5E5D59', '#87867F'
CLAY, DEEP, KRAFT, SKIN = '#D97757', '#BD5D3A', '#D4A27F', '#F2CBA8'
GLYPHS = {
    'A': '.###./#...#/#...#/#####/#...#/#...#/#...#', 'B': '####./#...#/#...#/####./#...#/#...#/####.',
    'C': '.###./#...#/#..../#..../#..../#...#/.###.', 'D': '####./#...#/#...#/#...#/#...#/#...#/####.',
    'E': '#####/#..../#..../####./#..../#..../#####', 'F': '#####/#..../#..../####./#..../#..../#....',
    'G': '.###./#...#/#..../#.###/#...#/#...#/.###.', 'H': '#...#/#...#/#...#/#####/#...#/#...#/#...#',
    'I': '.###./..#../..#../..#../..#../..#../.###.', 'J': '..###/...#./...#./...#./...#./#..#./.##..',
    'K': '#...#/#..#./#.#../##.../#.#../#..#./#...#', 'L': '#..../#..../#..../#..../#..../#..../#####',
    'M': '#...#/##.##/#.#.#/#.#.#/#...#/#...#/#...#', 'N': '#...#/#...#/##..#/#.#.#/#..##/#...#/#...#',
    'O': '.###./#...#/#...#/#...#/#...#/#...#/.###.', 'P': '####./#...#/#...#/####./#..../#..../#....',
    'Q': '.###./#...#/#...#/#...#/#.#.#/#..#./.##.#', 'R': '####./#...#/#...#/####./#.#../#..#./#...#',
    'S': '.####/#..../#..../.###./....#/....#/####.', 'T': '#####/..#../..#../..#../..#../..#../..#..',
    'U': '#...#/#...#/#...#/#...#/#...#/#...#/.###.', 'V': '#...#/#...#/#...#/#...#/#...#/.#.#./..#..',
    'W': '#...#/#...#/#...#/#.#.#/#.#.#/##.##/#...#', 'X': '#...#/#...#/.#.#./..#../.#.#./#...#/#...#',
    'Y': '#...#/#...#/.#.#./..#../..#../..#../..#..', 'Z': '#####/....#/...#./..#../.#.../#..../#####',
    '0': '.###./#...#/#..##/#.#.#/##..#/#...#/.###.', '1': '..#../.##../..#../..#../..#../..#../.###.',
    '2': '.###./#...#/....#/...#./..#../.#.../#####', '3': '####./....#/....#/.###./....#/....#/####.',
    '4': '...#./..##./.#.#./#..#./#####/...#./...#.', '5': '#####/#..../####./....#/....#/#...#/.###.',
    '6': '.###./#..../#..../####./#...#/#...#/.###.', '7': '#####/....#/...#./..#../.#.../.#.../.#...',
    '8': '.###./#...#/#...#/.###./#...#/#...#/.###.', '9': '.###./#...#/#...#/.####/....#/....#/.###.',
    '.': '...../...../...../...../...../.##../.##..', ',': '...../...../...../...../.##../..#../.#...',
    ':': '...../.##../.##../...../.##../.##../.....', '/': '....#/....#/...#./..#../.#.../#..../#....',
    '-': '...../...../...../#####/...../...../.....', '+': '...../..#../..#../#####/..#../..#../.....',
    '>': '.#.../..#../...#./....#/...#./..#../.#...',
}
for ch, rows in (('哈', '010010f2894498297c90097cf4494407c044'), ('工', '0007fc040040040040040040040040040ffe'),
                 ('大', '040040040040ffe0400a00a0110110208c06')):       # 12 rows, 3 hex digits each
    GLYPHS[ch] = '/'.join(f'{int(rows[i:i + 3], 16):012b}'.replace('0', '.').replace('1', '#') for i in range(0, 36, 3))
SPRITE = ('....KKKKKKKK....', '...KKKKKKKKKK...', '..KKKKKKKKKKKK..', '..KKKSSSSSSKKK..',
          '..KKSSSSSSSSKK..', '..KSSKSSSSKSSK..', '..KSSKSSSSKSSK..', '..KSSSSSSSSSSK..',
          '...KSSSSSSSSK...', '..KKTTTTTTTTKK..', '.KTTTTTTTTTTTTK.', '.KTTDTTTTTTDTTK.',
          '.KSSDTTTTTTDSSK.', '..KKKPPPPPPKKK..', '...KPPPKKPPPK...', '...KKKK..KKKK...')
STAR = {'sa': '..#../..#../#####/..#../..#..', 'sb': '#...#/.#.#./..#../.#.#./#...#', 'sc': '#.#.#/.###./#####/.###./#.#.#'}


def runs(rows, on='#'):
    """Path data for a bitmap: one 1-high rectangle per horizontal run."""
    return ''.join(f'M{m.start()} {y}h{len(m[0])}v1h-{len(m[0])}z'
                   for y, row in enumerate(rows) for m in re.finditer(f'{on}+', row))


# --- the SVG: 846 wide, one unit per CSS pixel in the profile column, everything on a 2px grid ---
W, H, P, X2 = 846, 500, 28, 420           # canvas, padding, left edge of the right-hand column
svg, defs, frames = [], {k: runs(v.split('/')) for k, v in STAR.items()}, []
add = svg.append


def span(s, k):
    return (sum(len(GLYPHS[ch].split('/')[0]) + 1 if ch != ' ' else 6 for ch in s) - 1) * k


def text(x, y, s, k, fill):
    """Pixel text with its top-left at (x, y), k px per font pixel. Returns the x where it ends."""
    uses, cx = [], 0
    for ch in s:
        if ch != ' ':
            defs[f'g{ord(ch):x}'] = runs(GLYPHS[ch].split('/'))
            uses.append(f'<use href="#g{ord(ch):x}" x="{cx}"/>')
        cx += span(ch, 1) + 1
    add(f'<g transform="translate({x} {y}) scale({k})" fill="{fill}">{"".join(uses)}</g>')
    return x + span(s, k)


def plate(x, y, w, h, fill, s=2):
    """A rectangle whose corners are cut in two s-sized steps."""
    add(f'<path fill="{fill}" d="M{x + 2 * s} {y}h{w - 4 * s}v{s}h{s}v{s}h{s}v{h - 4 * s}h-{s}v{s}h-{s}v{s}h-{w - 4 * s}'
        f'v-{s}h-{s}v-{s}h-{s}v-{h - 4 * s}h{s}v-{s}h{s}z"/>')


def panel(x, y, w, h, fill):
    plate(x, y, w, h, INK)
    plate(x + 2, y + 2, w - 4, h - 4, fill)


def star(x, y, k, delay=0, period=1.6):
    """Plus, full star, cross, full star: a star that turns in place."""
    style = f' style="animation-duration:{period}s;animation-delay:-{delay}s"'
    add(f'<g transform="translate({x} {y}) scale({k})" fill="{CLAY}"><use href="#sa" class="fa"{style}/>'
        f'<use href="#sb" class="fb"{style}/><use href="#sc" class="fc"{style}/></g>')


def heading(x, y, s):
    star(x, y + 3, 3, delay=x / 500)
    text(x + 24, y, s, 3, CLAY)


# the card
plate(6, 6, W - 6, H - 6, CLAY, 4)
plate(0, 0, W - 6, H - 6, INK, 4)
plate(4, 4, W - 14, H - 14, PAPER, 4)

# hero: an idling sprite, the name, school and age, a line that keeps retyping itself
panel(P, P, 132, 132, TILE)
for x, y, k, delay in ((P + 12, P + 14, 2, 0), (P + 108, P + 92, 2, 1.1), (P + 16, P + 100, 2, 1.7)):
    add(f'<path class="tw" transform="translate({x} {y}) scale({k})" fill="{KRAFT}" d="M1 0h1v1h1v1h-1v1h-1v-1h-1v-1h1z" '
        f'style="animation-delay:-{delay}s"/>')
star(P + 102, P + 12, 3)
add(f'<rect class="shade" x="{P + 30}" y="{P + 122}" width="72" height="4" fill="{RULE}"/><g class="bob">'
    f'<g transform="translate({P + 18} {P + 26}) scale(6)">'
    + ''.join(f'<path fill="{fill}" d="{runs(SPRITE, on)}"/>'
              for on, fill in (('K', INK), ('S', SKIN), ('T', CLAY), ('D', DEEP), ('P', '#3D3D3A')))
    + f'<path class="lid" fill="{SKIN}" d="M5 5h1v1h-1zM10 5h1v1h-1z"/></g></g>')
NX = P + 160
text(NX + 4, 34, NAME, 8, CLAY)
text(NX, 30, NAME, 8, INK)
for x, y, k, delay in ((732, 34, 4, .4), (780, 58, 2, 1.5), (800, 30, 2, .9)):
    add(f'<path class="tw" transform="translate({x} {y}) scale({k})" fill="{CLAY}" d="M1 0h1v1h1v1h-1v1h-1v-1h-1v-1h1z" '
        f'style="animation-delay:-{delay}s"/>')
add(f'<path class="march" d="M{NX} 99H{W - 6 - P}" stroke="{CLAY}" stroke-width="2" stroke-dasharray="8 6"/>')
x = text(NX, 117, 'SCHOOL', 2, MUTE) + 12
x = text(x, 108, SCHOOL, 2, INK) + 10
x = text(x, 110, 'HIT', 3, INK) + 40
x = text(x, 117, 'AGE', 2, MUTE) + 12
text(x, 110, str(AGE), 3, INK)
TX, SLOT = text(NX, 140, '>', 3, CLAY) + 18, 4        # each tagline holds the row for SLOT seconds
cycle = SLOT * len(TAGLINES)
add('<g clip-path="url(#row)">')
for i, line in enumerate(TAGLINES):
    n, delay = len(line), (cycle - SLOT * i) % cycle
    typed, held, gone = n * .06 / cycle, (SLOT - .9) / cycle, (SLOT - .4) / cycle
    frames.append(f'@keyframes ty{i}{{0%{{opacity:1;transform:translateX(0)}}{typed:.2%}{{opacity:1;transform:translateX({n * 18}px)}}'
                  f'{held:.2%}{{opacity:1;transform:translateX({n * 18}px)}}{gone:.2%}{{opacity:1;transform:translateX(0)}}'
                  f'{gone + .0001:.2%},to{{opacity:0;transform:translateX(0)}}}}')
    add(f'<g class="slot" style="{"opacity:0;" if i else ""}animation-delay:-{delay}s">')
    text(TX, 140, line, 3, INK)
    add(f'</g><g class="type" style="animation-name:ty{i};animation-timing-function:steps({n});animation-delay:-{delay}s">'
        f'<rect x="{TX}" y="138" width="{n * 18 + 30}" height="25" fill="{PAPER}"/>'
        f'<rect class="caret" x="{TX}" y="140" width="12" height="21" fill="{CLAY}"/></g>')
add('</g>')
frames.append(f'@keyframes slot{{0%,{1 / len(TAGLINES):.2%}{{opacity:1}}{1 / len(TAGLINES) + .0001:.2%},to{{opacity:0}}}}')
add(f'<path d="M{P} 179H{W - 6 - P}" stroke="{RULE}" stroke-width="2" stroke-dasharray="2 4"/>')

# left column: the stack lights up one badge at a time; skills
heading(P, 198, 'STACK')
x, beat = P, .7
for i, name in enumerate(STACK):
    w, delay = span(name, 2) + 20, (len(STACK) - i) % len(STACK) * beat
    add(f'<g class="hop" style="animation-delay:-{delay:.1f}s">')
    panel(x, 232, w, 30, CARD)
    text(x + 10, 240, name, 2, INK)
    add(f'<g class="hot" style="animation-delay:-{delay:.1f}s">')
    plate(x + 2, 234, w - 4, 26, CLAY)
    text(x + 10, 240, name, 2, CARD)
    add('</g></g>')
    x += w + 8
frames.append(f'@keyframes hop{{0%,{1 / len(STACK):.2%}{{transform:translateY(-4px)}}{1 / len(STACK) + .0001:.2%},to{{transform:translateY(0)}}}}'
              f'@keyframes hot{{0%,{1 / len(STACK):.2%}{{opacity:1}}{1 / len(STACK) + .0001:.2%},to{{opacity:0}}}}')
heading(P, 292, 'SKILLS')
for i, skill in enumerate(SKILLS):
    star(P + 2, 328 + 28 * i, 2, delay=i * .8, period=3.2)
    text(P + 24, 326 + 28 * i, skill, 2, INK)
text(P, 452, 'GITHUB.COM/BEIZI6', 2, MUTE)

# right column: the two projects
heading(X2, 198, 'PROJECTS')


def project(y, title, lang, lines):
    panel(X2, y, 392, 112, CARD)
    text(X2 + 12, y + 12, title, 3, INK)
    w = span(lang, 2) + 12
    plate(X2 + 380 - w, y + 12, w, 22, CLAY)
    text(X2 + 386 - w, y + 16, lang, 2, CARD)
    for i, line in enumerate(lines):
        text(X2 + 12, y + 44 + 20 * i, line, 2, BODY)


project(232, 'OTTY-RS', 'RUST', ['A TERMINAL REBUILT FROM SCRATCH', 'RUST ENGINE, ELECTRON FRONTEND'])
label = f'{done}/{tracked}'
pitch = (368 - 8 - span(label, 2)) // tracked       # one cell per tracked capability
for i in range(tracked):
    cls = 'dn' if i < done else 'pt' if i < done + partial else 'op'
    add(f'<rect class="{cls}" x="{X2 + 12 + i * pitch}" y="320" width="{pitch - 1}" height="12" style="animation-delay:{i * .05:.2f}s"/>')
text(X2 + 380 - span(label, 2), 319, label, 2, INK)
project(356, 'CSWITCH', 'TS', ['LOCAL ANTHROPIC-COMPATIBLE', 'GATEWAY FOR 3RD-PARTY LLM APIS'])
x = text(X2 + 12, 444, 'CLIENT', 2, BODY) + 8
for stop in ('CSWITCH', 'LLM APIS'):                # requests march through the gateway
    add(f'<path class="march" d="M{x} 451h22" stroke="{CLAY}" stroke-width="2" stroke-dasharray="4 4" style="animation-duration:.5s"/>')
    x = text(x + 24, 444, ">", 2, CLAY) + 8
    if stop == 'CSWITCH':
        plate(x, 438, span(stop, 2) + 16, 26, INK)
        x = text(x + 8, 444, stop, 2, CARD) + 16
    else:
        text(x, 444, stop, 2, BODY)

CSS = f'''
.bob{{animation:bob 1.4s steps(1) infinite}}
.shade{{transform-box:fill-box;transform-origin:center;animation:shade 1.4s steps(1) infinite}}
.lid{{opacity:0;animation:lid 4.2s steps(1) infinite}}
.fa,.fb{{opacity:0}}.fa{{animation:fa steps(1) infinite}}.fb{{animation:fb steps(1) infinite}}.fc{{animation:fc steps(1) infinite}}
.tw{{animation:tw 2.4s steps(1) infinite}}
.march{{animation:march .8s steps(7) infinite}}
.slot{{animation:slot {cycle}s infinite}}
.type{{opacity:0;animation-duration:{cycle}s;animation-iteration-count:infinite}}
.caret{{animation:tw .8s steps(1) infinite}}
.hop{{animation:hop {beat * len(STACK)}s infinite}}
.hot{{opacity:0;animation:hot {beat * len(STACK)}s infinite}}
.dn{{fill:{CLAY};animation:glint 5s infinite}}
.pt{{fill:{KRAFT};animation:tw 1.2s steps(1) infinite}}
.op{{fill:{RULE}}}
@keyframes bob{{50%{{transform:translateY(-6px)}}}}
@keyframes shade{{50%{{transform:scaleX(.78)}}}}
@keyframes lid{{96%{{opacity:1}}}}
@keyframes fa{{0%{{opacity:1}}25%,to{{opacity:0}}}}
@keyframes fb{{0%,25%{{opacity:0}}50%{{opacity:1}}75%,to{{opacity:0}}}}
@keyframes fc{{0%{{opacity:0}}25%{{opacity:1}}50%{{opacity:0}}75%,to{{opacity:1}}}}
@keyframes tw{{50%{{opacity:.25}}}}
@keyframes march{{to{{stroke-dashoffset:-14}}}}
@keyframes glint{{0%,6%,to{{fill:{CLAY}}}3%{{fill:#F6C4AE}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
'''
doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges">'
       f'<title>Xu Yuanshan, pixel card</title><style>{CSS}{"".join(frames)}</style><defs>'
       + ''.join(f'<path id="{k}" d="{d}"/>' for k, d in defs.items())
       + f'<clipPath id="row"><rect x="{TX - 2}" y="136" width="{W - 6 - P - TX + 2}" height="28"/></clipPath></defs>'
       + ''.join(svg) + '</svg>')
ElementTree.fromstring(doc)     # the check: malformed markup stops here, before anything is written
(HERE / 'pixel.svg').write_text(doc, encoding='utf-8', newline='\n')

# --- README.md: the same facts as text, with links (GitHub keeps <a> inside <pre>) ---
alt = (f'Pixel-art profile card. {NAME.title()}. School: {SCHOOL} (Harbin Institute of Technology). Age: {AGE}. '
       f'Stack: {", ".join(STACK).title().replace("Ts", "TypeScript")}. Skills: {", ".join(SKILLS).lower()}. '
       f'Projects: otty-rs, a terminal rebuilt from scratch with a Rust engine and an Electron frontend, {done} of {tracked} '
       f'tracked capabilities done; CSwitch, a local Anthropic-compatible gateway for third-party LLM APIs.')
ship = '\n'.join(f'<a href="https://github.com/BeiZi6/{name}">{name}</a>{" " * (22 - len(name))}{lang:<12}{escape(what)}'
                 for name, lang, what in SHIP)
(HERE.parent / 'README.md').write_text(f'''<!-- Generated by assets/pixel.py from an otty-rs checkout. Edit the script, not this file. -->
<img alt="{escape(alt)}" src="assets/pixel.svg">

`$ whoami` Xu Yuanshan (徐元山), M.Eng. student at Harbin Institute of Technology. AI engineering and forward-deployed engineering: I ship LLM gateways, agent plugins and desktop apps end to end. Research: synthetic multimodal data (visible / IR / SAR) in UE5. Stack: Rust, TypeScript, Python, C, Go.

<pre>
$ ls ship/
{ship}
</pre>

`$ cat now` [otty-rs](https://github.com/BeiZi6/otty-rs), the Otty terminal rebuilt from scratch: a Rust engine (VT, PTY, fonts, rasteriser) behind an Electron frontend. {done} of {tracked} tracked capabilities done, {partial} partial, {todo} open, as of `{head}` ({date}). Design notes: [引擎报事件，应用做决定](https://blog.xyucode.top/p/2026-10-06-otty-rs-怎么分层)
''', encoding='utf-8', newline='\n')
print(f'{head} {date}: {done}/{tracked} done, {partial} partial, {todo} open | pixel.svg {len(doc) / 1024:.1f} KB, {W}x{H}')
