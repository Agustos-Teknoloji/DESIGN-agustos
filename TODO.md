# DESIGN-agustos TODO

## Now

Bare element styles (2026-09-29, branch `fix/bare-element-styles`). Release v6.6.0. Emre asked for the best method.

- [x] Pair bare `h1` to `h4` and `p` with their `.type-*` rules in `tokens/web.css.tmpl`.
- [x] Compare every element on the nine screens and `ui/starter.html`, old CSS against new, at 1440px and 375px.
- [x] Remove the stale heading and paragraph rules from `adapters/astro/src/pages/blog/[...slug].astro`.
- [x] Add `tests/test_bare_elements.py`: it fails on v6.5.0 and passes now.
- [x] Record: `MEMORY.md` entry `2026-09-29 bare-elements-share-class-rules`, `CHANGELOG.md` for 6.6.0.
- [ ] Release: VERSION 6.6.0, build, `scripts/ci.sh`, tag `v6.6.0`, open the PR, and run `/design-push`.

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
