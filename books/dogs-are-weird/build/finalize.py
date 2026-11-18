#!/usr/bin/env python3
"""Snap PDF page boxes to exact KDP dimensions (Chromium rounds sizes to device pixels)."""
import json, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
ROOT = Path(__file__).resolve().parent.parent
spec = json.loads((ROOT / "build" / "cover-spec.json").read_text())
for name, w, h in [("interior.pdf", 8.625, 11.25), ("cover.pdf", spec["cover_w_in"], spec["cover_h_in"])]:
    f = ROOT / "output" / name
    r = PdfReader(f); wr = PdfWriter()
    for pg in r.pages:
        box = RectangleObject([0, 0, round(w * 72, 3), round(h * 72, 3)])
        pg.mediabox = box; pg.cropbox = box; pg.trimbox = box; pg.bleedbox = box
        wr.add_page(pg)
    wr.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    with open(f, "wb") as o: wr.write(o)
    print(name, len(r.pages), "pages", w, "x", h, "in", round(f.stat().st_size / 1e6, 1), "MB")
