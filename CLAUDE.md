# CLAUDE.md

This project's agent guidance lives in **[AGENTS.md](AGENTS.md)** — read it first.

Quick pointers: brand assets are indexed in [ASSETS.md](ASSETS.md); the spec is [DESIGN.md](DESIGN.md);
decision history is [MEMORY.md](MEMORY.md). Brand red is `#cf142a`. The favicon canonical is
`laz-gunesi-amblem/favicon/favicon.svg`.

## Design System v3

`agustos.com` is the reference implementation; this repository is authoritative. Begin shared design changes in `tokens/design-tokens.json` and `tokens/web.css.tmpl`, then run `python3 scripts/build_design_system.py`. Generated adapter CSS, WordPress `theme.json`, `tokens/resolved.json`, and everything under `brand/exports/` must not be edited directly. Use `python3 scripts/build_design_system.py --check` before handoff.
