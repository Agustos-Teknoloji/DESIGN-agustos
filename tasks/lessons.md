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
