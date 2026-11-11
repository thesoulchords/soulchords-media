import math, pathlib, json
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
F = (ROOT / "node_modules/@fontsource").resolve()
OUT = ROOT / "grid"; OUT.mkdir(exist_ok=True)

N = [  # pitch order C..B: slug, name, note, hz, colour, text colour on it
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

def ring(size, lit=(), stroke="#111", quiet="#D9D9D9", all_on=False, tri=None, dot=0.022, litdot=0.036, sw=1.4, mono=None):
    c, r = size/2, size*0.40
    pts = [(c + r*math.cos(math.radians(-90+i*30)), c + r*math.sin(math.radians(-90+i*30))) for i in range(12)]
    s = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}"><circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{sw}" opacity=".9"/>']
    if tri:
        p = " ".join(f"{pts[IDX[k]][0]:.1f},{pts[IDX[k]][1]:.1f}" for k in tri)
        s.append(f'<polygon points="{p}" fill="{stroke}" fill-opacity=".05" stroke="{stroke}" stroke-width="{sw*1.3}" stroke-linejoin="round"/>')
    for i, (x, y) in enumerate(pts):
        col = mono or N[i][4]; on = all_on or N[i][0] in lit
        if on:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size*litdot*2.2:.1f}" fill="{col}" opacity=".14"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{size*litdot:.1f}" fill="{col}"/>')
        else:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size*dot:.1f}" fill="{quiet}"/>')
    return "".join(s) + "</svg>"

BASE = f"""
@font-face{{font-family:Corm;font-weight:300;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2')}}
@font-face{{font-family:Corm;font-weight:300;font-style:italic;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-300-italic.woff2')}}
@font-face{{font-family:Corm;font-weight:400;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-400-normal.woff2')}}
@font-face{{font-family:Fig;font-weight:300;src:url('{F}/figtree/files/figtree-latin-300-normal.woff2')}}
@font-face{{font-family:Fig;font-weight:400;src:url('{F}/figtree/files/figtree-latin-400-normal.woff2')}}
@font-face{{font-family:EBI;font-style:italic;src:url('{F}/eb-garamond/files/eb-garamond-latin-400-italic.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative}}
.fr{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:90px 110px 200px}}
.eye{{font-family:Fig;font-weight:400;font-size:22px;letter-spacing:.3em;text-transform:uppercase;opacity:.65}}
.h1{{font-family:Corm;font-weight:300;line-height:1.02}}
.it{{font-family:EBI;font-style:italic}}
.body{{font-family:Corm;font-weight:300;font-size:56px;line-height:1.28}}
.sm{{font-family:Fig;font-weight:300;font-size:30px;line-height:1.5}}
.mark{{position:absolute;bottom:70px;left:0;right:0;display:flex;justify-content:center;align-items:baseline;gap:.42em;font-family:Corm;font-weight:400;font-size:26px}}
.mark span{{letter-spacing:.3em;margin-right:-.3em}}
.mark i{{font-family:EBI;font-size:34px}}
.num{{position:absolute;top:70px;right:80px;font-family:Fig;font-size:20px;letter-spacing:.2em;opacity:.5}}
"""

def page(body, bg="#fff", fg="#111", n=None):
    num = f'<div class="num">{n}</div>' if n else ""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}body{{background:{bg};color:{fg}}}</style></head><body>{num}{body}<div class='mark'><span>THE</span><i>Soul</i><span>CHORDS</span></div></body></html>"

CTA = lambda bg="#fff", fg="#111": page(f"""<div class="fr">
<div style="margin-bottom:60px">{ring(300, all_on=True, stroke=fg)}</div>
<div class="h1" style="font-size:92px">Every soul has a sound.</div>
<div class="it" style="font-size:66px;margin-top:14px">Listen to yours.</div>
<div class="eye" style="margin-top:64px">Find your chord · link in bio</div></div>""", bg, fg)

posts = []  # (key, title, [html slides], caption)

# 1  Every soul has a sound (black single)
posts.append(("p1_every_soul", "Every soul has a sound", [page("""<div class="fr" style="padding-bottom:160px">
<div class="h1" style="font-size:120px">Every soul<br>has a sound.</div>
<div class="it" style="font-size:80px;margin-top:30px">Listen to yours.</div></div>""", "#111", "#fff")],
"""Every soul has a sound.

Before every label, before every name, there was vibration. The Soul Chords listen for the three notes that sound most clearly through you, and how they move together as one chord.

Find your chord · link in bio"""))

# 2  The twelve (white single, all twelve lit with names)
names = "".join(f'<span style="display:inline-flex;align-items:center;gap:10px;margin:8px 16px"><span style="width:12px;height:12px;border-radius:50%;background:{n[4]}"></span>{n[1]}</span>' for n in N)
posts.append(("p2_the_twelve", "Twelve notes, one octave", [page(f"""<div class="fr" style="padding-bottom:170px">
<div class="eye">The twelve</div>
<div style="margin:40px 0 36px">{ring(560, all_on=True)}</div>
<div class="h1" style="font-size:76px">If love were a single sound,<br><span class="it" style="font-size:66px">these twelve would be its octave.</span></div>
<div class="sm" style="font-size:26px;margin-top:34px;max-width:860px;font-family:Corm;font-size:30px;line-height:1.3">{names}</div></div>""")],
"""If love were a single sound, these twelve would be its octave.

Twelve notes, from C to B, each a pure thread of the same love. Every soul carries all twelve. Three sound most clearly through you, and together they are your chord.

Which three are yours? Find your chord · link in bio"""))

# 3  Boethius (Ancient Voices, black carousel)
bk, wt = "#111", "#fff"
posts.append(("p3_boethius", "Ancient Voices: Boethius", [
 page("""<div class="fr"><div class="eye" style="margin-bottom:70px">Ancient voices · I</div>
<div class="it" style="font-size:84px;line-height:1.18">“Human music is understood by anyone who descends into themselves.”</div>
<div class="eye" style="margin-top:70px">Boethius · <i style="text-transform:none;letter-spacing:.05em;font-family:EBI">De institutione musica</i> · c. 520</div></div>""", bk, wt),
 page("""<div class="fr"><div class="eye" style="margin-bottom:60px">Who said it</div>
<div class="body" style="font-size:60px">Around 520, the Roman philosopher Boethius named three kinds of music: the music of the heavens, the music we play, and between them, <span class="it">musica humana</span>, the music inside a person.</div></div>""", bk, wt, "2 / 4"),
 page("""<div class="fr"><div class="eye" style="margin-bottom:60px">What it means now</div>
<div class="body" style="font-size:62px">Fifteen centuries later, the idea is the same. You carry a harmony of your own, and it can be heard if you listen inward.</div></div>""", bk, wt, "3 / 4"),
 CTA(bk, wt)],
"""“Human music is understood by anyone who descends into themselves.” — Boethius, c. 520

Boethius named three kinds of music: the music of the heavens, the music we play, and musica humana, the music inside a person. The Soul Chords are a way of listening to yours.

Find your chord · link in bio"""))

def note_carousel(slug, line2, line3, n_post):
    i = IDX[slug]; s, name, note, hz, col, fg = N[i]
    thread = {"wildling":"Kinship with the Earth<br>and all living things","visionary":"Seeing what’s possible"}[slug]
    return [
     page(f"""<div class="fr"><div class="eye">One of the twelve · {note} · {hz} Hz</div>
<div style="margin:56px 0 50px">{ring(420, lit=[slug], stroke=fg, quiet=('rgba(17,17,17,.28)' if fg=='#111' else 'rgba(255,255,255,.35)'), mono=fg)}</div>
<div class="h1" style="font-size:120px">The {name}</div>
<div class="it" style="font-size:48px;margin-top:22px;max-width:760px">{thread}</div></div>""", col, fg),
     page(f"""<div class="fr"><div class="eye" style="margin-bottom:60px">In a life</div><div class="body">{line2}</div></div>""", col, fg, "2 / 4"),
     page(f"""<div class="fr"><div class="eye" style="margin-bottom:60px">{'The gift' if slug=='wildling' else 'The growing edge'}</div><div class="body">{line3}</div></div>""", col, fg, "3 / 4"),
     page(f"""<div class="fr"><div class="h1" style="font-size:96px">Is the {name}<br>one of your three?</div>
<div class="it" style="font-size:62px;margin-top:30px">Listen to yours.</div>
<div class="eye" style="margin-top:70px">Find your chord · link in bio</div></div>""", col, fg)]

posts.append(("p4_wildling", "The Notes: the Wildling", note_carousel("wildling",
 "Wildlings feel the land and its creatures as kin, not scenery. They notice what is growing, what is missing and what is grieving.",
 "Tending. Living in rhythm with the seasons, and reminding everyone near them that we belong to something larger.", 4),
"""The Wildling · C · 264 Hz

Kinship with the Earth and all living things. Wildlings feel the land and its creatures as kin, not scenery, and their gift is tending: living in rhythm with the seasons.

Is the Wildling one of your three? Find your chord · link in bio"""))

# 5  Pythagoras and the hammers (white carousel)
ratio = lambda a, b, nm: f'<div style="display:flex;align-items:baseline;justify-content:center;gap:40px;margin:18px 0"><span class="h1" style="font-size:150px;width:330px;text-align:right">{a}:{b}</span><span class="it" style="font-size:56px;width:340px;text-align:left">{nm}</span></div>'
posts.append(("p5_pythagoras", "Mathematics: Pythagoras and the hammers", [
 page(f"""<div class="fr"><div class="eye">The mathematics of harmony</div>
<div class="h1" style="font-size:118px;margin-top:50px">Pythagoras<br><span class="it" style="font-size:96px">and the hammers</span></div>
<div style="margin-top:60px">{''.join(f'<div style="height:2.5px;width:300px;background:{c};margin:11px auto"></div>' for c in ['#111','#A9483A','#111'])}</div></div>"""),
 page("""<div class="fr"><div class="body">The story goes that Pythagoras walked past a forge and heard the hammers ringing together: some in harmony, some clashing.</div></div>""", n="2 / 6"),
 page("""<div class="fr"><div class="body">He found that the sound followed number. Measure a string, halve it, and the note rises an octave. The sweetest harmonies were the simplest ratios.</div></div>""", n="3 / 6"),
 page(f"""<div class="fr"><div class="eye" style="margin-bottom:40px">The first three harmonies</div>{ratio(2,1,'the octave')}{ratio(3,2,'the fifth')}{ratio(4,3,'the fourth')}</div>""", n="4 / 6"),
 page("""<div class="fr"><div class="body">Simple ratios sound open and at rest. Complex ones rub and pulse. That tension isn’t a flaw: it is what makes music move.</div></div>""", n="5 / 6"),
 CTA()],
"""Pythagoras and the hammers.

The story goes that Pythagoras heard a forge ringing and found that harmony follows number: 2:1 is the octave, 3:2 the fifth, 4:3 the fourth. Simple ratios rest; complex ones rub. Both make music move.

Every soul has a sound. Find your chord · link in bio"""))

posts.append(("p6_visionary", "The Notes: the Visionary", note_carousel("visionary",
 "Visionaries see whole horizons at once: what a person, a project or a world could become. Holding that vision is the gift itself.",
 "Discernment. Choosing which visions to carry forward, and knowing when and where to land.", 6),
"""The Visionary · G · 395.56 Hz

Seeing what’s possible. Visionaries see whole horizons at once: what a person, a project or a world could become. Their growing edge is knowing when and where to land.

Is the Visionary one of your three? Find your chord · link in bio"""))

# 7  The twelve as baristas
lines = {
 "wildling":"Knows which hillside the beans came from, keeps a fern alive behind the counter, and quietly composts the grounds.",
 "keystone":"Knows your order, your dog’s name and that your mother was sick. Asks how she’s doing. Somehow has time for everyone in line.",
 "beacon":"Turns the morning rush into a small celebration. You walk out lighter and can’t say exactly why.",
 "manifestor":"Introduces the two regulars who turn out to need each other. A month later they’ve started something together.",
 "wayshower":"Started the reusable-cup discount and the community board. Already working on the next thing.",
 "noble":"Notices the person counting coins at the back of the line and quietly covers the difference.",
 "mirror":"Asks what you’re really in the mood for. By the time you answer, you’ve worked something out about your week.",
 "visionary":"Can already see this café as a bookshop, a gallery and a gathering place. Has the sketch on the back of a receipt.",
 "alchemist":"Somehow their lattes taste better, almost magical. Regulars swear it’s something in their hands.",
 "architect":"Redesigned the counter so the line moves twice as fast. The espresso is exactly right, every single time.",
 "activator":"Hands you your coffee, says one small thing, and three days later you realize it changed your week. They don’t remember saying it.",
 "portal":"Was humming the song stuck in your head. The idea for the new drink came to them in a dream. It’s somehow perfect.",
}
cover = page(f"""<div class="fr"><div>{ring(330, all_on=True)}</div><div class="eye" style="margin-top:58px">A series</div>
<div class="h1" style="font-size:112px;margin-top:22px">The twelve<br><span class="it" style="font-size:96px">as baristas</span></div>
<div class="sm" style="margin-top:40px;color:#555">Same café. Same order. Twelve ways love moves.</div>
<div class="eye" style="margin-top:60px;font-size:20px">Swipe →</div></div>""")
slides = [cover]
for k, n in enumerate(N):
    slides.append(page(f"""<div class="fr"><div class="eye">{n[2]} · {n[3]} Hz</div>
<div style="margin-top:40px">{ring(240, lit=[n[0]])}</div>
<div class="h1" style="font-size:96px;margin-top:40px">The {n[1]}</div>
<div style="width:70px;height:2.5px;background:{n[4]};margin:38px auto 42px"></div>
<div class="body" style="font-size:52px">{lines[n[0]]}</div></div>""", n=f"{k+2:02d} / 13"))
posts.append(("p7_baristas", "The Twelve as baristas", slides,
"""The twelve as baristas. Same café, same order, twelve ways love moves.

Which one is serving you? Which one are you? Tell us in the comments.

Find your chord · link in bio"""))

# 8  What is a chord? (geometry)
mini = lambda tri, nm: f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px">{ring(250, lit=tri, tri=tri, sw=1.2)}<div class="it" style="font-size:40px">{nm}</div></div>'
posts.append(("p8_chord", "Chord Geometry: what is a chord?", [
 page(f"""<div class="fr"><div class="eye">Chord geometry</div>
<div class="h1" style="font-size:112px;margin-top:40px">Twelve notes.<br><span class="it" style="font-size:94px">Any three make a chord.</span></div></div>"""),
 page(f"""<div class="fr"><div>{ring(560, lit=['wildling','wayshower','visionary'], tri=['wildling','wayshower','visionary'])}</div>
<div class="body" style="margin-top:40px;font-size:52px">Place the twelve notes around a circle. Your three make a triangle.</div></div>""", n="2 / 5"),
 page(f"""<div class="fr"><div class="h1" style="font-size:84px">220 chords.<br><span class="it" style="font-size:72px">Only thirteen geometries.</span></div>
<div style="display:flex;gap:20px;margin-top:60px">{mini(['wildling','wayshower','visionary'],'Major')}{mini(['wildling','keystone','beacon'],'Cluster')}{mini(['manifestor','visionary','portal'],'Augmented')}</div></div>""", n="3 / 5"),
 page("""<div class="fr"><div class="body">The geometry is the harmony. Some ring open and bright; some sit close and rub. Your chord shows where your gifts rest with ease, and where they grow one another through friction.</div></div>""", n="4 / 5"),
 CTA()],
"""Twelve notes. Any three make a chord.

Place the twelve around a circle and your three make a triangle. There are 220 possible chords and only thirteen geometries, and the geometry is the harmony: open and bright, or close and rubbing, each with its own music.

What geometry is yours? Find your chord · link in bio"""))

# 9  The universe began with sound (white single)
posts.append(("p9_universe", "The universe began with sound", [page(f"""<div class="fr" style="padding-bottom:170px">
<div style="margin-bottom:64px">{ring(300, all_on=True)}</div>
<div class="h1" style="font-size:104px">The universe began<br>with sound.</div>
<div class="it" style="font-size:78px;margin-top:22px">Listen to yours.</div></div>""")],
"""The universe began with sound. Listen to yours.

Every tradition that has listened closely has said it: before there was matter, there was vibration. The Soul Chords are a way of hearing the music that is yours.

Find your chord · link in bio"""))

manifest = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for key, title, sl, cap in posts:
        files = []
        for j, html in enumerate(sl, 1):
            f = OUT / f"{key}_{j:02d}.html"; f.write_text(html)
            pg.goto(f.resolve().as_uri()); pg.wait_for_timeout(250)
            png = OUT / f"{key}_{j:02d}.png"; pg.screenshot(path=str(png)); files.append(png.name)
        manifest.append({"key": key, "title": title, "slides": files, "caption": cap})
    b.close()
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
print(sum(len(m["slides"]) for m in manifest), "slides")
