# Changelog

All notable changes to the Ağustos Design System are documented in this file.

## Unreleased

## [7.0.0] - 2026-09-29

A conventional reset of the website layer. Identity (symbol, wordmarks, six colours, fonts) and the engine stay. Consuming sites pin `v7.0.0` when they are ready: agustos.com and iesdesk.com first, memregunes.com and pldturkiye.com later.

### Changed

- Chrome follows the screen family, not the brand: every website uses the top menu and the footer; product UI alone uses the sidebar. `chrome` leaves `brand/brands.json`, and the build rejects it.
- The top menu holds at most five items. The rest go under one More menu, `site-header__more` (native `<details>`), which opens inline in the phone drawer.
- The footer is light and small: the lockup and one line, then one row of social, legal and language links. No column headings, no repeat of the top menu, no button.
- Type sits on one golden scale (16.5px × 1.272 per step): 13, 16.5, 21, 27, 34, 43, 55, 70, 89px. Hero 89px thin, H1 55px thin, H2 43px, H3 21px, H4 and footnote 13px, hero deck 21px. Bold is 600.
- Two radii: 6px for controls, 12px for cards and floating menus. `--radius-sm` is an alias of `--radius-md`.
- One section spacing, `--section-space` (72px to 104px), for sections, the closing band and the gap after the hero. Sections lose their dividing rule.
- The hero opens with two buttons: one primary, one secondary. Product listing pages use the 55px H1, not the hero.
- Cards: 12px radius, the card gap owns the spacing, titles carry no underline, and the border darkens on hover.
- Buttons are black everywhere. The dark-theme red primary CTA is gone; the dark primary inverts to white.
- Logos answer hover: the Ağustos logo turns black, every other house-brand logo turns red.
- Favicons are per brand: a white tile with the red Laz Güneşi for Ağustos and the black one for every other brand. Tab icons crop the tile tight (the sun fills about 94%) so the blades read at 16px; the large home-screen icons keep the maskable margin.
- The checker guards identity with errors and taste with warnings. AG024 (`data-theme` outside product UI) is a warning. AG010 allows radii up to 12px.
- `UI-KIT.md`: nine house rules replace the twelve principles, and the brand table shows each logo's ink and hover ink.
- `scripts/check_office_artifacts.py` fingerprints only the brand fields the Office generators read. The Office files did not change.

### Added

- `type-highlight`: one red highlighter stroke per page, on one to four words of the main headline, on every brand.
- Checker warnings AG025 (more than one highlighter) and AG026 (a sidebar on a website).

### Removed

- `hero-links`, `hero-link`, `hero-link--primary`, `hero-link--secondary`, `hero-action`, `hero-action--primary`, `hero-action--secondary`. Use `hero-actions` with `agustos-button`.
- `site-footer__cols`, `site-footer__col`, `site-footer__col-heading`, `site-footer__list`, `site-footer__cta`. Use `site-footer__links`.
- Checker rules AG022 (primary-CTA count) and AG023 (quotes), the screens-table fields `primaryCtaMax` and `quotes`, and brand `screenOverrides`.
- The `bold` (700) and `small` (4px) radius tokens.

### Rebuilt

- Brand guidelines PDFs and favicon files only. Lockups, social images, swatches, email signatures and Office files were not rebuilt.

## [6.5.0] - 2026-09-29

### Changed

- H3 is the middle step of the type scale: 22px, upright, weight 500. It was 18px italic, so card titles read as small print between 16.5px body text and the 34px to 52px H2. Every H3 changes: card titles, content subsections and the WordPress "Heading 3" size.
- The hero trust line uses the 15.5px `bodyCompact` size, not a hand-typed 13.5px. The proof line was the smallest text on the page.

## [6.4.0] - 2026-09-29

### Added

- A link placed directly in a card's `h2`, `h3` or `h4` stretches over the card, so the whole card is the 44px target, as hard rule 5 requires. Other links in the card sit above the stretch and keep their own destination. Where `:has()` works, the focus ring goes around the card.
- The checker warns (AG013) when a card has links but none sits in its heading, because that card cannot become a target.

### Fixed

- Breadcrumb links fill their 44px list item. They were 21px tall. The layout does not move.

## [6.3.0] - 2026-09-29

### Fixed

- A heading that opens a card, a section or a band has no top margin. Flex items and padded boxes never collapse margins, so the 2.5em section-break margin stacked on the card gap and the section padding: every card opened with a 45px empty band, and every section heading carried 130px above the section padding. The home screen is 525px shorter.
- Content text uses `--ink-soft` (10.4:1), not `--ink-faint` (3.75:1): breadcrumbs, table headers, form labels, `.type-h4`, blockquote citations and the sidebar note. `--ink-faint` stays on non-content marks only, and its token description says so.
- In the dark theme, `.band--cream` keeps its text dark. Before, band text was white on light gray at 1.19:1.
- `.agustos-chrome-link` centres its text in its 44px box, so the topbar language link aligns with the menu.
- The block after `.type-hero-deck` gets the 1em baseline gap. Hero links and actions keep their own margin.
- Sidebar link labels sit 8px from their count badges.
- Inline code uses the 4px radius token, not a literal 3px.
- The command boxes on `docs/what-generates.html` are readable.
- The product screen puts the series descriptor after the H1, not above it. `DESIGN.md` drops the Tier 3 eyebrow exception.
- `DESIGN.md` and the hand-written handbook pages name the current version. `tests/test_version_labels.py` keeps them in step with `VERSION`.

## [6.2.4] - 2026-09-28

### Changed

- The `memregunes` Home may show a small photo of each recommendation writer who gives permission.

## [6.2.3] - 2026-09-28

### Changed

- A brand can override a screen rule with `screenOverrides` in `brand/brands.json`. The generator validates it, and the checker applies it to pages that carry the brand class.
- The `memregunes` Home may show up to three recommendations as quotes, and photographs of Emre Güneş: a portrait and a photograph of him at work.

## [6.2.2] - 2026-09-28

### Added

- `check-agustos-ui.py --screens-only` runs only the screen rules (AG020 to AG024) on the rendered `.html` pages of a built site. An Astro or ERB layout fills `data-screen` at render time, so the source scan skips those rules. Run `check-agustos-ui.py dist --screens-only` after the build. `UI-KIT.md` documents the step.

### Fixed

- The checker matches the skipped folders (`SKIP_DIRS` and `--skip`) only below the scan root. Before, it matched every folder of the absolute path, so `check-agustos-ui.py dist` scanned no file, and neither did a project inside a folder named `dist`, `build` or `vendor`.
- The screen rules skip a redirect stub, a page with `<meta http-equiv="refresh">`. Astro writes one for each redirect, and a redirect is not a screen.

## [6.2.1] - 2026-09-27

### Changed

- The `memregunes` brand uses sidebar chrome. Its seven Turkish menu labels do not fit a topbar at 1024px.

## [6.2.0] - 2026-09-27

### Added

- Add the `memregunes` brand: the personal site of Emre Güneş at memregunes.com. Wordmark "emre güneş", neutral ink, topbar chrome.
- Brand guidelines: an 11-page A4 PDF for agustos, pataraz and pld, in English. Pages: cover, contents, introduction with the brand family, symbol, logo, clear space and minimum size, logo misuse, colour, typography, which file to use, and back cover. `brand/build_guidelines.py` writes the HTML and, with `--pdf`, renders the PDF. It replaces the 4-page PDF and its manual render step. `tests/test_guidelines.py` checks the 11 sections, registry-only colours, and no em dash, uppercase or eyebrow label (2026-09-27).

### Changed

- Generate the brand list of `check-agustos-ui.py` from `brand/brands.json`. A new brand no longer needs a hand edit in the checker.
- Allow a portrait of Emre Güneş on the home and about pages of the `memregunes` brand.
- Docs: `AGENTS.md` asks the agent to check with Emre before it rebuilds the brand guidelines PDFs after a big brand change (2026-09-27).
- CI: the local gate replaces GitHub Actions. `scripts/ci.sh` runs the three checks of the removed workflow, and `.githooks/pre-push` runs it before every push. Run `bin/setup` once per clone to activate the hook (2026-09-25).
- Docs: the ops baseline block in `AGENTS.md` names the new path of the CONTEXT-agustos checkout, `~/vaults/business/PROJECTS/CONTEXT-agustos` (2026-09-25).
- Docs: adopt the fleet root doc set. `AGENTS.md` follows the fleet shape: the ops baseline block, a source priority, a router, rules and a Traps section. `CLAUDE.md` is one line, `@AGENTS.md`. New `ARCHITECTURE.md` with a Testing section, new `MEMORY.md` with date-slug IDs, and new `TODO.md`. `archive/MEMORY.md` is frozen. The factory-only sections and the history leave `DESIGN.md`; the consumer contract stays. `HANDOFF.md`, `ASSETS.md` and `PATARAZ.md` stay at the root.
- Backfill, 2026-09-16 (PR #39): the seven parked review items from PR #38 closed. The generator writes the `screens/README.md` table, anchors its block-end search to each block, and refuses two steps that write one path. The handoff zip and the Claude Design screen cards carry every brand's datasheet assets and fail on a missing one. `/design-pull --target` checks the screens table. The Rails preview has its burger again, and the static screen has one photo well.
- Backfill, 2026-09-09: `MEMORY.md` moved to `archive/MEMORY.md` with no content change, and `pataraz-ui-brief.md` merged into `PATARAZ.md`. The root docs went from 11 files to 8.

### Removed

- `tasks/todo.md` and `tasks/lessons.md`. Open items moved to `TODO.md`, decisions to `MEMORY.md`, and repository lessons to the Traps section of `AGENTS.md`.

## [6.1.0] - 2026-09-16

### Added

- Checker rules for the screens table, baked into `check-agustos-ui.py` like the token table. Every page names its screen with `data-screen` on `<body>` (AG020), the name must be a row of the table (AG021), primary actions inside `<main>` stay within the row's limit (AG022), quotes appear only where the row allows them (AG023), and `data-theme` appears only on product UI (AG024). A templated value (an Astro or ERB layout) is skipped; check the rendered pages.
- The Astro layout takes a `screen` prop and the Rails helper a `screen:` option; both render `data-screen` on `<body>`. Product UI defaults to `app-shell` in Rails; every other page names its own.
- `content-index`, the ninth screen: the list of posts, one section per year, body-size title links with a footnote line each, no heading per title. Built from the live agustos.com blog index.

### Changed

- Claude Design: the project's own token, component, and specimen-card layers were retired on 2026-09-16. Its root `styles.css` now imports the pushed kit, and its `SKILL.md` points at `agustos-ui/UI-KIT.md` and the screen cards. The project owns drawings only (`ui_kits/`, `uploads/`). A verbatim copy of the retired layer is `artifacts/claude-design-own-stack-2026-09-16.zip`.

### Fixed

- `sync_claude_design.py pull` no longer loses a canvas file when the source directory holds nothing but its `uploads/<chat>/` folder; the single-folder unwrap now applies only when the page lives inside that folder.

### Migration

- Put `data-screen="<name>"` on every page's `<body>`, or the checker exits 1 with AG020. Pages that exceed a screen's primary CTA limit, carry quotes on a non-content screen, or set `data-theme` outside product UI now fail too.

## [6.0.0] - 2026-09-15

### Added

- Both site chromes in the kit: `site-sidebar*` (agustos, iesdesk, specquick) and `site-header*` with `site-footer*` (pataraz, pld), plus `site-lockup*` and `breadcrumb*`. Drawers are native popovers; groups are `details`. No JavaScript.
- A `chrome` field per brand in `brand/brands.json`, published in `ui/kit.json` and the UI-KIT brand table.
- The layout layer: `stack`, `cluster`, `prose`, `grid-2`, `grid-3`, `grid-4`, `grid-aside`, `band`, `band--cream`, `table-scroll`.
- `screens/`: one reference page per screen type on kit classes, with real content. The `screens` table in `tokens/design-tokens.json` holds each screen's rules and renders into `ui/UI-KIT.md`, `ui/kit.json`, `docs/web.html`, and the Claude Design cards.
- `docs/web.html` is generated from the screens table. The handoff zip packs `screens/`.
- The design direction list in `DESIGN.md` is generated from the registry between two markers.
- Claude Design: one card per screen under `Kit · Screens` and two chrome cards; `/design-pull` accepts any page folder or canvas file and records the target screen in `screens/design/README.md`.

### Changed

- `docs/web.html` no longer carries its own chrome rules; the Astro and Rails adapters use the kit chrome and ship no navigation script.
- `ui/UI-KIT.md`: one install section, the brand chrome table, the screens table, and the rule that the kit is plain CSS with no utility framework.
- pataraz.com's build target is Rails 8 with plain CSS. Tailwind is not supported anywhere.

### Removed

- `mockups/`: the four built pages became screens; the Claude Design references moved to `screens/design/`.
- `hero-example.html` (now `artifacts/agustos-hero-example-v3.1.0.html`) and the root `build_template.py`.
- The Rails `agustos-nav` Stimulus controller and both adapters' backdrop buttons.

### Migration

- Replace local header, footer, and sidebar CSS with the kit chrome classes. No chrome rule may live outside the kit.
- Rails: rename `agustos-header`, `agustos-footer`, and `agustos-nav-backdrop` to `site-header`, `site-footer`, and the popover backdrop.
- agustos.com: replace `side-menu` and `mobile-header` with `site-sidebar` and `site-sidebar-bar`; put `site-sidebar-layout` on `body`.
- Put `data-screen="<name>"` on `body`.
- Remove Tailwind or any other utility framework if present. The kit does not support one.
- Rails: delete the `agustos-nav` Stimulus controller with its `data-controller`, `data-action` (`keydown.esc`), and backdrop markup. The drawer is a native popover opened by `popovertarget`.
- Astro: delete the `nav-backdrop` markup, the `data-nav-open` attribute, and the script that toggled it. The drawer is a native popover opened by `popovertarget`.
- Both adapters: render the lockup with the kit classes `site-lockup`, `site-lockup__symbol`, and `site-lockup__name`. Drop local lockup classes and the `--lockup-color` custom property; the kit colours the footer lockup and the dark theme.

## [5.2.0] - 2026-09-13

### Added

- Claude Design sync. `scripts/sync_claude_design.py build` packs the kit, favicon, lockups, and preview cards under `agustos-ui/`; `/design-push` uploads that folder into the Claude Design project "Ağustos". `scripts/sync_claude_design.py pull` and `/design-pull` save a Design page under `mockups/claude-design/` as a reference with a status table. Workflow: `docs/claude-design-sync.html`.

### Changed

- One shared favicon for every house site: the bare red Laz Güneşi (`laz-gunesi-amblem/svg/master.svg`). Replaces per-brand negative-tile favicons. Canonical kit, adapter mirror, and all `brand/exports/<brand>/favicon/` sets updated; social avatars stay per-brand monograms.

## [5.1.1] - 2026-09-10

### Added

- `check-agustos-ui.py --skip <dir>` (repeatable) leaves frozen or generated folders out of the scan. agustos.com keeps a stale stylesheet alias for cached pages that must not be edited; consumers no longer have to hand-patch the generated checker to pass.

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

## Before 3.0.0.1 (backfill)

Added on 2026-09-24 from the closed items in the former `tasks/todo.md`. `archive/MEMORY.md` has the detail.

- 2026-07-19, v3 implementation: canonical foundations, semantic roles, recipes and compatibility metadata in one token registry. Generated canonical CSS, the Astro, Rails and WordPress mirrors, `theme.json` and a manifest, with a deterministic `--check` and tests. Word and PowerPoint read the same resolved token values.
- 2026-06-20, brand kit: `brand/brands.json` as the brand registry, vendored fonts, and `brand/build.py`. It generates lockups in three expressions, favicons and app icons, and social images. `brand/build_templates.py` generates the PowerPoint, Word and email signature templates. A four-page guidelines PDF and `.ase` and `.clr` swatches followed. Pataraz and PLD Türkiye got full kits. The house brands added later have logos, favicons and social images.
