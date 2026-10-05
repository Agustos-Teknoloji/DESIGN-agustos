# Design application handoff

Date: 2026-10-04
Design system version: 7.9.0
Status: Both chromes, the layout layer, and ten screens are in the kit. Websites and small products use the top menu and the footer; larger product UI uses the sidebar. The checker errors on identity and warns on taste. Share the five artifacts and screens/. Do not regenerate the factory.

Open these five artifacts first:

1. `DESIGN.md` — direction, colour, type, brands, principles.
2. `docs/fonts.html`
3. `docs/colour.html`
4. `docs/web.html` — one live frame per screen type, with that screen's rules. The pages are in `screens/`.
5. `docs/brands.html`

White paper, light gray `#ebebeb`, one pale red closing band. Shared red is a 2px rule, focus, and one highlighter stroke per page, never a fill. Buttons are black.

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

That writes `dist/agustos-ui-handoff-v7.9.0.zip`.
The zip holds the five artifacts, the kit, the screens, and lockup SVGs.
It does not hold generators, adapters, Office files, or decision history.

If you zip the whole repository, a coding agent regenerates CSS, logos, fonts, and Office files before it changes a page.

If you already opened the slim zip, skip packing. Start at Apply to a website.

## Apply to a website

1. Copy the zip's `ui/` folder to `vendor/agustos-ui/` in the target repository. Commit it.
2. Paste `vendor/agustos-ui/AGENTS-SNIPPET.md` into that project's `AGENTS.md`.
3. Load fonts first, then the stylesheet. Put a `brand-*` class and `data-screen` on `<body>`, plus `site-sidebar-layout` for the product sidebar only. Copy the chrome from the matching screen: every website uses the top menu (five items at most, the rest under More) and the footer.
4. Build each page from its screen in `screens/`. White paper, one pale red closing band, one primary and one secondary button, one H2 role. Dark theme uses the same six colours, flipped.
5. Name one primary destination. The header, the opening, and the closing band may carry it; the sections between them do not.
6. Start every page light. A theme switch is optional; the user picks dark, never the device.
7. Put photographs on product pages first. Leave listing and homepage type-only until those photos exist.
8. Keep quotes for content pages. Use the highlighter once, on the main headline.
9. Run `python3 vendor/agustos-ui/check-agustos-ui.py .` and make it exit 0.

Read `ui/UI-KIT.md` and the matching screen before you write markup.
Keep wordmarks lowercase in Inter Tight 650. Do not add red fills, red buttons, uppercase labels, arrows, or shadows.

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

- One primary destination: the header, the opening, and one closing pale red band. Advice, not a checked rule.
- The dark theme is the user's choice on any page. Every page starts light. Dark uses the locked six-colour flip.
- Photographs: product page first, then listing thumbnails, then homepage installation. Type-only pages stay complete.
- Blockquote and pullquote belong on content pages. Guidance, not a checked rule.
