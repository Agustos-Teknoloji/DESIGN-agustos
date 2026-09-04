# Adoption snippet

Paste the fenced block below into the consuming repository's `AGENTS.md`. Add a
one-line `CLAUDE.md` that points at `AGENTS.md` if the project does not have one.

Commit it once. Every coding agent that opens that repository afterwards picks up
the design system without anybody pasting a link again.

```markdown
## Design system — Ağustos UI kit (v3.1.0)

This project's UI is the Ağustos Design System. Before you write or change any markup, CSS, or
component, read `vendor/agustos-ui/UI-KIT.md`. If that file is absent, fetch
https://raw.githubusercontent.com/Agustos-Teknoloji/DESIGN-agustos/v3.1.0/ui/UI-KIT.md and follow it.

Use only its classes and CSS variables. Never retype a token value. Never invent a hex color.
Never restyle a kit class — compose instead. Brand red is `#cf142a`; `#D11D2B` is stale.
The `<body>` element must carry a `brand-*` class.

Before you call UI work done, run `python3 vendor/agustos-ui/check-agustos-ui.py .` and make it
exit 0.
```

## If the project does not vendor the kit

Replace the first paragraph with the CDN form. Keep the pinned version:

```markdown
This project's UI is the Ağustos Design System. Read https://raw.githubusercontent.com/Agustos-Teknoloji/DESIGN-agustos/v3.1.0/ui/UI-KIT.md before you write or
change any markup, CSS, or component. Load the kit with these two tags, fonts first:

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@v3.1.0/ui/agustos-fonts.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@v3.1.0/ui/agustos.css">
```

Never publish `@main` or `@latest` in a stylesheet URL. An unpinned link restyles the page the
moment a token changes upstream, with no review.
