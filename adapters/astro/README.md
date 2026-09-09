# Ağustos Astro Adapter

Astro 5 reference implementation for the [Ağustos Design System](../../DESIGN.md) v5.0.1.

This adapter is useful for static sites, documentation, marketing pages, and visual QA. It is not the canonical center of the system; shared decisions live in `../../tokens/design-tokens.json` and `DESIGN.md`.

> Building a UI in a repository that is not one of these adapters? Use the distribution kit
> at [`ui/UI-KIT.md`](../../ui/UI-KIT.md) instead — it needs no framework integration.

## What's Inside

```txt
adapters/astro/
├── astro.config.mjs
├── package.json
├── public/favicon.svg
├── scripts/render-design-html.mjs
└── src/
    ├── components/
    │   ├── BrandLockup.astro
    │   ├── Footer.astro
    │   ├── Header.astro
    │   ├── HeaderSearch.astro
    │   ├── HeaderUtility.astro
    │   └── LazGunesi.astro
    ├── types/chrome.ts
    ├── content/blog/
    ├── layouts/BaseLayout.astro
    ├── pages/
    │   ├── index.astro
    │   ├── about.astro
    │   ├── typography.astro
    │   └── blog/
    └── styles/tokens.css
```

## Run It

```bash
npm install
npm run dev
```

Build and preview:

```bash
npm run build
npm run preview
```

The production build runs Pagefind after Astro and verifies that the generated
index can be queried with the header's language and page/post filters.

## Chrome Configuration

`BaseLayout` accepts semantic `header` and `footer` configuration. Destinations
and copy are consumer data; spacing, states, responsive behavior, and typography
belong to the adapter.

```astro
<BaseLayout
  title="Pataraz"
  brand="pataraz"
  header={{
    homeHref: '/',
    nav: [{ href: '/products', label: 'Products' }],
    cta: { href: '/contact', label: 'Request pricing' },
    languageSwitch: { href: '/tr', label: 'Türkçe', code: 'TR' },
  }}
  footer={{
    description: 'Pataraz · project-grade lighting',
    columns: [{ heading: 'Company', links: [{ href: '/about', label: 'About' }] }],
    cta: { href: '/contact', label: 'Contact' },
  }}
>
  ...
</BaseLayout>
```

Set `searchable={false}` to exclude a page. Blog detail pages should pass
`searchKind="post"`; other pages default to `"page"`. Set
`header={{ search: false }}` to remove search from the chrome.

Marketing headers do not include a theme toggle. Product UI may pass
`header={{ theme: true }}` and, if the page itself is dark,
`theme="dark"` on `BaseLayout`.

Regenerate the standalone HTML preview from `DESIGN.md`:

```bash
node scripts/render-design-html.mjs
```

## Token Generation

The Astro token file is generated alongside every other web adapter:

```txt
../../tokens/design-tokens.json
src/styles/tokens.css
```

Run `python3 scripts/build_design_system.py` from the repository root. CI uses `--check` to reject drift.

## Brands

Every page can declare one of five brands via `BaseLayout`:

```astro
<BaseLayout brand="pataraz" title="Pataraz">
  ...
</BaseLayout>
```

Available brand ids:

- `agustos`
- `pataraz`
- `pld`
- `iesdesk`
- `specquick`

## Substrates and theme

White is the page paper. Cream is a full-bleed callout or CTA band, not a page substrate.

```astro
<section class="cta-band">
  ...
</section>
```

Dark theme is for product UI through `html[data-theme="dark"]`. Marketing, catalog, and spec pages stay light. They do not ship a theme toggle. The typography showcase includes a handbook inspect control; that is not a marketing pattern.

## Composition

Name one committing destination per page. That destination may appear in the header, the opening, and one closing cream band. Do not put a primary button in intervening sections. Footer Contact is separate chrome.

Photographs roll out in this order: product page, listing thumbnail, homepage installation. Type-only pages stay complete. Quotes belong on content pages only. Marketing uses a compact trust line.

## Turkish Locale

Set `lang="tr"` for Turkish pages:

```astro
<BaseLayout lang="tr" title="Ağustos">
  ...
</BaseLayout>
```

The design system depends on `lang="tr"` plus `font-feature-settings: "locl"` for correct Turkish uppercase behavior.

## Scope

This adapter demonstrates the v5.0.1 type tokens, one-row chrome, shared frame, editorial opening, filled-plus-outline actions, cream closing band, restrained card groups, and section rhythm. Rails monoliths should use `../rails/` instead of copying Astro components.
