# Pataraz — UI design brief

**This file is the single feed for designing the pataraz.com UI.** Attach or paste it into a
Claude design / frontend session and it has everything needed: brand visual language, page
templates, the component inventory, and real product content. Deeper rules live in
[DESIGN.md](DESIGN.md) (the system) and [PATARAZ.md](PATARAZ.md) (the brand); this brief is the
UI-relevant slice plus pointers to the real asset files.

> Build target is a **Rails 8 + Hotwire (Turbo/Stimulus) + Tailwind** monolith, Turkish-only,
> SQLite. You don't need the backend to design the UI — design in HTML/CSS (Tailwind), and the
> markup ports into ERB views directly. Keep it server-rendered and progressively enhanced.

---

## 1. What we're designing

**pataraz.com** — a Turkish, **B2B specification catalog** for the Pataraz premium luminaire
brand. The audience is lighting designers, architects, and electrical contractors who choose
luminaires for projects. They judge a product on its **numbers** and on the credibility of the
company behind them.

**The job of the site:** let a specifier find a product, trust it, read exact specs, and
download the datasheet ("teknik föy"). The **datasheet is the hero asset**; the site is its
catalog. Not a storytelling shop, not e-commerce.

**Tone:** technical, exact, calm, credible. Restraint is the strategy — "it does not shout; the
engineering speaks." When in doubt, show the number.

---

## 2. Brand visual language (self-contained)

### Color

| Token | Value | Use |
|---|---|---|
| **Pataraz blue** | `#1a24cc` | The single accent. A **signal, not decoration** — active state, section marks, the symbol, key links. Never a wash or gradient. |
| Cream (paper) | `#fefcf2` | Default page ground. The brand substrate. |
| White (paper-white) | `#ffffff` | Optional working/UI substrate (e.g. dense tables) via `.paper-white`. |
| Ink | `#1a1a1a` | Primary text. |
| Ink-soft | `#4a4a4a` | Secondary text. |
| Ink-faint | `#8a8a8a` | Captions, meta. |
| Rule | `#e8e3d0` | Hairline dividers on cream (`#e8e8e8` on white). |

Optional dark theme (opt-in, not required at launch): paper `#16140f`, ink `#f0ebd8`, blue
stays `#1a24cc`.

### Type — three families, one system

- **Inter Tight** — display, headings, UI, and the **wordmark** (the lockup is Inter Tight
  **650**, lowercase). Variable weight.
- **Inter** — body copy, paragraphs, inline.
- **JetBrains Mono** — **all numerics, units, codes, spec values.** This is the credibility
  signal: lumens, watts, kelvin, dimensions, product codes all set in mono so they align in
  columns and read as data.

Scale (from the design system — match it):

| Role | Family | Size | Weight | Tracking / leading |
|---|---|---|---|---|
| Hero | Inter Tight | `clamp(56px,9vw,112px)` | 300 | -0.045em · lh 0.96 |
| Hero (medium) | Inter Tight | `clamp(40px,6vw,72px)` | 400 | -0.032em · lh 1.02 |
| Hero deck/lead | Inter | `clamp(18px,1.5vw,21px)` | 400 | lh 1.55 |
| H1 | Inter Tight | 44px | 500 | -0.026em · lh 1.05 |
| H2 | Inter Tight | 24px | 500 | -0.014em · lh 1.18 |
| H3 | Inter Tight | 18px | 500 | lh 1.3 |
| H4 / eyebrow label | Inter Tight | 12px | 700 | (small caps-ish label) |
| Body | Inter | 16px | 400 | lh 1.65 |

### Substrate, rhythm, motion

- **Cream ground, generous whitespace, editorial vertical rhythm.** Calm pages with room to
  breathe — the opposite of a dense dashboard.
- **Motion is minimal and calm.** Hotwire gives instant filter/nav updates; do NOT add flashy
  transitions. A subtle fade on Turbo-frame swaps is the ceiling.
- One accent. The page is cream + ink + a little blue. That's the whole palette.

---

## 3. Look principles + anti-patterns

**Do**
- Lead with the product and its defining numbers.
- Set every spec value in JetBrains Mono; align units in columns.
- Use blue sparingly as a signal (a marker, an active filter, the download link).
- Hairline rules and whitespace to separate, not boxes and shadows.
- Turkish throughout (`lang="tr"`), İ/ı correct.

**Don't (AI-slop / off-brand)**
- No gradient hero blobs, glassmorphism, neon glows, or purple SaaS gradients.
- No drop-shadow "card soup," no rounded-everything, no emoji.
- No stock-photo hero of a generic office. Use the real product photography.
- No marketing superlatives ("revolutionary," "stunning"). Specifiers discount adjectives.
- Blue is never a background wash or a gradient. One flat accent.

---

## 4. Information architecture

```
/                 Home — brand frame, product-led hero, entry into series
/seriler          Series index (PL serisi, PX serisi)
/seriler/:series  Products in a series
/urunler          Catalog — filterable (series / mount / CCT), Hotwire-instant
/urunler/:code    THE spec page — gallery + key facts + documents + spec tables
/hakkinda         About — company credibility for specifiers
/iletisim         Contact — project enquiry
```

The **product spec page is the center of gravity.** Everything routes a specifier toward a
product's numbers and its downloadable PDF.

---

## 5. Page templates

### Home `/`
- **Hero:** calm, product-led. The PL22 (or a featured luminaire) photographed on cream, with
  2–3 defining numbers beside it (e.g. `2100–7500 K` · `Ra 93` · `4200 lm`) in mono. A short
  Inter-Tight headline, no slogan.
- **Series entry:** two clean blocks — PL serisi (tavan / ceiling), PX serisi (duvar / wall) —
  each linking into the catalog.
- Light "who is Pataraz" line for specifiers; link to About. No feature-grid filler.

### Catalog `/urunler`
- **Filter sidebar** (left): series, mount type (tavan / duvar), CCT range. Filters apply
  **instantly via Turbo Frame** — the product list swaps with no full reload; selected filters
  reflect in the URL (shareable). Works without JS (server-rendered).
- **Product grid** (right): `ProductCard`s — product photo, name + code (mono), series, 2–3
  key specs. Calm grid, hairline separation, lots of cream.

### Product spec page `/urunler/:code` — the hero page

> **A built reference page exists: [`mockups/pataraz-px22.html`](mockups/pataraz-px22.html).**
> Open it and match its visual language — it is the canonical look for the whole site. The
> series, catalog, and home pages should feel like they came from the same hand.

1. **Title block:** series eyebrow (blue, with a tick) → product name (Inter Tight, large) →
   one-line Turkish deck. No code/revision chip in the title.
2. **Hero (two columns):**
   - **Left — image gallery:** a main viewer + a thumbnail strip. Products have **several
     images** (product shots + the dimensioned technical drawing). Clicking a thumbnail swaps
     the main image; the drawing keeps a desaturated technical-grid treatment when shown.
   - **Right — Öne çıkanlar + Belgeler:** a compact key-facts list (4–5 headline specs in
     JetBrains Mono), then a **documents list** — products have **several downloads** (Teknik
     Föy PDF, IES/photometric, montaj kılavuzu, CE beyanı). Each row: file-type tag + name +
     download affordance.
3. **Description:** one short Turkish paragraph (Inter).
4. **Spec tables:** the **five grouped tables** (see §7) — the most important component. Group
   titles in blue with a marker; rows are `label … value`, values in **JetBrains Mono**,
   tabular-nums, right-aligned. Must match the datasheet PDF exactly.

### Series `/seriler`, `/seriler/:series`
- Series index: two family blocks with a one-line description and a representative image.
- Series show: the same `ProductCard` grid scoped to that series.

### About `/hakkinda`, Contact `/iletisim`
- About: short, credible company framing for specifiers (no fluff). Editorial, mostly type.
- Contact: project enquiry — name / firm / message; at launch a simple mailto or a basic
  form. Calm single-column.

---

## 6. Component inventory

| Component | Role |
|---|---|
| **`SpecTable`** | THE component. Renders the five Turkish spec groups; values in JetBrains Mono; `lang="tr"`. On-page truth == the PDF. |
| `Gallery` | Product images: main viewer + thumbnail strip, click-to-swap. Holds **several images** including the technical drawing (desaturated grid treatment). |
| `KeyFacts` | The "Öne çıkanlar" compact list — 4–5 headline specs in mono. |
| `DocumentList` | The "Belgeler" list — **several typed downloads** (PDF / IES / manual / CE), each a tag + name + download. |
| `ProductCard` | Catalog + series listing tile: image, name, code (mono), key specs. |
| `FilterSidebar` | Catalog filters → Turbo Frame, URL-reflected. |
| `Header` / `Footer` / `BrandLockup` | From the design system; re-themed blue. |

> **Content model note (folded back from the mock):** each product carries **`images[]`**
> (gallery, not a single photo) and **`documents[]`** (each = label + file + format, not a single
> PDF). The shared registry schema and the Rails model should reflect both.

---

## 7. Real sample content — design against these, not lorem

Two real products. Use this exact data so the spec tables and cards are true.

### PL22 — `pataraz-pl22`
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

### PX22 — `pataraz-px22`
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

**Number formatting (Turkish):** decimal **comma** (`29,8 kg`), thousands **dot**
(`30.000 saat`), ranges with en-dash (`2100–7500 K`), true minus `−` for signed ranges
(`−20 … +40 °C`), space before units (`160 W`) but not codes (`IP20`).

---

## 8. Asset files (real paths in this repo)

| Asset | Path |
|---|---|
| Logo (lockup, blue on light) | `brand/exports/pataraz/lockup/pataraz-lockup__positive.svg` |
| Logo (negative, on blue tile) | `brand/exports/pataraz/lockup/pataraz-lockup__negative.svg` |
| Favicon (white symbol on blue) | `brand/exports/pataraz/favicon/favicon.svg` (full set in that dir + `site.webmanifest`) |
| PL22 product photo | `brand/datasheet-assets/pataraz/pl22-urun.jpg` |
| PL22 dimension drawing | `brand/datasheet-assets/pataraz/pl22-drawing.png` |
| PX22 product photo | `brand/datasheet-assets/pataraz/px22-urun.jpg` |
| PX22 dimension drawing | `brand/datasheet-assets/pataraz/px22-drawing.png` |
| OG / link preview | `brand/exports/pataraz/social/pataraz-og.png` |
| Datasheet PDFs | `brand/exports/pataraz/datasheet/pataraz-pl22.pdf` · `pataraz-px22.pdf` |

---

## 9. Hard brand rules (don't break)

- **Blue is `#1a24cc`** everywhere. Never another blue, never a gradient, never a wash.
- **One symbol** (the Laz Güneşi sun), only ever in blue. Never redraw or recolor it.
- **Wordmark `pataraz`** — lowercase, Inter Tight 650, no tagline/subtitle on the lockup.
- **Numbers belong in JetBrains Mono.** Always.
- **Turkish, `lang="tr"`.** No English at launch.

---

## 10. How to use this brief

1. Start a Claude design / frontend session and attach this file.
2. Ask for the **product spec page first** (`/urunler/:code` with PX22) — it exercises the
   `SpecTable`, the visual row, and the download, and proves the look against real data.
3. Then the **catalog** (with the filter sidebar) and the **home** hero.
4. Output Tailwind HTML; it ports directly into the Rails ERB views.

Reference for anything not covered here: [DESIGN.md](DESIGN.md), [PATARAZ.md](PATARAZ.md).
