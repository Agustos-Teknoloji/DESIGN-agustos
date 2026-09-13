# Favicon & app-icon kit

Web-ready browser/OS icons for every Ağustos house site. Artwork is the bare red
Laz Güneşi from `../svg/master.svg` — **one shared favicon**, not a per-brand tile.

Brand red: `#cf142a` · Ground: transparent.

## What's in the kit

| File | Size | Purpose |
|---|---|---|
| `favicon.svg` | vector | **Primary favicon.** Byte-identical to `../svg/master.svg`. |
| `favicon.ico` | 16/32/48 | Legacy fallback (older browsers, feed readers, crawlers). |
| `favicon-32.png` | 32×32 | Optional explicit PNG fallback. |
| `favicon-16.png` | 16×16 | Optional explicit PNG fallback. |
| `apple-touch-icon.png` | 180×180 | iOS home-screen icon. |
| `icon-192.png` | 192×192 | Android / PWA. |
| `icon-512.png` | 512×512 | Android / PWA splash + install. |
| `site.webmanifest` | — | PWA manifest. `theme_color` = brand red. |
| `favicon-mono.svg` | vector | Same artwork as `favicon.svg`. For in-page use next to text/UI. |

## Drop into any site `<head>`

Copy the icon files to your site's web root, then:

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

The SVG is served to modern browsers; `.ico` is the universal fallback. If the icons live in a
subdirectory rather than the web root, adjust the `href`s and the `src` paths inside
`site.webmanifest` to match.

## Regenerating

`favicon.svg` / `favicon-mono.svg` are copies of `../svg/master.svg`. To rebuild the rasters:

1. Copy `../svg/master.svg` over `favicon.svg` and `favicon-mono.svg`.
2. Render PNGs with the brand kit's resvg helper (`brand/scripts/render_png.mjs`) at 16, 32, 180, 192, and 512.
3. Build `favicon.ico` with Pillow from a 256px PNG (`sizes` 16/32/48).

`brand/build.py` regenerates every `brand/exports/<brand>/favicon/` from the same master.
Update adapter `public/favicon.svg` mirrors in the same change.

See the repository root `ASSETS.md` for the canonical-source + mirror rules.
