# DESIGN-agustos TODO

## Now

Design review fixes (2026-09-29, branch `claude/repo-design-review-dc3da5`). One commit per fix; kit release v6.3.0 at the end.

- [x] FINDING-001: reset heading top margins inside `.agustos-card` and `.agustos-section__head` (flex containers never collapse margins).
- [x] FINDING-002: move content text (breadcrumbs, table headers, labels, legends, `.type-h4`, `cite`, sidebar note) from `--ink-faint` to `--ink-soft`.
- [x] FINDING-003: give the `pre` boxes on `docs/what-generates.html` ink text.
- [x] FINDING-004: rescope ink inside `.band--cream` in dark theme so band text stays dark.
- [x] FINDING-005: move the product descriptor below the H1 in `screens/product.html`; remove the eyebrow exception from `DESIGN.md`.
- [x] FINDING-006: centre `.agustos-chrome-link` text in its 44px box.
- [x] FINDING-008: align version labels in `DESIGN.md` and the docs with `VERSION`.
- [x] FINDING-009: add the baseline gap after `.type-hero-deck` when a paragraph follows.
- [x] FINDING-011: add a gap between sidebar link labels and their badges.
- [x] FINDING-012: use `var(--radius-sm)` for inline code.
- [x] Release: VERSION 6.3.0, build, `scripts/ci.sh`, CHANGELOG, MEMORY.
- [x] Tag `v6.3.0`, open PR #54, and run `/design-push` (Emre, 2026-09-29).

## Next

- Design review 2026-09-29, open decisions for Emre:
  - Card and breadcrumb targets: the kit says a card with one link makes the card the target, but no stretched-link rule exists, and breadcrumb anchors are 21px tall. Add both to the kit and the checker.
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
