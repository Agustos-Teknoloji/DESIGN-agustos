# DESIGN-agustos TODO

## Now

Kit v7.3.5: two heading steps (2026-09-30, branch `claude/kit-7.3.5-heading-steps`). Emre chose option B. Record: MEMORY.md 2026-09-30 heading-steps. Closes issue 75.

- [x] H2 40px, H3 and H4 32px; the subsection rule; tests; DESIGN.md; `VERSION` 7.3.5; CHANGELOG; build; before and after diff of every heading on the 9 screens at 1440 and 390px.
- [ ] Gate, PR, merge. The tag follows the merge; the next local session on `main` runs `/design-push`.
- [ ] iesdesk.com: vendor v7.3.5 in APP-iesdesk.

Kit v7.3.4: one break above each heading on a reading page (2026-09-30, branch `claude/kit-7.3.4-reading-rhythm`). Emre approved the kit fix. Record: MEMORY.md 2026-09-30 reading-rhythm.

- [x] `.container--reading .agustos-section` and the H2 rule; test; DESIGN.md; `VERSION` 7.3.4; CHANGELOG; build; browser check of `static` and `content` at 1440 and 390px.
- [x] Gate, PR 79, merge, tag `v7.3.4`. The next local session on `main` runs `/design-push`.
- [x] iesdesk.com: vendor v7.3.4 in APP-iesdesk (PR 289, on dev.iesdesk.com).
- [ ] agustos.com, memregunes.com, pldturkiye.com: vendor v7.3.4 with the v7.3.2 rollout above.

Kit v7.3.3: design review defects and quick wins (2026-09-30, branch `claude/design-system-review-5d869b`). Emre chose option B: the three defects plus the quick wins in one patch. Record: MEMORY.md 2026-09-30 review-patch.

- [x] A1. An open drawer (`site-header__panel`, `site-sidebar`) closes when keyboard focus leaves it (`ui/agustos-chrome.js`); the app shell loads the script.
- [x] A2. A disabled link drops its `href` (`role="link"`, `aria-disabled="true"`); the checker warns on `aria-disabled="true"` with an `href`.
- [x] A3. A search result excerpt turns ink on hover and focus (2.76:1 in the dark theme before); a states row guards it.
- [x] Table captions align to the start.
- [x] `color-scheme` follows the theme, and the light islands stay light.
- [x] Footer link hover is the 1px gray rule; states rows follow.
- [x] Reduced motion sets `--dur: 0s` for every transition.
- [x] DESIGN.md: the red rule on menu hover (line 159) and the `ss01` note (open digits, not the "a").
- [x] Tests, `VERSION` 7.3.3, CHANGELOG, DESIGN.md, MEMORY.md, build, gate (234 tests), browser check at 390 and 1440px, PR. The tag and `/design-push` follow the merge on `main`.
- [x] Guidelines PDFs rebuilt (Emre asked, 2026-09-30): Ağustos, Pataraz and PLD, 13 pages each.

Kit v7.3.2 defect patch (2026-09-30, branch `claude/kit-7.3.2`). Emre approved it. Record: MEMORY.md 2026-09-30 aria-current-section and anchor-snap.

- [x] `aria-current="true"` on a parent section in the Astro, Rails (menu and sidebar) and WordPress adapters; the chrome CSS highlights `page` and `true`; the nested screens; checker AG029.
- [x] Adoption snippet: only product UI uses the sidebar.
- [x] Header height measured at 375 and 1440px (65px, 126px with the search row); every anchor offset adds `--anchor-snap`.
- [x] Tests, `VERSION` 7.3.2, CHANGELOG, DESIGN.md, build, gate, PR. The tag follows the merge; Emre runs `/design-push`.
- [ ] agustos.com: vendor v7.3.2 in WEBSITE-agustos; its header marks a parent section `true`.
- [ ] memregunes.com: vendor v7.3.2 with `scripts/vendor-kit.sh`, and mark `/writing/` and `/tr/yazdiklarim/` `true` on posts (AG029 finds 102).
- [ ] pldturkiye.com: vendor v7.3.2 into `apps/pld-astro/vendor/agustos-ui/` and use `currentState` in `Header.astro`. This closes the Codex aria-current finding on WEBSITE-pldturkiye PR 50.
- [ ] iesdesk.com: vendor v7.3.2 in APP-iesdesk, so the Rails menu and sidebar use `agustos_nav_current`.
- [ ] `/design-push` for v7.3.2: Emre, Friday 2 October (calendar reminder).

Reading line (v7.3.1, 2026-09-30, branch `claude/kit-7.2.1-reading-line`). Emre chose the left edge with a free side zone and one line shared with the footer. Record: MEMORY.md 2026-09-30 reading-line.

- [x] `--measure-body` 41rem; `.container--reading > *`; footer site map on the same line with the `--space-xl` gap, stacked below 1280px; AG028 text; docs; tests; `VERSION` 7.3.1.
- [x] Build, gate, browser check at 1440, 1280, 1024 and 390px; PR 73 merged, tag `v7.3.1`. `/design-push` follows in the next local session on `main`.
- [x] Vendor v7.3.1 into iesdesk.com (APP-iesdesk PR 283, live on dev.iesdesk.com; iesdesk.com with the next release) and agustos.com (WEBSITE-agustos PR 162, which also adopts v7.3.0 and drops its local search styles).

Kit v7.3.0: one search and language recipe (B2), 2026-09-30, branch `claude/kit-7.2-search-recipe`. Emre approved the order (company page, then this, then the memregunes.com and pldturkiye.com rollout on v7.3.0).

- [x] Move the header search, the language link, the icon button and the utility slot from the Astro and Rails adapters into `tokens/web.css.tmpl`; delete the adapter copies.
- [x] Fix while moving: text in `--ink-soft`, not `--ink-faint` (3.75:1 fails the 4.5:1 floor); the icon button hover is the gray tile, not a red rule; the search input is 16px everywhere; sizes on the scale (13, 15.5, 16px); spacing from `--space-*`; the panel floats on the one menu shadow and the 12px radius.
- [x] Phone anchor offset: below 1024px, `scroll-padding-top` adds the 61px search row when a page has one (the header is 126px on agustos.com); agustos.com then drops its local script.
- [x] Registry classes and states rows; checker; tests; docs.
- [x] Before/after preview for Emre (monthly-release rule), then `VERSION` 7.3.0, CHANGELOG, MEMORY, build, gate, PR, `/design-push`.

Reading column (v7.2.0, 2026-09-30, branch `claude/kit-7.2.0-reading-column`). Emre chose option B (a release of its own) and 7.2.0. Record: MEMORY.md 2026-09-30 reading-column.

- [x] `.container--reading`, the derived Column in the screens table, checker AG028, screens, Astro pages, docs, tests, `VERSION` 7.2.0, CHANGELOG.
- [ ] Build, gate, browser check at 1440 and 390px; commit, push, PR. The tag and `/design-push` follow the merge.
- [x] Bump iesdesk.com (PR 282) and agustos.com (PR 159) content pages to v7.2.0. Superseded by v7.3.1.
- [x] The header search draft (`claude/kit-7.2-search-recipe`) renames itself to 7.3.0 when it rebases.

Chrome audit and v7.1.0 (2026-09-30, branch `claude/affectionate-ride-f41zre`). The audit checked the top menu, the sidebar and the footer against WCAG 2.2, the WAI-ARIA disclosure-navigation pattern and common B2B conventions; a Chromium probe measured every finding. Emre decided D1 to D3 on 2026-09-30. Record: MEMORY.md 2026-09-30 chrome-best-practice-fixes.

Release A, defects, plus the approved tweaks B1 and B4 (v7.1.0):

- [x] A1. Anchors and focus land below the sticky header (SC 2.4.11). Shipped first in v7.0.2; merged here.
- [x] A2. `ui/agustos-chrome.js` closes More on Escape, an outside click or focus leaving; the kit says "JavaScript only when it is the logical choice" (D1).
- [x] A3. The top menu never wraps; spacing tightens between 1024 and 1279px; `UI-KIT.md` documents about 65 characters for five labels at 1024px.
- [x] A4. Drawer close buttons (`site-header__close`, `site-sidebar__close`) and a page scroll lock.
- [x] A5. More and a closed sidebar group show the current page inside them.
- [x] A6. `@media print` drops the chrome.
- [x] A7. `lang` on language links in the starter, the screens and the Astro and Rails adapters.
- [x] A8. Checker AG027 warns on a sixth top-menu item.
- [x] B1. Hover is a 1px gray rule; the 2px red rule marks the current page alone (D2, option C).
- [x] B4. Chrome links use the registered 15.5px `bodyCompact` size.
- [x] A9. Starter, screens (a sidebar group in `app-shell`), adapters, tests, `VERSION` 7.1.0, `CHANGELOG.md`, `MEMORY.md`, build, gate, browser check.
- [x] `/design-push` for v7.1.0 (2026-09-30, from Emre's Mac).
- [x] Guidelines PDFs rebuilt (Emre said yes, 2026-09-30): the states table shows the gray menu hover and the footer rows; 13 pages.

Footer and sitemap (v7.1.0), and the next chrome release (B2):

- [x] B2 (v7.2.0). The kit has no search or language control. Astro and Rails each style their own `site-header__search*` and `site-header__lang-link`, about 35 rules each at off-scale 11, 12.5 and 14px. Move one recipe into `tokens/web.css.tmpl` and delete the adapter copies.
- [x] B3. Footer site map (v7.1.0): the contact block from the İTO registry facts and three groups on the Ağustos screens and the starter; Astro and Rails take `address` and `groups`. Record: MEMORY.md 2026-09-30 footer-site-map.
- [x] B5. `sitemap.xml` guidance per adapter in `DESIGN.md` and the adapter READMEs. Astro already ships `@astrojs/sitemap`.
- [x] Footer phone and email (Emre, 2026-09-30): +90 850 885 1996, agustos@agustos.com.
- [x] The "Bilgi toplumu hizmetleri" page is live on agustos.com (2026-09-30, WEBSITE-agustos PR 158), with the İTO chamber number.

Not recommended, because they add weight against the house rules: a mega menu, a header that hides on scroll, a sidebar that collapses to an icon rail, and a back-to-top button.

v7.0.2 patch (2026-09-30, branch `claude/new-kit-worktrees-a927f9`). The agustos.com v7 adoption found two kit defects; Emre asked for the patch. Record: MEMORY.md 2026-09-30 topbar-anchor-offset.

- [x] `tokens/web.css.tmpl`: `--site-header-height` (65px, from the control minimum, the chrome padding and the rule) sets the top menu's `min-height` and `html:has(.site-header) { scroll-padding-top }`.
- [x] Astro and Rails adapters: a search result link keeps the red focus ring.
- [x] Tests for both; `VERSION` 7.0.2, CHANGELOG, MEMORY; build and gate green.
- [x] Commit, push, PR #65. The tag and `/design-push` follow the merge.
- [x] Bump agustos.com (PR #157) and iesdesk.com (PR #274) to v7.0.2; the agustos.com focus rule is gone. Its scroll script stays for the phone search row (see Next).
- [x] Both sites run kit v7.1.0 (2026-09-30): agustos.com #157 is live, iesdesk #274 merged and passed `bin/ci` in release #277.

v7.0.1 interactive states (2026-09-30, branch `claude/rails-html-template-kbacva`). Emre approved the fix, the white Ağustos logo hover on dark, and the guidelines rebuild. Record: MEMORY.md 2026-09-30 states-table-contract.

- [x] Browser probe of every element in rest, hover, focus and pressed, light and dark.
- [x] `tokens/web.css.tmpl`: field border and placeholder, dark hover, light islands, More hover, dark logo hover, pressed, disabled.
- [x] `states` table in the registry; the build refuses a failing pair; `kit.json`, `docs/web.html`, `UI-KIT.md`.
- [x] Guidelines: Colour in use, Emphasis, corrected Typography; PDFs rebuilt (13 pages).
- [x] Tests, docs, `VERSION` 7.0.1, gate green.
- [x] Tag `v7.0.1`: automatic since 2026-09-30 (release-tags-on-main).
- [x] `/design-push` for v7.0.1: covered by the v7.1.0 push (2026-09-30).

v7.0.0 conventional reset (2026-09-29, branch `claude/rails-html-template-kbacva`). Emre approved each part from the live preview and asked for it to ship without further approvals. Plan and facts: MEMORY.md 2026-09-29 v7-conventional-reset and the five records after it.

- [x] Registry: golden type scale, four weights, two radii, one section spacing, nine house rules, screens table without `primaryCtaMax` and `quotes`, class list.
- [x] `brand/brands.json`: drop `chrome` and `screenOverrides`. Office fingerprint narrowed to the fields Office reads; manifest rewritten, Office files unchanged.
- [x] `tokens/web.css.tmpl`: top menu with More, light one-row footer, two-button hero, section rhythm, cards, pale red band, black buttons, logo hover, highlighter, bold 600.
- [x] Build: chrome from the screen family; checker keeps identity errors, taste rules warn, AG022 and AG023 removed, AG025 and AG026 added.
- [x] Screens: eight website screens on the top menu and the simple footer; home shows the highlighter; listings use the H1.
- [x] Starter and Claude Design chrome cards on the v7 chrome.
- [x] Adapters (Astro, Rails, WordPress): v7 chrome, footer links API, More menu.
- [x] Per-brand favicons (tight crop at tab sizes, Emre: "crop") and the guidelines PDFs.
- [x] Hand-written docs: DESIGN.md, docs/*.html, README, ARCHITECTURE, HANDOFF, PATARAZ.
- [x] `AGENTS.md`, `ASSETS.md`.
- [x] Gate green, visual check, commit, push, draft PR #60.
- [x] Tag `v7.0.0`: automatic since 2026-09-30 (release-tags-on-main).
- [x] `/design-push` for v7.0.0: covered by the v7.1.0 push (2026-09-30).
- [x] Rollout: agustos.com and iesdesk.com run v7.1.0 (2026-09-30). memregunes.com (PR 31) and pldturkiye.com (PR 50) run v7.3.1 on their dev sites (2026-09-30); both go live at their launches.

## Next

- Design review 2026-09-29, open decisions for Emre:
  - Labels above headings remain on `screens/product-finder.html` (series above each card title), `screens/static.html` (role above each name) and `screens/content.html` (date above the H1). Decide whether a dateline is allowed, then move the rest below their headings.
  - App shell: the four stat cards do not need to be cards, and the marked one puts a 2px border on a rounded card. Try a `grid-4` of ruled figures.
  - App shell tabs have no tab semantics or arrow-key handling. Wire them up or use plain filter links.
  - "Six colours" is not literally true: `--ink-faint` #8a8378 and `--rule` #e8e4da are extra hexes, and dark `--ink-soft` reuses #8a8378. Either reword the contract or change the tokens.
  - Link hover turns text red on light paper, which reads as red used as an element's own colour. Since v7.0.1 the dark theme dims the ink instead. Confirm or change the light rule.
  - Handbook pages carry no chrome, copy `.book-nav` into each page, use their own 720px and 820px breakpoints, and `docs/handoff-setup.html` fills a bar with red.
  - Breakpoints 759px, 760px and 1023px have no token. Add one set to the registry.

- Design review 2026-09-30, for the monthly release (v7.3.3 shipped the defects and quick wins):
  - Screens: port the v7.3.0 search and language markup into all nine; they still use `agustos-chrome-link`. One page opening for breadcrumb, H1 and deck (`products` opens with `site-frame`, `content-index` with `container`: H1 at 44 vs 156px).
  - Type scale: map the six off-scale sizes (13.5, 15, 16, 20, 22, 26px) to steps or name them as tokens. Decide whether `ss01` (open digits) stays.
  - Tokens: a `--focus-ring` token for the 13 hand-typed rings; read `--measure-*` and `bodyCompact` through `var()`; one icon-button recipe; two hover idioms (a rule for links, a fill for menu rows).
  - Phone and tablet: product title before the media below 760px; finder results collapse inside `grid-aside` at 768px; year and download links reach 44px.
  - Docs: one entry point (DESIGN.md:7 vs UI-KIT.md:3); cut the Versioning paragraph to the current release; drop v3 and v5 remnants; "topbar" to "top menu"; six brands, not five; the browser baseline is 2024 (`:has()`, `popover`), not 2022.
  - Best practice: a component status and a deprecation window for the aliases; `prefers-color-scheme` for product UI; `required` and `aria-describedby` in the starter form; per-brand favicons on the Pataraz and IESDesk screens.

- Register printer-matched CMYK and Pantone values for the six colours and the identity inks in `brand/brands.json`, then show them on the colour page of `brand/build_guidelines.py`. Ask the printer for a proof first; do not convert the screen values.
- Rebuild `adapters/astro/src/pages/blog/index.astro` on `type-dl` and `type-footnote`, like `screens/content-index.html`. Remove its scoped `<style>` block and the H2 for each post title, which break the list-page rule.
