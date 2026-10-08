# DESIGN-agustos TODO

## Now

- [x] Kit v7.11.2: hover only where a mouse hovers, and long words break (MEMORY.md 2026-10-08 touch-fixes).
- [ ] Before/after phone screenshots to Emre, then merge. After the merge on `main`: `/design-push`.
- [ ] memregunes.com vendors v7.11.2 and deletes its `#audience` rule in `src/styles/home.css` (WEBSITE-memregunes MEMORY 2026-10-06 consulting-first-part, "reopen if").

## Next

- Ask Emre whether to rebuild the brand guidelines PDFs now that `banuucak` joined the family (AGENTS.md: a brand that joins needs his yes). Rebuild only on his yes.
- banuucak exports when Emre asks: `brand/build.py` for the banuucak favicon kit and lockups, then ASSETS.md. Until then banuucak.com uses the generic black-sun favicon, which every non-Ağustos brand shares.
- agustos.com, memregunes.com and pldturkiye.com adopt v7.7.0 (follow-up list in the v7.7.0 plan).
- Run the Astro and Rails adapter test suites in `scripts/ci.sh`. Today they run only by hand, so the gate does not see an adapter that breaks the kit contract.
- pataraz2 (dev.pataraz.com) still runs kit v6.1.0. Move it to v7 in its own task: top menu, light footer, `agustos-chrome.js`, then the v7.x consumer changes. It needs a before/after preview for Emre.
- Photo viewer recipe, taken from banuucak.com (WEBSITE-banuucak PR 18; its MEMORY.md, 2026-10-06 photo-viewer). A click on a photo in an article opens it large in a native `<dialog>` on `--paper`. The controls are `agustos-button` text labels (Önceki, Sonraki, Kapat) and a counter. The arrow keys and a swipe step through the photos of the page, Esc closes the viewer, and the focus goes back to the photo. The script has about 80 lines and no library. The large photo reuses the `srcset` of the page with `sizes="100vw"`, so a site makes no new file. Files to lift: `src/components/PhotoViewer.astro`, `src/scripts/photo-viewer.js` and the `photo-viewer*` rules in `src/styles/site.css`. To ship it in the kit: the classes in `tokens/web.css.tmpl`, the script beside `agustos-chrome.js`, a recipe in `ui/UI-KIT.md` next to the article media recipe of the 2026-10-01 audit, and a gallery case on `screens/content.html`. Use `--focus-ring` once that token exists. Open decision for Emre: a paper or a dark background (banuucak uses paper, because no other screen is dark). Ship it in a monthly release after a before/after preview. Until then, a site that needs a viewer copies the banuucak files.
- Give a reference screen the three v7.6.2 cases (a meta line with no deck, a contents list under a breadcrumb, a meta line in a stack), so the screen sweep covers them. No screen held them, so v7.6.0 shipped all three defects.
- Kit audit 2026-10-01 (three reviews; the v7.5.0 stack fix closed the first finding of each):
  - CSS structure: cascade layers (`reset < base < components < layout < utilities`), after an audit of each site, because every unlayered consumer rule then wins; components drop outer margins, so layout owns all spacing; container queries for cards and grids in columns; `overflow-wrap` on body, so a long Turkish word or a URL cannot overflow a 375px phone; `forced-colors` rules.
  - Checker (12 of 59 UI-KIT rules fully enforced): AG009 reads component `<style>` blocks (12 hidden overrides on agustos.com, 1 on PLD); hero and closing band per screen; red beyond backgrounds (`color`, `fill`, borders); off-scale font sizes and weights of 700 and up; move the repository-test rules (header and footer, no footer button, `lang`) into the checker; a way to run the screen rules on the Rails site, which has no static build.
  - Docs: ship `screens/` with the kit, because a consumer agent never receives them; a "page type to screen and recipe" table (contact, pricing, FAQ, case study, 404, data table); replace "do the conventional thing" with "stop and ask for a recipe"; recipes for form states, article media and footnotes, pagination, image ratio and placeholder; fix the starter's contradictions (an eyebrow above the H1, "paper (cream, default)").
- Add a theme-invariant reverse-ink token (cream or white) to the registry for negative lockups, and use it on the Astro `/typography` negative tiles. In the dark toggle the house-brand tiles are off-black on off-black paper, so their edge disappears; decide whether the tile needs a rule. See MEMORY.md, negative-tile-cream.
- Design review 2026-09-29, open decisions for Emre:
  - Labels above headings remain on `screens/product-finder.html` (series above each card title) and `screens/static.html` (role above each name). Move them below their headings, like the date in v7.6.0 (no dateline above a title: Emre chose option D on 2026-10-01).
  - Checker: warn when a page puts a line above its H1 (the v7.6.0 page-opening rule), so consuming sites find their old datelines.
  - App shell: the four stat cards do not need to be cards, and the marked one puts a 2px border on a rounded card. Try a `grid-4` of ruled figures.
  - App shell tabs have no tab semantics or arrow-key handling. Wire them up or use plain filter links.
  - "Six colours" is not literally true: `--ink-faint` #8a8378 and `--rule` #e8e4da are extra hexes, and dark `--ink-soft` reuses #8a8378. Either reword the contract or change the tokens.
  - Link hover turns text red on light paper, which reads as red used as an element's own colour. Since v7.0.1 the dark theme dims the ink instead. Confirm or change the light rule.
  - Handbook pages carry no chrome, copy `.book-nav` into each page, use their own 720px and 820px breakpoints, and `docs/handoff-setup.html` fills a bar with red.
  - Breakpoints 759px, 760px and 1023px have no token. Add one set to the registry.

- Design review 2026-09-30, for the monthly release (v7.3.3 shipped the defects and quick wins):
  - Screens: port the v7.3.0 search and language markup into all nine; they still use `agustos-chrome-link`. One page opening for breadcrumb, H1 and deck (`products` opens with `site-frame`, `content-index` with `container`: H1 at 44 vs 156px).
  - Type scale: map the six off-scale sizes (13.5, 15, 16, 20, 22, 26px) to steps or name them as tokens. Decide whether `ss01` (open digits) stays.
  - Tokens: a `--focus-ring` token for the 13 hand-typed rings; read `--measure-*` and `bodyCompact` through `var()`; one icon-button recipe; two hover idioms (a rule for links, a fill for menu rows).
  - Phone and tablet: product title before the media below 760px; finder results collapse inside `grid-aside` at 768px; year and download links reach 44px.
  - Docs: one entry point (DESIGN.md:7 vs UI-KIT.md:3); cut the Versioning paragraph to the current release; drop v3 and v5 remnants; "topbar" to "top menu"; six brands, not five; the browser baseline is 2024 (`:has()`, `popover`), not 2022.
  - Best practice: a component status and a deprecation window for the aliases; `required` and `aria-describedby` in the starter form; per-brand favicons on the Pataraz and IESDesk screens.

- Brand guidelines PDF, three candidate pages from the 2026-10-01 comparison with common practice. No standard sets the sections; agency guides name seven, and these three are missing. Each one needs Emre's yes before the PDFs are rebuilt (MEMORY.md, guidelines-rebuild-on-request).
  - Tone of voice: a short page from `standards/voice.md` in the SKILL-writing repo.
  - Application examples: one real use for each section (letterhead, email signature, social post, datasheet), not only the file list.
  - Accessibility: one line on "Colour in use", "Text on any background keeps 4.5:1 contrast (WCAG 2.2 AA)", so partners who make their own material follow the kit's floors.
- Register printer-matched CMYK and Pantone values for the six colours and the identity inks in `brand/brands.json`, then show them on the colour page of `brand/build_guidelines.py`. Ask the printer for a proof first; do not convert the screen values.
- Rebuild `adapters/astro/src/pages/blog/index.astro` on `type-dl` and `type-footnote`, like `screens/content-index.html`. Remove its scoped `<style>` block and the H2 for each post title, which break the list-page rule.
- Kit against the good-css list, 2026-10-08 (MEMORY.md, good-css-skill and touch-fixes). v7.11.2 shipped the touch hover and the long-word break. For the monthly release, with a before/after preview:
  - An `:active` state on every link and menu row (buttons have one; 3 rules today), then remove the grey tap flash. Touch users then get press feedback everywhere.
  - `text-wrap: pretty` on body text, so a paragraph does not end on one short word. Headings already balance.
  - `100svh` in place of `100vh` on `body`, so a short page fits the phone screen under the browser bar.
  - Remove `text-rendering: optimizeLegibility` from `html, body`. `font-feature-settings` already turns kerning on.
  - The type scale in rem, together with the six off-scale sizes (Design review 2026-09-30, Type scale). Then every size follows the reader's browser font size; at the default 16px nothing moves.
  - Skipped on 2026-10-08: safe-area insets (no site uses `viewport-fit=cover`), `overflow: clip` (three of the six rules lock the page behind the open menu), `font-synthesis: none` (a site without the italic files loses its italics), `scrollbar-gutter: stable`, `field-sizing` and `:user-invalid` (no form needs them yet).
