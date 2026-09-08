# Design application handoff

Date: 2026-09-08
Design system version: 5.0.0
Status: Kit is ready. Copy it. Do not regenerate it.

Open these five artifacts first:

1. `DESIGN.md` — direction, colour, type, brands, principles.
2. `docs/fonts.html`
3. `docs/colour.html`
4. `docs/web.html` — header, footer, homepage, listing, finder, product page, spec sheet. Dark theme included.
5. `docs/brands.html`

## What this file is

Instructions for applying the existing UI kit to another repository.
This is not a prompt to rebuild the design system.

## Do not reproduce

Do not run `scripts/build_design_system.py`.
Do not run `brand/build.py`, `brand/build_templates.py`, or `scripts/build_ui_fonts.py`.
Do not read `DESIGN.md` or `MEMORY.md` to style a website.
Do not retype token values. Do not redraw the Laz Güneşi.

Those commands rebuild generated files that already ship in `ui/` and `brand/exports/`.
A website agent that runs them spends its time on the factory, not on the page.

## Share this, not the factory

From this repository:

```bash
python3 scripts/pack_handoff.py
```

That writes `dist/agustos-ui-handoff-v5.0.0.zip` (about 0.8 MB).
The zip holds the kit, lockup SVGs, this file, and the HTML map.
It does not hold generators, adapters, Office files, or decision history.

If you zip the whole repository, a coding agent regenerates CSS, logos, fonts, and Office files before it changes a page.

If you already opened the slim zip, skip packing. Start at Apply to a website.

## Apply to a website

1. Copy the zip's `ui/` folder to `vendor/agustos-ui/` in the target repository. Commit it.
2. Paste `vendor/agustos-ui/AGENTS-SNIPPET.md` into that project's `AGENTS.md`.
3. Load fonts first, then the stylesheet. Put a `brand-*` class on `<body>`.
4. Use kit classes and `var(--name)`. Compose. Do not restyle kit classes.
5. Run `python3 vendor/agustos-ui/check-agustos-ui.py .` and make it exit 0.

Read `vendor/agustos-ui/UI-KIT.md` before you write markup.
Open `vendor/agustos-ui/starter.html` to see every class once.

## If a Claude Design zip arrives in this repository

Edit only:

- `tokens/design-tokens.json`
- `tokens/web.css.tmpl`
- `brand/brands.json` (only when identity ink, wordmark, or roster changes)

Then run `python3 scripts/build_design_system.py`.
Do not rebuild logos, Office files, fonts, or datasheets unless asked.
Do not copy `.dc.html` markup into this repository.

See `docs/handoff-setup.html`.
