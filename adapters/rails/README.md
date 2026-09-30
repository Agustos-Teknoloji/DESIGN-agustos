# Ağustos Rails Adapter (kit v7.0.0)

Plain-ERB, Hotwire-compatible implementation of the Ağustos Design System. The
adapter matches the Astro top menu and footer grammar without depending on Astro
or a client-side search data protocol.

Chrome follows the screen family, not the brand. Website pages (the default
`shell: :marketing`) render the top menu and the footer for every brand.
Product UI (`shell: :product`) alone renders the kit sidebar and puts
`site-sidebar-layout` on `<body>`. No brand registers chrome.

> Building a UI in a repository that is not one of these adapters? Use the distribution kit
> at [`ui/UI-KIT.md`](../../ui/UI-KIT.md) instead — it needs no framework integration.

## Install Manually

Copy the adapter surfaces into the equivalent Rails directories:

```txt
app/assets/stylesheets/agustos/
app/helpers/agustos_theme_helper.rb
app/views/layouts/agustos.html.erb
app/views/agustos/shared/
app/javascript/controllers/agustos_*_controller.js
```

Import `agustos/tokens` and `agustos/components`; the kit styles both the
website chrome and the product sidebar, so product UI needs no extra
stylesheet. Register the Stimulus controllers
using the same mechanism as the host application. Load fonts first. Copy
`ui/agustos-fonts.css` and `ui/fonts/` (or install the `@fontsource-variable`
packages). The live search option requires Turbo. The header drawer is a
native popover styled by the kit, and so is the product sidebar drawer; the
More menu is a native `details`. The adapter ships search and theme
controllers only.

Use the layout from a controller:

```ruby
class ApplicationController < ActionController::Base
  layout "agustos"
end
```

Static previews (no Rails process). Serve from the repository root so font files resolve:

```bash
python3 -m http.server 4332
```

Then open `/adapters/rails/preview/marketing.html` and `/adapters/rails/preview/product-ui.html`.

## Chrome Configuration

`agustos_theme` accepts brand and page metadata plus semantic chrome hashes:

```ruby
before_action do
  agustos_theme(
    brand: :pataraz,
    lang: :tr,
    substrate: :white,
    screen: :products,
    home_href: root_path,
    nav: [
      { label: "Ürünler", href: products_path },
      { label: "Ürün bul", href: finder_path },
      { label: "Seriler", href: series_path },
      { label: "Projeler", href: projects_path },
      { label: "Hakkında", href: about_path },
      { label: "Kariyer", href: careers_path }
    ],
    more_label: "Daha fazla",
    cta: { label: "Fiyat isteyin", href: contact_path },
    language_switch: { code: "EN", label: "English", href: en_root_path, hreflang: "en" },
    search: { url: search_path, param: :q },
    footer: {
      note: "© Pataraz, 2026",
      links: [
        { label: "LinkedIn", href: "https://www.linkedin.com/company/pataraz/", external: true },
        { label: "Gizlilik ve KVKK", href: privacy_path },
        { label: "English", href: en_root_path, hreflang: "en" }
      ]
    }
  )
end
```

`screen` names the kit screen this page is (`home`, `static`, `content`,
`content-index`, `products`, `product-finder`, `product`, `spec-sheet`,
`app-shell`) and renders as `data-screen` on `<body>`. The kit checker holds the
page to that screen's row: the highlighter once, the sidebar only on product
UI, `data-theme` only on product UI. Product UI defaults to `app-shell`; every
website page must set its own, or the checker reports it.

**Top menu (`nav`).** At most five items. With more than five, the header keeps
the first four as `site-header__link` and moves the rest into one
`<details class="site-header__more">`, the last child of `site-header__nav`:
its `summary` reads `more_label` (default "Daha fazla" for `lang: :tr`, "More"
otherwise) and its `site-header__more-menu` holds `site-header__more-link`
items. The current page gets `aria-current="page"` in the menu or under More:
exact matching for `/`, prefix matching for nested sections, and `current:
true` on an item forces it. `agustos_nav_split` returns `[menu, more]` for a
custom header.

**Footer (`footer`).** `note` is the one `type-footnote` line under the lockup.
`links` is one flat list for social, legal, and language, each with `label`,
`href`, and optional `external`, `aria_label`, and `hreflang`; `aria_label` on
the footer hash names its nav (default "Alt menü" / "Footer"). The footer has
no column headings, no repeat of the top menu, and no button. v7 removed
`description`, `columns`, and the footer `cta`; move a footer description into
`note` and flatten column links into `links`, keeping only social, legal, and
language destinations.

`cta`, `language_switch`, and `search` may be `nil`. Links accept `aria_label`,
`hreflang`, and `external: true`; external links receive `_blank` plus
`noopener noreferrer`.

Websites ship light and carry no theme toggle. Product UI uses the app shell
(`shell: :product`): the layout renders `agustos/shared/sidebar`
(`site-sidebar-bar` with the burger below 1024px, then `site-sidebar` with the
lockup, `site-sidebar__nav`, an optional dark control in
`site-sidebar__utility`, and a `site-sidebar__note`):

```ruby
agustos_theme(
  brand: :iesdesk,
  shell: :product,
  theme: true,
  screen: :app_shell,
  sidebar: {
    nav: [
      { label: "Batches", href: batches_path, badge: "6" },
      { label: "Validation", href: validation_path, badge: "157", badge_tone: :warning }
    ],
    note: "Local cache 1.8 / 4 GB. Files never leave this machine."
  }
)
```

Sidebar items take `label`, `href`, optional `badge` and `badge_tone`
(`success`, `warning`, `danger`, `info`), and `current`.

## Composition

Copy the matching screen from `screens/`. A website page opens with a
`type-hero` headline, a `type-hero-deck`, a `<div class="hero-actions">` with
one `agustos-button agustos-button--primary` and one
`agustos-button agustos-button--secondary`, and a `hero-trust` line. Wrap one to
four words of the main headline in `<mark class="type-highlight">`, once per
page. Close with one `band band--cream`. Do not put a primary button in
intervening sections. Buttons are black; never add a red button style. The
retired `hero-action*` and `hero-link*` classes are gone.

Photographs roll out in this order: product page, listing thumbnail, homepage
installation. Type-only pages stay complete. Quotes belong on content pages
only. Marketing uses a compact trust line.

See `app/views/agustos/examples/show.html.erb` for marketing and
`app/views/agustos/examples/product.html.erb` for the IESDesk validation-run
product UI, built after `screens/app-shell.html`. Product UI does not use the
website header or footer, and websites never use the sidebar.

## Turbo Search Contract

The header submits a debounced GET request after two characters into a unique
Turbo Frame. The endpoint owns querying and renders the supplied structural
partial; no JSON endpoint or ActionCable channel is required.

```ruby
def index
  query = params[:q].to_s.strip
  groups = Search.new(query).groups

  render partial: "agustos/shared/search_results", locals: {
    frame_id: params.require(:frame_id),
    query: query,
    status: "#{groups.sum { |group| group[:items].size }} results",
    groups: groups
  }
end
```

Each group has `heading`, optional `total`, and `items`. Each item has `href`,
`title`, and optional `excerpt`; excerpts are sanitized to allow only `<mark>`.
Without JavaScript, a `<noscript>` form performs a normal GET navigation. The
endpoint can render a complete search page for that request while using the
shared result partial for Turbo Frame requests:

```ruby
if turbo_frame_request?
  render partial: "agustos/shared/search_results", locals: result_locals
else
  render :index, locals: { query: query, groups: groups }
end
```

## Verification

Run the dependency-free adapter contract tests:

```bash
ruby test/adapter_contract_test.rb
```

The Rails adapter should not invent a separate visual system. Framework files
handle layout, configuration, partial rendering, Turbo, and Stimulus. Shared
visual primitives are generated from `tokens/design-tokens.json`; verify drift
from the repository root with `python3 scripts/build_design_system.py --check`.

Applications using ViewComponent can follow the semantic component boundaries in
[`docs/view_component.md`](docs/view_component.md) without changing the ERB search contract.
