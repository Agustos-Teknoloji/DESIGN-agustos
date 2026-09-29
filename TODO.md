# DESIGN-agustos TODO

## Now

Middle type step and trust line (2026-09-29, branch `claude/37signals-design-philosophy-aaff31`). Release v6.5.0. Emre chose a global upright H3.

- [x] H3 becomes the middle step: `fontSize.h3` 18px to 22px in `tokens/design-tokens.json`. In `tokens/web.css.tmpl`, `.type-h3` drops `font-style: italic`, keeps weight 500, and sets line-height 1.25 and letter-spacing -0.015em.
- [x] Trust line: `.hero-trust` uses `{{foundations.fontSize.bodyCompact}}` (15.5px), not a hand-typed 13.5px.
- [x] Docs: update the `.type-h3` row, the Markdown mapping row ("Italic by token rule") and the two `.hero-trust` rows in `DESIGN.md` (hand-written, outside the generated block). Change the specimen text in `docs/fonts.html` ("Subsection in italic Tight").
- [x] Leave alone: `screens/design/` (pulled references), the Office templates (`heading3Size` is their own recipe), and the guidelines PDFs (they do not show the type scale).
- [x] Build, `--check`, `scripts/ci.sh`, and `check-agustos-ui.py screens --skip design`.
- [x] Browser check at 1440px and 375px: home, content, static, products, product-finder. Card titles, content subsections and the trust line. Confirm no card title wraps badly at 22px.
- [x] Record: `MEMORY.md` entry `2026-09-29 h3-upright-middle-step` (amends archive "Turning point 10": the italic was needed when H2 was small; size now separates H2 from H3). `CHANGELOG.md` for 6.5.0.
- [ ] Release: VERSION 6.5.0, tag `v6.5.0`, open the PR, and run `/design-push`.

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
