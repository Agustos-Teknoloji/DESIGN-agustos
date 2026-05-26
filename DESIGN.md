# Ağustos Design System

**Version 2.1.1** · Type-first design system for Emre Güneş's brand portfolio
**Last updated:** May 26, 2026
**Status:** Patch update · Rule clarifications, implementation notes, accessibility gates, and QA checklist · Token count remains 24

---

## What this is

A typographic design system covering web, document, and product UI surfaces for a multi-brand portfolio. Built typography-first because that's the durable layer, colors change, components change, typefaces and rules persist.

The portfolio currently spans:

- **Ağustos Teknoloji.** Lighting agency and distribution (red, `#cf142a`)
- **Pataraz.** Premium luminaire brand at mid-tier pricing (blue, `#1a24cc`)
- **PLD Türkiye.** Lighting publication archive (black, `#1a1a1a`)
- **Photometric Batch.** Software for lighting data (green, `#1f6b4a`)

Future brands plug in by choosing a name and a color. No new typography, no new logo design, no new structural decisions.

---

## System philosophy

Six rules that govern every decision in the system. These are non-negotiable; they're how the system survives over time.

### 1. Portability over preference

Every design decision must survive translation across markdown → web → PDF → docx → plain text. Treatments that exist only in HTML are luxuries, not primitives. If a treatment can't be expressed in standard markdown, it doesn't belong in the system.

### 2. The publisher precedes the brand

All visible brand systems express "from Emre's house" first, individual brand identity second. This is the inverse of most multi-brand systems. The shared symbol and shared typography identify the publisher; brand color and name identify the publication.

### 3. One symbol, forever

The Laz Güneşi is the publisher's mark. Every brand carries it, regardless of category. The symbol is fixed; the discipline of one symbol is more valuable than per-brand symbolism. Brands flex on two axes only: name and color.

### 4. Color must sit with cream

Brand colors must be selected (or refined) for the cream substrate. Raw web colors fight the paper; designed colors integrate. Pataraz's original `#0000FF` was refined to `#1a24cc` for this reason.

### 5. Brand color is a signal, not decoration

The link is the primary interactive brand expression: bold + 2px brand-colored underline. Brand color may also appear where it carries a defined semantic role: identity marks, the page-defining hero eyebrow, editorial markers (blockquote border, pullquote opening quote, list markers, footnote refs), and focus rings. Everything else is ink on paper. Brand color carries meaning (identity, navigation, structure, accessibility), never surface decoration.

### 6. Turkish content declares its language

Every Turkish content block carries `lang="tr"`. CSS enables `font-feature-settings: "locl"` globally. This is a correctness requirement, not a preference, without it, `text-transform: uppercase` produces wrong capitalization (i → I instead of i → İ).

---

## The type stack

Three families. Each with one job. No overlap. As of v2.0 the system runs on a single sibling pair (Inter Tight + Inter) plus a code mono, the editorial serif has been retired in favor of one paired family from logotype to footnote.

### Inter Tight (Display)

Designed by Rasmus Andersson, the same designer as Inter, as a tighter, more compressed sibling for display use. Variable wght axis 100–900 with italics. Shares Inter's skeleton, so the pair harmonizes by construction. Used for the **logotype, hero tokens, all headings (H1–H4), eyebrows, UI labels, table headers, badges, dashboard numerals, pullquotes**, and any "designed" surface.

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

## CSS variables

Drop into any project. Twelve base variables define the system, plus one runtime alias (`--brand`) that resolves to the active brand color.

```css
:root {
  /* Substrate */
  --paper: #fefcf2;        /* Cream, branded contexts */
  --paper-white: #ffffff;  /* White, universal fallback, email, default web */

  /* Ink */
  --ink: #1a1a1a;          /* Primary text */
  --ink-soft: #4a4a4a;     /* Secondary text, soft headings */
  --ink-faint: #8a8a8a;    /* Tertiary, captions, footnotes */

  /* Rule (separator color) */
  --rule: #e8e3d0;         /* For cream substrate */
  --rule-white: #e8e8e8;   /* For white substrate */

  /* Brand colors, pick one per page */
  --brand-agustos: #cf142a;
  --brand-pataraz: #1a24cc;
  --brand-pld: #1a1a1a;
  --brand-photometric: #1f6b4a;
  --brand: var(--brand-agustos);

  /* Type stacks, v2.0 */
  --display: 'Inter Tight Variable', 'Inter Tight', 'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --body:    'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji";
  --mono:    'JetBrains Mono', 'SF Mono', Menlo, Consolas, ui-monospace, monospace;
}
```

**Note on naming.** v1.x used `--serif`, `--sans`, `--logotype` to name the three faces by category. v2.0 names them by role. `--display` (anything designed) and `--body` (anything read at length), because the system no longer has a serif/sans split. Mono is unchanged.

**Per-brand application:**

```css
.brand-agustos { --brand: var(--brand-agustos); }
.brand-pataraz { --brand: var(--brand-pataraz); }
.brand-pld     { --brand: var(--brand-pld); }
.brand-photo   { --brand: var(--brand-photometric); }
```

Inside any brand-scoped element, `var(--brand)` resolves to the correct color. Adding a new brand is one line. Without a brand class, `--brand` falls back to Ağustos red.

**Substrate helpers:**

```css
.paper-white {
  --paper: var(--paper-white);
  --rule: var(--rule-white);
}
```

White is an opt-in working substrate. Cream remains the default branded substrate.

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

**The `ss01` stylistic set** is enabled globally for Inter, it switches the single-storey lowercase `a` to the more neutral two-storey form Inter ships in `ss01`. This is a project-level taste decision; flip it off if a future audit prefers the default.

---

## The 24 tokens

Each token has exactly one job. When writing content, ask only: which one of these is this? Token count went from 22 → 24 in v2.0 with the addition of `.type-hero` and `.type-hero-md`; v2.1.1 keeps the count at 24 and clarifies named component styles around the tokens.

### Hero (2) · NEW IN v2.0

| Token | Size | Weight | Family | Notes |
|---|---|---|---|---|
| `.type-hero` | clamp(56px, 9vw, 112px) / lh 0.96 | 300 | Display | Tracking -0.045em. Margin-bottom 0.5em. **Big hero**, landing pages, launches, brand portfolio. One per page maximum. |
| `.type-hero-md` | clamp(40px, 6vw, 72px) / lh 1.02 | 400 | Display | Tracking -0.032em. Margin-bottom 0.5em. **Medium hero**, inner-page headers, section openers, feature blocks. |

The hero deck is a separate utility (`.type-hero-deck`), upright body at 18–21px, max-width 54ch, paired with either hero token. It is a supporting lead, not a quote, so it does not use italic. Eyebrow above hero uses `.type-h4` in brand color; this is an allowed semantic brand accent because it labels the page-defining statement.

### Hero element styles

The HERO section is a page-opening composition, not a new token family. It combines two typography tokens, one deck utility, and component styles. On the homepage, the hero text should occupy the first viewport as a top-aligned editorial opening; the page should not vertically center the statement or split it into text/media columns. Name the parts consistently so design notes, implementation, and CMS fields all refer to the same things.

| Element | Style | Required | Definition |
|---|---|---|---|
| **Headline** | `.type-hero` or `.type-hero-md` | Required | The page statement. Ink-on-paper, never a link. On the current Ağustos homepage, use `.type-hero-md`; it matches the existing site voice: calmer, slightly heavier, and less launch-like. Reserve `.type-hero` for more dramatic landing pages, launches, and brand portfolio openings. Let the homepage headline use the full page measure; do not constrain it to a narrow poster column. One headline per hero. |
| **Supporting Copy** | `.type-hero-deck` | Recommended | One supporting lead, 1-2 sentences, max-width 54ch, upright body, ink-soft. Explains the promise; does not repeat the headline. |
| **Primary CTA** | `.hero-link.hero-link--primary` inside `.hero-links` | Optional | Main navigational path. The homepage may have two primary path links when it opens into two equal business lines. Bold editorial link with arrow and brand-colored underline. No filled button in the homepage hero. |
| **Secondary CTA** | `.hero-link.hero-link--secondary` inside `.hero-links` | Optional | Lower-priority contact or support action placed after the primary path links. Ink-soft editorial link with arrow and brand-colored underline. |
| **Trust Signals** | `.hero-trust` | Optional | Compact proof line below the actions: year range, client count, geography, partner names, standards, warranty, press, or certification. Body family at 13.5-14px, ink-faint or ink-soft. No badges, pills, or logo-wall treatment in the hero. |
| **Hero Visual** | `.hero-visual` | Optional | Actual product, place, object, state, screenshot, diagram, render, or media. On the homepage, keep it below or after the text-led first viewport unless the visual is the product itself. Avoid decorative-only gradients, abstract logo collages, or framed visual cards that compete with the headline. |

Optional `.type-h4` eyebrow may sit above the headline for category/context. Optional `.type-body` summary may sit between Supporting Copy and CTAs only when the page needs a second level of explanation; it is not one of the named HERO styles.

Recommended order:

1. Optional `.type-h4` eyebrow.
2. **Headline**.
3. **Supporting Copy**.
4. Optional `.type-body` summary.
5. `.hero-links` containing one or two **Primary CTA** links and optional **Secondary CTA**.
6. **Trust Signals**.
7. **Hero Visual** as the adjacent or following visual plane.

Do not make the hero headline itself the call to action. Headline links create an oversized underline and confuse hierarchy: the statement starts behaving like a button. Keep the title as ink-on-paper; put navigation in the action row.

CTA philosophy for the homepage is **editorial link, not product button**. Stripe-style filled buttons conflict with the rule that brand color is a signal, not a filled surface. Pentagram-style outlined boxes are internally consistent, but they still turn the action into a UI object. Ağustos should follow the restrained publisher pattern: bold text link, arrow, brand underline. The hero stays typographic.

Hero component styles are web/component utilities, not typography tokens. Homepage hero action utilities are editorial links; boxed `.hero-action` utilities may still be used for lower section-opening CTA rows where target size and scannability matter more than first-impression typography. `.hero-trust` and `.hero-visual` belong to hero sections only:

| Utility | Role | Style |
|---|---|---|
| `.hero-links` | Homepage action row | Flex row, wraps, 1rem row gap, 1.5rem column gap, 2rem above. |
| `.hero-link` | Base homepage action link | Display family, 17-21px, weight 600, brand-colored 2px underline, arrow after text. The arrow may be literal text or `::after`; either is acceptable if accessible text stays clean. |
| `.hero-link--primary` | Main homepage path action | Ink text, weight 600. Use one or two when the homepage has equal primary destinations. |
| `.hero-link--secondary` | Secondary homepage action | Ink-soft text, weight 500. |
| `.hero-trust` | Trust signal line | Body family, 13.5-14px, line-height 1.5, ink-faint or ink-soft, margin-top 2rem to 3.5rem after actions. Items stay textual and compact. |
| `.hero-visual` | Visual plane | Media container for the hero image/render/screenshot/diagram. Full-width within its layout column, no decorative card chrome, caption through `.type-figure` when needed. |

Actions are links, not generic buttons. In the homepage hero they should not look button-like: the action is part of the typographic composition. In lower sections, boxed links can appear when the surrounding layout needs clearer tap targets.

**Implementation status.** `.hero-links`, `.hero-link`, `.hero-link--primary`, `.hero-link--secondary`, and boxed `.hero-action*` utilities exist in the local `tokens.css`. `.hero-trust` and `.hero-visual` are specified here as required hero utilities and should be mirrored into `tokens.css` before they are used in production hero templates.

### Headings (4)

| Token | Size | Weight | Family | Notes |
|---|---|---|---|---|
| `.type-h1` | 44px / lh 1.05 | 500 | Display | Tracking -0.026em. Page title, first H1 is the page itself. |
| `.type-h2` | 24px / lh 1.18 | 500 | Display | Tracking -0.014em. Section break. |
| `.type-h3` | 18px / lh 1.3 | 500, italic | Display | Italic separates categorically from H2. Inter Tight italics carry well. |
| `.type-h4` | 12px | 700, uppercase | Display | Tracking 0.14em. Absorbs eyebrow + meta + label roles. |

### Body & inline (8)

| Token | Size | Weight | Family | Notes |
|---|---|---|---|---|
| `.type-body` | 16.5px / lh 1.65 | 400 | Body | Body text and paragraphs. |
| `em` | inherit | 400, italic | Body | Titles, foreign words, technical terms, deck/byline by role. |
| `strong` | inherit | 700 | Body | Emphasis, key terms. |
| `a` | inherit | 600 | Body | Bold + 2px brand-color underline, 3px offset. Primary interactive brand expression. |
| `code` (inline) | 0.86em | 400 | Mono | Background `rgba(0,0,0,0.05)`, padding 1px 5px. |
| `sub` | 0.7em | 500 | Body | Vertical-align -0.25em. For chemical formulas (CO₂). |
| `sup` | 0.7em | 500 | Body | Vertical-align 0.5em. For units (m²), exponents, footnote refs. |
| `s` | inherit | 400 | Body | Strikethrough, ink-faint. For revisions, deprecated values. |

### Block-level (9)

| Token | Size | Family | Notes |
|---|---|---|---|
| `.type-blockquote` | 18px / lh 1.55 | Body italic | Border-left 2px brand. `cite` is display, uppercase. |
| `.type-pullquote` | 26px / lh 1.22 | Display | Borders top + bottom. Opening curly quote in brand color. |
| `.type-list-ol` | 16.5px / lh 1.65 | Body | Markers in brand color. |
| `.type-list-ul` | 16.5px / lh 1.65 | Body | Markers in brand color. |
| `.type-dl` | 16px | Body | dt at 600 weight, dd at 400 weight in ink-soft. |
| `.type-figure` | placeholder + caption | — | Caption is 13.5px italic body, ink-faint. |
| `.type-code-block` | 13.5px | Mono | Background ink, color rule. |
| `.type-table` | 14px | Body cells, display headers | Tabular numerals. Last column right-aligned. |
| `.type-divider` | 1px | — | Background var(--rule). For section breaks. |

### Supporting (1)

| Token | Size | Family | Notes |
|---|---|---|---|
| `.type-footnote` | 12.5px | Body | Ink-faint. `sup` markers in brand color, weight 600. |

### Vertical rhythm: three tiers, no exceptions

The system uses **one consistent rhythm** with one structural exception. Visual hierarchy comes from heading size and weight, not from inconsistent spacing. Earlier versions tried "headings hug their content" (asymmetric tops and bottoms, intro-block special cases, deck-after-H1 rules) and the result was a page with five different gap sizes. v2.0 reverts to the simpler logic: every element flows at the same distance from the previous one; section markers get extra room above; one explicit eyebrow exception.

**Tier 1, Baseline (1em ≈ 16px below every block element)**

Every block-level token has `margin-bottom: 1em` and `margin-top: 0`. The next element sits 16px below, period. Listed exhaustively so future-me knows the rule covers everything:

| Token | margin |
|---|---|
| `.type-hero`, `.type-hero-md` | `0 0 0.5em` |
| `.type-hero-deck` | `0` (relies on hero's bottom margin) |
| `.type-h1` | `0 0 1em` |
| `.type-body` | `0 0 1em` |
| `.type-blockquote` | `0 0 1em` |
| `.type-list-ol`, `.type-list-ul` | `0 0 1em` |
| `.type-dl` | `0 0 1em` |
| `.type-figure` | `0 0 1em` |
| `.type-table` | `0 0 1em` |
| `.type-code-block` | `0 0 1em` |

**Tier 2, Section break (2.5em ≈ 40px above all markers, 1em below)**

A single shared `margin-top: 2.5em` for every element that visually marks a section break, sub-section, or closing block. Below the marker, baseline 1em, same as everything else. Hierarchy comes from heading size and weight, not graduated spacing.

| Token | margin |
|---|---|
| `.type-h2` | `2.5em 0 1em` |
| `.type-h3` | `2.5em 0 1em` |
| `.type-h4` (mid-article) | `2.5em 0 1em` |
| `.type-pullquote` | `2.5em 0 1em` |
| `hr.type-divider` | `2.5em 0 1em` |
| `.type-footnote` | `2.5em` + `padding-top` + `border-top` (editorial scope) |

CSS adjacent vertical margins collapse to the larger value (per CSS spec), so a heading with `margin-top: 2.5em` follows a paragraph with `margin-bottom: 1em` at the heading's 2.5em, a clean section break without double-counting margins.

**Tier 3, Eyebrow exception (≈ 8px, editorial scope only)**

`.type-h4:first-child` (used as a label for `.type-h1`) collapses its margin-top to zero and the H1 gets `margin-top: 8px`. The eyebrow is a caption for the title, not a section marker. This is the **only** explicit exception in the system.

**Internal (intra-block) spacing, not part of the rhythm**

These values sit *inside* a block, not *between* blocks, so they don't follow the 3-tier system:

| Element | Internal spacing | Why |
|---|---|---|
| `blockquote padding` | `0.25em 0 0.25em 1.25em` | Vertical breathing inside the quote, horizontal indent past the brand-colored border |
| `blockquote cite margin-top` | `0.6em` | Attribution gap below the quote text |
| `pullquote padding` | `1em 0` | Vertical breathing inside the bordered block |
| `list padding-left` | `1.5em` | Bullet/number gutter |
| `dl dt margin-top` | `1em` (zero on `:first-child`) | Gap between definition pairs |
| `dl dd margin` | `0` | Definition hugs its term |
| `figure figcaption margin-top` | `0.5em` | Caption sits tight under the image |
| `code-block padding` | `1em 1.25em` | Code breathing inside the dark block |
| `table cells padding` | `0.5em 0.75em` | Standard table cell breathing |
| `hero action margin-top` | `1.5rem` | Action row sits close to the deck but is visually separate from the statement. |

**⚠ Specificity warning for editorial-scope rules**

When a parent element scopes its children's flow spacing via adjacent-sibling selectors (e.g., `.editorial > * + *`), that selector's specificity is `(0,1,0)`: the **same** as a token rule like `.t-h1` or `.t-deck`. If the token rules declare `margin: 0` (as they do, to be reset-friendly), they will **override** the scope rule whenever they're declared later in the source. The fix is to raise the scope selector's specificity, for the editorial scope, use `article.editorial > * + *` (`(0,1,1)`) instead of `.editorial > * + *`. The same applies anywhere a "container scope" is applying flow margins to children whose token rules also touch margin.

This bug was present from v1.0 through the early v2.0 spacing iterations, all the "bumps" to the baseline rule were silently overridden by token resets. Verify any new flow-spacing rule renders the value you set by inspecting computed styles, not by trusting the CSS reads correctly.

**Tuning history**

The baseline went 16px (v1.x) → 24px → 32px → 40px → **16px (current)**. The first three bumps were silently nullified by the specificity bug above; the value the page was actually rendering was 0px between most elements. Once the bug was fixed (specificity raised to `article.editorial >`), the 40px baseline finally took effect, and read as too generous. Settled at 16px baseline + 40px section break as the simplest expressive system: 1em flow rhythm, 2.5em chapter mark, 0.5em eyebrow exception.

Captured as Principle 1 in `CONTEXT/ops/working-principles-claude.md` ("Consistency before local optimization") and Principle 2 ("Verify the rendered output, not the written CSS"), and now also as a CSS specificity warning here, so future-me doesn't regress.

**What was removed in v2.0**

- The `H1 + .t-deck` adjacent-sibling rule (deck now flows at baseline 24px).
- The `.t-deck + .t-body` adjacent-sibling rule (body flows at baseline).
- The heading-hugs-first-paragraph pattern across H2/H3/H4 (first paragraph flows at baseline).
- Asymmetric heading margins (huge top, tight bottom).

If a specific page needs different spacing, scope it locally, don't loosen the tokens.

---

## Markdown coverage

Every token maps to a standard markdown primitive. The system survives the round-trip from Obsidian → web → PDF → docx → plain text.

| Markdown | Renders as | Notes |
|---|---|---|
| (template-only, not markdown) | `.type-hero` / `.type-hero-md` | Hero tokens live in page templates, not markdown. Markdown bodies start at H1. |
| `# Title` | H1 | First H1 is the page title |
| `## Section` | H2 | |
| `### Subsection` | H3 | Italic by token rule |
| `#### Label` | H4 | Uppercase eyebrow/meta |
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

The Laz Güneşi; 18 blades, 20° apart, rotational sun. Every brand carries it, in brand color.
Source of truth: `laz-gunesi-amblem/svg/master.svg` (parametric rebuild from the original Illustrator file). Asset kit (SVG/PDF/PNG/CSS) lives in the same folder.

### The lockup

```
[ Symbol ]  brandname
```

- Symbol height = 1.4× wordmark cap height (≈ `Math.round(size * 1.4 * 0.7)` in pixels)
- Symbol-to-wordmark gap = 0.4× wordmark size
- Wordmark in `--display` (Inter Tight), `font-weight: 300` (Light), `letter-spacing: -0.005em`
- Variable `wght` axis 100–900. Light (300) is the working weight; the tighter proportions of Inter Tight (vs. Inter) lock the wordmark cleanly without negative tracking acrobatics.
- **Always lowercase.** `text-transform: lowercase` is enforced on `.lockup__name` so the wordmark renders lowercase regardless of how the brandname prop is passed. The prop can stay Title Case for SEO/aria; CSS does the visual normalization.
- Wordmark color = `--brand` (matches the symbol, the lockup reads as one mark, not two)
- **No subtitle.** The publisher mark is one word and one symbol. Sublabels and taglines belong elsewhere (page metadata, page subtitle, footer copy), not on the lockup.
- **No hover underline, ever.** The lockup is identity, not a normal text link. Hover must be visually quiet. If the lockup is clickable, keyboard focus must still be visible through an accessible focus outline or equivalent site-level focus treatment.
- **Optical vertical centering.** The symbol receives `transform: translateY(0.08em)` so its geometric center aligns with the wordmark's *optical* center, not the line-box geometric center. Lowercase text concentrates its visual mass between baseline and x-height; the upper portion of the line-box is mostly empty (only ascenders and the ğ breve reach there). Without the 0.08em shift, the symbol reads as floating high above all-lowercase wordmarks. Tested across all four brand wordmarks including the breve-heavy `ağustos` and ascender-light `pataraz`: single value works for both.

The `mono` expression substitutes `--ink` for `--brand` in single-color contexts (print, stamps, fax-quality).

### Per-brand wordmarks

Each brand has a fixed lowercase display name, mapped in `BaseLayout.astro`:

| Brand class | Wordmark | Color |
|---|---|---|
| `agustos` | `ağustos` | `--brand-agustos` (#cf142a) |
| `pataraz` | `pataraz` | `--brand-pataraz` (#1a24cc) |
| `pld` | `pld türkiye` | `--brand-pld` (#1a1a1a) |
| `photo` | `photometric` | `--brand-photometric` (#1f6b4a) |

**Why one-word wordmarks (where possible).** Each visible mark is a single noun: `ağustos`, `pataraz`, `photometric`. The exception is `pld türkiye` where the country qualifier is integral to the publication's identity. Drop "teknoloji," "luminaires," "batch", those describe what the brand does, not what it's called.

The page `<title>` is independent and stays Title Case (e.g. "Ağustos Teknoloji, lighting agency and distribution") for SEO and browser-tab readability. Title and wordmark are deliberately separate concerns.

### Three expressions

1. **Positive.** Symbol + wordmark in brand color on cream/white substrate. Primary use, 90% of contexts.
2. **Negative.** Symbol in cream/white on brand-color tile. For favicons, monograms, brand-color tiles.
3. **Mono.** Symbol + wordmark in ink on cream, or cream on ink. Single-color print, stamps, fax-quality.

No fourth expression exists.

### Logotype: Inter Tight Light (v2.0)

The wordmark uses **Inter Tight** (Rasmus Andersson. SIL OFL 1.1). Tighter, more compressed sibling of Inter, designed by the same hand and sharing the same skeleton. Variable `wght` axis 100–900 with italics. Used at **Light (300)** for the lockup.

Inter Tight is the wordmark face. It is also the system display face, the same family powers heroes, headings, eyebrows, UI labels, and table headers. This consolidation is intentional: in v2.0 the wordmark and the surrounding chrome are drawn from the same family, so the lockup integrates with its context rather than asserting itself as a separate face.

Why Inter Tight: after seven prior iterations (Fraunces semi-bold, Fraunces slim+WONK, Space Grotesk Light, Manrope ExtraLight, IBM Plex Sans Light, Tenor Sans Regular, Plus Jakarta Sans Light), a final round comparison evaluated Plus Jakarta 300/200, Hanken Grotesk 300, Geist 300, and Inter Tight 300 alongside a system-pairing decision (retire Newsreader for Inter as body). Inter Tight won on three axes: best-in-class Turkish `ğ` rendering, paired-skeleton harmony with Inter for body, and a "tight" axis that earns the *slick* descriptor without going couture-thin. The system-level question, retire Newsreader, was decided in favor of consolidation: one paired family, simpler to maintain, more rigorous register from logo to caption.

The Turkish `ğ` in Inter Tight is humanist; the breve integrates with the letter body. Inter has gold-standard Latin Extended coverage. `ğ`, `İ`, `ı`, `ş`, `ç`, `ö`, `ü` all draw correctly without locale tricks.

Self-hosted via `@fontsource-variable/inter-tight` (logotype + display) and `@fontsource-variable/inter` (body). System-font fallback on both, so any context where web fonts don't load (email, embedded UI, slow networks) degrades cleanly to the user's native UI font.

CSS tokens:

```css
--display: 'Inter Tight Variable', 'Inter Tight', 'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
--body:    'Inter Variable', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji";
```

Full reasoning for the v2.0 decision in MEMORY.md turning points 19–28.

### Adding a new brand

1. Pick a lowercase wordmark (1–3 words; should look balanced next to the symbol).
2. Pick a color (refined to sit with cream substrate, designed, not raw). Add to `tokens.css` as `--brand-{slug}` and a `.brand-{slug}` selector.
3. Add the wordmark to the `BRAND_WORDMARKS` map in `BaseLayout.astro`.
4. Pass `brand="{slug}"` to `BaseLayout`. Lockup inherits color, font, weight, axes, and the lowercase rule automatically.

Total time: ~10 minutes per brand. No new design work.

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

**Why this matters:** without `lang="tr"`, CSS `text-transform: uppercase` converts lowercase `i` to dotless `I` instead of dotted `İ`. This silently produces wrong Turkish in any uppercase styling, eyebrows, brand names, table headers, H4 labels. With the rule applied, Turkish capitalization renders correctly everywhere.

---

## Accessibility requirements

Accessibility is part of the design system, not an implementation afterthought. The system's restraint only works if interactive states remain legible and keyboard-operable.

### Focus and keyboard

- Every interactive element must expose a visible `:focus-visible` state.
- Brand color may be used for focus rings because it is a semantic interaction signal.
- Skip links are required on full web layouts with persistent navigation.
- Minimum practical target size for button-like controls is 44px on the shorter axis. Editorial text links may be smaller if they sit in prose, but they must have enough line-height and spacing to be tapped comfortably.

### Contrast

- Body text uses `--ink` on `--paper` or `--paper-white`.
- Secondary text uses `--ink-soft`; use `--ink-faint` only for captions, footnotes, dates, and low-priority proof lines.
- Brand-colored links and focus rings must be checked on cream, white, and dark substrates.
- Negative expressions (cream/white on brand-color tiles) must be checked per brand, especially Pataraz blue and Photometric green.

### Motion and state

- Transitions should be short and functional (roughly 120-180ms).
- Do not encode meaning in color alone. Links use both weight and underline; active navigation uses position, text, and state, not just color.
- Dark theme is allowed as an opt-in implementation layer, but it must preserve the same token relationships: paper, ink, rule, brand, not a separate visual system.

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

The system supports two canonical paper colors plus one opt-in dark UI layer. Same tokens, same rules, different `--paper` value.

### Cream `#fefcf2` (primary, branded contexts)

Marketing pages, editorial articles, proposals, beautifully-typeset cover documents. The paper carries warmth and editorial register.

### White `#ffffff` (universal, working contexts)

Email, docx defaults, generic web, printer paper, dashboards, product UI. The paper disappears; the typography carries the brand.

A single CSS variable swap flips the system. No other token changes.

### Dark `#16140f` (opt-in UI context)

Dark theme is an implementation layer for screens, not a third brand substrate. It inverts paper, ink, and rule while keeping brand colors stable. The dark paper keeps a warm undertone so cream-trained brand colors still integrate. Use dark theme for user preference and product UI comfort, not as a default editorial expression.

---

## Brand color refinement protocol

When adding a brand, the brand color must be evaluated against the cream substrate. Raw web colors (pure hues like `#0000FF`, `#FF0000`, `#00FF00`) fight the paper. Designed colors integrate.

**Refinement process:**

1. Place the raw color next to `#fefcf2` in a test render.
2. If the color feels aggressive, slightly off, or "fights" the paper, refine it.
3. Typical refinements: shift 5–10% darker, reduce saturation 5–15%, push slightly toward the paper's warm hue.

**Example:** Pataraz original `#0000FF` → refined `#1a24cc`. Same blue identity, sits with paper instead of fighting it.

---

## What was cut, and why

Future-you may wonder why these don't exist. They were considered and rejected.

| Cut | Reason |
|---|---|
| ~~`.type-display-xl` (64px)~~; *brought back in v2.0 as `.type-hero` and `.type-hero-md`* | v1.x argued layout creates presence above what type alone provides. v2.0 reversed that for landing/brand pages where the hero *is* the layout. Hero exists at two scales (big and medium); H1 still does page-title duty inside articles. |
| `.type-display` (48px) | Sat between Display-XL and H1 with no clear job. H1 absorbs chapter and cover. |
| `.type-eyebrow` (small uppercase brand-color) | H4 absorbs eyebrow. Brand color appears as an eyebrow accent **only above hero tokens**; elsewhere, H4 stays ink-soft unless a local semantic role explicitly earns brand color. |
| `.type-deck` (italic sub-headline) | Solved by `.type-hero-deck` utility for hero contexts; otherwise use normal body or `*italic*` only when the copy is genuinely editorial emphasis. |
| `.type-byline` (italic 14px) | Editorial italic body does the job. Inline within prose if helpful. |
| `.type-sc` (small caps for brand names) | Editorial flourish, not a system primitive. Brand names render fine in regular case. |
| `.type-small` (generic secondary) | If it's secondary, it's a footnote. No middle tier. |
| `.type-meta` (UI labels) | H4 absorbs meta. One token, one job, across all label-like contexts. |
| `.type-caption` (figure caption) | Lives inside `.type-figure` as `figcaption`. Not addressable; inherent. |
| `strong em` (bold italic) | Rarely the right choice. If something needs strongest emphasis, bold or italic alone is sufficient. |
| Universal yellow highlight (`<mark>`) | Non-portable across markdown environments. The system uses link treatment for emphasized terms instead. |
| Strong-em as separate token | Bold or italic alone covers all needed emphasis levels. |

---

## Implementation notes

### Web utilities

The canonical web implementation lives in `astro/src/styles/tokens.css`. Typography tokens are the portable core. Layout and interaction helpers are implementation utilities and may evolve without increasing the typography token count.

Current non-token utilities:

| Utility | Role |
|---|---|
| `.paper-white` | Switches `--paper` and `--rule` to white-context values. |
| `html[data-theme="dark"]` | Optional dark theme; inverts paper/ink/rule while keeping brand colors stable. |
| `.container` | Default readable page measure and vertical page padding. |
| `.hero-links`, `.hero-link*` | Editorial homepage hero action row. |
| `.hero-action*` | Boxed lower-section CTA links where tap target and scannability matter. |
| `.skip-link` | Keyboard accessibility utility for persistent navigation layouts. |

Specified but not yet fully mirrored in the local CSS: `.hero-trust` and `.hero-visual`. Add them to both mirrored token files before using those classes in production.

### Pandoc template

For docx and PDF generation from markdown, the Pandoc template applies the same CSS variables and class names as the web rendering. Same source, two surfaces.

A reference template should:

- Set `lang: tr` in frontmatter for Turkish documents
- Apply Inter Tight / Inter / JetBrains Mono via system font installations
- Map markdown elements to the 24 tokens and named utilities via class names
- Preserve `tnum` for tabular numerals in tables

(Template file: TBD; to be developed during implementation phase.)

### Font loading

Self-host the three families through `@fontsource-variable/inter-tight`, `@fontsource-variable/inter`, and `@fontsource/jetbrains-mono` in web projects. Fallback stacks ensure no rendering failure even if web fonts don't load. Email contexts will permanently use native fallbacks from the stack; this is acceptable.

### Browser support

The system uses CSS custom properties, `font-variation-settings`, `color-mix()`, `font-feature-settings`. All supported in browsers from 2022 forward. No IE support, no Edge Legacy support, both are end-of-life.

### QA checklist

Run this checklist before calling a system change complete:

1. Render the typography showcase and confirm all 24 tokens appear.
2. Inspect computed margins for H2/H3/H4, body, lists, tables, code blocks, and dividers; verify the 1em baseline and 2.5em section break actually render.
3. Test Turkish uppercase with `lang="tr"` on H4/table-header-style text: `başlık`, `i`, and `ışık` must uppercase correctly.
4. Check cream, white, and dark substrates.
5. Check all brand colors on cream and dark substrates, including link underline, focus ring, list marker, and negative lockup.
6. Test keyboard navigation: skip link, sidebar/header nav, language controls, theme toggle, hero links, and boxed actions.
7. Verify mobile and desktop widths; text must not overlap, clip, or force horizontal scrolling except inside code blocks and wide tables.
8. If tokens changed, mirror `astro/src/styles/tokens.css` and `PROJECTS/WEBSITE-agustos/src/styles/tokens.css` in the same session.
9. If document export changed, render docx/PDF samples and inspect typography, tables, footnotes, and Turkish locale handling.

---

## Files in this system

When fully implemented, the system consists of:

- `DESIGN.md` (this file), canonical specification
- `MEMORY.md`: decision history and reasoning
- `astro/src/styles/tokens.css`: **canonical** CSS variables and base rules (this folder)
- `agustos-template.docx`: Pandoc reference template
- `agustos-template.tex`: LaTeX template for PDF (optional)
- `examples/`: rendered samples in HTML, docx, PDF
- `fonts/`: self-hosted font files

### Mirrored implementation

The canonical `tokens.css` is **mirrored** to the production website at `PROJECTS/WEBSITE-agustos/src/styles/tokens.css`. The two files must stay byte-identical except for their headers.

> **⚠ Sync rule.** When editing tokens here, propagate the change to `PROJECTS/WEBSITE-agustos/src/styles/tokens.css` in the same session. When editing tokens there, mirror back here. Both file headers state this rule. The full sync protocol lives in `PROJECTS/WEBSITE-agustos/CLAUDE.md`. Drift between the two files is a defect, treat it as such.

Why mirror instead of symlink or `@import`: a symlink breaks across git/Cloudflare deploy boundaries and on Windows-native checkouts; an `@import` couples the website's deploy to the spec project's file layout and fails on static hosts. The mirror is durable across deploy contexts; the cost is the discipline of two-place edits, captured by the sync rule.

(Files marked TBD will be developed during implementation phase. This document is the specification; actual files come next.)

---

## Versioning

This is **v2.1.1**. Subsequent changes follow semantic versioning:

- **Major.** Breaking changes to token names, structural removal, philosophy shifts
- **Minor.** New tokens, new brand additions, additive-only changes
- **Patch.** Color refinements, weight tuning, fallback adjustments

Each version updates this document and notes the change in MEMORY.md.

---

## Authority

This system was designed by Emre Güneş in dialogue with Claude over the course of one extended design conversation in May 2026. It reflects Emre's editorial sensibility, business priorities, and engineering principles. Decisions documented in MEMORY.md.

The system is the product of his judgment, not Claude's. Future changes should be made by him, with reasoning documented.
