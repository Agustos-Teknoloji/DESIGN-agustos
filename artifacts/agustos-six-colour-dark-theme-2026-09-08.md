# Ağustos — design decisions (v3, September 2026)

Supersedes the cream-substrate direction. This file records what was decided, the value to use, and the rule that governs it. If a decision is not here, it is not decided.

Applies to: marketing website, product pages, spec sheets, product UI (IESDesk).
Type is unchanged from the Ağustos design system: **Inter Tight** (display), **Inter** (body), **JetBrains Mono** (technical data).

---

## 1. Direction

Premium, clean, minimalistic, direct. B2B, addressed to architects and lighting designers. Scandinavian restraint with Mediterranean warmth — the warmth is carried by the grays, the cream band and the copy, not by decoration.

- White substrate. Cream is no longer the paper.
- Type-only. No decorative imagery, no gradients, no textures, no patterns.
- Flat surfaces. No shadows anywhere.
- Radii: 6 px on controls and small panels, 10 px on cards.

## 2. Palette

Six colours. No seventh, no alternate shades.

| Role | Hex | Where |
|---|---|---|
| White | `#ffffff` | Primary substrate, ~70% of every surface |
| Cream (light red) | `#fdf5f5` | Full-bleed callout and CTA bands. Logo red at 5% into white |
| Light gray | `#ebebeb` | Functional surfaces: key-figure tiles, image regions, summary panels |
| Dark gray | `#404040` | Secondary text |
| Black (off-black) | `#15130f` | Headlines, filled buttons, footer |
| Red | `#cf142a` | Signal only. Identical to the logo red |

Support values: hairline rule `#e8e4da`, faint label text `#8a8378`.

Rules:

- **Red is one hex.** `#cf142a`, the logo red. No tints, no darker hover shade, never a large fill.
- **Cream is one hex** and always appears as a full-bleed band with hairline rules top and bottom, never as an inset rounded card.
- Every band on a page uses the same background. Do not mix a gray band and a cream band.
- Approximate proportion: 70 white · 14 light gray · 8 black · 5 cream · 3 red.

## 3. Where red is allowed

Exactly two places:

1. The 2 px rule under a link inside content, including inside a sentence.
2. The 2 px rule revealed under a menu item on hover, and on the current menu item.

Never: a red fill, red as an element's own colour (icons included), red on a stat or figure, a red button.

## 4. Type

- No uppercase anywhere. Labels, table headers, breadcrumbs and menu items are sentence case with normal tracking.
- No eyebrow labels above headlines. The headline carries the opening.
- Small labels: Inter Tight, 12.5–13 px, weight 600, `#8a8378`.
- Headlines: Inter Tight, weight 300–400, tight negative tracking. Hero at 300.
- Body: Inter, 16.5–20 px, 1.6 line height, `#404040` for secondary copy, `#15130f` for primary.
- Technical data (order codes, file names, email, years): JetBrains Mono, tabular figures.
- Numbers in tables and dashboards: `font-variant-numeric: tabular-nums`.

## 5. Actions

Four treatments, no fifth.

| Treatment | Job |
|---|---|
| Filled black button | The committing action. One per band |
| Outline button | The real alternative, downloads included |
| Text + 2 px red rule | A link inside reading matter |
| Plain label | Navigation: menu, breadcrumb, footer |

Rules:

- One size everywhere: 44 px minimum height, 6 px radius, no shadow, no arrow.
- Labels are sentence case, verb first: "Request pricing", not "Pricing request".
- A CTA pair is always filled + outline. Never two filled buttons, never a borderless label next to a filled button.
- Buttons never appear in the menu except the single CTA.

### Hover and focus

- Filled black: stays black.
- Outline: fills black, label turns white.
- Content link: ink turns red, the rule stays.
- Menu item and menu icon: ink goes to `#15130f`, the 2 px red rule appears below.
- Focus (keyboard): 2 px red outline at 2 px offset, on buttons and links alike.
- Duration 150 ms, `cubic-bezier(0.2, 0, 0, 1)`. Nothing scales, lifts or glows.

## 6. Header

Three zones on one row:

1. Left: the lockup.
2. Centre: menu items, sentence case, 15 px.
3. Right: utility actions, then the CTA last.

Utility actions are a search glyph, the language name in its own language ("Türkçe"), and a theme glyph. Icons are 1.5 px line, monochrome, inheriting `currentColor`, and hover exactly like the text items. Exactly one CTA button in the header.

## 7. Footer

Permanently black `#15130f`. Links are plain white labels — no red rule. The footer CTA is a white filled button with black label, hovering to `#e8e4da`. Every standalone contact action reads "Contact" — the same word everywhere, never "Contact studio" or a variant.

## 8. Layout

- Content column max 1180 px, 32 px gutters — in line with current practice (1140–1280 px is the standard desktop content width; full-bleed backgrounds and bands stretch edge to edge, the text/content column doesn't).
- Body measure 72ch, hero supporting copy 54ch — text uses `ch`, never a px cap, so the measure holds regardless of font-size.
- Compact vertical rhythm: 64 px between sections.
- **Fluid, not breakpoint-driven.** No fixed breakpoints (no "at 768px do X"). Headings and hero type scale with `clamp(min, preferred-vw, max)`. Card and column rows are `flex-wrap` with `flex: 1 1 <basis>`, not a fixed-column grid — this is what keeps a row from ever leaving an orphaned cell or an empty track at an in-between width, and it's the modern default over rigid Bootstrap-style breakpoints.
- `box-sizing: border-box` on anything with both a flex-basis and padding — a content-box mismatch is what causes rows to wrap wrong.
- Bands are full-bleed with hairline rules; content inside them uses the same 1180 px column.
- Everything except spec sheets is fluid. Spec sheets are fixed A4.
- If a component ever needs to look different depending on where it's dropped (e.g. a card in a 3-up grid vs. a narrow sidebar), reach for a container query on that component rather than a page-level breakpoint.

## 9. Brands

One publisher, five names. The symbol and type are shared; only name and colour differ.

| Brand | Wordmark | Mark colour |
|---|---|---|
| Ağustos Teknoloji | `ağustos` | Red `#cf142a` |
| Pataraz | `pataraz` | Off-black `#15130f` |
| PLD Türkiye | `pld türkiye` | Off-black `#15130f` |
| IESDesk | `iesdesk` | Off-black `#15130f` |
| SpecQuick | `specquick` | Off-black `#15130f` |

Only the publisher mark is red. Every other brand uses the one off-black — not `#1a1a1a`, not black.

## 10. Dark theme

Locked. No new colours — the same six roles, flipped:

| Role | Hex | Was (light theme) |
|---|---|---|
| Paper (substrate) | `#15130f` | Black |
| Surface (cards, borders) | `#404040` | Dark gray |
| Callout band (header, stat bands, CTA bands) | `#ebebeb` | Light gray |
| Ink (headlines, primary text) | `#ffffff` | White |
| Ink soft (secondary text) | `#8a8378` | Faint label |
| Red | `#cf142a` | Unchanged — the one value that never adapts to substrate |

- The primary CTA in a dark hero is filled red, the secondary is filled white — the one approved deviation from "never a red fill," since black-on-dark isn't available as the commit colour.
- Full reference build: `Homepage (Dark).dc.html`.
- Still open (implementation scope, not palette): whether dark ships on marketing pages or is reserved for product UI (IESDesk/SpecQuick); photography treatment on a dark ground.

## 11. Open decisions

- How often the primary CTA may repeat on one page (currently: menu, hero, contact band, plus the footer's separate CTA).
- Whether the quote treatment (indented, attributed) appears on content pages only — currently removed from marketing pages.

## 12. Files in this project

| File | What it is |
|---|---|
| `Design.dc.html` | Summary hub — principles, and links to every file below |
| `Homepage.dc.html` | The marketing homepage, reference implementation of these rules |
| `Products.dc.html` | The product catalogue, grouped by series |
| `Product page.dc.html` | Product page with the configurator |
| `Product Finder.dc.html` | Interactive filter tool |
| `Spec sheet.dc.html` | Single-page A4 spec sheet, print-ready |
| `Colours.dc.html` | The six-colour palette, decided |
| `Fonts.dc.html` | The full type hierarchy, decided |
| `Brands.dc.html` | The five brand names sharing one symbol and colour rule |
| `Direction.dc.html` | The direction board that set the palette |
| `Action rules.dc.html` | The action tiers, as decided |
| `Dark Theme.dc.html` | The dark palette, locked |
| `Homepage (Dark).dc.html` | Full homepage reference in the dark theme |
| `DESIGN-DECISIONS.md` | This file |
