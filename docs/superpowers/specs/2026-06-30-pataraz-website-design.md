# pataraz.com — website design spec

**Date:** 2026-06-30
**Status:** approved design, pending implementation plan
**Brand spec:** [PATARAZ.md](../../../PATARAZ.md) (positioning, identity, website direction §3, datasheet conventions §4)

## 1. Goal

Build **pataraz.com**: a Turkish, B2B specification catalog for the Pataraz premium
luminaire brand. A specifier (lighting designer, architect, electrical contractor) should
find a product, trust the company, read exact numbers, and download the datasheet ("teknik
föy"). Per PATARAZ.md §1 the **datasheet is the hero asset**; the site is its catalog.

Success = a specifier can filter to a product and reach its spec + PDF in two or three
clicks, with on-page numbers that exactly match the PDF.

## 2. Stack (fixed by product owner)

- **Ruby 3.3+ / Rails 8** monolith.
- **SQLite** as the production database (file-based `production.sqlite3`), plus Solid
  Queue / Solid Cache (also SQLite) — Rails 8 defaults.
- **Tailwind CSS** via `tailwindcss-rails` (standalone CLI, **no Node toolchain**).
- **Hotwire** (Turbo + Stimulus) for dynamic catalog filtration and instant navigation.
  No React/Next.

## 3. Two-repo architecture & the brand seam

The Rails app lives in **its own repository** (`pataraz.com`), deployed independently.
`DESIGN-agustos` (this repo) remains the **brand source of truth**. They connect through a
single, version-pinned seam — never hand-copied data.

```
DESIGN-agustos (this repo) ──────────────┐  source of truth
  brand/products/*.json   (registry)      │
  brand/build_datasheet.py → PDFs         │
  brand/exports/pataraz/   (favicon,      │
     lockup, datasheet PDFs)              │
  brand/datasheet-assets/pataraz/ (photos)│
                                          │ git submodule (pinned)
pataraz.com (new repo) ───────────────────┘
  vendor/agustos-brand/  ← submodule of DESIGN-agustos
  rake pataraz:sync  → seeds SQLite from the registry JSON,
                       copies favicon/lockup/PDFs/images into the app
  app/ (Rails monolith)
```

- **Submodule, pinned to a commit.** The site builds reproducibly against a known brand
  version; bumping the submodule is a deliberate, reviewable act.
- **`rake pataraz:sync`** is the only bridge: it (a) reads `vendor/agustos-brand/brand/
  products/*.json` and upserts `Product` rows, and (b) copies the brand images, favicon,
  lockup, and generated datasheet PDFs into `public/` / `app/assets/`.
- Rationale: this preserves PATARAZ.md §4's "the on-page spec and the PDF must agree —
  same source of truth," now across a repo boundary and two languages (Python + Ruby).

## 4. Work in DESIGN-agustos (this repo) — the registry refactor

This is the prerequisite that makes the seam honest. Done here, on a branch off `main`.

1. **Extract product data to a registry.** Move each entry of the `PRODUCTS` dict in
   `brand/build_datasheet.py` into `brand/products/<product-key>.json` (one file per
   product: `pataraz-pl22.json`, `pataraz-px22.json`, `agustos-pro-spot-28.json`). Schema =
   today's entry verbatim (`brand, name, series, code, doc_type, rev, description, dim_note,
   specs{groups}, photo, drawing, certifications?, ordering?`).
2. **Refactor `build_datasheet.py`** to load `PRODUCTS` from `brand/products/*.json` instead
   of the inline dict. Behavior, output, and `REQUIRED_FIELDS` validation unchanged — verify
   the regenerated PL22/PX22 PDFs are byte-comparable (or visually identical) to current.
3. **Document the registry** in `ASSETS.md` and PATARAZ.md §4 (the registry is now the
   canonical product-data location; `build_datasheet.py` consumes it).
4. **Update PATARAZ.md §3** "Implementation note" — replace the Astro-adapter pointer with
   the Rails direction (the IA/look guidance in §3 stays; only the framework note changes).

This work can ship as its own PR before the website repo exists.

## 5. The Rails app (new repo)

### 5.1 Theming — Tailwind on top of the design system

Seed from `adapters/rails/`: copy `tokens.css`, `components.css`, `agustos_theme_helper.rb`,
the `agustos` layout, and `_brand_lockup`. Re-theme to Pataraz blue and Turkish:

- The design tokens (CSS variables in `tokens.css`) remain the source of truth. Tailwind's
  theme **references them** (`colors.brand → var(--brand)`, `cream → var(--paper)`, `ink`,
  the Inter Tight / Inter / JetBrains Mono families). Utilities for layout, tokens for brand.
- Brand applied via the existing helper / `.brand-pataraz` (`--brand: #1a1a1a`, shared `--signal: #cf142a`), `lang="tr"`.
- Favicon + lockup come from `brand/exports/pataraz/` via the sync task.

### 5.2 Data model

`Product` (one row per registry entry):

- **Filterable columns** (indexed, drive Hotwire filtering): `code`, `name`, `series`,
  `brand`, `mount_type`, `power_w`, `lumens`, `cct_min`, `cct_max`, `cri`.
- **`specs` JSON column** — the full grouped spec tables verbatim (the five Turkish groups),
  so the spec page renders exactly what the PDF shows without re-modeling every field.
- **Asset references** — `photo`, `drawing`, `datasheet_pdf` (paths populated by sync).
- Derived/filterable fields are parsed from the registry on seed; the `specs` blob is the
  display truth. Seeding is idempotent (upsert on `code`).

No admin/auth at launch — products change in the registry, then `rake pataraz:sync`.

### 5.3 Routes & pages (Turkish, ASCII slugs)

| Route | Controller#action | Purpose |
|---|---|---|
| `/` | `home#index` | Brand frame, calm product-led hero, entry into series |
| `/seriler` | `series#index` | The families (PL serisi, PX serisi) |
| `/seriler/:series` | `series#show` | Products in a series |
| `/urunler` | `products#index` | **Catalog with Hotwire filtering** (series / mount / CCT) |
| `/urunler/:code` | `products#show` | The spec page: photo + dimensioned drawing, description, the five grouped spec tables, prominent datasheet download |
| `/hakkinda` | `pages#about` | Company credibility for specifiers |
| `/iletisim` | `pages#contact` | Project enquiry (mailto / simple form at launch) |

Datasheet PDFs served from `public/datasheets/<code>.pdf` (copied by sync).

### 5.4 Hotwire filtration

`/urunler` renders a filter sidebar + a results list inside a **Turbo Frame**. Changing a
filter (series, mount type, CCT range) requests the same action with query params; the frame
swaps the list with no full reload. A small Stimulus controller debounces inputs and reflects
state in the URL (shareable filtered views). Filtering is server-side SQLite queries on the
indexed columns — fast at catalog scale, progressively enhanced (works without JS).

### 5.5 Key components / partials

- **`SpecTable`** (most important) — renders the five Turkish groups from `specs`; numerics
  and units in **JetBrains Mono**; `lang="tr"` for İ/ı.
- **`ProductCard`** (series + catalog listing), **`ProductHero`**, **`DimensionDrawing`**,
  **`DatasheetDownload`**, plus the shared `Header` / `Footer` / `_brand_lockup`.

## 6. Deploy

- **Kamal** (Rails 8 default, Docker — already installed locally) to a single small **VPS**
  (Hetzner / DigitalOcean, ~$5–10/mo).
- **Persistent volume** for `production.sqlite3` and the Solid Queue/Cache DBs — the one
  hard requirement of file-based SQLite in production. The datasheet PDFs/images ship inside
  the image (synced at build), so only the DB needs the volume.
- TLS via Kamal's built-in proxy. Domain `pataraz.com`.
- This **supersedes** the repo's Astro→Cloudflare-Pages deploy rule, which applies only to
  static sites, not a stateful Rails monolith.

## 7. Environment setup (step 0)

System Ruby is 2.6 and Rails isn't installed. Setup, per-project, with the already-installed
**mise**:

```
mise use ruby@3.3        # in the pataraz.com repo
gem install rails -v '~> 8.0'
rails new . -d sqlite3 --css tailwind   # Hotwire is default in Rails 8
```

Docker is present for Kamal. No Node required (Tailwind standalone CLI).

## 8. Out of scope (YAGNI at launch)

No CMS / admin UI, no authentication, no e-commerce or pricing, no English/i18n, no
full-text search (the catalog is small; filtering covers it), no SSR-less static export.
Each is a clean future addition; none is designed out.

## 9. Verification

- `rails test` + a **system test** proving the `/urunler` filters narrow results correctly
  (with and without JS).
- **Parity check:** PL22 and PX22 on-page spec tables match their generated PDFs
  number-for-number (same registry → assert in a test).
- `bin/rails zeitwerk:check`, `tailwindcss` build clean.
- Turkish İ/ı capitalization correct; blue lockup + negative-on-blue favicon correct.
- Lighthouse: performance + a11y pass on home, catalog, and a product page.

## 10. Build order (for the plan)

1. **DESIGN-agustos:** registry refactor (§4) — ships first, independently.
2. **pataraz.com repo:** scaffold (Rails 8 + Tailwind + Hotwire), brand submodule + sync task.
3. Data model + seed from registry.
4. Product spec page + `SpecTable` (prove parity early).
5. Catalog + Hotwire filtering.
6. Home, series, about, contact.
7. Kamal deploy to VPS.

## 11. Open follow-ups (not blockers)

- Exact VPS provider/region and the `pataraz.com` DNS cutover — decided at deploy time.
- Contact form: mailto at launch; a real form-to-email (Action Mailer) is a fast follow.
- PATARAZ.md §3 framework-note update lands with the §4 registry documentation change.
# Historical implementation note

The layout and content decisions in this document remain useful, but its Pataraz
blue references are superseded by `DESIGN.md` and `PATARAZ.md`: Pataraz identity
is black and white, and Ağustos red is the shared interface signal.
