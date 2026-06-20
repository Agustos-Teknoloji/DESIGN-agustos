# Brand assets — canonical index

**The one place to find every Ağustos brand asset.** If you need the logo, the symbol, the
favicon, the colors, or the fonts, the canonical file is listed here. Don't hunt; don't guess;
don't re-create something that already exists. If you add or move a brand asset, update this file
in the same change.

Related: [DESIGN.md](DESIGN.md) is the canonical *specification* (the rules); this file is the
canonical *asset map* (the files). [MEMORY.md](MEMORY.md) holds the decision history.

---

## Brand colors

| Token | Value | Use |
|---|---|---|
| **Ağustos red** | `#cf142a` | The brand color. **This is the single source of truth** — see note below. |
| Pataraz blue | `#1a24cc` | Sibling brand. |
| PLD black | `#1a1a1a` | Sibling brand. |
| Photometric green | `#1f6b4a` | Sibling brand. |
| Cream (paper) | `#fefcf2` | Primary branded substrate. |
| Ink | `#1a1a1a` | Primary text. |

Canonical color source: [`tokens/agustos.css`](tokens/agustos.css) (mirrored — see DESIGN.md §"Mirrored implementation").

> **One red.** Ağustos red is `#cf142a` everywhere — tokens, symbol SVGs, favicons, exports.
> An earlier `#D11D2B` in the symbol kit was reconciled to `#cf142a` (they are perceptually
> near-identical; the value matters because agents copy the hex). If you find `#D11D2B` anywhere,
> it is stale — fix it to `#cf142a`.

## The symbol — Laz Güneşi

18-blade rotational sun, the publisher's permanent mark ("one symbol, forever"). Carried by every
brand, in that brand's color.

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

Web-ready browser/OS icons. The **negative expression** (white symbol on a red tile) per
DESIGN.md §"Three expressions" — the documented favicon treatment.

| Asset | Path | Use |
|---|---|---|
| **Favicon kit** | [`laz-gunesi-amblem/favicon/`](laz-gunesi-amblem/favicon/) | `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-192/512.png`, `site.webmanifest`. |
| `<head>` snippet + guide | [`laz-gunesi-amblem/favicon/README.md`](laz-gunesi-amblem/favicon/README.md) | Copy-paste link tags; regeneration steps. |
| In-page symbol | [`laz-gunesi-amblem/favicon/favicon-mono.svg`](laz-gunesi-amblem/favicon/favicon-mono.svg) | Bare red symbol on transparent — for UI next to text, **not** the browser tab. |

**Canonical favicon = `laz-gunesi-amblem/favicon/favicon.svg`.** Any other `favicon.svg` in the repo
(e.g. an adapter's `public/`) is a **mirror** — when the canonical changes, update the mirrors in the
same change. Adapter mirror today: [`adapters/astro/public/favicon.svg`](adapters/astro/public/favicon.svg).

## Typography

Three families, self-hosted via fontsource. Full spec in DESIGN.md §"The type stack".

| Role | Family | Notes |
|---|---|---|
| Display / logotype | **Inter Tight** | Wordmark at weight 650. |
| Body | **Inter** | Paragraphs, inline. |
| Mono | **JetBrains Mono** | Code, hex, identifiers. |

Token definitions: [`tokens/agustos.css`](tokens/agustos.css) (`--display`, `--body`, `--mono`).

## The lockup (logo)

`[ symbol ]  wordmark` — symbol + lowercase brandname in brand color. This is a *typographic*
lockup, not a static image: it is composed at render time from the symbol + Inter Tight.

| Implementation | Path |
|---|---|
| Astro component | [`adapters/astro/src/components/BrandLockup.astro`](adapters/astro/src/components/BrandLockup.astro) |
| Rails partial | `adapters/rails/app/views/agustos/shared/` |

Grammar and rules: DESIGN.md §"Logo system".

---

## Known gaps / follow-ups

- **Print PDFs still at `#D11D2B`.** `laz-gunesi-amblem/pdf/laz-gunesi__red*.pdf` were not
  regenerated to `#cf142a` — there is no vector SVG→PDF rasterizer available locally
  (rsvg/inkscape/cairosvg). The difference is visually negligible. Regenerate from the updated
  `svg/` when one of those tools is installed.

## Sync rules (don't let assets drift)

1. **Tokens** mirror to adapter + website copies — see DESIGN.md §"Mirrored implementation".
2. **Favicon** canonical lives in `laz-gunesi-amblem/favicon/`; adapter `public/` copies are mirrors.
3. **This index** must be updated whenever a brand asset is added, moved, or recolored.
