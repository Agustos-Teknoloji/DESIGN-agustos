# Ağustos Rails Adapter v5.0.1

Plain-ERB, Hotwire-compatible implementation of the Ağustos Design System. The
adapter matches the Astro topbar/footer grammar without depending on Astro or a
client-side search data protocol.

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

Import `agustos/tokens` and `agustos/components`. Product pages also load
`agustos/product` when `shell: :product`. Register the Stimulus controllers
using the same mechanism as the host application. Load fonts first. Copy
`ui/agustos-fonts.css` and `ui/fonts/` (or install the `@fontsource-variable`
packages). The live search option requires Turbo. Navigation and theme remain
ordinary HTML controls enhanced by Stimulus.

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
    lang: :en,
    substrate: :white,
    home_href: root_path,
    nav: [
      { label: "Products", href: products_path },
      { label: "About", href: about_path }
    ],
    cta: { label: "Request pricing", href: contact_path },
    language_switch: { code: "TR", label: "Türkçe", href: tr_root_path },
    search: { url: search_path, param: :q },
    footer: {
      description: "Pataraz · project-grade lighting",
      columns: [
        { heading: "Company", links: [{ label: "About", href: about_path }] }
      ],
      cta: { label: "Contact", href: contact_path }
    }
  )
end
```

`cta`, `language_switch`, and `search` may be `nil`. Links accept `aria_label`
and `external: true`; external links receive `_blank` plus
`noopener noreferrer`. Active navigation uses exact matching for `/` and prefix
matching for nested sections.

Marketing headers do not include a theme toggle. Product UI uses a separate
app shell (`shell: :product`). It ships on white paper with an opt-in dark
control in the sidebar:

```ruby
agustos_theme(
  brand: :iesdesk,
  shell: :product,
  theme: true
)
```

## Composition

Name one committing destination per page. That destination may appear in the
header, the opening, and one closing cream band. Do not put a primary button in
intervening sections. Footer Contact is separate chrome.

Photographs roll out in this order: product page, listing thumbnail, homepage
installation. Type-only pages stay complete. Quotes belong on content pages
only. Marketing uses a compact trust line.

See `app/views/agustos/examples/show.html.erb` for marketing and
`app/views/agustos/examples/product.html.erb` for the IESDesk validation-run
product UI. Product UI does not use the marketing header or footer.

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
