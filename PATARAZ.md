# Pataraz — brand spec

The brand-specific spec for **Pataraz**. Pataraz is a *faithful sibling* in the Ağustos
Design System: it shares one symbol, one type stack, and one set of rules, and differs only
by **color** (`#1a24cc`) and **wordmark** (`pataraz`).

This file does **not** restate the whole system. It records what is *Pataraz-specific* and
points back to the master documents for everything else:

- **[DESIGN.md](DESIGN.md)** — the canonical specification (the rules). The master.
- **[ASSETS.md](ASSETS.md)** — where every Pataraz asset file lives.
- **[MEMORY.md](MEMORY.md)** — why decisions were made (read before reversing one).
- **[AGENTS.md](AGENTS.md)** — the task → file router for AI tools.

> **Inheritance rule.** When a *shared* rule changes, it changes in `DESIGN.md` and Pataraz
> inherits it automatically. Never fork a system rule into this file — only document what is
> genuinely Pataraz-only. If you find a shared rule copied here, delete the copy and link
> `DESIGN.md` instead.

---

## 1. Positioning & audience

**Pataraz is a premium luminaire brand for the B2B specification market.** It is the in-house
premium product line within the Ağustos portfolio — where Ağustos is the parent technology and
distribution company, Pataraz is the brand that *makes and specifies the light*.

**Primary audience:** lighting designers, architects, interior architects, electrical
contractors, and specifiers who choose luminaires for projects — not casual retail buyers.
These readers evaluate a product on its numbers (lumens, CRI, color temperature, IP rating,
lifetime) and on the credibility of the company behind them.

**The promise.** Premium luminaires, specified with precision. Pataraz earns trust through
*exactness* — complete, honest, well-presented technical data — and through restraint. It does
not shout; the engineering speaks.

**Tone of voice.** Technical, exact, calm, credible. Turkish-first for the home market (the
products, datasheets, and spec language are Turkish — see `DESIGN.md` §"Turkish locale
handling"). Never marketing-loud, never padded with adjectives a specifier would discount. When
in doubt, give the number.

**No tagline.** Pataraz is intentionally tagline-free (`brands.json` records this). The wordmark
stands alone. This is a confidence signal appropriate to a spec-market brand — and one less
thing to translate or maintain across artifacts.

**How it differs from Ağustos**

| | Ağustos | Pataraz |
|---|---|---|
| Role | Parent: technology + curated distribution | In-house premium luminaire brand |
| Audience | Broad / commercial | B2B spec market (designers, specifiers) |
| Color | Red `#cf142a` | Blue `#1a24cc` |
| Hero asset | The portfolio | The product datasheet ("teknik föy") |
| Tagline | *curated solutions* / *seçkin çözümler* | none |

`MEMORY.md` records *why* the premium positioning leans on the shared editorial type register:
it lets Pataraz feel premium without bespoke design spend. Keep that — the restraint is the
strategy, not a budget compromise.

---

## 2. Identity rules (Pataraz-specific)

Everything below is the *shared* system applied to Pataraz. The rule lives in `DESIGN.md`; this
section only notes the Pataraz value and the few things to check because the color is blue.

### Color

- **Pataraz blue is `#1a24cc`.** This is the single source of truth — tokens, symbol SVGs,
  favicons, exports. `--brand-pataraz` in `DESIGN.md` §"CSS variables".
- **Why not `#0000FF`.** The original pure web-blue was *refined* to `#1a24cc` so it sits with
  the cream substrate instead of fighting it (`DESIGN.md` §"Color must sit with cream" and
  §"Brand color refinement protocol"; rationale in `MEMORY.md`). Pure `#0000FF` is stale — if you
  find it, it is a bug; fix it to `#1a24cc`.
- Cream paper `#fefcf2`, ink `#1a1a1a`, and the substrate strategy are shared, unchanged
  (`DESIGN.md` §"Substrate strategy").

### Symbol & lockup

- **Symbol:** the shared Laz Güneşi (18-blade sun), in Pataraz blue. Never redrawn, never
  recolored to anything but `#1a24cc`. One symbol, forever (`DESIGN.md` §"The symbol").
- **Wordmark:** `pataraz` — lowercase, single noun (no "luminaires"/"aydınlatma" qualifier on
  the mark), Inter Tight weight **650** (`DESIGN.md` §"Per-brand wordmarks", §"Logotype: Inter
  Tight 650"). Never a tagline or subtitle on the lockup.
- **Lockup:** `[ symbol ] pataraz` composed at render time, not a static image
  (`DESIGN.md` §"The lockup").

### Type stack

Shared, unchanged: **Inter Tight** (display/wordmark), **Inter** (body), **JetBrains Mono**
(specs, codes, hex, identifiers — useful on datasheets). `DESIGN.md` §"The type stack".

### Three expressions & favicon

- **positive** (blue marks on light/dark) — default, ~90% of uses.
- **negative** (cream/white marks on a blue tile) — favicons, blue banners.
- **mono** (single ink) — single-color print, engraving.
- The **favicon is the negative expression**: white symbol on a blue `#1a24cc` tile
  (`DESIGN.md` §"Three expressions", §"Favicon & app icons").

> **Blue-specific check.** When placing cream/white on the blue tile, verify contrast and
> legibility per `DESIGN.md` §"Accessibility requirements / Contrast" — Pataraz blue is a flagged
> case there. Re-check any negative composition before shipping.

### Where the files are

All generated, never hand-edited: `brand/exports/pataraz/` (lockups, favicon, social, office,
swatches, email, guidelines, datasheet). To change an asset, edit `brand/brands.json` or the
master symbol and re-run the build — see `ASSETS.md` and `brand/README.md`.

---

## 3. Website direction — pataraz.com

The new site is a **specification / reference catalog**, not a storytelling shop. Its job is to
let a specifier find a product, trust the company, and walk away with the datasheet. Built
entirely inside the shared system (cream substrate, the type stack, blue as the single accent).

### Information architecture

```
Home
├── Series            (the product families, e.g. PL serisi)
│   └── Product        (one luminaire — the spec page)
│       └── Datasheet / Downloads   (the "teknik föy" PDF + any docs)
├── About             (the company / credibility for specifiers)
└── Contact           (project enquiry, reps, where to buy/spec)
```

The **Product page is the center of gravity** — everything routes a specifier toward a product's
numbers and its downloadable datasheet. Series pages are navigational; Home frames the brand and
points into Series.

### Look & component notes (within the system)

- **Substrate & accent.** Cream `#fefcf2` ground, ink `#1a1a1a` text, blue `#1a24cc` as the
  *single* accent — used as a signal (active state, section marks, the symbol), not decoration
  (`DESIGN.md` §"Brand color is a signal, not decoration").
- **Hero.** Calm and product-led: the luminaire and its defining numbers, not a slogan. Lots of
  cream, generous rhythm (`DESIGN.md` §"Vertical rhythm").
- **Spec tables.** The most important component. Mirror the datasheet's grouped structure
  (Elektriksel / Fotometrik / Fiziksel / Koruma & Ortam / Ömür & Garanti). Numbers and units in
  **JetBrains Mono** for alignment and credibility; Turkish labels, `lang="tr"` so İ/ı
  capitalize correctly.
- **Product page.** Photo + dimensioned drawing, short description, the grouped spec tables, and
  a prominent **datasheet download**. The on-page spec and the PDF datasheet must agree — same
  source of truth.
- **Typography & lockup** per `DESIGN.md`; favicon is the negative-on-blue set in
  `brand/exports/pataraz/favicon/` (with `site.webmanifest`).
- **Accessibility & Turkish locale** are non-negotiable — follow `DESIGN.md`
  §"Accessibility requirements" and §"Turkish locale handling".

> Implementation note: the Astro adapter (`adapters/astro/`) already carries the brand tokens,
> the `BrandLockup` component, and the favicon mirror — start the site from there rather than
> re-wiring the system.

---

## 4. Product datasheet conventions

The datasheet ("teknik föy") is Pataraz's **hero asset** (Section 1). Like everything else in the
kit it is *generated, not hand-made*: the data lives in one place and the brand chrome (lockup,
blue, footer) resolves from `brands.json`. **Never hand-edit files under `brand/exports/`.**

This section documents the conventions the engine already encodes, so every future datasheet
matches the two real ones (PL22, PX22) without re-deriving the rules.

### Where it lives & how to build

| | |
|---|---|
| Engine + product data | `brand/build_datasheet.py` — the `PRODUCTS` dict is the one place to edit |
| Product photo + dimensioned drawing | `brand/datasheet-assets/pataraz/<code>-urun.jpg` · `<code>-drawing.png` |
| Output (generated) | `brand/exports/pataraz/datasheet/<product-key>.html` · `.pdf` (e.g. `pataraz-px22.*`) |

```bash
# one product, with PDF:
python3 brand/build_datasheet.py --product pataraz-px22 --pdf
# every product for the brand:
python3 brand/build_datasheet.py --brand pataraz --pdf
```

`--pdf` renders via the `browse` headless engine. The datasheet reuses the generated lockup, so
run `python3 brand/build.py --brand pataraz` first if `exports/pataraz/lockup/` is empty. See
`brand/templates/README.md`.

### Product key & fields

- **Key:** `<brand>-<code>`, lowercase kebab-case (e.g. `pataraz-px22`). Validated at build time.
- **Required** (build fails loudly if missing): `brand`, `name`, `series`, `code`, `doc_type`,
  `rev`, `description`, `specs`.
- **Optional:** `photo`, `drawing`, `dim_note`, `certifications`, `ordering`.
- `series` format: `"<SERİ> serisi · <kısa tanım>"` — e.g. `"PX serisi · ultra ince duvar penceresi"`.

### Naming — descriptive, not yet a formal scheme

There is **no generative naming rule yet**; names are assigned per product as the range grows.
Document what a product *is*, don't force it into a system that isn't settled. As-built today:

- **PL serisi** — *tavan penceresi* (ceiling) artificial-skylight panels.
- **PX serisi** — *duvar penceresi* (wall) sibling. PL22 and PX22 share one optical-electrical
  core (160 W · 4200 lm · 2100–7500 K · Ra 93), differing only in size, weight, and mounting.

When the catalog matures into a real scheme, formalize it here — until then, keep it descriptive.

### Spec-field grammar — the five groups

Specs render as grouped tables. Use these **Turkish group labels in this order**; add rows within
a group as the product needs, but don't invent new top-level groups without reason:

1. **Elektriksel** — güç, besleme, sürücü, kontrol…
2. **Fotometrik** — ışık çıkışı, renk sıcaklığı, Ra, ışın açısı…
3. **Fiziksel** — boyutlar, ağırlık, gövde, montaj…
4. **Koruma & Ortam** — IP, ta, izolasyon sınıfı, IK…
5. **Ömür & Garanti** — ömür (L-değeri), garanti.

`lang="tr"` is set so İ/ı capitalize correctly — keep labels Turkish.

### Number & unit formatting (Turkish typography)

| Rule | Example |
|---|---|
| Decimal **comma** | `29,8 kg` · `> 0,90` |
| Thousands **dot** | `2.600 lm` · `30.000 saat` |
| Range with **en-dash** | `2100–7500 K` · `220–240 V` |
| Signed range: **true minus** `−` (U+2212) + spaced ellipsis | `−20 … +40 °C` |
| **Space** before unit (but not for codes) | `160 W` · `4200 lm` · but `IP20`, `Class II` |
| **Middle dot** `·` to join values | `Bluetooth · DALI` · `Sıva altı · sıva üstü` |
| Lifetime form | `L70B50 @ 30.000 saat` |

### Optional sections

- **`certifications`** — a list (`["CE", "RoHS"]`) rendered as badges. Omit when none is published.
- **`ordering`** — a `{columns, rows}` SKU/variant matrix. Omit for single-SKU tunable products
  (PL/PX have no published variants, so they carry no ordering matrix).

### Data honesty

- Transcribe from the manufacturer's spec and **cite the source in a comment** (e.g.
  `pataraz.com/px-serisi/px22`, with the date).
- Fields the public page omits: leave as `—`, **or** carry a value from a same-platform sibling
  *with a comment flagging the assumption* (PX22 carries IP / ta / izolasyon / ömür / garanti from
  PL22). Confirm against the full spec sheet before treating a carried value as final.
- Fix transcription errors at the **source asset**, not just the text (the PX22 drawing's
  `718 → 781` width transposition was corrected in the PNG).

---

*Pataraz is a brand within the Ağustos Design System. For any rule not stated here, `DESIGN.md`
is authoritative.*
