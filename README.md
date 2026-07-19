# Ağustos Design System

Typography-first design system for Emre Güneş's multi-brand portfolio.

The canonical specification is [DESIGN.md](DESIGN.md). A rendered HTML preview lives at [artifacts/agustos-design-system-v3.0.0.html](artifacts/agustos-design-system-v3.0.0.html). Every brand asset — logo, symbol, favicon, colors, fonts — is indexed in [ASSETS.md](ASSETS.md); agents should start at [AGENTS.md](AGENTS.md).

This repository is intentionally platform-neutral. Astro, Rails, and future implementations are adapters of the same system, not separate design systems.

## What is included

- `ASSETS.md`: **canonical index of every brand asset** (logo, symbol, favicon, colors, fonts). Start here to find a file.
- `AGENTS.md`: entry point for automated agents working in this repo.
- `DESIGN.md`: canonical design-system specification.
- `MEMORY.md`: decision history and reasoning.
- `tokens/agustos.css`: platform-neutral CSS token source.
- `adapters/astro/`: Astro adapter, demo implementation, and typography showcase.
- `adapters/rails/`: Rails monolith adapter skeleton.
- Configurable v3 site chrome: sticky topbar, responsive drawer/search, and structured footer in both adapters.
- `laz-gunesi-amblem/`: Laz Güneşi symbol source, exported assets, and the favicon/app-icon kit (`favicon/`).
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
