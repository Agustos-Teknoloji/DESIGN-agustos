# Ağustos design system agent notes

This repository is the source of the Ağustos design system: the token registry, the `ui/` kit that apps vendor, its checker, and the brand assets of every house brand.
agustos.com is the reference implementation; this repository is authoritative. Use the router, and read only the files that your task needs.

## Ops baseline (generated from CONTEXT-agustos/ops/fleet.md, do not edit by hand)
- Role: source of the house-kit tier. Apps vendor a tagged release.
- CI: pre-push hook
- Fleet rules: `ops/AGENTS.md` in the `CONTEXT-agustos` repo (`~/vaults/business/PROJECTS/CONTEXT-agustos` on Emre's Mac)
- If a local rule conflicts with ops, stop and ask Emre.

## Source priority

When two files disagree, the first file in this list wins:

1. `tokens/design-tokens.json` and `brand/brands.json`
2. `DESIGN.md`
3. `ui/UI-KIT.md` (generated from the registry)
4. `MEMORY.md`
5. `archive/MEMORY.md`

A measured live site beats any doc on what ships. Flag the drift, and fix the doc in the same change.

## Router

| Task | Start here | Read next only if needed |
|---|---|---|
| Set up, generate and verify | [README.md](README.md) | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Understand the structure, or write and run tests | [ARCHITECTURE.md](ARCHITECTURE.md) | `scripts/ci.sh`, the local gate that the pre-push hook runs |
| **Build a UI in another repository** (Astro, WordPress, Rails, plain HTML) | **[ui/UI-KIT.md](ui/UI-KIT.md)**, then the matching `screens/<name>.html` | [docs/web.html](docs/web.html) for every screen with its rules, then [DESIGN.md](DESIGN.md) |
| Change tokens or web recipes | `tokens/design-tokens.json` and `tokens/web.css.tmpl` | [docs/what-generates.html](docs/what-generates.html) for what a change regenerates |
| Add or change a screen (home, static, content, content-index, products, product-finder, product, spec-sheet, app-shell) | `screens/<name>.html` and the `screens` table in `tokens/design-tokens.json` | [screens/README.md](screens/README.md), then the build and `/design-push` |
| Change or add a brand | [brand/README.md](brand/README.md) and `brand/brands.json` | The build. Run the full `brand/build.py` only if asked. |
| Find a logo, favicon, social image, document or other finished asset | [ASSETS.md](ASSETS.md) | `brand/exports/<brand>/`, and the "I need" table below |
| Build a Pataraz website or datasheet | [PATARAZ.md](PATARAZ.md) | [DESIGN.md](DESIGN.md), then the export or generator README |
| **Share this system as a zip** | **[docs/handoff-setup.html](docs/handoff-setup.html)**, then `python3 scripts/pack_handoff.py` | [HANDOFF.md](HANDOFF.md). Do not zip the whole repository. |
| **Push the kit, chrome and screens to Claude Design** (after a token, kit, favicon, logo or screen change) | **[docs/claude-design-sync.html](docs/claude-design-sync.html)**, then `/design-push` in Claude Code | [.claude/skills/design-push/SKILL.md](.claude/skills/design-push/SKILL.md) |
| **Save a Claude Design page as a reference for a screen** | `/design-pull <remote path> --target <screen>` in Claude Code | [screens/design/README.md](screens/design/README.md), [.claude/skills/design-pull/SKILL.md](.claude/skills/design-pull/SKILL.md) |
| Generate this system into a new medium (documents, slides, native app) | `tokens/design-system-handoff.json` | [adapters/astro/README.md](adapters/astro/README.md), [adapters/rails/README.md](adapters/rails/README.md), [adapters/wordpress/README.md](adapters/wordpress/README.md), [brand/templates/README.md](brand/templates/README.md) |
| See the fonts, colours or brands | [docs/fonts.html](docs/fonts.html), [docs/colour.html](docs/colour.html), [docs/brands.html](docs/brands.html) | [DESIGN.md](DESIGN.md) |
| Find why a decision was made | [MEMORY.md](MEMORY.md) | [archive/MEMORY.md](archive/MEMORY.md), the history before the root doc set. Read it before you reverse a decision. |
| See what is next | [TODO.md](TODO.md) | |
| Record a release | [CHANGELOG.md](CHANGELOG.md), `VERSION` | |
| Read an old plan or spec | `docs/superpowers/` (dated history, not rules) | |

## 30-second model

- One company, several brands: **ağustos** (parent), **pataraz**, **pld türkiye**, **iesdesk**, **specquick**.
- Every brand shares **one symbol**, the Laz Güneşi (18-blade sun). Ağustos alone owns red; every other house brand uses black or white identity ink and differs by its **wordmark**.
- The logo ("lockup") is the symbol plus the lowercase wordmark in the registered identity ink. It is always lowercase, with no tagline.
- **Shared red `#cf142a` is a 2px rule** under content links and on menu hover or current, plus keyboard focus. It is never a fill, except the dark-theme primary CTA.
- The design direction is **İskandivvian: Scandinavian restraint filtered through Mediterranean warmth.** The twelve principles, the avoid list, the brand chrome table and the screens table live in `ui/UI-KIT.md`, generated from `tokens/design-tokens.json`. Read that file. Do not restate it.
- A new house brand is a registry entry in `brand/brands.json` (wordmark, neutral identity ink, domain) plus the two build scripts: about ten minutes, no new design work. `brand/README.md` has the steps.

## "I need ___": use this file

First pick the **brand** (`agustos`, `pataraz`, `pld`, `iesdesk`, `specquick`), then the use. Put the brand slug into `<brand>` in the path.

| I need | File |
|---|---|
| The logo for a **website or app** (vector) | `brand/exports/<brand>/lockup/<brand>-lockup__positive.svg` |
| The logo on a **dark, brand-color or photo** background | `…/lockup/<brand>-lockup__negative.svg` |
| The logo in a **single ink color** (print, engraving) | `…/lockup/<brand>-lockup__mono.svg` |
| The logo for **print or business cards** | `…/lockup/<brand>-lockup__positive.pdf` (or `__negative`, `__mono`) |
| The logo for a **slide or social post** (raster) | `…/lockup/<brand>-lockup__positive.png` (2400px) or `…@800.png` |
| A **favicon, browser tab or app icon** | `laz-gunesi-amblem/favicon/favicon.svg`, the canonical file, shared by every site. The rest of the kit is in `laz-gunesi-amblem/favicon/`, and each brand has the same files under `brand/exports/<brand>/favicon/`. |
| A **square profile avatar** | `brand/exports/<brand>/social/<brand>-avatar-1000.png` (or `-400`) |
| A **link-preview or OG image** (1200×630) | `brand/exports/<brand>/social/<brand>-og.png` |
| Just the **symbol**, no wordmark | `laz-gunesi-amblem/svg/master.svg` (also the shared favicon artwork) |
| **Brand colors as swatches** | `brand/exports/<brand>/swatches/<brand>.ase` (Adobe) or `.clr` (Apple) |
| A **PowerPoint, Word or Google-compatible** template | `brand/exports/<brand>/office/<brand>-template.pptx`, `-document-template.docx`, `-letterhead.docx` |
| An **email signature** | `brand/exports/<brand>/email/` (one signature HTML file per brand) |
| **Brand guidelines** to share | `brand/exports/<brand>/guidelines/<brand>-brand-guidelines.pdf` |
| A **product datasheet** (lighting "teknik föy", A4) | `brand/exports/<brand>/datasheet/<product-key>.pdf` (for example `pataraz-px22.pdf`; edit `PRODUCTS` in `brand/build_datasheet.py`, then run it again) |
| The **fonts** (to install) | `brand/fonts/` (Inter Tight, Inter, JetBrains Mono, with licenses) |

> Coverage: `agustos`, `pataraz` and `pld` have the **full** set above. `iesdesk` and `specquick` have
> **logos, favicons and social only** (no office, swatches, email or guidelines yet). The **datasheet**
> kit holds many products per brand: real Pataraz sheets (`pataraz-pl22`, `pataraz-px22`,
> `pataraz-py300600`, `pataraz-py600600`, `pataraz-py6001200`) and an
> `agustos` sample (`agustos-pro-spot-28`). Other brands produce a generic sheet on demand.

## The three logo expressions: pick by background

1. **positive**: registered identity marks on a light or cream background, red for Ağustos and black for every other house brand. This is the default, about 90% of uses.
2. **negative**: cream or white marks on the identity tile, red for Ağustos and black for every other house brand. Social avatars and identity banners. (Favicons use the shared red `master.svg` instead.)
3. **mono**: one ink color. Single-color print, stamps, engraving.

There is no fourth expression. Do not invent a white-on-transparent "reverse" logo; `positive` already works on dark.

## Brands at a glance

| Brand (slug) | Wordmark | Color | Domain | Chrome | Kit |
|---|---|---|---|---|---|
| `agustos` | ağustos | `#cf142a` | agustos.com | sidebar | full |
| `pataraz` | pataraz | `#15130f` | pataraz.com | topbar with footer | full |
| `pld` | pld türkiye | `#15130f` | pldturkiye.com | topbar with footer | full |
| `iesdesk` | iesdesk | `#15130f` | iesdesk.com | sidebar | logos only |
| `specquick` | specquick | `#15130f` | specquick.com | sidebar | logos only |

Novara (outdoor kitchen furniture) is a brand that Ağustos **represents and distributes** (like Soraa, CoeLux), **not** a house brand. It has no assets here and needs none.

**Pataraz** has its own brand spec, [PATARAZ.md](PATARAZ.md): positioning (B2B spec market), identity rules, datasheet conventions and website direction. Read it before you build the Pataraz site or a datasheet. `DESIGN.md` stays the master for every shared rule.

## Rules

- Use brand red `#cf142a`. Fix any other brand red that you find: the older value is stale, and the checker reports it.
- Set the wordmark in Inter Tight, weight 650, lowercase, in the registered identity ink. Never put a tagline or subtitle on the lockup.
- Use one symbol for all brands, and never redraw it. Use red for the Ağustos identity and black or white for every other house brand.
- Keep signal and identity separate. Red rules and focus never make a non-Ağustos logo red.
- Use the brand's registered chrome from `brand/brands.json` (`chrome`). Style chrome only in `tokens/web.css.tmpl`.
- Edit `tokens/design-tokens.json` or `tokens/web.css.tmpl`, then run `python3 scripts/build_design_system.py`. Never hand-edit generated CSS, `theme.json`, `tokens/resolved.json` or anything under `brand/exports/`.
- Run `bin/setup` once in each new clone. It activates the pre-push hook in `.githooks/`, which runs `scripts/ci.sh` before every push.
- After an everyday source change, run the build, then `scripts/ci.sh`: the `--check` steps and the unit tests. Run `--check` before every handoff.
- Run `brand/build.py`, `brand/build_templates.py`, `scripts/build_ui_fonts.py` or `brand/build_datasheet.py` only when the user asks for a full rebuild. Then update `ASSETS.md`.
- Rebuild the Office files (letterhead, document template, PowerPoint) only when Emre asks, and only after the Ağustos brand approach changed: identity ink, wordmark, logo, or the document or presentation recipe. A website-only token edit never needs one. Never rebuild them as a reflex to a drift warning from the local gate. See [MEMORY.md](MEMORY.md), office-rebuild-on-request.
- Keep taglines in `brand/brands.json` (`tagline_en`, `tagline_tr`). Use them sparingly, and never print them on an artifact.
- Update `ASSETS.md` in the same change when you add, move or recolor a brand asset.
- Give any change under `ui/` a `VERSION` bump, a rebuild, a `v<VERSION>` tag and a `/design-push`, all in the same change. Consumers pin the tag.
- Tell consuming projects to load `ui/agustos.css` and use `var(--name)`. A project that hand-types `#cf142a` or `--paper: #ffffff` has a defect; `python3 ui/check-agustos-ui.py <project>` finds it.
- Load the fonts, not only the stacks. `agustos.css` sets font stacks only; without `ui/agustos-fonts.css` or the `@fontsource-variable` packages, a page renders in system sans while it appears to comply.
- For consumer projects, treat `ui/`, `tokens/design-system-handoff.json` and `brand/exports/` as ready-to-use inputs. A project that builds web interfaces needs `ui/UI-KIT.md` and nothing else. A consumer never regenerates this repository.
- Do not load or paste the whole repository into context. Find the task in the router, then read only its files.
- Write each new decision in `MEMORY.md` with a date-slug ID. Read `archive/MEMORY.md` only before you change a source decision or propose a reversal.
- Write the plan for a task under `## Now` in `TODO.md`. Keep 5 items at most under `## Next`.
- Record shipped work in `CHANGELOG.md` with additive lines.

## Traps

- Never edit inside the generated block of `DESIGN.md`. Edit the registry, run the build, then `--check`. The build and `tests/test_design_system.py` compare the block byte for byte.
- Put a rule that consuming sites must follow into `ui/check-agustos-ui.py.tmpl`, not only into a repository test. A rule that only a repository test reads never reaches a consuming site.
- Do not take a grep for a runtime-set attribute, such as `data-theme`, as proof that a doc never shows it. `docs/colour.html` shows dark through a toggle that sets the attribute at runtime.
- Before you delete CSS, `git grep` the adapters and screens for its custom properties. A deleted property left both adapter footers with an invisible lockup.
- Keep the `/design-push`, `/design-pull` and `--target` strings in this file, and never name the retired Claude Design pull folder here. `tests/test_design_sync.py` asserts both.
