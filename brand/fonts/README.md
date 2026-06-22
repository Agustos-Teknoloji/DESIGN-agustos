# Brand Fonts

The three families of the Ağustos Design System, vendored here so anyone can install
them before opening a template or building a document. All three are free and
open-source under the SIL Open Font License (OFL) — see each `OFL.txt`.

| Folder | Family | Role | Used at |
|---|---|---|---|
| `inter-tight/` | Inter Tight | Display — logo, headings, UI labels | Semibold (650) for the wordmark |
| `inter/` | Inter | Body — paragraphs, captions, tables | 400 / 700 |
| `jetbrains-mono/` | JetBrains Mono | Monospace — code, data | 400 |

These are **variable** fonts: one file covers every weight from 100–900. Roman and
Italic ship separately.

## Install (do this before opening any office template)

- **macOS** — select all `.ttf` files → right-click → *Open* → *Install Font* (Font Book).
- **Windows** — select all `.ttf` files → right-click → *Install for all users*.
- **Google Workspace** — Inter and Inter Tight are available directly in the Docs/Slides
  font picker (Inter Tight via *More fonts*); no install needed.

## Why these are bundled, not just linked

A brand kit should work offline and on any machine. The website self-hosts these via
`@fontsource-variable/*`, but a colleague making a slide deck or a printer setting a
business card needs the actual files — so they live here.

## Source

Fetched from the official Google Fonts repository (`github.com/google/fonts`, OFL).
To refresh, re-download `InterTight[wght].ttf`, `Inter[opsz,wght].ttf`, and
`JetBrainsMono[wght].ttf` (plus their Italic and `OFL.txt` files).
