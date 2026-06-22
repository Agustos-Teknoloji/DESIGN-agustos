# Favicon & app-icon kit

Web-ready browser/OS icons for the Ağustos brand, derived from the Laz Güneşi symbol
(`../svg/master.svg`). This is the **negative expression** from DESIGN.md §"Three expressions":
the white symbol on a brand-red tile — the documented favicon treatment, chosen because a solid
tile keeps its brand color and silhouette at 16px where the bare symbol's thin blades wash out.

Brand red: `#cf142a` · Tile corner radius: 20/100 (rounded square).

## What's in the kit

| File | Size | Purpose |
|---|---|---|
| `favicon.svg` | vector | **Primary favicon.** Modern browsers. Rounded red tile, white sun, real transparency. |
| `favicon.ico` | 16/32/48 | Legacy fallback (older browsers, feed readers, crawlers). Square, opaque. |
| `favicon-32.png` | 32×32 | Optional explicit PNG fallback. Square, opaque. |
| `favicon-16.png` | 16×16 | Optional explicit PNG fallback. Square, opaque. |
| `apple-touch-icon.png` | 180×180 | iOS home-screen icon. Full-bleed (iOS applies its own rounded mask). |
| `icon-192.png` | 192×192 | Android / PWA. Maskable-safe padding. |
| `icon-512.png` | 512×512 | Android / PWA splash + install. Maskable-safe padding. |
| `site.webmanifest` | — | PWA manifest. `theme_color` = brand red, `background_color` = cream. |
| `favicon-mono.svg` | vector | Bare red symbol on transparent. For **in-page** use (next to text/UI), **not** the browser tab. |

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

The two SVGs are the source of truth. To rebuild the rasters (macOS):

- PNGs: render with `qlmanage -t -s <px>` then normalize size with `sips -z <px> <px>`.
  Browser/legacy fallbacks (`favicon-*.png`, `favicon.ico`) come from a **full-bleed square**
  render (opaque — no transparent corners to leak white on dark chrome); Apple/PWA icons come
  from the same square (the OS rounds them).
- `.ico`: assemble with Pillow — open the largest PNG as base and `append_images` the smaller
  ones, so all of 16/32/48 are embedded (Pillow will not upscale a small base).

See the repository root `ASSETS.md` for the canonical-source + mirror rules.
