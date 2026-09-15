# Lessons — Ağustos Design System

Patterns captured from corrections, to avoid repeating mistakes.

## Process

1. **Plans always go to `tasks/todo.md` — not just chat.** (2026-06-20) When the user asks to
   "create a plan," write it to the TODO file as checkable items and keep it updated as work
   progresses. Discussing the plan in chat is not enough; the TODO file is the durable record.

## Brand / assets

2. **The running product is the source of truth, not the spec doc.** (2026-06-20) I generated the
   Ağustos lockup from `DESIGN.md` / `tokens.css` / `BrandLockup.astro`, which all say the wordmark
   is **Inter Tight Light (300), letter-spacing −0.005em**. But the live site agustos.com renders
   **weight 650, letter-spacing normal** — the docs had drifted. The logo looked wrong.
   **Rule:** when an asset has a live production reference, measure the live computed styles first
   (`/browse` → `getComputedStyle` on the real element) and treat the running product as canonical
   when it conflicts with stale specs. Flag the drift so the docs can be reconciled.

3. **Second instance of lesson 2, on chrome this time.** (2026-09-15) `DESIGN.md` §"Site chrome"
   and the v3.0 record in `archive/MEMORY.md` say agustos.com shipped a one-row topbar in July
   2026 and retired the sidebar. The live site ships a 240px fixed left sidebar
   (`aside.side-menu`) on every page, with a sticky mobile header and drawer. The product owner
   is happy with it. I argued from the stale record until the user corrected me.
   **Rule:** before recommending any chrome, layout, or component rule as "already decided,"
   open the live site and probe it. A recorded decision that the live product does not show
   is a proposal, not a fact.
