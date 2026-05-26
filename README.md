# Ağustos Design System

Typography-first design system for Emre Güneş's multi-brand portfolio.

The canonical specification is [DESIGN.md](DESIGN.md). A rendered HTML preview lives at [artifacts/agustos-design-system-v2.1.1.html](artifacts/agustos-design-system-v2.1.1.html).

This repository is intentionally platform-neutral. Astro, Rails, and future implementations are adapters of the same system, not separate design systems.

## What is included

- `DESIGN.md`: canonical design-system specification.
- `MEMORY.md`: decision history and reasoning.
- `tokens/agustos.css`: platform-neutral CSS token source.
- `adapters/astro/`: Astro adapter, demo implementation, and typography showcase.
- `adapters/rails/`: Rails monolith adapter skeleton.
- `laz-gunesi-amblem/`: Laz Güneşi symbol source and exported assets.
- `artifacts/`: rendered design explorations and previews.

## Adapter Strategy

Use the design system through the adapter that matches the application:

- Rails monoliths should start from `adapters/rails/`.
- Astro/static sites should start from `adapters/astro/`.
- Shared CSS changes should begin in `tokens/agustos.css`, then be mirrored into adapter copies.

Astro is a reference implementation, not the canonical center of the system.

## Astro Preview

```bash
cd adapters/astro
npm install
npm run dev
```

To regenerate the standalone HTML preview from `DESIGN.md`:

```bash
cd adapters/astro
node scripts/render-design-html.mjs
```

## Rails Usage

Copy the Rails adapter files into a Rails app:

```txt
adapters/rails/app/assets/stylesheets/agustos/
adapters/rails/app/helpers/agustos_theme_helper.rb
adapters/rails/app/views/layouts/agustos.html.erb
adapters/rails/app/views/agustos/shared/
```

Then use `layout "agustos"` from Rails controllers. See [adapters/rails/README.md](adapters/rails/README.md).
