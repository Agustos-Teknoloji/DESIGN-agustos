# Favicon and app-icon kit

Web-ready browser and OS icons. This folder is the **Ağustos** favicon, the canonical kit.
The tab icon is the red Laz Güneşi (`#cf142a`) on a transparent background.
Every other house brand uses the same symbol in black (`#15130f`), in `brand/exports/<brand>/favicon/`.
That set includes `banuucak`. Decision: MEMORY.md, 2026-10-15 transparent-tab-favicons.

Symbol: `#cf142a` on the tab icon. No background rectangle. The symbol paths are `../svg/master.svg`, verbatim.

## What is in the kit

| File | Size | Purpose |
|---|---|---|
| `favicon.svg` | vector | **Primary tab icon.** Transparent background, red symbol. Byte-identical to `brand/exports/agustos/favicon/favicon.svg`. |
| `favicon.ico` | 16/32/48 | Legacy fallback. Transparent background. |
| `favicon-32.png` | 32×32 | Optional PNG fallback. Transparent background. |
| `favicon-16.png` | 16×16 | Optional PNG fallback. Transparent background. |
| `apple-touch-icon.png` | 180×180 | iOS home-screen icon. **Solid white background.** |
| `icon-192.png` | 192×192 | Android / PWA. **Solid white background.** |
| `icon-512.png` | 512×512 | Android / PWA splash and install. **Solid white background.** |
| `site.webmanifest` | — | PWA manifest. `theme_color` is Ağustos red. `background_color` is white. |
| `favicon-mono.svg` | vector | The bare symbol, no crop (= `../svg/master.svg`). For in-page use next to text. Not a tab icon. |

iOS and Android fill a transparent icon with black. A black sun on that fill would vanish.
`apple-touch-icon.png` and the PWA icons (192 and 512) therefore keep a solid white background.
Emre can overrule this exception.

## Drop into any site `<head>`

Copy the icon files to your site's web root, then:

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

For a site of another brand, copy `brand/exports/<brand>/favicon/` instead. Its manifest names
`favicon-192.png` and `favicon-512.png`. Those two files, and `apple-touch-icon.png`, keep the white square.
`favicon.svg`, `favicon.ico`, `favicon-16.png` and `favicon-32.png` stay transparent.

The SVG is served to modern browsers. `.ico` is the universal fallback. If the icons live in a
subdirectory rather than the web root, adjust the `href`s and the `src` paths inside
`site.webmanifest` to match.

## Regenerating

Never edit these files by hand. From `brand/`:

```sh
../.venv/bin/python build.py --favicons
```

That rebuilds this folder and every `brand/exports/<brand>/favicon/`, and writes no other
export. Tab icons (`favicon.svg`, `favicon-16.png`, `favicon-32.png`, the PNGs up to 64px, `favicon.ico`) use a tight crop and a transparent background.
The viewBox is the master viewBox at 1/1.05 of its size, so the blades span about 94% of it and still
read at 16px. Large icons (the apple-touch icon, the manifest icons, 180px and up) keep a solid white
background and the master viewBox at 1/0.9, so the blades span about 81% and sit inside the maskable safe zone.
Only the background changes. The symbol paths stay verbatim.

`adapters/astro/public/favicon.svg` is the black transparent tab icon (`#15130f`), not this red kit.
The same command writes it. A site of Ağustos copies this folder.

See the repository root `ASSETS.md` for the canonical-source rules.
