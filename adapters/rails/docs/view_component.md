# ViewComponent Option

The Rails adapter is intentionally plain ERB first. If a Rails app uses ViewComponent, the same partials can later become components without changing the design grammar.

Suggested component boundary:

```txt
app/components/agustos/brand_lockup_component.rb
app/components/agustos/header_component.rb
app/components/agustos/footer_component.rb
app/components/agustos/sidebar_component.rb      # product UI only
app/components/agustos/search_results_component.rb
app/components/agustos/hero_component.rb
app/components/agustos/card_grid_component.rb
```

Keep ViewComponent props semantic:

```ruby
Agustos::HeroComponent.new(
  title: "Işığın mimariyle buluştuğu yer.",
  highlight: "mimariyle",          # one to four words of the title, once per page
  deck: "A calm, typographic hero.",
  primary: { label: "Aydınlatma", href: "/aydinlatma" },
  secondary: { label: "Danışmanlık", href: "/danismanlik" },
  trust: "12 aydınlatma markası · 2 kurumsal yazılım"
)

Agustos::HeaderComponent.new(nav: nav_items, more_label: "Daha fazla", cta: { label: "İletişim", href: "/iletisim" })
Agustos::FooterComponent.new(note: "© Ağustos Teknoloji, 1996–2026", links: footer_links)
```

The hero renders `hero-actions` with one `agustos-button--primary` and one
`agustos-button--secondary`. The header keeps the five-item rule of the ERB
partial: more than five items render the first four and put the rest under
one `site-header__more`. The footer takes a `note` and one flat `links` list,
with no columns and no button. The sidebar component belongs to product UI
(`shell: :product`) only; chrome follows the screen family, never the brand.

Avoid component props that expose raw style choices such as font size, color, or margins. Those belong to `tokens.css`.

Keep search results server-rendered. A ViewComponent replacement should accept
the same `frame_id`, `query`, `status`, and `groups` locals documented by the ERB
partial so controllers do not change when presentation is upgraded.
