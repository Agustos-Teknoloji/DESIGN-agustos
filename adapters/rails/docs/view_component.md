# ViewComponent Option

The Rails adapter is intentionally plain ERB first. If a Rails app uses ViewComponent, the same partials can later become components without changing the design grammar.

Suggested component boundary:

```txt
app/components/agustos/brand_lockup_component.rb
app/components/agustos/sidebar_component.rb
app/components/agustos/hero_component.rb
app/components/agustos/card_grid_component.rb
```

Keep ViewComponent props semantic:

```ruby
Agustos::HeroComponent.new(
  eyebrow: "Ağustos",
  title: "Işığın mimariyle buluştuğu yer.",
  deck: "A calm, typographic hero.",
  primary_links: [{ label: "Aydınlatma", href: "/aydinlatma" }]
)
```

Avoid component props that expose raw style choices such as font size, color, or margins. Those belong to `tokens.css`.

