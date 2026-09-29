# DESIGN-agustos TODO

## Now

Sidebar bar anchor offset (2026-09-29, branch `fix/sidebar-bar-anchor-offset`). Release v6.6.1. Found in the memregunes speakers review: below 1024px the sticky `site-sidebar-bar` covers the target of an in-page anchor.

- [x] Add `--sidebar-bar-height` from existing tokens, and `scroll-padding-top` on `html` under the 1024px query, only when the page has a `site-sidebar-bar`.
- [x] Test: the variable is built from tokens, and the topbar and desktop get no scroll padding.
- [x] Verify in a browser at 375px (anchor lands below the bar), at 1440px (no change) and on a topbar screen (no change).
- [x] Record: `MEMORY.md` entry `2026-09-29 sidebar-bar-scroll-padding`, `CHANGELOG.md` for 6.6.1, `UI-KIT.md` variable list.
- [ ] Release: VERSION 6.6.1, build, `scripts/ci.sh`, tag `v6.6.1`, PR, `/design-push`.

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
- Topbar anchors: the sticky `site-header` (85px) covers an in-page anchor target at every width. Give it the same `scroll-padding-top` fix as the sidebar bar in v6.6.1, from a `--site-header-height` variable.
- Topbar menu: tighten the spacing of `site-header__nav` between 1024 and 1280px, so long Turkish labels fit on one row (Emre, 2026-09-27: for the future).
