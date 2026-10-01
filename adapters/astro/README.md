# Ağustos Astro Adapter

Astro 5 reference implementation for the [Ağustos Design System](../../DESIGN.md), kit v7.6.0.

This adapter is useful for static sites, documentation, marketing pages, and visual QA. It is not the canonical center of the system; shared decisions live in `../../tokens/design-tokens.json` and `DESIGN.md`.

> Building a UI in a repository that is not one of these adapters? Use the distribution kit
> at [`ui/UI-KIT.md`](../../ui/UI-KIT.md) instead — it needs no framework integration.

## What's Inside

```txt
adapters/astro/
├── astro.config.mjs
├── package.json
├── public/favicon.svg
├── scripts/render-design-html.mjs
└── src/
    ├── components/
    │   ├── BrandLockup.astro
    │   ├── Footer.astro
    │   ├── Header.astro
    │   ├── HeaderSearch.astro
    │   ├── HeaderUtility.astro
    │   └── LazGunesi.astro
    ├── types/chrome.ts
    ├── content/blog/
    ├── layouts/BaseLayout.astro
    ├── pages/
    │   ├── index.astro
    │   ├── about.astro
    │   ├── typography.astro
    │   └── blog/
    └── styles/tokens.css
```

## Run It

```bash
npm install
npm run dev
```

Build and preview:

```bash
npm run build
npm run preview
```

The production build runs Pagefind after Astro and verifies that the generated
index can be queried with the header's language and page/post filters.

## Chrome Configuration

Chrome follows the screen family, not the brand. `BaseLayout` renders website
chrome, the top menu and the footer, for every brand and every website screen
(`home`, `static`, `content`, `content-index`, `products`, `product-finder`,
`product`, `spec-sheet`). It never renders the sidebar: that belongs to product
UI (`app-shell`), which this adapter does not ship.

`BaseLayout` accepts semantic `header` and `footer` configuration. Destinations
and copy are consumer data; spacing, states, responsive behavior, and typography
belong to the kit.

```astro
<BaseLayout
  title="Pataraz"
  brand="pataraz"
  lang="tr"
  screen="home"
  header={{
    homeHref: '/',
    nav: [
      { href: '/urunler', label: 'Ürünler' },
      { href: '/urun-bul', label: 'Ürün bul' },
      { href: '/seriler', label: 'Seriler' },
      { href: '/projeler', label: 'Projeler' },
      { href: '/hakkinda', label: 'Hakkında' },
      { href: '/kariyer', label: 'Kariyer' },
    ],
    moreLabel: 'Daha fazla',
    cta: { href: '/iletisim', label: 'Fiyat isteyin' },
    languageSwitch: { href: '/en', label: 'English', code: 'EN', hreflang: 'en' },
  }}
  footer={{
    note: '© Pataraz, 2026',
    links: [
      { href: 'https://www.linkedin.com/company/pataraz/', label: 'LinkedIn', external: true },
      { href: '/gizlilik', label: 'Gizlilik ve KVKK' },
      { href: '/en', label: 'English', hreflang: 'en' },
    ],
  }}
>
  ...
</BaseLayout>
```

**Header.** `nav` is the top menu. It shows at most five items. With more than
five, the header renders the first four as `site-header__link` and puts the
rest in one `<details class="site-header__more">` as the last child of
`site-header__nav`, whose `summary` reads `moreLabel` (default "Daha fazla" for
`lang="tr"`, "More" otherwise) and whose `site-header__more-menu` holds
`site-header__more-link` items. The current page gets `aria-current="page"`, in
the menu or under More; on a nested route, the parent section gets
`aria-current="true"` (`currentState()` in `src/types/chrome.ts`; trailing
slashes do not count, and `/` is only ever exact). `cta` (default "Start a project"; `null` removes it) is
the one header button; `languageSwitch` and search sit in `site-header__end`.

**Footer.** `note` is the one `type-footnote` line under the lockup. `links` is
one flat list of `{ href, label, external?, ariaLabel?, hreflang? }` for social,
legal, and language, rendered as one row of `site-footer__link` items;
`ariaLabel` names the footer nav (default "Alt menü" / "Footer"). The optional
site map (v7.1.0) sits above that row: `address` is the lines of the contact
block (legal name and address), `contact` is its phone and email links, and
`groups` is at most three
`{ title, links }` of at most five links each, the pages people look for. With
a site map the lockup moves into the contact block. There is no footer button;
`description`, `columns`, and the footer `cta` were removed in v7.

External links (`external: true`) open in a new tab with `noopener noreferrer`.

Set `searchable={false}` to exclude a page. Blog detail pages should pass
`searchKind="post"`; other pages default to `"page"`. Set
`header={{ search: false }}` to remove search from the chrome.

Websites ship light and carry no theme toggle. `header={{ theme: true }}` and
`theme="dark"` remain for inspecting product-UI dark (the typography showcase
uses the toggle); do not use them on a website page.

The header drawer and its backdrop are native popovers styled by the kit, with
a close button inside the drawer. The header script imports the kit's
`src/scripts/agustos-chrome.js` (generated; do not edit), which closes the More
menu on Escape, an outside click or focus leaving, and handles search and the
optional theme toggle. A language link carries `lang` from its `hreflang`.

Regenerate the standalone HTML preview from `DESIGN.md`:

```bash
node scripts/render-design-html.mjs
```

## Token Generation

The Astro token file is generated alongside every other web adapter:

```txt
../../tokens/design-tokens.json
src/styles/tokens.css
```

Run `python3 scripts/build_design_system.py` from the repository root. The local gate, `scripts/ci.sh`, uses `--check` to reject drift.

## Brands

Every page can declare one of five brands via `BaseLayout`. The brand sets the
identity ink and the wordmark; it does not pick the chrome.

```astro
<BaseLayout brand="pataraz" title="Pataraz">
  ...
</BaseLayout>
```

Available brand ids:

- `agustos`
- `pataraz`
- `pld`
- `iesdesk`
- `specquick`

## Substrates and theme

White is the page paper. The pale red closing band is the kit's `band band--cream`, once per page, not a page substrate.

```astro
<section class="band band--cream">
  <div class="site-frame">...</div>
</section>
```

Dark theme is for product UI through `html[data-theme="dark"]`. Marketing, catalog, and spec pages stay light. They do not ship a theme toggle. The typography showcase includes a handbook inspect control; that is not a marketing pattern.

## Composition

Copy the matching screen from `screens/` instead of designing a page. A website page opens with a `type-hero` headline (or `type-h1` on listing and content pages), a `type-hero-deck`, a `<div class="hero-actions">` with one `agustos-button agustos-button--primary` and one `agustos-button agustos-button--secondary`, and a `hero-trust` line. Wrap one to four words of the main headline in `<mark class="type-highlight">`, once per page. It closes with one `band band--cream`. Do not put a primary button in intervening sections. Buttons are black; never style a red button. The retired `hero-links`, `hero-link*`, and `hero-action*` classes are gone.

Photographs roll out in this order: product page, listing thumbnail, homepage installation. Type-only pages stay complete. Quotes belong on content pages only. Marketing uses a compact trust line.

## Turkish Locale

Set `lang="tr"` for Turkish pages:

```astro
<BaseLayout lang="tr" title="Ağustos">
  ...
</BaseLayout>
```

The design system depends on `lang="tr"` plus `font-feature-settings: "locl"` for correct Turkish uppercase behavior.

## Scope

This adapter demonstrates the v7.0.0 type tokens, the website chrome (top menu with More, simple footer), shared frame, the hero with one highlighter and two buttons, the closing band, restrained card groups, and section rhythm. Rails monoliths should use `../rails/` instead of copying Astro components.
