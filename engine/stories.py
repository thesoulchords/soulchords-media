import math, pathlib, re, shutil
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
F = (ROOT / "node_modules/@fontsource").resolve()
OUT = ROOT / "stories"; shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir()

N = [
 ("wildling","Wildling","C","264","#74854A","#fff"),
 ("keystone","Keystone","C♯","279.70","#B06F57","#111"),
 ("beacon","Beacon","D","296.33","#D4935A","#111"),
 ("manifestor","Manifestor","D♯","313.96","#C4A15A","#111"),
 ("wayshower","Wayshower","E","332.62","#A9483A","#fff"),
 ("noble","Noble","F","352.40","#6E9C87","#111"),
 ("mirror","Mirror","F♯","373.36","#6F93AE","#111"),
 ("visionary","Visionary","G","395.56","#5B6591","#fff"),
 ("alchemist","Alchemist","G♯","419.08","#7E6A9A","#fff"),
 ("architect","Architect","A","444","#6E7780","#fff"),
 ("activator","Activator","A♯","470.40","#A35C7A","#fff"),
 ("portal","Portal","B","498.37","#5E9EA3","#111"),
]
IDX = {n[0]: i for i, n in enumerate(N)}

# thread + summary from the note pages, so stories match the site word for word
src = (ROOT / "note_page.html").read_text()
TXT = {m[0]: (m[1], m[2]) for m in re.findall(r"\['(\w+)','\w+','[^']*','#\w+','([^']*)','([^']*)'", src)}

def ring(size, lit=(), stroke="#fff", quiet="rgba(255,255,255,.3)", all_on=False, tri=None, line=None,
         dot=0.022, litdot=0.036, sw=1.6, mono=None):
    c, r = size/2, size*0.40
    pts = [(c + r*math.cos(math.radians(-90+i*30)), c + r*math.sin(math.radians(-90+i*30))) for i in range(12)]
    s = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}"><circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{sw}" opacity=".9"/>']
    if tri:
        p = " ".join(f"{pts[IDX[k]][0]:.1f},{pts[IDX[k]][1]:.1f}" for k in tri)
        s.append(f'<polygon points="{p}" fill="{stroke}" fill-opacity=".06" stroke="{stroke}" stroke-width="{sw*1.3}" stroke-linejoin="round"/>')
    if line:
        (x1, y1), (x2, y2) = pts[IDX[line[0]]], pts[IDX[line[1]]]
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw*1.3}" stroke-dasharray="2 9" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(pts):
        col = mono or N[i][4]; on = all_on or N[i][0] in lit
        if on:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size*litdot*2.2:.1f}" fill="{col}" opacity=".16"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{size*litdot:.1f}" fill="{col}"/>')
        else:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size*dot:.1f}" fill="{quiet}"/>')
    return "".join(s) + "</svg>"

CSS = f"""
@font-face{{font-family:Corm;font-weight:300;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2')}}
@font-face{{font-family:Corm;font-weight:400;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-400-normal.woff2')}}
@font-face{{font-family:EBI;font-style:italic;src:url('{F}/eb-garamond/files/eb-garamond-latin-400-italic.woff2')}}
@font-face{{font-family:Fig;font-weight:300;src:url('{F}/figtree/files/figtree-latin-300-normal.woff2')}}
@font-face{{font-family:Fig;font-weight:400;src:url('{F}/figtree/files/figtree-latin-400-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;position:relative;font-family:Fig}}
.f{{position:absolute;left:0;right:0;top:260px;bottom:360px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 110px}}
.eye{{font-family:Fig;font-size:26px;letter-spacing:.32em;text-transform:uppercase;opacity:.62}}
.h{{font-family:EBI;font-style:italic;font-size:92px;line-height:1.12;margin-top:56px}}
.h2{{font-family:Corm;font-weight:300;font-size:128px;line-height:1;margin-top:52px}}
.th{{font-family:EBI;font-style:italic;font-size:50px;line-height:1.25;margin-top:30px}}
.b{{font-family:Corm;font-weight:300;font-size:52px;line-height:1.35;margin-top:44px;max-width:820px;opacity:.86}}
.rule{{width:80px;height:2px;margin:46px auto 0;opacity:.7}}
.cta{{font-family:Fig;font-size:26px;letter-spacing:.26em;text-transform:uppercase;margin-top:70px;padding:24px 46px;border:1.5px solid currentColor;border-radius:999px;opacity:.85}}
.mark{{position:absolute;bottom:300px;left:0;right:0;display:flex;justify-content:center;align-items:baseline;gap:.42em;font-family:Corm;font-weight:400;font-size:28px;opacity:.8}}
.mark span{{letter-spacing:.3em;margin-right:-.3em}}.mark i{{font-family:EBI;font-size:36px}}
"""
MARK = "<div class='mark'><span>THE</span><i>Soul</i><span>CHORDS</span></div>"

def page(body, bg="#0d0d0e", fg="#fff"):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body style='background:{bg};color:{fg}'><div class='f'>{body}</div>{MARK}</body></html>"

S = {}  # folder -> list of (name, html)

# ---------- 1. Start here ----------
S["1_start_here"] = [
 ("01", page(f"<div>{ring(420, all_on=True)}</div><div class='h'>Every soul<br>has a sound.</div><div class='b'>The Soul Chords is a way of hearing who you are.</div>")),
 ("02", page(f"<div class='eye'>Twelve notes</div><div style='margin-top:56px'>{ring(560, all_on=True, litdot=.03)}</div><div class='b'>Twelve notes, twelve ways of being.<br>Each one a gift the world needs.</div>")),
 ("03", page(f"<div class='eye'>Your chord</div><div style='margin-top:56px'>{ring(520, lit=('wildling','wayshower','visionary'), tri=('wildling','wayshower','visionary'))}</div><div class='h' style='font-size:84px'>Three notes are yours.</div><div class='b'>Played together, they are your chord.</div>")),
 ("04", page(f"<div class='eye'>The listening</div><div class='h'>Hear the twelve.<br>Notice which are yours.</div><div class='b'>A guided listening, about thirty minutes.<br>Free.</div>")),
 ("05", page(f"<div>{ring(300, all_on=True)}</div><div class='h'>Find your chord.</div><div class='cta'>Link in bio</div>")),
]

# ---------- 2. The Twelve ----------
tw = [("00", page(f"<div class='eye'>The twelve</div><div style='margin-top:56px'>{ring(560, all_on=True, litdot=.03)}</div><div class='h' style='font-size:84px'>Meet the twelve notes.</div><div class='b'>Tap through, C to B.</div>"))]
for i, (slug, name, note, hz, col, fg) in enumerate(N):
    thread, summ = TXT[slug]
    tw.append((f"{i+1:02d}", page(
        f"<div class='eye'>{note} · {hz} Hz</div><div style='margin-top:50px'>{ring(380, lit=(slug,), stroke=fg, quiet=('rgba(255,255,255,.4)' if fg=='#fff' else 'rgba(0,0,0,.28)'), mono=fg)}</div>"
        f"<div class='h2'>The {name}</div><div class='th'>{thread}</div><div class='rule' style='background:{fg}'></div><div class='b' style='font-size:46px'>{summ}</div>",
        bg=col, fg=fg)))
tw.append(("13", page(f"<div>{ring(300, all_on=True)}</div><div class='h' style='font-size:84px'>Which three are yours?</div><div class='cta'>Link in bio</div>")))
S["2_the_twelve"] = tw

# ---------- 3. The listening ----------
S["3_the_listening"] = [
 ("01", page(f"<div class='eye'>The listening · 1</div><div style='margin-top:56px'>{ring(440, lit=('wildling','visionary'), line=('wildling','visionary'))}</div><div class='h' style='font-size:84px'>It begins with<br>an attunement.</div><div class='b'>The open fifth, C and G, to settle in.</div>")),
 ("02", page(f"<div class='eye'>The listening · 2</div><div class='h'>The twelve notes,<br>one at a time.</div><div class='b'>About thirty minutes. Find a quiet place, and listen for what moves in you.</div>")),
 ("03", page(f"<div class='eye'>The listening · 3</div><div style='margin-top:56px'>{ring(440, lit=('beacon','noble','portal'), tri=('beacon','noble','portal'))}</div><div class='h' style='font-size:84px'>Your reading.</div><div class='b'>Your three notes, the shape of your chord, and what they mean together.</div>")),
 ("04", page(f"<div>{ring(300, all_on=True)}</div><div class='h'>Begin the listening.</div><div class='b'>Free.</div><div class='cta' style='margin-top:50px'>Link in bio</div>")),
]

# ---------- 4. Harmony ----------
S["4_harmony"] = [
 ("01", page(f"<div class='eye'>Harmony</div><div style='margin-top:56px'>{ring(460, lit=('mirror','architect'), line=('mirror','architect'))}</div><div class='h' style='font-size:84px'>Hear where<br>you harmonize.</div><div class='b'>Any two notes, side by side.</div>")),
 ("02", page(f"<div class='eye'>Harmony</div><div class='h'>Invite someone<br>from your reading.</div><div class='b'>A partner, a friend, a sister. See where your chords meet.</div>")),
 ("03", page(f"<div>{ring(300, all_on=True)}</div><div class='h'>Free, with<br>every reading.</div><div class='cta'>Link in bio</div>")),
]

# ---------- 5. Attunements ----------
S["5_attunements"] = [
 ("01", page(f"<div class='eye'>Morning Attunement</div><div style='margin-top:56px'>{ring(420, lit=('wildling',))}</div><div class='h' style='font-size:84px'>At dawn, the Pythagoreans tuned the soul with sound.</div><div class='b'>Every Monday, one note to begin the week. Sound on.</div>")),
]

# ---------- covers (1080x1920, glyph centred for the circle crop) ----------
def cover(svg):
    return f"<!doctype html><html><body style='margin:0;width:1080px;height:1920px;background:#0d0d0e;display:flex;align-items:center;justify-content:center'>{svg}</body></html>"
W = "#fff"; Q = "rgba(255,255,255,.38)"
def g(inner): return f"<svg width='560' height='560' viewBox='0 0 560 560'>{inner}</svg>"
COV = {
 "1_start_here": g(f"<circle cx='280' cy='280' r='200' fill='none' stroke='{W}' stroke-width='5'/><circle cx='280' cy='80' r='26' fill='{W}'/>"),
 "2_the_twelve": g("<circle cx='280' cy='280' r='200' fill='none' stroke='#fff' stroke-width='5'/>" + "".join(f"<circle cx='{280+200*math.cos(math.radians(-90+i*30)):.1f}' cy='{280+200*math.sin(math.radians(-90+i*30)):.1f}' r='17' fill='{N[i][4]}'/>" for i in range(12))),
 "3_the_listening": g("".join(f"<circle cx='280' cy='280' r='{r}' fill='none' stroke='{W}' stroke-width='5' opacity='{o}'/>" for r, o in [(70,1),(140,.6),(210,.3)]) + f"<circle cx='280' cy='280' r='20' fill='{W}'/>"),
 "4_harmony": g(f"<circle cx='210' cy='280' r='140' fill='none' stroke='{W}' stroke-width='5'/><circle cx='350' cy='280' r='140' fill='none' stroke='{W}' stroke-width='5'/>"),
 "5_attunements": g(f"<path d='M110 330 A170 170 0 0 1 450 330' fill='none' stroke='{W}' stroke-width='5'/><line x1='60' y1='330' x2='500' y2='330' stroke='{W}' stroke-width='5'/>"
                    + "".join(f"<line x1='{280+215*math.cos(math.radians(a)):.1f}' y1='{330-215*math.sin(math.radians(a)):.1f}' x2='{280+250*math.cos(math.radians(a)):.1f}' y2='{330-250*math.sin(math.radians(a)):.1f}' stroke='{W}' stroke-width='5' stroke-linecap='round' opacity='.6'/>" for a in (30,60,90,120,150))
                    + f"<line x1='160' y1='390' x2='400' y2='390' stroke='{Q}' stroke-width='5'/><line x1='220' y1='440' x2='340' y2='440' stroke='{Q}' stroke-width='5'/>"),
}

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    def shot(html, path):
        tmp = OUT / "_t.html"; tmp.write_text(html); pg.goto(tmp.as_uri()); pg.wait_for_timeout(250); pg.screenshot(path=str(path))
    for folder, frames in S.items():
        d = OUT / folder; d.mkdir()
        for name, html in frames: shot(html, d / f"{folder[2:]}_{name}.png")
    cd = OUT / "covers"; cd.mkdir()
    for k, svg in COV.items(): shot(cover(svg), cd / f"cover_{k}.png")
    (OUT / "_t.html").unlink(); b.close()
print("done")
