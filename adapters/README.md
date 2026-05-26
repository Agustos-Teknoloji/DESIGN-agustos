# Ağustos Adapters

Framework-specific implementations of the Ağustos Design System.

The design system itself is platform-neutral. Adapters translate the same tokens, layouts, and brand rules into the conventions of a framework.

## Current Adapters

- `rails/`: Rails monolith skeleton with CSS, helper, layout, and ERB partials.

## Existing Reference Implementation

The Astro reference implementation currently lives at `../astro/`. It remains there for local continuity and because it is already wired as a demo app. A future cleanup can move it to `adapters/astro/` once the path change can be done safely across local tooling and Git history.

