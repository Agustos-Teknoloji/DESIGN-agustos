# Screens

One reference page per screen type, hand-written on kit classes only. The rules for each
screen live in the `screens` table in `tokens/design-tokens.json`. `ui/UI-KIT.md`,
`ui/kit.json`, `docs/web.html`, and the Claude Design cards render from that table.

<!-- generated: screens.table -->
| Screen | File | Family | Sample brand | Chrome |
|---|---|---|---|---|
| home | `home.html` | marketing | agustos | topbar |
| static | `static.html` | content | agustos | topbar |
| content | `content.html` | content | agustos | topbar |
| content-index | `content-index.html` | content | agustos | topbar |
| products | `products.html` | catalog | pataraz | topbar |
| product-finder | `product-finder.html` | catalog | pataraz | topbar |
| product | `product.html` | catalog | pataraz | topbar |
| spec-sheet | `spec-sheet.html` | document | pataraz | topbar |
| app-shell | `app-shell.html` | product UI | iesdesk | sidebar |
| app-top-menu | `app-top-menu.html` | product UI | iesdesk | topbar |
<!-- /generated -->

## Rules

1. A complete HTML document with `lang="tr"` (`lang="en"` for the product UI screens).
2. Load `../ui/agustos-fonts.css`, then `../ui/agustos.css`. Website screens also load
   `../ui/agustos-chrome.js` with `defer`. Link the canonical favicon.
3. `body` carries `brand-<slug>`, `data-screen="<name>"`, and `site-sidebar-layout` when the
   screen's chrome is the sidebar.
4. Kit classes only. No `style` attribute. No `<style>` element. No script, except the kit's
   `agustos-chrome.js` on every screen and, on a screen with a theme switch, the one-line theme
   script from `kit.json` (`themeScript`) in `<head>`, before the stylesheets.
5. Images come from this repository or are gray wells. No external URL.
6. Swap the `brand-*` class for another house brand and use that brand's chrome.
7. `python3 ui/check-agustos-ui.py screens --skip design` exits 0. `tests/test_screens.py`
   enforces every rule above, the primary CTA limit, and the quote rule.

## Preview

Run `python3 -m http.server 4390` at the repository root (or start the `agustos-docs` entry in
`.claude/launch.json`) and open `http://localhost:4390/screens/home.html`. The generated index
`docs/web.html` frames every screen with its rules.

## Claude Design references

Pages pulled from Claude Design land under [`design/`](design/), with the status table in
[`design/README.md`](design/README.md). Nothing in this folder imports them.
