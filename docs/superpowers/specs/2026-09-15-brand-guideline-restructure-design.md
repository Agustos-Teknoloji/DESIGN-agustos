# Brand guideline restructure — design

**Date:** 2026-09-15
**Status:** approved design, pending implementation plan
**Branch:** `claude/brand-guideline-repo-9ba5e3`
**Release:** v6.0.0
**Related:** [DESIGN.md](../../../DESIGN.md), [AGENTS.md](../../../AGENTS.md), [ui/UI-KIT.md](../../../ui/UI-KIT.md), [2026-09-13-claude-design-sync-design.md](2026-09-13-claude-design-sync-design.md), [archive/MEMORY.md](../../../archive/MEMORY.md)

## 1. Goal

Make this repository a brand guideline that an agent or a person reads cold and designs from.
The guideline covers the logo, the colours, the type, the chrome, light and dark, and one
reference page per screen type. It keeps a working two-way loop with the Claude Design project.

Done means:

1. An agent that has only `ui/UI-KIT.md` and `screens/` builds any of the eight page types for
   any house brand, with the correct chrome, without inventing CSS.
2. Every rule that applies per screen lives once, in the token registry, and every document,
   card, and checker reads it from there.
3. A page drawn in Claude Design lands beside the screen it updates, and the rebuilt screen
   goes back to Claude Design as a card, each with one command.

## 2. Decisions locked

| Date | Decision | Where recorded |
|---|---|---|
| 2026-09-15 | Plain CSS everywhere. No Tailwind in this repository or in any consuming site. | `archive/MEMORY.md`, "Vanilla CSS, no Tailwind" |
| 2026-09-15 | Two chromes ship in the kit: a sidebar and a topbar with footer. Each brand registers one. | this spec, §5 |
| 2026-09-15 | Chrome per brand: agustos sidebar, pataraz topbar, pld topbar, iesdesk sidebar, specquick sidebar. | this spec, §5.4 |
| 2026-09-15 | agustos.com keeps its sidebar. The live site ships a 240px fixed sidebar on every page; the July 2026 topbar record in `DESIGN.md` did not match the live site. | `tasks/lessons.md` lesson 3 |
| 2026-09-15 | Dark theme is allowed on product UI only. Product UI uses the sidebar as its app shell. | this spec, §8 |
| 2026-09-15 | About is the `static` screen, content family: 65ch measure, quotes allowed, one reserved people-or-place photo slot, no hero CTA, one closing cream band. The same screen serves privacy, terms, and the KVKK notice. | this spec, §7 |
| 2026-09-15 | Registry-driven build (approach A). Screens stay hand-written HTML on kit classes; the generator renders every table, index, and card from the registry. | this spec, §4 |
| 2026-09-15 | All three consumers at once: the Claude Design loop, pataraz.com, and agustos.com. One release. | this spec, §14 |

## 3. Current state

The `/dhh` review of 2026-09-15 found six problems, in order:

1. The site chrome is not in the kit. Six implementations of one header exist: three full copies
   under `mockups/`, one in `docs/web.html`, one in the Astro adapter, one in the Rails adapter.
2. No single artifact is "a screen". The product page exists in five places under five names.
3. The Claude Design pull is locked to `ui_kits/`. The four real screens were copied from the
   canvas by hand and rebuilt by hand.
4. The design direction has one machine source and three hand copies.
5. Per-screen rules are prose that the checker cannot read.
6. Root nits: a stale hero example, a PowerPoint script with pre-v5 colours, a stale version
   line, a Tailwind contradiction, and the "do not zip the factory" text in four files.

Verified on the live site on 2026-09-15: agustos.com renders `aside.side-menu`, a fixed 240px
left column, on every page. It holds the lockup, five links, two collapsible groups, the filled
contact button, search, language, and the copyright line. There is no footer element. Mobile
shows a sticky header with a burger and a drawer. Light only.

## 4. Architecture

The four layers stay. A fifth layer, screens, sits between recipes and adapters.

1. Foundations: colour, type, spacing, measure, radii, motion.
2. Semantic roles: paper, surface, ink, rule, signal, focus.
3. Recipes: chrome, hero, section, card, data table, document, presentation.
4. **Screens: one reference composition per page type, hand-written on kit classes.**
5. Adapters: Astro, WordPress, Rails, Office.

Hand-edited sources after this change:

| Source | Owns |
|---|---|
| `tokens/design-tokens.json` | foundations, roles, recipes, the design direction, **the `screens` table** |
| `brand/brands.json` | identity per brand, **the `chrome` field per brand** |
| `tokens/web.css.tmpl` | web behaviour, **both chromes, the layout layer** |
| `screens/*.html` | the eight reference pages |
| `DESIGN.md` | the human specification, with one generated block |
| `ui/*.tmpl`, `docs/web.html.tmpl` | text templates the generator fills |

Generated after this change, in addition to today's outputs:

| Output | From |
|---|---|
| `ui/UI-KIT.md` screens table and brand chrome column | `screens` table, `brands.json` |
| `ui/kit.json` `screens` and per-brand `chrome` | same |
| `docs/web.html` | `docs/web.html.tmpl` plus the `screens` table |
| the generated block in `DESIGN.md` | `designDirection.principles` |
| `dist/claude-design/agustos-ui/cards/screen-*.html` and `chrome-*.html` | `screens/*.html`, the card list |

Nothing is stated twice. Theme follows the screen family. Chrome follows the brand.

## 5. Chrome in the kit

Both chromes live in `tokens/web.css.tmpl` and generate into `agustos.css`. The kit ships no
JavaScript. The drawer uses the native `popover` attribute. Collapsible groups use `details`.
Adapters may add scripts; the kit renders without them.

### 5.1 Sidebar family

| Class | Role |
|---|---|
| `site-sidebar` | the fixed 240px column: white paper, 1px rule on the right |
| `site-sidebar__lockup` | brand lockup at the top |
| `site-sidebar__nav`, `site-sidebar__link` | primary destinations; the current page carries a 2px red rule on its left edge |
| `site-sidebar__group` | a `details` element for a collapsible group such as social or legal |
| `site-sidebar__cta` | one filled button, the chrome's single primary action |
| `site-sidebar__utility` | search and language |
| `site-sidebar__note` | the copyright line |
| `site-sidebar-bar` | the sticky mobile bar: lockup and burger |
| `site-sidebar-burger` | the button that opens the drawer |
| `site-sidebar-layout` | on `body`; offsets `main` by the sidebar width at 1024px and above |

Geometry comes from `recipes.chrome`. It gains `sidebarWidth` (240px). Below 1024px the sidebar
is a native popover opened by the burger; above 1024px the stylesheet forces it visible and
the popover is inert.

### 5.2 Topbar family

| Class | Role |
|---|---|
| `site-header`, `site-header__bar` | the sticky one-row header inside a `site-frame` |
| `site-header__lockup` | brand lockup |
| `site-header__nav`, `site-header__link` | primary destinations; the current page carries a 2px red rule underneath |
| `site-header__end` | the slot for CTA, search, and language |
| `site-header__cta` | one filled button |
| `site-header__burger`, `site-header__panel` | the drawer below 1024px; the panel is a native popover |
| `site-footer`, `site-footer__inner` | the structured footer inside a `site-frame` |
| `site-footer__brand` | mono lockup and publisher description |
| `site-footer__cols`, `site-footer__col`, `site-footer__col-heading`, `site-footer__list`, `site-footer__link` | configurable link columns; one column at 760px |
| `site-footer__cta` | the footer contact action, separate from the page primary |
| `breadcrumb`, `breadcrumb__link` | the small trail above a page title |

The topbar names are the Astro adapter's existing names, kept. `nav-backdrop` goes; the popover
backdrop replaces it. Search stays an adapter concern; the kit leaves the slot.

### 5.3 Shared rules

- Header and footer destinations, copy, and columns are configuration. The kit styles them.
- Every clickable control meets `--control-min` (44px).
- Focus rings use the shared signal. Escape closes an open drawer, which the popover provides.
- Neither chrome carries a theme control on marketing brands. The app shell carries it in the
  sidebar utility slot.

### 5.4 Chrome per brand

`brand/brands.json` gains one field per brand:

```json
"chrome": "sidebar"
```

| Brand | Chrome |
|---|---|
| agustos | sidebar |
| pataraz | topbar |
| pld | topbar |
| iesdesk | sidebar |
| specquick | sidebar |

The generator writes the value into `ui/kit.json` and into the brand table in `ui/UI-KIT.md`. A
page writes one chrome's markup; the field tells the agent which one. The generator refuses a
value outside `sidebar` and `topbar`.

### 5.5 Migration

- The Astro adapter deletes the scoped styles in `Header.astro` and `Footer.astro` and keeps
  the kit class names.
- The Rails adapter renames `agustos-header`, `agustos-footer`, and `agustos-nav-backdrop` to
  the kit names and deletes its chrome rules from `components.css`.
- `docs/web.html` loses its inline chrome rules. It becomes a generated index (§7.5).
- agustos.com replaces `side-menu` and `mobile-header` with `site-sidebar` and
  `site-sidebar-bar` in its own repository. That migration is outside this repository.
- After this change, no `.site-header`, `.site-footer`, `.site-sidebar`, or `.side-menu` rule
  exists in this repository outside `tokens/web.css.tmpl`. A test enforces it.

## 6. Layout layer

Seven classes, generated into `agustos.css`:

| Class | Does |
|---|---|
| `stack` | vertical rhythm; children separated by `--space-md` |
| `cluster` | a wrapping inline row of actions or links; gap `--space-sm`; centred cross axis |
| `grid-2`, `grid-3`, `grid-4` | equal columns; gap `--space-lg`; `grid-4` drops to two columns at 1023px; all drop to one column at 759px |
| `band` | a full-bleed section with `--space-3xl` block padding; holds a `site-frame` |
| `band--cream` | the same on the cream substrate, with a hairline rule above and below |

After this, no page in the repository declares its own frame, band, or grid.

## 7. The screens folder

### 7.1 Files

`screens/` at the repository root holds eight hand-written pages.

| File | Screen | Family | Sample brand, chrome | Sample content |
|---|---|---|---|---|
| `home.html` | home | marketing | agustos, sidebar | the live agustos.com homepage |
| `static.html` | static | content | agustos, sidebar | the live Biz kimiz page: intro, timeline, team |
| `content.html` | content | content | agustos, sidebar | one post from the live blog |
| `products.html` | products | catalog | pataraz, topbar | PL, PX, PY series, from the current mockup |
| `product-finder.html` | product-finder | catalog | pataraz, topbar | filter column and results, from the current mockup |
| `product.html` | product | catalog | pataraz, topbar | PX22, from the current mockup |
| `spec-sheet.html` | spec-sheet | document | pataraz, topbar | PX22 teknik föy, from the current mockup |
| `app-shell.html` | app-shell | product UI | iesdesk, sidebar | the IESDesk validation run, from the Rails preview |

Real content on purpose. Each file proves the rules on a page the company ships.

### 7.2 Rules for every screen file

1. A complete HTML document with `lang="tr"`.
2. Loads `../ui/agustos-fonts.css`, then `../ui/agustos.css`. Links the canonical favicon.
3. `body` carries a `brand-*` class, `data-screen="<name>"`, and `site-sidebar-layout` when
   the brand's chrome is the sidebar.
4. Uses kit classes only. No `style` attribute. No `<style>` block. A test enforces this.
5. `app-shell.html` carries one `<script>` of at most five lines for the theme control. No
   other file carries a script.
6. Images come from this repository or are gray wells. No external URL.
7. The header comment states: swap the `brand-*` class for another brand and use that brand's
   registered chrome.
8. `python3 ui/check-agustos-ui.py screens` exits 0.

### 7.3 Source of the sample content

- home, static, content: the live agustos.com pages, read on 2026-09-15. Copy is Turkish.
- products, product-finder, product, spec-sheet: `mockups/products.html`,
  `mockups/product-finder.html`, `mockups/product.html`, `mockups/spec-sheet.html`, rebuilt
  without their inline chrome and section CSS.
- app-shell: `adapters/rails/preview/product-ui.html`, rebuilt on kit classes.

### 7.4 What retires

- `mockups/products.html`, `product.html`, `product-finder.html`, `spec-sheet.html` move into
  `screens/` under the names above.
- `mockups/pataraz-px22.html` is deleted. The spec-sheet screen covers it.
- `mockups/claude-design/` moves to `screens/design/` (§10.3).
- `mockups/` is removed.

### 7.5 Preview, index, and handoff

- The `agustos-docs` entry in `.claude/launch.json` serves the repository root, so
  `http://localhost:4390/screens/<file>` previews any screen.
- `docs/web.html` is generated from `docs/web.html.tmpl` plus the `screens` table: one section
  per screen with its name, purpose, family, chrome, theme, CTA limit, quote rule, photo rule,
  a lazy frame of the file, and a link. The five standard artifacts keep their names.
- `scripts/pack_handoff.py` packs `screens/*.html` and rewrites their stylesheet paths and the
  index's frame paths to the zip root.

## 8. The screens table

`tokens/design-tokens.json` gains a top-level `screens` object. One entry per screen, seven
fields:

```json
"screens": {
  "product": {
    "file": "product.html",
    "family": "catalog",
    "brand": "pataraz",
    "purpose": "One luminaire: photograph or drawing, description, grouped specification tables, datasheet download.",
    "primaryCtaMax": 2,
    "quotes": false,
    "photo": "product photograph or drawing, first in the rollout"
  }
}
```

| Field | Values | Meaning |
|---|---|---|
| `file` | a file name under `screens/` | the reference page |
| `family` | `marketing`, `content`, `catalog`, `document`, `product-ui` | sets the theme rule |
| `brand` | a slug from `brands.json` | the sample brand; sets the chrome of the sample |
| `purpose` | one sentence | what the page is for |
| `primaryCtaMax` | integer | the most times the page primary may appear in the body |
| `quotes` | boolean | whether blockquote and pullquote are allowed |
| `photo` | one phrase | where the page sits in the photography rollout |

Derived, never stored: `theme` is `dark-allowed` when `family` is `product-ui`, otherwise
`light`. `chrome` is the brand's registered chrome.

Values:

| Screen | family | brand | primaryCtaMax | quotes | photo |
|---|---|---|---|---|---|
| home | marketing | agustos | 2 | false | one installation photograph, third in the rollout |
| static | content | agustos | 1 | true | people and places that explain the work |
| content | content | agustos | 1 | true | only when it explains the content |
| products | catalog | pataraz | 1 | false | product thumbnails, second in the rollout |
| product-finder | catalog | pataraz | 1 | false | product thumbnails, second in the rollout |
| product | catalog | pataraz | 2 | false | product photograph or drawing, first in the rollout |
| spec-sheet | document | pataraz | 0 | false | product photograph and dimensioned drawing |
| app-shell | product-ui | iesdesk | 1 | false | none |

The generator renders the table into `ui/UI-KIT.md`, `ui/kit.json`, and `docs/web.html`. The
sync bundle renders one card per row (§10.1).

## 9. UI-KIT.md changes

- A screens table: name, family, chrome, theme, CTA limit, quotes, photo.
- A chrome column in the brand table.
- Two rows in the class table: Chrome (both families and breadcrumb) and Layout.
- The install sections merge into one. The stylesheet warning shortens. The line cap stays at
  200; the test keeps it.
- The Tailwind sentence becomes: "The kit is plain CSS. Do not add Tailwind, Bootstrap, or
  another utility framework."
- The composition paragraph points at the screens table instead of restating it.

## 10. The Design loop

### 10.1 Push ships screens and chrome as cards

`scripts/sync_claude_design.py build` adds two card groups:

- `Kit · Screens`: one card per row of the `screens` table. The builder copies
  `screens/<file>` to `agustos-ui/cards/screen-<name>.html`, prepends the `@dsCard` marker
  with viewport 1280 by 900, name from the screen, subtitle "family · chrome · theme", and
  rewrites the stylesheet, favicon, and lockup paths to the bundle layout.
- `Kit · Chrome`: `chrome-sidebar.html` and `chrome-topbar.html`, built like today's cards,
  each showing one chrome with a short main area.

Push still writes `agustos-ui/**` only. Design's own cards, components, and tokens stay
untouched.

### 10.2 Pull accepts any remote page or canvas file

`scripts/sync_claude_design.py pull --page <remote path> [--target <screen>]`:

- A remote directory is a built page. The tool fetches the subtree and the shared runtime, as
  today, and captures a screenshot.
- A remote path that ends in `.dc.html` is one canvas page. The tool fetches that file only.
  The canvas runtime is not in the project, so the page does not render locally and no
  screenshot is taken. The row says so.
- The `ui_kits/` prefix lock is removed. Paths are still confined to the project.
- `--target` names the screen the reference updates, or `new`. Default `new`.

### 10.3 References live beside the screens

- Pulled references land at `screens/design/<slug>/`, where the slug is the last path segment
  in lower-case with spaces and the `.dc.html` suffix removed.
- The shared runtime stays at `screens/design/` root, overwritten on every pull.
- `screens/README.md` holds the status table: reference, remote path, pulled date, target
  screen, status `pending` or `implemented`, built in.
- The four hand-copied canvas pages under `mockups/claude-design/canvas/` are deleted and
  re-pulled through the tool so their rows are traceable. `ui_kits/website` is re-pulled.
  `ui_kits/iesdesk` is pulled for the first time as the app-shell reference.
- Nothing in `ui/` or `tokens/` imports anything under `screens/design/`. Tests and `--check`
  never treat it as generated. The checker is told to skip it.

### 10.4 The loop

1. Release: `/design-push` sends the kit, two chrome cards, and eight screen cards.
2. Design: a designer draws a page or edits from a screen card.
3. Return: `/design-pull <remote path> --target <screen>` lands the page beside its target
   with a `pending` row.
4. Build: rebuild `screens/<name>.html` on kit classes from the reference. The checker exits
   0. Flip the row to `implemented`.
5. Release again: `/design-push` sends the updated card. A new screen is one new row in the
   `screens` table and one new file. The generator does the rest.

### 10.5 Unchanged

Repointing Design's own `tokens/fonts.css` and `assets/laz-gunesi.svg` at the pushed copies
stays deferred, as recorded on 2026-09-13.

> **Closed 2026-09-16.** Design's own rule layer was retired instead of repointed: `tokens/`,
> `components/`, and `cards/` deleted, `styles.css` importing the pushed kit, `SKILL.md`
> pointing at `agustos-ui/UI-KIT.md`. See `archive/MEMORY.md`, "Design's own stack retired".

## 11. One source for the direction prose

- `tokens/design-tokens.json` `designDirection` stays the source.
- `AGENTS.md` deletes its "Design direction" paragraph and points at `ui/UI-KIT.md` in two
  lines.
- `DESIGN.md` keeps its direction section. The "Apply the direction" list is generated between
  `<!-- generated: designDirection.principles -->` and `<!-- /generated -->`. The build script
  rewrites the block in place; `--check` compares it. The rest of `DESIGN.md` stays hand-written.
- "Do not zip the factory" lives in `HANDOFF.md` only. `README.md` and `tokens/README.md` link
  to it.

## 12. Documentation reconciliation and cleanup

| File | Change |
|---|---|
| `DESIGN.md` §Site chrome | describe both chromes, the per-brand choice, the popover drawer; name agustos.com as a sidebar site; remove "the fixed left sidebar is retired" |
| `DESIGN.md` §V3 architecture, `CLAUDE.md` | rename "v3" labels to "Architecture" |
| `DESIGN.md` §Versioning | record v6.0.0 and the reason for the major |
| `archive/MEMORY.md` | new entry "Two chromes, chosen per brand (2026-09-15)": the July topbar record did not match the live site; both chromes ship; agustos.com keeps the sidebar |
| `README.md` | version sentence to 6.0.0; add the screens layer; link HANDOFF.md for the factory rule |
| `HANDOFF.md` | the five artifacts plus `screens/`; the pull section names `screens/design/` |
| `PATARAZ.md` | §3 implementation note points at `screens/` and `ui/`; the component table says "topbar chrome from the kit" |
| `AGENTS.md` | routing rows for screens, the pull, and the push; direction paragraph replaced by a pointer |
| `CHANGELOG.md` | `[6.0.0]` with a Migration section (§14.2) |
| `hero-example.html` | move to `artifacts/agustos-hero-example-v3.1.0.html` |
| `build_template.py` | delete; nothing references it; `brand/build_templates.py` covers Office |
| `docs/handoff-setup.html` | mention `screens/` in the kit map |

## 13. Tests

Added to the existing suite. Every test is deterministic and runs in CI with `--check`.

1. Every entry in the `screens` table names a file that exists, and every `screens/*.html` has
   an entry.
2. No `<style>` block and no `style` attribute in `screens/*.html`; at most one `<script>` in the
   folder, in `app-shell.html`.
3. `check-agustos-ui.py screens` exits 0.
4. Every brand has a `chrome` value in `{sidebar, topbar}`.
5. Every chrome and layout class is in `compatibility.cssClasses` and reaches every generated
   stylesheet (the existing class tests cover this once the list grows).
6. No chrome rule exists outside `tokens/web.css.tmpl` in this repository.
7. `ui/UI-KIT.md` names every screen and stays at 200 lines or fewer.
8. The generated block in `DESIGN.md` and `docs/web.html` are in the manifest and current.
9. The sync bundle holds one `screen-*.html` card per screen and two `chrome-*.html` cards.
10. `pull` accepts a directory and a `.dc.html` path, writes the status row, records the
    target, and refuses a path outside the project.

Visual pass, from the `DESIGN.md` QA checklist: both chromes at 375, 768, and 1280; keyboard
through the drawer; Escape closes it; every control at 44px; the app shell in light and dark.

## 14. Versioning, release, and phases

### 14.1 Version

6.0.0. The major records the chrome contract: consumers replace their local chrome with the
kit's and adopt one name. VERSION, the registry, the manifest, and `kit.json` agree; the tag
`v6.0.0` lands in the same change.

### 14.2 Migration note for CHANGELOG

- Replace local header, footer, and sidebar CSS with the kit chrome classes.
- Rails: rename `agustos-header`, `agustos-footer`, and `agustos-nav-backdrop` to
  `site-header`, `site-footer`, and the popover backdrop.
- agustos.com: replace `side-menu` and `mobile-header` with `site-sidebar` and
  `site-sidebar-bar`; put `site-sidebar-layout` on `body`.
- Put `data-screen="<name>"` on `body`.
- Remove Tailwind or any other utility framework if present. The kit does not support one.

### 14.3 Phases

One branch, one pull request to `main`, one commit or a few per phase, the version bump last.

1. Registry and template: chrome, layout layer, `chrome` per brand, `screens` table, generator
   renders, tests.
2. Screens: the eight files with real content; `mockups/` retired; checker clean.
3. Adapter migration: Astro, Rails, `docs/web.html`.
4. Design loop: screen and chrome cards, pull without the prefix lock, `screens/design/`,
   references re-pulled, status table.
5. Documentation and cleanup: §11, §12, CHANGELOG, archive entry.
6. Release: VERSION 6.0.0, rebuild, `--check`, tests, tag, `/design-push`.

### 14.4 Out of scope, recorded as follow-ups

- Per-screen checker rules: count primary buttons against `primaryCtaMax`, flag quotes on a
  non-content screen, flag a theme control outside product UI. Needs `data-screen` and
  `kit.json.screens`, both delivered here.
- Extracting the datasheet `PRODUCTS` dict into `brand/products/*.json`.
- Repointing Design's own tokens and symbol at the pushed copies. (Closed 2026-09-16 by retiring that layer; see §10.5.)
- The agustos.com and pataraz.com migrations themselves.

## 15. Acceptance

1. An agent with `ui/UI-KIT.md` and `screens/` builds any of the eight page types for any brand
   with the correct chrome and no invented CSS.
2. `python3 ui/check-agustos-ui.py screens` exits 0. No `<style>` in `screens/`.
3. `python3 scripts/build_design_system.py --check` and `python3 -m unittest discover -s tests`
   pass. `docs/web.html`, the UI-KIT screens table, `kit.json.screens`, and the `DESIGN.md`
   block are generated.
4. After `/design-push`, the Design System pane shows `Kit · Screens` with eight cards and
   `Kit · Chrome` with two. A second push is a no-op.
5. `/design-pull` of one canvas file and of `ui_kits/iesdesk` both land under `screens/design/`
   with rows in `screens/README.md`.
6. No chrome rule exists outside `tokens/web.css.tmpl` in this repository.
7. Tag `v6.0.0` exists. Every CDN pin in the kit says `@v6.0.0`.
