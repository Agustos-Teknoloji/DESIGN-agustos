# Laz Güneşi Amblemi: Brand Asset Kit

Clean, parametrically-rebuilt vector master and full asset kit derived from the original Adobe Illustrator file (`source/laz-gunesi-amblem__original.ai`).

## What's in this kit

```
svg/  ; Editable vector masters (use these as the source of truth)
pdf/  ; Print-ready vector PDFs
png/  ; Pre-rendered transparent PNGs at 256 / 512 / 1024 / 2048 / 4096 px
css/  ; Self-contained CSS (SVG embedded as data URI) + live demo page
source/— Original .ai and .pdf files (do not edit; reference only)
docs/ ; Geometry data and rebuild verification
```

## The mark

- **18 blades**, rotated 20° apart around a common center
- **Brand red:** `#cf142a` (RGB 207, 20, 42)
- Square viewBox, mark perfectly centered on (0, 0) with ~10% safe padding
- Even-odd fill rule, no strokes, scales cleanly to any size

## Color variants

| File | Use for |
|---|---|
| `laz-gunesi__red.svg` | **Primary mark.** Use anywhere with a light or neutral background |
| `laz-gunesi__white.svg` | Reverse mark. Use on dark or photographic backgrounds |
| `laz-gunesi__black.svg` | Mono. For single-color print, faxes, embossing, engraving |
| `laz-gunesi__red-on-white.svg` | Locked-up red on white. Use when you need a guaranteed white background |
| `laz-gunesi__white-on-black.svg` | Reverse lockup |
| `laz-gunesi__red-on-black.svg` | Decorative lockup for dark themes |

## Picking the right file

- **Web / app UI:** `svg/laz-gunesi__red.svg` (or white for dark mode)
- **Slides, docs, social posts:** `png/laz-gunesi__red_1024px.png`
- **Avatars / favicons:** `png/laz-gunesi__red_256px.png` or `512px.png`
- **Print, signage, business cards:** `pdf/laz-gunesi__red.pdf`
- **Embroidery, vinyl cutting, laser, CNC:** `svg/laz-gunesi__black.svg` (single closed shape, no overlaps)

## Using it in HTML/CSS

```html
<link rel="stylesheet" href="css/laz-sun.css">

<span class="laz-sun laz-sun--md"></span>                <!-- 40px brand red -->
<span class="laz-sun laz-sun--xl laz-sun--white"></span> <!-- 128px white on dark bg -->
<span class="laz-sun laz-sun--lg laz-sun--spin"></span>  <!-- 64px, spinning -->
<span class="laz-sun" style="--laz-size: 200px; --laz-color: #5B2C6F"></span>
```

The CSS file is fully self-contained, the SVG is embedded as a data URI, so no extra HTTP requests. ~13 KB total.

Two flavors are included:

- `.laz-sun` uses `mask-image`, so the color follows `--laz-color` (default brand red). Use this for white-on-dark, hover effects, or any non-red palette.
- `.laz-sun--bg` uses `background-image` with the red baked in. Slightly broader browser coverage; use when you don't need to recolor.

Open `css/demo.html` in a browser to see every variant side by side.

## Rebuild quality

The rebuild matches the original to **0.08% pixel difference** at matched scale, see `docs/rebuild-vs-original.png`. The diff is sub-pixel anti-aliasing noise plus the removal of two duplicate paths that existed in the original Illustrator export.

The rebuilt vectors are **~250× smaller than the original PDF** (2 KB vs 535 KB) for the same visual fidelity.

## Geometry data

`docs/master_geometry.json` contains the full parametric definition:
- `blade_count`: 18
- `blade_spacing_deg`: 20.0
- `art_radius_pts`: 52.65
- `blades[]`: each blade's angle from center and centered SVG path data

Use this if you ever need to:
- Regenerate the symbol at a different blade count
- Export to formats not in this kit (DXF, EPS, embroidery, CSV of curve coordinates)
- Animate the blades individually
