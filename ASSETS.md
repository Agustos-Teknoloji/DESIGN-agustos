# Brand assets — canonical index

**The one place to find every Ağustos brand asset.** If you need the logo, the symbol, the
favicon, the colors, or the fonts, the canonical file is listed here. Don't hunt; don't guess;
don't re-create something that already exists. If you add or move a brand asset, update this file
in the same change.

Related: [DESIGN.md](DESIGN.md) is the canonical *specification* (the rules); this file is the
canonical *asset map* (the files). [MEMORY.md](MEMORY.md) holds the decision log.

---

## Identity ink and shared signal

| Token | Value | Use |
|---|---|---|
| **Ağustos red identity** | `#cf142a` | Ağustos symbol and wordmark; also the shared interaction signal. |
| House-brand identity ink | `#15130f` | Pataraz, PLD Türkiye, IESDesk, SpecQuick, and future house-brand positive marks. |
| Shared interaction signal | `#cf142a` | 2px content-link rule, current-page menu rule, and keyboard focus. Never a fill. |
| White (paper) | `#ffffff` | Primary substrate. |
| Cream (callout band) | `#fdf5f5` | Full-bleed callout and CTA bands only. |
| Ink | `#15130f` | Headlines, filled buttons, footer, and house-brand identity. |

Canonical color source: [`tokens/design-tokens.json`](tokens/design-tokens.json) plus the per-brand values in [`brand/brands.json`](brand/brands.json). `tokens/agustos.css` is generated.

> **One red.** Ağustos red is `#cf142a` everywhere — tokens, symbol SVGs, favicons, exports.
> An earlier `#D11D2B` in the symbol kit was reconciled to `#cf142a` (they are perceptually
> near-identical; the value matters because agents copy the hex). If you find `#D11D2B` anywhere,
> it is stale — fix it to `#cf142a`.

## The symbol — Laz Güneşi

18-blade rotational sun, the publisher's permanent mark ("one symbol, forever"). Carried by every
brand, in its registered identity ink.

| Asset | Path | Use |
|---|---|---|
| **Vector master** | [`laz-gunesi-amblem/svg/master.svg`](laz-gunesi-amblem/svg/master.svg) | Source of truth for the symbol shape. |
| Color variants (SVG) | `laz-gunesi-amblem/svg/laz-gunesi__*.svg` | red / white / black / on-white / on-black lockups. |
| Pre-rendered PNGs | `laz-gunesi-amblem/png/` | 256–4096px, transparent. For slides, social, avatars. |
| Print PDFs | `laz-gunesi-amblem/pdf/` | Print, signage, cards. **See PDF note below.** |
| Self-contained CSS | [`laz-gunesi-amblem/css/laz-sun.css`](laz-gunesi-amblem/css/laz-sun.css) | `.laz-sun` helper, SVG embedded as data-URI. |
| Original art | `laz-gunesi-amblem/source/*.ai` `.pdf` | Reference only — do not edit. |
| Geometry | [`laz-gunesi-amblem/docs/master_geometry.json`](laz-gunesi-amblem/docs/master_geometry.json) | Parametric definition (blade count, angles, paths). |

Full kit guide: [`laz-gunesi-amblem/README.md`](laz-gunesi-amblem/README.md).

## Favicon & app icons

Web-ready browser/OS icons. **Every favicon is a white tile carrying the Laz Güneşi in the
brand's identity ink**: red `#cf142a` for Ağustos, black `#15130f` for every other house brand
(MEMORY.md 2026-09-29 per-brand-favicons). The symbol paths are `master.svg`, verbatim.

| Asset | Path | Use |
|---|---|---|
| **Favicon kit (Ağustos, canonical)** | [`laz-gunesi-amblem/favicon/`](laz-gunesi-amblem/favicon/) | `favicon.svg` (red sun on white tile), `favicon.ico`, `favicon-16/32.png`, `apple-touch-icon.png`, `icon-192/512.png`, `site.webmanifest`. |
| **Favicon kit (per brand)** | `brand/exports/<brand>/favicon/` | Same tile; black sun for every brand except `agustos`. `favicon.svg`, `favicon.ico`, `favicon-16…512.png`, `apple-touch-icon.png`, `site.webmanifest`. Also generated for `memregunes` and `selimgunes`. |
| `<head>` snippet + guide | [`laz-gunesi-amblem/favicon/README.md`](laz-gunesi-amblem/favicon/README.md) | Copy-paste link tags; regeneration steps. |
| In-page symbol | [`laz-gunesi-amblem/favicon/favicon-mono.svg`](laz-gunesi-amblem/favicon/favicon-mono.svg) | The bare symbol (= `master.svg`, no tile), for UI next to text. Not a tab icon. |

**Canonical favicon = `laz-gunesi-amblem/favicon/favicon.svg`**, the Ağustos favicon. It is
byte-identical to `brand/exports/agustos/favicon/favicon.svg`. A site for any other brand uses
its own `brand/exports/<brand>/favicon/`. Each brand's `site.webmanifest` sets `theme_color` to
the brand's identity ink and `background_color` to white. All of it comes from
`brand/build.py --favicons`, which writes no other export.
Any other `favicon.svg` in the repo (e.g. an adapter's `public/`) is a **mirror** — when the
canonical changes, update the mirrors in the same change. Adapter mirror today:
[`adapters/astro/public/favicon.svg`](adapters/astro/public/favicon.svg).

## Typography

Three families, self-hosted via fontsource. Full spec in DESIGN.md §"The type stack".

| Role | Family | Notes |
|---|---|---|
| Display / logotype | **Inter Tight** | Wordmark at weight 650. |
| Body | **Inter** | Paragraphs, inline. |
| Mono | **JetBrains Mono** | Code, hex, identifiers. |

Token definitions: [`tokens/agustos.css`](tokens/agustos.css) (`--display`, `--body`, `--mono`).

## The lockup (logo)

`[ symbol ]  wordmark` — symbol + lowercase brandname in registered identity ink. This is a *typographic*
lockup, not a static image: it is composed at render time from the symbol + Inter Tight.

| Implementation | Path |
|---|---|
| Astro component | [`adapters/astro/src/components/BrandLockup.astro`](adapters/astro/src/components/BrandLockup.astro) |
| Rails partial | `adapters/rails/app/views/agustos/shared/` |

Grammar and rules: DESIGN.md §"Logo system".

---

## Brand kit — generated per-brand assets

`brand/` is the generate-don't-maintain asset kit (the static-export complement to the
render-time lockup above). Edit the registry or master symbol, then run the two build
scripts; never hand-edit `exports/`.

| Asset | Path |
|---|---|
| Registry (keystone, source of truth) | [`brand/brands.json`](brand/brands.json) |
| Engine — logos / favicons / social | [`brand/build.py`](brand/build.py) |
| Engine — office / swatches / email | [`brand/build_templates.py`](brand/build_templates.py) |
| Engine — brand guidelines (14-page A4 PDF, rebuilt 2026-10-03 for v7.7.0) | [`brand/build_guidelines.py`](brand/build_guidelines.py) |
| Engine — editable PowerPoint / Google Slides import | [`brand/build_presentation.mjs`](brand/build_presentation.mjs) |
| Office artifact drift manifest (9 files, generated) | [`brand/exports/office-manifest.json`](brand/exports/office-manifest.json) |
| Engine — product datasheet (lighting "teknik föy") | [`brand/build_datasheet.py`](brand/build_datasheet.py) |
| Engine: LinkedIn post templates (portrait 1080×1350, square 1200×1200) | [`brand/build_social_posts.py`](brand/build_social_posts.py) |
| Fonts (Inter Tight, Inter, JetBrains Mono) + OFL | `brand/fonts/` |
| Client brand logos (HEPER, LIGMAN; the LIGMAN file is a trace until LIGMAN sends the vector) | `brand/clients/<slug>/logo.svg`, with the client's file as `logo-source.png` |
| Per-brand exports | `brand/exports/<brand>/` |

Each `exports/<brand>/` holds: `lockup/` (positive/negative/mono × svg·pdf·png), `favicon/`,
`social/`, `swatches/` (.ase/.clr), `email/` (signature), `office/` (editable PPTX, letterhead DOCX, styled document DOCX),
`guidelines/` (14-page PDF), and `datasheet/` (A4 lighting product sheets, html + pdf). Full
kits: `agustos`, `pataraz`, `pld`; `iesdesk`, `specquick` and `selimgunes` have logos only. The `datasheet/` folder holds
one sheet per product — real Pataraz luminaires (`pataraz-pl22`, `pataraz-px22`, and the
PY series `pataraz-py300600` / `pataraz-py600600` / `pataraz-py6001200`) and an `agustos`
sample (`agustos-pro-spot-28`); add a product by editing the `PRODUCTS` dict in
`build_datasheet.py` (keyed by product, each naming its brand). `social/` also holds the
LinkedIn post templates, `<post-key>-portrait` and `<post-key>-square` (html + png), one sample per
full-kit brand (`agustos-company`, `pataraz-px22`, `pld-editorial`); add a post by editing the `POSTS`
dict in `build_social_posts.py`, then run `python3 brand/build_social_posts.py --png`. Docs: `brand/README.md`,
`brand/templates/README.md`.

The portable single-file coding-system contract is [`tokens/design-system-handoff.json`](tokens/design-system-handoff.json). It contains resolved tokens, brand values, recipes, family-resemblance rules, forbidden patterns, and acceptance checks; supply the exact logo asset separately when implementing a branded interface.

---

## Web distribution kit — `ui/`

Generated. What another repository consumes to build an interface. Never hand-edit; edit the
`.tmpl` sources and re-run `python3 scripts/build_design_system.py`.

| Asset | Path | Note |
|---|---|---|
| Entry point | `ui/UI-KIT.md` | The one file an agent reads. |
| Stylesheet | `ui/agustos.css` | Byte-identical to `tokens/agustos.css` apart from the header. |
| Webfont CSS | `ui/agustos-fonts.css` | Relative `url()`, so it resolves from CDN and vendored alike. |
| Webfonts | `ui/fonts/*.woff2` | 5 subset variable faces, ~600 KB total. Generated by `scripts/build_ui_fonts.py` from `brand/fonts/`. |
| Font licenses | `ui/fonts/OFL-*.txt` | SIL OFL. Must travel with the binaries. |
| Client brand files | `ui/brands/<slug>.css`, `ui/brands/<slug>.svg`, `ui/brands/<slug>-dark.svg` | One set per client in `brand/brands.json` `clients`: the button colour on `.brand-<slug>`, and the logo for each theme. |
| Reference render | `ui/starter.html` | Every published class, once. |
| Machine index | `ui/kit.json` | Contract plus file hashes. |
| Checker | `ui/check-agustos-ui.py` | Consumers run it to prove compliance. |
| Adoption snippet | `ui/AGENTS-SNIPPET.md` | Paste into a consuming repo's `AGENTS.md`. |

## Known gaps / follow-ups

- **Print PDFs still at `#D11D2B`.** `laz-gunesi-amblem/pdf/laz-gunesi__red*.pdf` predate the
  single-red change. A vector SVG→PDF/PNG pipeline now exists in `brand/` (reportlab + resvg,
  see `brand/requirements.txt`); regenerate these from the updated `svg/` with it. The visual
  difference is negligible.

## Sync rules (don't let assets drift)

1. **Tokens** are generated into adapter copies — run `python3 scripts/build_design_system.py`; `--check` rejects drift.
2. **Favicon** canonical (Ağustos) lives in `laz-gunesi-amblem/favicon/`, per-brand kits in `brand/exports/<brand>/favicon/`; adapter `public/` copies are mirrors.
3. **This index** must be updated whenever a brand asset is added, moved, or recolored.
4. **`ui/` is generated** — edit the `.tmpl` sources, never the outputs. `ui/fonts/` regenerates
   separately via `scripts/build_ui_fonts.py`, and only when the masters in `brand/fonts/` change.
5. **Any `ui/` change needs a VERSION bump and a matching `v<VERSION>` tag** in the same change.
   Consumers pin that tag; an unpinned consumer is a defect the checker reports as `AG008`.
