# Agent guide — Ağustos Design System

You are working in the **canonical source** of the Ağustos design system. Read these before acting:

1. **[ASSETS.md](ASSETS.md)** — the index of every brand asset (logo, symbol, favicon, colors, fonts).
   Find the file here before creating or hunting for one.
2. **[DESIGN.md](DESIGN.md)** — the canonical specification (tokens, type stack, rules, philosophy).
3. **[MEMORY.md](MEMORY.md)** — decision history and reasoning. Check before reversing a past choice.

## Fast facts

- **Brand red is `#cf142a`.** One value everywhere. `#D11D2B` is stale — fix it if you see it.
- **The symbol** (Laz Güneşi) source of truth is `laz-gunesi-amblem/svg/master.svg`. One symbol, all brands.
- **The favicon** canonical is `laz-gunesi-amblem/favicon/favicon.svg`; other `favicon.svg` files are mirrors.
- **This repo is platform-neutral.** Astro and Rails under `adapters/` are *adapters*, not the system.
- **Tokens are mirrored**, not imported. Editing `tokens/agustos.css` means updating its copies in the
  same change — see DESIGN.md §"Mirrored implementation".

## Rules

- Don't re-create an asset that already exists — check ASSETS.md first.
- If you add, move, or recolor a brand asset, **update ASSETS.md in the same change**.
- This system is the product of Emre Güneş's judgment; document non-obvious decisions in MEMORY.md.
