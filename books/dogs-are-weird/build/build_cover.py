#!/usr/bin/env python3
"""Builds the KDP paperback full-wrap cover (back + spine + front) as build/cover.html.

Spine width = page count x paper thickness. Defaults to KDP premium color paper.
Re-run after the interior page count changes, then: node build/render.js cover
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUTHOR = "Tayeb Msalem"
EDITION = "Christmas Gift Edition · 2027"
PAPER = {"premium_color": 0.002347, "standard_color": 0.002252}
paper = sys.argv[1] if len(sys.argv) > 1 else "premium_color"
pages = json.loads((ROOT / "build" / "manifest.json").read_text())["pages"]

TRIM_W, TRIM_H, BLEED = 8.5, 11.0, 0.125
spine = round(pages * PAPER[paper], 4)
W = BLEED + TRIM_W + spine + TRIM_W + BLEED
H = BLEED + TRIM_H + BLEED
SAFE = 0.375  # KDP: keep text 0.375in inside trim
FX = BLEED + TRIM_W + spine          # left edge of the front trim
PAD = BLEED + SAFE + 0.1             # text inset from the outer bleed edge


def img(name):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if (ROOT / "images" / f"{name}{ext}").exists():
            return f"../images/{name}{ext}"
    return None


hero = img("COVER-front")
back_art = img("COVER-back")
FRONT_PHOTO_H = round((TRIM_W + BLEED) / 1.5, 3)   # full-bleed band at the image's own 3:2 shape
BACK_PHOTO_TOP, BACK_PHOTO_H = 4.55, 4.75
spine_pt = min(15, spine * 72 * 0.55)

html = f"""<!doctype html><html lang="en-US"><head><meta charset="utf-8"><title>Dogs Are Weird Cover</title>
<link rel="stylesheet" href="style.css"><style>
@page {{ size: {W}in {H}in; margin: 0; }}
html, body {{ background: #555; }}
:root {{ --green: #123A28; --deep: #0A2318; --gold: #E9C46A; --gold2: #F6DE9C; --cream: #FFF8EA; }}
.wrap {{ width: {W}in; height: {H}in; position: relative; overflow: hidden; color: var(--cream);
  background: radial-gradient(ellipse 60% 55% at 78% 22%, #1F5A3E 0%, var(--green) 55%, var(--deep) 100%); }}
.snow {{ opacity: .32; }}
.abs {{ position: absolute; }}

/* ---------- photos ---------- */
.photo {{ position: absolute; background-size: cover; background-position: center; }}
.photo::after {{ content: ""; position: absolute; left: 0; right: 0; }}
.fphoto {{ left: {FX}in; width: {TRIM_W + BLEED}in; bottom: 0; height: {FRONT_PHOTO_H}in; background-position: center 40%;
  -webkit-mask-image: linear-gradient(transparent 0, #000 1.3in); mask-image: linear-gradient(transparent 0, #000 1.3in); }}
.fphoto::after {{ bottom: 0; height: 1.55in; background: linear-gradient(rgba(6,22,15,0), rgba(6,22,15,.92)); }}
.bphoto {{ left: 0; width: {BLEED + TRIM_W}in; top: {BACK_PHOTO_TOP}in; bottom: 0; background-position: 18% 45%;
  -webkit-mask-image: linear-gradient(transparent 0, #000 1.1in); mask-image: linear-gradient(transparent 0, #000 1.1in); }}
.bphoto::after {{ bottom: 0; height: 2.4in; background: linear-gradient(rgba(6,22,15,0), rgba(6,22,15,.9) 70%); }}

/* ---------- front ---------- */
.front {{ left: {FX + SAFE}in; width: {TRIM_W - 2 * SAFE}in; top: {BLEED + SAFE + 0.15}in; text-align: center; }}
.kicker {{ display: flex; align-items: center; justify-content: center; gap: .16in;
  font: 700 9.5pt "InterB"; letter-spacing: .34em; text-transform: uppercase; color: var(--gold); }}
.kicker::before, .kicker::after {{ content: ""; height: 1px; width: .9in; background: linear-gradient(90deg, rgba(233,196,106,0), var(--gold)); }}
.kicker::after {{ transform: scaleX(-1); }}
.title {{ margin-top: .2in; font: 400 112pt/.86 "Lilita"; letter-spacing: .01em; color: #fff;
  text-shadow: 0 .05in 0 rgba(0,0,0,.28), 0 .12in .35in rgba(0,0,0,.35); }}
.love {{ margin-top: .1in; font: italic 800 60pt/1 "Fraunces"; font-variation-settings: "SOFT" 100, "WONK" 1; color: var(--gold);
  text-shadow: 0 .04in .18in rgba(0,0,0,.35); }}
.rule {{ width: 1.1in; height: 2px; margin: .2in auto .16in; background: var(--gold); opacity: .8; }}
.sub {{ font: 600 13pt/1.42 "InterB"; color: var(--cream); max-width: 6.3in; margin: 0 auto; letter-spacing: .01em; }}
.seal {{ position: absolute; left: {FX + TRIM_W - SAFE - 1.2}in; top: {H - FRONT_PHOTO_H + 0.1}in; width: 1.2in; height: 1.2in; border-radius: 50%;
  background: radial-gradient(circle at 32% 28%, #FFF1C2 0%, var(--gold) 45%, #B8862E 100%);
  box-shadow: 0 .08in .25in rgba(0,0,0,.45), inset 0 0 0 .05in rgba(255,255,255,.25);
  display: grid; place-items: center; text-align: center; color: #3B2A06; }}
.seal::before {{ content: ""; position: absolute; inset: .09in; border-radius: 50%; border: 1.2px solid rgba(59,42,6,.45); }}
.seal b {{ display: block; font: 400 30pt/.9 "Lilita"; }}
.seal span {{ display: block; font: 800 7pt/1.25 "InterB"; letter-spacing: .16em; text-transform: uppercase; margin-top: .03in; }}
.author {{ position: absolute; left: {FX}in; width: {TRIM_W}in; bottom: {BLEED + SAFE + 0.05}in; text-align: center;
  font: 700 15pt "InterB"; letter-spacing: .38em; text-transform: uppercase; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,.6); }}

/* ---------- spine ---------- */
.spine {{ position: absolute; top: 0; bottom: 0; left: {BLEED + TRIM_W}in; width: {spine}in;
  background: linear-gradient(90deg, #08201A, #0C2A1D 50%, #08201A); display: flex; align-items: center; justify-content: center; }}
.spine .s {{ transform: rotate(90deg); white-space: nowrap; display: flex; align-items: center; gap: .32in; }}
.spine .t {{ font: 400 {spine_pt:.1f}pt "Lilita"; letter-spacing: .05em; color: #fff; }}
.spine .t span {{ color: var(--gold); }}
.spine .a {{ font: 700 {spine_pt * 0.5:.1f}pt "InterB"; letter-spacing: .28em; text-transform: uppercase; color: var(--gold2); }}
.spine .dot {{ width: .07in; height: .07in; border-radius: 50%; background: var(--gold); }}

/* ---------- back ---------- */
.back {{ left: {PAD}in; width: {TRIM_W - 2 * SAFE - 0.2}in; top: {BLEED + SAFE + 0.15}in; }}
.back h3 {{ font: 400 34pt/1.02 "Lilita"; color: var(--gold); letter-spacing: .005em; }}
.back .lead {{ font: italic 400 14.5pt/1.45 "Fraunces"; margin: .17in 0 .2in; color: var(--cream); }}
.back ul {{ list-style: none; font: 400 11.3pt/1.42 "InterB"; color: rgba(255,248,234,.95); }}
.back li {{ padding-left: .32in; position: relative; margin-bottom: .09in; }}
.back li b {{ font-weight: 700; color: #fff; }}
.back li::before {{ content: "★"; position: absolute; left: 0; top: -.01in; font-size: 12.5pt; color: var(--gold); }}
.gift {{ position: absolute; left: {PAD}in; bottom: {BLEED + SAFE + 0.05}in; width: 4.6in; }}
.gift .c {{ font: 700 21pt/1.1 "Caveat"; color: var(--gold); }}
.gift .n {{ margin-top: .1in; font: 700 8.5pt "InterB"; letter-spacing: .3em; text-transform: uppercase; color: rgba(255,248,234,.7); }}
.barcode {{ position: absolute; left: {BLEED + TRIM_W - 0.25 - 2}in; bottom: {BLEED + 0.25}in; width: 2in; height: 1.2in; background: #fff; }}
</style></head><body><div class="wrap">
<div class="snow"></div>

<div class="photo bphoto" style="background-image:url('{back_art}')"></div>
<div class="abs back">
  <h3>Warning: This Book Contains Extreme Levels of Dog.</h3>
  <p class="lead">Why does the Husky argue? Why does the Frenchie act like a tiny CEO? Why does the Golden Retriever love absolutely everyone, including the vacuum?</p>
  <ul>
    <li><b>103 real dog breeds</b> with photo-style portraits, real facts and laugh-out-loud personality profiles</li>
    <li><b>8 hilarious categories,</b> from The Drama Queens to The Dogs Who Think They Own Everything</li>
    <li><b>15 comedy chapters:</b> dog dating profiles, text messages, zombie survival odds and more</li>
    <li><b>Christmas bonus:</b> festive portraits, a holiday quiz, awards and a keepsake page for your own dog</li>
  </ul>
</div>
<div class="gift"><div class="c">The perfect gift for every dog lover (and every weird human).</div><div class="n">{AUTHOR}</div></div>
<div class="barcode"></div>

<div class="spine"><div class="s"><div class="t">DOGS ARE WEIRD. <span>WE LOVE THEM.</span></div><div class="dot"></div><div class="a">{AUTHOR}</div></div></div>

<div class="photo fphoto" style="background-image:url('{hero}')"></div>
<div class="abs front">
  <div class="kicker">{EDITION}</div>
  <div class="title">DOGS ARE<br>WEIRD.</div>
  <div class="love">We Love Them.</div>
  <div class="rule"></div>
  <div class="sub">100+ Hilarious Dog Breeds, Crazy Personalities, Adorable Portraits &amp; Facts That Will Make You Laugh</div>
</div>
<div class="seal"><div><b>103</b><span>Dog<br>Breeds</span></div></div>
<div class="author">{AUTHOR}</div>
</div></body></html>"""
(ROOT / "build" / "cover.html").write_text(html, encoding="utf-8")
spec = {"paper": paper, "pages": pages, "spine_in": spine, "cover_w_in": round(W, 4), "cover_h_in": H}
(ROOT / "build" / "cover-spec.json").write_text(json.dumps(spec, indent=1))
print(spec)
