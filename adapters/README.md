# Ağustos Adapters

Framework-specific implementations of the Ağustos Design System, kit v7.14.0.

The design system itself is platform-neutral. Adapters translate the same tokens, layouts, and brand rules into the conventions of a framework.

> Building a UI in a repository that is not one of these adapters? Use the distribution kit
> at [`ui/UI-KIT.md`](../ui/UI-KIT.md) instead — it needs no framework integration.

## Chrome follows the screen family

Every adapter picks chrome by the kind of page, never by the brand:

- **Websites** (marketing, content, catalog, document screens) use the top menu (`site-header*`) and the footer (`site-footer*`), for every house brand.
- **Product UI** (the `app-shell` screen) alone uses the sidebar (`site-sidebar*`, with `site-sidebar-layout` on `<body>`).

The top menu shows at most five items. When the nav config holds more than five, the adapters render the first four as links and put the rest in one `site-header__more` menu ("Daha fazla" in Turkish, "More" in English; the label is configurable). The footer takes one `note` line and one flat list of `links` for social, legal, and language, and no button. An optional site map sits above it: `address` lines, `contact` links (phone, email) and at most three `groups` of at most five links. Every site also publishes `sitemap.xml`: Astro `@astrojs/sitemap`, WordPress core `wp-sitemap.xml`, Rails `sitemap_generator`.

## Current Adapters

- `astro/`: Astro reference implementation and typography showcase (websites).
- `rails/`: Rails monolith skeleton with the website chrome, a marketing example, and a product UI example on the kit sidebar.
- `wordpress/`: Global Styles (`theme.json`) and the generated kit CSS for a block theme.
