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

## Process, continued

4. **"Let's discuss" means prose, not a form.** (2026-09-16) The user asked to discuss what the
   brand guideline was missing; I answered with a gap analysis and then fired an AskUserQuestion
   form, which the user rejected. The discussion continued in chat and the decision came in
   chat. **Rule:** when the user frames a task as a discussion, present findings and a
   recommendation in prose and end with one or two plain questions. Reach for a decision form
   only when the user asks for options or the choice is a one-way door.

5. **Run the plan through `/dhh` before presenting it, then boil it down.** (2026-09-16) My
   eight-item, five-step follow-ups plan survived a `/dhh` review as three moves: two items were
   the same problem (a stale rule layer beside the kit), one was a second implementation of an
   existing test, one added a status value for a single row, one framed a doc change that did not
   work (a double iframe of a click-toggled theme). Three items were already closed by a merged
   PR I had not re-read. **Rule:** before presenting a plan, re-read main for work that already
   landed, merge items that share a root cause, and prefer moving an existing implementation over
   writing a second one. A plan that fits in three moves is usually the right size.

## Environment

6. **Probe the toolchain before the first real command.** (2026-09-16) After a macOS upgrade,
   `/usr/bin/git` and `/usr/bin/python3` were Xcode shims that failed on a licence prompt, and the
   first few calls worked before later ones failed. I lost a round of tool calls to it.
   **Rule:** when a familiar command fails with an unfamiliar error, run one probe for the binary
   (`which -a`, a direct Command Line Tools path) before retrying or reporting a blocker; the
   workaround is one environment variable, not a user action.
