# Ağustos Astro Adapter

Astro 5 reference implementation for the [Ağustos Design System](../../DESIGN.md).

This adapter is useful for static sites, documentation, marketing pages, and visual QA. It is not the canonical center of the system; shared decisions live in `../../tokens/design-tokens.json` and `DESIGN.md`.

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
    │   ├── LazGunesi.astro
    │   └── Header.astro
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

White is the reference-site default. Cream remains available for explicitly branded editorial contexts:

```astro
<BaseLayout substrate="cream" title="Branded Editorial Page">
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

This adapter demonstrates the v3 type tokens, one-row chrome, shared frame, editorial opening, restrained card groups, and section rhythm. Rails monoliths should use `../rails/` instead of copying Astro components.
