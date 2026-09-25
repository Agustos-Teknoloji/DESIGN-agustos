# Ağustos Design System

Cross-medium design system for Ağustos and its house brands. `agustos.com` is the design laboratory and reference implementation; this repository is the authority.

The system preserves the established identity—Laz Güneşi, lowercase wordmarks, Inter Tight + Inter—while separating identity ink from interaction: Ağustos alone is red, every other house brand is black/white, and shared red signals links, focus, and small emphasis everywhere.

## Design direction

**İskandivvian: Scandinavian restraint filtered through Mediterranean warmth.**

Create minimal, functional, and elegant experiences that feel calm, welcoming, and human.
Express warmth through comfortable spacing, clear typography, existing neutral surfaces, and direct language.
Keep the experience welcoming and easy to use.

`DESIGN.md` defines the rules. `tokens/design-tokens.json` holds the portable `designDirection` contract.
The generator publishes this contract in the handoff, resolved registry, and UI kit.
The current release is in `VERSION`. [CHANGELOG.md](CHANGELOG.md) lists what each release changed, with a Migration section for each major version.

## Architecture

The layers, the hand-edited sources, the generated outputs and the tests are in [ARCHITECTURE.md](ARCHITECTURE.md).

## Generate and verify

Run `bin/setup` once in each new clone. It activates the pre-push hook in `.githooks/`.
The hook runs `scripts/ci.sh`, the local gate, and refuses a push that fails it.

After an everyday source change, refresh the kit. Do not rebuild logos, Office files, or fonts
unless someone asks.

```bash
python3 scripts/build_design_system.py
python3 scripts/build_design_system.py --check
python3 -m unittest discover -s tests
```

Run `scripts/ci.sh` to run the full gate by hand.

The five standard artifacts are [DESIGN.md](DESIGN.md), [docs/fonts.html](docs/fonts.html), [docs/colour.html](docs/colour.html), [docs/web.html](docs/web.html), and [docs/brands.html](docs/brands.html).

The everyday command writes `ui/` and the matching token CSS. Adapter CSS and the handoff JSON
travel with that same command. Logos, Office templates, webfonts, and datasheets do not.

A full rebuild is manual. Run it only when asked:

```bash
./.venv/bin/python brand/build.py
./.venv/bin/python brand/build_templates.py
./.venv/bin/python scripts/build_ui_fonts.py
python3 brand/build_datasheet.py --pdf
python3 scripts/check_office_artifacts.py --check
```

## Distribution kit

`ui/` is what another repository consumes. It is generated; do not hand-edit anything in it except
`UI-KIT.md.tmpl`, `starter.html.tmpl`, `check-agustos-ui.py.tmpl`, `AGENTS-SNIPPET.md.tmpl`, and
`LICENSE`.

| File | Purpose |
|---|---|
| `UI-KIT.md` | The entry point. One compact contract, sufficient on its own. |
| `agustos.css` | The stylesheet. Byte-identical to `tokens/agustos.css` apart from its header. |
| `agustos-fonts.css` + `fonts/` | Self-hosted Inter Tight, Inter, and JetBrains Mono. **Required** — the stylesheet declares font stacks, not faces. |
| `starter.html` | Every published class, rendered once, including both chromes and the layout layer. |
| `kit.json` | The same contract, machine-readable, with file hashes. |
| `check-agustos-ui.py` | Compliance checker a consuming project runs to prove it complied. |
| `AGENTS-SNIPPET.md` | The stanza a consuming repository pastes into its own `AGENTS.md`. |

Two ways to consume it:

- **Production** — copy `ui/` into `vendor/agustos-ui/` and commit it. No runtime dependency on a
  third-party CDN, and the bundler can process the CSS normally.
- **Prototypes** — link the version-pinned CDN URLs in `UI-KIT.md`. Never `@main` or `@latest`: an
  unpinned link restyles a live page the moment a token changes, with no review.

Preview the kit locally with the `agustos-ui-kit` entry in `.claude/launch.json`, or:

```bash
python3 -m http.server 4330 --directory ui
```

To hand the kit to another coding agent, read [HANDOFF.md](HANDOFF.md) and run `python3 scripts/pack_handoff.py`.

Any change under `ui/` requires a VERSION bump, a rebuild, and a matching `v<VERSION>` git tag in the
same change. `VERSION` participates in the manifest's source hash, so the local gate (`scripts/ci.sh`) fails
if the rebuild is missed.

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
