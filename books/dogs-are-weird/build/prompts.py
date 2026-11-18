#!/usr/bin/env python3
"""Generates image-prompts.md and image-prompts.csv: one prompt per illustration slot."""
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import build as B  # noqa: E402  (builds HTML as a side effect; harmless)
X = B.X

STYLE = ("premium photorealistic 3D render, professional pet-photography aesthetic, ultra-detailed realistic fur, "
         "expressive glossy eyes with catchlights, anatomically correct {breed} with accurate breed coat colors and proportions, "
         "soft cinematic studio lighting with warm key light and rim light, shallow depth of field, high-end editorial gift-book quality, "
         "funny and adorable expression, 8.5x11 print, 300 dpi, no text, no watermark")
NEG = ("text, letters, watermark, logo, extra legs, extra paws, fused toes, missing tail when breed has one, deformed eyes, "
       "cross-eyed, blurry, low resolution, plastic look, cartoon, human hands, duplicate dog, wrong breed markings")
rows = []
for b in B.ALL:
    rows.append((b.img_id, f"Breed portrait p.{B.index_pages[b.name]}", b.name, "1:1 square, 3000x3000 px",
                 f"Portrait of a {b.name}. {b.portrait}. " + STYLE.format(breed=b.name)))
for c in X.CATEGORIES:
    names = ", ".join(x.name for x in dict(B.GROUPS)[c[0]][:6])
    rows.append((f"CAT-{c[0]}", f"Chapter opener: {c[1]}", names, "16:10 landscape, 4200x2600 px",
                  f"Group portrait for a chapter called '{c[1]}' ({c[2]}): {names} posing together like a movie poster, each with a personality-matched comic expression, backdrop color {c[4]}. " + STYLE.format(breed="dogs")))
for i, n, d, cap in X.CHRISTMAS_PORTRAITS:
    rows.append((f"XMAS-{i}", "Christmas portrait gallery", n, "3:4 portrait, 2400x3200 px",
                 f"Christmas portrait of a {n}: {d} Cozy winter scene, subtle snow, warm golden fairy lights, tasteful festive accessories. " + STYLE.format(breed=n)))
extra = [
    ("XMAS-hero", "Christmas chapter opener", "Golden Retriever, Corgi, French Bulldog, Husky", "16:10 landscape, 4200x2600 px", "A cozy living room on Christmas Eve: a Golden Retriever, Pembroke Welsh Corgi, French Bulldog and Siberian Husky in Santa hats around a glowing tree, snow falling outside the window, warm golden light."),
    ("XMAS-awards", "Festive Dog Awards page", "Pembroke Welsh Corgi", "16:9 landscape, 4200x2360 px", "A Corgi in a reindeer costume proudly accepting a tiny golden trophy on a small stage with red velvet curtains and twinkling lights."),
    ("ART-habits", "Daily Habits chapter", "Labrador Retriever", "16:9 landscape, 4200x2360 px", "A yellow Labrador spinning in circles on a round dog bed, playful motion blur on the tail, cozy living room."),
    ("ART-dating", "Dating Profile chapter", "Great Dane, Chihuahua", "16:9 landscape, 4200x2360 px", "A Great Dane and a tiny Chihuahua on a candlelit dinner date at a bistro table, sharing one spaghetti noodle, romantic warm bokeh."),
    ("COVER-front", "Front cover hero (most important image)", "Golden Retriever, French Bulldog, Corgi, Husky, Pug, Dachshund", "4:3 landscape, 4800x3600 px; keep faces in center 80%", "Six dogs in a lineup on a snowy cozy set: Golden Retriever looking extremely happy and slightly clueless in a Santa hat, French Bulldog as an angry little CEO in a tiny tie, Corgi wearing a small gold crown with enormous confidence, Husky dramatically staring into the distance with a scarf, Pug looking shocked holding a candy cane, Dachshund wrapped in Christmas lights. Deep green background with subtle snow, warm golden light."),
    ("COVER-back", "Back cover", "Pug", "16:9 landscape, 4200x2600 px", "A Pug in a Santa hat looking shocked at a pile of unwrapped gifts and torn wrapping paper, deep green background, warm light."),
]
for r in extra:
    rows.append(r[:4] + (r[4] + " " + STYLE.format(breed="dogs"),))

with open(ROOT / "image-prompts.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["file_id", "used_on", "subject", "aspect_and_size", "prompt", "negative_prompt"])
    for r in rows: w.writerow(list(r) + [NEG])
md = ["# Illustration Prompt Pack: Dogs Are Weird. We Love Them.", "",
      f"**{len(rows)} illustrations, all pending.** No image generator was reachable when this book was built, so every slot in the PDF prints a labeled placeholder (`IMG-001` and so on).",
      "", "## How to finish the art", "",
      "1. Generate each image with the prompt below (Midjourney v7, Flux 1.1 Pro, Imagen 4, GPT-Image or similar). Add the negative prompt where the tool supports one.",
      "2. Check every image for correct breed markings, four legs, natural paws and eyes. Regenerate anything that is anatomically wrong or blurry.",
      "3. Save as `images/<file_id>.jpg` (or .png/.webp) at the listed size or larger. Use RGB at 300 dpi for the final print size.",
      "4. Rebuild: `python3 build/build.py && python3 build/build_cover.py && node build/render.js all && python3 build/finalize.py`. Placeholders are replaced automatically.",
      "5. Confirm you hold commercial rights to every image under your generator's terms. KDP requires you to disclose AI-generated images when you publish.",
      "", f"**Negative prompt (all images):** {NEG}", ""]
for r in rows:
    md += [f"### {r[0]} | {r[2]}", f"*{r[1]} · {r[3]}*", "", "```", r[4], "```", ""]
(ROOT / "image-prompts.md").write_text("\n".join(md))
print(len(rows), "prompts")
