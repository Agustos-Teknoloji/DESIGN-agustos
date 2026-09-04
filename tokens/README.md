# Design tokens

`design-tokens.json` is the canonical cross-medium registry. It follows the Design Tokens Community Group shape (`$type`, `$value`, and `{alias.path}` references) while adding explicit semantic, theme, recipe, and compatibility sections needed by this system.

Edit:

- `design-tokens.json` for foundations, semantic roles, themes, and recipes.
- `../brand/brands.json` for per-brand identity values.
- `web.css.tmpl` for portable web behavior and compatibility classes.

Then run:

```bash
python3 scripts/build_design_system.py
python3 scripts/build_design_system.py --check
```

Generated files include `agustos.css`, `resolved.json`, `design-system-handoff.json`, `generated-manifest.json`, framework token CSS, and WordPress `theme.json`.

## Which artifact does another system need?

| You are… | Use | Why |
|---|---|---|
| Building a web UI in another repository | `ui/UI-KIT.md` | Ready-made CSS and classes. Nothing to translate. |
| Generating this system into a new medium (slides, native app, print) | `design-system-handoff.json` | The full contract: invariants, forbidden patterns, recipes, embedded symbol. |
| Writing a trusted generator inside this repository | `resolved.json` | Compact platform-neutral values, no contract prose. |

Picking `design-system-handoff.json` for a website is the common mistake: it makes the agent
re-derive CSS that `ui/agustos.css` already contains, and two agents deriving separately produce
two different buttons.

## Handoff to another coding system

Give the other system [`design-system-handoff.json`](design-system-handoff.json) when you need one portable, machine-readable file. It contains resolved tokens, brands, the exact embedded Laz Güneşi SVG plus its checksum, recipes, compatibility classes, invariants, forbidden patterns, medium translations, and acceptance checks.

That file is sufficient to establish the interface grammar and preserve the exact symbol. Exported outline lockups remain preferable when available; if an implementation cannot use the embedded SVG or the referenced lockup, it must request the asset rather than approximate it.

Consumer deployments vendor or attach the handoff file as context. They do not run this repository's generators. Regenerate CSS, Office, and brand exports only when the canonical tokens, brand registry, templates, or symbol change.

`resolved.json` remains the compact platform-neutral input for trusted generators such as Word and PowerPoint; the handoff file is the safer prompt/context artifact for a general coding system.
