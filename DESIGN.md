# Ağustos Design System

**Version 7.4.0** · Cross-medium design system for Emre Güneş's brand portfolio

## Standard artifacts

These five files are the shareable system. Open the HTML in a browser. Stylesheets sit next to the HTML files. Read this file before you write markup.

1. **This file (`DESIGN.md`)** — contract for any LLM or implementer: direction, colour, type, brands, principles, and rules.
2. [`docs/fonts.html`](docs/fonts.html) — families, sizes, weights, Turkish, wordmark rules.
3. [`docs/colour.html`](docs/colour.html) — substrate, ink, signal, identity, dark theme.
4. [`docs/web.html`](docs/web.html) — one live frame per screen type, with that screen's rules. The pages are in `screens/`.
5. [`docs/brands.html`](docs/brands.html) — house brands and lockup expressions.

Everything else in this repository is factory: generators, adapters, Office files, and decision history.

---

## What this is

A typographic design system covering web, document, presentation, and product UI surfaces for a multi-brand portfolio. It is built typography-first because that is the durable layer: components change, while alignment, type, hierarchy, and rules persist.

`agustos.com` is the design laboratory and reference implementation. Proven patterns are promoted from real website use into this repository; the live site is never the literal source of truth. `tokens/design-tokens.json`, `brand/brands.json`, and this specification are authoritative.

The portfolio currently spans:

- **Ağustos Teknoloji.** Lighting agency and distribution (red, `#cf142a`)
- **Pataraz.** Premium luminaire brand at mid-tier pricing (black/white identity)
- **PLD Türkiye.** Lighting publication archive (off-black, `#15130f`)
- **IESDesk.** Software for lighting data (black/white identity) — successor to Photometric Batch
- **SpecQuick.** House brand (black/white identity)

Future house brands plug in by choosing a name. They inherit black/white identity ink, shared red interaction signals, typography, logo geometry, and structure.

---

## Design direction — İskandivvian

**Scandinavian restraint filtered through Mediterranean warmth.**

İskandivvian is the project label for this defined direction.
Create minimal, functional, and elegant experiences that feel calm, welcoming, and human.
Use clarity, alignment, and low visual noise to provide structure.
Use comfortable proportions, warm neutral surfaces, and helpful language to provide warmth.
Keep the experience welcoming and easy to use.

### Apply the direction

<!-- generated: designDirection.principles -->
- Use six colours: white #ffffff as the paper, pale red #fdf5f5 for the closing band, light gray #ebebeb for functional surfaces, dark gray #404040 for secondary text, off-black #15130f for text and buttons, and red #cf142a. Two support values serve only hairlines (#e8e4da) and faint marks (#8a8378). A new value needs a deleted one.
- Set type on one golden scale: the 16.5px body times 1.272 per step, so every second step is the golden ratio (13, 16.5, 21, 27, 34, 43, 55, 70, 89px). Headings are thin: hero 89px light, H1 55px light, H2 43px regular, H3 21px medium. Use four weights (300, 400, 500, 600). The wordmark alone uses 650.
- Use two radii, 6px for controls and 12px for cards, and one section spacing. Do not use gradients or textures. The only shadow sits under a menu that floats above the page.
- Red is identity and signal, never action: the logo, the 2px link and menu rule, keyboard focus, and one highlighter stroke per page. Buttons are black. The Ağustos logo is red and turns black on hover; every other house brand's logo is black and turns red on hover.
- Use the highlighter once per page, on one to four words of the main headline. Never on links, buttons, numbers, body text, or product UI. The sentence must read the same without it.
- Websites use the top menu with at most five items. Extra pages go under one More menu, and social, legal, and language links live in the footer. Product UI uses the sidebar. Websites ship light; dark theme is for product UI.
- Copy a screen; do not design a page. Open with a headline, a deck, two buttons, and a trust line. Close with one pale red band.
- Bold (600) marks a fact the reader scans for, at most once per paragraph. Italic marks names of publications and projects, foreign terms, and quoted phrases. Underline is for links only. Do not combine them, and do not use uppercase labels, eyebrow headings, or coloured text.
- When unsure, do the conventional thing. Collect design tweaks and release the kit once a month; fix real defects at once.
<!-- /generated -->

### Imagery

Natural light and material detail can support relevant images.
Use images when they explain the content.
Keep text, tables, and controls on plain surfaces.
Use shadows only when they clarify layering.
Avoid unrelated lifestyle imagery, inflated luxury claims, excessive whitespace, and forced friendliness.

Type-only pages are complete. A gray well may mark a reserved photo slot.
Roll photographs out in this order:

1. Product page: one product photograph or drawing. Preserve the real finish. No lifestyle crop.
2. Listing: the same product crop as a thumbnail, after the product photograph exists.
3. Homepage: one installation photograph, after listing thumbnails exist, and only when it shows a real place or the work.
4. About and content pages: people and places that explain the work.

Do not put a photograph behind body text, forms, or tables.
Do not fill every card with an image.

### Cross-medium application

Editorial pages can carry more atmosphere through composition and relevant photography.
Software uses the same warmth through language, spacing, and clear controls.
Documents and technical sheets retain plain reading surfaces and economical printing.
Presentations use calm hierarchy, purposeful spacing, and relevant images.
Every medium must remain clear and useful.

### Implementation contract

`tokens/design-tokens.json` owns the machine-readable `designDirection` field.
The generator publishes it in the handoff, resolved registry, and UI kit.
Version 5 applies the approved white-substrate palette, type scale, action system, layout measure, and locked dark theme.
The dark theme reuses the same six colours, flipped. No new hexes.
Marketing pages stay light. Dark theme is for product UI.

## Website composition

These rules close the remaining website application questions.
They apply to every house-brand site.
Copy a screen from `screens/`; do not design a page.

### One primary destination

Name one committing destination per page.
It may appear in the header, in the opening, and in the one closing pale red band.
Do not place a primary button in the sections, cards, or lists between them.
This is advice, not a checked rule: v7.0.0 removed the checker's button count.

A button pair is one primary and one secondary `agustos-button`. Never two primary buttons in one band.
Form submits (Show matches, Send) are task actions. They do not count as the page primary.
The footer carries no button.
In-prose links with a 2px red rule are not buttons.

### Dark theme

Marketing pages, product catalog pages, and spec sheets ship on white paper.
They do not include a theme toggle.
Dark theme is for product UI (IESDesk and similar tools) and honors user preference there.
Use the locked six-colour flip: paper `#15130f`, surface `#404040`, callout `#ebebeb`, ink `#ffffff`, ink-soft `#8a8378`.
Buttons invert with the ink: the primary is white on off-black. Red never fills a button, in either theme.
The handbook dark control inspects that theme. It is not a marketing pattern.
Do not design a dark-first marketing page.
Do not place photography on a dark marketing hero.

### Photography

See Imagery above for the rollout order.
Product pages earn the first real photograph.
Until that photograph exists, keep the gray well and ship the page.

### Quotes

Keep `.type-blockquote` and `.type-pullquote` for content pages: articles, interviews, notes, and case studies.
Proof on a marketing page is a compact trust line, not a testimonial.
This is guidance. The checker no longer enforces it.

## System philosophy

Six rules that govern every decision in the system. These are non-negotiable; they're how the system survives over time.

### 1. Portability over preference

Every design decision must survive translation across markdown → web → PDF → docx → plain text. Meaning and reading order must survive standard markdown. Optional presentation treatments must never carry essential meaning.

### 2. The publisher precedes the brand

All visible brand systems express "from Emre's house" first, individual brand identity second. This is the inverse of most multi-brand systems. The shared symbol, typography, neutral identity model, and red interaction signal identify the publisher; the wordmark names the publication.

### 3. One symbol, forever

The Laz Güneşi is the publisher's mark. Every brand carries it, regardless of category. The symbol is fixed; the discipline of one symbol is more valuable than per-brand symbolism. House brands flex through name and content, not a palette of logo colors.

### 4. Ağustos alone owns red as identity

Ağustos uses red `#cf142a` for its symbol and wordmark. Pataraz, PLD Türkiye, IESDesk, SpecQuick, and future house brands use off-black `#15130f` on light substrates and cream/white on black identity tiles. Do not invent a chromatic identity color for each brand.

### 5. Shared red is a signal, not decoration

Red is identity and signal, never action. The link is the primary shared interaction expression: a 2px red underline on content links. The same 2px rule marks the current page in a menu; a menu hover is a 1px gray rule. Keyboard focus is a 2px red outline at 2px offset. One highlighter stroke per page marks one to four words of the main headline. Red is never a fill, a button, a statistic, or text colour, except that a content link turns red on hover on light paper. Buttons are black on every brand and in both themes. The identity role (`brandMark`) and interaction role (`signal`) are separate: at rest, red never recolors a non-Ağustos logo. On the web the logo answers hover: the Ağustos logo turns black, every other house-brand logo turns red. In the dark theme red text on off-black scores 3.35:1, below the text floor, so a link hover dims the ink instead and the red rule stays; the Ağustos logo turns white. Every state in both themes is a row of the `states` table in `tokens/design-tokens.json`, and the build refuses a pair below its floor (4.5:1 text, 3:1 borders, logos and focus).

### 6. Turkish content declares its language

Every Turkish content block carries `lang="tr"`. CSS enables `font-feature-settings: "locl"` globally. This is a correctness requirement, not a preference, without it, `text-transform: uppercase` produces wrong capitalization (i → I instead of i → İ).

---

## Architecture and governance

The website redesign contributed a compositional grammar, not merely a handful of CSS values: one chrome per screen family, one aligned frame, large editorial openings, signal color used selectively, bordered content groups, small radii, short motion, and generous section rhythm.

The system separates that grammar into five layers:

| Layer | Owns | Canonical representation |
|---|---|---|
| **Foundations** | Color, type, weights, sizes, spacing, measure, borders, radii, motion | `tokens/design-tokens.json` → `foundations` |
| **Semantic roles** | Paper, surface, ink, muted ink, rule, brand mark, shared signal, focus, display/body/data text | `tokens/design-tokens.json` → `semantic` and `themes` |
| **Recipes** | Chrome, hero, section opening, editorial link, card, data table, document, presentation | `tokens/design-tokens.json` → `recipes` plus `tokens/web.css.tmpl` where behavior is web-specific |
| **Screens** | One reference composition per page type, on kit classes | `screens/*.html`, hand-written; their rules in `tokens/design-tokens.json` → `screens` |
| **Adapters** | Astro, WordPress, Rails, PowerPoint, Word/Google Docs | Generated and framework-specific files under `adapters/` and `brand/` |

The factory side (the promotion loop, the generators and the drift checks) is in `ARCHITECTURE.md` in the source repository.

---

## The type stack

Three families. Each with one job. No overlap. As of v2.0 the system runs on a single sibling pair (Inter Tight + Inter) plus a code mono, the editorial serif has been retired in favor of one paired family from logotype to footnote.

### Inter Tight (Display)

Designed by Rasmus Andersson, the same designer as Inter, as a tighter, more compressed sibling for display use. Variable wght axis 100–900 with italics. Shares Inter's skeleton, so the pair harmonizes by construction. Used for the **logotype, hero tokens, all headings (H1–H4), UI labels, table headers, badges, dashboard numerals, pullquotes**, and any "designed" surface.

**Fallback stack:**

```css
font-family: 'Inter Tight', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

Inter Tight falls back to Inter (same designer, very close metrics), then to the user's native UI font. Designed degradation, not breakage.

### Inter (Body)

The most rigorously screen-engineered open-source sans. Hinted, optical-sized, with gold-standard Latin Extended including Turkish (`ç`, `ğ`, `ı`, `İ`, `ö`, `ş`, `ü`). Variable wght axis 100–900 with italics. Used for **paragraph body, em, strong, links, lists, blockquote, definition lists, footnotes, figure captions, and table cells**, every paragraph and inline element.

**Fallback stack:**

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji";
```

The fallback chain resolves to SF Pro on Apple, Segoe UI on Windows, Roboto on Android. Apple Color Emoji at the tail keeps emoji rendering native if any inline emoji slip into copy.

### JetBrains Mono (Monospace)

Designed for code legibility. Excellent ligatures, tabular figures, clear 0/O and 1/l/I disambiguation. Supports Turkish diacritics. Used for inline code, code blocks, file paths, hex codes, technical identifiers, section markers.

**Fallback stack:**

```css
font-family: 'JetBrains Mono', 'SF Mono', Menlo, Consolas, ui-monospace, monospace;
```

---

## Generated web variables

`tokens/design-tokens.json` is canonical. `tokens/agustos.css` is a generated, drop-in web artifact; do not edit it directly. The CSS keeps the established class APIs and the runtime `--brand` alias so existing sites can move to v3 without a visual reset.

```css
:root {
  /* Substrate */
  --paper: #ffffff;        /* White, primary paper */
  --paper-white: #ffffff;  /* Compatibility alias */
  --cream: #fdf5f5;        /* Pale red. The one closing band only */
  --surface: #ebebeb;      /* Functional tiles, image regions, summary panels */
  --footer-paper: #ffffff; /* Footer ground: white under a hairline. Never inverts. */
  --footer-ink: #15130f;   /* Footer type. Never inverts. */

  /* Ink */
  --ink: #15130f;          /* Headlines, buttons, house-brand identity */
  --ink-soft: #404040;     /* Secondary text */
  --ink-faint: #8a8378;    /* Labels and quiet metadata */

  /* Rule (separator color) */
  --rule: #e8e4da;         /* Hairline on light surfaces */
  --rule-white: #e8e4da;   /* Compatibility alias */

  /* Radii: two, nothing rounder */
  --radius-sm: 6px;   /* alias of --radius-md, kept for compatibility */
  --radius-md: 6px;   /* controls: buttons, inputs, badges, menu items */
  --radius-lg: 12px;  /* cards and floating menus */

  /* The one section spacing: sections, the closing band, the gap after the hero */
  --section-space: clamp(72px, 9vw, 104px);

  /* Motion */
  --dur: 150ms;
  --ease: cubic-bezier(0.2, 0, 0, 1);

  /* Shared interaction signal across every brand */
  --signal: #cf142a;

  /* Identity ink, selected per page */
  --brand-agustos: #cf142a;
  --brand-pataraz: #15130f;
  --brand-pld: #15130f;
  --brand-iesdesk: #15130f;
  --brand-specquick: #15130f;
  --brand: var(--brand-agustos);

  /* Type stacks, v2.0 */
  --display: 'Inter Tight Variable', 'Inter Tight', 'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --body:    'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji";
  --mono:    'JetBrains Mono', 'SF Mono', Menlo, Consolas, ui-monospace, monospace;
}
```

Radii and motion were first proven in the website redesign and are now foundations. Two radii, not a full numeric scale, preserve the system's restraint principle: 6px for controls, 12px for cards and floating menus. The checker warns (AG010) on anything rounder than 12px. There are no shadows, except the one under a menu that floats above the page (the top menu's More).

**Note on naming.** v1.x used `--serif`, `--sans`, `--logotype` to name the three faces by category. v2.0 names them by role. `--display` (anything designed) and `--body` (anything read at length), because the system no longer has a serif/sans split. Mono is unchanged.

**Per-brand application:**

```css
.brand-agustos   { --brand: var(--brand-agustos); }
.brand-pataraz   { --brand: var(--brand-pataraz); }
.brand-pld       { --brand: var(--brand-pld); }
.brand-iesdesk   { --brand: var(--brand-iesdesk); }
.brand-specquick { --brand: var(--brand-specquick); }
```

Inside any brand-scoped element, `var(--brand)` resolves to its identity ink. `var(--signal)` remains Ağustos red across every brand. Without a brand class, `--brand` falls back to Ağustos red.

**Substrate helpers:**

```css
.paper-white {
  --paper: var(--paper-white);
  --rule: var(--rule-white);
}
```

White is the default paper. Pale red (`--cream` in token names) is the one closing band, not a page substrate. `.paper-white` remains a compatibility class.

---

## Global styles

```css
html, body {
  background: var(--paper);
  color: var(--ink);
  font-family: var(--body);
  font-feature-settings: "locl" on, "kern" on, "ss01" on;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}
```

**The `locl` feature is mandatory.** It activates locale-aware OpenType lookups, which makes Turkish capitalization render correctly when `lang="tr"` is declared on content.

**The `ss01` stylistic set** is enabled globally. In Inter, `ss01` is open digits: the 4, 6 and 9 take open forms, in running text and in spec tables alike. It does not change the `a`, which is two-storey by default (`cv11` gives the single-storey form). Keeping open digits is a taste decision (MEMORY.md, review-patch).

---

## Typography and content tokens

Each token has exactly one job. When writing content, ask only: which one of these is this? V3 keeps the useful v2 class API while moving its values into the structured registry.

### One golden scale

Every text size sits on one scale: the 16.5px body times 1.272 (the square root of the golden ratio) per step, so every second step is the golden ratio. The steps are 13, 16.5, 21, 27, 34, 43, 55, 70, and 89px. Headings shrink one or two steps on small screens through `clamp()`. `bodyCompact` (15.5px) is the one UI size off the scale: menus, buttons, and the hero trust line.

Four weights: 300, 400, 500, and 600. The wordmark alone uses 650. Headings are thin: the hero and H1 at 300, H2 at 400, H3 at 500.

### Hero (2)

| Token | Size | Weight | Family | Notes |
|---|---|---|---|---|
| `.type-hero` | clamp(55px, 7vw, 89px) / lh 0.97 | 300 | Display | Tracking -0.042em. Max-width 15ch. Margin-bottom 32px (`--space-2xl`). Marketing page opening. One per page maximum. |
| `.type-hero-md` | clamp(43px, 4.6vw, 55px) / lh 1.0 | 300 | Display | Tracking -0.04em. The H1 size: `heroMedium` is an alias of `h1`, kept for compatibility. |

Two measures exist for text: `--measure-text` (54ch) is the hero deck, `--measure-body` (41rem, 656px) is the reading line: long-form prose such as posts, policies and profiles. A line of running text stays between 45 and 75 characters (Bringhurst, Baymard, GOV.UK), and WCAG 1.4.8 sets 80 as the ceiling; 41rem holds about 75 characters of Inter at 16.5px. The line is in `rem`, not `ch`, because `ch` follows the font size of each element, and the footer and the article would then put the line in different places. Cap the column, not each paragraph: a content page stops each block at the line with `.container--reading`, and a full-frame page caps each text block with `.prose`. The hero deck is a separate utility (`.type-hero-deck`), upright body at 21px, max-width 54ch, paired with either hero token. It is a supporting lead, not a quote, so it does not use italic. Do not place an eyebrow above the hero. The headline carries the opening.

### Hero element styles

The HERO section is a page-opening composition, not a new token family. It combines a headline, one deck utility, the shared buttons, and a trust line. On the homepage, the hero text should occupy the first viewport as a top-aligned editorial opening; the page should not vertically center the statement or split it into text/media columns. Name the parts consistently so design notes, implementation, and CMS fields all refer to the same things.

| Element | Style | Required | Definition |
|---|---|---|---|
| **Headline** | `.type-hero` or `.type-h1` | Required | The page statement. Ink-on-paper, never a link. Marketing openings use `.type-hero` (89px). Listing and content pages use `.type-h1` (55px), including the product listing and the product finder. One headline per hero. It may carry the page's one highlighter stroke. |
| **Supporting Copy** | `.type-hero-deck` | Recommended | One supporting lead, 1-2 sentences, max-width 54ch, upright body at 21px, ink-soft. Explains the promise; does not repeat the headline. |
| **Primary button** | `.agustos-button.agustos-button--primary` inside `.hero-actions` | Recommended | The committing action. Filled black, 44px, no arrow. One per band. |
| **Secondary button** | `.agustos-button.agustos-button--secondary` inside `.hero-actions` | Recommended | The real alternative. A quiet outline; hover firms the border to ink. |
| **Trust Signals** | `.hero-trust` | Recommended | Compact proof line below the actions: year range, client count, geography, partner names, standards, warranty, press, or certification. Body family at 15.5px (`bodyCompact`), ink-soft. No badges, pills, or logo-wall treatment in the hero. |
| **Hero Visual** | `.hero-visual` | Optional | Actual product, place, object, state, screenshot, diagram, render, or media. On the homepage, keep it below or after the text-led first viewport unless the visual is the product itself. Avoid decorative-only gradients, abstract logo collages, or framed visual cards that compete with the headline. |

Optional `.type-body` summary may sit between Supporting Copy and the buttons only when the page needs a second level of explanation. Do not add an eyebrow above the headline.

Recommended order:

1. **Headline**.
2. **Supporting Copy**.
3. Optional `.type-body` summary.
4. `.hero-actions` containing one **Primary button** and one **Secondary button**.
5. **Trust Signals**.
6. **Hero Visual** as the adjacent or following visual plane.

Do not make the hero headline itself the call to action. Headline links create an oversized underline and confuse hierarchy: the statement starts behaving like a button. Keep the title as ink-on-paper; put navigation in the action row.

The hero opens with two buttons: one primary, one secondary. A content link with a 2px red rule is the in-prose action, not the band-level commit. Do not use arrows. The page closes with one `band band--cream`.

Hero component styles are web/component utilities, not typography tokens. The hero buttons are the shared `agustos-button`. `.hero-trust` and `.hero-visual` belong to hero sections only:

| Utility | Role | Style |
|---|---|---|
| `.hero-actions` | Band-level action row | Flex row, wraps, 12px gap, 32px (`--space-2xl`) above. Holds one primary and one secondary `agustos-button`. |
| `.hero-trust` | Trust signal line | Body family, 15.5px (`bodyCompact`), line-height 1.5, ink-soft, 32px above. Items stay textual and compact. |
| `.hero-visual` | Visual plane | Media container for the hero image/render/screenshot/diagram. Full-width within its layout column, 64px above, no decorative card chrome, caption through `.type-figure` when needed. |

v7.0.0 retired `.hero-links`, `.hero-link*`, and the `.hero-action*` aliases. Use `agustos-button` in the action row and a plain content link in prose.

The page opening (`.container`) pads `clamp(56px, 9vw, 112px)` above and `clamp(8px, 1.5vw, 16px)` below. The bottom is small on purpose: the first section below brings the section spacing.

**Implementation status.** The hero actions, trust, and visual utilities are generated into all web adapters from the registry.

### Headings (4)

| Token | Size | Weight | Family | Notes |
|---|---|---|---|---|
| `.type-h1` | clamp(43px, 4.6vw, 55px) / lh 1.0 | 300 | Display | Tracking -0.04em. Page and product title, and the listing-page opening. |
| `.type-h2` | clamp(34px, 3.4vw, 43px) / lh 1.06 | 400 | Display | Tracking -0.032em. One H2 role on marketing and product pages. |
| `.type-h3` | 21px / lh 1.25 | 500, upright | Display | Tracking -0.014em. The middle step between body and H2. Size separates it from H2. |
| `.type-h4` | 13px / lh 1.4 | 600, sentence case | Display | Tracking 0.005em. Ink-soft. Labels, table headers, breadcrumbs. No uppercase. |

Both hero tokens, `.type-h1` and `.type-h2` set `text-wrap: balance`, so a two-line heading breaks into two even lines instead of a long line and a stub. Browsers without support wrap as before.

Four heading roles are the whole scale. Lists of titles (a blog index, a brand list) do not get a fifth size between H2 and H3; they use body-size links with a footnote line, the same idiom as an article list. v5.1.0 records this after a review found list pages set every title at H2.

### Body & inline (8)

| Token | Size | Weight | Family | Notes |
|---|---|---|---|---|
| `.type-body` | 16.5px / lh 1.65 | 400 | Body | Body text and paragraphs. |
| `em` | inherit | 400, italic | Body | Names of publications and projects, foreign terms, quoted phrases. |
| `strong` | inherit | 600 | Body | A fact the reader scans for, at most once per paragraph. |
| `a` | inherit | 600 | Body | Bold + 2px shared-red underline, 3px offset. Primary family interaction expression. |
| `a:visited` | inherit | 600 | Body | Ink-soft text, same red rule. Set with `:where`, so chrome links styled by class keep their colour and hover still wins. |
| `code` (inline) | 0.86em | 400 | Mono | Background `rgba(0,0,0,0.05)`, padding 1px 5px. |
| `sub` | 0.7em | 500 | Body | Vertical-align -0.25em. For chemical formulas (CO₂). |
| `sup` | 0.7em | 500 | Body | Vertical-align 0.5em. For units (m²), exponents, footnote refs. |
| `s` | inherit | 400 | Body | Strikethrough, ink-soft. For revisions, deprecated values. |

Underline is for links only. Do not use uppercase labels, eyebrow headings, or coloured text.

### Highlighter

`<mark class="type-highlight">` wraps one to four words of the main headline, once per page. It draws brand red at 15 to 20% as a marker stroke behind the words; the text stays ink. It applies to every brand.

- Never on links, buttons, numbers, body text, or product UI.
- The sentence must read the same without it.
- The checker warns (AG025) when a page carries more than one.

```html
<h1 class="type-hero"><mark class="type-highlight">Net tercihleri</mark> olan küçük bir ekibiz.</h1>
```

### Block-level (9)

| Token | Size | Family | Notes |
|---|---|---|---|
| `.type-blockquote` | 22px / lh 1.35 | Display italic | Border-left 2px ink. `cite` is display, 13px, weight 600, sentence case, ink-soft. Meant for content pages. |
| `.type-pullquote` | 26px / lh 1.22 | Display | Borders top + bottom. Opening curly quote in ink. Meant for content pages. |
| `.type-list-ol` | 16.5px / lh 1.65 | Body | Markers in ink. |
| `.type-list-ul` | 16.5px / lh 1.65 | Body | Markers in ink. |
| `.type-dl` | 16px | Body | dt at 600 weight, dd at 400 weight in ink-soft. |
| `.type-figure` | placeholder + caption | — | Caption is 13.5px italic body, ink-soft. |
| `.type-code-block` | 13.5px | Mono | Background ink, color rule. |
| `.type-table` | 15.5px | Body cells, display headers | Headers 13px, weight 600, ink-soft. Tabular numerals. Last column right-aligned. |
| `.type-divider` | 1px | — | Background var(--rule). For section breaks. |

### Supporting (1)

| Token | Size | Family | Notes |
|---|---|---|---|
| `.type-footnote` | 13px | Body | Ink-soft. `sup` markers in ink, weight 600. |

### Vertical rhythm: two tiers

The system uses **one consistent rhythm**. Visual hierarchy comes from heading size and weight, not from inconsistent spacing. Earlier versions tried "headings hug their content" (asymmetric tops and bottoms, intro-block special cases, deck-after-H1 rules) and the result was a page with five different gap sizes. v2.0 reverts to the simpler logic: every element flows at the same distance from the previous one, and section markers get extra room above.

**Tier 1, Baseline (1em ≈ 16px below every block element)**

Every block-level token has `margin-bottom: 1em` and `margin-top: 0`. The next element sits 16px below, period. Listed exhaustively so future-me knows the rule covers everything:

| Token | margin |
|---|---|
| `.type-hero` | `0 0 32px` (`--space-2xl`) |
| `.type-hero-md` | `0 0 24px` (`--space-xl`) |
| `.type-hero-deck` | `0` (relies on hero's bottom margin) |
| `.type-h1` | `0 0 1em` |
| `.type-body` | `0 0 1em` |
| `.type-blockquote` | `0 0 1em` |
| `.type-list-ol`, `.type-list-ul` | `0 0 1em` |
| `.type-dl` | `0 0 1em` |
| `.type-figure` | `0 0 1em` |
| `.type-table` | `0 0 1em` |
| `.type-code-block` | `0 0 1em` |

**Tier 2, Section break (two heading steps in px, 1em below)**

A heading gets a fixed break above it: 40px (`--space-3xl`) above an H2, 32px (`--space-2xl`) above an H3 or an H4. The bigger heading gets more space, and heading size and weight carry the rest of the hierarchy. Below the heading, baseline 1em, same as everything else. The pullquote and the divider keep 2.5em of their own size. Until v7.3.4 every heading took 2.5em of its own size: 108px above an H2 and 53px above an H3, so a subheading took more space than the section heading above it on a page that set the H2 to 40px (issue 75, v7.3.5).

| Token | margin |
|---|---|
| `.type-h2` | `40px 0 1em` (`--space-3xl`) |
| `.type-h3` | `32px 0 1em` (`--space-2xl`) |
| `.type-h4` (mid-article) | `32px 0 1em` (`--space-2xl`) |
| `.type-pullquote` | `2.5em 0 1em` |
| `hr.type-divider` | `2.5em 0 1em` |
| `.type-footnote` | `2.5em` + `padding-top` + `border-top` (editorial scope) |

CSS adjacent vertical margins collapse to the larger value (per CSS spec), so a heading with `margin-top: 40px` follows a paragraph with `margin-bottom: 1em` at 40px, a clean section break without double-counting margins.

**No eyebrow tier.** Do not place a label above a heading. Put metadata below the heading it describes, for example as `.type-hero-deck` after the H1.

**Containers own their edges.** A heading that opens a card, a section or a band has no top margin. Flex items and padded boxes never collapse margins, so the Tier 2 margin would stack on the container's gap or padding. Card children carry no margin at all: the card's 12px gap spaces them. A `<section>` inside a section is a subsection in the text flow, so its heading keeps the break of its level (v7.3.5).

**One section spacing.** `.agustos-section` and `.band` pad `--section-space` (`clamp(72px, 9vw, 104px)`) above and below. Sections carry no dividing rule. Two sections in a row share one gap, not two. The closing band uses the same spacing.

**A reading page is one article.** Inside `.container--reading`, a section drops its band padding and takes a 40px top margin (`--space-3xl`). An H2 takes the same 40px everywhere (v7.3.5). The margin collapses with the last margin above it, so the break is 40px after a paragraph too. The kit screens `static` and `content` measure 40px at 1440 and 390px (v7.3.4).

**Internal (intra-block) spacing, not part of the rhythm**

These values sit *inside* a block, not *between* blocks, so they don't follow the 3-tier system:

| Element | Internal spacing | Why |
|---|---|---|
| `blockquote padding` | `0.25em 0 0.25em 1.25em` | Vertical breathing inside the quote, horizontal indent past the shared-red border |
| `blockquote cite margin-top` | `0.6em` | Attribution gap below the quote text |
| `pullquote padding` | `1em 0` | Vertical breathing inside the bordered block |
| `list padding-left` | `1.5em` | Bullet/number gutter |
| `dl dt margin-top` | `1em` (zero on `:first-child`) | Gap between definition pairs |
| `dl dd margin` | `0` | Definition hugs its term |
| `figure figcaption margin-top` | `0.5em` | Caption sits tight under the image |
| `code-block padding` | `1em 1.25em` | Code breathing inside the dark block |
| `table cells padding` | `0.5em 0.75em` | Standard table cell breathing |
| `hero-actions margin-top` | `32px` (`--space-2xl`) | Action row sits close to the deck but is visually separate from the statement. |
| `card padding` / `gap` | `24px` / `12px` | The card owns the space around and between its children. |

**Flow spacing specificity.** Scope flow spacing with `article.editorial > * + *` (specificity 0,1,1), not `.editorial > * + *` (0,1,0). Token rules reset `margin` at 0,1,0, so a later token rule overrides a scope rule of equal specificity. Check the computed style of every new flow-spacing rule.

If a specific page needs different spacing, scope it locally, don't loosen the tokens.

---

## Markdown coverage

Every token maps to a standard markdown primitive. The system survives the round-trip from Obsidian → web → PDF → docx → plain text.

| Markdown | Renders as | Notes |
|---|---|---|
| (template-only, not markdown) | `.type-hero` / `.type-hero-md` | Hero tokens live in page templates, not markdown. Markdown bodies start at H1. |
| `# Title` | H1 | First H1 is the page title |
| `## Section` | H2 | |
| `### Subsection` | H3 | Upright, 21px |
| `#### Label` | H4 | Sentence-case label or meta, below its heading |
| `**bold**` | strong | |
| `*italic*` or `_italic_` | em | |
| `[text](url)` | a | Bold + brand underline |
| `` `code` `` | code (inline) | |
| `~subscript~` | sub | Pandoc / Obsidian extension |
| `^superscript^` | sup | Pandoc / Obsidian extension |
| `~~strikethrough~~` | s | GFM standard |
| `> quote` | blockquote | |
| `1. item` | ordered list | |
| `- item` | unordered list | |
| `term : def` | definition list | Pandoc extension |
| `![caption](img.jpg)` | figure | |
| ` ```lang ` | code block | |
| `\| h \| h \|` | table | GFM |
| `---` | divider | |
| `[^1]` and `[^1]: note` | footnote | Pandoc / Obsidian |
| `::: pullquote` | pullquote | Pandoc fenced div, only non-portable token |

**Note on pullquote:** the only token that requires Pandoc-specific syntax. Renders as plain blockquote in CommonMark / GFM environments. Acceptable trade-off for an editorial system.

---

## Logo system

### The symbol

The Laz Güneşi; 18 blades, 20° apart, rotational sun. Every brand carries the exact same symbol in its registered identity ink.
Source of truth: `laz-gunesi-amblem/svg/master.svg` (parametric rebuild from the original Illustrator file). Asset kit (SVG/PDF/PNG/CSS) lives in the same folder.

### The lockup

```
[ Symbol ]  brandname
```

- Symbol height = 1.4× wordmark cap height (≈ `Math.round(size * 1.4 * 0.7)` in pixels)
- Symbol-to-wordmark gap = 0.4× wordmark size
- Wordmark in `--display` (Inter Tight), `font-weight: 650`, `letter-spacing: 0`
- Variable `wght` axis 100–900. Weight 650 is the working wordmark weight: bold enough to hold at 16–20px, still refined beside the Laz Güneşi. The tighter proportions of Inter Tight (vs. Inter) keep the lockup compact without negative tracking.
- **Always lowercase.** `text-transform: lowercase` is enforced on `.lockup__name` so the wordmark renders lowercase regardless of how the brandname prop is passed. The prop can stay Title Case for SEO/aria; CSS does the visual normalization.
- Wordmark color = `--brand` (identity ink; matches the symbol so the lockup reads as one mark)
- **No subtitle.** The publisher mark is one word and one symbol. Sublabels and taglines belong elsewhere (page metadata, page subtitle, footer copy), not on the lockup.
- **No hover underline, ever.** The lockup is identity, not a normal text link. On the web, hover swaps its ink and nothing else: the Ağustos lockup turns from red to black, every other house-brand lockup turns from black to red. If the lockup is clickable, keyboard focus must still be visible through an accessible focus outline or equivalent site-level focus treatment.
- **Optical vertical centering.** The symbol receives `transform: translateY(0.08em)` so its geometric center aligns with the wordmark's *optical* center, not the line-box geometric center. Lowercase text concentrates its visual mass between baseline and x-height; the upper portion of the line-box is mostly empty (only ascenders and the ğ breve reach there). Without the 0.08em shift, the symbol reads as floating high above all-lowercase wordmarks. Tested across all four brand wordmarks including the breve-heavy `ağustos` and ascender-light `pataraz`: single value works for both.

The `mono` expression substitutes `--ink` for `--brand` in single-color contexts (print, stamps, fax-quality).

### Per-brand wordmarks

Each brand has a fixed lowercase display name, mapped in `BaseLayout.astro`:

| Brand class | Wordmark | Color |
|---|---|---|
| `agustos` | `ağustos` | `--brand-agustos` (#cf142a) |
| `pataraz` | `pataraz` | `--brand-pataraz` (#15130f) |
| `pld` | `pld türkiye` | `--brand-pld` (#15130f) |
| `iesdesk` | `iesdesk` | `--brand-iesdesk` (#15130f) |
| `specquick` | `specquick` | `--brand-specquick` (#15130f) |

**Why one-word wordmarks (where possible).** Each visible mark is a single noun: `ağustos`, `pataraz`, `iesdesk`, `specquick`. The exception is `pld türkiye` where the country qualifier is integral to the publication's identity. Drop "teknoloji," "luminaires," "batch", those describe what the brand does, not what it's called.

The page `<title>` is independent and stays Title Case (e.g. "Ağustos Teknoloji, lighting agency and distribution") for SEO and browser-tab readability. Title and wordmark are deliberately separate concerns.

### Three expressions

1. **Positive.** Symbol + wordmark in identity ink on cream/white substrate. Ağustos is red; all other house brands are black. Primary use, 90% of contexts.
2. **Negative.** Symbol + wordmark in cream/white on the identity tile: red for Ağustos, black for every other house brand. For monograms, social avatars, and identity tiles.
3. **Mono.** Symbol + wordmark in ink on cream, or cream on ink. Single-color print, stamps, fax-quality.

No fourth expression exists.

### Favicon & app icons

Each brand has its own favicon: a white tile carrying the Laz Güneşi in the brand's identity ink. The Ağustos favicon carries the red sun. Every other house brand carries the black sun. The white tile keeps the mark readable on any tab colour. The symbol paths are `laz-gunesi-amblem/svg/master.svg`, verbatim.

Canonical kit: `laz-gunesi-amblem/favicon/`, the Ağustos favicon: `favicon.svg` (red sun on the white tile), `favicon.ico`, `apple-touch-icon.png`, `icon-192.png` / `icon-512.png` + `site.webmanifest`, and `favicon-mono.svg` (the bare symbol, for in-page use, not a tab icon). Copy-paste `<head>` tags and regeneration steps live in that folder's `README.md`.

`brand/exports/<brand>/favicon/` holds each brand's kit; the Ağustos copy is byte-identical to the canonical. A site for any other brand uses its own folder. Each brand's manifest sets `theme_color` to its identity ink and `background_color` to white. Adapter `public/favicon.svg` files are **mirrors** of the canonical; update them in the same change. The full asset map and sync rules are in the repo-root `ASSETS.md`.

### Logotype: Inter Tight 650

The wordmark uses **Inter Tight** (Rasmus Andersson. SIL OFL 1.1). Tighter, more compressed sibling of Inter, designed by the same hand and sharing the same skeleton. Variable `wght` axis 100–900 with italics. Used at **650** for the lockup.

Inter Tight is the wordmark face. It is also the system display face, the same family powers heroes, headings, UI labels, and table headers. This consolidation is intentional: in v2.0 the wordmark and the surrounding chrome are drawn from the same family, so the lockup integrates with its context rather than asserting itself as a separate face.

The Turkish `ğ` in Inter Tight is humanist; the breve integrates with the letter body. Inter has gold-standard Latin Extended coverage. `ğ`, `İ`, `ı`, `ş`, `ç`, `ö`, `ü` all draw correctly without locale tricks.

Self-hosted via `@fontsource-variable/inter-tight` (logotype + display) and `@fontsource-variable/inter` (body). System-font fallback on both, so any context where web fonts don't load (email, embedded UI, slow networks) degrades cleanly to the user's native UI font.

CSS tokens:

```css
--display: 'Inter Tight Variable', 'Inter Tight', 'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
--body:    'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji";
```

The full reasoning for the logotype is in `archive/MEMORY.md`, "Turning point 19" to "Turning point 23", and in the section moved from this file.

### Adding a new brand

1. Pick a lowercase wordmark (1–3 words; should look balanced next to the symbol).
2. Use neutral identity ink `#15130f` unless this is Ağustos. A chromatic exception requires an explicit governance change.
3. Add the registry entry and regenerate; generated adapters expose `--brand-{slug}` and the matching class.
4. Add the wordmark to the framework brand map when an adapter requires one.
5. Apply the brand class. The lockup inherits identity ink, font, weight, axes, and the lowercase rule; interactions continue to use shared red.

Total time: ~10 minutes per brand. No new design work.

**Personal brand exception.** The `memregunes` brand is the personal site of Emre Güneş. On a personal site, the person is the work. Its home and about pages may show photographs of him. One is a portrait. Another shows him at work, such as on stage at a lighting event. Its home page may also show up to three recommendations as quotes. Each quote names the writer, the role and the company. Each quote may show a small photo of its writer, but only with the writer's permission. No override carries this any more: v7.0.0 removed the quote rule from the checker and brand `screenOverrides` with it. Every other photography rule applies. When the site adopts v7, its seven menu labels become four plus More, and its social and legal links move to the footer.

---

## Turkish locale handling

Mandatory for Turkish content. Three places to apply:

### HTML

```html
<article lang="tr">
  <h1>Işığın mimariyle buluştuğu yer.</h1>
</article>
```

### CSS (already in global styles)

```css
html {
  font-feature-settings: "locl" on, "kern" on;
}
```

### Markdown via Pandoc YAML frontmatter

```yaml
---
lang: tr
---
```

**Why this matters:** without `lang="tr"`, CSS `text-transform: uppercase` converts lowercase `i` to dotless `I` instead of dotted `İ`. This silently produces wrong Turkish in any uppercase styling, brand names, table headers, H4 labels. With the rule applied, Turkish capitalization renders correctly everywhere.

---

## Accessibility requirements

Accessibility is part of the design system, not an implementation afterthought. The system's restraint only works if interactive states remain legible and keyboard-operable.

### Focus and keyboard

- Every interactive element must expose a visible `:focus-visible` state.
- Shared signal red is used for focus rings because focus belongs to interaction, not identity.
- Skip links are required on full web layouts with persistent navigation.
- Minimum practical target size for button-like controls is 44px on the shorter axis. Editorial text links may be smaller if they sit in prose, but they must have enough line-height and spacing to be tapped comfortably.
- A card whose heading holds a link is the target. The kit stretches that link over the card and moves the focus ring to the card. Other links in the card stay clickable on their own. Breadcrumb links fill their 44px row.

### Contrast

- Body text uses `--ink` on `--paper` or `--paper-white`.
- Secondary text uses `--ink-soft`. `--ink-faint` scores 3.36-3.45 contrast on every substrate, below the 4.5:1 floor for text — it is reserved for non-content marks (form field borders, disabled state) that WCAG does not hold to that floor. Placeholder text is text and uses `--ink-soft`. Footnotes, captions, citations, and proof lines are content and use `--ink-soft`.
- Shared-red links and focus rings must be checked on cream, white, light gray, and dark substrates.
- Negative expressions must preserve cream/white contrast on red Ağustos tiles and black house-brand tiles.

### Motion and state

- Transitions should be short and functional (150ms, `cubic-bezier(0.2, 0, 0, 1)`).
- Do not encode meaning in color alone. Links use both weight and underline; active navigation uses position, text, and state, not just color.
- Dark theme is allowed as an opt-in layer for product UI. It must preserve the same six colour roles, flipped: paper, surface, cream/callout, ink, ink-soft, and shared signal. Marketing pages stay light.

---

## Character coverage

All three faces use the **Google Fonts Latin Plus** glyph set. Verified support for:

- **Currencies**, ₺ € $ £ ¥ ¢
- **Technical**, ° ² ³ ₂ × − ± µ → ← ≈ ≠ ≤ ≥
- **Editorial** — " " ' ' – — … § ¶ © ® ™ † ‡ • ·
- **Turkish alphabet**, ç Ç ğ Ğ ı I i İ ö Ö ş Ş ü Ü
- **Numerals.** Both proportional and tabular (`font-variant-numeric: tabular-nums`)

**Not supported:** Cyrillic, Greek, Arabic, Hebrew, CJK. Not relevant to current business; would require typeface swap if needed.

---

## Substrate strategy

The system supports one white paper, one pale red closing band, one functional gray, plus one opt-in dark UI layer. Same tokens, same rules.

### White `#ffffff` (primary paper)

Marketing pages, product pages, email, documents, dashboards, and product UI. About 70% of every surface.

### Pale red `#fdf5f5` (the closing band only)

The one full-bleed closing band per page (`band band--cream`; token names still say cream). It carries the same section spacing as every section. Never an inset rounded card. Never the page paper. Logo red at 5% into white.

### Light gray `#ebebeb` (functional surface)

Key-figure tiles, image regions, and summary panels.

A single CSS variable swap still flips dark theme. Pale red is not a third page substrate.

### Dark `#15130f` (product UI; locked)

Same six colours, flipped. Paper `#15130f`, surface `#404040`, callout band `#ebebeb`, ink `#ffffff`, ink-soft `#8a8378`, red unchanged.
Buttons invert with the ink: the primary is white on off-black. No red fill.
The footer variables do not follow the flip.
Marketing, catalog, and spec pages stay on white paper. They do not include a theme toggle.

---

## Identity and signal color governance

Color has two separate jobs and they must never collapse into one token:

1. **Identity ink (`brandMark` / `--brand`).** Ağustos is red `#cf142a`. Every other house brand is off-black `#15130f` on light substrates and cream/white on black identity fields.
2. **Interaction signal (`signal` / `--signal`).** Always red `#cf142a` across every brand. Use it only for the 2px content-link rule, the 2px current-page menu rule (a menu hover is a 1px gray rule), keyboard focus, one highlighter stroke per page, and the hover state of a house-brand logo. Buttons are black, never red.

A new chromatic house-brand identity is a philosophy change, not a routine registry choice. It requires updating this specification, `brand/brands.json`, tokens, tests, and the decision history together.

---

## Implementation notes

### Repository architecture

The repository layout, the hand-edited sources and the generated outputs are in `ARCHITECTURE.md` in the source repository. Consumers integrate through the `ui/` kit or `tokens/design-system-handoff.json`, and never run the generators or repair a generated file by hand. The system does not depend on Astro. Rails apps use the Rails adapter or copy the platform-neutral tokens directly.

### Web utilities

The platform-neutral web behavior lives in `tokens/web.css.tmpl`; its values resolve from `tokens/design-tokens.json`. `tokens/agustos.css` and adapter token files are generated outputs.

Current non-token utilities:

| Utility | Role |
|---|---|
| `.paper-white` | Compatibility class. White is already the default paper. |
| `html[data-theme="dark"]` | Product-UI dark theme. Same six colours, flipped. Paper `#15130f`, surface `#404040`, callout `#ebebeb`, ink `#ffffff`, ink-soft `#8a8378`. Buttons invert with the ink. Marketing pages do not set this. |
| `.site-frame` | Shared site-chrome frame: 1180px content measure plus 32px gutters. |
| `.container` | The same frame geometry plus default vertical page padding. |
| `.container--reading` | A content page: the frame keeps its left edge, and each block stops at the reading line. The side zone to the right stays free. |
| `.agustos-contents` | "On this page" on a long legal page: a `details` disclosure of the main sections, a direct child of `.container--reading`. A folded line below 1280px; open and sticky in the side zone at 1280px and wider. No script. |
| `.hero-actions` | The opening's button row: one primary and one secondary `agustos-button`. |
| `.skip-link` | Keyboard accessibility utility for persistent navigation layouts. |
| `.site-lockup`, `.site-lockup__symbol`, `.site-lockup__name` | The brand lockup: exact symbol plus lowercase wordmark. |
| `.site-sidebar*`, `.site-sidebar-bar`, `.site-sidebar-burger`, `.site-sidebar-layout` | The sidebar chrome, product UI only. Drawer below 1024px. |
| `.site-header*`, `.site-footer*` | The top menu and the footer, on every website. Five items at most, the rest under `site-header__more`. Drawer below 1024px. |
| `.breadcrumb`, `.breadcrumb__link` | The trail above a page title. |
| `.stack`, `.cluster`, `.prose`, `.grid-2`, `.grid-3`, `.grid-4`, `.grid-aside`, `.band`, `.band--cream`, `.table-scroll` | The layout layer. No page declares its own frame, band, grid, or measure. |

UI primitives — NEW IN v3.1. Product-surface controls in the same grammar as the editorial layer:
hairline rules, 6/12px radii, one 2px signal accent per element, 44px targets.

| Group | Classes | Notes |
|---|---|---|
| Forms | `.agustos-fieldset` `.agustos-field` `.agustos-field--invalid` `.agustos-label` `.agustos-label--required` `.agustos-input` `.agustos-textarea` `.agustos-select` `.agustos-check` `.agustos-hint` `.agustos-error` | Inputs are 16px to prevent iOS focus zoom. Checkboxes and radios use `accent-color: var(--ink)`. Labels are sentence case. The invalid state responds to `aria-invalid` as well as the class. `.agustos-hint` uses `--ink-soft`, not `--ink-faint`. |
| Buttons | `.agustos-button` `--primary` `--secondary` `--quiet` | Buttons are black on every brand. Primary is filled black; hover lightens it to dark gray. Secondary is a quiet outline; hover firms the border to ink. `--quiet` is the in-prose red-ruled text action on a button element. Pressed, a button moves 1px down; the primary returns to full ink and the secondary fills light gray. Disabled (`disabled` on a button; on a link, no `href`, `role="link"` and `aria-disabled="true"`), it turns gray and does not react. Never two primary buttons in one band. In dark theme they invert with the ink. |
| Badges | `.agustos-badge` `--success` `--warning` `--danger` `--info` `--signal` | The `.type-h4` typographic register at badge scale. Bordered and transparent, never a filled pill. |
| Notices | `.agustos-notice` `.agustos-notice__title` `--success` `--warning` `--danger` `--info` | The same 2px left-rule grammar as `blockquote` and `.agustos-card--marked`, in ink or state color, not signal red. |
| Tabs | `.agustos-tabs` `.agustos-tab` `.agustos-tabs__panel` | Active state via `aria-selected="true"` or `.is-active`; a 2px signal underline, the existing current-item marker. |

Deliberately absent, and to stay absent: pagination, modals, tooltips, dropdowns (the top
menu's More is the one exception, with the contents list as a disclosure of the page, not a menu), toasts, and progress bars. Breadcrumbs, the two chromes, and the layout layer joined the kit in v6.0.0
because every reference screen needed them. Everything else composes from cards, buttons, the
layout classes, and the `type-*` classes. This is a restrained editorial system, not a
component framework.

`--state-*` tokens are substrate-specific as of v3.1: the light values score 2.19-3.11 contrast on
dark paper, so `html[data-theme="dark"]` overrides all four with `state*Dark` variants that clear
7:1. Any future component consuming a state color inherits this automatically.

Hero, section, card, and editorial-link recipes are emitted into every web adapter.

The 1180px value is the content measure, not the padded outer width. `.site-frame`
and `.container` therefore cap their border box at `1244px`: 1180px
of content plus a 32px gutter on each side. This keeps header, homepage,
breadcrumbs, page content, and footer aligned without narrowing the readable
measure. Component-specific utilities may set vertical padding, but should not
redefine this horizontal geometry. Every region shares two vertical lines: the
frame's left edge, where the logo, the breadcrumbs, the text and the footer
contact block start, and the reading line (`--measure-body`), where the text of
a content page and the footer contact block end. Right of the reading line, after
the `--space-xl` gap, is the side zone: the footer groups, and a side column when
a content page needs one. The header menu stays centered and is not an anchor,
because its width changes with every label and language. Below 1280px the side
zone cannot hold three footer groups, so the footer groups move under the contact block.

Composition rules the web template follows:

- Preserve Inter Tight, Inter, and JetBrains Mono. Establish hierarchy through readable size, weight, and spacing.
- Keep wordmarks lowercase at Inter Tight 650. Use the exact Laz Güneşi asset and registered identity ink.
- Use one 1180px alignment frame with 32px gutters. Scale type with `clamp()`. Lay out card rows with the kit's layout classes (`grid-2`, `grid-3`, `grid-4`, or `cluster`); the grids collapse to one column below 760px. Never declare a page-local grid.

### Site chrome

The kit ships two chromes, and the screen family picks one, not the brand. Every website
(marketing, content, catalog, and document screens) uses the top menu and the footer. Product UI
(the app shell) uses the sidebar. Brands no longer register a chrome: v7.0.0 removed `chrome`
from `brand/brands.json`, and the build rejects it. The checker warns (AG026) on a sidebar outside
product UI, and (AG027) on a sixth top-menu item. Both chromes are generated from
`tokens/web.css.tmpl` into every web stylesheet. No chrome rule exists anywhere else in this
repository; a test enforces it. The kit uses JavaScript only when it is the logical choice:
drawers are native popovers with a close button (`site-header__close`, `site-sidebar__close`),
collapsible groups and More are `details`, and `ui/agustos-chrome.js`, about 30 lines, closes
More on Escape, an outside click or focus leaving, and closes an open drawer when focus leaves
it. Without the script More still opens and closes on click, and a drawer still closes on
Escape, an outside click and its close button. Print drops the menus, the drawers and the footer links.

The top menu (`site-header`) is a sticky one-row header inside the shared frame: the lockup,
primary links, and an end slot for the action, search, and language. The current page
(`aria-current="page"`) carries a 2px red rule underneath. On a nested route the parent item is
the current section: it carries `aria-current="true"`, never `"page"`, and the same rule, so a
screen reader does not announce the parent as the current page. A hover darkens the ink over a
1px gray rule, so red always means "you are here". The header is 65px (`--site-header-height`),
and the page's scroll padding keeps an anchor target or a focused element below it; the padding
adds 1px (`--anchor-snap`) because a browser scrolls to whole pixels. The row never wraps: between 1024 and
1279px its spacing tightens, and five labels fit at 1024px up to about 65 characters together,
More included. Below 1024px the burger opens the panel as a drawer; the page behind it holds
still.

**Five items at most.** The top menu holds at most five links. Put every other page in one
`site-header__more` `details` whose `summary` is a `site-header__link` reading "Daha fazla" or
"More". Its `site-header__more-menu` holds `site-header__more-link` items. On desktop the menu
floats under the item on a 12px radius with the system's one shadow; in the phone drawer the
More items open inline. When the current page sits under More, the More item carries the red
rule. Social, legal, and language links do not go in the top menu; they live
in the footer.

The footer (`site-footer`) is light and small: white paper under a hairline, in the same frame.
`site-footer__brand` holds the lockup and one `type-footnote` line. One `site-footer__links`
list holds a single row of `site-footer__link` items for social, legal, and language. No button:
the top menu and the closing band carry the action. `--footer-paper` is white and `--footer-ink`
off-black, and neither follows the theme flip. v7.0.0 retired `site-footer__cols`, `__col`,
`__col-heading`, `__list`, and `__cta`.

**Site map (optional, v7.1.0).** Above the bottom row, `site-footer__map` holds
`site-footer__contact` (the lockup and an `address`: the legal name, the registered address, and
a `site-footer__links` row with the phone and email)
and one `site-footer__groups` nav of at most three `site-footer__group`s. Each group is a
sentence-case `site-footer__group-title` over at most five `site-footer__link`s in
`site-footer__group-links`: the pages people look for, such as the represented brands, not every
page. The contact block ends on the reading line and the groups fill the side zone; below 1280px the groups move under the contact block, and below 760px they sit two across. The bottom row then holds the footnote (with the
MERSİS number on a Turkish company site) and the legal, social and language links, including the
company-information page that TTK 1524 asks of a capital company. Footer links help visitors and
page discovery; the search-engine work belongs to `sitemap.xml`, which every site publishes and
registers in Google Search Console (Astro `@astrojs/sitemap`, WordPress core `wp-sitemap.xml`,
Rails `sitemap_generator`).

The sidebar (`site-sidebar`), product UI only, is a fixed 240px column, white paper with a
hairline rule on the right: the lockup, primary links, `details` groups, one action, a utility
slot for search, language, and the theme control, and a note. The current page carries a 2px
red rule on the left of its link, and a closed group that holds it carries the rule on its
summary; a hover is a 1px gray rule. Below 1024px a sticky bar with the lockup and a burger opens
the sidebar as a drawer.

The lockup (`site-lockup`) is the exact symbol inline plus the lowercase wordmark in the
registered identity ink. Hover swaps the ink: Ağustos red to black, every other brand black to
red. Dark theme lifts house brands to white; Ağustos stays red.

Destinations, copy, and link lists are configuration, never brand policy. Search is an adapter
concern: the Astro reference uses Pagefind inside its own `site-header__search-*` classes; the
Rails adapter uses a GET form into a Turbo Frame. Every control is at least 44px; the
responsive search input is 16px to prevent iOS focus zoom.

### Rails adapter

Rails monoliths should use `adapters/rails/` as the starting point. The adapter provides:

- `app/assets/stylesheets/agustos/tokens.css`
- `app/assets/stylesheets/agustos/components.css`
- `app/helpers/agustos_theme_helper.rb`
- `app/views/layouts/agustos.html.erb`
- shared ERB partials for the exact lockup, header, footer, and Turbo search results
- focused Stimulus controllers for drawer, theme, and search panel behavior

The Rails adapter is plain ERB first. If an app uses ViewComponent, components can wrap the same semantic pieces later without changing the design grammar.

### Office and Google adapters

`brand/build_templates.py` reads `tokens/resolved.json` to create A4 Word letterheads and styled document templates. The document template uses native Word styles and imports into Google Docs; the title sanitizer audit must pass before release.

`brand/build_presentation.mjs` uses `@oai/artifact-tool` to create editable 16:9 PowerPoint layouts. The same PPTX is the Google Slides import seed. Web recipes are translated into presentation-native compositions rather than copied as UI.

### Font loading

`tokens/agustos.css` declares font **stacks**, not faces. A project that loads it without also
loading the fonts renders in system sans while appearing to comply. This is the most common way to
get the system wrong, so the kit ships the fonts.

Primary path — `ui/agustos-fonts.css` plus `ui/fonts/*.woff2`, loaded **before** `agustos.css`.
Subset to Latin, Latin Extended-A/B, Turkish, typographic punctuation, and the lira sign; full
variable weight axes retained, so the wordmark's 650 still resolves. Generated by
`scripts/build_ui_fonts.py`, which is deliberately outside the main build because subsetting needs
`fonttools[woff2]` and the local gate runs without it. The `url()` references are relative, so one file
serves both the CDN and a vendored copy. SIL Open Font License: each `OFL.txt` travels with the
binaries.

npm alternative — `@fontsource-variable/inter-tight`, `@fontsource-variable/inter`, and
`@fontsource-variable/jetbrains-mono`. This is what agustos.com uses; such projects skip
`agustos-fonts.css` entirely.

Prototype fallback — the Google Fonts `<link>`. Prototypes only: it puts a third-party request on
every page load, which is the wrong posture for TR/EU privacy.

Fallback stacks ensure no rendering failure even if web fonts don't load. Email contexts will
permanently use native fallbacks from the stack; this is acceptable.

### Browser support

The system uses CSS custom properties, `font-variation-settings`, `color-mix()`, `font-feature-settings`. All supported in browsers from 2022 forward. No IE support, no Edge Legacy support, both are end-of-life.

### QA checklist

Run this checklist before calling a system change complete:

1. Render the typography showcase and confirm the established typography/content classes appear.
2. Inspect computed margins for H2/H3/H4, body, lists, tables, code blocks, and dividers; verify the 1em baseline and the heading breaks (40px above an H2, 32px above an H3 or an H4) actually render.
3. Test Turkish uppercase with `lang="tr"` on H4/table-header-style text: `başlık`, `i`, and `ışık` must uppercase correctly.
4. Check cream, white, light gray, and dark substrates.
5. Check red Ağustos and black house-brand lockups separately; verify shared-red link, focus, and marker behavior under every brand class.
6. Test keyboard navigation: skip link, header nav, the More menu, search results, language controls, and the hero buttons. On product UI, also test the theme control.
7. Verify the More menu (floating on desktop, inline in the drawer, closing on Escape and an outside click), responsive search row, drawer close button, backdrop and Escape, 44px controls, and 16px responsive input.
8. Verify mobile and desktop widths; text must not overlap, clip, or force horizontal scrolling except inside code blocks and wide tables.
The factory checks (generators, Office exports and a `ui/` release) are in `ARCHITECTURE.md`, section "Testing", in the source repository.

---

## Versioning

This is **v7.4.0**. The release adds the "On this page" list, `agustos-contents`: a no-script disclosure of a long legal page's main sections, folded below 1280px and open and in view in the side zone at 1280px and wider, and checker warning AG031. v7.3.5: The patch gives headings two fixed breaks: 40px above an H2 and 32px above an H3 or an H4, on every page. Before, each heading took 2.5 times its own size, so an H3 took 53px, more than the 40px of a reading-page H2. A heading that opens a `<section>` inside a section keeps its break. v7.3.4: The patch gives a reading page one break above each H2 and each section: 40px (`--space-3xl`), a margin that collapses with the last margin above it. Before, a section on a reading page kept the band padding of a marketing page (121 to 144px at 1440px), and a bare H2 took 2.5 times its own size (108px). v7.3.3: The patch fixes three defects and five small rules from the 2026-09-30 design review. An open drawer closes when keyboard focus leaves it, so focus never lands on the page behind it (`ui/agustos-chrome.js`, now on every screen). A disabled link drops its `href`, because `aria-disabled` alone does not stop a click; the checker warns on one that keeps it (AG030). A search result excerpt takes the ink on its hover fill (2.76:1 in the dark theme before). Table captions align to the start, `color-scheme` follows the theme, a footer link hover is the 1px gray rule, and reduced motion sets `--dur` to 0s for every transition. v7.3.2: The patch fixes three defects. A parent menu item on a nested route carries `aria-current="true"`, not `"page"`, and the chrome draws the red rule for both; the checker warns on a parent marked `"page"` in built pages (AG029). The adoption snippet says that only product UI uses the sidebar. Every anchor offset adds 1px (`--anchor-snap`), because a browser scrolls to whole pixels and a fractional target stopped under the sticky chrome. v7.3.1: The patch moves the reading column of a content page back to the frame's left edge and gives every region one reading line: `--measure-body` becomes 41rem (656px, about 75 characters), the text of a content page and the footer contact block end on it, and the footer groups fill the side zone to its right. Below 1280px the footer groups move under the contact block. v7.3.0: The kit owns the header search and the language link: one recipe replaces the copies in the Astro and Rails adapters, its text clears 4.5:1, its input is 16px, and below 1024px the anchor offset adds the 61px search row. v7.2.0 gave every content page one reading column: `.container--reading` puts the title, the text and the headings at the 65ch body measure in the center of the frame, so a wide screen no longer shows text on the left half and nothing on the right. The screens table gains a derived Column (reading for the content family, frame for the rest), and the checker warns on a full-width `container` on a content screen (AG028). v7.1.0 fixed the chrome against WCAG 2.2 and common navigation practice, measured in a browser: a focused element no longer hides under the sticky top menu, the top menu keeps one row at 1024px, the More menu closes on Escape and an outside click (`ui/agustos-chrome.js`, the kit's first script), each drawer gains a close button and holds the page still, a More or a sidebar group shows the current page inside it, print drops the chrome, language links carry `lang`, and the checker warns on a sixth top-menu item (AG027). A menu hover becomes a 1px gray rule, so the 2px red rule marks the current page alone, and the footer gains an optional site map. v7.0.2 kept an in-page anchor below the sticky top menu at every width (`--site-header-height`), and the Astro and Rails adapters keep the focus ring on a search result. v7.0.1 fixed interactive states in both themes, measured in a browser: form field borders clear 3:1 and placeholders 4.5:1, the dark theme dims a hover instead of turning text red, the footer and the closing band stay light islands in the dark theme, the dark More menu and logo hovers work, and buttons gain pressed and disabled states. The registry's `states` table lists every pair, and the brand guidelines gain Colour in use and Emphasis pages. v7.0.0 reset the website layer to convention and kept identity and the engine. Chrome follows the screen family, not the brand: every website uses the top menu (five items at most, the rest under More) and a light footer; product UI uses the sidebar, and `chrome` left `brand/brands.json`. Type sits on one golden scale (13 to 89px) with four weights; radii are 6 and 12px; sections share one spacing and no dividing rule. Red is identity and signal, never action: buttons are black everywhere, the dark-theme red primary is gone, house-brand logos turn red on hover, and one highlighter stroke per page joins the kit. The hero opens with two `agustos-button`s; `hero-links`, `hero-link*`, `hero-action*` and the footer columns and button are retired. The checker guards identity with errors and taste with warnings: AG022 (primary CTA count), AG023 (quotes), the screens-table fields `primaryCtaMax` and `quotes`, and brand `screenOverrides` are removed; AG025 (highlighter) and AG026 (sidebar on a website) join. Each brand's favicon is a white tile with its own sun: red for Ağustos, black for every other brand. History: v6.6.1 kept an in-page anchor below the sticky sidebar bar on phones (the product sidebar in v7). v6.6.0 styled bare `h1` to `h4` and `p` with their `.type-*` rules, so Markdown and CMS output matches the kit without classes. v6.5.0 gave the type scale its middle step (an upright H3) and set the hero trust line in the 15.5px `bodyCompact` size. v6.4.0 made cards and breadcrumbs 44px targets: a card's heading link stretches over the card, and the checker warns (AG013) when it cannot. v6.3.0 tightened the rhythm: a heading that opens a card, a section or a band lost its section-break margin, and content text moved from `--ink-faint` to `--ink-soft` to pass contrast. v6.2 added brand `screenOverrides`, removed in v7.0.0. v6.1.0 made the checker enforce the screens table on every page (`data-screen` on `<body>`; primary CTA limit, quotes, and theme per row; v7.0.0 kept only the theme rule, as a warning), added the `content-index` screen, and gave both reference adapters the `screen` switch. v6.0.0 recorded the chrome contract: consumers replace their local chrome with the kit's and adopt one name. v5.0.0 recorded the design philosophy change. Subsequent changes follow semantic versioning:

- **Major.** Breaking changes to token names, structural removal, philosophy shifts
- **Minor.** New tokens, new brand additions, additive-only changes
- **Patch.** Color refinements, weight tuning, fallback adjustments

Versions are three-segment. Four-segment numbers break jsDelivr's semver ranges, and the kit is
pinned by tag.

`VERSION` is the single source. `tokens/design-tokens.json`, the handoff, the manifest, and
`ui/kit.json` must all agree; a test enforces it, and the generator refuses to build when `VERSION`
and the registry disagree.

**Any change under `ui/` requires a VERSION bump, a dated CHANGELOG section, and a rebuild in the same
change.** Consumers pin the `v<VERSION>` tag, which `.github/workflows/tag-release.yml` creates on the merge
when the release reaches `main`; nobody tags by hand. `VERSION` participates in the manifest's source hash, so the local gate
fails if the rebuild is missed — without that, a version bump would leave every pinned URL in the kit
stale while `--check` still reported clean.

Each version updates this document, lists its changes in `CHANGELOG.md`, and records its decisions in `MEMORY.md`.

---

## Authority

This system was designed by Emre Güneş in dialogue with Claude over the course of one extended design conversation in May 2026. It reflects Emre's editorial sensibility, business priorities, and engineering principles. Decisions are documented in `MEMORY.md`, and the history before 2026-09-24 in `archive/MEMORY.md`.

The system is the product of his judgment, not Claude's. Future changes should be made by him, with reasoning documented.
