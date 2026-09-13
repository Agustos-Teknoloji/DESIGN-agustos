# Design Canvas pages

Four pages pulled verbatim from the Claude Design chat "Color palette and design direction",
project "Ağustos" (`uploads/Color palette and design direction (1)/`). These are raw
`.dc.html` Design Canvas artboards, not built `ui_kits/` pages, so
`scripts/sync_claude_design.py pull` cannot fetch them — its `--page` flag is locked to the
`ui_kits/` prefix. They were copied by hand instead.

## What is different here

- Each file is a single `.dc.html` document with an inline `Component` script (state,
  filters, configurator logic). There is no separate `.jsx`/`.css`/`index.html` split.
- Each file loads `./support.js` and, for the spec sheet, `./doc-page.js`. Those are
  Claude Design's own canvas-runtime scripts. They are not vendored into this repository,
  so these files will not render standalone in a browser here — open them inside the
  Claude Design project to preview them. No `index.png` screenshot was captured for the
  same reason.
- Cross-links between the four use sibling `.dc.html` filenames (`Products.dc.html`,
  `Product page.dc.html`, `Product Finder.dc.html`, `Spec sheet.dc.html`), matching how
  Claude Design links pages within one canvas.

## Files

| File | Design page | Pulled |
|---|---|---|
| `Products.dc.html` | Products | 2026-09-13 |
| `Product page.dc.html` | Product page | 2026-09-13 |
| `Product Finder.dc.html` | Product Finder | 2026-09-13 |
| `Spec sheet.dc.html` | Spec sheet | 2026-09-13 |

## When you build one of these

Same rule as the rest of `mockups/claude-design/`: read the markup here for intent only.
Rebuild the layout in the website repository with `ui/UI-KIT.md` and the kit classes. Do
not copy this markup or inline styles — the kit is generated from `tokens/`, not from
canvas exports.

## Built

All four are now built as real, standalone HTML — plain `ui/agustos.css` classes and
tokens, no framework — at [`mockups/products.html`](../../products.html),
[`mockups/product.html`](../../product.html), [`mockups/product-finder.html`](../../product-finder.html),
and [`mockups/spec-sheet.html`](../../spec-sheet.html). `python3 ui/check-agustos-ui.py mockups`
scores the four of them clean; the errors that command still reports all come from this
`canvas/` folder, which stays as reference and isn't meant to pass.
