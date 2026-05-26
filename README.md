# Ağustos Design System

Typography-first design system for Emre Güneş's multi-brand portfolio.

The canonical specification is [DESIGN.md](DESIGN.md). A rendered HTML preview lives at [artifacts/agustos-design-system-v2.1.1.html](artifacts/agustos-design-system-v2.1.1.html).

## What is included

- `DESIGN.md`: canonical design-system specification.
- `MEMORY.md`: decision history and reasoning.
- `astro/`: Astro implementation and typography showcase.
- `laz-gunesi-amblem/`: Laz Güneşi symbol source and exported assets.
- `artifacts/`: rendered design explorations and previews.

## Local preview

```bash
cd astro
npm install
npm run dev
```

To regenerate the standalone HTML preview from `DESIGN.md`:

```bash
cd astro
node scripts/render-design-html.mjs
```

