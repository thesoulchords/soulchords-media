import math, pathlib, subprocess, numpy as np, wave
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
F = (ROOT / "node_modules/@fontsource").resolve()
OUT = ROOT / "reel"; FR = OUT / "frames"; FR.mkdir(parents=True, exist_ok=True)
FPS, DUR = 30, 25.0
COLS = ["#74854A","#B06F57","#D4935A","#C4A15A","#A9483A","#6E9C87","#6F93AE","#5B6591","#7E6A9A","#6E7780","#A35C7A","#5E9EA3"]
LIT, NAME, NOTE, HZ = 0, "The Wildling", "C", 264.0

# ---------- audio ----------
sr = 44100; t = np.arange(int(sr*DUR))/sr
def breath(tt):  # 0..1 swell: inhale 4-8 & 12-16 rise, exhale fall; steady before/after
    b = np.full_like(tt, .55)
    for s in (5, 13):
        up = (tt >= s) & (tt < s+4); dn = (tt >= s+4) & (tt < s+8)
        b[up] = .55 + .45*np.sin((tt[up]-s)/4*math.pi/2)**2
        b[dn] = 1.0 - .45*np.sin((tt[dn]-s-4)/4*math.pi/2)**2
    return b
f = HZ
tone = (np.sin(2*np.pi*f*t) + .5*np.sin(2*np.pi*f*1.003*t) + .35*np.sin(2*np.pi*f*.9965*t)
        + .22*np.sin(2*np.pi*2*f*t) + .07*np.sin(2*np.pi*3*f*t) + .25*np.sin(2*np.pi*f/2*t))
env = np.clip(t/2.0, 0, 1) * np.clip((DUR-t)/3.5, 0, 1) * breath(t)
strike = np.exp(-t/2.2) * (np.sin(2*np.pi*2*f*t)*.25 + np.sin(2*np.pi*f*t)*.4) * np.clip(t/.02, 0, 1)
sig = tone*env*.9 + strike*.6
# light room reverb (simple multi-tap)
rev = np.zeros_like(sig)
for d, g in [(.031,.35),(.047,.3),(.071,.25),(.113,.2),(.167,.15),(.241,.1)]:
    n = int(d*sr); rev[n:] += sig[:-n]*g
sig = sig + rev*.5
sig = sig/np.max(np.abs(sig))*.6
stereo = np.stack([sig, np.roll(sig, int(.012*sr))], axis=1)
with wave.open(str(OUT/"tone.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((stereo*32767).astype(np.int16).tobytes())

# ---------- visuals ----------
pts = "".join(f'<circle id="p{i}" cx="{540+330*math.cos(math.radians(-90+i*30)):.1f}" cy="{860+330*math.sin(math.radians(-90+i*30)):.1f}" r="{20 if i==LIT else 9}" fill="{COLS[i] if i==LIT else "rgba(255,255,255,.28)"}"/>' for i in range(12))
gx, gy = 540+330*math.cos(math.radians(-90+LIT*30)), 860+330*math.sin(math.radians(-90+LIT*30))
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Corm;font-weight:300;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2')}}
@font-face{{font-family:Corm;font-weight:400;src:url('{F}/cormorant-garamond/files/cormorant-garamond-latin-400-normal.woff2')}}
@font-face{{font-family:EBI;font-style:italic;src:url('{F}/eb-garamond/files/eb-garamond-latin-400-italic.woff2')}}
@font-face{{font-family:Fig;font-weight:400;src:url('{F}/figtree/files/figtree-latin-400-normal.woff2')}}
*{{margin:0;padding:0}}body{{width:1080px;height:1920px;background:#0d0d0e;color:#fff;overflow:hidden;position:relative}}
.eye{{position:absolute;top:300px;width:100%;text-align:center;font-family:Fig;font-size:26px;letter-spacing:.32em;color:rgba(255,255,255,.6)}}
.cue{{position:absolute;top:1300px;width:100%;text-align:center;font-family:EBI;font-style:italic;font-size:76px;line-height:1.15;transition:none}}
.cs{{font-family:Corm;font-style:normal;font-weight:300;font-size:46px;line-height:1.2;margin-top:10px;color:rgba(255,255,255,.72)}}
.sub{{position:absolute;top:1235px;width:100%;text-align:center;font-family:Fig;font-size:24px;letter-spacing:.28em;color:rgba(255,255,255,.55)}}
.mark{{position:absolute;bottom:330px;left:0;right:0;display:flex;justify-content:center;align-items:baseline;gap:.42em;font-family:Corm;font-weight:400;font-size:28px;color:rgba(255,255,255,.75)}}
.mark span{{letter-spacing:.3em;margin-right:-.3em}}.mark i{{font-family:EBI;font-size:36px}}
</style></head><body>
<div class="eye">MORNING ATTUNEMENT</div>
<svg width="1080" height="1920" style="position:absolute;inset:0">
<circle id="glow2" cx="{gx:.1f}" cy="{gy:.1f}" r="90" fill="{COLS[LIT]}" opacity=".10"/>
<circle id="glow" cx="{gx:.1f}" cy="{gy:.1f}" r="46" fill="{COLS[LIT]}" opacity=".25"/>
<circle id="ring" cx="540" cy="860" r="330" fill="none" stroke="rgba(255,255,255,.8)" stroke-width="2"/>{pts}</svg>
<div class="sub" id="sub">{NAME.upper()} · {NOTE} · {HZ:g} HZ</div>
<div class="cue" id="cue"></div>
<div class="mark" id="mark"><span>THE</span><i>Soul</i><span>CHORDS</span></div>
<script>
const CUES=[[0,5,"At dawn, the Pythagoreans<br>tuned the soul with sound.",""],[5,9,"Inhale","the day\u2019s possibilities"],[9,13,"Exhale","yesterday\u2019s worries"],[13,17,"Inhale","one clear note"],[17,21,"Exhale","what isn\u2019t yours to carry"],[21,25.5,"Every soul has a sound.","Listen to yours."]];
function br(t){{for(const s of [5,13]){{if(t>=s&&t<s+4)return .55+.45*Math.sin((t-s)/4*Math.PI/2)**2; if(t>=s+4&&t<s+8)return 1-.45*Math.sin((t-s-4)/4*Math.PI/2)**2;}}return .55}}
window.draw=function(t){{
 const b=br(t), fade=Math.min(1,t/1.2)*Math.min(1,(25-t)/1.2);
 document.body.style.opacity=fade;
 const g=document.getElementById('glow'),g2=document.getElementById('glow2');
 g.setAttribute('r',36+40*b);g.setAttribute('opacity',.12+.25*b);g2.setAttribute('r',70+90*b);g2.setAttribute('opacity',.04+.10*b);
 document.getElementById('ring').setAttribute('r',326+8*b);
 let txt="",sb="",a=0;for(const [s,e,c,d] of CUES){{if(t>=s&&t<e){{txt=c;sb=d;a=Math.min(1,(t-s)/.8,(e-t)/.8);}}}}
 const cu=document.getElementById('cue');cu.innerHTML=txt+(sb?'<div class="cs">'+sb+'</div>':'');cu.style.opacity=Math.max(0,a);
}};
</script></body></html>"""
(OUT/"reel.html").write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.goto((OUT/"reel.html").resolve().as_uri()); pg.wait_for_timeout(600)
    n = int(FPS*DUR)
    for i in range(n):
        pg.evaluate(f"draw({i/FPS})")
        pg.screenshot(path=str(FR/f"f{i:04d}.jpg"), type="jpeg", quality=92)
    b.close()
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",str(FR/"f%04d.jpg"),"-i",str(OUT/"tone.wav"),
  "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",
  str(OUT/"morning_attunement_C_wildling.mp4")], check=True)
print("done")
