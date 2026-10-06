# Changelog

All notable changes to the Ağustos Design System are documented in this file.

## [Unreleased]

## [7.11.0] - 2026-10-06

A minor release: the kit gains the landing page, a page that makes several arguments in a row. Emre approved the rules on 2026-10-06, after he rejected alternating sides on memregunes.com/consulting. memregunes.com built them first with its own classes (WEBSITE-memregunes PR 91). Decision record: MEMORY 2026-10-06 landing-page. A site that does not add the new classes changes nothing.

### Added

- The landing page rules in `UI-KIT.md` and `DESIGN.md`: one argument per section, in a fixed order; three levels of space; the text on one left edge and each picture in the side zone to its right; a picture adds information; one size for a series of drawings; a change of pattern at least once; no rule and no band between parts; text first on a phone. Sources: NN/g on zigzag layouts, proximity and the illusion of completeness, and Refactoring UI on spacing.
- `container--landing` on the page column. On a reading page the sections sit `--section-space` (72 to 104px) apart, not 40px. Each picture is centered on the text of its part, and every picture takes half the reading line at most.
- `reading-split` and `reading-split__media`: a part with a picture beside its text. From 1024px the text keeps the reading line and the picture fills the side zone, aligned at the top; below 1024px they stack in markup order. The picture never takes the left side, whatever the markup order.
- `reading-wide`: a part of a reading page that runs across the frame from 1024px, for example a `grid-3`.
- The `landing` reference screen (`screens/landing.html`, content family, reading column): a sample Ağustos consulting page with two drawings in one series.

### Changed

- The checker tests use `pricing` as the example of an unknown screen name, because `landing` is now a screen.
- The `UI-KIT.md` length limit rises from 230 to 235 lines, for the new screen row and the landing page rules.

## [7.10.0] - 2026-10-06

An extra minor release under MEMORY 2026-09-29 monthly-kit-release: memregunes.com shows its seven pages in the top menu, a site exception to the five-item rule, and its Turkish row overlaps itself between 1024 and about 1150px. Emre approved the fix on 2026-10-06 ("yes to all three, go ahead"): the burger menu on narrower screens instead of a crowded row. He saw a mockup of the folded and the full menu. Decision record: MEMORY 2026-10-06 header-fold-wide. A site that does not add the modifier changes nothing.

### Added

- `site-header--fold-wide`, an opt-in modifier on `<header class="site-header">`. With it the top menu folds into the burger and the drawer below 1280px, not below 1024px. Use it when the row does not fit at 1024px: long labels, or a site exception with more items. 1280px is the kit's small-laptop breakpoint, so no new breakpoint enters the kit.
- `agustos-chrome.js` treats 1280px as the drawer width for a top menu with the modifier: it opens every More of the open drawer below 1280px, and it clears the marks at 1280px and wider.
- The Astro adapter takes `header={{ foldWide: true }}`, and the Rails adapter takes `agustos_theme(fold_wide: true)`. Both add the modifier.

### Changed

- The build writes the top-menu drawer rules twice from one source in `tokens/web.css.tmpl`: below 1024px for every top menu, and from 1024 to 1279px scoped to `:where(.site-header--fold-wide)`. `:where()` keeps the weight of each rule, so the drawer wins over the tighter small-laptop spacing by order alone.

## [7.9.0] - 2026-10-05

An extra minor release under MEMORY 2026-09-29 monthly-kit-release: banuucak.com moves from WordPress to Astro with the kit, and it needs its brand. Emre approved the brand on 2026-10-05 ("yes to all four, go ahead", to the banuucak.com spec questions). Decision record: MEMORY 2026-10-05 banuucak-brand. Consuming sites change nothing.

### Added

- The `banuucak` brand: the personal site of Banu Uçak at banuucak.com. Wordmark "banu uçak", neutral ink, no Office files. `brand-banuucak` joins the brand classes, the CSS and the checker.
- `brand-banuucak` may show photographs of Banu Uçak on `home` and `static`. `home` and `content-index` may list her posts as cards with a cover photograph.

### Changed

- Docs: the cap on `## Next` in `TODO.md` rises from 20 to 50 items, per the fleet rule `2026-10-05 next-cap-50` in ops. `AGENTS.md` states the new cap. No kit change, so no version bump (2026-10-05).
- Docs: the ops baseline block in `AGENTS.md` adds the TODO.md line. Each open TODO.md item has a card in the Basecamp project CODING, and a sync job updates the card. The two rule lines become one line. No kit change, so no version bump (2026-10-05).

## [7.8.1] - 2026-10-04

A defect patch under MEMORY 2026-09-29 monthly-kit-release: real defects ship at once. The IESDesk dark audit on kit v7.7.0 found it, and v7.8.0 still had it. Decision record: MEMORY 2026-10-04 dark-code-blocks. The patch number follows v7.8.0, because the tag workflow tags only a version newer than the newest tag.

### Fixed

- Code blocks in the dark theme. A `pre` or `type-code-block` is an ink panel with rule-coloured text, and the dark theme flips both roles, so the block turned into a white panel with dark text (for example the IES anatomy example on the IESDesk Learn page). In the dark theme a code block now takes `var(--surface)` with `var(--ink)`: white on dark gray, 10.4:1. Light is unchanged. The inline-code tint of the dark theme stays off the lines inside a block.
- Print outlines a dark-theme code block as it does a light one: the dark rule outranked the print reset of a bare `pre`.

### Added

- States row "Code block": light rule on ink (14.61:1), dark ink on surface (10.37:1).

## [7.8.0] - 2026-10-04

An extra minor release under MEMORY 2026-09-29 monthly-kit-release: the HEPER dashboard admin moves to Madmin with the kit, and LIGMAN One follows. Emre asked for client brands on 2026-10-04 ("For brands like HEPER, LIGMAN etc, let's have logo and 1 Colour which will be used instead of black."; "Let's have dark theme as well."). Decision record: MEMORY 2026-10-04 client-brands. Emre approved the before and after preview on 2026-10-04 ("approved").

### Added

- Client brands. `brand/brands.json` gains `clients`: each client registers a title, a domain, an SVG logo and one colour. The colour takes the place of black on the primary button. The kit keeps its fonts, greys and red signal.
- The build writes `ui/brands/<slug>.css`, `ui/brands/<slug>.svg` and `ui/brands/<slug>-dark.svg` for each client. The CSS file sets the button fill, its text (white or the kit ink, whichever has more contrast) and a hover fill 15% darker. The dark logo turns near-black fills into the dark-theme ink.
- The first clients: `brand-heper` (HEPER red `#ed1c24`, white text) and `brand-ligman` (LIGMAN yellow `#fcaf17`, ink text).
- `site-lockup__logo`, `site-lockup__logo--light` and `site-lockup__logo--dark`: the client logo images inside the `site-lockup` link, in place of the symbol and the wordmark. The kit shows the one that suits the theme, and print shows the light one.
- `kit.json` gains `clients` (stylesheet, logos, button colours and contrast per client), and `brandClasses` lists the client classes. UI-KIT.md gains a Client brands section.

### Changed

- The primary button reads `--action`, `--action-ink` and `--action-hover`. Each falls back to the current value, so a house brand page does not change.

### Known gap

- White text on HEPER red is 4.38:1, below the 4.5:1 minimum for the 15.5px button text. The hover fill reaches 5.6:1.

## [7.7.0] - 2026-10-03

An extra minor release under MEMORY 2026-09-29 monthly-kit-release: IESDesk moves every page to one top menu and offers the dark theme everywhere (IESDesk MEMORY 2026-10-03 one-top-bar, dark-theme-everywhere), and the kit rules blocked both. Emre approved the change on 2026-10-03 ("Let's change the UI kit rule. Footer should change too."; "user should choose light or dark, not the system to dictate"; "Everything starts with light first").

### Changed

- Every site may offer the dark theme. The rule "Websites ship light; dark theme is for product UI" and the ban on a theme switch on a website are gone. Every page starts light, and a site without the switch stays light.
- The footer and the closing band turn dark with the page. The light islands are gone. The dark band is the dark paper between two hairline rules, so red keeps 3.35:1 and secondary text 4.95:1.
- Print is always light, also with the dark theme on.
- Product UI may use the top menu when it has about ten destinations or fewer. The new screen `app-top-menu` shows it. The app shell keeps the sidebar.
- Below 640px the drawer covers the whole width: the top-menu panel and the sidebar drawer alike. From 640 to 1023px it keeps `min(320px, 86vw)`.
- The screens table field `theme` is `light-first` for every screen.
- AG024 warns on a page that starts dark (`data-theme="dark"` on the served `<html>`), not on any `data-theme`. AG027 counts only the items in `site-header__nav`, so an account list in `site-header__end` does not count. AG026 warns on a sidebar on every screen whose chrome is the top menu, `app-top-menu` included. AG024 and AG027 step over ERB and PHP tags inside a start tag, and AG034 accepts a Rails `javascript_tag` that carries the head script.

### Added

- The theme switch: `agustos-theme-switch`, `agustos-theme-switch__to-dark`, `agustos-theme-switch__to-light`, `agustos-theme-switch__label`, with `data-agustos-theme`. `agustos-chrome.js` flips the theme and keeps it under `agustos:theme`; `kit.json` publishes the head script as `themeScript`.
- Grouped More lists: `site-header__more-menu--groups`, `site-header__more-group`, `site-header__more-group-title`. A More holds at most two groups: columns on a wide screen, stacked in the drawer.
- The phone drawer shows every More open, with its summary as a small title (`data-agustos-unfold`, set by `agustos-chrome.js`). Without the script each More folds as before. The script clears the marks at 1024px and wider and before Turbo caches the page, so Back never brings back a More that is stuck open.
- The account list: `site-header__more--end` and `site-header__more-label`, and a button reset for a sign-out `button.site-header__more-link` in a `form`.
- AG033 warns on `prefers-color-scheme` in any checked file but Markdown: CSS, a script or a page.
- AG034 warns on a theme switch without the kit head script before the stylesheets.
- AG035 warns on a More with more than two groups, because a third group goes past the edge of the page at 1024px.
- AG036 warns on a theme switch on a page that does not load `agustos-chrome.js`, because the switch then does nothing.
- States rows: the dark footer, the band secondary text, the focus ring in the band, the theme switch, the More group title.

### Deprecated

- `site-header__theme-sun` and `site-header__theme-moon`. Use `agustos-theme-switch`. They stay until v8.

### Documentation

- UI-KIT.md, DESIGN.md, HANDOFF.md, the adapters and the handbook pages state the new rules. The brand guidelines PDFs are rebuilt with the new "Colour in use" rule (Emre approved, 2026-10-03).

### Migration

- A site that adds no switch changes no markup and stays light. Its desktop header, footer and band look the same in light. Below 1024px every More in the drawer shows open with its title, and below 640px the drawer fills the screen. Check each site at 375px and 800px.
- A site that adds the switch puts the head script (`kit.json` `themeScript`) in `<head>`, after the viewport meta and before the stylesheets, with its CSP nonce. AG034 warns when it is missing. A page with the switch also loads `agustos-chrome.js`; AG036 warns when it does not.
- A site that sets text on `var(--cream)` outside `band--cream` changes it before it adds the switch: in the dark theme `--cream` stays light gray `#ebebeb` under white ink.
- A site that renders `data-theme="dark"` on `<html>` from the server now gets AG024. Apply the stored choice with the head script instead.
- A site with its own theme handler (Astro or Rails adapter copies, IESDesk `agustos_theme_controller.js`) removes it when it adopts `data-agustos-theme`, or the click flips the theme twice.
- Rails adapter: the `color_scheme:` option and `agustos_dark?` are removed, so a caller that passes `color_scheme:` gets an `ArgumentError`. The Stimulus theme controller is deleted. A host that shows the switch imports `agustos/chrome`.
- Astro adapter: the `BaseLayout` `theme` prop is removed, so no page renders dark from the server. `header={{ theme: true }}` adds the kit switch and the head script.
- A site that renders `site-header__theme-sun` or `site-header__theme-moon` keeps working until v8. Move to `agustos-theme-switch`.

## [7.6.2] - 2026-10-01

A defect patch from the agustos.com move to v7.6.1 (WEBSITE-agustos PR 167). Emre asked for it before the last two site PRs merge. Each defect was measured in a browser before and after the fix. Consuming sites change no markup. A site that added its own space under a meta line, as agustos.com does on `.post-header`, can remove it.

### Fixed

- "On this page" sits level with the H1 when the page opens with a breadcrumb. At 1280px and wider the list kept the 112px hero padding, but since v7.6.0 such a page starts 16px under the menu. The list title sat 28px below the top of the H1. It now starts under the trail (16 + 44 + 24px). Measured at 1440px: 28px to 0. A page with no breadcrumb does not change.
- A meta line with no deck above it takes 24px before the text, as it does after a deck. It took 1em of its own size: 13px on the agustos.com cookie pages.
- Inside a `stack`, the meta line keeps the same spaces. A stack is a flex column, so margins add up: the v7.6.0 meta-line margin plus the stack gap gave 40px before body text and 56px before buttons. Both meta-line margins now skip a stack, and the stack sets 12px under a deck and 24px to the next block through `--stack-space`. A heading below keeps its own break (40px before an H2).
- Measured on all 9 screens at 1440 and 390px: no box moves, because no screen holds one of these three cases.

### Documentation

- UI-KIT.md and DESIGN.md: a page with no deck puts the meta line under the title, with 24px before the text; the contents list sits level with the H1, with or without a breadcrumb.

## [7.6.1] - 2026-10-01

A defect patch. It fixes the meta-line gap, found while four sites moved to v7.6.0 (WEBSITE-pldturkiye PR 55), and the paths in the exported HTML. Consuming sites change no markup.

### Fixed

- The meta line sits 12px (`recipes.hero.metaGap`) under the deck, as v7.6.0 states. The general rule that puts 1em after a deck was more specific, so the meta line took 1em of its own size: 13px. That rule now skips a `type-footnote`. Measured at 1440 and 390px: 13 to 12px on the `content` and `spec-sheet` screens. The space after a deck on `product`, `home` and `products` does not change (16, 32 and 16px).
- The datasheet and brand guidelines HTML (`brand/build_datasheet.py`, `brand/build_guidelines.py`) reference fonts, lockups and SVG drawings by paths relative to the HTML file. Before, they used absolute `file:///` URLs of the folder that ran the build, so the HTML fell back to system fonts on another machine or after a worktree was deleted. Each rebuild from another folder also changed every line that held a path. The PDFs embed their fonts and did not change. `tests/test_export_paths.py` fails on a `file:` URL and on a reference that does not resolve. The committed exports change on the next rebuild.
- Rebuilt the six datasheets and the three guidelines on the relative paths (Emre asked, 2026-10-01). The HTML holds no `file:` URL; only the path lines changed. `pdfinfo` confirms 14 pages for each guidelines PDF and 1 page for each datasheet, and `pdffonts` shows Inter, Inter Tight and JetBrains Mono embedded in each PDF.
- `brand/build_social_posts.py` uses the same `rel_url` as the datasheet and guidelines builders. Its own `rel` counted the `..` steps from the output folder as given. The PNG render opens the page by its resolved path, so in a symlinked output folder the fonts did not load and the PNG fell back to system fonts. It also did not URL-encode the path. `tests/test_export_paths.py` now covers the social posts. The committed post HTML is not rebuilt; a rebuild changes only the encoding of the three font URLs, and the PNGs stay pixel-identical.

### Changed

- Rebuilt brand exports on the v7.6.0 generators (Emre asked, 2026-10-01). The guidelines PDFs for Ağustos, Pataraz and PLD have 14 pages with "In every medium" and the type table. The six datasheets drop all-caps labels, red text and the 650 title weight, and take the registry's faces, weights and print sizes.

### Documentation

- CHANGELOG.md: the v7.5.0 section had the heading of v7.6.0 after the renumber merge. It now reads 7.5.0.

## [7.6.0] - 2026-10-01

One brand in every medium. Emre asked for a kit that feels like one brand on websites, datasheets and LinkedIn, the three media of the next six months, and approved the heading rhythm from a before/after preview. Record: MEMORY.md 2026-10-01 one-brand-every-medium.

Consuming sites move the date line of an article from above the H1 to under the deck, as a `type-footnote`. Text below an H1 or a heading moves up (see Changed). A site may add `type-spec` to its spec tables and lists, and may replace hand-typed type sizes with the new variables.

### Added

- One type contract. `recipes.typeRoles` in the registry has one row per text role: class, face, size, weight, line height, tracking, the space around it, what it is for and what not to use it for. UI-KIT.md prints it as "Type and spacing", `kit.json` and `tokens/resolved.json` publish it as `typeRoles`, and the brand guidelines and the LinkedIn templates read it.
- Variables for every type step: `--size-hero` to `--size-h4`, `--size-deck`, `--size-quote`, `--size-pullquote`, `--size-form-field`, with `--leading-*` and `--tracking-*` per role, and the heading rhythm `--space-before-h2`, `--space-before-h3`, `--space-after-title`, `--space-after-h2`, `--space-after-h3`, `--space-after-h4`. Before, only 3 of about 10 sizes had a name, so a site had to retype the others.
- `type-spec` on a `table` or a `dl` of product specifications: values in JetBrains Mono with tabular figures, labels in Inter Tight. The `product` and `spec-sheet` screens use it. Spec values now look the same on the web and the datasheet.
- `designDirection.invariants`: seven rules that hold in every medium, each with its form on a website, a datasheet and LinkedIn. DESIGN.md prints them under "One brand in every medium"; the brand guidelines gain a page, "In every medium" (14 pages).
- `docs/family.html`, the family-photo sheet: Pataraz PX22 as the product page, the datasheet and a LinkedIn post side by side, with the rules and the type table under them. Review it at each monthly release.
- LinkedIn post templates: `recipes.social` and `brand/build_social_posts.py` write a portrait (1080 × 1350) and a square (1200 × 1200) post per full-kit brand from the type table.

### Changed

- The space below a heading is a fixed step, smaller than the space above it, so the heading binds to the text it opens: 32px under a hero or an H1 to its deck (55px under an H1 before), 20px under an H2 (43px), 12px under an H3 (21px), 8px under an H4 (13px). Measured on the `content` and `static` screens at 1440 and 390px.
- A page that opens with a breadcrumb starts 16px under the top menu, on a `container` and a `site-frame` alike. The `content`, `static` and `content-index` screens had the full hero padding above the trail (112px at 1440px, 56px on a phone), and `products` and `product` had none. Emre found the empty band in the preview.
- The page opening reads breadcrumb, title, deck, meta line. The title sits 24px under the breadcrumb (it touched the trail on `products`, `static` and `product-finder`), and a date or revision line is a `type-footnote` 12px under the deck, never a label above the title. The `content` and `spec-sheet` screens and the Astro blog post move their line, and `spec-sheet` gains the breadcrumb of an inner page (Ana sayfa / Ürünler / PX serisi / PX22 / Teknik föy). `starter.html` moves its version label from above the title into the trust line. Emre chose this (option D) from four rendered options; lighter text alone fails the 4.5:1 floor.
- `type-hero-md` takes the 32px title gap (24px before), like `type-hero` and the H1.
- The stack (v7.5.0) reads the same heading variables, so a title, a heading or a hero part sits the same inside a stack as outside it. A title or an H1 in a stack sits 32px above its deck: 24px after a `type-hero-md` before, and 16px after an H1, as on the product screen. A heading in a stack takes 20, 12 or 8px below it, like the text flow.
- Six sizes move onto the scale or a named token: block quote 22 to 21px, pull quote 26 to 27px, definition list 16 to 16.5px, figure caption and code block 13.5 to 13px, button 15 to 15.5px. Inputs keep 16px as `--size-form-field`. Only the site lockup keeps a pixel size.

### Fixed

- `brand/build_datasheet.py` follows the house rules: no all-caps tracked labels, no red text, no 650 weight on the title, and colours, faces, weights and print sizes come from `tokens/resolved.json`. The exported datasheets change when Emre asks for the rebuild.
- The brand guidelines Typography page reads the type table: the H1 tracking matches the web (-0.04em, was -0.035em), and the line length reads "about 75 characters" (was 65). The guidelines' own titles drop the 650 weight. The PDFs change when Emre asks for the rebuild.

### Documentation

- DESIGN.md matches the CSS: the H2 gap, the footnote rule, the faces of block quotes and spec values, and the sizes above.
- UI-KIT.md: the two paragraphs that repeated house rules 5 and 8 are gone; the highlighter markup moves to the type section. Its line limit is 220 (was 200) for the type table.

## [7.5.1] - 2026-10-01

A defect patch from the 2026-10-01 kit audit. Emre asked for it after v7.5.0. Each defect was measured in a browser before and after the fix. Consuming sites change no markup. A site that patched `[hidden]` itself, as memregunes.com does in `home.css`, can remove the patch.

### Fixed

- The `hidden` attribute hides every element. A kit class that sets `display` outweighed the browser's own rule: a hidden `agustos-button` showed as `inline-flex`, a hidden `stack` as `flex`. Both now compute to `none`. `hidden="until-found"` keeps the browser's find-in-page behaviour.
- A card takes the hover only when its heading holds a link. A card without a link darkened its border on hover and signalled a click that did nothing, as the app-shell stat cards did.
- A marked card keeps its 2px ink rule on hover. The hover set all four borders, so the rule faded to the 30% gray.
- A hovered skip link keeps white text on its ink box. `a:hover` turned it red: 3.35:1, below the 4.5:1 text floor.
- Code blocks and the primary button print as outlines. The print dialog drops backgrounds by default, so the light code text printed at about 1.2:1 and the button printed white on white. The outlines read the same with background graphics on or off (checked with a headless Chrome PDF before and after).

## [7.5.0] - 2026-10-01

A minor release from the memregunes.com home review. Emre asked for the kit fix on 2026-10-01, and chose four hero layouts. Consuming sites change no markup for the stack fix. A site that added its own margins inside a `.stack` to work around it can remove them.

### Fixed

- `.stack` keeps the vertical rhythm. Each child sits `--stack-space` below the one before it: 16px, or the break of the child. 40px above an H2; 32px above an H3, an H4, `hero-actions` and `hero-trust`; 24px below a `type-hero-md`; 32px below a `type-hero`; 64px above a `hero-visual`; 24px below a fieldset. Before, the stack cleared every margin and set a flat 16px gap. The memregunes.com hero, a `type-hero-md`, a deck, buttons and a trust line in a stack, measured 16, 16 and 16px; it now measures 24, 32 and 32px, the same as the hero outside a stack, at 1440 and 390px.
- `--stack-space` does not inherit (`@property`), so a nested stack starts at 16px again.
- Inside a stack, a fieldset and a field no longer add their own margins to the gap. On the product-finder screen the space between fieldsets was 40px (24px margin plus the 16px gap); it is now 24px. The buttons below the last field moved from 32px to 16px.
- The space after a hero deck (1em) no longer overrides `hero-trust` and `hero-visual`. A deck followed by a trust line took 16px instead of 32px, and one followed by an image took 16px instead of 64px. Inside a stack, the stack sets this space. On the product screen the deck and the body text measured 33px (1em plus the gap); they now measure 16px.

### Added

- Two hero layouts with an image beside the text: `hero-split` (image on the right) and `hero-split--media-start` (image on the left), with `hero-split__media` on the figure. The text stays first in the markup, so a phone and a screen reader get it first. Below 760px the image follows the text. With text only and an image below (`hero-visual`), the hero has four layouts. `starter.html` renders a split hero.
- AG032 (warning): a homepage with no highlighter. AG025 warned only on a second stroke, so a homepage with none passed. The screens table derives the rule from the family: the marketing family (the homepage) takes one stroke, every other family at most one.

### Documentation

- `UI-KIT.md`: the four hero layouts, the stack rule, and "copy carries markup": a headline or a paragraph must be able to hold `<mark>`, `<strong>`, `<em>` and links. memregunes.com stored its hero copy as plain strings, so it had no place for its highlighter and bold.
- The house rule reads: the highlighter goes on one to four words of the main headline, once on the homepage and at most once on any other page.
- `DESIGN.md`: the hero section lists the four layouts and drops the rule that a homepage hero is text only.

## [7.4.2] - 2026-09-30

A defect patch from the final review of the contents list (v7.4.0). Emre chose 24px above the folded line on 2026-09-30. Consuming sites add `aria-hidden="true"` to the list title; nothing else in their markup changes.

### Fixed

- The folded line of the contents list sits 24px (`--space-xl`) below the page opening. It had no top margin, so on iesdesk.com it hugged the date line by 13px while the text below it started 40px lower.
- The visible title of the contents list takes `aria-hidden="true"`. A screen reader heard "On this page" twice: the `nav` label and the title.
- AG031 no longer warns when a page leaves a `<p>` open before the list. The checker closes the `<p>` the way a browser does.
- Astro adapter, `/typography`: the "Negative expression" tiles use `var(--cream)` for the lockup. They used `--footer-ink`, which is off-black since the footer became light in v7. The four house-brand lockups were invisible at 1:1, and the Ağustos lockup was off-black on red. Measured after the fix: 5.16:1 on red and 17.28:1 on off-black in light, 4.65:1 and 15.56:1 in the dark toggle.
- The Astro adapter builds from a clean clone on a Mac with Homebrew `vips`. The adapter now uses Astro's passthrough image service, so the build does not import sharp. Before, sharp tried to compile against the system libvips, the compile failed, and npm removed sharp without an error. `astro build` then failed with "Rollup failed to resolve import sharp". Every built page is byte-identical to the build before the change.
- `adapters/astro/package.json` and its lockfile root state v7.4.1. They stated v7.3.2.

### Documentation

- `UI-KIT.md` and `DESIGN.md`: AG031 reads full pages only, so a site that draws the list from a partial or a component needs its own page test.
- `MEMORY.md`: the 2026-09-30 page-contents record moves above the v7.3.x records, newest first.

## [7.4.1] - 2026-09-30

A defect patch for the checker. Found on WEBSITE-pldturkiye PR 52. Consuming sites change no markup; a site that loads `agustos-chrome.js` as a file only to avoid the warning can go back to a plain import.

### Fixed

- `check-agustos-ui.py` screen rules read markup only. Astro inlines a processed script under 4 KB, so a site that imports `agustos-chrome.js` from a `<script>` carried the selector `.site-sidebar[popover]` on every page, and `--screens-only` warned AG026 on each one. The rules now blank comments, inline `<script>` bodies and inline `<style>` bodies first. The same fix stops false AG024 (a `[data-theme]` selector in an inline style), AG025, AG027, AG028, AG029 and AG030 findings from inline code.
- Each screen warning gives the line of its own match. Before, the line came from the first copy of the matched text, so an AG026 or an AG025 pointed at a stylesheet or at the first highlighter.
- The kit's Astro adapter showed no AG026 only because its Header script, with the search code, is 4,926 bytes and is not inlined. The same page with the chrome script inlined gave AG026 before the fix and no finding after it.

### Documentation

- UI-KIT.md: the screen rules read markup only.
- The Astro adapter README names the current kit version (it still named v7.3.5).

## [7.4.0] - 2026-09-30

The "On this page" list, the first side column. Emre chose the pages, the behaviour and the phone layout on 2026-09-30 and approved the reader view from a live preview on iesdesk.com/privacy. Consuming sites add the markup to a long legal page; nothing else changes.

### Added

- `agustos-contents` with `__toggle`, `__title`, `__list` and `__link`: a `details` disclosure of the page's main sections, a direct child of `container--reading`. Below 1280px it is one folded line under the page opening. At 1280px and wider it sits in the side zone, open, and stays in view (`position: sticky` on `::details-content`); a tall list scrolls inside itself. It needs no script. A browser without `::details-content` keeps the folded line.
- `.container--reading` is `position: relative`.
- Checker warning AG031: an `agustos-contents` that is not a direct child of `container--reading`.
- `starter.html` shows one instance.
## [7.3.5] - 2026-09-30

A defect patch that closes issue 75. Emre chose two steps (option B) from a side-by-side preview. Consuming sites change no markup.

### Fixed

- A heading takes a fixed break above it: 40px (`--space-3xl`) above an H2, 32px (`--space-2xl`) above an H3 or an H4. Each heading took 2.5 times its own size (108px, 53px and 33px), so on the IESDesk Learn pages a subheading took 53px, more than the 40px above a chapter heading. The v7.3.4 H2 rule for reading pages is now the base rule and is removed.
- A heading that opens a `<section>` inside a kit section keeps the break of its level. The "containers own their edges" rule reached it and removed its space, so the IESDesk privacy notice showed 16px above each H3, the same as a paragraph gap.
- Measured in a browser before and after, on all 9 screens at 1440 and 390px: only the subheadings move (52.5px to 32px on `content`, `product-finder` and `static`). A 32.5px break rounds to 32px.

### Documentation

- DESIGN.md, "Vertical rhythm": Tier 2 states the two steps and the subsection rule.

## [7.3.4] - 2026-09-30

A defect patch. Emre approved it after the IESDesk About page showed 132px above each heading. Consuming sites change no markup.

### Fixed

- A reading page (`.container--reading`) is one article, so a section and an H2 in it take one break: 40px (`--space-3xl`). A section drops its band padding and takes a top margin, and a direct H2 or an H2 in `.prose` takes the same margin. The margin collapses with the last margin above it. Measured in a browser at 1440 and 390px: the `static` screen went from 121px and 144px to 40px, and the `content` screen from 108px and 123px to 40px. A home or product page keeps the section spacing.

### Documentation

- DESIGN.md, "Vertical rhythm": a new paragraph, "A reading page is one article".
- Issue 75 stays open for the H3 and H4 break (2.5em of the heading size).

## [7.3.3] - 2026-09-30

A patch from the 2026-09-30 design review. Emre chose the three defects plus the quick wins in one release. Consuming sites load `agustos-chrome.js` on every page with the chrome, and drop the `href` from any disabled link.

### Fixed

- An open drawer (`site-header__panel`, `site-sidebar`) closes when keyboard focus leaves it. Before, Tab after the last drawer item moved focus to the page behind the open drawer (measured at 390px on the home screen). A native popover does not do this, so `ui/agustos-chrome.js` does. The app shell now loads the script too.
- A disabled link is inert. `aria-disabled="true"` only restyled a link, so a click or Enter still followed its `href`. The contract is now: a link drops its `href` and takes `role="link"` and `aria-disabled="true"`.
- A search result excerpt takes `--ink` on the hover and focus fill, and its match mark moves to the paper. In the dark theme the excerpt was `#8a8378` on `#404040`, 2.76:1. A states row guards the pair.
- Table captions align to the start. Browsers center them, so the spec-sheet group labels sat centered over left-aligned tables.
- `color-scheme` follows the theme: light by default, dark under `data-theme="dark"`, light on the footer and the closing band. Scrollbars, checkboxes and select menus stayed light on the dark theme.
- A footer link hover is the 1px gray rule, as in the top menu. It drew the 2px red rule, which marks the current page alone (v7.1.0).
- Reduced motion sets `--dur: 0s`, which stops every transition. The hand-kept selector list had missed content links, the language link and the search controls.

### Added

- Checker warning AG030: a link with `aria-disabled="true"` that keeps its `href`.

### Documentation

- DESIGN.md no longer says a menu hover draws the red rule, and it states the one red-text exception (a content link hover on light paper).
- The `ss01` note is corrected: in Inter it switches to open digits (4, 6 and 9). It never changed the "a", which is two-storey by default.
- The guidelines PDFs are rebuilt (Emre asked, 2026-09-30). The Colour in use table shows the gray footer hover rule and the search result row.

## [7.3.2] - 2026-09-30

A defect patch. Emre approved it. Consuming sites that build their own header change one line: a parent section on a nested route takes `aria-current="true"`.

### Fixed

- A parent menu item on a nested route (for example `/haberler/` on `/haberler/guncel/`) carried `aria-current="page"`, so a screen reader announced the parent as the current page. The Astro header (`currentState()`) and the Rails helper (`agustos_nav_current`, which also drives the sidebar) now set `page` only on the exact route and `true` on an ancestor section. Trailing slashes do not count, `/` is only ever exact, and a link with a fragment or a query (`/about#team`) is never current. The WordPress example adds `true` to `wp_nav_menu` ancestors.
- Every chrome selector that highlights `[aria-current="page"]` (top-menu link, More summary, More link, sidebar link and group, `.agustos-chrome-link`) also matches `[aria-current="true"]`, so the section keeps the red rule. Breadcrumbs keep `page` only.
- The content, product and spec-sheet screens mark their parent menu item `true`.
- Every anchor offset adds `--anchor-snap` (1px). A browser scrolls to whole pixels, so a target at a fractional position stopped up to 0.5px under the 65px header in a Chromium probe. `--site-header-height` already equals the rendered header: 65px at 1440 and 375px, 126px with the phone search row.
- The adoption snippet no longer names a "sidebar brand". Every website uses the top menu and the footer; only product UI uses the sidebar.

### Added

- Checker warning AG029 (`--screens-only`, built pages): a link with `aria-current="page"` that points to a section above the page, or to home from a nested page.

## [7.3.1] - 2026-09-30

One reading line for every region. v7.2.0 put the text of a content page in the center of the frame, so on agustos.com the logo and the breadcrumbs started at 130px and the text at 393px: two left edges on one page. Emre compared the published layouts (Apple centers; GOV.UK, NN/g and 37signals keep the text on the left edge, GOV.UK and NN/g with a side column) and chose the left edge with a free side zone. Consuming sites change no markup.

### Changed

- `--measure-body` is 41rem (656px, about 75 characters of Inter at 16.5px) instead of 65ch. A `rem` line sits in the same place in every element; `ch` followed the font size of each element.
- `.container--reading` keeps the frame's left edge, and each block inside it stops at the reading line. The side zone to the right stays free for a side column.
- The footer site map splits on the same line: the contact block ends on it, and the groups fill the side zone after a `--space-xl` gap, the same gap as between the groups. Below 1280px the groups move under the contact block, because the side zone cannot hold three groups.
- Checker AG028 names the reading line instead of a centered column.

## [7.3.0] - 2026-09-30

One header search and language recipe in the kit (B2). Emre approved it from a before/after preview. Consuming sites load no search or language styles of their own; the Astro and Rails adapters drop theirs.

### Fixed

- Search text (status, group headings, result excerpts) and the language link use `--ink-soft` (10.37:1). They used `--ink-faint` (3.75:1), below the 4.5:1 text floor.
- The search input is 16px at every width. It was 14px on desktop, off the type scale.
- Below 1024px an in-page anchor lands below the whole header: `--site-header-search-height` (61px) adds the search row to the offset (126px on agustos.com). A site can drop a local offset script.
- The Astro icon button no longer draws a red rule on hover; it uses the gray tile, like the Rails one and the burger.
- Search result links use the regular weight; the bare link weight made the excerpts bold.

### Changed

- `tokens/web.css.tmpl` styles `site-header__search*`, `site-header__lang-link`, `site-header__utility*`, `site-header__icon-btn` and the theme icons. Sizes sit on the scale, spacing comes from `--space-*`, and the panel floats on the menu shadow and the 12px radius.
- The language link reads like the other chrome links: `bodyCompact`, medium weight, a 1px gray rule on hover.
- The Rails no-script search uses `agustos-input` and `agustos-button`.

## [7.2.0] - 2026-09-30

One reading column for content pages. On a 1440px screen the privacy page of iesdesk.com showed its text on the left 654px of a 1244px frame and nothing on the right, because `.prose` capped each paragraph while the column kept the full frame. The kit's own static screen did the same. Consuming sites moving from `v7.1.0` add `container--reading` next to `container` on each content page (About, privacy, terms, an article, a list of posts); nothing else in their markup changes.

### Added

- `.container--reading`: the whole column of a content page at the 65ch body measure plus the gutters, in the center of the frame. The line length stays the same (654px at 1440px); the empty space splits evenly on both sides.
- The screens table gains a derived Column: `reading` for the content family (`static`, `content`, `content-index`), `frame` for every other family. `UI-KIT.md`, `kit.json` and `docs/web.html` show it.
- Checker warning AG028: a full-width `container` on a content screen.

### Changed

- `screens/static.html`, `screens/content.html` and `screens/content-index.html`, and the Astro About, post and post-list pages, use the reading column. The Astro typography showcase keeps the frame.
- `DESIGN.md` states the line-length rule: 45 to 75 characters, 65ch in the kit, 80 as the WCAG 1.4.8 ceiling. Cap the column, not each paragraph.

## [7.1.0] - 2026-09-30

Chrome fixes from a best-practice audit of the top menu, the product sidebar and the footer against WCAG 2.2 and the WAI-ARIA disclosure pattern, each measured in Chromium. Consuming sites moving from `v7.0.x` add the drawer close button, `lang` on language links, and one `<script src="/vendor/agustos-ui/agustos-chrome.js" defer>`; nothing else in their markup changes.

### Fixed

- A focused element no longer hides under the sticky top menu (WCAG 2.2 SC 2.4.11); the anchor offset from v7.0.2 covers focus too.
- The top menu keeps one row at 1024px. Long Turkish labels wrapped it to two rows and grew the header from 65px to 137px; the row no longer wraps, and its spacing tightens between 1024 and 1279px. Five labels fit at 1024px up to about 65 characters together, More included.
- The More menu closes on Escape, an outside click or focus leaving, and Escape returns focus to it. It stayed open before.
- Each drawer has a visible close button (`site-header__close`, `site-sidebar__close`; `popovertargetaction="hide"`), and the page behind an open drawer no longer scrolls.
- A More menu or a closed sidebar group that holds the current page now shows the 2px red rule.
- Print drops the top menu, the sidebar, the drawers and the footer links; the footer keeps the lockup and its line.
- Language links carry `lang` as well as `hreflang`, so a Turkish screen reader pronounces "English" in English (WCAG SC 3.1.2). The starter, the screens and the Astro and Rails adapters set it.

### Changed

- A menu hover darkens the ink over a 1px gray rule (`--ink-faint`, 3.75:1 light, 4.95:1 dark); the 2px red rule marks the current page alone. Top menu, sidebar and chrome links (Emre chose option C from a preview, 2026-09-30). The `states` table gains the hover-rule row.
- Top-menu, sidebar and chrome links use the registered `bodyCompact` size (15.5px) instead of a literal 15px.
- The kit uses JavaScript only when it is the logical choice. `UI-KIT.md`, `DESIGN.md` and the CSS comments no longer say "No JavaScript".
- The footer may repeat top-menu pages in its site map; the one-row rule and "no column headings" are gone. No button still.

### Added

- `ui/agustos-chrome.js`, the kit's first script (about 15 lines, optional): it closes More. Without it More still opens and closes on click. The build copies it into the Astro (`src/scripts/`), Rails (`app/javascript/agustos/chrome.js`) and WordPress (`assets/js/`) adapters; the Astro header imports it, and the WordPress example enqueues it.
- Checker warning AG027: more than five top-menu items, the More toggle included.
- `screens/app-shell.html` shows a sidebar group, so the group has a reference instance.
- An optional footer site map: `site-footer__map`, `__contact` (the lockup and an `address`), `__groups`, `__group`, `__group-title` and `__group-links`; at most three groups of at most five links. The Ağustos screens and the starter show it with the company's registered name, address, phone, email and MERSİS number; the Pataraz screens keep the plain footer. The Astro and Rails footers take `address`, `contact` and `groups`. Emre approved it from a preview (2026-09-30).
- `sitemap.xml` guidance for every site, per adapter.
- Brand guidelines PDFs rebuilt for agustos, pataraz and pld (Emre, 2026-09-30): the Colour in use page shows the gray menu hover and the footer rows. Still 13 A4 pages. Rendered with Playwright's Chromium, with the same CSS page size and print backgrounds as the browse tool, because a cloud session has no browse tool.

## [7.0.2] - 2026-09-30

Two defects that the agustos.com adoption of v7.0.1 found. Consuming sites can move from `v7.0.1` to `v7.0.2` with no markup change.

### Fixed

- Top menu: an in-page anchor lands below the sticky `site-header`, not under it, at every width. The new `--site-header-height` (65px: the 44px target, 10px chrome padding above and below, and the rule) gives the menu its `min-height` and `html:has(.site-header)` its `scroll-padding-top`, so the two cannot drift.
- Astro and Rails adapters: a search result link keeps the 2px red focus ring. The adapters removed it with `outline: 0`.
- `tests/test_release_tags.py` clears the `GIT_*` variables. Under the pre-push hook, its scratch repository wrote `core.bare=true` and a test identity into this repository's config.

### Added

- `.github/workflows/tag-release.yml` and `scripts/release_tags.py`: each release is tagged `v<VERSION>` on its merge when it reaches `main`, from a local or a cloud session alike. The first run tags `v7.0.0` and `v7.0.1`, which a cloud session could not push.
- `/design-push` runs by itself at the start of a local Claude Code session on `main` (after a fast-forward pull) when that machine has not pushed the current bundle: a SessionStart hook in `.claude/settings.json` runs `scripts/sync_claude_design.py status --hook`, and the skill records each push with `mark-pushed`. Cloud sessions skip the check.

## [7.0.1] - 2026-09-30

Interactive states, measured in a browser in both themes and fixed. Consuming sites can move from `v7.0.0` to `v7.0.1` with no markup change.

### Fixed

- Form fields: the border uses `--ink-faint` (3.75:1 light, 4.95:1 dark, was 1.27:1) and the placeholder `--ink-soft` (10.37:1, was 3.75:1).
- Dark theme: a link or quiet-button hover dims the ink instead of turning text red (4.95:1, was 3.35:1). The red rule stays.
- Dark theme: the footer and the closing band scope the light colour roles back in. Footer links no longer vanish on hover (was 1.00:1), and a button in the closing band stays readable.
- Dark theme: the More menu hover is white on dark gray (10.37:1, was 1.19:1). In both themes it uses the functional gray, not the closing band's pale red.
- Dark theme: logos answer hover. House brands turn red; the Ağustos logo turns white.

### Added

- Pressed state: buttons move 1px down; the primary returns to full ink, the secondary fills light gray.
- Disabled buttons: `disabled` or `aria-disabled="true"` turns a button gray and stops hover and press.
- The `states` table in `tokens/design-tokens.json`: every state in both themes with its colour pair. The build refuses a pair below 4.5:1 (text) or 3:1 (borders, logos, focus). Published in `ui/kit.json` (`states`) and `docs/web.html`, summarised in `UI-KIT.md`.
- Brand guidelines, now 13 pages: "Colour in use" (the states table and the four state rules) and "Emphasis" (highlighter, bold, italic, underline, colour and capitals, with do and don't examples). Rebuilt for agustos, pataraz and pld.

### Changed

- Guidelines Typography page: headings are thin (hero and H1 at 300, H2 at 400, H3 at 500) with their sizes from the registry; 650 is the wordmark alone. It said 650 for headings.
- Emphasis rule: bold, italic and underline are never combined.

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

## [6.6.1] - 2026-09-29

### Fixed

- Below 1024px, an in-page anchor on a sidebar page lands below the sticky `site-sidebar-bar`. The bar covered the target, so a link such as `#y2010` showed only the line under the heading. The kit sets `scroll-padding-top` on `html` only when the page has the bar, so topbar pages and desktop do not change.

### Added

- `--sidebar-bar-height` (61px): the 44px target, 8px above and below, and the 1px rule. The bar and the scroll offset both read it.

## [6.6.0] - 2026-09-29

### Fixed

- Bare `h1`, `h2`, `h3`, `h4` and `p` share the rules of `.type-h1` to `.type-h4` and `.type-body`. `UI-KIT.md` promised that bare elements are styled, but only lists, tables, links, code, quotes and rules were. Markdown and CMS output rendered its headings and paragraphs in browser defaults.
- Footnotes and form hints lose a 12.5px top margin that came from the browser default for `p`. A form hint now sits 4px under its field, the field's own gap.
- The Astro adapter blog post page drops its hand-written heading and paragraph rules. They restated the kit with stale values, such as an 18px italic H3.

### Added

- `tests/test_bare_elements.py` reads the promise in `UI-KIT.md` and fails when a named element does not share the rule of its class.

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
