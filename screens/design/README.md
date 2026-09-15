# Claude Design references

Pages pulled verbatim from the Claude Design project "Ağustos". Each one is a reference for a
screen under `screens/`, or for a new screen.

- Project: https://claude.ai/design/p/7fee69d5-01ee-4727-beaf-cb6c5bd923c4
- Project ID: `7fee69d5-01ee-4727-beaf-cb6c5bd923c4`
- Pulled by: `python3 scripts/sync_claude_design.py pull` (see `.claude/skills/design-pull/SKILL.md`)
- Repository commit at pull: `e3292db`

These files are references, not kit sources. Nothing in `ui/` or `screens/*.html` imports them.
A built page keeps its remote folder layout here so its relative links resolve; the shared runtime
at this folder's root (`styles.css`, `_ds_bundle.js`, `tokens/`) is overwritten on every pull, and
a pull replaces a page folder except its `index.png`. A canvas page (`*.dc.html`) lands under
`canvas/`; its runtime is not exported, so it does not render here and has no screenshot.

## When you build one of these

1. Open the reference beside your editor. Open `index.png` when it exists.
2. Rebuild `screens/<target>.html` on kit classes. Do not copy the Design markup or CSS.
3. Run `python3 ui/check-agustos-ui.py screens --skip design` until it exits 0.
4. Change the row below to `implemented` and record where it shipped.
5. Run `/design-push` so the updated screen card reaches Claude Design.

## Status

| Reference | Remote path | Pulled | Target screen | Status | Built in |
|---|---|---|---|---|---|
| website | ui_kits/website | 2026-09-13 | home | pending | — |
