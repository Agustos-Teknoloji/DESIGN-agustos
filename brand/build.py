#!/usr/bin/env python3
"""
Ağustos brand kit — asset generator (the engine).

Reads the keystone registry (brands.json) and the shared symbol
(laz-gunesi-amblem/svg/master.svg) and emits per-brand, ready-to-hand-off assets:

  exports/<brand>/lockup/   symbol + wordmark, 3 expressions x {svg, pdf, png}
  exports/<brand>/favicon/  favicon.ico/.svg, apple-touch-icon, manifest png, site.webmanifest
  exports/<brand>/social/   square avatar (400/1000) + 1200x630 og image

Design choices (see DESIGN.md):
  - The wordmark is baked to vector OUTLINES via fontTools, so every asset is
    self-contained and renders identically with NO font installed.
  - SVG is the master format. PDF is produced with reportlab (pure Python),
    PNG with the node resvg helper (prebuilt binary, no system Cairo needed).
  - Lockup geometry follows the spec: symbol height = 1.4x wordmark cap height,
    symbol-to-wordmark gap = 0.4x wordmark size, Inter Tight Light, lowercase,
    optical (not geometric) vertical centering for lowercase wordmarks.

Usage:
  ../.venv/bin/python build.py                  # every brand in the registry
  ../.venv/bin/python build.py --brand agustos  # a single brand
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PIL import Image

BRAND_DIR = Path(__file__).resolve().parent
ROOT = BRAND_DIR.parent
FONT_PATH = BRAND_DIR / "fonts" / "inter-tight" / "InterTight[wght].ttf"
RENDER_JS = BRAND_DIR / "scripts" / "render_png.mjs"
REGISTRY = BRAND_DIR / "brands.json"

# Output PNG widths
LOCKUP_PNG_W = 2400          # retina master
LOCKUP_PNG_W_SMALL = 800     # web-friendly
FAVICON_SIZES = [16, 32, 48, 64, 180, 192, 256, 512]
AVATAR_SIZES = [1000, 400]
OG_W, OG_H = 1200, 630


# ----------------------------------------------------------------------------
# Symbol (shared Laz Güneşi) — parsed once
# ----------------------------------------------------------------------------

def load_symbol():
    svg = (ROOT / "laz-gunesi-amblem" / "svg" / "master.svg").read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([\-\d.\s]+)"', svg).group(1).split()
    minx, miny, w, h = map(float, vb)
    paths = re.findall(r'<path[^>]*\bd="([^"]+)"', svg)
    return paths, (minx, miny, w, h)


SYMBOL_PATHS, SYMBOL_VB = load_symbol()


def symbol_group(color, cx, cy, side):
    """Symbol scaled to `side` (height), centered on (cx, cy). The master is
    centered on (0,0), so we just scale then translate the center into place."""
    _, _, w, _h = SYMBOL_VB
    scale = side / w
    body = "".join(f'<path d="{d}"/>' for d in SYMBOL_PATHS)
    return (f'<g fill="{color}" fill-rule="evenodd" '
            f'transform="translate({cx:.3f},{cy:.3f}) scale({scale:.6f})">{body}</g>')


# ----------------------------------------------------------------------------
# Wordmark — baked to outlines
# ----------------------------------------------------------------------------

def load_display_font(weight):
    inst = instantiateVariableFont(TTFont(FONT_PATH), {"wght": weight}, inplace=False)
    upem = inst["head"].unitsPerEm
    os2 = inst["OS/2"]
    cap = getattr(os2, "sCapHeight", None) or int(upem * 0.727)
    xh = getattr(os2, "sxHeight", None) or int(upem * 0.536)
    return {
        "glyphs": inst.getGlyphSet(),
        "cmap": inst.getBestCmap(),
        "hmtx": inst["hmtx"],
        "upem": upem,
        "cap": cap,
        "xh": xh,
    }


def wordmark_group(text, color, x0, baseline, font, sc, tracking_px):
    """Place each glyph as an outlined <path>. scale(sc, -sc) maps font units
    (y-up) into SVG space (y-down) with the baseline at `baseline`."""
    glyphs, cmap, hmtx = font["glyphs"], font["cmap"], font["hmtx"]
    parts = []
    penx = x0
    n = len(text)
    for i, ch in enumerate(text):
        gname = cmap[ord(ch)]
        pen = SVGPathPen(glyphs)
        glyphs[gname].draw(pen)
        d = pen.getCommands()
        if d:  # spaces have no contour
            parts.append(
                f'<path d="{d}" transform="translate({penx:.3f},{baseline:.3f}) '
                f'scale({sc:.6f},{-sc:.6f})"/>'
            )
        penx += hmtx[gname][0] * sc
        if i < n - 1:
            penx += tracking_px
    return f'<g fill="{color}">{"".join(parts)}</g>', penx


# ----------------------------------------------------------------------------
# Composed assets
# ----------------------------------------------------------------------------

def build_lockup(text, mark_color, font, tracking_em, bg_color=None, fs=200.0):
    """Returns (svg, W, H, inner) for one lockup expression. `inner` is the
    translate-wrapped content group, reused (unscaled) by the OG composer."""
    sc = fs / font["upem"]
    cap_px = font["cap"] * sc
    xh_px = font["xh"] * sc
    tracking_px = tracking_em * fs

    # Symbol box = wordmark font size (matches the live site: a 24px wordmark
    # carries a 24px symbol box). Equivalent to the component's size*1.4*0.7.
    side = 1.4 * 0.7 * fs
    gap = 0.4 * fs                   # symbol-to-wordmark gap = 0.4x wordmark size
    baseline = side * 1.2            # provisional; whole thing is re-origined below
    sym_cx = side / 2.0
    # Lowercase optical centering: center the symbol on the x-height band, not the
    # cap box. Centering on cap height makes the symbol read as floating high above
    # all-lowercase wordmarks (see DESIGN.md lockup notes).
    sym_cy = baseline - xh_px * 0.5

    sym = symbol_group(mark_color, sym_cx, sym_cy, side)
    wm, right = wordmark_group(text, mark_color, side + gap, baseline, font, sc, tracking_px)

    # Tight bounding box across symbol + wordmark.
    sym_top, sym_bot = sym_cy - side / 2, sym_cy + side / 2
    cap_top = baseline - cap_px * 1.04   # headroom for ascenders / the ğ breve
    top = min(sym_top, cap_top)
    bot = max(sym_bot, baseline)
    margin = 0.06 * fs
    ox, oy = margin, margin - top
    W = (right - 0.0) + 2 * margin
    H = (bot - top) + 2 * margin

    inner = f'<g transform="translate({ox:.3f},{oy:.3f})">{sym}{wm}</g>'
    bg = (f'<rect x="0" y="0" width="{W:.3f}" height="{H:.3f}" fill="{bg_color}"/>'
          if bg_color else "")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.3f} {H:.3f}" '
           f'width="{W:.1f}" height="{H:.1f}" role="img" aria-label="{text} lockup">'
           f'{bg}{inner}</svg>')
    return svg, W, H, inner


def build_monogram(mark_color, tile_color, size=512.0, radius_ratio=0.0, symbol_ratio=0.62):
    """Square tile: symbol in `mark_color` on a `tile_color` field. Full-bleed by
    default (radius_ratio=0) so platforms that crop avatars to circles stay clean."""
    rx = size * radius_ratio
    bg = f'<rect x="0" y="0" width="{size}" height="{size}" rx="{rx:.2f}" fill="{tile_color}"/>'
    sym = symbol_group(mark_color, size / 2, size / 2, size * symbol_ratio)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'width="{size}" height="{size}" role="img">{bg}{sym}</svg>')


def build_og(inner, W, H, paper, og_w=OG_W, og_h=OG_H, target_ratio=0.54):
    scale = (og_w * target_ratio) / W
    max_h = og_h * 0.5
    if H * scale > max_h:
        scale = max_h / H
    tx = (og_w - W * scale) / 2
    ty = (og_h - H * scale) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {og_w} {og_h}" '
            f'width="{og_w}" height="{og_h}" role="img">'
            f'<rect x="0" y="0" width="{og_w}" height="{og_h}" fill="{paper}"/>'
            f'<g transform="translate({tx:.2f},{ty:.2f}) scale({scale:.5f})">{inner}</g></svg>')


# ----------------------------------------------------------------------------
# Output helpers
# ----------------------------------------------------------------------------

def write_svg(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def svg_to_pdf(svg_path: Path, pdf_path: Path):
    renderPDF.drawToFile(svg2rlg(str(svg_path)), str(pdf_path))


def render_pngs(jobs):
    """jobs: list of (svg_path, out_path, width). Rendered in one node process."""
    if not jobs:
        return
    payload = [{"svg": str(s), "out": str(o), "width": int(w)} for s, o, w in jobs]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        jobs_file = f.name
    subprocess.run(["node", str(RENDER_JS), jobs_file], check=True, cwd=str(BRAND_DIR))


def write_ico(src_png: Path, ico_path: Path):
    img = Image.open(src_png).convert("RGBA")
    img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])


# ----------------------------------------------------------------------------
# Per-brand build
# ----------------------------------------------------------------------------

def build_brand(slug, brand, reg):
    text = brand["wordmark"]
    color = brand["color"]
    paper = reg["substrate"]["paper"]
    ink = reg["substrate"]["ink"]
    tracking_em = reg["type"]["wordmark_tracking_em"]
    weight = reg["type"]["wordmark_weight"]
    font = load_display_font(weight)

    base = BRAND_DIR / "exports" / slug
    lk, fv, so = base / "lockup", base / "favicon", base / "social"
    png_jobs = []

    # --- Lockups: positive / negative / mono ---
    expressions = {
        "positive": dict(mark=color, bg=None),    # brand color on transparent (primary)
        "negative": dict(mark=paper, bg=color),   # cream marks on brand field
        "mono":     dict(mark=ink,   bg=None),    # single-color print
    }
    positive_inner = positive_wh = None
    for name, e in expressions.items():
        svg, W, H, inner = build_lockup(text, e["mark"], font, tracking_em, bg_color=e["bg"])
        svg_path = write_svg(lk / f"{slug}-lockup__{name}.svg", svg)
        svg_to_pdf(svg_path, lk / f"{slug}-lockup__{name}.pdf")
        png_jobs.append((svg_path, lk / f"{slug}-lockup__{name}.png", LOCKUP_PNG_W))
        png_jobs.append((svg_path, lk / f"{slug}-lockup__{name}@{LOCKUP_PNG_W_SMALL}.png",
                         LOCKUP_PNG_W_SMALL))
        if name == "positive":
            positive_inner, positive_wh = inner, (W, H)

    # --- Favicons + app icons (negative monogram: cream symbol on brand tile) ---
    fav_svg = write_svg(fv / "favicon.svg", build_monogram(paper, color))
    for s in FAVICON_SIZES:
        png_jobs.append((fav_svg, fv / f"favicon-{s}.png", s))

    # --- Social: avatar (same monogram) + OG image ---
    av_svg = write_svg(so / f"{slug}-avatar.svg", build_monogram(paper, color))
    for s in AVATAR_SIZES:
        png_jobs.append((av_svg, so / f"{slug}-avatar-{s}.png", s))
    og_svg = write_svg(so / f"{slug}-og.svg",
                       build_og(positive_inner, *positive_wh, paper))
    png_jobs.append((og_svg, so / f"{slug}-og.png", OG_W))

    # Rasterize everything in one node call.
    render_pngs(png_jobs)

    # --- Post-raster: .ico, named apple-touch icon, web manifest ---
    write_ico(fv / "favicon-256.png", fv / "favicon.ico")
    Image.open(fv / "favicon-180.png").save(fv / "apple-touch-icon.png")
    manifest = {
        "name": brand.get("title", slug),
        "short_name": text,
        "icons": [
            {"src": "favicon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "favicon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": color,
        "background_color": paper,
        "display": "standalone",
    }
    (fv / "site.webmanifest").write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                                         encoding="utf-8")

    n_files = sum(1 for _ in base.rglob("*") if _.is_file())
    print(f"  ✓ {slug}: {n_files} files -> {base.relative_to(ROOT)}")


def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", help="build a single brand slug (default: all)")
    args = ap.parse_args()

    brands = reg["brands"]
    targets = {args.brand: brands[args.brand]} if args.brand else brands
    if args.brand and args.brand not in brands:
        raise SystemExit(f"unknown brand '{args.brand}'. known: {', '.join(brands)}")

    print(f"Building {len(targets)} brand(s)...")
    for slug, brand in targets.items():
        build_brand(slug, brand, reg)
    print("Done.")


if __name__ == "__main__":
    main()
