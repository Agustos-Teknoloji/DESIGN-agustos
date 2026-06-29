# Agent guide — Ağustos brand assets

Entry point for any AI tool (Claude, Cursor, Copilot, Codex, etc.). Goal: get you to the
**right brand asset file fast**, and stop you from re-creating something that already exists.

## 30-second model

- One company, several brands: **ağustos** (parent), **pataraz**, **pld türkiye**, **photometric**.
- Every brand shares **one symbol** — the Laz Güneşi (18-blade sun) — and differs only by its
  **wordmark** and **color**.
- The logo (“lockup”) = symbol + lowercase wordmark in the brand color. Always lowercase. No tagline on it.

## Where to look, in order

1. **[ASSETS.md](ASSETS.md)** — the canonical index of every asset file, by category. Check here first.
2. **`brand/exports/<brand>/`** — ready-to-use, per-brand exported files (logos, favicons, social, docs).
3. **[DESIGN.md](DESIGN.md)** — the rules/spec. **[MEMORY.md](MEMORY.md)** — why decisions were made
   (read before reversing one). **[brand/README.md](brand/README.md)** — how to regenerate or add a brand.

## "I need ___" → use this file

First pick the **brand** (`agustos` · `pataraz` · `pld` · `photometric`), then the use. Substitute the
brand slug into `<brand>` in the path (e.g. `agustos`, `pld`).

| I need… | File |
|---|---|
| The logo for a **website/app** (vector) | `brand/exports/<brand>/lockup/<brand>-lockup__positive.svg` |
| The logo on a **dark / brand-color / photo** background | `…/lockup/<brand>-lockup__negative.svg` |
| The logo in a **single ink color** (print, engraving) | `…/lockup/<brand>-lockup__mono.svg` |
| The logo for **print / business cards** | `…/lockup/<brand>-lockup__positive.pdf` (or `__negative` / `__mono`) |
| The logo for a **slide / social post** (raster) | `…/lockup/<brand>-lockup__positive.png` (2400px) or `…@800.png` |
| A **favicon / browser tab / app icon** | `brand/exports/<brand>/favicon/` (full set + `site.webmanifest`) |
| A **square profile avatar** | `brand/exports/<brand>/social/<brand>-avatar-1000.png` (or `-400`) |
| A **link-preview / OG image** (1200×630) | `brand/exports/<brand>/social/<brand>-og.png` |
| Just the **symbol**, no wordmark | `laz-gunesi-amblem/svg/master.svg` (recolor to the brand color) |
| The **generic symbol favicon** (not per-brand) | `laz-gunesi-amblem/favicon/favicon.svg` |
| **Brand colors as swatches** | `brand/exports/<brand>/swatches/<brand>.ase` (Adobe) · `.clr` (Apple) |
| A **PowerPoint / Word** template | `brand/exports/<brand>/office/<brand>-template.pptx` · `-letterhead.docx` |
| An **email signature** | `brand/exports/<brand>/email/<brand>-signature.html` |
| **Brand guidelines** to share | `brand/exports/<brand>/guidelines/<brand>-brand-guidelines.pdf` |
| A **product datasheet** (lighting "teknik föy", A4) | `brand/exports/<brand>/datasheet/<product-key>.pdf` (e.g. `pataraz-px22.pdf`; edit `PRODUCTS` in `brand/build_datasheet.py`, re-run) |
| The **fonts** (to install) | `brand/fonts/` (Inter Tight, Inter, JetBrains Mono + licenses) |

> Coverage: `agustos`, `pataraz`, `pld` have the **full** set above. `photometric` has **logos,
> favicons, and social only** (no office / swatches / email / guidelines yet). The **datasheet**
> kit holds many products per brand: real Pataraz sheets (`pataraz-pl22`, `pataraz-px22`) and an
> `agustos` sample (`agustos-pro-spot-28`); other brands produce a generic sheet on demand.

## The three logo expressions — pick by background

1. **positive** — brand color marks on a light/cream **or** dark background (the brand color reads on
   both). This is the default, ~90% of uses.
2. **negative** — cream/white marks on a brand-color tile. Favicons, brand-color banners.
3. **mono** — one ink color. Single-color print, stamps, engraving.

There is no fourth expression. Do not invent a white-on-transparent "reverse" logo — `positive` already
works on dark.

## Brands at a glance

| Brand (slug) | Wordmark | Color | Domain | Kit |
|---|---|---|---|---|
| `agustos` | ağustos | `#cf142a` | agustos.com | full |
| `pataraz` | pataraz | `#1a24cc` | pataraz.com | full |
| `pld` | pld türkiye | `#1a1a1a` | pldturkiye.com | full |
| `photometric` | photometric | `#1f6b4a` | — | logos only |

Novara (outdoor kitchen furniture) is a brand Ağustos **represents/distributes** (like Soraa, CoeLux),
**not** a house brand — it has no assets here and needs none.

## Hard rules — do not break

- **Brand red is `#cf142a`.** `#D11D2B` is stale; if you see it, fix it to `#cf142a`.
- **Wordmark = Inter Tight, weight 650, lowercase, brand color.** Never put a tagline or subtitle on the lockup.
- **One symbol for all brands.** Never redraw it or recolor it to anything but a brand color.
- **NEVER hand-edit anything under `brand/exports/`.** It is all generated. To change an asset, edit
  **`brand/brands.json`** (the keystone registry) or the master symbol, then re-run the build
  (`brand/build.py` + `brand/build_templates.py` — see `brand/README.md`). Then update `ASSETS.md`.
- **Taglines** are defined in `brand/brands.json` (`tagline_en` / `tagline_tr`) but used sparingly and
  **not printed** on artifacts. The lockup is always tagline-free.
- If you **add, move, or recolor** any brand asset, **update `ASSETS.md` in the same change**.

## Regenerate or add a brand

Everything derives from `brand/brands.json` + the master symbol. Add a registry entry (wordmark, color,
domain) and run the two build scripts — ~10 minutes, no new design work. Full steps: `brand/README.md`.
