# Ağustos Astro Adapter v3.0.0

Astro 5 reference implementation for the [Ağustos Design System](../../DESIGN.md).

This adapter is useful for static sites, documentation, marketing pages, and visual QA. It is not the canonical center of the system; shared design decisions live in `DESIGN.md` and shared token CSS starts in `../../tokens/agustos.css`.

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
    │   ├── LazGunesi.astro
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
    cta: { href: '/contact', label: 'Contact' },
    languageSwitch: { href: '/tr', label: 'Türkçe', code: 'TR' },
  }}
  footer={{
    description: 'Pataraz · project-grade lighting',
    columns: [{ heading: 'Company', links: [{ href: '/about', label: 'About' }] }],
  }}
>
  ...
</BaseLayout>
```

Set `searchable={false}` to exclude a page. Blog detail pages should pass
`searchKind="post"`; other pages default to `"page"`. Set
`header={{ search: false }}` to remove search from the chrome.

Regenerate the standalone HTML preview from `DESIGN.md`:

```bash
node scripts/render-design-html.mjs
```

## Token Sync

The Astro token file mirrors the platform-neutral source:

```txt
../../tokens/agustos.css
src/styles/tokens.css
```

Token bodies should stay byte-identical except for header comments and framework-specific wrappers.

## Brands

Every page can declare one of four brands via `BaseLayout`:

```astro
<BaseLayout brand="pataraz" title="Pataraz">
  ...
</BaseLayout>
```

Available brand ids:

- `agustos`
- `pataraz`
- `pld`
- `photo`

## Substrates

Cream is the default branded substrate. White is available for working contexts:

```astro
<BaseLayout substrate="white" title="Working Page">
  ...
</BaseLayout>
```

Dark theme is an opt-in user preference layer through `html[data-theme="dark"]`.

## Turkish Locale

Set `lang="tr"` for Turkish pages:

```astro
<BaseLayout lang="tr" title="Ağustos">
  ...
</BaseLayout>
```

The design system depends on `lang="tr"` plus `font-feature-settings: "locl"` for correct Turkish uppercase behavior.

## Scope

This adapter demonstrates all 24 typography tokens and the v3 topbar/footer chrome. Rails monoliths should use `../rails/` instead of copying Astro components.
