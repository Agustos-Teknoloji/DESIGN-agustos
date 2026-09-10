# Changelog

All notable changes to the Ağustos Design System are documented in this file.

## Unreleased

## [5.1.0] - 2026-09-10

### Added

- Visited content links settle to ink-soft (`a:where(:visited)`). The `:where` keeps element specificity, so menu and chrome links styled by class keep their colour and hover still turns red.
- `text-wrap: balance` on both hero tokens, `.type-h1` and `.type-h2`.
- `.hero-link` carries an invisible 44px hit area (padding with a matching negative margin). The typographic look is unchanged; the target meets hard rule 5.

### Changed

- `--measure-body` is 65ch (was 72ch). 72ch in Inter ran to about 95 characters per line. 65ch is about 42rem at 16.5px, the content column agustos.com already uses, and reads at about 80 characters. `--measure-text` (54ch) stays the hero deck measure; the docs now say which measure is for what.
- The heading scale stays at four roles. A review asked for a list-title size between H2 and H3; lists of titles use body-size links with a footnote line instead, the article-list idiom. Recorded in DESIGN.md.

### Migration

- Vendor `ui/` at v5.1.0. Replace raw `max-width: 42rem` on prose columns with `var(--measure-body)`.

### Changed

- Align the Astro adapter with v5.0.1 composition rules.
- Marketing chrome omits the theme toggle.
- Header and footer use kit buttons and footer colour tokens.
- Recreate the Astro homepage from the marketing site kit: editorial opening, selected-work cards, one cream band, and footer chrome. Hold locked rules: no arrows, no quotes, no marketing theme toggle.
- Align the Rails adapter with v5.0.1 composition: no marketing theme toggle, kit header and footer buttons, a homepage trust line, one closing cream CTA band, and the IESDesk validation-run product UI from the kit (sidebar app shell, white paper, opt-in dark).

## [5.0.1] - 2026-09-08

### Changed

- Lock CTA repetition: the same primary destination appears in the header, the opening, and at most one closing cream band.
- Ship marketing, catalog, and spec pages on white paper. Reserve dark theme for product UI, using the locked six-colour flip from v5.0.0.
- Roll photographs out in this order: product page, listing thumbnail, homepage installation. Type-only pages stay complete.
- Restrict blockquote and pullquote to content pages. Marketing pages use a compact trust line.
- Add a slim handoff zip (`scripts/pack_handoff.py`) and an HTML map of the factory versus the kit.
- Tell website agents to copy `ui/` and stop. Do not zip the whole repository or re-run generators.
- Everyday source changes refresh the UI kit only. Logos, Office files, fonts, and datasheets wait for an explicit ask.
- Publish five standard artifacts: `DESIGN.md` plus HTML explainers for fonts, colour, web elements, and brands.

### Fixed

- Load handbook HTML with same-folder stylesheets so the pages render when opened as files.

## [5.0.0] - 2026-09-08

### Changed

- Apply the approved white-substrate visual direction: white paper, cream callout bands `#fdf5f5`, light gray surfaces `#ebebeb`, off-black ink `#15130f`.
- Set secondary text to dark gray `#404040`.
- Ration red `#cf142a` to the 2px content-link rule, the 2px menu hover or current-page rule, and keyboard focus.
- Lock the dark theme as the same six colours, flipped: paper `#15130f`, surface `#404040`, callout `#ebebeb`, ink `#ffffff`, ink-soft `#8a8378`.
- Allow one red fill: the dark-theme primary CTA. The secondary CTA on dark is filled white.
- Keep the footer off-black in both themes.
- Lock one H2 role, sentence-case labels, a filled-plus-outline button system, and an 1180px content column with 32px gutters.
- Move house-brand identity ink from `#1a1a1a` to `#15130f`.
- Preserve public CSS class names.

### Migration

- Vendor the complete v5.0.0 kit after release. Default paper is now white.
- Replace cream-page layouts with white paper plus optional cream bands.
- Restyle CTA pairs as filled black plus outline. Remove arrows and uppercase labels.
- On dark pages, restyle the primary CTA as filled red and the secondary as filled white.

## [4.0.2] - 2026-09-07

### Changed

- Complete the handoff with clear boundaries between finished repository work and pending website application.
- Carry forward the latest main-branch contrast fixes and license correction into the versioned kit.
- Regenerate the distribution files and manifests for the integrated release.

## [4.0.1] - 2026-09-07

### Changed

- Simplify the design direction around clarity, warmth, and human language.
- Remove material treatments as a design topic from current guidance and consumer contracts.
- Update the website brief and implementation plan to match the clarified direction.
- Preserve existing visual values, layouts, and public CSS classes.

## [4.0.0] - 2026-09-07

### Changed

- Adopt İskandivvian: Scandinavian restraint filtered through Mediterranean warmth.
- Define warmth through clear typography, purposeful spacing, neutral surfaces, and helpful language. Texture is optional.
- Publish the canonical design direction in the resolved registry, handoff, UI kit, and contributor guidance.
- Preserve numeric tokens, existing layouts, fonts, logos, and public CSS classes. Website application follows separately.
- Correct the README source list to identify the handoff as generated.

### Migration

- Vendor the complete v4.0.0 kit after release. Keep both stylesheets and bundled fonts together.
- Read the new design guidance before applying it to website compositions.
- Existing class names and token variables need no migration.

## [3.1.0] - 2026-09-04

### Added

- UI primitives for product surfaces: forms, buttons, badges, notices, and tabs. Same grammar as the editorial layer, composed entirely from existing tokens.
- Substrate-specific state colors. The four `--state-*` values scored 2.19 to 3.11 contrast on dark paper; `html[data-theme="dark"]` now overrides all four with variants above 7.
- A `ui/` distribution kit: one entry-point document, the stylesheet, self-hosted webfonts, a reference render, a machine-readable index, and a compliance checker. Another repository consumes this instead of re-deriving the system.
- Self-hosted subset webfonts under `ui/fonts/`, generated by `scripts/build_ui_fonts.py`. The stylesheet previously declared font stacks with no faces, so a project could load the system and still render in system fonts.
- A compliance checker, `ui/check-agustos-ui.py`. It reports hardcoded token values, missing font loading, unpinned CDN URLs, a missing brand class, oversized radii, gradients, and overridden kit classes.
- Reduced-motion handling, which the handoff contract promised and nothing delivered.

### Changed

- `VERSION` is now three-segment semantic versioning. Four segments break the semver ranges the distribution CDN uses.
- The published class list grew from 33 entries to 75, and a test now verifies that every published class exists in every generated stylesheet. Nothing verified this before.
- The `--mono` stack leads with the variable font name, matching `--display` and `--body`.

### Fixed

- Stale brand roster in the Astro adapter README: four brands became five, and the retired `photo` slug became `iesdesk` and `specquick`.
- Stale generation status for `pataraz` and `pld` in the brand README. Both kits exist.

## [3.0.0.1] - 2026-07-20

### Added

- Established proprietary, all-rights-reserved terms for the public repository while preserving third-party licenses.

### Changed

- Routed coding systems to the smallest authoritative files so they can use the design system without loading the entire repository into context.
