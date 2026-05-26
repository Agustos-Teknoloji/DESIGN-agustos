# Ağustos Rails Adapter

Rails implementation skeleton for the Ağustos Design System.

This adapter is intended for Rails monoliths that want the typography, brand, substrate, and layout grammar from `DESIGN.md` without depending on Astro.

## Install Manually

Copy these files into a Rails app:

```txt
app/assets/stylesheets/agustos/tokens.css
app/assets/stylesheets/agustos/components.css
app/helpers/agustos_theme_helper.rb
app/views/layouts/agustos.html.erb
app/views/agustos/shared/_brand_lockup.html.erb
app/views/agustos/shared/_sidebar.html.erb
```

Then import the styles from your app stylesheet:

```css
@import "agustos/tokens";
@import "agustos/components";
```

With Propshaft, keep the files under `app/assets/stylesheets/agustos/`. With cssbundling-rails, import them from your bundled entrypoint instead.

## Layout Usage

Use the layout from a controller:

```ruby
class ApplicationController < ActionController::Base
  layout "agustos"
end
```

Set brand, language, and substrate per controller or action:

```ruby
before_action do
  agustos_theme brand: :agustos, lang: :tr, substrate: :cream
end
```

## Design Rule

The Rails adapter should not invent a separate visual system. It consumes the same tokens as Astro and `WEBSITE-agustos`; Rails-specific files should only handle layout, helpers, partials, and framework ergonomics.

