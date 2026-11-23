# Dogs Are Weird. We Love Them. (Christmas Gift Edition 2027)

A 150-page, full-color, 8.5 x 11 in paperback gift book for Amazon KDP, with 103 dog breeds, 14 comedy chapters and a Christmas section.

## What's here

| Path | What it is |
|---|---|
| `output/interior.pdf` | Print-ready interior: 150 pages, 8.625 x 11.25 in with bleed, fonts embedded |
| `output/cover.pdf` | Full-wrap cover (back, spine, front), 17.6021 x 11.25 in, premium color spine |
| `output/preview-cover.png` | Quick look at the cover |
| `content/breeds_*.py` | All 103 breed profiles: 15 fields each, plus art direction |
| `content/extras.py` | Humor chapters, quizzes, Christmas pages, dedication, welcome and closing text |
| `image-prompts.md` / `.csv` | 125 illustration prompts with file IDs, sizes and a negative prompt |
| `KDP-LISTING.md` | KDP settings, description, keywords, categories, pricing and launch checklist |
| `build/` | Layout engine (HTML/CSS rendered by Chromium) and open-license fonts (OFL) |

## Status

- **Text and layout: complete.** No page overflows.
- **Illustrations: complete (125 of 125), in cartoon style.** The art is drawn in code by `art/dogs.py`. It gives each breed its own portrait, with breed coat colors and markings, ears, fur type, a funny expression and an accessory. It also draws the 8 chapter group scenes, 8 Christmas portraits, 4 feature scenes and the front and back cover art. The images are 1600 px JPEGs, over 300 dpi at print size.
- **Upgrading to photo-realistic art:** generate images with the prompts in `image-prompts.md` and save them into `images/` with the same file names (for example `IMG-001.jpg`). Then rebuild.

## Rebuild

```bash
cd books/dogs-are-weird
python3 art/make_art.py && node art/render_svgs.js   # redraw the cartoon art (optional)
python3 build/build.py          # interior HTML + manifest
python3 build/build_cover.py    # cover HTML; pass standard_color for that paper
python3 build/prompts.py        # refresh prompt pack (optional)
node build/render.js all        # PDFs through Playwright/Chromium
python3 build/finalize.py       # snap PDF boxes to exact KDP sizes
```

The auto-fit step scales the text on each page to fill its frame, so you can edit the copy freely. `render.js` reports any page that still overflows.

## Book map

1–8 front matter (title, copyright, Christmas 2027 opening, dedication, gift message, contents, welcome, how to read) ·
9–137 eight breed categories, each with an opener page and followed by its humor chapters ·
138–146 Christmas section · 147–148 breed index · 149 closing page · 150 blank
