# Ağustos UI kit — v6.0.0

Read this complete interface contract before building for an Ağustos-family brand. You do not need to open `DESIGN.md`.

Use the generated registry values. Request missing values instead of inventing them.

## Design direction — İskandivvian

Scandinavian restraint filtered through Mediterranean warmth.

Create minimal, functional, and elegant interfaces that feel warm and human.
İskandivvian is our project label. Keep the experience welcoming and easy to use.

- Use white as the paper. Reserve cream for full-bleed callout and CTA bands. The six colours are white #ffffff, cream #fdf5f5, light gray #ebebeb, dark gray #404040, off-black #15130f, and red #cf142a.
- Express warmth through those grays, cream bands, comfortable spacing, readable typography, and approachable language.
- Make every section useful. Keep navigation, information, and next actions easy to understand.
- Use clear hierarchy and one alignment frame. Let spacing explain relationships without hiding useful content.
- Use modest corners and hairline rules. Do not use shadows, gradients, or textures.
- Keep text, controls, and technical tables on plain surfaces. Use authentic imagery only when it explains the work.
- Ration red to the 2px content-link rule, the 2px menu hover or current-page rule, and keyboard focus. The one fill exception is the dark-theme primary CTA. Dark theme reuses the same six roles, flipped. Retain registered logos, fonts, and accessible contrast.
- Write direct, helpful copy in sentence case. Do not use uppercase labels or eyebrow headings.
- Repeat the same primary CTA at most twice in the page body: the opening and one closing cream band. The header may carry it once.
- Ship marketing, catalog, and spec pages on white paper. Reserve dark theme for product UI.
- Introduce photographs in this order: product page, listing thumbnail, then homepage installation. Type-only pages stay complete.
- Use blockquote and pullquote on content pages only. Marketing pages use a compact trust line, not a testimonial.

Avoid:

- Ornamental Mediterranean motifs or unrelated lifestyle imagery
- Red fills, red buttons, red statistics, or red as an element's own colour, except the dark-theme primary CTA
- Uppercase labels, eyebrow labels, arrows on buttons, or decorative motion
- Inflated luxury claims or forced friendliness
- A primary button in every section, card, or list
- A theme toggle on marketing chrome
- Lifestyle photography or a photograph behind body text
- Testimonial quotes on marketing pages

## Install

The kit is plain CSS. Do not add Tailwind, Bootstrap, or another utility framework. `agustos.css` styles the whole page, including bare HTML elements, and a second page stylesheet conflicts with it.

Production: copy `agustos.css`, `agustos-fonts.css`, `fonts/` (5 woff2 files and 3 OFL.txt, which must travel with them), `check-agustos-ui.py`, and `UI-KIT.md` into `vendor/agustos-ui/` and commit them. Then load the two stylesheets, **fonts first**:

```html
<link rel="stylesheet" href="/vendor/agustos-ui/agustos-fonts.css">
<link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">
```

npm projects may skip `agustos-fonts.css` and run `npm i @fontsource-variable/inter-tight @fontsource-variable/inter @fontsource-variable/jetbrains-mono` instead.

Prototypes with no build step may link the CDN copies. **Pin to `@v6.0.0`.** Never `@main` or `@latest`; an unpinned link restyles a live page the moment a token changes.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@v6.0.0/ui/agustos-fonts.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@v6.0.0/ui/agustos.css">
```

## Page skeleton

```html
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="/vendor/agustos-ui/agustos-fonts.css">
  <link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">
</head>
<body class="brand-agustos site-sidebar-layout" data-screen="home">
  <a class="skip-link" href="#main">İçeriğe geç</a>
  <!-- the brand's chrome: see Chrome below -->
  <main id="main" class="container">
    <!-- your page -->
  </main>
</body>
</html>
```

Use `lang="tr"` for Turkish content so locale-sensitive capitalization renders correctly. Put `data-screen="<name>"` on `body` with a name from the screens table.

## Brand, chrome, theme

Each brand registers one chrome. `agustos` alone owns red identity ink; other house brands use off-black `#15130f` or white. Shared red (`#cf142a`) is a 2px rule under content links and menu hover or current, plus keyboard focus. Never a fill except the dark primary CTA.

| Brand | Class | Chrome |
|---|---|---|
| ağustos | `brand-agustos` | sidebar |
| pataraz | `brand-pataraz` | topbar |
| pld türkiye | `brand-pld` | topbar |
| iesdesk | `brand-iesdesk` | sidebar |
| specquick | `brand-specquick` | sidebar |

| Switch | Values | Where |
|---|---|---|
| Brand | one `brand-*` class from the table | `<body>`, required |
| Chrome | `site-sidebar-layout` on `<body>` for sidebar brands; nothing for topbar brands | `<body>` |
| Theme | `data-theme="dark"` (product UI only; same six colours, flipped) | `<html>` |
| Substrate | white paper by default; `paper-white` remains valid | `<body>` |

## Chrome

Both chromes ship. No JavaScript: drawers are native popovers, groups are `details`. Copy the markup from `starter.html`, which renders the sidebar as its own chrome and the topbar and footer inside it.

- **Sidebar** (`site-sidebar*`): a fixed 240px column with the lockup, `site-sidebar__nav` links, `site-sidebar__group` details for social and legal, one `site-sidebar__cta`, a `site-sidebar__utility` slot for search and language, and a `site-sidebar__note`. Below 1024px a sticky `site-sidebar-bar` with the burger opens it as a drawer.
- **Topbar** (`site-header*`, `site-footer*`): a sticky one-row header inside a `site-frame` with the lockup, `site-header__nav`, and a `site-header__end` slot for CTA, search, and language; a structured footer with `site-footer__brand` and configurable `site-footer__col` columns. Below 1024px the burger opens `site-header__panel` as a drawer.
- **Lockup** (`site-lockup`): the exact Laz Güneşi symbol inline plus a lowercase wordmark. Never redraw the symbol; copy it from `starter.html`.
- The current page carries `aria-current="page"`: a 2px red rule on the left in the sidebar, underneath in the topbar. Every control is 44px.
- Destinations, copy, and columns are configuration. The kit styles them; it never decides them.

## Screens

One reference page per screen type lives in the source repository under `screens/`, hand-written on these classes. Build any page from the matching screen. Theme follows the family; chrome follows the brand.

| Screen | Family | Chrome | Theme | Primary CTA in body | Quotes | Photography |
|---|---|---|---|---|---|---|
| `home` | marketing | sidebar | light | at most 2 | no | one installation photograph, third in the rollout |
| `static` | content | sidebar | light | at most 1 | yes | people and places that explain the work |
| `content` | content | sidebar | light | at most 1 | yes | only when it explains the content |
| `products` | catalog | topbar | light | at most 1 | no | product thumbnails, second in the rollout |
| `product-finder` | catalog | topbar | light | at most 1 | no | product thumbnails, second in the rollout |
| `product` | catalog | topbar | light | at most 2 | no | product photograph or drawing, first in the rollout |
| `spec-sheet` | document | topbar | light | at most 0 | no | product photograph and dimensioned drawing |
| `app-shell` | product UI | sidebar | dark allowed | at most 1 | no | none |

Form submits are task actions and do not count as the page primary. Footer Contact is separate chrome. Marketing pages use a compact trust line, not a testimonial. Photographs arrive in the rollout order shown; type-only pages stay complete.

## Classes

Every class the kit publishes. See `starter.html` for one rendered instance of each.

| Group | Classes |
|---|---|
| Frame | `site-frame` `container` `skip-link` |
| Layout | `stack` `cluster` `prose` `grid-2` `grid-3` `grid-4` `grid-aside` `band` `band--cream` |
| Headings | `type-hero` `type-hero-md` `type-hero-deck` `type-h1` `type-h2` `type-h3` `type-h4` |
| Text | `type-body` `type-link` `type-code` `type-blockquote` `type-pullquote` `type-footnote` |
| Blocks | `type-list-ul` `type-list-ol` `type-dl` `type-figure` `type-code-block` `type-table` `type-divider` |
| Hero | `hero-actions` `hero-action` `hero-action--primary` `hero-action--secondary` · `hero-links` `hero-link` `hero-link--primary` `hero-link--secondary` · `hero-trust` `hero-visual` |
| Sections | `agustos-section` `agustos-section__head` |
| Cards | `agustos-card-grid` `agustos-card` `agustos-card--marked` |
| Chrome | `agustos-chrome-link` · `site-lockup` `site-lockup__symbol` `site-lockup__name` · `site-sidebar-layout` `site-sidebar` `site-sidebar__nav` `site-sidebar__link` `site-sidebar__group` `site-sidebar__cta` `site-sidebar__utility` `site-sidebar__note` `site-sidebar-bar` `site-sidebar-burger` · `site-header` `site-header__bar` `site-header__panel` `site-header__nav` `site-header__link` `site-header__end` `site-header__cta` `site-header__burger` · `site-footer` `site-footer__inner` `site-footer__brand` `site-footer__cols` `site-footer__col` `site-footer__col-heading` `site-footer__list` `site-footer__link` `site-footer__cta` · `breadcrumb` `breadcrumb__link` |
| Forms | `agustos-fieldset` `agustos-field` `agustos-field--invalid` · `agustos-label` `agustos-label--required` · `agustos-input` `agustos-textarea` `agustos-select` `agustos-check` `agustos-hint` `agustos-error` |
| Buttons | `agustos-button` `--primary` `--secondary` `--quiet` |
| Badges | `agustos-badge` `--success` `--warning` `--danger` `--info` `--signal` |
| Notices | `agustos-notice` `agustos-notice__title` `--success` `--warning` `--danger` `--info` |
| Tabs | `agustos-tabs` `agustos-tab` `agustos-tabs__panel` |

Bare HTML elements are styled too: `h1`–`h4`, `p`, `a`, `ul`, `ol`, `dl`, `table`, `blockquote`, `pre`, `code`, `hr`. Semantic markup gets the right result without classes.

Compose missing components from `agustos-card`, `agustos-button`, the layout classes, and `type-*`. `prose` caps a text block at the 65ch measure. Do not import another component library.

## Variables

Use `var(--name)`, never the literal value. Spacing `--space-2xs` … `--space-6xl`.
Radii `--radius-sm` (4px) `--radius-md` (6px) `--radius-lg` (10px) — nothing larger exists.
Color `--paper` `--cream` `--surface` `--ink` `--ink-soft` `--ink-faint` `--rule` `--signal` `--brand`
`--footer-*` `--state-success|warning|danger|info`. Type `--display` `--body` `--mono`.
Motion `--dur` `--ease`. Targets `--control-min` (44px). Frame `--measure-content` (1180px). Sidebar `--sidebar-width` (240px).
Measures `--measure-text` (54ch, hero deck) and `--measure-body` (65ch, long-form prose: posts, policies, profiles).

`ui/kit.json` carries the same lists in machine-readable form, plus the brand and screens tables.

## Hard rules

1. **Never retype a token value.** Use `var(--signal)`, not `#cf142a`.
2. **Brand red is `#cf142a`.** `#D11D2B` is stale — fix it wherever you find it.
3. **Never restyle a kit class.** Overriding `.agustos-card` breaks every other page. Compose a new class.
4. **Radii are 4, 6, and 10px.** Nothing rounder. No pills, no blobs, no gradients.
5. **44px minimum for anything clickable.** `--control-min` exists for this. Links inside running text are exempt; `hero-link` carries an invisible 44px hit area, and a card with one stretched link makes the card the target.
6. **Never redraw the Laz Güneşi symbol.** Copy the `site-lockup` markup from `starter.html`.
7. **Use the brand's registered chrome.** A sidebar brand never gets a topbar page, and the reverse.

## Verify before you call it done

```bash
python3 vendor/agustos-ui/check-agustos-ui.py .
```

Fix reported token values, font loading, CDN pins, brand classes, radii, and class overrides.
Use `--strict` to fail on warnings; use `--json` for structured output. Exit 0 confirms automated checks passed.
Use `--skip <dir>` (repeatable) for frozen or generated folders the project must not edit. Do not hand-edit the checker; it is regenerated with the kit.
Check for a newer kit with `python3 vendor/agustos-ui/check-agustos-ui.py --update-check`.

## If you need more than this file

- `kit.json` — the same contract, machine-readable, with file hashes.
- `starter.html` — every class, rendered once, including both chromes.
- `screens/` in the source repository — one reference page per screen type.
- `tokens/design-system-handoff.json` in the source repository — the full cross-medium contract with the embedded symbol.

Source: `Agustos-Teknoloji/DESIGN-agustos` · licensed under `ui/LICENSE`.
