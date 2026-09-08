# Design application handoff

Date: 2026-09-08
Design system version: 5.0.0
Status: White-substrate visual direction applied to this repository. Consumer websites still need to vendor v5.0.0.

## Objective

Apply Scandinavian restraint filtered through Mediterranean warmth.
Create minimal, functional, and elegant experiences that feel calm, welcoming, and human.
Express warmth through white paper, warm grays, cream callout bands, clear typography, comfortable spacing, and helpful language.

## Completed work

- Applied the approved white-substrate palette, type scale, action system, and 1180px frame to the canonical registry.
- Rationed red to the 2px content-link rule, the 2px menu hover or current-page rule, and keyboard focus.
- Moved house-brand identity ink to `#15130f`.
- Regenerated the UI kit, adapters, and brand identity assets.
- Kept public CSS class names. Dark theme remains an open decision.

## Sources to read

1. Read `AGENTS.md` in the target repository.
2. Read this design repository's `ui/UI-KIT.md` for website work.
3. Read `DESIGN.md` for the palette, type, action, and layout rules.
4. Read `PATARAZ.md` when the selected brand is Pataraz.

For another medium, start with `tokens/design-system-handoff.json` and the matching adapter instructions.

## Remaining website work

1. Vendor `ui/` at v5.0.0 into the target website.
2. Map pages to the kit: white paper, cream bands, filled-plus-outline buttons, one H2 role.
3. Implement the three-zone header and the permanent black footer with a white "Contact" CTA.
4. Check font loading, Turkish language handling, keyboard access, contrast, and supported themes.
5. Run the target project's required tests and `python3 vendor/agustos-ui/check-agustos-ui.py .`.

## Implementation boundaries

Use the six-color palette and existing fonts. Keep wordmarks lowercase in Inter Tight 650.
Use the exact Laz Güneşi asset and each brand's registered identity ink.
Do not add red fills, uppercase labels, eyebrow headings, arrows, or shadows.
Load both the generated stylesheet and fonts. Use kit classes and token variables.
Consumer repositories must not regenerate this design repository or redeclare its token values.

## Open decisions

- How often the primary CTA may repeat on one page.
- The dark-theme palette.
- Photography rollout.
- Whether the quote treatment appears on content pages only.
