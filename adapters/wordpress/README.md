# Ağustos WordPress Adapter

This adapter translates Ağustos Design System v3 into WordPress Global Styles. It is an adapter, not a complete theme.

Copy `theme.json` to a block theme root and `assets/css/agustos.css` to the theme assets directory. Merge `functions.php.example` into the theme bootstrap to enqueue the generated behavior and recipe layer.

Both generated files come from `tokens/design-tokens.json`; never edit them directly:

```bash
python3 scripts/build_design_system.py
python3 scripts/build_design_system.py --check
```

Use WordPress blocks for native authoring. Apply the shared recipe classes (`agustos-section`, `agustos-card-grid`, `agustos-card`, `agustos-chrome-link`) only where Global Styles cannot express the intended composition.

Set the site brand on the body or a wrapping block with `brand-agustos`, `brand-pataraz`, `brand-pld`, or `brand-photo`. Add `paper-white` for the white working substrate.
