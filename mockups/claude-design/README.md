# Claude Design references

Pages pulled verbatim from the Claude Design project "Ağustos".

- Project: https://claude.ai/design/p/7fee69d5-01ee-4727-beaf-cb6c5bd923c4
- Project ID: `7fee69d5-01ee-4727-beaf-cb6c5bd923c4`
- Pulled by: `python3 scripts/sync_claude_design.py pull` (see `.claude/skills/design-pull/SKILL.md`)

These files are references, not kit sources. Nothing in `ui/` imports them.
The shared runtime at this folder's root (`styles.css`, `_ds_bundle.js`, `tokens/`) is
overwritten on every pull. Each page folder holds the page and an `index.png` screenshot.

## When you build one of these pages

1. Open the page folder and `index.png` beside your editor.
2. Rebuild the layout in the website repository with `ui/UI-KIT.md` and the kit classes.
3. Do not copy the Design markup or CSS. The kit is generated from the three sources.
4. Run `python3 vendor/agustos-ui/check-agustos-ui.py .` until it exits 0.
5. Change the row below to `implemented` and record the repository and commit.

## Status

| Remote path | Pulled | Status | Built in |
|---|---|---|---|
| ui_kits/website | 2026-09-13 | pending | — |
