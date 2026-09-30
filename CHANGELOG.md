# Changelog

All notable changes to the Ağustos Design System are documented in this file.

## [Unreleased]

### Fixed

- The Astro adapter builds from a clean clone on a Mac with Homebrew `vips`. The adapter now uses Astro's passthrough image service, so the build does not import sharp. Before, sharp tried to compile against the system libvips, the compile failed, and npm removed sharp without an error. `astro build` then failed with "Rollup failed to resolve import sharp". Every built page is byte-identical to the build before the change.
- `adapters/astro/package.json` and its lockfile root state v7.4.1. They stated v7.3.2.

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
