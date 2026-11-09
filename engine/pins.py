import math, pathlib, re, json, shutil
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
F = (ROOT / "node_modules/@fontsource").resolve()
OUT = ROOT / "pins"; shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir()
SITE = "https://thesoulchords.com"

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
src = (ROOT / "note_page.html").read_text()
TXT = {m[0]: (m[1], m[2]) for m in re.findall(r"\['(\w+)','\w+','[^']*','#\w+','([^']*)','([^']*)'", src)}
IVORY, INK, BLACK = "#F6F2EC", "#141414", "#0d0d0e"

def ring(size, lit=(), stroke="#111", quiet="#CFCFCF", all_on=False, dot=0.022, litdot=0.036, sw=1.6, mono=None):
    c, r = size/2, size*0.40
    pts = [(c + r*math.cos(math.radians(-90+i*30)), c + r*math.sin(math.radians(-90+i*30))) for i in range(12)]
    s = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}"><circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{sw}" opacity=".9"/>']
    for i, (x, y) in enumerate(pts):
        col = mono or N[i][4]; on = all_on or N[i][0] in lit
        if on: s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size*litdot*2.2:.1f}" fill="{col}" opacity=".15"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{size*litdot:.1f}" fill="{col}"/>')
        else: s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size*dot:.1f}" fill="{quiet}"/>')
    return "".join(s) + "</svg>"

CSS = f"""
@font-face{{font-family:Corm;font-weight:300;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2')}}
@font-face{{font-family:Corm;font-weight:400;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-400-normal.woff2')}}
@font-face{{font-family:EBI;font-style:italic;src:url('{F}/eb-garamond/files/eb-garamond-latin-400-italic.woff2')}}
@font-face{{font-family:Fig;font-weight:300;src:url('{F}/figtree/files/figtree-latin-300-normal.woff2')}}
@font-face{{font-family:Fig;font-weight:400;src:url('{F}/figtree/files/figtree-latin-400-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1000px;height:1500px;overflow:hidden;position:relative}}
.f{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:110px 90px 190px}}
.eye{{font-family:Fig;font-size:22px;letter-spacing:.3em;text-transform:uppercase;opacity:.65}}
.t{{font-family:Corm;font-weight:300;line-height:1.02}}
.it{{font-family:EBI;font-style:italic}}
.b{{font-family:Corm;font-weight:300;font-size:44px;line-height:1.32}}
.url{{position:absolute;bottom:130px;left:0;right:0;text-align:center;font-family:Fig;font-size:24px;letter-spacing:.14em;opacity:.75}}
.mark{{position:absolute;bottom:62px;left:0;right:0;display:flex;justify-content:center;align-items:baseline;gap:.42em;font-family:Corm;font-weight:400;font-size:26px}}
.mark span{{letter-spacing:.3em;margin-right:-.3em}}.mark i{{font-family:EBI;font-size:34px}}
"""
def page(body, bg, fg, url):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body style='background:{bg};color:{fg}'>"
            f"<div class='f'>{body}</div><div class='url'>{url}</div><div class='mark'><span>THE</span><i>Soul</i><span>CHORDS</span></div></body></html>")

PINS = []  # dict(key, html, title, desc, link, board)

# --- 12 note pins: one per soul archetype, linking to its note page ---
for slug, name, note, hz, col, fg in N:
    thread, summ = TXT[slug]
    q = "rgba(255,255,255,.4)" if fg == "#fff" else "rgba(0,0,0,.25)"
    html = page(f"""<div class="eye">Soul archetype · {note} · {hz} Hz</div>
<div style="margin-top:70px">{ring(400, lit=(slug,), stroke=fg, quiet=q, mono=fg)}</div>
<div class="t" style="font-size:{132 if len(name)<9 else 112}px;margin-top:64px;white-space:nowrap">The {name}</div>
<div class="it" style="font-size:46px;margin-top:26px;line-height:1.25">{thread}</div>
<div style="width:80px;height:2px;background:{fg};opacity:.7;margin:46px auto"></div>
<div class="b" style="max-width:780px">{summ}</div>""", col, fg, f"Hear the {name} · thesoulchords.com")
    PINS.append(dict(key=f"note_{slug}", html=html, board="The 12 Soul Archetypes", link=f"{SITE}/note/{slug}",
        title=f"The {name} soul archetype: {thread[0].lower() + thread[1:]}",
        desc=f"{summ} The {name} is one of twelve soul archetypes in The Soul Chords, each a note of the octave. Its note is {note} at {hz} Hz. Hear it, and find the three notes that make your soul chord."))

# --- Reference chart: the 12 soul notes and their frequencies ---
rows = "".join(f"""<div style="display:flex;align-items:center;gap:30px;padding:10px 0;border-bottom:1px solid rgba(0,0,0,.12)">
<div style="width:34px;height:34px;border-radius:50%;background:{col};flex:none"></div>
<div style="font-family:Fig;font-size:28px;width:70px;text-align:left">{note}</div>
<div style="font-family:Corm;font-size:44px;flex:1;text-align:left">The {name}</div>
<div style="font-family:Fig;font-weight:300;font-size:28px;opacity:.7">{hz} Hz</div></div>""" for slug, name, note, hz, col, fg in N)
PINS.append(dict(key="chart_twelve", board="Sound and the Soul", link=f"{SITE}/archetypes",
    html=page(f"""<div class="eye">A reference chart</div>
<div class="t" style="font-size:88px;margin-top:26px">The 12 Soul Notes</div>
<div class="it" style="font-size:44px;margin-top:14px">and their frequencies</div>
<div style="width:100%;margin-top:46px;border-top:1px solid rgba(0,0,0,.12)">{rows}</div>""", IVORY, INK, "thesoulchords.com"),
    title="The 12 soul notes and their frequencies: a chart of the soul archetypes",
    desc="Twelve notes of the octave, from C at 264 Hz to B at 498.37 Hz, each a soul archetype: Wildling, Keystone, Beacon, Manifestor, Wayshower, Noble, Mirror, Visionary, Alchemist, Architect, Activator and Portal. Three sound most clearly through you, and together they are your soul chord."))

# --- Which one are you? ---
names = "".join(f"<div style='display:flex;align-items:center;gap:16px;font-family:Corm;font-size:40px;text-align:left'><span style='width:24px;height:24px;border-radius:50%;background:{col};flex:none'></span>{name}</div>" for _, name, _, _, col, _ in N)
PINS.append(dict(key="quiz_which", board="Find Your Soul Chord", link=SITE,
    html=page(f"""<div class="eye">Free · about thirty minutes</div>
<div class="it" style="font-size:96px;line-height:1.08;margin-top:40px">Which of the 12 soul notes are you?</div>
<div style="margin-top:56px">{ring(380, all_on=True, stroke="#fff", quiet="#555")}</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px 30px;margin-top:56px;width:100%">{names}</div>""", BLACK, "#fff", "Find your chord · thesoulchords.com"),
    title="Which of the 12 soul archetypes are you? A free soul chord listening",
    desc="A free, guided listening of about thirty minutes. Hear the twelve notes one at a time and notice which three are yours. Together they make your soul chord, with a reading of what your three notes mean together."))

# --- Pythagoras's ratios ---
def bar(frac, op): return f"<div style='height:6px;width:{int(700*frac)}px;background:{INK};opacity:{op};border-radius:3px'></div>"
ratio = lambda r, n, lines, line: f"""<div style="display:flex;align-items:center;gap:40px;padding:36px 0;border-bottom:1px solid rgba(0,0,0,.12);text-align:left">
<div style="font-family:Corm;font-size:92px;width:170px">{r}</div><div style="flex:1"><div style="font-family:Corm;font-size:48px">The {n}</div>
<div style="display:flex;flex-direction:column;gap:12px;margin:18px 0">{lines}</div><div style="font-family:Fig;font-weight:300;font-size:26px;opacity:.7">{line}</div></div></div>"""
PINS.append(dict(key="chart_pythagoras", board="Music of the Spheres", link=f"{SITE}/archetypes",
    html=page(f"""<div class="eye">The music of number</div>
<div class="t" style="font-size:92px;margin-top:34px">Pythagoras's<br>harmony ratios</div>
<div class="b" style="font-size:36px;margin-top:30px;max-width:760px">Halve a string and it sings an octave higher. Harmony follows simple number.</div>
<div style="width:100%;margin-top:40px;border-top:1px solid rgba(0,0,0,.12)">
{ratio("2:1","octave",bar(1,.9)+bar(.5,.9),"The same note, higher. The most at rest.")}
{ratio("3:2","fifth",bar(1,.9)+bar(2/3,.9),"Open and strong. The heart of most music.")}
{ratio("4:3","fourth",bar(1,.9)+bar(3/4,.9),"Steady, with a gentle lift.")}</div>""", IVORY, INK, "thesoulchords.com"),
    title="Pythagoras's harmony ratios: the octave 2:1, the fifth 3:2 and the fourth 4:3",
    desc="The story goes that Pythagoras heard a forge ringing and found that harmony follows number. A string halved sounds the octave (2:1); two thirds of it, the fifth (3:2); three quarters, the fourth (4:3). The root of the music of the spheres, and of The Soul Chords."))

# --- Ritual how-to ---
step = lambda n, h, t: f"""<div style="display:flex;gap:40px;text-align:left;padding:34px 0;border-bottom:1px solid rgba(255,255,255,.14)">
<div style="font-family:Corm;font-size:84px;width:70px;opacity:.6;line-height:1">{n}</div>
<div><div class="it" style="font-size:52px">{h}</div><div class="b" style="font-size:36px;margin-top:10px;opacity:.8">{t}</div></div></div>"""
PINS.append(dict(key="ritual_morning", board="Morning Rituals", link=SITE,
    html=page(f"""<div class="eye">Morning ritual · two minutes</div>
<div class="t" style="font-size:96px;margin-top:34px">A morning<br>sound ritual</div>
<div class="b" style="font-size:36px;margin-top:28px;max-width:760px;opacity:.8">At dawn, the Pythagoreans tuned the soul with sound before the day began.</div>
<div style="width:100%;margin-top:40px;border-top:1px solid rgba(255,255,255,.14)">
{step(1,"Sound one clear note","A tuning fork, a singing bowl, a single key on a piano.")}
{step(2,"Breathe with it","Inhale for four as it rings, exhale for four as it fades.")}
{step(3,"Let it settle","Wait for the silence before the first word of the day.")}</div>""", BLACK, "#fff", "thesoulchords.com"),
    title="A two-minute morning sound ritual, the way the Pythagoreans began the day",
    desc="A simple morning routine for the soul: sound one clear note, breathe with it as it rings and fades, and let the silence settle before you speak. The Pythagoreans began each day with music so the soul would wake well-tuned."))

# --- Ancient quote ---
PINS.append(dict(key="quote_boethius", board="Ancient Wisdom Quotes", link=SITE,
    html=page(f"""<div style="flex:1"></div><div class="it" style="font-size:150px;line-height:.5;opacity:.5">“</div>
<div class="it" style="font-size:72px;line-height:1.22;margin-top:30px">Human music is understood by anyone who descends into themselves.</div>
<div style="width:80px;height:2px;background:#fff;opacity:.6;margin:56px auto 40px"></div>
<div class="eye">Boethius · c. 520</div><div style="flex:1"></div>""", BLACK, "#fff", "thesoulchords.com"),
    title="“Human music is understood by anyone who descends into themselves.” Boethius",
    desc="Around 520 the philosopher Boethius named three kinds of music: the music of the heavens, the music we play, and musica humana, the music inside a person. An ancient quote on sound and the soul."))

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1000,"height":1500})
    for pin in PINS:
        t = OUT/"_t.html"; t.write_text(pin["html"]); pg.goto(t.as_uri()); pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT/f"{pin['key']}.jpg"), type="jpeg", quality=92)
    b.close()
json.dump([{k: v for k, v in p.items() if k != "html"} for p in PINS], open(OUT/"manifest.json","w"), ensure_ascii=False, indent=1)
(OUT/"_t.html").unlink(); print(len(PINS))
