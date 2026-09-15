# Product UI kit — IESDesk

The **product-UI** surface of the Ağustos system, the inverse of the website kit: **white substrate** always (no cream — that band is marketing-site-only), an opt-in **warm dark** theme, and no brand hue to ration. IESDesk reads, validates, and converts IES/LDT photometric files at scale; this kit mocks its validation dashboard.

Open **`index.html`** to run it. Toggle **Light/Dark** in the sidebar foot.

## What's here

| File | Role |
|---|---|
| `index.html` | Shell + the **Product UI** starting point. Loads React + Babel, `styles.css`, `pq.css`, the bundle, then the JSX. |
| `app.jsx` | `PqApp` — holds view + theme state, applies `.brand-iesdesk` to the shell and `data-theme="dark"` to `<html>`. |
| `sidebar.jsx` | `PqSidebar` — `Lockup` (iesdesk) + functional nav with counts, local-cache meter, theme toggle. |
| `dashboard.jsx` | `PqDashboard` — topbar, processing band, stat tiles, and the validation table with status pills. |
| `pq.css` | Layout shell only. No type or color literals; tokens + `.type-*` throughout. |

## How it stays on-system

- **No brand hue to spend.** Under the v3 rules only the publisher (Ağustos) mark is red — every other brand, IESDesk included, is the one off-black. So this kit has nothing to "ration": accents are expressed with **ink fills** (active nav, progress/cache fills, the Export button) and the **light-gray functional surface** `--surface` (the featured "Valid" stat tile, the table header row) — never colour, and never red (red stays reserved for content links and menu-hover, neither of which exist in this dense product surface).
- **Status is text-led, never colour-alone.** `✓ Valid` is the one solid-ink pill; `⚠ Flagged` / `✕ Error` / `– Skipped` are differentiated by **glyph + label + border weight**, all in ink.
- **No uppercase anywhere.** Table headers, filters, and the breadcrumb are sentence case with normal tracking — the v3 rule applies inside product UI too, not just the marketing site.
- **One button size, no arrow.** `Button` is always 44px min height; there's no `size` or `arrow` prop anymore. `variant="brand"` (filled red) is reserved for a dark-theme hero CTA and never appears here.
- **Dashboard numerals.** Stat values and table figures use the display family with **tabular figures** (`font-variant-numeric: tabular-nums`).
- **Technical identifiers are mono.** Filenames, formats, counts, and the breadcrumb use JetBrains Mono.
- **Restraint over chrome.** Hairline rules, 6/10px radii, no shadows, no colored surface fills beyond the one functional gray.

## Extending

- **Data:** `STATS` and `ROWS` live in `dashboard.jsx`; `NAV` lives in `sidebar.jsx`.
- **New panel:** add a component, export it to `window`, drop it into `PqDashboard`'s scroll area. Use the spacing scale and `.type-*` tokens; never introduce raw color or font values, and never reach for red on a stat, figure, or fill.
