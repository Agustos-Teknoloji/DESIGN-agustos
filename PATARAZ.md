# Pataraz — brand spec & UI brief

The brand-specific spec for **Pataraz**, and the single feed for designing the pataraz.com UI.
Pataraz is a *faithful sibling* in the Ağustos Design System: it shares one symbol, one type
stack, one neutral identity model, and one set of rules. Its distinguishing identity element is
the **wordmark** (`pataraz`).

This file does **not** restate the whole system. It records what is *Pataraz-specific* and
points back to the master documents for everything else:

- **[DESIGN.md](DESIGN.md)** — the canonical specification (the rules). The master.
- **[ASSETS.md](ASSETS.md)** — where every Pataraz asset file lives.
- **[archive/MEMORY.md](archive/MEMORY.md)** — why decisions were made (read before reversing one).
- **[AGENTS.md](AGENTS.md)** — the task → file router for AI tools.

> **Inheritance rule.** When a *shared* rule changes, it changes in `DESIGN.md` and Pataraz
> inherits it automatically. Never fork a system rule into this file — only document what is
> genuinely Pataraz-only. If you find a shared rule copied here, delete the copy and link
> `DESIGN.md` instead.

> **Build target for pataraz.com:** a **Rails 8 + Hotwire (Turbo/Stimulus) + Tailwind** monolith,
> Turkish-only, SQLite. You don't need the backend to design the UI — design in HTML/CSS
> (Tailwind), and the markup ports into ERB views directly. Keep it server-rendered and
> progressively enhanced.

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
not shout; the engineering speaks. When in doubt, show the number.

**Tone of voice.** Technical, exact, calm, credible. Turkish-first for the home market (the
products, datasheets, and spec language are Turkish — see `DESIGN.md` §"Turkish locale
handling"). Never marketing-loud, never padded with adjectives a specifier would discount.

**No tagline.** Pataraz is intentionally tagline-free (`brands.json` records this). The wordmark
stands alone. This is a confidence signal appropriate to a spec-market brand — and one less
thing to translate or maintain across artifacts.

**How it differs from Ağustos**

| | Ağustos | Pataraz |
|---|---|---|
| Role | Parent: technology + curated distribution | In-house premium luminaire brand |
| Audience | Broad / commercial | B2B spec market (designers, specifiers) |
| Identity ink | Red `#cf142a` | Off-black `#15130f` |
| Interaction signal | Red `#cf142a` | Shared red `#cf142a` |
| Hero asset | The portfolio | The product datasheet ("teknik föy") |
| Tagline | *curated solutions* / *seçkin çözümler* | none |

`archive/MEMORY.md` records *why* the premium positioning leans on the shared editorial type
register: it lets Pataraz feel premium without bespoke design spend. Keep that — the restraint is
the strategy, not a budget compromise.

---

## 2. Identity rules (Pataraz-specific)

Everything below is the *shared* system applied to Pataraz. The rule lives in `DESIGN.md`; this
section only notes the Pataraz application.

### Color

- **Pataraz identity ink is off-black `#15130f`.** The positive lockup is off-black on white;
  the negative lockup is cream/white on a black tile.
- **Shared interaction signal is Ağustos red `#cf142a`.** Content links and menu hover use a 2px red rule. Red never recolors the Pataraz logo.
- Pataraz blue is retired. `#1a24cc` and the older `#0000FF` are historical values, not active tokens.
- White paper `#ffffff`, cream bands `#fdf5f5`, and off-black ink `#15130f` are shared (`DESIGN.md` §"Substrate strategy"). Every other role token (surface, muted ink, rule) is the shared system value — see `DESIGN.md` §"Generated web variables"; do not re-list them here.

### Symbol & lockup

- **Symbol:** the shared Laz Güneşi (18-blade sun), in black for the positive identity expression.
  Never redraw it or substitute an approximation. One symbol, forever (`DESIGN.md` §"The symbol").
- **Wordmark:** `pataraz` — lowercase, single noun (no "luminaires"/"aydınlatma" qualifier on
  the mark), Inter Tight weight **650** (`DESIGN.md` §"Per-brand wordmarks", §"Logotype: Inter
  Tight 650"). Never a tagline or subtitle on the lockup.
- **Lockup:** `[ symbol ] pataraz` composed at render time, not a static image
  (`DESIGN.md` §"The lockup").

### Type stack

Shared, unchanged: **Inter Tight** (display, headings, UI, and the wordmark), **Inter** (body
copy), **JetBrains Mono** (all numerics, units, codes, and spec values — the credibility signal:
lumens, watts, kelvin, dimensions, and product codes set in mono so they align in columns and
read as data). Full scale and exact sizes/weights live in `DESIGN.md` §"Typography and content
tokens" — do not re-list pixel values here; they have drifted from the live spec before (see
`tasks/lessons.md`).

### Three expressions & favicon

- **positive** (black marks on light) — default, ~90% of uses.
- **negative** (cream/white marks on a black tile) — favicons and identity tiles.
- **mono** (single ink) — single-color print, engraving.
- The **favicon is the negative expression**: white symbol on an off-black `#15130f` tile
  (`DESIGN.md` §"Three expressions", §"Favicon & app icons").

Verify every negative composition for contrast and small-size legibility before shipping.

### Where the files are

All generated, never hand-edited: `brand/exports/pataraz/` (lockups, favicon, social, office,
swatches, email, guidelines, datasheet). To change an asset, edit `brand/brands.json` or the
master symbol and re-run the build — see `ASSETS.md` and `brand/README.md`.

For the two shipped products, the real files are:

| Asset | Path |
|---|---|
| Logo (positive, black on light) | `brand/exports/pataraz/lockup/pataraz-lockup__positive.svg` |
| Logo (negative, on black tile) | `brand/exports/pataraz/lockup/pataraz-lockup__negative.svg` |
| Favicon (white symbol on black) | `brand/exports/pataraz/favicon/favicon.svg` (full set in that dir + `site.webmanifest`) |
| OG / link preview | `brand/exports/pataraz/social/pataraz-og.png` |
| PL22 product photo / drawing | `brand/datasheet-assets/pataraz/pl22-urun.jpg` / `pl22-drawing.png` |
| PX22 product photo / drawing | `brand/datasheet-assets/pataraz/px22-urun.jpg` / `px22-drawing.png` |
| Datasheet PDFs | `brand/exports/pataraz/datasheet/pataraz-pl22.pdf` · `pataraz-px22.pdf` |

---

## 3. Website direction — pataraz.com

The site is a **specification / reference catalog**, not a storytelling shop. Its job is to let
a specifier find a product, trust the company, read exact specs, and download the datasheet
("teknik föy"). The datasheet is the hero asset; the site is its catalog — not e-commerce. Built
entirely inside the shared system (white substrate, off-black identity ink, rationed red rules).

> A built reference page exists: [`mockups/pataraz-px22.html`](mockups/pataraz-px22.html). Open
> it and match its visual language — it is the canonical look for the whole site. When designing,
> start with the **product spec page** against real PX22 data (§5 below); it exercises the spec
> table, the gallery, and the download, and proves the look before the catalog or home page.

### Information architecture

```
/                 Home — brand frame, product-led hero, entry into series
/seriler          Series index (PL serisi, PX serisi)
/seriler/:series  Products in a series
/urunler          Catalog — filterable (series / mount / CCT), Hotwire-instant
/urunler/:code    THE spec page — gallery + key facts + documents + spec tables
/hakkinda         About — company credibility for specifiers
/iletisim         Contact — project enquiry
```

The **product spec page (`/urunler/:code`) is the center of gravity** — everything routes a
specifier toward a product's numbers and its downloadable datasheet. Series and catalog pages
are navigational; Home frames the brand and points into them.

### Look & component notes (within the system)

Apply İskandivvian: Scandinavian restraint filtered through Mediterranean warmth.
Keep product discovery and technical comparison clear, calm, and functional.
Use comfortable spacing, plain surfaces, and direct explanations to make the experience approachable.
Use naturally lit installation photographs only when they support product understanding.
Introduce photographs in this order: product page, listing thumbnail, then homepage.
Type-only pages stay complete until those photographs exist.
Preserve product finishes, technical facts, black identity ink, and red interaction signals.
Keep marketing and catalog pages on white paper. Dark theme is for product UI, not pataraz.com.
Repeat the same primary CTA at most twice in the page body: the opening and one closing cream band.
Do not use quote treatments on marketing or product pages.

**Do**
- Lead with the product and its defining numbers.
- Set every spec value in JetBrains Mono; align units in columns.
- Use red sparingly as a shared signal (a marker, an active filter, the download link).
- Hairline rules and whitespace to separate, not boxes and shadows.
- Turkish throughout (`lang="tr"`), İ/ı correct.

**Don't (AI-slop / off-brand)**
- No gradient hero blobs, glassmorphism, neon glows, or purple SaaS gradients.
- No drop-shadow "card soup," no rounded-everything, no emoji.
- No stock-photo hero of a generic office. Use the real product photography.
- No marketing superlatives ("revolutionary," "stunning"). Specifiers discount adjectives.
- Red is never a background wash or a gradient. It remains a small, flat interaction signal.

Component notes:

- **Hero.** Calm and product-led: the luminaire and its defining numbers, not a slogan. Generous rhythm (`DESIGN.md` §"Vertical rhythm").
- **Spec tables.** The most important component. Mirror the datasheet's grouped structure
  (Elektriksel / Fotometrik / Fiziksel / Koruma & Ortam / Ömür & Garanti). Numbers and units in
  **JetBrains Mono** for alignment and credibility; Turkish labels, `lang="tr"` so İ/ı
  capitalize correctly. The on-page spec and the PDF datasheet must agree — same source of truth.
- **Product page.** Two columns: a **gallery** (main viewer + thumbnail strip; products carry
  **several images** including the dimensioned technical drawing, shown desaturated), and a
  compact **key-facts** list (4–5 headline specs in mono) plus a **documents list** — products
  carry **several downloads** (Teknik Föy PDF, IES/photometric, montaj kılavuzu, CE beyanı), each
  a file-type tag + name + download affordance. Each product's schema needs `images[]` and
  `documents[]`, not single fields.
- **Catalog.** Filter sidebar (series, mount type, CCT range) applies instantly via Turbo Frame —
  no full reload, filters reflect in the URL, and it works without JS. Product grid uses calm
  cards: photo, name + code (mono), series, 2–3 key specs.
- **Typography & lockup** per `DESIGN.md`; favicon is the negative-on-black set in
  `brand/exports/pataraz/favicon/` (with `site.webmanifest`).
- **Accessibility & Turkish locale** are non-negotiable — follow `DESIGN.md`
  §"Accessibility requirements" and §"Turkish locale handling".

Component inventory:

| Component | Role |
|---|---|
| **`SpecTable`** | THE component. Renders the five Turkish spec groups; values in JetBrains Mono; `lang="tr"`. On-page truth == the PDF. |
| `Gallery` | Product images: main viewer + thumbnail strip, click-to-swap. Holds several images including the technical drawing. |
| `KeyFacts` | The "Öne çıkanlar" compact list — 4–5 headline specs in mono. |
| `DocumentList` | The "Belgeler" list — several typed downloads (PDF / IES / manual / CE), each a tag + name + download. |
| `ProductCard` | Catalog + series listing tile: image, name, code (mono), key specs. |
| `FilterSidebar` | Catalog filters → Turbo Frame, URL-reflected. |
| `Header` / `Footer` / `BrandLockup` | From the design system; neutral Pataraz identity with shared red interactions. |

> Implementation note: the Astro adapter (`adapters/astro/`) already carries the brand tokens,
> the `BrandLockup` component, and the favicon mirror — start the site from there rather than
> re-wiring the system.

---

## 4. Product datasheet conventions

The datasheet ("teknik föy") is Pataraz's **hero asset** (Section 1). Like everything else in the
kit it is *generated, not hand-made*: the data lives in one place and the brand chrome (lockup,
identity ink, footer) resolves from `brands.json`. **Never hand-edit files under `brand/exports/`.**

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

### Real products, for reference

Two real products ship today. Design and build against this exact data, not lorem ipsum, so spec
tables and cards are true from the first draft.

**PL22 — `pataraz-pl22`**
- **Series:** PL serisi · ultra ince tavan penceresi (ceiling)
- **Description (TR):** "Gökyüzü penceresi etkisi yaratan ultra ince tavan paneli. 2100–7500 K
  ayarlanabilir beyaz ışığıyla gün ışığının ritmini iç mekâna taşır; yüksek renksel geriverim
  (Ra 93) ile renkleri doğal gösterir. Sıva üstü montaj, Bluetooth ve DALI ile kontrol."
- **Dimensions:** B × D × Y: 1236 × 636 × 70 mm

| Group | Rows |
|---|---|
| **Elektriksel** | Güç `160 W` · Kontrol sistemi `Bluetooth · DALI` |
| **Fotometrik** | Işık çıkışı `4200 lm` · Renk sıcaklığı `2100–7500 K (ayarlanabilir)` · Renksel geriverim `Ra 93` |
| **Fiziksel** | Boyutlar `1236 × 636 × 70 mm` · Ağırlık `29,8 kg` · Montaj şekli `Sıva üstü` · Montaj yeri `Tavan` |
| **Koruma & Ortam** | Koruma sınıfı (IP) `IP20` · Ortam sıcaklığı (ta) `−20 … +40 °C` · İzolasyon sınıfı `Class II` |
| **Ömür & Garanti** | Ömür `L70B50 @ 30.000 saat` · Garanti `2 yıl` |

**PX22 — `pataraz-px22`**
- **Series:** PX serisi · ultra ince duvar penceresi (wall)
- **Description (TR):** "Duvar penceresi etkisi yaratan ultra ince ışık paneli. 2100–7500 K
  ayarlanabilir beyaz ışığıyla gün ışığının ritmini penceresiz iç mekânlara taşır; yüksek
  renksel geriverim (Ra 93) ile renkleri doğal gösterir. Sıva altı veya sıva üstü montaj,
  Bluetooth ve DALI ile kontrol."
- **Dimensions:** G × Y × D: 781 × 1332 × 66 mm

| Group | Rows |
|---|---|
| **Elektriksel** | Güç `160 W` · Kontrol sistemi `Bluetooth · DALI` |
| **Fotometrik** | Işık çıkışı `4200 lm` · Renk sıcaklığı `2100–7500 K (ayarlanabilir)` · Renksel geriverim `Ra 93` |
| **Fiziksel** | Boyutlar `781 × 1332 × 66 mm` · Ağırlık `29,4 kg` · Montaj şekli `Sıva altı · sıva üstü` · Montaj yeri `Duvar` |
| **Koruma & Ortam** | Koruma sınıfı (IP) `IP20` · Ortam sıcaklığı (ta) `−20 … +40 °C` · İzolasyon sınıfı `Class II` |
| **Ömür & Garanti** | Ömür `L70B50 @ 30.000 saat` · Garanti `2 yıl` |

---

*Pataraz is a brand within the Ağustos Design System. For any rule not stated here, `DESIGN.md`
is authoritative.*
