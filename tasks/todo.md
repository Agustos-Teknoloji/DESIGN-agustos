# Brand Kit — Ağustos & Sub-Brands

**Goal:** Stand up a maintainable brand-asset kit. One hand-edited registry + the shared
symbol generate every per-brand deliverable. First pass proves it on **Ağustos only**;
`pataraz`, `pld türkiye`, `photometric` follow by re-running the engine.

**Decisions locked (2026-06-20):**
- Office surfaces: PowerPoint, Keynote, Google Slides, Word/Pages letterhead.
- Brand scope this pass: **Ağustos only** (pilot the pipeline).
- Approach: **generated pipeline** (`build.py`) — assets derive from sources, never hand-maintained.

**Architecture:** hand-maintain 3 sources (`brands.json`, `laz-gunesi-amblem/`, `tokens` + `DESIGN.md`)
→ `build.py` → generated `exports/` → consumed by web / print / office / social.

---

## Phase 0 — Keystone & scaffolding  ✅ DONE
- [x] Create `brand/` directory (sits beside `laz-gunesi-amblem/`, reuses its kit convention)
- [x] Scaffold `brand/brands.json` with all 4 brands prefilled (slug, wordmark, color, title).
      `agustos` filled (title + domain agustos.com); tagline + others' domain/tagline left TODO.
- [x] `brand/fonts/` — vendored Inter Tight + Inter + JetBrains Mono (variable ttf, roman+italic),
      OFL licenses, and `README.md` (install-before-office instructions)
- [x] Note in `MEMORY.md`: `brands.json` is now the single source for brand identity data.
      Registry is additive — existing `tokens.css` and adapters untouched this pass.

## Phase 1 — The engine (build.py) — generate Ağustos assets  ✅ DONE
- [x] Tooling chosen after probe: fonttools (outline) + reportlab (PDF) + resvg/node (PNG) + Pillow.
      No system Cairo needed. Python venv at repo `.venv` (gitignored); deps in `brand/README.md`.
- [x] `build.py` reads `brands.json` + `laz-gunesi-amblem/svg/master.svg`
- [x] **Lockups** (symbol + Inter Tight Light wordmark, outlined, per DESIGN.md geometry):
      3 expressions × {svg, pdf, png@2400 + @800} → `exports/agustos/lockup/`
- [x] **Favicons + app icons**: favicon.ico, favicon.svg, apple-touch-icon, manifest PNGs,
      `site.webmanifest` → `exports/agustos/favicon/`
- [x] **Social**: square avatar (400/1000) + OG image 1200×630 → `exports/agustos/social/`
- [x] Idempotent re-run; `--brand <slug>` flag (defaults to all brands in registry)
- [x] **Verified visually**: positive/negative lockups, PDF fill-rule, favicon, OG all reviewed.

## Phase 2 — Office & document templates (Ağustos)
- [ ] **PowerPoint** `.potx` + theme — generated from tokens (python-pptx / pptx skill) — AUTO tier
- [ ] **Word** `.dotx` letterhead + HTML email signature — generated (docx skill) — AUTO tier
- [ ] **Keynote** template — hand-build spec + starter (proprietary; not script-generated) — HAND tier
- [ ] **Google Slides** master deck — setup spec + shareable copy-me link — HAND tier
- [ ] **Pages** letterhead — hand-build spec (proprietary) — HAND tier
- [ ] `templates/README.md` — which self-update vs. which are hand-maintained, and how to re-skin per brand

## Phase 3 — Shareable brand guidelines (FULL — optional this pass)
- [ ] 2–4pp PDF for non-engineers (partners, printers): logo do/don'ts, color, type, clear-space.
      Derived from `DESIGN.md`, NOT a copy of the 43KB engineering spec.

## Phase 4 — Scale to sub-brands (after Ağustos approved)
- [ ] Run `build.py` for pataraz, pld türkiye, photometric (≈10 min; no new design work)
- [ ] Re-skin office templates per brand (cover color + wordmark swap)

## Maintenance contract (the "keep up to date" answer)
- [ ] `brand/README.md`: to change anything — edit `brands.json` (or `master.svg`) → run `build.py`.
      Never hand-edit files under `exports/`. Office HAND-tier templates: edit in-app, re-export.

---

## Review

**Phase 0 + 1 complete (Ağustos), 2026-06-20.**

Delivered:
- `brand/brands.json` — keystone registry (4 brands).
- `brand/fonts/` — Inter Tight, Inter, JetBrains Mono (variable, roman+italic) + OFL + install README.
- `brand/build.py` — the engine; `brand/scripts/render_png.mjs` — node/resvg PNG helper.
- `brand/exports/agustos/` — 29 files: lockups (positive/negative/mono × svg/pdf/png), full
  favicon + app-icon set + webmanifest, social avatar (400/1000) + 1200×630 OG image.
- `brand/README.md` — maintenance contract ("edit sources, never edit exports").

Engineering decisions worth remembering:
- Wordmark baked to vector **outlines** → assets are font-independent (no install needed at point of use).
- Renderer chosen empirically after a dependency probe (reportlab needs Cairo for PNG → used resvg/node instead).
- No system libraries installed; venv + node-local deps only.

Verification: all key outputs rendered and inspected by eye; PDF rasterized via `sips` to
confirm vector fill-rule. Lockup geometry matches the DESIGN.md spec.

**Correction (2026-06-20):** first generation used the spec weight (Inter Tight Light 300,
tracking -0.005em) and looked wrong. Verified live agustos.com computed styles via /browse:
actual wordmark is **weight 650, letter-spacing normal**. Updated `brands.json` + `build.py`,
regenerated. Wordmark width now matches live to 0.15% (88.41px vs 88.28px @ 24px). ⚠ DESIGN.md /
tokens.css / BrandLockup.astro still say 300 — design-system docs are stale vs the live brand.

Reconciliation (2026-06-20, user chose "update spec to 650"): updated DESIGN.md (logotype
section + lockup grammar), BrandLockup.astro, Rails components.css, and typography.astro
showcase to weight 650 / normal tracking. tokens.css left unchanged (its 300 is .type-hero,
not the lockup). Design-system spec now matches the live brand.

Open / next:
- Confirm Ağustos **tagline** in `brands.json` (currently TODO).
- Phase 2 (office templates), Phase 3 (guidelines PDF), Phase 4 (other 3 brands) not started.
