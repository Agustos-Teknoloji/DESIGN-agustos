# DESIGN-agustos TODO

## Now

Chrome audit and v7.1.0 (2026-09-30, branch `claude/affectionate-ride-f41zre`). The audit checked the top menu, the sidebar and the footer against WCAG 2.2, the WAI-ARIA disclosure-navigation pattern and common B2B conventions; a Chromium probe measured every finding. Emre decided D1 to D3 on 2026-09-30. Record: MEMORY.md 2026-09-30 chrome-best-practice-fixes.

Release A, defects, plus the approved tweaks B1 and B4 (v7.1.0):

- [x] A1. `--site-header-height` (65px) sets `scroll-padding-top`, so anchors and focus land below the sticky header (SC 2.4.11).
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
- [ ] `/design-push` for v7.1.0: runs by itself in the next local Claude Code session on `main`.
- [x] Guidelines PDFs rebuilt (Emre said yes, 2026-09-30): the states table shows the gray menu hover and the footer rows; 13 pages.

Footer and sitemap (v7.1.0), and the next chrome release (B2):

- [ ] B2. The kit has no search or language control. Astro and Rails each style their own `site-header__search*` and `site-header__lang-link`, about 35 rules each at off-scale 11, 12.5 and 14px. Move one recipe into `tokens/web.css.tmpl` and delete the adapter copies.
- [x] B3. Footer site map (v7.1.0): the contact block from the İTO registry facts and three groups on the Ağustos screens and the starter; Astro and Rails take `address` and `groups`. Record: MEMORY.md 2026-09-30 footer-site-map.
- [x] B5. `sitemap.xml` guidance per adapter in `DESIGN.md` and the adapter READMEs. Astro already ships `@astrojs/sitemap`.
- [x] Footer phone and email (Emre, 2026-09-30): +90 850 885 1996, agustos@agustos.com.
- [ ] Emre publishes the "Bilgi toplumu hizmetleri" page on agustos.com (contents confirmed with the legal advisor).

Not recommended, because they add weight against the house rules: a mega menu, a header that hides on scroll, a sidebar that collapses to an icon rail, and a back-to-top button.

v7.0.1 interactive states (2026-09-30, branch `claude/rails-html-template-kbacva`). Emre approved the fix, the white Ağustos logo hover on dark, and the guidelines rebuild. Record: MEMORY.md 2026-09-30 states-table-contract.

- [x] Browser probe of every element in rest, hover, focus and pressed, light and dark.
- [x] `tokens/web.css.tmpl`: field border and placeholder, dark hover, light islands, More hover, dark logo hover, pressed, disabled.
- [x] `states` table in the registry; the build refuses a failing pair; `kit.json`, `docs/web.html`, `UI-KIT.md`.
- [x] Guidelines: Colour in use, Emphasis, corrected Typography; PDFs rebuilt (13 pages).
- [x] Tests, docs, `VERSION` 7.0.1, gate green.
- [x] Tag `v7.0.1`: automatic since 2026-09-30 (release-tags-on-main).
- [ ] `/design-push` for v7.0.1: runs by itself in the next local Claude Code session (2026-09-30 design-push-at-session-start).

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
- [ ] `/design-push` for v7.0.0: covered by the v7.0.1 push in the next local session.
- [ ] Rollout: agustos.com and iesdesk.com pin v7.0.0 first; memregunes.com and pldturkiye.com later.

## Next

- Design review 2026-09-29, open decisions for Emre:
  - Labels above headings remain on `screens/product-finder.html` (series above each card title), `screens/static.html` (role above each name) and `screens/content.html` (date above the H1). Decide whether a dateline is allowed, then move the rest below their headings.
  - App shell: the four stat cards do not need to be cards, and the marked one puts a 2px border on a rounded card. Try a `grid-4` of ruled figures.
  - App shell tabs have no tab semantics or arrow-key handling. Wire them up or use plain filter links.
  - "Six colours" is not literally true: `--ink-faint` #8a8378 and `--rule` #e8e4da are extra hexes, and dark `--ink-soft` reuses #8a8378. Either reword the contract or change the tokens.
  - Link hover turns text red on light paper, which reads as red used as an element's own colour. Since v7.0.1 the dark theme dims the ink instead. Confirm or change the light rule.
  - Handbook pages carry no chrome, copy `.book-nav` into each page, use their own 720px and 820px breakpoints, and `docs/handoff-setup.html` fills a bar with red.
  - Breakpoints 759px, 760px and 1023px have no token. Add one set to the registry.

- Register printer-matched CMYK and Pantone values for the six colours and the identity inks in `brand/brands.json`, then show them on the colour page of `brand/build_guidelines.py`. Ask the printer for a proof first; do not convert the screen values.
- Rebuild `adapters/astro/src/pages/blog/index.astro` on `type-dl` and `type-footnote`, like `screens/content-index.html`. Remove its scoped `<style>` block and the H2 for each post title, which break the list-page rule.
- Close PR #12 ("Register the SpecQuick house brand") as superseded, or rebase it on the root doc set. SpecQuick is already registered on `main`, and the PR still writes the old root `MEMORY.md`.
