#!/usr/bin/env python3
"""Writes every illustration in the book as SVG into art/svg/ (render with render_svgs.js)."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
import dogs
from content import breeds_1, breeds_2, breeds_3, breeds_4, extras as X

OUT = HERE / "svg"; OUT.mkdir(exist_ok=True)
GROUPS = [("drama", breeds_1.DRAMA), ("tiny", breeds_1.TINY), ("fluffy", breeds_2.FLUFFY), ("couch", breeds_2.COUCH),
          ("athletic", breeds_3.ATHLETIC), ("giants", breeds_3.GIANTS), ("weird", breeds_4.WEIRD), ("owners", breeds_4.OWNERS)]
W = lambda name, svg: (OUT / f"{name}.svg").write_text(svg)

n = 0
for key, lst in GROUPS:
    for b in lst:
        n += 1
        assert b.name in dogs.SPECS, b.name
        W(f"IMG-{n:03d}", dogs.portrait_svg(b.name, n))

CAT_SCENE = {"drama": "spotlight", "tiny": "office", "fluffy": "snow", "couch": "couch", "athletic": "park", "giants": "alps", "weird": "studio", "owners": "palace"}
CAT_PICK = {
    "drama": ["Pug", "Siberian Husky", "Afghan Hound", "Basset Hound", "Shih Tzu"],
    "tiny": ["Chihuahua", "Yorkshire Terrier", "French Bulldog", "Dachshund", "Boston Terrier"],
    "fluffy": ["Pomeranian", "Samoyed", "Chow Chow", "Keeshond", "Old English Sheepdog"],
    "couch": ["Greyhound", "Bulldog", "Chinese Shar-Pei", "Bullmastiff", "Japanese Chin"],
    "athletic": ["Border Collie", "Golden Retriever", "German Shepherd", "Dalmatian", "Australian Shepherd"],
    "giants": ["Newfoundland", "Great Dane", "Bernese Mountain Dog", "Saint Bernard", "Irish Wolfhound"],
    "weird": ["Puli", "Chinese Crested", "Bull Terrier", "Bedlington Terrier", "Basenji"],
    "owners": ["Shiba Inu", "Rottweiler", "Pembroke Welsh Corgi", "Akita", "Beagle"],
}
for i, (key, names) in enumerate(CAT_PICK.items()):
    W(f"CAT-{key}", dogs.group_svg(names, 1690, 1000, CAT_SCENE[key], 500 + i, rows=2))

XACC = {"Golden Retriever": ["lights", "santa"], "French Bulldog": ["santa"], "Pembroke Welsh Corgi": ["antlers"],
        "Siberian Husky": ["scarf", "santa"], "Pug": ["candycane"], "Dachshund": ["scarf", "santa"],
        "Bernese Mountain Dog": ["santa", "lights"], "Chihuahua": ["sweater", "santa"]}
XEXP = {"Golden Retriever": "clueless", "French Bulldog": "grumpy", "Pembroke Welsh Corgi": "smug", "Siberian Husky": "howl",
        "Pug": "shocked", "Dachshund": "proud", "Bernese Mountain Dog": "joy", "Chihuahua": "shocked"}
for i, name, desc, cap in X.CHRISTMAS_PORTRAITS:
    W(f"XMAS-{i}", dogs.portrait_svg(name, 700 + int(i[1:]), scene="xmas", acc=XACC[name], expr=XEXP[name]))

hero = ["Golden Retriever", "Pembroke Welsh Corgi", "French Bulldog", "Siberian Husky"]
W("XMAS-hero", dogs.group_svg(hero, 1690, 1000, "xmas", 801, rows=2, accs={k: XACC[k] for k in hero}, exprs={k: XEXP[k] for k in hero}))

trophy = ('<g transform="translate(1500,560)"><path d="M-90 0 H90 Q90 150 0 170 Q-90 150 -90 0Z" fill="#F2C230" stroke="#2B1E16" stroke-width="7"/>'
          '<path d="M-90 30 q-60 0 -50 60 q10 40 50 40 M90 30 q60 0 50 60 q-10 40 -50 40" stroke="#2B1E16" stroke-width="7" fill="none"/>'
          '<rect x="-25" y="170" width="50" height="80" fill="#C99A1A" stroke="#2B1E16" stroke-width="7"/><rect x="-90" y="250" width="180" height="50" rx="8" fill="#5B3A22" stroke="#2B1E16" stroke-width="7"/>'
          '<text x="0" y="100" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="64" fill="#9C7A12">#1</text></g>')
W("XMAS-awards", dogs.group_svg(["Pembroke Welsh Corgi", "Chihuahua", "Beagle"], 1900, 1000, "redcarpet", 802,
                                accs={"Pembroke Welsh Corgi": ["antlers", "medal"], "Chihuahua": ["sweater"], "Beagle": ["santa"]},
                                exprs={"Pembroke Welsh Corgi": "smug", "Chihuahua": "joy", "Beagle": "shocked"}).replace("</svg>", trophy + "</svg>"))

swirl = "".join(f'<path d="M{x} 300 a 90 40 0 1 1 1 0" stroke="#fff" stroke-width="10" fill="none" stroke-opacity=".7" stroke-linecap="round"/>' for x in (300, 1560))
zz = '<text x="1560" y="250" font-family="sans-serif" font-weight="900" font-size="110" fill="#fff" fill-opacity=".8">Z z z</text>'
W("ART-habits", dogs.group_svg(["Labrador Retriever", "Bulldog", "Beagle"], 1900, 1000, "cozy", 803,
                               accs={"Labrador Retriever": ["tennis"], "Bulldog": ["blanket"], "Beagle": []},
                               exprs={"Labrador Retriever": "clueless", "Bulldog": "sleepy", "Beagle": "sideeye"}).replace("</svg>", swirl[:0] + zz + "</svg>"))
heart = '<path transform="translate(950,190) scale(4)" d="M0 10 C -25 -12 -12 -32 0 -16 C 12 -32 25 -12 0 10Z" fill="#E84A5F" stroke="#2B1E16" stroke-width="2"/>'
W("ART-dating", dogs.group_svg(["Great Dane", "Chihuahua"], 1900, 1000, "candle", 804,
                               accs={"Great Dane": ["bowtie"], "Chihuahua": ["flower", "pearls"]},
                               exprs={"Great Dane": "cute", "Chihuahua": "joy"}).replace("</svg>", heart + "</svg>"))

cover6 = ["Siberian Husky", "Pembroke Welsh Corgi", "French Bulldog", "Golden Retriever", "Pug", "Dachshund"]
W("COVER-front", dogs.group_svg(cover6, 1400, 1000, "xmas", 900, rows=2, spread=540,
                                accs={"Siberian Husky": ["scarf"], "Pembroke Welsh Corgi": ["crown"], "French Bulldog": ["tie", "santa"],
                                      "Golden Retriever": ["santa", "lights"], "Pug": ["candycane"], "Dachshund": ["lights"]},
                                exprs={"Siberian Husky": "dramatic", "Pembroke Welsh Corgi": "smug", "French Bulldog": "grumpy",
                                       "Golden Retriever": "clueless", "Pug": "shocked", "Dachshund": "proud"}))
gifts = "".join(f'<g transform="translate({x},{y})"><rect x="-80" y="-70" width="160" height="140" fill="{c}" stroke="#2B1E16" stroke-width="7"/>'
                f'<rect x="-14" y="-70" width="28" height="140" fill="#F2C230"/><rect x="-80" y="-12" width="160" height="24" fill="#F2C230"/></g>'
                for x, y, c in [(330, 900, "#D62E2E"), (1430, 900, "#2E86B5"), (1560, 820, "#5FB37A")])
W("COVER-back", dogs.group_svg(["Pug"], 1760, 1000, "xmas", 901, accs={"Pug": ["santa"]}, exprs={"Pug": "shocked"}).replace("</svg>", gifts + "</svg>"))
print("svgs:", len(list(OUT.glob("*.svg"))))
