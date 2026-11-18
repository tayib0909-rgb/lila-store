#!/usr/bin/env python3
"""Builds the KDP paperback full-wrap cover (back + spine + front) as build/cover.html.

Spine width = page count x paper thickness. Defaults to KDP premium color paper.
Re-run after the interior page count changes, then: node build/render.js cover
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUTHOR = "[Author Name]"          # <- set before publishing
PAPER = {"premium_color": 0.002347, "standard_color": 0.002252}
paper = sys.argv[1] if len(sys.argv) > 1 else "premium_color"
pages = json.loads((ROOT / "build" / "manifest.json").read_text())["pages"]

TRIM_W, TRIM_H, BLEED = 8.5, 11.0, 0.125
spine = round(pages * PAPER[paper], 4)
W = BLEED + TRIM_W + spine + TRIM_W + BLEED
H = BLEED + TRIM_H + BLEED
SAFE = 0.375  # KDP: keep text 0.375in inside trim


def img(name):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if (ROOT / "images" / f"{name}{ext}").exists():
            return f"../images/{name}{ext}"
    return None


hero = img("COVER-front")
back_art = img("COVER-back")
ph = lambda id_, d: (f'<div class="ph"><div class="tag">Cover art · Illustration pending</div><div class="id">{id_}</div><div class="dir">{d}</div></div>')

hero_html = (f'<div class="hero" style="background-image:url(\'{hero}\')"></div>' if hero else
             '<div class="hero">' + ph("COVER-front", "A lineup of Golden Retriever, French Bulldog, Corgi, Husky, Pug and Dachshund in cozy Christmas accessories, each with a hilarious expression, photorealistic 3D, warm golden studio light, subtle falling snow") + "</div>")
back_html = (f'<div class="bart" style="background-image:url(\'{back_art}\')"></div>' if back_art else
             '<div class="bart" style="margin:.18in 0">' + ph("COVER-back", "Pug in a Santa hat looking shocked at a pile of unwrapped gifts") + "</div>")

html = f"""<!doctype html><html lang="en-US"><head><meta charset="utf-8"><title>Dogs Are Weird Cover</title>
<link rel="stylesheet" href="style.css"><style>
@page {{ size: {W}in {H}in; margin: 0; }}
html, body {{ background: #555; }}
.wrap {{ width: {W}in; height: {H}in; position: relative; overflow: hidden;
  background: radial-gradient(ellipse at 75% 35%, #2E6A4D 0%, #17402D 50%, #0D2619 100%); color: #FFF7E6; }}
.snow {{ opacity: .45; }}
.panel {{ position: absolute; top: {BLEED + SAFE}in; bottom: {BLEED + SAFE}in; }}
.front {{ left: {BLEED + TRIM_W + spine + SAFE}in; width: {TRIM_W - 2 * SAFE}in; display: flex; flex-direction: column; align-items: center; text-align: center; }}
.back {{ left: {BLEED + SAFE}in; width: {TRIM_W - 2 * SAFE}in; display: flex; flex-direction: column; }}
.spine {{ position: absolute; top: 0; bottom: 0; left: {BLEED + TRIM_W}in; width: {spine}in; background: #B3261E;
  display: flex; align-items: center; justify-content: center; }}
.spine div {{ transform: rotate(90deg); white-space: nowrap; font: 400 {min(15, spine * 72 * 0.62):.1f}pt "Lilita"; letter-spacing: .04em; color: #fff; }}
.spine div span {{ color: #F2D27A; }} .spine small {{ font: 600 7pt "InterB"; margin-left: .3in; letter-spacing: .1em; }}
.badge {{ position: absolute; top: -.15in; right: -.05in; width: 1.15in; height: 1.15in; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #FF6F61, #B3261E 60%, #7A140E);
  display: grid; place-items: center; text-align: center; font: 800 8pt/1.2 "InterB"; letter-spacing: .12em; text-transform: uppercase; color: #fff; transform: rotate(12deg);
  box-shadow: 0 8px 24px rgba(0,0,0,.4); border: 3px dashed rgba(255,255,255,.55); }}
.badge b {{ display: block; font: 400 22pt/1 "Lilita"; letter-spacing: 0; color: #F2D27A; }}
.t1 {{ font: 400 74pt/.88 "Lilita"; letter-spacing: .005em; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.25); margin-top: .15in; }}
.t2 {{ font: 400 74pt/.88 "Lilita"; color: #F2D27A; text-shadow: 0 4px 0 rgba(0,0,0,.25); }}
.sub {{ margin-top: .18in; background: #FFF7E6; color: #17402D; border-radius: 999px; padding: .09in .3in; font: 800 10.5pt/1.3 "InterB"; letter-spacing: .02em; max-width: 7in; }}
.hero {{ flex: 1; width: 100%; margin-top: .22in; border-radius: 26px; background-size: cover; background-position: center; position: relative; overflow: hidden; background-color: rgba(255,255,255,.08); }}
.ph {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: .4in; border: 2px dashed rgba(255,255,255,.5); border-radius: 26px; background: rgba(255,255,255,.08); }}
.ph .tag {{ color: #F2D27A; }} .ph .id {{ color: #fff; }} .ph .dir {{ color: rgba(255,247,230,.85); }}
.edition {{ margin-top: .18in; font: 800 9.5pt "InterB"; letter-spacing: .32em; text-transform: uppercase; color: #F2D27A; }}
.author {{ font: italic 500 13pt "Fraunces"; margin-top: .04in; }}
.back h3 {{ font: 400 30pt/1 "Lilita"; color: #F2D27A; }}
.back .lead {{ font: italic 400 13pt/1.45 "Fraunces"; margin: .14in 0 .16in; }}
.back ul {{ list-style: none; font: 500 10.5pt/1.45 "InterB"; }}
.back li {{ padding-left: .28in; position: relative; margin-bottom: .07in; }}
.back li::before {{ content: "★"; position: absolute; left: 0; font-size: 11pt; color: #F2D27A; }}
.bart {{ flex: 1; margin-bottom: 1.6in !important; border-radius: 20px; margin: .18in 0; position: relative; overflow: hidden; background-size: cover; background-position: center; }}
.back .gift {{ font: 700 19pt "Caveat"; color: #F2D27A; }}
.barcode {{ position: absolute; left: {BLEED + TRIM_W - 0.25 - 2}in; bottom: {BLEED + 0.25}in; width: 2in; height: 1.2in; background: #fff; border-radius: 4px; display: grid; place-items: center;
  font: 600 6.5pt "InterB"; color: #999; letter-spacing: .1em; text-align: center; }}
.guides .g {{ position: absolute; border: 0 dashed rgba(0,255,255,.8); }}
</style></head><body><div class="wrap">
<div class="snow"></div>
<div class="panel back">
  <h3>Warning: This Book Contains Extreme Levels of Dog.</h3>
  <p class="lead">Why does the Husky argue? Why does the Frenchie act like a tiny CEO? Why does the Golden Retriever love absolutely everyone, including the vacuum?</p>
  <ul>
    <li><b>103 real dog breeds</b> with stunning portraits, real facts and laugh-out-loud personality profiles</li>
    <li><b>8 hilarious categories</b>, from The Drama Queens to The Dogs Who Think They Own Everything</li>
    <li><b>15 comedy chapters:</b> dog dating profiles, text messages, zombie survival odds and more</li>
    <li><b>Christmas bonus:</b> festive portraits, a holiday quiz, awards and a keepsake page for your own dog</li>
  </ul>
  {back_html}
  <div class="gift" style="position:absolute;bottom:.15in;left:0;width:4.8in">The perfect gift for every dog lover (and every weird human).</div>
</div>
<div class="spine"><div>DOGS ARE WEIRD. <span>WE LOVE THEM.</span><small>{AUTHOR}</small></div></div>
<div class="panel front">
  <div class="badge"><div><b>2027</b>Christmas<br>Gift Edition</div></div>
  <div class="t1">DOGS ARE WEIRD.</div>
  <div class="t2">WE LOVE THEM.</div>
  <div class="sub">100+ Hilarious Dog Breeds, Crazy Personalities, Adorable Portraits &amp; Facts That Will Make You Laugh</div>
  {hero_html}
  <div class="edition">Christmas Gift Edition 2027</div>
  <div class="author">{AUTHOR}</div>
</div>
<div class="barcode">BARCODE AREA<br>(KDP places ISBN barcode)<br>keep clear</div>
</div></body></html>"""
(ROOT / "build" / "cover.html").write_text(html)
spec = {"paper": paper, "pages": pages, "spine_in": spine, "cover_w_in": round(W, 4), "cover_h_in": H}
(ROOT / "build" / "cover-spec.json").write_text(json.dumps(spec, indent=1))
print(spec)
