# DESIGN-agustos TODO

## Now

Chrome audit, plan only (2026-09-30, branch `claude/affectionate-ride-f41zre`). This plan checks the top menu, the sidebar and the footer against WCAG 2.2, the WAI-ARIA disclosure-navigation pattern and common B2B conventions. A Chromium probe of `ui/starter.html`, `screens/home.html` and `screens/app-shell.html` at 390, 1024, 1100, 1280 and 1440px measured every finding. Nothing is built yet: Emre approves the plan, then decides D1 to D3.

The kit already follows these practices: the skip link, 44px targets, `aria-current`, at most five items plus a click-to-open More, native popover drawers (Escape and backdrop close them, and the burger reports its expanded state), focus rings, reduced motion, an independently scrolling sidebar, the breadcrumb, and a light footer in a named `nav`.

Release A, defects (fix now, v7.1.0, because new classes are added):

- [ ] A1. The sticky header covers link targets. `#forms` lands at 0px under the 65px header, not the 85px that this file said before, and a focused element can hide under it too (WCAG 2.2 SC 2.4.11). Add `--site-header-height` from the registry and set `html:has(.site-header) { scroll-padding-top }`, as for the sidebar bar in v6.6.1.
- [ ] A2. The More menu stays open after Escape and after an outside click. Move it from `<details>` to a native popover (`popovertarget`, anchor-positioned under its item). This adds no JavaScript. In the drawer, show the More items flat, with no toggle. Style both markups for one release. D1.
- [ ] A3. The top menu wraps onto two rows at 1024 to 1179px with realistic Turkish labels ("Aydınlatma Tasarımı", "Proje Danışmanlığı", …). The header then grows from 65px to 137px. Set `nowrap` on the menu and narrow `recipes.chrome.gap` between 1024 and 1279px (Emre, 2026-09-27). Document a label budget in `UI-KIT.md`.
- [ ] A4. The drawers have no visible close button, and the page scrolls behind them. Add `site-header__close` and `site-sidebar__close` (`popovertargetaction="hide"`, no JavaScript), and lock page scroll while a drawer is open.
- [ ] A5. A parent item never shows the current page. When the current page sits under More or in a `site-sidebar__group`, the parent carries no mark. Style `:has([aria-current="page"])` on the More toggle and the group summary. The markup opens a group that holds the current page.
- [ ] A6. Printing shows the chrome. No `@media print` exists, so the sticky header, footer and drawers print on every sheet, including `spec-sheet`. Hide the chrome and remove sticky positioning in print.
- [ ] A7. The "English" link has `hreflang` but no `lang="en"`, so a Turkish screen reader mispronounces it (WCAG SC 3.1.2). Fix it in the starter, the screens and the three adapters.
- [ ] A8. The five-item rule has no check. The checker gets AG027, a warning for more than five direct top-menu items, so the rule reaches consuming sites.
- [ ] A9. Close-out: the starter, the nine screens (one sidebar group in `app-shell`), the Astro, Rails and WordPress adapters, the tests, `VERSION`, `CHANGELOG.md`, a `MEMORY.md` record, the build, the gate and `/design-push` from a local session.

Release B, design tweaks (the next monthly release, after Emre approves a before/after preview):

- [ ] B1. Hover looks the same as the current page: both show the 2px red rule, so hovering suggests a second "you are here". Hover darkens the ink only, and the red rule marks the current page alone. D2.
- [ ] B2. The kit has no search or language control. Astro and Rails each style their own `site-header__search*` and `site-header__lang-link`, about 35 rules each at off-scale 11, 12.5 and 14px. Move one recipe into `tokens/web.css.tmpl` and delete the adapter copies.
- [ ] B3. The footer has no slot for contact details. A B2B footer usually carries an address, phone and email. Turkish capital companies also publish a company-information page ("Bilgi toplumu hizmetleri", TTK 1524; confirm with legal) and a cookie policy. Add an optional `<address class="site-footer__contact">` line, with no columns, and list the recommended legal links in `UI-KIT.md`. D3.
- [ ] B4. The top-menu and sidebar links use a literal 15px. Use the registry `bodyCompact` size.

Decisions for Emre:

- D1. The More menu. Recommended: a native popover (no JavaScript, and Escape and outside click come free). The alternative is a 10-line script on `<details>`, which breaks the no-JavaScript rule.
- D2. The hover. Recommended: the ink darkens and there is no rule. The alternative is a 1px gray rule on hover.
- D3. The footer contact line. Recommended: yes, as an optional slot that a site can leave out.

Not recommended, because they add weight against the house rules: a mega menu, a header that hides on scroll, a sidebar that collapses to an icon rail, a footer site map in columns, and a back-to-top button.

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
