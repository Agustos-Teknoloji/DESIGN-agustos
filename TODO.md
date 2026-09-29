# DESIGN-agustos TODO

## Now

Design review fixes (2026-09-29, branch `claude/repo-design-review-dc3da5`). One commit per fix; kit release v6.3.0 at the end.

- [ ] FINDING-001: reset heading top margins inside `.agustos-card` and `.agustos-section__head` (flex containers never collapse margins).
- [ ] FINDING-002: move content text (breadcrumbs, table headers, labels, legends, `.type-h4`, `cite`, sidebar note) from `--ink-faint` to `--ink-soft`.
- [ ] FINDING-003: give the `pre` boxes on `docs/what-generates.html` ink text.
- [ ] FINDING-004: rescope ink inside `.band--cream` in dark theme so band text stays dark.
- [ ] FINDING-005: move the product descriptor below the H1 in `screens/product.html`; remove the eyebrow exception from `DESIGN.md`.
- [ ] FINDING-006: centre `.agustos-chrome-link` text in its 44px box.
- [ ] FINDING-008: align version labels in `DESIGN.md` and the docs with `VERSION`.
- [ ] FINDING-009: add the baseline gap after `.type-hero-deck` when a paragraph follows.
- [ ] FINDING-011: add a gap between sidebar link labels and their badges.
- [ ] FINDING-012: use `var(--radius-sm)` for inline code.
- [ ] Release: VERSION 6.3.0, build, `scripts/ci.sh`, CHANGELOG, MEMORY. Tag and `/design-push` only after Emre says yes.

## Next

- Register printer-matched CMYK and Pantone values for the six colours and the identity inks in `brand/brands.json`, then show them on the colour page of `brand/build_guidelines.py`. Ask the printer for a proof first; do not convert the screen values.
- Rebuild `adapters/astro/src/pages/blog/index.astro` on `type-dl` and `type-footnote`, like `screens/content-index.html`. Remove its scoped `<style>` block and the H2 for each post title, which break the list-page rule.
- Close PR #12 ("Register the SpecQuick house brand") as superseded, or rebase it on the root doc set. SpecQuick is already registered on `main`, and the PR still writes the old root `MEMORY.md`.
- Topbar menu: tighten the spacing of `site-header__nav` between 1024 and 1280px, so long Turkish labels fit on one row (Emre, 2026-09-27: for the future).
