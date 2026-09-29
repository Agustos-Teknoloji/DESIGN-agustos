# DESIGN-agustos TODO

## Now

v7.0.0 conventional reset (2026-09-29, branch `claude/rails-html-template-kbacva`). Emre approved each part from the live preview and asked for it to ship without further approvals. Plan and facts: MEMORY.md 2026-09-29 v7-conventional-reset and the five records after it.

- [x] Registry: golden type scale, four weights, two radii, one section spacing, nine house rules, screens table without `primaryCtaMax` and `quotes`, class list.
- [x] `brand/brands.json`: drop `chrome` and `screenOverrides`. Office fingerprint narrowed to the fields Office reads; manifest rewritten, Office files unchanged.
- [x] `tokens/web.css.tmpl`: top menu with More, light one-row footer, two-button hero, section rhythm, cards, pale red band, black buttons, logo hover, highlighter, bold 600.
- [x] Build: chrome from the screen family; checker keeps identity errors, taste rules warn, AG022 and AG023 removed, AG025 and AG026 added.
- [x] Screens: eight website screens on the top menu and the simple footer; home shows the highlighter; listings use the H1.
- [x] Starter and Claude Design chrome cards on the v7 chrome.
- [ ] Adapters (Astro, Rails, WordPress): v7 chrome, footer links API, More menu.
- [ ] Per-brand favicons and the guidelines PDFs.
- [ ] Hand-written docs: DESIGN.md, docs/*.html, README, ARCHITECTURE.
- [ ] `AGENTS.md`, `ASSETS.md`.
- [ ] Gate green, visual check, commit, push, tag `v7.0.0`, draft PR, `/design-push`.
- [ ] Rollout: agustos.com and iesdesk.com pin v7.0.0 first; memregunes.com and pldturkiye.com later.

## Next

- Design review 2026-09-29, open decisions for Emre:
  - Labels above headings remain on `screens/product-finder.html` (series above each card title), `screens/static.html` (role above each name) and `screens/content.html` (date above the H1). Decide whether a dateline is allowed, then move the rest below their headings.
  - App shell: the four stat cards do not need to be cards, and the marked one puts a 2px border on a rounded card. Try a `grid-4` of ruled figures.
  - App shell tabs have no tab semantics or arrow-key handling. Wire them up or use plain filter links.
  - "Six colours" is not literally true: `--ink-faint` #8a8378 and `--rule` #e8e4da are extra hexes, and dark `--ink-soft` reuses #8a8378. Either reword the contract or change the tokens.
  - Link hover turns text red, which reads as red used as an element's own colour. Confirm or change the rule.
  - Handbook pages carry no chrome, copy `.book-nav` into each page, use their own 720px and 820px breakpoints, and `docs/handoff-setup.html` fills a bar with red.
  - Breakpoints 759px, 760px and 1023px have no token. Add one set to the registry.

- Register printer-matched CMYK and Pantone values for the six colours and the identity inks in `brand/brands.json`, then show them on the colour page of `brand/build_guidelines.py`. Ask the printer for a proof first; do not convert the screen values.
- Rebuild `adapters/astro/src/pages/blog/index.astro` on `type-dl` and `type-footnote`, like `screens/content-index.html`. Remove its scoped `<style>` block and the H2 for each post title, which break the list-page rule.
- Close PR #12 ("Register the SpecQuick house brand") as superseded, or rebase it on the root doc set. SpecQuick is already registered on `main`, and the PR still writes the old root `MEMORY.md`.
- Topbar menu: tighten the spacing of `site-header__nav` between 1024 and 1280px, so long Turkish labels fit on one row (Emre, 2026-09-27: for the future).
