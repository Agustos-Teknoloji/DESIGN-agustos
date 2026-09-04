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
- `ui/`, the distribution kit (see below)
- `brand/exports/office-manifest.json`, covering nine Office artifacts and their generator sources

Web fonts are generated separately, because subsetting needs `fonttools[woff2]` and CI does not
install it. Run it only when the master fonts in `brand/fonts/` change:

```bash
./.venv/bin/python scripts/build_ui_fonts.py
```

Office artifacts consume `tokens/resolved.json`:

```bash
python3 brand/build_templates.py --brand agustos
```

PowerPoint generation uses the plain-ESM `brand/build_presentation.mjs` source and the declared public `pptxgenjs` dependency. Word output includes both a compact letterhead and a styled document template suitable for import into Google Docs.

## Distribution kit

`ui/` is what another repository consumes. It is generated; do not hand-edit anything in it except
`UI-KIT.md.tmpl`, `starter.html.tmpl`, `check-agustos-ui.py.tmpl`, `AGENTS-SNIPPET.md.tmpl`, and
`LICENSE`.

| File | Purpose |
|---|---|
| `UI-KIT.md` | The entry point. One file, 162 lines, sufficient on its own. |
| `agustos.css` | The stylesheet. Byte-identical to `tokens/agustos.css` apart from its header. |
| `agustos-fonts.css` + `fonts/` | Self-hosted Inter Tight, Inter, and JetBrains Mono. **Required** — the stylesheet declares font stacks, not faces. |
| `starter.html` | Every published class, rendered once. |
| `kit.json` | The same contract, machine-readable, with file hashes. |
| `check-agustos-ui.py` | Compliance checker a consuming project runs to prove it complied. |
| `AGENTS-SNIPPET.md` | The stanza a consuming repository pastes into its own `AGENTS.md`. |

Two ways to consume it:

- **Production** — copy `ui/` into `vendor/agustos-ui/` and commit it. No runtime dependency on a
  third-party CDN, and the bundler can process the CSS normally.
- **Prototypes** — link the version-pinned CDN URLs in `UI-KIT.md`. Never `@main` or `@latest`: an
  unpinned link restyles a live page the moment a token changes, with no review.

Preview it locally with the `agustos-ui-kit` entry in `.claude/launch.json`, or:

```bash
python3 -m http.server 4330 --directory ui
```

Any change under `ui/` requires a VERSION bump, a rebuild, and a matching `v<VERSION>` git tag in the
same change. `VERSION` participates in the manifest's source hash, so CI fails if the rebuild is
missed.

## Adapters

- [Astro](adapters/astro/README.md): reference web implementation and visual QA surface.
- [Rails](adapters/rails/README.md): topbar, shared frame, helpers, and ERB partials for a monolith.
- [WordPress](adapters/wordpress/README.md): generated Global Styles plus the shared recipe layer.
- [Office](brand/templates/README.md): PowerPoint/Google Slides and Word/Google Docs translation.

Brand assets are indexed in [ASSETS.md](ASSETS.md). Automated agents should begin with
[AGENTS.md](AGENTS.md), which routes each task to the smallest authoritative set of files without
loading the entire repository into context.

The frozen, standalone v3.0.0 specification is available at
[`artifacts/agustos-design-system-v3.0.0.html`](artifacts/agustos-design-system-v3.0.0.html).

## License

Copyright © 2026 Ağustos Teknoloji. This repository is proprietary and all rights are reserved.
See [LICENSE](LICENSE) for the complete terms.

**Exception:** `ui/` and `tokens/` — the distribution kit — are licensed permissively under
[`ui/LICENSE`](ui/LICENSE) so other parties can build interfaces with the system. Every brand name,
wordmark, logo, and the Laz Güneşi symbol remain reserved, as does everything under `brand/exports/`.
Fonts in `ui/fonts/` are SIL Open Font License 1.1.
