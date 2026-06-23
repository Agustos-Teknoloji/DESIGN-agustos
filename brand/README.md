# Ağustos Brand Kit

Ready-to-hand-off brand assets for Ağustos and its sub-brands, generated from a
single source of truth. This folder is the brand-asset manager's home base.

## The one rule

**Edit the sources. Never hand-edit `exports/`.**

Everything under `exports/` is generated. If you touch it by hand, the next build
overwrites your change and the brand drifts. To change anything, edit a source and
re-run the build:

| To change… | Edit this | Then run |
|---|---|---|
| a wordmark, color, tagline, domain | `brands.json` | `build.py` |
| the symbol itself | `../laz-gunesi-amblem/svg/master.svg` | `build.py` |
| type stack / tracking | `brands.json` → `type` | `build.py` |

## Quick start

```bash
# one-time setup (from the repo root)
python3 -m venv .venv && ./.venv/bin/pip install -r brand/requirements.txt
cd brand && npm install

# 1. visual assets — logos, favicons, social
../.venv/bin/python build.py --brand agustos          # omit --brand for all

# 2. working documents — office, swatches, email, guidelines source
../.venv/bin/python build_templates.py --brand agustos
# then render the guidelines PDF (one browse command — see templates/README.md)

# 3. product datasheet ("teknik föy") — lighting spec sheet, A4, renders its own PDF
python3 build_datasheet.py --brand agustos --pdf   # std-lib only; no venv needed
```

## What gets generated

Per brand, under `exports/<brand>/`:

```
lockup/      symbol + wordmark — positive / negative / mono, each as svg + pdf + png (2400 & 800px)
favicon/     favicon.ico, favicon.svg, apple-touch-icon.png, manifest pngs, site.webmanifest
social/      square avatar (400 & 1000px) + 1200x630 og image (svg + png)
swatches/    <brand>.ase (Adobe) + <brand>.clr (Apple)
email/       <brand>-signature.html (email-safe, self-contained)
office/      <brand>-letterhead.docx + <brand>-template.pptx
guidelines/  <brand>-brand-guidelines.html + .pdf (4-page shareable)
datasheet/   <brand>-datasheet-template.html + .pdf (A4 lighting product "teknik föy")
```

`build.py` makes the first three (visual assets); `build_templates.py` makes the
working documents; `build_datasheet.py` makes the product datasheet. See
`templates/README.md` for using the Office files in PowerPoint / Keynote /
Google Slides / Word / Pages.

### The datasheet generator

`build_datasheet.py` is a third engine, for lighting product spec sheets. Unlike the
others (brand chrome only), a datasheet is **half template, half data**: the brand half
(lockup, colour, footer) resolves from `brands.json`; the product half lives in the
`PRODUCTS` dict at the top of the script. Each brand ships one sample luminaire so the
field structure is self-documenting.

- **To document a new product:** copy a `PRODUCTS` block, swap the values, point
  `photo` / `drawing` at image files under `datasheet-assets/<slug>/` (omit them to keep
  the dashed placeholders). Raster images are base64-embedded, so the HTML/PDF stay
  self-contained. `pataraz` (PL22) is a worked example built from real data; values the
  source did not publish are left as `—` placeholders to fill in.
- **To change which specs appear:** edit the `specs` groups — the group name becomes the
  brand-coloured section label; rows render in order, flowing into two columns.
- **Ordering matrix + certifications are optional** — omit those keys and the section
  disappears (e.g. PL22 is a single tunable SKU with no published variants).
- Labels are Turkish (`lang="tr"`, so İ/ı capitalise correctly). Values are set in
  JetBrains Mono with tabular numerals; brand colour is used only as a signal.
- Std-lib only (no PIL/reportlab) — runs on system `python3`. `--pdf` renders via the
  gstack `browse` tool; A4 page size is set in the HTML's `@page` rule.

- **positive** — brand color on transparent. Primary, ~90% of uses.
- **negative** — cream marks on a brand-color field. Banners, brand tiles.
- **mono** — single ink color on transparent. Print, stamps, engraving.

The wordmark is baked to vector **outlines**, so every file renders identically with
no font installed.

## How it works

`brands.json` + the shared symbol → `build.py` → `exports/`. The engine:

1. Instances Inter Tight at the wordmark weight (650, from `brands.json`) and converts each wordmark to outline paths (`fontTools`).
2. Composes the lockup with the symbol per `DESIGN.md` geometry (symbol = 1.4× cap height, gap = 0.4× size, optical centering for lowercase).
3. Writes SVG masters, renders PDF (`reportlab`, pure Python) and PNG (`scripts/render_png.mjs`, the `resvg` binary — no system Cairo needed).
4. Builds `.ico`, app icons, and the web manifest with Pillow.

## Adding a brand

1. Add an entry to `brands.json`: `wordmark`, `color`, `title`, `domain`, and optionally
   `tagline_en` / `tagline_tr` (either, both, or neither — taglines are defined as reference
   but not printed on artifacts; see the `$tagline_policy` note in `brands.json`).
2. Run `../.venv/bin/python build.py --brand <slug>` (logos/favicons/social), then
   `../.venv/bin/python build_templates.py --brand <slug>` (documents).

No new design work — the brand inherits the symbol, type, geometry, and all three
expressions automatically. ~10 minutes.

## Status

- ✅ `agustos` — full kit generated and reviewed: logos, favicons, social, swatches,
  email signature, Office templates (PPTX/DOCX), and 4-page guidelines PDF.
- ⏳ `pataraz`, `pld`, `photometric` — registered, not yet generated. Run both scripts
  (`build.py` then `build_templates.py`) per brand when ready.
- 📄 Datasheet template (`build_datasheet.py`) — `pataraz` is a real product (**PL22**,
  data + photo from pataraz.com); `agustos` is a sample (**Pro Spot 28**) showing the full
  template (ordering matrix + certs). Other brands generate a generic sheet on demand.
