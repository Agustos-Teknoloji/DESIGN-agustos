# Ağustos Design System

Cross-medium design system for Ağustos and its house brands. `agustos.com` is the design laboratory and reference implementation; this repository is the authority.

The system preserves the established identity—Laz Güneşi, lowercase wordmarks, Inter Tight + Inter—while separating identity ink from interaction: Ağustos alone is red, every other house brand is black/white, and shared red signals links, focus, and small emphasis everywhere.

## Architecture

Four layers separate durable decisions from platform syntax:

1. **Foundations:** color, typography, spacing, measure, radii, and motion.
2. **Semantic roles:** paper, surface, ink, muted ink, rule, brand signal, focus, display, body, and data.
3. **Recipes:** chrome, hero, section opening, editorial link, card, data table, document, and presentation.
4. **Adapters:** Astro, WordPress, Rails, PowerPoint, and Word/Google Docs.

Hand-edit these sources:

- `tokens/design-tokens.json` — canonical cross-medium design registry.
- `tokens/design-system-handoff.json` — generated, self-contained contract to give another coding system. This is the primary integration artifact.
- `brand/brands.json` — canonical brand identity registry.
- `tokens/web.css.tmpl` — platform-neutral web behavior and compatibility classes.
- `DESIGN.md` — human-readable specification and governance.
- `MEMORY.md` — decision history.

Everything under `brand/exports/` and all generated token/adapter files are outputs. Consumer deployments use the checked-in handoff or adapter; they never regenerate this repository's artifacts.

## Generate and verify

```bash
python3 scripts/build_design_system.py
python3 scripts/build_design_system.py --check
python3 scripts/check_office_artifacts.py --check
python3 -m unittest discover -s tests
```

The generator writes:

- `tokens/agustos.css` and `tokens/resolved.json`
- `tokens/design-system-handoff.json`, the portable machine-readable implementation contract
- Astro and Rails token CSS
- WordPress `theme.json` and CSS
- `tokens/generated-manifest.json`, including content hashes for drift detection
- `brand/exports/office-manifest.json`, covering nine Office artifacts and their generator sources

Office artifacts consume `tokens/resolved.json`:

```bash
python3 brand/build_templates.py --brand agustos
```

PowerPoint generation uses the plain-ESM `brand/build_presentation.mjs` source and the declared public `pptxgenjs` dependency. Word output includes both a compact letterhead and a styled document template suitable for import into Google Docs.

## Adapters

- [Astro](adapters/astro/README.md): reference web implementation and visual QA surface.
- [Rails](adapters/rails/README.md): topbar, shared frame, helpers, and ERB partials for a monolith.
- [WordPress](adapters/wordpress/README.md): generated Global Styles plus the shared recipe layer.
- [Office](brand/templates/README.md): PowerPoint/Google Slides and Word/Google Docs translation.

Brand assets are indexed in [ASSETS.md](ASSETS.md). Automated agents should begin with [AGENTS.md](AGENTS.md).
