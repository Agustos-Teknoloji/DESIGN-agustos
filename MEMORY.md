# Design System Memory

**Companion to DESIGN.md** · How the system arrived at its current form
**Conversation date:** May 8, 2026
**Purpose:** Prevent re-litigation of decisions already made. When future-Emre wonders "why did we decide X," the answer lives here.

---

## How to read this document

This is a chronological record of turning points, moments where the system's direction changed, an option was rejected, or a principle was named. It's not a diary of every decision; only the ones worth remembering.

For each turning point: what was on the table, what was chosen, and *why*. The "why" matters more than the "what", the why is what prevents future-you from rebuilding something already torn down.

---

## Conventions (where things live)

A few structural rules that outlive any single decision. They're documented here once so we don't relitigate them.

### `artifacts/`: exploratory & frozen-in-time

Everything that informed a decision but isn't a production deliverable lives in `artifacts/`. That includes: typeface comparisons, logotype specimens, color exploration sheets, mockups, and any HTML page built to evaluate options. These are dated or versioned, never edited after the decision they informed has been made, they're the "what we considered" half of the historical record (DESIGN.md captures "what we chose," MEMORY.md captures "why").

Naming convention: `agustos-{topic}-{variant}.html` (and matching `.pdf` archives where the visual fidelity matters long-term. Google Fonts URLs and CDN dependencies can rot, so PDF snapshots preserve the visual evidence).

### `laz-gunesi-amblem/`: production asset kit

The shipped, canonical brand assets. SVG masters, PDFs, PNGs at standard sizes, the live `laz-sun.css` that consumers can `<link>` to. Everything in here is referenced from production code (the Astro site, future docs, partner sites). Files here are versioned with the system and updated as the symbol or asset kit evolves.

### Astro project: the implementation

`astro/src/` is the live reference implementation. Components, layouts, tokens, content. Editing here changes what users see on the running site.

### The split, in one sentence

> If a file informs a decision, it goes in `artifacts/`. If a file *is* a brand asset, it goes in `laz-gunesi-amblem/`. If a file renders a page, it goes in `astro/src/`.

---

## Turning point 1: Starting reference: the Hamming page

The conversation began with a screenshot of a Richard Hamming book page (Cormorant-style serif, single-family typography, yellow highlights, generous whitespace, justified body text with hyphenation). This became the anchor for "editorial restraint" as a design direction.

**Why it mattered:** The reference established the *register* for the entire system before any specific decisions were made. Editorial-school typography (NYT, Stripe Press, Tufte) rather than SaaS-school (Inter + cards + UI chrome). Every subsequent decision was filtered through "does this fit the editorial register?"

---

## Turning point 2: Two hats acknowledged

Initial framing: Emre operates two distinct businesses. Ağustos Teknoloji (agency, Turkish, specifiers) and PIM-STEPS consultancy (English, manufacturers). The decision was made to build a **unified system, two voices**, one set of primitives, two expressions, sibling-brand recognition.

Later expanded to four brands: Ağustos, Pataraz, PLD Türkiye, Photometric Batch.

**Why it mattered:** This locked in the "multi-brand from a shared system" architecture. If we'd built for just Ağustos, we'd have to redo it for Pataraz. Building for the portfolio from the start forced systemic thinking.

---

## Turning point 3: Typography exploration over commitment

When asked to pick a typeface, Emre said *"I'm not sure between sans-serif or serif. But I want it to be readable in every device. Yet distinctive. I want to explore options."*

This was the right instinct. We rendered four candidates (Inter Tight + Source Serif 4, Instrument Serif + Geist, Fraunces alone, Manrope + Newsreader) against actual Turkish + English content before deciding.

**Why it mattered:** Picking from a list is a different decision than picking from rendered evidence. Every typography choice that followed was anchored in actual visual judgment, not abstract description.

---

## Turning point 4: Fraunces selected, then later rejected

Initial choice: Fraunces (single variable family). Reasoning: most disciplined option, most distinctive, single-family Hamming approach.

Later rejected after the "boldish body" feedback revealed Fraunces' character was wrong for body reading at length.

**Why it mattered:** Demonstrates the value of testing a typeface in *every* context (display, body, italic, bold, links) before committing. Fraunces' display sizes are excellent; its body is too assertive. We discovered this only by rendering full hierarchy in real content.

---

## Turning point 5: Color philosophy: brand color on link only

Two philosophies were considered:

- **Philosophy A:** Brand color is the link. Yellow is the universal highlight. Brands feel like sections of a magazine.
- **Philosophy B:** Brand color is link AND highlight. Each brand has its own atmosphere. Brands feel like separate publications.

Emre chose A, with the further refinement: *"I want this system to work anywhere anytime."*

This led to the deeper realization: highlight as a concept is non-portable in standard markdown. **Highlight was eliminated from the system entirely.** Only bold, italic, and link survived as inline emphasis primitives.

**Why it mattered:** This was the moment the system became *sustainable*. Removing highlight from the vocabulary meant every emphasis decision now maps to standard markdown that survives the round-trip across Obsidian, GitHub, Pandoc, plain text. The most disciplined version of the system.

---

## Turning point 6: Substrate-agnostic principle

Emre asked: *"I want to make sure system works even with white background."*

This led to defining cream `#fefcf2` as the *primary* substrate but ensuring every token works against white `#ffffff` too. Cream became a flavor, not a requirement.

**Why it mattered:** Email rendering, docx defaults, generic web, and printer paper all use white. A system that needs cream is fragile; a system that works on white *and* cream is portable. This decision protected the system from email rendering failures and dash boards in white-default environments.

---

## Turning point 7: Logo system: same symbol, forever

Considered three options:

- Same symbol for all brands (most disciplined)
- Each brand has its own symbol (more conventional)
- Hybrid with future-brand escape hatch (compromise)

Emre chose: **same symbol forever, no escape hatch.** *"The discipline matters more than the symbolism."*

The Laz Güneşi (Laz sun) becomes the publisher's mark across all brands. New brands plug in by choosing only a name and a color.

**Why it mattered:** This was a contrarian move, most brand consultants would tell you per-brand symbols are correct. Emre chose systemic discipline over per-brand expressiveness. This prevents the "logo redesign" problem: every new brand requires zero design work, just two decisions.

---

## Turning point 8: Turkish locale handling

Discovered during the logo work: CSS `text-transform: uppercase` in Turkish content silently produces wrong capitalization without `lang="tr"` declared. The lowercase `i` becomes `I` (dotless) instead of `İ` (dotted).

This was elevated to a system rule: every Turkish content block must declare `lang="tr"`, and CSS must enable `font-feature-settings: "locl"` globally.

**Why it mattered:** Without this rule, Turkish capitalization is silently wrong everywhere uppercase styling is applied, eyebrows, brand names, table headers, H4 labels. Catching it during system design rather than in production saved real reputational damage. This is exactly the kind of detail that distinguishes a designed system from a copy-pasted one.

---

## Turning point 9: Token simplification rounds

The system started at ~30 tokens (full editorial vocabulary including display-xl, display, eyebrow, deck, byline, small, meta, small-caps).

Emre pushed back: *"This feels too much. Anything to be simplified?"*

Multiple cut rounds followed:

- **Cut Display-XL and Display**. H1 is the biggest thing on the page
- **Cut Eyebrow, Deck, Byline.** Absorbed into H4 and italic body
- **Cut Small, Meta, Caption.** Absorbed into existing tokens or removed as unnecessary tier
- **Cut Small Caps.** Editorial flourish, not a primitive
- **Cut Strong-em.** Bold or italic alone covers needed emphasis levels

Final count: **22 tokens.** Down from ~30.

**Why it mattered:** Smaller systems are more sustainable. Every token is a decision the writer must make; fewer tokens = fewer decisions = faster writing = easier handoff to anyone else. Emre's instinct ("everything seems unnecessary") was correct, the original system had decoration disguised as structure.

---

## Turning point 10: Heading distinctness fix

Emre flagged: *"Are H2 and H3 distinctive enough?"*

After audit, two changes:

- **H1 increased from 36px to 44px.** Page title now genuinely announces
- **H3 made italic.** Categorically different from H2, not just different size

The italic H3 is a Tufte move. It gives subsections a softer, more editorial register that's structurally distinct from H2's role as section break.

**Why it mattered:** Hierarchy that requires squinting to distinguish levels is broken hierarchy. The fix made the system more legible without adding tokens, same vocabulary, better rhythm.

---

## Turning point 11: Standard markdown coverage audit

Emre asked: *"A standard markdown token list, is it all covered? Anything missing?"*

Audit revealed three gaps:

- **Subscript** (CO₂, H₂O), added
- **Superscript** (m², m³), added
- **Strikethrough** (revision marks), added

These are all standard in Pandoc / Obsidian / GFM. Important for technical lighting writing where formulas and units appear constantly.

**Why it mattered:** Going from "feels complete" to "actually covers all standard markdown" closes the door on future "we need to add this" requests. The system isn't almost-complete; it's complete.

---

## Turning point 12: Body weight problem (Fraunces specifically)

Emre flagged: *"Body feels a bit boldish, I was thinking of thinner approach where I can fell the bold ones. Now everything seems boldish."*

This was a Fraunces character problem, its weight 400 sits visually heavier than book conventions expect.

Tried four solutions:

- **Option A:** Body 380 / Bold 600 (lighter body)
- **Option B:** Body 400 / Bold 700 (heavier bold)
- **Option C:** Body 380 / Bold 650 (both)
- **Option D:** SOFT axis tweak

Emre chose Option A but flagged uncertainty.

**Why it mattered:** This was the diagnostic signal that revealed Fraunces wasn't quite right for body. The "Option A feels OK but not 100% sure" feedback led directly to questioning the typeface itself, not just its weight tuning.

---

## Turning point 13: Typeface family pivot to Newsreader

After the weight tuning didn't fully resolve the body comfort issue, we tested four typefaces side-by-side: Fraunces (current), Source Serif 4, Newsreader, EB Garamond. Same locked-down system, same content.

Emre's response: *"I feel close to Newsreader."*

Newsreader was designed by Production Type *specifically* for screen body reading at length. Its optical-size axis means letterforms genuinely change shape between body (16px) and display (44px) sizes. This was the typeface whose mission matched what Emre was trying to do.

**Why it mattered:** The "boldish body" problem was never about weight tuning, it was about typeface character. The right answer was changing the typeface, not the weights. This is the kind of root-cause shift that separates a system that works from one that doesn't.

---

## Turning point 14: Sans-only consideration and resolution

After fatigue with serif options, Emre said: *"Should we try sans-serif fonts as well? I'm leaning to sans-serif only."*

We tested five sans candidates (Inter, IBM Plex Sans, Geist, Manrope, Inter Tight) at full system fidelity.

Critical realization during evaluation: **Sans-only optimizes for Photometric Batch (1 brand) at the cost of Pataraz, PLD Türkiye, and Ağustos editorial (3 brands).** The premium positioning of Pataraz specifically relies on editorial register to feel premium without spending.

Emre's question shifted: *"What about fall back strategy?"* and then *"Something that can stay relevant over the time in 10 years or so?"*

The longevity question reframed the entire decision. **Newsreader, in the book-serif tradition (250 years old), ages better than any sans candidate.** Sans typefaces ride trends; book serifs survive them.

**Why it mattered:** Without the longevity question, we might have committed to a sans for short-term feel reasons. Asking "10 years from now" exposed which decisions were fashion and which were infrastructure. Newsreader is infrastructure.

---

## Turning point 15: Source Sans 3 chosen as Newsreader companion

With Newsreader locked as the editorial face, the question became which sans pairs with it for product UI.

Considered: Inter (workmanlike), IBM Plex Sans (humanist warmth, good companion), Geist (too "of-2024"), Manrope (too geometric), Source Sans 3 (matched-sibling philosophy).

**Source Sans 3 won** because it shares Newsreader's design philosophy (humanist, screen-optimized, designed-as-infrastructure). It's the closest thing to an "official sibling" Newsreader has.

**Why it mattered:** Pairing decisions are different from standalone decisions. The right companion isn't "the best sans", it's "the sans that makes the serif stronger." Source Sans 3 disappears next to Newsreader the way good infrastructure disappears.

---

## Turning point 16: Character coverage verification

Before locking the system, Emre asked: *"Currency symbols etc, any compatibility issues that we should think of? I really want this to be done once and move further."*

Built explicit verification specimen testing:

- Currencies (₺ € $ £ ¥ ¢)
- Technical (° ² ³ ₂ × − ± µ → ← ≈ ≠ ≤ ≥)
- Editorial (" " ' ' – — … § ¶ © ® ™ † ‡ • ·)
- Turkish alphabet (full)
- Numerals (proportional and tabular)

All three faces (Newsreader, Source Sans 3, JetBrains Mono) ship the **Google Fonts Latin Plus** glyph set. All characters verified present and correctly rendered.

**Why it mattered:** This is the kind of detail that's invisible until it breaks in production. Verifying character coverage *before* locking the system means future-Emre never has to debug a missing ₺ in a Pataraz pricing PDF or an incorrect Turkish capital İ in a brand name.

---

## Turning point 17: Final lock

System locked at version 1.0:

- **Type:** Newsreader (serif) + Source Sans 3 (sans) + JetBrains Mono
- **22 tokens** mapped cleanly to standard markdown
- **Color:** Brand on links only, cream + white substrates
- **Logo:** One symbol forever, name + color flex
- **Locale:** `lang="tr"` mandatory for Turkish content
- **Coverage:** Verified across currencies, technical, editorial, Turkish

**Why it mattered:** This was the moment when "design exploration" became "design specification." Every decision was tested against real content, real languages, real character sets, real surfaces. The system is the product of judgment, not enthusiasm.

---

## Turning point 18: Implementation phase: spec to running site

The system left specification mode in May 2026. An Astro reference site was built implementing every token, brand class, lockup, and substrate behavior. Around the same time, the original Adobe Illustrator file for the Laz Güneşi (`laz-gunesi-amblem.ai`, 2019) surfaced and was parametrically rebuilt as a clean 18-blade SVG (centered, deduplicated, ~250× smaller than the source PDF for the same visual).

The `LazGunesi.astro` placeholder (12 simple rays + a disc, labeled "Swap with the final mark when ready; the API stays stable") was replaced with the real geometry. The component API stayed identical: `size`, `title`, `class`, `currentColor` inheritance, so `BrandLockup` and any other call sites kept working untouched.

A full asset kit (SVG masters in red/black/white/lockups, PDFs, PNGs at 256/512/1024/2048/4096, plus a self-contained `laz-sun.css` with mask + background variants) was packaged at `laz-gunesi-amblem/` next to DESIGN.md and MEMORY.md.

**Why it mattered:** The placeholder-to-real swap proved the system's portability claim, the symbol changed, every consumer kept working, no design decisions were re-opened. This is what "stable API" buys you, and it's the first real test the system passed.

---

## Turning point 19: Logotype decision: Fraunces, scoped to wordmark only

In v1.0 the wordmark used Newsreader Display at opsz 60. After implementation, Emre flagged that the lockup felt quiet. *"I want to find a proper Font for the Logo type. So that we can use it as brand asset from now on."*, plus three constraints: brand color, no underline on hover, no subtitle.

A specimen sheet was rendered at three sizes (20px / 44px / 120px) for five candidates: Fraunces, Instrument Serif, Bricolage Grotesque, DM Serif Display, and the Newsreader baseline. Emre picked Fraunces.

**This is not a reversal of TP12 / TP13.** Those rejected Fraunces as **body type** at small sizes, the "boldish body" character problem at 16px reading length. The logotype use is fundamentally different: ~20–200px, one word, set ~once per page. At display sizes Fraunces' character is a feature, not a defect. TP4 had already noted: "Fraunces' display sizes are excellent."

So the system now uses **two serifs**: Newsreader for body and headings (the reading layer), Fraunces for the wordmark only (the identity layer). They are siblings, both modern revivals of mid-20th-century display traditions, both have optical sizing, both were designed for screen. The pairing is intentional, and bounded: Fraunces appears nowhere except inside `BrandLockup`.

The decision was load-bearing on three things:

1. **The `ğ` reads at every size.** Fraunces' breve has presence at 18px and personality at 200px. None of the other candidates nailed this, and `ğ` is the only character that matters in "Ağustos."
2. **opsz handles the lockup math automatically.** The component renders the wordmark at anywhere from 18px (header) to 200px (hero); Fraunces' opsz axis tunes terminals and contrast continuously across that range. No manual size variants.
3. **Family kinship over family identity.** Fraunces ≠ Newsreader, but they belong to the same design tradition. The wordmark feels related to the body, not foreign to it.

A new `--logotype` token was added to `tokens.css` (separate stack from `--serif`), `BrandLockup` was updated to use it, the secondary-line prop was removed (no subtitle on the publisher mark), wordmark color shifted from `--ink` to `--brand`, and the hover underline was explicitly suppressed.

**Why it mattered:** Confirmed that prior rejections aren't permanent bans, they're scoped rejections. Fraunces was wrong for one job and right for another. The system is durable enough to re-examine a typeface with new evidence and reach the opposite conclusion without contradicting itself. The discipline isn't "never reconsider", it's "reconsider only with new information and a clear scope."

---

## Turning point 20: Logotype re-tune: slim, lowercase, four brands, WONK on

After v1.1 shipped with Fraunces at semi-bold (weight 600, opsz 96, WONK 0), Emre flagged that the existing physical logo (rounded chunky sans, "agustos teknoloji" with no `ğ`) wasn't what he wanted, and showed me the source, making it clear the brief was: **slim, distinctive, eye-catching, lowercase, ağustos / pataraz / pld türkiye / photometric batch**.

A second specimen was rendered with five slim candidates: Fraunces Light + WONK (system retune), Cormorant Garamond Light, Instrument Serif Italic, Bricolage Grotesque Light, Bodoni Moda Light. Each shown with all four brand wordmarks, their own brand colors, at hero and small sizes.

Emre picked **Fraunces Light + WONK**, the system retune.

Three changes shipped:

1. **Variation settings flipped from semi-bold to slim-with-character.** `font-weight: 600 → 300`, `opsz: 96 → 144`, `WONK: 0 → 1`, `letter-spacing: -0.020em → -0.030em`. The WONK axis swaps in alternate letterforms (single-story g, characterful ear on a, distinctive y descender). This is what makes "slim" not feel "thin and forgettable."

2. **`text-transform: lowercase` enforced in CSS.** The `brandname` prop can be passed in any case (Title Case is fine for SEO/aria/screen readers); the visible wordmark always renders lowercase. Visual rule lives in CSS, not in data.

3. **Per-brand wordmark map in `BaseLayout.astro`.** `agustos → ağustos`, `pataraz → pataraz`, `pld → pld türkiye`, `photo → photometric batch`. The `<title>` tag stays Title Case (separate concern). Adding a new brand = adding one map entry.

**Why it mattered:** Confirmed two principles already named:

- **Variable axes are the unit of taste-tuning, not font swaps** (TP19 introduced Fraunces; TP20 just dialed it differently). The font hasn't changed in two months; the look has changed twice. This is what variable fonts buy you, and what mid-2010s static-font systems couldn't.
- **Pick the unit of normalization carefully.** Lowercase enforcement could have been a content rule ("write all brandnames lowercase"), a build rule (transform at build time), or a CSS rule. CSS won because it preserves the structured data (Title Case in the prop, which screen readers and search engines can use) while controlling presentation. The right place to normalize visual style is the visual layer.

Side benefit: the previous logo's qualifier ("teknoloji") is now gone, the wordmark is the brand, not the brand-and-its-category. Cleaner, more confident, more like a publisher's mark.

---

## Turning point 21: Logotype pivot: Fraunces → Space Grotesk

After v1.2 shipped with slim Fraunces + WONK, Emre showed the existing physical logo and said he liked **Bricolage Grotesque Light** and **Bodoni Moda Light** from the v2 specimen, and asked for "more options in this direction." A v3 specimen rendered five new candidates: Space Grotesk Light, Manrope ExtraLight, Familjen Grotesk Light, Playfair Display Light, Italiana.

Emre picked **Space Grotesk Light**. The Fraunces installation was removed and replaced with `@fontsource-variable/space-grotesk`. The lockup variation settings simplified. Space Grotesk has a single `wght` axis, no opsz/SOFT/WONK to tune.

**The deeper lesson, what the Fraunces detour taught us.** Two versions of Fraunces shipped (semi-bold in v1.1, slim+WONK in v1.2) before the brand felt right. Looking back, even slim Fraunces with the WONK axis on read as **serif personality**, warm, editorial, a little academic. That fit Newsreader (the body type) but fought the brand's intended direction, which was magazine-modern, structural, design-forward.

The signal that something was off came when Emre showed the existing chunky-rounded logo and described what he didn't like: too warm, too friendly, too "established corporate." Even though the existing logo was a sans, the *direction* he was rejecting was warmth and roundness, and slim Fraunces, despite being a different category, still carried warmth. The v3 candidates explicitly explored "structural confidence without warmth," and the answer landed on a grotesque sans.

**What this validates.**

- **Two specimens beat one.** v2 surfaced what Emre actually responded to (Bricolage + Bodoni) which differed from what he initially said yes to in v1 (Fraunces semi-bold). The picks people make on round one are often picks-by-elimination; the picks they make on round two are picks-by-affinity. We should default to multiple specimens for any high-signal aesthetic decision.
- **Listening for what's being rejected, not just what's being chosen.** "I'm not fond of the existing one" pointed at warmth/chunkiness. That same direction was hiding in slim Fraunces. The v3 brief came from reading that rejection precisely.
- **Fraunces wasn't wasted.** The two Fraunces rounds taught the system that "slim editorial serif" wasn't the answer, without that evidence, we'd have endlessly tweaked Fraunces axes thinking the next setting would land it. Negative results clear the search space.

**What the system gains structurally.** Space Grotesk simplifies the lockup: no opsz axis to tune per size, no WONK toggle to remember, just `font-weight: 300`. The whole `font-variation-settings` line is gone from `BrandLockup.astro`. Fewer knobs = fewer things to get wrong = a more durable spec.

---

## Turning point 22: Logotype lands on Manrope ExtraLight; wordmarks finalized

After v1.3 shipped Space Grotesk Light, Emre returned with two locked decisions:

1. **Font: Manrope ExtraLight** (weight 200), not Space Grotesk.
2. **Wordmark for `photo` brand: `photometric`**, dropping "batch."

Both came from the same place. *more refined, less distinctive*. Space Grotesk had character (double-story g, tall ascenders, design-forward energy); Manrope has geometry without flourish. The choice means: let the symbol be the distinctive element; the wordmark is the steady supporting voice. Same logic for shortening the wordmark, strip the qualifier, keep the noun.

**Final per-brand wordmarks:**

| Brand class | Wordmark | Notes |
|---|---|---|
| `agustos` | `ağustos` | Drop "teknoloji", describes work, not identity |
| `pataraz` | `pataraz` | Drop "luminaires", same reason |
| `pld` | `pld türkiye` | Keep "türkiye", country qualifier is integral to the publication |
| `photo` | `photometric` | Drop "batch", describes the product, not the brand |

Three of the four wordmarks are now single nouns. The principle: **a wordmark is a name, not a description.** "Apple" doesn't say "apple computers" in its mark. "Stripe" doesn't say "stripe payments." If a brand needs to communicate what it does, that's the job of the page (the H1, the description, the product copy), not the lockup.

**The four-font journey, end to end:**

| Version | Font | Weight | Why it shipped | What it taught |
|---|---|---|---|---|
| v1.1 | Fraunces | 600 (SemiBold) | First implementation; matched body type | Too quiet as a wordmark; no claim of ownership |
| v1.2 | Fraunces | 300 + WONK 1 | "I want a NEW fresh look" → axis-tune the existing font | Even slim Fraunces still read as serif personality, warm, editorial |
| v1.3 | Space Grotesk | 300 (Light) | "I like Bricolage and Bodoni Moda" → grotesque sans direction | Distinctive geometric energy, but more personality than the brand needed |
| v1.4 | Manrope | 200 (ExtraLight) | "Let's go with Manrope" | Refined product-design register; symbol leads, wordmark supports |

**What this validates.**

- **Specimen-driven decisions converge faster than discussion-driven ones.** Three rounds of specimens (v1, v2, v3) and four shipped versions. Each picked-by-elimination round narrowed the search space. By the time Manrope was picked, it was a confident "this" rather than a tentative "maybe this."
- **The right answer is often the third or fourth answer, not the first.** Initial picks tend to favor "interesting"; later picks tend to favor "right." Fraunces was interesting. Manrope is right.
- **Variable fonts let you A/B test taste in CSS, not in npm.** Two of the four versions were pure axis tunes, same font, different weight/axes. That's the cheapest possible iteration loop for typography decisions, and we should default to it before adding a font to the stack.
- **Wordmarks are nouns, not descriptions.** Strip qualifiers. If a wordmark needs explanation, the page does the explaining.

**Structural simplification.** Manrope, like Space Grotesk before it, has a single `wght` axis. The lockup `font-variation-settings` line is gone (already removed in v1.3). What's left: `font-family`, `font-weight: 200`, `letter-spacing: -0.030em`, `text-transform: lowercase`. Five properties. That's the durable spec.

---

## Turning point 23: Bold logotype finalization: Inter Tight 650

After the v2 consolidation onto Inter Tight + Inter, Emre questioned whether the logotype should stay light. The hunch was correct: Inter Tight 300 was elegant, but too quiet beside the dense Laz Güneşi mark at real header sizes.

A context board compared the previous/current Light lockups against bolder candidates: Inter Tight 650, Inter Tight 730, Hanken Grotesk 700, Plus Jakarta Sans 700, and Bricolage Grotesque 700. Each was tested in desktop header, mobile header, document, dark footer, and brand-family contexts.

Emre chose **Inter Tight 650 with neutral tracking**.

**Why it mattered:** This was not a font pivot, it was a weight finalization. The underlying v2 decision still holds: one paired family from logo to body. Weight 650 gives the wordmark enough presence at 16–20px without making it shout, and keeps the portfolio lockup calm across `ağustos`, `pataraz`, `pld türkiye`, and `photometric`. Inter Tight 730 was the upper edge; Bricolage 700 had more character but would have made the logo a separate personality again. The final choice is the conservative bold move: same system, better authority.

---

## Turning point 24: Brand-asset home, favicon kit, red reconciliation (June 2026)

A request for "a favicon for agustos.com" surfaced three latent problems: scattered favicon copies with no canonical source, no real favicon *kit* (only a lone SVG), and — most importantly — **two different brand reds in active use**. The symbol kit (`master.svg`, its README, geometry JSON, CSS) declared `#D11D2B`; the design system (`tokens/agustos.css`, DESIGN.md, every favicon) used `#cf142a`. Perceptually near-identical, but a source-of-truth conflict: an agent copying "brand red" had a 50/50 chance of being wrong.

Resolutions:

1. **One red: `#cf142a`.** The design-system token wins (DESIGN.md is the stated authority). All symbol SVGs, CSS, geometry JSON, and READMEs reconciled. The five transparent red PNGs were recolored losslessly (preserve alpha, swap RGB); the two two-tone variants rebuilt by compositing onto white/black. Print PDFs left at `#D11D2B` and flagged in ASSETS.md — no vector SVG→PDF rasterizer available locally, and the difference is invisible.
2. **Favicon = the Negative expression.** White Laz Güneşi on a red rounded tile, per DESIGN.md §"Three expressions". Verified by rendering at 16px: the bare symbol's thin blades wash out to a faint ring; the tile holds its color and silhouette. The bare symbol stays available as `favicon-mono.svg` for in-page use.
3. **A real kit** at `laz-gunesi-amblem/favicon/`: `favicon.svg`, multi-resolution `favicon.ico` (16/32/48), `apple-touch-icon.png` (full-bleed for iOS masking), PWA icons + `site.webmanifest`, and a `<head>` snippet. Legacy raster fallbacks use a full-bleed square (opaque) to avoid white-corner leakage on dark browser chrome.
4. **A discoverable home.** Root `ASSETS.md` indexes every brand asset (canonical path, color, use); `AGENTS.md` + a thin `CLAUDE.md` point any agent to it. Canonical-vs-mirror rule added for favicons (the adapter `public/` copy is a mirror), echoing the existing tokens mirror discipline.

**Why it mattered:** the favicon was the easy part. The real work was making the brand's assets findable and internally consistent so the *next* agent doesn't recreate, mis-color, or hunt. Drift is a defect; this pass closed the favicon/red drift and built the index to prevent the next one.

---

## Principles named during the conversation

These weren't all stated upfront. They emerged as turning points required them:

1. **Portability over preference.** Every decision must survive markdown round-trip
2. **The publisher precedes the brand.** House identity comes before individual brand
3. **One symbol, forever.** Discipline over per-brand symbolism
4. **Color must sit with cream.** Designed colors integrate, raw colors fight
5. **Brand color in exactly one role.** Links, nothing else
6. **Turkish content declares its language**, `lang="tr"` is correctness, not preference

Each principle was articulated when a decision required it. They're now permanent rules of the system.

---

## What was considered and rejected

For future reference, these alternatives were on the table at various points:

- **Single-family Fraunces.** Distinctive but body too assertive
- **Inter as primary.** Too ubiquitous, too SaaS-default
- **Geist.** Beautiful but too "of-2024," poor longevity
- **Manrope.** Your existing pick before this work; geometric character doesn't pair with editorial register
- **EB Garamond.** Too old-world, doesn't match the modern brand portfolio
- **Pure blue Pataraz** `#0000FF`: too aggressive against cream substrate
- **Universal yellow highlight.** Non-portable in markdown
- **Per-brand symbol design.** Sacrifices systemic discipline
- **Display-xl size at 64px.** Unnecessary; H1 absorbs hero
- **Editorial decoration tokens** (eyebrow, deck, byline, small, meta), absorbed into existing tokens

Each was rejected for documented reasons. None should be reconsidered without strong new evidence.

---

## Open questions parked for later

These weren't resolved during the design phase but are noted for the implementation phase:

- **Logo SVG geometry.** Needs designer-quality SVG path data from canonical source. The placeholder approximation in earlier specimens is not the final mark.
- **Pandoc template development.** The template fragment for docx/PDF generation is specified but not yet built.
- **Self-hosted font deployment.** Fonts can be served via Google Fonts CDN initially; self-hosting from each project's GitHub releases is the long-term move.
- **Dark mode.** Not addressed in v1.0. Could be added in v1.1 by inverting `--paper` and `--ink` variables.
- **Email-specific stylesheet.** Emails strip `@font-face`; a fallback-only stylesheet for email templates may be useful.

---

## Lessons captured for future-Emre

A few patterns from this conversation worth remembering:

1. **Test before committing.** Every typeface decision became correct only after rendering it against real content. Description ≠ evidence.

2. **Audit at every simplification opportunity.** "Anything to simplify?" was asked multiple times and produced cuts every time. The system got better with each round.

3. **Ask the longevity question.** "10 years from now" reframed several decisions. It separated infrastructure choices from fashion choices.

4. **Verify before locking.** Character coverage verification, Turkish locale handling, fallback testing, all caught real issues before production.

5. **Trust your push-back instincts.** "This feels too much," "I feel like body is boldish," "Should we try sans?", every push-back was correct and led to a better system. The instinct that something is off is usually right.

6. **Document the why.** This file exists because future-you may not remember why H4 absorbed eyebrow, why Pataraz shifted from `#0000FF` to `#1a24cc`, why we cut strong-em. The reasoning matters more than the conclusion.

---

## Status

System is at **v2.1.2**. DESIGN.md captures the specification. This file captures the reasoning.

**v1.0.** Specification complete (all tokens, brand classes, lockup grammar, substrate behavior).
**v1.1.** Implementation phase: Astro reference site live, real Laz Güneşi shipped (replacing the placeholder), logotype locked to Fraunces with new `--logotype` token, lockup simplified (brand color, no subtitle, no hover underline).
**v1.2.** Logotype re-tuned (slim Fraunces with WONK axis on), wordmarks always lowercase across all four brands, per-brand wordmark map in BaseLayout, page `<title>` kept Title Case as a separate concern.
**v1.3.** Logotype pivot to Space Grotesk Light (geometric grotesque sans). Two Fraunces versions had taught the team that "slim editorial serif" wasn't the brand's true direction.
**v1.4.** Logotype lands on Manrope ExtraLight; wordmarks finalized to single nouns where possible (`ağustos`, `pataraz`, `photometric`, plus `pld türkiye`). Symbol leads, wordmark supports.
**v2.0.** System consolidated onto Inter Tight + Inter + JetBrains Mono; Inter Tight became both display family and wordmark face.
**v2.1.2.** Logotype weight finalized at Inter Tight 650 with neutral tracking after bold-context comparison. Same family, stronger mark.

The system is in production use. Future v2.x updates: additional brands, dark mode, Pandoc/docx template parity. Documented in DESIGN.md as they ship.

## Brand asset kit (2026-06-20)

The spec/tokens layer was complete, but no *exported, hand-off-ready* assets existed
(no lockup files, favicons, social images, font hand-off). Added `brand/` as the
asset-manager home with a **generate-don't-maintain** architecture:

- **`brand/brands.json`** is the new keystone registry — one source for each brand's
  slug, wordmark, color, title, domain, tagline. Resolves the identity-data duplication
  previously split between `tokens.css` and `BaseLayout.astro` (registry is additive;
  the running adapters were not changed in this pass).
- **`brand/build.py`** is the engine. It bakes wordmarks to vector **outlines**
  (`fontTools`, Inter Tight) so assets are font-independent, composes lockups per
  the DESIGN.md geometry, and emits SVG + PDF (`reportlab`) + PNG (`resvg` via node).
- **Wordmark weight = 650, letter-spacing normal** — matched to the LIVE site agustos.com
  (verified via browser computed styles, 2026-06-20). The spec/component originally said
  Light (300) / -0.005em; this was a real drift between the docs and the production brand.
  **Reconciled 2026-06-20:** `DESIGN.md`, `adapters/astro/.../BrandLockup.astro`, the Rails
  `components.css`, and the typography showcase were all updated to 650 / normal. NOTE:
  `tokens.css` `font-weight: 300` is `.type-hero` (big hero text), NOT the lockup — left as-is.
  Stored in `brands.json` → `type.wordmark_weight`.
- Per brand `build.py` generates lockups (positive/negative/mono), favicons + app icons,
  and social avatar + OG image under `exports/<brand>/` (committed, like `laz-gunesi-amblem/`).
- **`brand/build_templates.py`** (sibling) generates the working documents from the same
  registry: `.ase`/`.clr` colour swatches, an email-safe HTML signature, a PowerPoint `.pptx`
  + Word `.docx` letterhead, and a 4-page brand-guidelines PDF (branded HTML rendered via the
  gstack `browse` tool, embedding the bundled fonts). Keynote/Slides/Pages are covered by
  importing the .pptx/.docx — no separate generation. Deps: python-pptx, python-docx,
  pyobjc (for .clr); pinned in `brand/requirements.txt`. See `brand/templates/README.md`.
- **Maintenance contract:** edit `brands.json` or the master symbol, then run `build.py`.
  Never hand-edit `exports/`. This is how the kit stays drift-free across all brands.

Status (2026-06-22): full kits (logos + documents) for **`agustos`**, **`pataraz`** (pataraz.com),
and **`pld türkiye`** (pldturkiye.com). **`photometric`** has logos only (documents deferred).
Taglines are now defined-but-unshown (per-brand `tagline_en`/`tagline_tr`); agustos = "curated
solutions" / "seçkin çözümler", others none. The lockup is always tagline-free. Novara is a brand
Ağustos *represents* (distributes), not a house sub-brand. Weight 650 was reached independently
here and on `chore/brand-assets-home` (v2.1.2) and converged in this merge.

## Product datasheet template (2026-06-22)

The kit generated brand chrome (logos, office docs, guidelines) but no **product**
artifact. Lighting is the business; a luminaire spec sheet ("teknik föy") is the
single most-used customer-facing document Ağustos and Pataraz produce. Added
`brand/build_datasheet.py` — a third engine alongside `build.py` (logos) and
`build_templates.py` (office docs).

Decisions made:

- **Half template, half data.** Unlike the other engines (brand chrome only), a
  datasheet carries per-product data. The brand half (lockup, colour, footer) resolves
  from `brands.json`; the product half is a `PRODUCTS` dict in the script, so each sheet
  is self-documenting rather than a blank form. `agustos` ships a sample (*Pro Spot 28*
  track spot) exercising the full template; **`pataraz` is a real product — PL22**, an
  ultra-thin tunable-white "tavan penceresi" (artificial-skylight) panel, with data and
  product photo transcribed from pataraz.com/pl-serisi/pl22 (2026-06-23), plus a dimensioned
  technical drawing (1236 × 636 × 70 mm) supplied by the product owner.
- **Turkish, full professional spec.** Labels in Turkish (`lang="tr"` for İ/ı). Field
  groups: Elektriksel · Fotometrik · Fiziksel · Koruma & Ortam · Ömür & Garanti, plus a
  sipariş (ordering) matrix and certifications — ERCO/Zumtobel-grade depth.
- **The design system maps onto a data-dense sheet without new rules.** Inter Tight for
  the header and section labels, Inter for prose, **JetBrains Mono + tabular numerals for
  every spec value and order code**, brand colour as a signal only (header rule, section
  ticks, table top-border, order codes) — never as fill.
- **2-column spec grid, not 3.** A first pass packed groups into three columns; it looked
  dense but forced long values (`24° (15°/24°/36° seçenekli)`) to wrap the label and risked
  clipping into the gutter on real user content. Two columns give each row room to stay on
  one line — the standard luminaire-datasheet layout — and the sheet still fits one A4.
- **Self-contained, std-lib only.** Embeds the bundled fonts and the lockup SVG via
  `file://` URIs (same pattern as the guidelines), so it needs no PIL/reportlab and runs on
  system `python3`; `--pdf` renders A4 via the gstack `browse` tool. Verified one page per
  sheet (page clamped to `height:297mm; overflow:hidden` with a measured ~5mm gap above the
  footer, after trimming the photo/drawing slots from 4:3 to 3:2).

- **Honest placeholders over fabricated specs.** Building PL22 from the public product page
  (which lists only 9 fields), unpublished values (IP, ta, lifetime, warranty) were rendered
  as `—`, never invented — the sheet doubled as a precise to-do of what the manufacturer's
  full spec sheet must supply. The product owner then supplied them (IP20, −20…+40 °C, Class II,
  L70B50 @ 30.000 h, 2 yıl warranty), completing the sheet. Ordering matrix + certifications
  became optional keys (a
  single tunable SKU has no variants), and raster product photos are base64-embedded so the
  HTML stays self-contained. Photos live in `brand/datasheet-assets/<slug>/` (inputs, kept
  out of the generated `exports/`).

**Why it mattered:** the kit can now produce the document the business actually sells with,
on-brand and regenerable, without hand-built InDesign files drifting from the system.
Generated for `agustos` (sample) and `pataraz` (real PL22); other brands produce a generic
placeholder sheet on demand.

## Datasheet engine: many products per brand + PX22 (2026-06-23)

A request for the **PX22** sheet (pataraz.com/px-serisi/px22) exposed the datasheet engine's
one structural shortcut: `PRODUCTS` was keyed by **brand slug**, so a brand could hold exactly
one luminaire. Dropping PX22 in would have overwritten the committed PL22 sheet — a regression.
The business has whole series (T · L · PY · PL · PX), each with multiple SKUs, so one-per-brand
was always a template-demo limitation, not a real constraint. PX22 was the first signal to fix it.

Decisions:

- **`PRODUCTS` is now a flat registry keyed by product** (`pataraz-pl22`, `pataraz-px22`,
  `agustos-pro-spot-28`), each entry naming its `brand`. Output is per-product:
  `exports/<brand>/datasheet/<product-key>.{html,pdf}`. CLI gained `--product <key>`; `--brand`
  now builds *all* of a brand's products. The old `<brand>-datasheet-template.*` files were
  renamed to their product keys and removed (PL22 was never a "template" once it became a real
  product — the name was already a misnomer the MEMORY had flagged).
- **PX22 is PL22's wall-mounted sibling** ("duvar penceresi" vs PL22's ceiling "tavan penceresi").
  The public page publishes the same 9 fields as PL22 and confirms an **identical electrical /
  photometric / control core** (160 W, Bluetooth+DALI, 2100–7500 K, Ra 93, 4200 lm); only size
  (781 × 1332 × 66 mm), weight (29,4 kg) and mounting (sıva altı/üstü, duvar) differ.
- **Carried over PL22's 5 unpublished values** (IP20, −20…+40 °C, Class II, L70B50 @ 30.000 h,
  2 yıl warranty) at the product owner's explicit direction — a deliberate, scoped exception to
  the "honest placeholders over fabricated specs" rule (TP: 2026-06-22), justified because PX22
  shares PL22's exact platform. Logged as a same-platform **assumption** in the `PRODUCTS` comment;
  confirm against the manufacturer's full PX22 spec sheet before treating as fact.
- **Technical drawing supplied by the owner** (front + side elevation), saved to
  `datasheet-assets/pataraz/px22-drawing.png` and wired into the second visual slot — full parity
  with PL22's layout, no placeholder.
- **Width is 781 mm (owner-confirmed); the drawing mislabeled it 718** (height 1332 and depth 66
  agreed across sources — a textbook 781↔718 transposition, this time in the drawing, not the page).
  Rather than re-render the label and risk a font mismatch on a CAD drawing, the PNG was corrected
  **by reordering its own glyphs** — "781" reuses the exact 7/8/1 of "718", so the three digit
  bitmaps were cut and recomposed 7‑8‑1 (white-boxed the original, the dimension line was already
  broken around the text). Pixel-identical font/weight/colour, zero re-typesetting. Sheet + drawing
  now both read **781 × 1332 × 66 mm**.

**Why it mattered:** the kit went from "one demo product per brand" to "a real product catalogue,"
without changing the template, the design system, or any brand chrome. Adding the next luminaire is
now one `PRODUCTS` block + a photo, and PL22 survived untouched.

## pataraz.com website: stack, registry spine, design feed (2026-06-30)

Kicked off **pataraz.com** — a Turkish, B2B specification catalog (the datasheet is the hero asset;
the site is its catalog). Captured first as a brand spec ([PATARAZ.md](PATARAZ.md), a faithful-sibling
identity doc), then a website design spec
([docs/superpowers/specs/2026-06-30-pataraz-website-design.md](docs/superpowers/specs/2026-06-30-pataraz-website-design.md)).

Decisions:

- **Stack: Rails 8 + SQLite + Tailwind + Hotwire monolith** (product owner's call), in **its own
  repo**, deployed via **Kamal → VPS** (SQLite needs a persistent disk, so single-server, not
  Cloudflare Pages — the repo's Astro→CF-Pages rule does not apply to a stateful Rails app). An
  earlier Astro draft was discarded when the owner named the Rails stack; the pivot cost nothing
  because the load-bearing decision below was framework-independent.
- **One shared product registry is the spine.** Product data moves out of `build_datasheet.py`'s
  inline `PRODUCTS` dict into `brand/products/*.json`; **both** the Python PDF builder and the Rails
  site read it. This is the structural answer to PATARAZ.md §3's "the on-page spec and the PDF must
  agree" — "keep two things in sync" (a discipline that eventually fails) becomes "there is only one
  thing." It survived the Astro→Rails pivot unchanged, which is how we knew it was right.
- **Design-first via a single feed file.** [pataraz-ui-brief.md](pataraz-ui-brief.md) is the
  self-contained brief to hand any Claude design session (brand tokens, page templates, component
  inventory, real PL22/PX22 content, asset paths). A built reference page,
  [mockups/pataraz-px22.html](mockups/pataraz-px22.html), is the visual anchor it points to —
  editorial-technical, cream + one blue accent, JetBrains Mono numerics, the real lockup inlined.
- **Mocking the UI found two missing data fields.** The product page needs a **`images[]`** gallery
  and a **`documents[]`** list (datasheet, IES, montaj kılavuzu, CE) — not the single `photo` /
  `datasheet_pdf` the spec's data model first had. Designing before building surfaced a registry-schema
  gap; folded back into the spec and the brief.

**Why it mattered:** the website got a settled stack and a no-drift data architecture *before* a line
of app code, and the brand visual language was proven on the hardest page (the product spec sheet)
before committing to the build. The Rails app, when it starts, is scaffolding against a known design
and a single source of truth — not discovery.

## v2.2 — radius and motion tokens, header CTA height overrides a mock (2026-07-10)

**On the table:** WEBSITE-agustos's topbar/homepage redesign (sourced from a
Claude-generated design handoff) needed `border-radius` and transition-duration
values the system hadn't formalized yet — every consuming component had been
hand-writing `120ms ease` and one-off radii.

**Chosen:** Added exactly three radii (`--radius-sm` 4px, `--radius-md` 6px,
`--radius-lg` 10px — small controls / buttons / cards) and two motion tokens
(`--dur` 120ms, `--ease` ease). Three radii, not a full numeric scale, to hold the
line on the system's "three tiers per dimension" restraint principle rather than
open the door to a fourth or fifth radius the first time someone wants a
slightly-different card corner.

**Also decided, same session:** the redesign's source mock specified the header's
"Bize Ulaşın" CTA button at 36px min-height ("small button size"). This system's
own accessibility section already requires a 44px minimum for button-like
controls. Rather than carve out an exception for compact chrome buttons, the
44px rule was kept as-is and the button was sized to comply — the mock was treated
as high-fidelity-but-not-infallible, and an existing, deliberately-written
accessibility rule outranks a visual reference file.

**Why this matters for future work:** the next brand site to reuse this system's
chrome patterns (Pataraz, PLD Türkiye, Photometric Batch — see DESIGN.md's "Adding
a new brand") inherits both the new tokens and this precedent: mock fidelity is
high, but it isn't a substitute for the system's own written accessibility rules
when the two conflict.

## v2.3 — one content measure across site chrome and pages (2026-07-14)

**Found:** WEBSITE-agustos's July topbar redesign used `max-width: 920px` on
elements that also carried 1.5rem horizontal padding. With the global border-box
reset, the header, homepage, and footer therefore had an 872px content area while
the established `.container` utility still provided 920px. At desktop widths the
two content edges differed by 24px on each side.

**Chosen:** 920px remains the content measure. Added `.site-frame` and rebuilt
`.container` on one 968px padded outer frame (`920px + 3rem`), with 1.5rem gutters.
`.site-frame` owns horizontal geometry for chrome and bespoke page sections;
`.container` adds the existing 4rem/6rem vertical page padding.

**Why it matters:** new chrome and old pages now share one rule instead of matching
by repeated numbers. Responsive behavior is unchanged, inner pages keep their
existing content density, and future components can opt into the frame without
recreating the box-model calculation.

## PY series datasheets: three sheets, one per size (2026-08-10)

Added `pataraz-py300600`, `pataraz-py600600`, `pataraz-py6001200` to the datasheet
`PRODUCTS` registry — PY serisi, Pataraz's recessed ceiling "ışık paneli" (light
panel), in its three published sizes. Data + photos transcribed from
pataraz.com/py-serisi/py300600, /py600600, /py6001200. User explicitly chose
**three separate sheets** over a single series sheet with a size matrix — each size
is a full standalone A4 document, not a shared table.

Two decisions worth remembering:

1. **The shared product photo is not a site defect.** pataraz.com serves the
   identical image for PY300600 (300×600mm) and PY6001200 (1200×600mm). First read
   as a content-integrity bug (two different products, one photo) — flagged to the
   user before building. The actual reason: both panels are 1:2 elongated
   rectangles (300:600 and 600:1200 reduce to the same ratio), so an illustrative
   3D render — which conveys shape, not absolute scale — is legitimately identical
   for both. PY600600 (square, 1:1) correctly has its own distinct render. **Always
   check the ratio math before calling a shared asset a bug** — the site was right,
   the instinct to flag it first (rather than silently ship or silently "fix" it)
   was still the correct move.

2. **No same-platform carry-over for the unpublished environmental fields**, unlike
   PX22's decision to carry IP/ta/insulation/lifetime/warranty from PL22. PY serisi
   is a different form factor (flat recessed panel vs. windowed skylight box), and
   no explicit direction was given to assume shared platform this time — so those
   five fields are honest `—` placeholders, per the project's default "honest
   placeholders over fabricated specs" rule. Carry-over is the exception (requires
   an explicit same-platform judgment call), not the default.

Also added a new spec row, **"Gökyüzü boyutu"** (visible illuminated aperture size,
smaller than the housing since the panel recesses into the ceiling) — a real
published field unique to this product type that PL22/PX22 don't have. Placed in
the Fiziksel group, right after Boyutlar.

**Why it mattered:** confirms the multi-product engine (built for PX22) scales
cleanly to a size-variant family — three new `PRODUCTS` entries, zero engine
changes, `_validate_products()` passed all three on the first build. Also
reinforces that "looks like a bug" claims about third-party data should be checked
against the math before being treated as fact.

## PY series follow-up: 36→43mm correction + in-house technical drawings (2026-08-10)

Same day, same three products. The owner supplied a technical drawing (side
profile + front elevation, PY300600 at 300×600) showing thickness **43mm** —
disagreeing with the 36mm published on pataraz.com and already on the sheet.
Flagged before touching anything (same instinct as the PX22 718/781 case);
confirmed by the owner: 36mm is the flat panel alone, 43mm is the true installed
depth once the mounting clips are included. **pataraz.com itself still shows
36mm** — the owner is correcting the live site separately; this fix only covers
the datasheet, and this repo has no access to edit the external site.

Applied 43mm to **all three sizes**, not just PY300600 — the assumption is that
the clip/edge hardware is shared across the PY family (same mounting system,
only the panel area changes). Flagged as an assumption in the `PRODUCTS` comment;
confirm if any size turns out to use different clips.

**No technical drawing existed for any PY size on pataraz.com** (confirmed by
checking each product page directly — one product photo each, no dimensioned
drawing). Generated all three in-house as programmatic SVG — a Python script
(two-view: side profile with mounting-clip glyphs + depth dimension; front
elevation with double-outline frame + width/height dimension lines) matching the
owner-supplied reference's exact visual convention, parameterized per product so
each size gets correct real proportions (a genuine 1:2 rectangle for
300×600/1200×600, a true square for 600×600) rather than a generic placeholder.
Saved at `datasheet-assets/pataraz/py{300600,600600,6001200}-drawing.svg`.

**Tooling note:** `cairosvg` (considered for SVG→PNG preview) needs system
`libcairo`, not installed and not worth a system-level install for a one-off
preview; PyMuPDF (already in use for other PDF/SVG work this session) renders
SVG pages directly via `fitz.open(path)` — no extra system dependency. Prefer
PyMuPDF over cairosvg for any future SVG rasterization in this environment.

**Why it mattered:** the dashed "Teknik çizim pending" placeholder is now a real,
correctly-dimensioned drawing on all three sheets — matching PL22/PX22's
completeness — without waiting on the manufacturer to publish one. The 36/43
discrepancy also reinforces the same lesson as PX22 718/781: always surface a
numeric conflict between sources before either silently trusting one or silently
"fixing" it.

**Same-day reversal:** the initial PY entries left Koruma & Ortam / Ömür & Garanti
as honest "—" placeholders (different form factor from PL/PX, no carry-over
direction given). The user then explicitly said to use PX22's values — so all
three PY sizes now carry IP20 / −20…+40 °C / Class II / L70B50 @ 30.000 saat /
2 yıl, same as PL22/PX22. This is not a contradiction of the earlier "no
assumption without direction" default — it's the exception firing exactly as
designed: honest placeholder is the default *until* the product owner makes the
same-platform call explicitly, same pattern as PX22's own carry-over from PL22.
