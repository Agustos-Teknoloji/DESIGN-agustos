# Ağustos UI kit — v7.3.2

Read this complete interface contract before building for an Ağustos-family brand. You do not need to open `DESIGN.md`.

Use the generated registry values. Request missing values instead of inventing them.

## Design direction — İskandivvian

Scandinavian restraint filtered through Mediterranean warmth.

Create minimal, functional, and elegant interfaces that feel warm and human.
İskandivvian is our project label. Keep the experience welcoming and easy to use.

- Use six colours: white #ffffff as the paper, pale red #fdf5f5 for the closing band, light gray #ebebeb for functional surfaces, dark gray #404040 for secondary text, off-black #15130f for text and buttons, and red #cf142a. Two support values serve only hairlines (#e8e4da) and faint marks (#8a8378). A new value needs a deleted one.
- Set type on one golden scale: the 16.5px body times 1.272 per step, so every second step is the golden ratio (13, 16.5, 21, 27, 34, 43, 55, 70, 89px). Headings are thin: hero 89px light, H1 55px light, H2 43px regular, H3 21px medium. Use four weights (300, 400, 500, 600). The wordmark alone uses 650.
- Use two radii, 6px for controls and 12px for cards, and one section spacing. Do not use gradients or textures. The only shadow sits under a menu that floats above the page.
- Red is identity and signal, never action: the logo, the 2px link and menu rule, keyboard focus, and one highlighter stroke per page. Buttons are black. The Ağustos logo is red and turns black on hover; every other house brand's logo is black and turns red on hover.
- Use the highlighter once per page, on one to four words of the main headline. Never on links, buttons, numbers, body text, or product UI. The sentence must read the same without it.
- Websites use the top menu with at most five items. Extra pages go under one More menu, and social, legal, and language links live in the footer. Product UI uses the sidebar. Websites ship light; dark theme is for product UI.
- Copy a screen; do not design a page. Open with a headline, a deck, two buttons, and a trust line. Close with one pale red band.
- Bold (600) marks a fact the reader scans for, at most once per paragraph. Italic marks names of publications and projects, foreign terms, and quoted phrases. Underline is for links only. Do not combine them, and do not use uppercase labels, eyebrow headings, or coloured text.
- When unsure, do the conventional thing. Collect design tweaks and release the kit once a month; fix real defects at once.

Avoid:

- Red buttons, red statistics, red fills, or red text. The logo and the one highlighter stroke are the only red areas
- More than one highlighter stroke on a page
- Uppercase labels, eyebrow labels, arrows on buttons, or decorative motion
- Inflated luxury claims or forced friendliness
- A primary button in every section, card, or list
- A sidebar on a website, or more than five items in its top menu
- A theme toggle on a website
- Lifestyle photography or a photograph behind body text

## Install

The kit is plain CSS. Do not add Tailwind, Bootstrap, or another utility framework. `agustos.css` styles the whole page, including bare HTML elements, and a second page stylesheet conflicts with it.

Production: copy `agustos.css`, `agustos-fonts.css`, `fonts/` (5 woff2 files and 3 OFL.txt, which must travel with them), `agustos-chrome.js`, `check-agustos-ui.py`, and `UI-KIT.md` into `vendor/agustos-ui/` and commit them. Then load the two stylesheets, **fonts first**:

```html
<link rel="stylesheet" href="/vendor/agustos-ui/agustos-fonts.css">
<link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">
```

npm projects may skip `agustos-fonts.css` and run `npm i @fontsource-variable/inter-tight @fontsource-variable/inter @fontsource-variable/jetbrains-mono` instead.

Prototypes with no build step may link the CDN copies. **Pin to `@v7.3.2`.** Never `@main` or `@latest`; an unpinned link restyles a live page the moment a token changes.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@v7.3.2/ui/agustos-fonts.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@v7.3.2/ui/agustos.css">
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
<body class="brand-agustos" data-screen="home">
  <a class="skip-link" href="#main">İçeriğe geç</a>
  <!-- the top menu, or the sidebar in product UI: see Chrome below -->
  <main id="main" class="container">
    <!-- your page -->
  </main>
</body>
</html>
```

Use `lang="tr"` for Turkish content so locale-sensitive capitalization renders correctly. Put `data-screen="<name>"` on `body` with a name from the screens table.

## Brand, chrome, theme

`agustos` alone owns red identity ink; every other house brand uses off-black `#15130f`, or white on dark. On the web the logo answers hover: the Ağustos logo turns black, every other logo turns red. Shared red (`#cf142a`) is otherwise a 2px rule under content links and under the current menu item, keyboard focus, and one highlighter stroke per page. Buttons are black, never red.

| Brand | Class | Logo | Logo on hover |
|---|---|---|---|
| ağustos | `brand-agustos` | red | black |
| pataraz | `brand-pataraz` | black | red |
| pld türkiye | `brand-pld` | black | red |
| iesdesk | `brand-iesdesk` | black | red |
| specquick | `brand-specquick` | black | red |
| emre güneş | `brand-memregunes` | black | red |

| Switch | Values | Where |
|---|---|---|
| Brand | one `brand-*` class from the table | `<body>`, required |
| Chrome | nothing for websites (top menu and footer); `site-sidebar-layout` on `<body>` for product UI only | `<body>` |
| Theme | `data-theme="dark"` (product UI only; same six colours, flipped) | `<html>` |
| Substrate | white paper by default; `paper-white` remains valid | `<body>` |

## Chrome

Chrome follows the screen family, not the brand: every website uses the top menu and the footer; product UI uses the sidebar. JavaScript only when it is the logical choice: drawers are native popovers with a `site-header__close` or `site-sidebar__close` button, groups and More are `details`, and `agustos-chrome.js` (load once with `defer`) closes More on Escape, an outside click, or focus leaving. Print drops the chrome. Copy the markup from `starter.html`.

- **Top menu** (`site-header*`, `site-footer*`): a sticky one-row header inside a `site-frame` with the lockup, `site-header__nav`, and a `site-header__end` slot for search, language, and the CTA; the kit styles the search (`site-header__search*`, a row under the bar below 1024px) and the `site-header__lang-link`. **At most five items**, about 65 characters together with More, so the row fits at 1024px. Put extra pages in one `site-header__more` `details` whose `summary` is a `site-header__link` ("Daha fazla" or "More") and whose `site-header__more-menu` holds `site-header__more-link` items. The footer is light: `site-footer__brand` holds the lockup and one `type-footnote` line; one `site-footer__links` list holds a single row of `site-footer__link` items for social, legal, and language. No button. An optional site map sits above that row: `site-footer__map` holds `site-footer__contact` (the lockup and an `address`: legal name and address) and one `site-footer__groups` nav of at most three `site-footer__group`s, each a sentence-case `site-footer__group-title` over at most five links in `site-footer__group-links`. List the pages people look for, not every page; `sitemap.xml` serves search engines. Below 1024px the burger opens `site-header__panel` as a drawer, and the More items open inline.
- **Sidebar** (`site-sidebar*`), product UI only: a fixed 240px column with the lockup, `site-sidebar__nav` links, `site-sidebar__group` details, a `site-sidebar__utility` slot, and a `site-sidebar__note`. Below 1024px a sticky `site-sidebar-bar` with the burger opens it as a drawer.
- **Lockup** (`site-lockup`): the exact Laz Güneşi symbol inline plus a lowercase wordmark. Never redraw the symbol; copy it from `starter.html`. Hover swaps its ink: Ağustos red to black, every other brand black to red.
- The current page carries `aria-current="page"` and the section that holds it (a parent item on a nested route) `aria-current="true"`: a 2px red rule underneath in the top menu, on the left in the sidebar; a More or a closed group that holds either carries the rule too. Breadcrumbs keep `page` only. Hover darkens the ink over a 1px gray rule. Every control is 44px.
- Destinations, copy, and columns are configuration. The kit styles them; it never decides them.

## Screens

One reference page per screen type lives in the source repository under `screens/`, hand-written on these classes. Build any page from the matching screen. Theme, chrome and column follow the family. **Column:** a content page (About, privacy, terms, an article, a list of posts) uses `<div class="container container--reading">`: its title, deck, headings and text start on the frame's left edge and stop at the reading line (`--measure-body`, 41rem, about 75 characters). The side zone to the right stays free for a side column, and the footer site map splits on the same line. Every other page uses the full frame and caps a text block with `prose`. Cap the column, not each paragraph; the checker warns on a full-width `container` on a content screen (AG028).

| Screen | Family | Chrome | Column | Theme | Photography |
|---|---|---|---|---|---|
| `home` | marketing | topbar | frame | light | one installation photograph, third in the rollout |
| `static` | content | topbar | reading | light | people and places that explain the work |
| `content` | content | topbar | reading | light | only when it explains the content |
| `content-index` | content | topbar | reading | light | none; titles stay type-only |
| `products` | catalog | topbar | frame | light | product thumbnails, second in the rollout |
| `product-finder` | catalog | topbar | frame | light | product thumbnails, second in the rollout |
| `product` | catalog | topbar | frame | light | product photograph or drawing, first in the rollout |
| `spec-sheet` | document | topbar | frame | light | product photograph and dimensioned drawing |
| `app-shell` | product UI | sidebar | frame | dark allowed | none |

A website page opens with a `type-hero` headline (or a `type-h1` on listing and content pages), a `type-hero-deck`, a `hero-actions` row with one primary and one secondary `agustos-button`, and a `hero-trust` line. It closes with one `band band--cream`.

**The highlighter.** Wrap one to four words of the main headline in `<mark class="type-highlight">`. Once per page (the checker warns, AG025). Never on links, buttons, numbers, body text, or product UI. The sentence must read the same without it.

**Emphasis.** `strong` (600) marks a fact the reader scans for, at most once per paragraph. `em` marks names of publications and projects, foreign terms, and quoted phrases. Underline is for links only. Never combine them. No uppercase labels, eyebrow headings, or coloured text.

**States.** The kit styles every state; compose from it rather than restyle. Hover: light paper turns a content link red; the dark theme dims the ink instead (red text on off-black is 3.35:1) and keeps the red rule. Pressed: buttons move 1px down. Disabled: the `disabled` attribute, or `aria-disabled="true"` on a link, turns a control gray and inert. The footer and the closing band stay light in the dark theme. Text clears 4.5:1 and borders, logos and focus 3:1 in both themes; `kit.json` (`states`) and `docs/web.html` carry every pair with its ratio.

`brand-memregunes` may show photographs of Emre Güneş on `home` and `static`.

## Classes

Every class the kit publishes. See `starter.html` for one rendered instance of each.

| Group | Classes |
|---|---|
| Frame | `site-frame` `container` `container--reading` `skip-link` |
| Layout | `stack` `cluster` `prose` `grid-2` `grid-3` `grid-4` `grid-aside` `band` `band--cream` `table-scroll` |
| Headings | `type-hero` `type-hero-md` `type-hero-deck` `type-h1` `type-h2` `type-h3` `type-h4` |
| Text | `type-body` `type-link` `type-code` `type-blockquote` `type-pullquote` `type-footnote` `type-highlight` |
| Blocks | `type-list-ul` `type-list-ol` `type-dl` `type-figure` `type-code-block` `type-table` `type-divider` |
| Hero | `hero-actions` `hero-trust` `hero-visual` |
| Sections | `agustos-section` `agustos-section__head` |
| Cards | `agustos-card-grid` `agustos-card` `agustos-card--marked` |
| Chrome | `agustos-chrome-link` · `site-lockup` `site-lockup__symbol` `site-lockup__name` · `site-sidebar-layout` `site-sidebar` `site-sidebar__nav` `site-sidebar__link` `site-sidebar__group` `site-sidebar__cta` `site-sidebar__utility` `site-sidebar__note` `site-sidebar-bar` `site-sidebar-burger` `site-sidebar__close` · `site-header` `site-header__bar` `site-header__panel` `site-header__nav` `site-header__link` `site-header__more` `site-header__more-menu` `site-header__more-link` `site-header__end` `site-header__cta` `site-header__burger` `site-header__close` · search and language: `site-header__utility` `site-header__utility--bar` `site-header__utility--drawer` `site-header__icon-btn` `site-header__theme-sun` `site-header__theme-moon` `site-header__lang-link` `site-header__search` `site-header__search--desktop` `site-header__search--responsive` `site-header__search-toggle` `site-header__search-panel` `site-header__search-field` `site-header__search-output` `site-header__search-status` `site-header__search-results` `site-header__search-group` `site-header__search-heading` `site-header__search-heading-count` `site-header__search-list` `site-header__search-result` `site-header__search-result-title` `site-header__search-result-excerpt` `site-header__search-row` `site-header__search-shell` `site-header__noscript-search` · `site-footer` `site-footer__inner` `site-footer__brand` `site-footer__links` `site-footer__link` `site-footer__map` `site-footer__contact` `site-footer__groups` `site-footer__group` `site-footer__group-title` `site-footer__group-links` · `breadcrumb` `breadcrumb__link` |
| Forms | `agustos-fieldset` `agustos-field` `agustos-field--invalid` · `agustos-label` `agustos-label--required` · `agustos-input` `agustos-textarea` `agustos-select` `agustos-check` `agustos-hint` `agustos-error` |
| Buttons | `agustos-button` `--primary` `--secondary` `--quiet` |
| Badges | `agustos-badge` `--success` `--warning` `--danger` `--info` `--signal` |
| Notices | `agustos-notice` `agustos-notice__title` `--success` `--warning` `--danger` `--info` |
| Tabs | `agustos-tabs` `agustos-tab` `agustos-tabs__panel` |

Bare HTML elements are styled too: `h1`–`h4`, `p`, `a`, `ul`, `ol`, `dl`, `table`, `blockquote`, `pre`, `code`, `hr`. Semantic markup gets the right result without classes.

Compose missing components from `agustos-card`, `agustos-button`, the layout classes, and `type-*`. `prose` caps a text block at the reading line on a full-frame page; `container--reading` caps the whole column of a content page. Do not import another component library.

## Variables

Use `var(--name)`, never the literal value. Spacing `--space-2xs` … `--space-6xl`.
Radii `--radius-md` (6px, controls) and `--radius-lg` (12px, cards). `--radius-sm` is an alias of `--radius-md`. Nothing larger exists.
Color `--paper` `--cream` `--surface` `--ink` `--ink-soft` `--ink-faint` `--rule` `--signal` `--brand`
`--footer-*` `--state-success|warning|danger|info`. Type `--display` `--body` `--mono`; sizes follow one golden scale (13, 16.5, 21, 27, 34, 43, 55, 70, 89px). Section spacing `--section-space`.
Motion `--dur` `--ease`. Targets `--control-min` (44px). Frame `--measure-content` (1180px). Product sidebar `--sidebar-width` (240px) and `--sidebar-bar-height` (61px, the sticky bar below 1024px; the kit sets it as `scroll-padding-top`, so an anchor lands below the bar).
Measures `--measure-text` (54ch, hero deck) and `--measure-body` (41rem, the reading line: long-form prose, and the split of a content page and the footer site map).

`ui/kit.json` carries the same lists in machine-readable form, plus the brand and screens tables.

## Hard rules

1. **Never retype a token value.** Use `var(--signal)`, not `#cf142a`.
2. **Brand red is `#cf142a`.** `#D11D2B` is stale — fix it wherever you find it.
3. **Never restyle a kit class.** Overriding `.agustos-card` breaks every other page. Compose a new class.
4. **Radii are 6 and 12px.** Nothing rounder. No pills, no blobs, no gradients.
5. **44px minimum for anything clickable.** `--control-min` exists for this. Links inside running text are exempt. Put a card's main link directly in its `h2`, `h3` or `h4`: the kit stretches that link over the card, so the whole card is the target. The checker warns (AG013) when a card's links all sit outside a heading.
6. **Never redraw the Laz Güneşi symbol.** Copy the `site-lockup` markup from `starter.html`.
7. **Websites use the top menu; product UI uses the sidebar.** At most five top-menu items; the rest go under More. The checker warns on a sidebar outside product UI (AG026) and on a sixth top-menu item (AG027).

## Verify before you call it done

```bash
python3 vendor/agustos-ui/check-agustos-ui.py .
```

Fix reported token values, font loading, CDN pins, brand classes, radii, and class overrides.
Every page must carry `data-screen="<name>"` on `<body>`. Errors guard identity: token values, the brand red, font loading, CDN pins, brand classes, and screen names. Taste rules only warn: `data-theme` outside product UI (AG024), more than one highlighter (AG025), a sidebar on a website (AG026), more than five top-menu items (AG027), and, on built pages (`--screens-only`), `aria-current="page"` on a parent section (AG029), radii, gradients, and class overrides.
If a layout fills `data-screen` at render time (Astro, ERB), the source scan skips those rules. Build the site, then run `python3 vendor/agustos-ui/check-agustos-ui.py dist --screens-only` on the output folder.
Use `--strict` to fail on warnings; use `--json` for structured output. Exit 0 confirms automated checks passed.
Use `--skip <dir>` (repeatable) for frozen or generated folders the project must not edit. Do not hand-edit the checker; it is regenerated with the kit.
Check for a newer kit with `python3 vendor/agustos-ui/check-agustos-ui.py --update-check`.

## If you need more than this file

- `kit.json` — the same contract, machine-readable, with file hashes.
- `starter.html` — every class, rendered once, including the top menu, the footer and the product sidebar.
- `screens/` in the source repository — one reference page per screen type.
- `tokens/design-system-handoff.json` in the source repository — the full cross-medium contract with the embedded symbol.

Source: `Agustos-Teknoloji/DESIGN-agustos` · licensed under `ui/LICENSE`.
