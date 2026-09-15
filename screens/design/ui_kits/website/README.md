# Website kit — Ağustos marketing site

The editorial marketing-site surface of the Ağustos design system. One structure, four brands: the **brand axis is name + color only** — switch brand in the header and the symbol, wordmark, eyebrow, link underlines, nav active-state, and focus rings all re-resolve `var(--brand)`. Nothing structural changes.

Open **`index.html`** to run it.

## What's here

| File | Role |
|---|---|
| `index.html` | Shell. Loads React + Babel, `styles.css`, `site.css`, the `_ds_bundle.js`, then the four JSX files in order. Also the **Website** starting point. |
| `app.jsx` | Composes the page and holds the per-brand `SITE` content map (the multi-brand demonstration). Mounts `#root`. |
| `header.jsx` | `SiteHeader` (top-bar nav) **and** `SiteSidebar` (left-rail nav) — both carry the `Lockup` + nav + brand switcher. |
| `hero.jsx` | `SiteHero` — top-aligned editorial hero: eyebrow → `.type-hero-md` headline → `.type-hero-deck` → `hero-links` → `.hero-trust`. |
| `sections.jsx` | `SiteWork` (3-up `Card` grid), `SiteBand` (featured pullquote + actions), `SiteFooter` (mono `Lockup` + columns). |
| `site.css` | Layout shell only — header, sidebar, grid, band, footer. **No type or color values**; every color comes from tokens, every type style from `.type-*`. |
| `tweaks-panel.jsx` | The Tweaks shell + controls (host-protocol wiring). |

## Two layouts (Tweaks)

The kit ships **two navigation layouts**, switchable live from the **Tweaks** panel:

- **Sidebar** (default) — a fixed left rail with the lockup, a vertical nav, and the brand switcher pinned to the bottom under a "Viewing as" label. Collapses to a stacked top strip under 820px.
- **Top bar** — the original sticky editorial header with horizontal nav and an inline brand switcher.

Two more tweaks are included by default: **Hero headline scale** (`medium` = `.type-hero-md`, `large` = `.type-hero`) and **Substrate** (`cream` / `white`). All three are content-agnostic — they flip layout/scale/paper without touching the brand axis. The default `TWEAK_DEFAULTS` block lives at the top of `app.jsx`.

Note: chrome nav links (header/sidebar/footer) opt out of the global editorial brand-underline via a specificity-matched rule at the top of `site.css` — they are navigation, not editorial links.

## How it uses the system

- **Components** come from the bundle: `const { Lockup, Link, Button, Badge, Card } = window.AUstosDesignSystem_7fee69`.
- **The hero follows the spec exactly** (DESIGN.md → "Hero element styles"): the headline is ink-on-paper `.type-hero-md`, never a link; actions are editorial `Link`s with brand underline + arrow, never filled buttons; one `.hero-trust` proof line, no badge wall.
- **Brand color is rationed** — it appears only on the symbol/wordmark, the hero eyebrow, link underlines, the active switcher pill, and the one `marked` featured card's leading rule. Everything else is ink on cream.
- **Substrate is cream** (`--paper`), the default branded paper. No gradients, textures, or decorative imagery.

## Extending

- **Add a brand:** add a `--brand-{slug}` + `.brand-{slug}` line in `tokens/colors.css`, add the wordmark to `BRANDS` in `header.jsx`, and add a content block to `SITE` in `app.jsx`. ~10 minutes, no new design work.
- **Edit content:** everything visible lives in the `SITE` map in `app.jsx` — copy, nav labels, work items, footer columns. Structure and styling stay in the JSX/CSS.
- **New section:** add a `Site*` component in `sections.jsx`, export it to `window`, and drop it into `App` in `app.jsx`. Reach for the `.type-*` tokens and the spacing scale (`var(--space-*)`); don't introduce raw color or font values.
