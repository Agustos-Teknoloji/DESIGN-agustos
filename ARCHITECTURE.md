# Architecture

This repository is the factory for the Ağustos Design System. It holds the registries, the generators, the adapters and the brand assets. Consumers get the product: the generated `ui/` kit, the handoff JSON and the files under `brand/exports/`. They never run the generators. [HANDOFF.md](HANDOFF.md) and `scripts/pack_handoff.py` define what leaves the factory.

## Layers

The system has five layers: foundations, semantic roles, recipes, screens and adapters. The table in [DESIGN.md](DESIGN.md), section "Architecture and governance", defines what each layer owns and where it lives. The system does not depend on Astro. Astro is a reference implementation and a visual QA surface. Rails apps use the Rails adapter or copy the platform-neutral tokens.

## Sources you edit by hand

```txt
tokens/design-tokens.json Canonical cross-medium token registry, including the screens table
brand/brands.json         Canonical brand identity registry, including the chrome per brand
tokens/web.css.tmpl       Platform-neutral web behavior and compatibility classes
ui/*.tmpl                 Templates for UI-KIT.md, starter.html, the checker and the AGENTS snippet
screens/*.html            One reference page per screen type, on kit classes
DESIGN.md                 Human-readable specification, outside its generated block
laz-gunesi-amblem/        The master symbol and the canonical favicon kit
scripts/                  Generators, drift checks, the handoff packer and the Claude Design sync
adapters/                 Astro, Rails and WordPress translations
brand/                    Office, datasheet and asset generators
```

Decisions live in [MEMORY.md](MEMORY.md). History before the root doc set lives in [archive/MEMORY.md](archive/MEMORY.md).

## Generated outputs

Everything below is generated. Never edit it by hand. Repair the source and regenerate.

- `tokens/resolved.json`: resolved cross-medium values for the downstream generators.
- `tokens/design-system-handoff.json`: the single-file integration contract for coding systems.
- `tokens/agustos.css`: the portable CSS.
- `ui/`: the distribution kit, except its `*.tmpl` files and `LICENSE`.
- Adapter CSS, the WordPress `theme.json`, and the manifest.
- The design-direction block in `DESIGN.md`, between its markers, and the table in `screens/README.md`.
- `docs/web.html`, from `docs/web.html.tmpl` and the screens table.
- Everything under `brand/exports/`: lockups, favicons, social images, Office files, swatches, guidelines and datasheets.

Two build paths exist:

1. Everyday: `python3 scripts/build_design_system.py` writes `ui/`, the token CSS, the adapter CSS, the handoff JSON and the generated blocks.
2. Full rebuild, only when Emre asks: `brand/build.py`, `brand/build_templates.py`, `scripts/build_ui_fonts.py` and `brand/build_datasheet.py`. [README.md](README.md) lists the commands.

Generated files are committed, so consumer deployments never depend on this repository. Each generator has a `--check` mode, and CI fails on a stale file. `VERSION` is part of the manifest source hash, so a change under `ui/` without a rebuild fails CI. `scripts/check_office_artifacts.py` fingerprints only the fields that the Office generators read (MEMORY.md, 2026-09-13 office-rebuild-on-request).

## Promotion loop

A pattern moves from a live site into the system in five steps:

1. Test the pattern on a real site with real content.
2. Confirm that it is reusable and consistent with the identity principles.
3. Express the durable decision as a foundation, a semantic role, a recipe or a screen row here.
4. Regenerate the adapters and artifacts.
5. Run the drift, platform and visual checks before the release.

A web header does not become a Word header verbatim. Each adapter keeps the alignment, hierarchy, type, signal color and spacing logic, and translates them into the native conventions of its medium.

## Claude Design boundary

This repository owns the rules. `/design-push` writes only `agustos-ui/**` in the Claude Design project. `/design-pull` writes only `screens/design/**` here, each page for a named target screen. The skills are `.claude/skills/design-push/SKILL.md` and `.claude/skills/design-pull/SKILL.md`, and `scripts/sync_claude_design.py` does the work.

## Forbidden

- Tailwind, or any other CSS framework or CSS toolchain (MEMORY.md, 2026-09-15 vanilla-css-no-tailwind).
- A hand edit of a generated file, including anything under `brand/exports/` and `ui/` outside its templates.
- A full asset rebuild that Emre did not ask for.

## Testing

Test the generators, the published kit contract and the adapters. The kit is a public API: a class that `compatibility.cssClasses` lists must exist in the generated CSS, and every text color token must pass contrast on every substrate.

The CI definition is [.github/workflows/design-system.yml](.github/workflows/design-system.yml). It runs on every pull request and on every push to `main`. Run its three steps locally before you push:

```bash
python3 scripts/build_design_system.py --check
python3 scripts/check_office_artifacts.py --check
python3 -m unittest discover -s tests
```

CI uses Python 3.12. The macOS system Python is 3.9, so run the steps with `mise exec python@3.12 -- python3 ...` to match CI.

Suites:

| Suite | What it covers |
|---|---|
| `tests/test_design_system.py` | The registry, token resolution, the screens table, the generated outputs and their drift, the handoff contract, and the generated block in `DESIGN.md` |
| `tests/test_ui_kit.py` | The `ui/` kit: the published class list, contrast, fonts and the checker |
| `tests/test_screens.py` | One reference page per row of the screens table, on kit classes only; runs the checker on `screens/` |
| `tests/test_adapter_contracts.py` | The Astro, Rails and WordPress adapter sources, the CI workflow, and the handoff JSON against the kit contract |
| `tests/test_office_artifacts.py` | The Word and PowerPoint contract and the Office fingerprint |
| `tests/test_pack_handoff.py` | The handoff zip: what it holds and what it leaves out |
| `tests/test_design_sync.py` | The Claude Design push and pull, and the docs that route to them |
| `adapters/astro/tests/*.test.mjs` | Astro chrome and Pagefind; run with the scripts in `adapters/astro/package.json` |
| `adapters/rails/test/adapter_contract_test.rb` | The Rails adapter contract; [adapters/rails/README.md](adapters/rails/README.md) has the command |

Before you call a system change done, also do these factory checks. The visual checks for consumers are in the QA checklist in `DESIGN.md`.

1. If an Office export changed, render every DOCX page and PPTX slide, run the Google Docs title sanitizer, and run the overflow checks.
2. If `ui/` changed, bump `VERSION`, rebuild, and tag `v<VERSION>` in the same change. Serve `ui/`, and confirm that the woff2 files load and that Inter Tight renders. A font stack alone is not proof.

Known gaps:

- CI does not run the Astro or Rails adapter tests. Run them locally when you change an adapter.
- No test renders the Office files. The render check above is manual.
