# Design application handoff

Date: 2026-09-15
Design system version: 6.0.0
Status: Both chromes, the layout layer, and the screens are in the kit. Share the five artifacts and screens/. Do not regenerate the factory.

Open these five artifacts first:

1. `DESIGN.md` — direction, colour, type, brands, principles.
2. `docs/fonts.html`
3. `docs/colour.html`
4. `docs/web.html` — one live frame per screen type, with that screen's rules. The pages are in `screens/`.
5. `docs/brands.html`

White paper, light gray `#ebebeb`, cream callout bands. Shared red is a 2px rule, not a fill, except the dark primary CTA.

## What this file is

Instructions for applying the existing UI kit to another repository.
This is not a prompt to rebuild the design system.

## Do not reproduce

Do not run `scripts/build_design_system.py`.
Do not run `brand/build.py`, `brand/build_templates.py`, or `scripts/build_ui_fonts.py`.
Do not retype token values. Do not redraw the Laz Güneşi.

Those commands rebuild generated files that already ship in `ui/` and `brand/exports/`.
A website agent that runs them spends its time on the factory, not on the page.

## Share this, not the factory

From this repository:

```bash
python3 scripts/pack_handoff.py
```

That writes `dist/agustos-ui-handoff-v6.0.0.zip`.
The zip holds the five artifacts, the kit, the screens, and lockup SVGs.
It does not hold generators, adapters, Office files, or decision history.

If you zip the whole repository, a coding agent regenerates CSS, logos, fonts, and Office files before it changes a page.

If you already opened the slim zip, skip packing. Start at Apply to a website.

## Apply to a website

1. Copy the zip's `ui/` folder to `vendor/agustos-ui/` in the target repository. Commit it.
2. Paste `vendor/agustos-ui/AGENTS-SNIPPET.md` into that project's `AGENTS.md`.
3. Load fonts first, then the stylesheet. Put a `brand-*` class and `data-screen` on `<body>`, plus `site-sidebar-layout` for a sidebar brand. Copy the brand's chrome from the matching screen.
4. Build each page from its screen in `screens/`. White paper, cream bands, filled-plus-outline buttons, one H2 role. Dark theme uses the same six colours, flipped.
5. Repeat the same primary CTA only in the opening and one closing cream band. The header may carry it once.
6. Keep marketing, catalog, and spec pages light. Do not add a theme toggle there.
7. Put photographs on product pages first. Leave listing and homepage type-only until those photos exist.
8. Use quotes on content pages only.
9. Run `python3 vendor/agustos-ui/check-agustos-ui.py .` and make it exit 0.

Read `ui/UI-KIT.md` and the matching screen before you write markup.
Keep wordmarks lowercase in Inter Tight 650. Do not add red fills, uppercase labels, arrows, or shadows.

## If a Claude Design zip or page arrives in this repository

Run `/design-pull <remote path> --target <screen>` in Claude Code, or `python3 scripts/sync_claude_design.py pull --from <zip> --page <remote path> --target <screen>`.
The page lands under `screens/design/` as a reference for one screen under `screens/`. Read `docs/claude-design-sync.html` for the full workflow.

A Design page is not a merge. If it shows a rule the kit lacks, edit only:

- `tokens/design-tokens.json`
- `tokens/web.css.tmpl`
- `brand/brands.json` (only when identity ink, wordmark, or roster changes)

Then run `python3 scripts/build_design_system.py`, and `/design-push` so Claude Design receives the rule.
Then rebuild `screens/<target>.html` on kit classes from the reference, flip its row in `screens/design/README.md` to implemented, and run `/design-push` again so the screen card updates.
Do not rebuild logos, Office files, fonts, or datasheets unless asked.
Do not copy Design markup or CSS into `ui/` or `tokens/`.

## Locked composition

- Same primary CTA: header once, page body at most twice (opening and one closing cream band).
- Dark theme ships on product UI. Marketing, catalog, and spec pages stay light. Dark uses the locked six-colour flip.
- Photographs: product page first, then listing thumbnails, then homepage installation. Type-only pages stay complete.
- Blockquote and pullquote appear on content pages only.
