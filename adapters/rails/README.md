# Ağustos Rails Adapter v3.0.0

Plain-ERB, Hotwire-compatible implementation of the Ağustos Design System. The
adapter matches the Astro topbar/footer grammar without depending on Astro or a
client-side search data protocol.

## Install Manually

Copy the adapter surfaces into the equivalent Rails directories:

```txt
app/assets/stylesheets/agustos/
app/helpers/agustos_theme_helper.rb
app/views/layouts/agustos.html.erb
app/views/agustos/shared/
app/javascript/controllers/agustos_*_controller.js
```

Import the two stylesheets and register the three Stimulus controllers using the
same mechanism as the host application. The live search option requires Turbo;
navigation and theme remain ordinary HTML controls enhanced by Stimulus.

Use the layout from a controller:

```ruby
class ApplicationController < ActionController::Base
  layout "agustos"
end
```

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
    cta: { label: "Contact", href: contact_path },
    language_switch: { code: "TR", label: "Türkçe", href: tr_root_path },
    search: { url: search_path, param: :q },
    footer: {
      description: "Pataraz · project-grade lighting",
      columns: [
        { heading: "Company", links: [{ label: "About", href: about_path }] }
      ]
    }
  )
end
```

`cta`, `language_switch`, and `search` may be `nil`. Links accept `aria_label`
and `external: true`; external links receive `_blank` plus
`noopener noreferrer`. Active navigation uses exact matching for `/` and prefix
matching for nested sections.

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
