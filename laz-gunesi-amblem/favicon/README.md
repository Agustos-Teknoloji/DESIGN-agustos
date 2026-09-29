# Favicon & app-icon kit

Web-ready browser/OS icons. This folder is the **Ağustos** favicon, the canonical kit: the red
Laz Güneşi on a white square tile. Every other house brand has the same tile with a black
(`#15130f`) Laz Güneşi in `brand/exports/<brand>/favicon/` (MEMORY.md 2026-09-29
per-brand-favicons).

Symbol: `#cf142a` · Tile: `#ffffff` · The symbol paths are `../svg/master.svg`, verbatim.

## What's in the kit

| File | Size | Purpose |
|---|---|---|
| `favicon.svg` | vector | **Primary favicon.** White tile, red symbol. Byte-identical to `brand/exports/agustos/favicon/favicon.svg`. |
| `favicon.ico` | 16/32/48 | Legacy fallback (older browsers, feed readers, crawlers). |
| `favicon-32.png` | 32×32 | Optional explicit PNG fallback. |
| `favicon-16.png` | 16×16 | Optional explicit PNG fallback. |
| `apple-touch-icon.png` | 180×180 | iOS home-screen icon (full white square). |
| `icon-192.png` | 192×192 | Android / PWA. |
| `icon-512.png` | 512×512 | Android / PWA splash + install. |
| `site.webmanifest` | — | PWA manifest. `theme_color` = Ağustos red, `background_color` = white. |
| `favicon-mono.svg` | vector | The bare symbol, no tile (= `../svg/master.svg`). For in-page use next to text/UI, not as a tab icon. |

## Drop into any site `<head>`

Copy the icon files to your site's web root, then:

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

For a site of another brand, copy `brand/exports/<brand>/favicon/` instead; its manifest names
`favicon-192.png` and `favicon-512.png`.

The SVG is served to modern browsers; `.ico` is the universal fallback. If the icons live in a
subdirectory rather than the web root, adjust the `href`s and the `src` paths inside
`site.webmanifest` to match.

## Regenerating

Never edit these files by hand. From `brand/`:

```sh
../.venv/bin/python build.py --favicons
```

That rebuilds this folder and every `brand/exports/<brand>/favicon/`, and writes no other
export. The tile is the master viewBox grown to 1/0.9 of its size, so the blades span about
80% of the tile: legible at 16px and inside the maskable safe zone.
Update adapter `public/favicon.svg` mirrors in the same change.

See the repository root `ASSETS.md` for the canonical-source + mirror rules.
