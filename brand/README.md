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
python3 -m venv .venv && ./.venv/bin/pip install fonttools brotli svglib reportlab pillow
cd brand && npm install

# generate everything
../.venv/bin/python build.py                  # all brands
../.venv/bin/python build.py --brand agustos  # one brand
```

## What gets generated

Per brand, under `exports/<brand>/`:

```
lockup/   symbol + wordmark — positive / negative / mono, each as svg + pdf + png (2400 & 800px)
favicon/  favicon.ico, favicon.svg, apple-touch-icon.png, manifest pngs, site.webmanifest
social/   square avatar (400 & 1000px) + 1200x630 og image (svg + png)
```

- **positive** — brand color on transparent. Primary, ~90% of uses.
- **negative** — cream marks on a brand-color field. Banners, brand tiles.
- **mono** — single ink color on transparent. Print, stamps, engraving.

The wordmark is baked to vector **outlines**, so every file renders identically with
no font installed.

## How it works

`brands.json` + the shared symbol → `build.py` → `exports/`. The engine:

1. Instances Inter Tight at weight 300 and converts each wordmark to outline paths (`fontTools`).
2. Composes the lockup with the symbol per `DESIGN.md` geometry (symbol = 1.4× cap height, gap = 0.4× size, optical centering for lowercase).
3. Writes SVG masters, renders PDF (`reportlab`, pure Python) and PNG (`scripts/render_png.mjs`, the `resvg` binary — no system Cairo needed).
4. Builds `.ico`, app icons, and the web manifest with Pillow.

## Adding a brand

1. Add an entry to `brands.json` (`wordmark`, `color`, `title`, `domain`, `tagline`).
2. Run `../.venv/bin/python build.py --brand <slug>`.

No new design work — the brand inherits the symbol, type, geometry, and all three
expressions automatically. ~10 minutes.

## Status

- ✅ `agustos` — generated and reviewed.
- ⏳ `pataraz`, `pld`, `photometric` — registered, not yet generated (run the build when ready).
- 📁 `templates/` — office decks & letterhead (Phase 2, see `../tasks/todo.md`).
