import math, pathlib
from playwright.sync_api import sync_playwright
OUT = pathlib.Path("stories/covers_staff"); OUT.mkdir(exist_ok=True)
W, H, CY = 1080, 1920, 960
GAP = 62  # staff line spacing
def staff():
    return "".join(f"<line x1='0' y1='{CY+k*GAP}' x2='{W}' y2='{CY+k*GAP}' stroke='#fff' stroke-width='4' opacity='.3'/>" for k in (-2,-1,0,1,2))
def path(f, x0=170, x1=910):
    # flat on the middle line to x0, the shape f(t) for t in 0..1 between x0 and x1, flat again to the edge
    pts = [(0, CY), (x0, CY)] + [(x0+(x1-x0)*i/400, CY - f(i/400)) for i in range(401)] + [(x1, CY), (W, CY)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
env = lambda t: math.sin(math.pi*t)  # rises from and returns to zero, so every cover ends on the middle line
SHAPES = {
 "1_start_here":   lambda t: 2.2*GAP*math.exp(-((t-.5)/.07)**2),                         # one struck note: a single jump
 "2_the_twelve":   lambda t: 1.3*GAP*env(t)*math.sin(2*math.pi*6*t),                     # twelve crests and troughs
 "3_the_listening":lambda t: 1.9*GAP*math.sin(math.pi*t)**2*math.sin(2*math.pi*4*t),     # a swell that rises and fades
 "4_harmony":      lambda t: 1.6*GAP*env(t)*math.sin(2*math.pi*2*t),                     # long, slow wave
 "5_attunements":  lambda t: -1.8*GAP*math.sin(math.pi*t)**3,                            # a breath down and back
 "6_flat":         lambda t: 0,                                                          # rest
}
def harmony_second(t): return -1.6*GAP*env(t)*math.sin(2*math.pi*2*t)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":W,"height":H})
    for k, f in SHAPES.items():
        extra = f"<path d='{path(harmony_second)}' fill='none' stroke='#fff' stroke-width='10' opacity='.5' stroke-linecap='round' stroke-linejoin='round'/>" if k == "4_harmony" else ""
        svg = f"<svg width='{W}' height='{H}'>{staff()}{extra}<path d='{path(f)}' fill='none' stroke='#fff' stroke-width='10' stroke-linecap='round' stroke-linejoin='round'/></svg>"
        pg.set_content(f"<body style='margin:0;background:#0d0d0e'>{svg}</body>")
        pg.screenshot(path=str(OUT/f"cover_{k}.png"))
    b.close()
