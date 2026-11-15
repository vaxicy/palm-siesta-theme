#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Palm Siesta Theme — flat vector logo candidates (SVG, headless Chromium).

Style: **flat** — solid fills only, no gradients, no highlights, no outlines.
Two or three shapes per mark.

The palette is five light pastels, so the mark needs a dark anchor: deep clay
`#4B322A` carries the frame of every composition and the pastels only fill it.
That way the icon reads on the butter page, on the sand toolbar and in the store.

Playwright screenshots each SVG cell with omit_background=True (true
transparency); PIL only composes the contact sheets, the inline strip and the
official logo/logo.png exported from SELECTED.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512
PREVIEW = 256
SELECTED = "01"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(vals):
    return "#%02X%02X%02X" % tuple(vals)


ROSE = hx(_C["frame"])                             # #ECABB2
SAND = hx(_C["toolbar"])                           # #EDD4B9
BUTTER = hx(_C["ntp_background"])                  # #FBEDBF
MARIGOLD = hx(_C["button_background_secondary"])   # #F9DA81
MINT = hx(_C["button_background"])                 # #A9E6DD
INK = hx(_C["ntp_text"])                           # #4B322B
LINK = hx(_C["ntp_link"])                          # #A34A52


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s<g transform="translate(128 128) scale(0.94) '
            'translate(-128 -128)">%s</g></svg>' % (CELL, CELL, defs, body))


def circle(cx, cy, r, fill):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, fill)


def arch(x0, x1, top, bottom, fill):
    """A rounded-top window: straight sides, semicircular head."""
    r = (x1 - x0) / 2.0
    return ('<path d="M%.1f %.1f V%.1f a%.1f %.1f 0 0 1 %.1f 0 V%.1f Z" fill="%s"/>'
            % (x0, bottom, top + r, r, r, x1 - x0, bottom, fill))


def palm(cx, cy, size, angle, fill, blades=5, spread=76):
    """A palm crown: long tapered blades fanning out of one point."""
    out = ['<g transform="translate(%.1f %.1f) rotate(%.1f)">' % (cx, cy, angle)]
    for i in range(blades):
        a = -spread / 2 + spread * i / max(1, blades - 1)
        out.append('<g transform="rotate(%.1f)">' % a)
        out.append('<path d="M0 0 Q%.1f %.1f %.1f 0 Q%.1f %.1f 0 0 Z" fill="%s"/>'
                   % (size * 0.52, size * 0.30, size,
                      size * 0.52, -size * 0.30, fill))
        out.append("</g>")
    out.append('<circle cx="0" cy="0" r="%.1f" fill="%s"/>' % (size * 0.09, fill))
    out.append("</g>")
    return "".join(out)


def wave(y, amp, fill, x0=32, x1=224, bottom=224):
    span = (x1 - x0) / 3.0
    return ('<path d="M%.1f %.1f q%.1f -%.1f %.1f 0 q%.1f %.1f %.1f 0 q%.1f -%.1f %.1f 0 '
            'V%d H%.1f Z" fill="%s"/>'
            % (x0, y, span / 2, amp, span, span / 2, amp, span, span / 2, amp, span,
               bottom, x0, fill))


# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
%s
%s
%s
""" % (circle(128, 128, 96, INK),
       arch(84, 172, 76, 208, ROSE),
       circle(128, 132, 26, MARIGOLD)))

SVG_02 = svg_open("""
%s
%s
%s
""" % (arch(52, 204, 56, 212, INK),
       arch(80, 176, 92, 196, BUTTER),
       circle(128, 140, 24, MARIGOLD)))

SVG_03 = svg_open("""
%s
%s
%s
""" % (circle(128, 128, 96, INK),
       circle(128, 120, 46, MARIGOLD),
       palm(78, 196, 92, -26, MINT)))

SVG_04 = svg_open("""
<defs><clipPath id="c4"><circle cx="128" cy="128" r="96"/></clipPath></defs>
%s
<g clip-path="url(#c4)">
  %s
  %s
</g>
""" % (circle(128, 128, 96, BUTTER),
       wave(116, 22, ROSE),
       wave(152, 18, MARIGOLD)))

SVG_05 = svg_open("""
%s
%s
%s
%s
""" % (circle(128, 128, 96, INK),
       arch(70, 138, 84, 200, ROSE),
       arch(126, 186, 116, 200, MARIGOLD),
       circle(160, 96, 18, MINT)))

SVG_06 = svg_open("""
%s
%s
%s
""" % (circle(128, 128, 96, MARIGOLD),
       palm(76, 190, 104, -30, INK),
       circle(150, 104, 32, INK)))

CANDIDATES = [
    ("01", "arch-disc", "Clay disc with a rose arch and a marigold sun", SVG_01),
    ("02", "arch-only", "Clay arch outline with a butter window and sun", SVG_02),
    ("03", "palm-sun", "Clay disc, marigold sun, mint palm frond", SVG_03),
    ("04", "dune-bands", "Three dune layers on butter — most graphic", SVG_04),
    ("05", "twin-arch", "Two arches in clay disc — most architectural", SVG_05),
    ("06", "palm-sun-dark", "Marigold disc with a clay frond and sun", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join('<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
                    for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception:
            # bundled headless shell may be missing after a Playwright update
            b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA").resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 6 and bbox[1] > 6 and bbox[2] < PREVIEW - 6 and bbox[3] < PREVIEW - 6, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), BUTTER)
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=INK)
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, (251, 237, 191), (75, 50, 43), (150, 116, 92),
                  CAND_DIR / "contact-light.png", "Palm Siesta — flat candidates (butter page)")
    contact_sheet(rendered, (236, 171, 178), (75, 50, 43), (120, 74, 62),
                  CAND_DIR / "contact-dark.png", "Palm Siesta — candidates on the rose frame")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
