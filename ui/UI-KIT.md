# Ağustos UI kit — v5.0.0

Read this complete interface contract before building for an Ağustos-family brand. You do not need to open `DESIGN.md`.

Use the generated registry values. Request missing values instead of inventing them.

## Design direction — İskandivvian

Scandinavian restraint filtered through Mediterranean warmth.

Create minimal, functional, and elegant interfaces that feel warm and human.
İskandivvian is our project label. Keep the experience welcoming and easy to use.

- White is the primary substrate (~70% of every surface); cream is a full-bleed callout/CTA-band tint only, never the page paper.
- Make every section useful. Keep navigation, information, and next actions easy to understand.
- Use clear hierarchy and one alignment frame. Let spacing explain relationships without hiding useful content.
- Use modest corners and selective borders. Flat surfaces — no shadows anywhere.
- Use authentic imagery only when it explains people, places, products, or work. Preserve product colors and technical facts.
- Keep text, controls, and technical tables on plain surfaces. Flat pages without imagery are a complete expression.
- Retain registered logos, font families, red interaction signals, supported themes, and accessible contrast.
- Write direct, helpful copy with familiar words. Explain practical benefits and next steps. Sentence case everywhere — no uppercase labels, eyebrows, or headers.

Avoid:

- Ornamental Mediterranean motifs or unrelated lifestyle imagery
- Replacing red interaction signals with earthy accent colors
- Low-contrast text, vague labels, excessive whitespace, or decorative motion
- Inflated luxury claims, forced friendliness, uppercase text, or any shadow
- Cream used as a page substrate, an inset rounded card, or mixed with a gray band on the same page

## Install — production

Copy these into `vendor/agustos-ui/` in your project and commit them:

    agustos.css
    agustos-fonts.css
    fonts/                 (5 woff2 files + 3 OFL.txt — the licenses must travel with them)
    check-agustos-ui.py
    UI-KIT.md

Then load the two stylesheets, **fonts first**:

```html
<link rel="stylesheet" href="/vendor/agustos-ui/agustos-fonts.css">
<link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">
```

Vendoring removes runtime CDN dependencies and supports local bundling.

**npm projects may skip `agustos-fonts.css`** and install the fonts instead:

```
npm i @fontsource-variable/inter-tight @fontsource-variable/inter @fontsource-variable/jetbrains-mono
```

## Install — prototypes only

For a throwaway mockup with no build step:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@v5.0.0/ui/agustos-fonts.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@v5.0.0/ui/agustos.css">
```

**Pin stylesheet URLs to `@v5.0.0`.** Never publish `@main` or `@latest`; upstream changes can restyle your page.

## One warning before you start

`agustos.css` styles the whole page, including bare HTML elements.
**Do not combine it with Bootstrap, Tailwind preflight, or another page stylesheet.** Their rules can conflict.

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
<body class="brand-agustos">
  <a class="skip-link" href="#main">İçeriğe geç</a>
  <main id="main" class="container">
    <!-- your page -->
  </main>
</body>
</html>
```

Use `lang="tr"` for Turkish content so locale-sensitive capitalization renders correctly.

## Brand, substrate, theme

| Switch | Values | Where |
|---|---|---|
| Brand | `brand-agustos` · `brand-pataraz` · `brand-pld` · `brand-iesdesk` · `brand-specquick` | `<body>`, required |
| Substrate | white by default; `band-cream` for a full-bleed callout/CTA band only, never a page or an inset card; `paper-white` is a no-op kept for back-compat | `<body>`/section |
| Theme | `data-theme="dark"` (opt-in) | `<html>` |

Ağustos alone owns red identity ink. Other house brands use black or white.
Shared red (`#cf142a`) signals links, focus, markers, and small emphasis. Never recolor another house-brand logo red.

## Classes

Every class the kit publishes. See `starter.html` for one rendered instance of each.

| Group | Classes |
|---|---|
| Frame | `site-frame` `container` `skip-link` |
| Headings | `type-hero` `type-hero-md` `type-hero-deck` `type-h1` `type-h2` `type-h3` `type-h4` |
| Text | `type-body` `type-link` `type-code` `type-blockquote` `type-pullquote` `type-footnote` |
| Blocks | `type-list-ul` `type-list-ol` `type-dl` `type-figure` `type-code-block` `type-table` `type-divider` |
| Hero | `hero-actions` `hero-action` `hero-action--primary` `hero-action--secondary` · `hero-links` `hero-link` `hero-link--primary` `hero-link--secondary` · `hero-trust` `hero-visual` |
| Sections | `agustos-section` `agustos-section__head` |
| Cards | `agustos-card-grid` `agustos-card` `agustos-card--marked` |
| Chrome | `agustos-chrome-link` |
| Forms | `agustos-fieldset` `agustos-field` `agustos-field--invalid` · `agustos-label` `agustos-label--required` · `agustos-input` `agustos-textarea` `agustos-select` `agustos-check` `agustos-hint` `agustos-error` |
| Buttons | `agustos-button` `--primary` (filled, committing) `--secondary` (outline, alternative) — no third tier |
| Badges | `agustos-badge` `--success` `--warning` `--danger` `--info` `--signal` |
| Notices | `agustos-notice` `agustos-notice__title` `--success` `--warning` `--danger` `--info` |
| Tabs | `agustos-tabs` `agustos-tab` `agustos-tabs__panel` |

Bare HTML elements are styled too: `h1`–`h4`, `p`, `a`, `ul`, `ol`, `dl`, `table`,
`blockquote`, `pre`, `code`, `hr`. Semantic markup gets the right result without classes.

Compose missing components from `agustos-card`, `agustos-button`, and `type-*` classes. Do not import another component library.

## Variables

Use `var(--name)`, never the literal value. Spacing `--space-2xs` … `--space-6xl`.
Radii `--radius-sm` (4px) `--radius-md` (6px) `--radius-lg` (10px) — nothing larger exists.
Color `--paper` `--ink` `--ink-soft` `--ink-faint` `--rule` `--signal` `--brand`
`--state-success|warning|danger|info`. Type `--display` `--body` `--mono`.
Motion `--dur` `--ease`. Targets `--control-min` (44px). Frame `--measure-content` (920px).

`ui/kit.json` carries the same list in machine-readable form.

## Hard rules

1. **Never retype a token value.** Use `var(--signal)`, not `#cf142a`.
2. **Brand red is `#cf142a`.** `#D11D2B` is stale — fix it wherever you find it.
3. **Never restyle a kit class.** Overriding `.agustos-card` breaks every other page. Compose a new class.
4. **Radii are 4, 6, and 10px.** Nothing rounder. No pills, no blobs, no gradients.
5. **44px minimum for anything clickable.** `--control-min` exists for this.
6. **Never redraw the Laz Güneşi symbol.** If you need the logo and do not have the file, request it.

## Verify before you call it done

```bash
python3 vendor/agustos-ui/check-agustos-ui.py .
```

Fix reported token values, font loading, CDN pins, brand classes, radii, and class overrides.
Use `--strict` to fail on warnings; use `--json` for structured output. Exit 0 confirms automated checks passed.

## Check for a newer kit

```bash
python3 vendor/agustos-ui/check-agustos-ui.py --update-check
```

## If you need more than this file

- `kit.json` — the same contract, machine-readable, with file hashes.
- `starter.html` — every class, rendered once.
- `tokens/design-system-handoff.json` in the source repository — the full cross-medium contract with the embedded symbol.

Source: `Agustos-Teknoloji/DESIGN-agustos` · licensed under `ui/LICENSE`.
