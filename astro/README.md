# Ağustos Astro

A working Astro 5 reference site implementing the [Ağustos Design System v1.7](../DESIGN.md), typography-first, multi-brand, cream-paper-by-default. Logotype in Plus Jakarta Sans Light; symbol is the real Laz Güneşi.

## What's inside

```
astro/
├── astro.config.mjs        Astro 5 config. MDX, sitemap
├── package.json            Astro, fonts, MDX, sitemap, TS
├── public/
│   └── favicon.svg         Laz Güneşi (default brand: red)
├── src/
│   ├── components/
│   │   ├── LazGunesi.astro       Publisher's mark; 18-blade Laz Güneşi
│   │   ├── BrandLockup.astro     Symbol + lowercase wordmark in Plus Jakarta Sans Light
│   │   ├── Header.astro          Site nav
│   │   └── Footer.astro          Publisher attribution
│   ├── content.config.ts         Blog content collection (zod-typed)
│   ├── content/
│   │   └── blog/                 Sample posts (one EN, one TR)
│   ├── layouts/
│   │   └── BaseLayout.astro      Brand class, lang, substrate, font imports
│   ├── pages/
│   │   ├── index.astro           Home
│   │   ├── about.astro           Portfolio overview
│   │   ├── typography.astro      All 22 tokens on one page + brand switcher
│   │   └── blog/
│   │       ├── index.astro       Post list
│   │       └── [...slug].astro   Post detail
│   └── styles/
│       └── tokens.css            ⭐ The system; 12 vars, 22 tokens, 3 stacks
```

## Run it

**One-click (macOS):** double-click `start-dev.command` in this folder. It handles `npm install` if needed, starts the dev server, and opens `http://localhost:4321` in your browser.

**Manual:**

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static output to dist/
npm run preview  # serve the build locally
```

## How brand switching works

Every page declares one of four brands via `BaseLayout`'s `brand` prop:

```astro
<BaseLayout brand="pataraz">
  ...
</BaseLayout>
```

That sets the body class to `brand-pataraz`, which redefines `--brand` to `#1a24cc`. The link colour follows automatically, and per Rule 5 of the system, the link is the *only* place brand colour appears. Everything else is ink on paper.

Available brands: `agustos` (default), `pataraz`, `pld`, `photo`.

## How substrate switching works

For working/UI/email contexts (where the cream warmth would feel out of place):

```astro
<BaseLayout substrate="white">
  ...
</BaseLayout>
```

That swaps `--paper` to `#ffffff` and `--rule` to the white-paper variant. Same tokens, same rules, only the substrate changes.

## How Turkish content works

Set `lang="tr"` at the layout level for whole-page Turkish content:

```astro
<BaseLayout lang="tr" title="...">
  ...
</BaseLayout>
```

…or on individual elements when mixing languages:

```html
<p lang="tr"><strong>başlık</strong> denemesi</p>
```

The global `font-feature-settings: "locl"` rule and the `lang` attribute together ensure `text-transform: uppercase` produces `İ` (not `I`) for lowercase `i`. This is non-negotiable, without it, every uppercase Turkish heading is silently wrong.

## Adding a new brand

Per the spec, ~30 minutes:

1. Add the colour to `:root` in `src/styles/tokens.css`:
   ```css
   --brand-newbrand: #refinedhex;
   ```
2. Add the brand class:
   ```css
   .brand-newbrand { --brand: var(--brand-newbrand); }
   ```
3. Extend the `Brand` union in `src/layouts/BaseLayout.astro` and the `brand` enum in `src/content.config.ts`.

That's it. No new typography, no new logo work, no new tokens.

## Adding a new post

Drop a markdown (or `.mdx`) file into `src/content/blog/`:

```markdown
---
title: A new post
deck: Optional sub-headline.
date: 2026-06-01
lang: en        # or 'tr'
brand: agustos  # any of the four
---

Body markdown here. The 22 tokens map directly to standard markdown elements
(see DESIGN.md §"Markdown coverage"), so just write naturally.
```

## What this implementation does

- **All 22 tokens** are present in `tokens.css` and exercised on `/typography`.
- **All four brands** are wired up; switch live on the typography page or at layout level.
- **Both substrates** (cream and white) are supported via one CSS-variable swap.
- **Turkish locale** correctness. `locl` is on globally, layout accepts `lang`, sample post uses `lang="tr"`.
- **Self-hosted fonts** via `@fontsource-variable/newsreader` (variable, opsz axis), `@fontsource/source-sans-3`, `@fontsource/jetbrains-mono`, and `@fontsource-variable/plus-jakarta-sans` (logotype only).
- **Markdown content** flows through the system. H1–H4, blockquote, lists, code, tables all inherit token rules.

## What this implementation does *not* do

- **Pandoc / docx / PDF templates.** The spec mentions these as future companions to the web rendering. They're scoped out of this Astro starter; they'd live alongside it.
- **Per-brand homepages.** The demo is wired for Ağustos. To stand up Pataraz, PLD, or Photometric as full sites, duplicate the page tree under their brand class (or split into separate Astro projects sharing `tokens.css`).

## Reference

The canonical spec is `../DESIGN.md`. Decision history lives in `../MEMORY.md` (when authored). When the spec and this code diverge, the spec wins, open an issue and align the code.
