# Design application handoff

Date: 2026-09-07
Design system version: 4.0.1
Status: Design direction approved. Repository contract updated. Visual application remains pending.

## Objective

Apply Scandinavian restraint filtered through Mediterranean warmth.
Create minimal, functional, and elegant experiences that feel calm, welcoming, and human.
Express warmth through clear typography, comfortable spacing, existing neutral surfaces, and helpful language.

## Completed work

- Updated the authoritative design rules and contributor guidance.
- Added the canonical `designDirection` field in `tokens/design-tokens.json`.
- Published that direction through the generated handoff, resolved registry, and UI kit.
- Updated Pataraz guidance and the website brief.
- Preserved existing visual token values, font families, logos, and public CSS classes.
- Passed 70 tests, generation checks, and Office manifest checks.

The completed work establishes the design contract. It does not redesign existing pages or Office layouts.
Visual comparisons, new compositions, and visual acceptance checks remain pending.
The earlier plan in `artifacts/` records exploration. Do not execute it as an outstanding checklist.
Do not repeat its v4.0.0 release or assume that proposed palette additions were approved.

## Sources to read

1. Read `AGENTS.md` in the target repository.
2. Read this design repository's `ui/UI-KIT.md` for website work.
3. Read `artifacts/agustos-iskandivvian-website-brief-2026-09-07.md` for the approved website direction.
4. Read `PATARAZ.md` when the selected brand is Pataraz.
5. Read `DESIGN.md` and `MEMORY.md` only when proposing changes to shared design decisions.

For another medium, start with `tokens/design-system-handoff.json` and the matching adapter instructions.

## Inputs needed for website application

Confirm the target website repository, brand, and pages or flow to change.
Inspect its existing content, functionality, and project instructions before asking for details already available there.
The approved style alone does not identify the target website or its business goal.

## Remaining website work

1. Inspect the target website and capture representative mobile and desktop pages.
2. Map its content and components to the existing UI kit.
3. Prepare a representative page that demonstrates the approved direction using real content.
4. Review that page before extending its composition to the remaining scope.
5. Implement responsive layouts and preserve working navigation, forms, and product information.
6. Check font loading, Turkish language handling, keyboard access, contrast, and supported themes.
7. Run the target project's required tests and `python3 vendor/agustos-ui/check-agustos-ui.py .`.
8. Report changed pages, verification results, and remaining limitations. Publish only when requested.

## Implementation boundaries

Use the existing palette and fonts first. Keep wordmarks lowercase in Inter Tight 650.
Use the exact Laz Güneşi asset and each brand's registered identity ink.
Preserve shared red links, focus, and interaction signals.
Load both the generated stylesheet and fonts. Use kit classes and token variables.
Consumer repositories must not regenerate this design repository or redeclare its token values.
Propose shared source changes separately when representative examples demonstrate a repeated need.
Do not change Office templates or unrelated websites as part of website application.

## Delivery and access

Use a repository checkout that contains this handoff and the current `VERSION` file.
Vendor the matching `ui/` folder into the target website repository.
Use versioned CDN links only after the matching tag is available on the remote repository.
For an offline transfer, provide the repository folder or an archive with its generated assets and fonts.
