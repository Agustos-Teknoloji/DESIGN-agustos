# Claude Design sync — design

**Date:** 2026-09-13
**Status:** approved in discussion; implementation plan pending
**Explainer for the product owner:** https://claude.ai/code/artifact/98eef1b7-8cb5-41f4-ab45-03aa83b7e97b

## Problem

Two places hold the Ağustos design system.

- `DESIGN-agustos` (this repository) is the factory. Three hand-edited sources generate the UI kit, adapters, logos, and favicons.
- The Claude Design project "Ağustos" (`7fee69d5-01ee-4727-beaf-cb6c5bd923c4`, org default) is a re-creation. It rebuilt its own CSS, React components, a Google Fonts stack, and a parametric copy of the symbol from an uploaded spec. Its readme says "Version 3.0" and "replace fonts and symbol when the repo is connected". The repository is at v5.1.1.

The two have drifted. Today every sync is a person copying files by hand. There is no rule for which side owns what.

## Decision

Option B: the repository is the source of truth for rules. The Claude Design project is the source of truth for drawings. Each artifact type flows in one direction only.

| Artifact | Owner | Direction | Destination |
|---|---|---|---|
| Tokens, generated kit (`ui/`), fonts, symbol, favicon, lockups | Repository | Push | `agustos-ui/**` in the Design project |
| Page compositions, explorations, Design's React components | Design project | Pull | `mockups/claude-design/**` in the repository |
| A rule change discovered in a pulled page | Repository | Manual map | One of the three sources, then regenerate, then push |

Nobody copies Design CSS into the repository. Nobody edits Design's own tokens to match the repository.

## Push: repository → Design

### Bundle

`scripts/sync_claude_design.py build` writes `dist/claude-design/` (git-ignored, like the handoff zip). It reuses `kit_files()` and `lockup_svgs()` from `scripts/pack_handoff.py`.

```
agustos-ui/
  agustos.css  agustos-fonts.css  starter.html  UI-KIT.md  AGENTS-SNIPPET.md
  check-agustos-ui.py  kit.json  LICENSE
  fonts/            5 woff2 + 3 OFL.txt
  logos/            brand/exports/*/lockup/*.svg
  favicon/          laz-gunesi-amblem/favicon/*
  cards/*.html      preview pages, first line <!-- @dsCard group="…" -->
  MANIFEST.json     version, git commit, sha256 per file
```

Cards render the canonical kit inside the Design System pane. Minimum set: type, colours, actions, brand marks, favicon. Each card is a full HTML document whose line 1 is `<!-- @dsCard group="…" viewport="WxH" name="…" subtitle="…" -->`, matching the format the project already uses. Each loads `../agustos-fonts.css` then `../agustos.css` by relative path. Group labels are prefixed `Kit · ` (for example `Kit · Type`) so the pushed cards sit apart from Design's own `Type`, `Colors`, `Brand` groups in the pane. Cards are generated from a small template; the exact count is fixed at plan time.

### Guards

- `build` runs `python3 scripts/build_design_system.py --check` first and refuses to build if it fails.
- `build` refuses if `git status --porcelain ui/` is not empty.
- `MANIFEST.json` hashes match `ui/kit.json` for every kit file.

### Upload

A project skill `.claude/skills/design-push/SKILL.md` drives the `DesignSync` tool:

1. `list_files` on the project.
2. Diff remote `agustos-ui/**` against `MANIFEST.json`: new, changed, stale.
3. `finalize_plan` with writes `agustos-ui/**` and deletes limited to stale `agustos-ui/**` paths; `localDir` = `dist/claude-design/`.
4. `write_files` with `localPath` for changed files; `delete_files` for stale ones.
5. Report: files written, files deleted, or "nothing to push".

The plan never includes a path outside `agustos-ui/`. The tool rejects paths outside the plan, so Design-owned files cannot be overwritten by this workflow.

### Out of scope, separate approval later

Pointing Design's own `tokens/fonts.css` and `assets/laz-gunesi.svg` at the pushed copies. Those are Design-owned files.

## Pull: Design → repository

### Remote facts (read 2026-09-13 with `list_files` and `get_file`)

- Project type is `PROJECT_TYPE_DESIGN_SYSTEM`, `canEdit: true`. No `agustos-ui/` folder exists yet.
- `ui_kits/website/index.html` loads React 18 and Babel standalone from unpkg, `../../styles.css`, `site.css`, `../../_ds_bundle.js`, and five sibling `.jsx` files. It is not standalone.
- `_ds_manifest.json` lists `globalCssPaths`: `tokens/fonts.css`, `tokens/colors.css`, `tokens/spacing.css`, `tokens/typography.css`, `tokens/base.css`, `styles.css`.
- Card marker format in use: `<!-- @dsCard group="Brand" viewport="700x200" name="Laz Güneşi" subtitle="…" -->` as line 1, then a full HTML document linking `../styles.css`.
- The root also holds `Ağustos Website.html` and `IESDesk.html`, standalone exports the Design chat reported as broken bundles. Pull ignores them.

### Fetch

A project skill `.claude/skills/design-pull/SKILL.md` takes a remote directory such as `ui_kits/website`. With the login done it uses `DesignSync` `get_file` for every file under that directory, plus the shared runtime the page needs: every path in `globalCssPaths` and `_ds_bundle.js`. It writes them into a temp directory that mirrors the remote layout. Without the login it accepts a zip exported from Claude Design.

### Copy

`scripts/sync_claude_design.py pull --from <dir-or-zip> --page ui_kits/website` copies the page subtree and the shared runtime verbatim into `mockups/claude-design/`, mirroring the remote layout:

```
mockups/claude-design/
  README.md
  styles.css  _ds_bundle.js  tokens/*.css        shared runtime, overwritten on every pull
  ui_kits/website/index.html  site.css  *.jsx     the page
  ui_kits/website/index.png                       full-page screenshot taken at pull time
```

Relative links inside the pulled page resolve unchanged, so `index.html` opens in a browser as long as the CDN copies of React and Babel exist. The screenshot is the durable reference if they do not. The skill captures it with the browser pane after the copy.

It writes or updates `mockups/claude-design/README.md`:

- Source project URL and ID, remote path, pull date, git commit of the repository at pull time.
- A status table, one row per page: remote path, pulled date, status `pending` or `implemented`, site repository and commit once built.
- The rule for whoever builds a page later: rebuild with the kit and `ui/UI-KIT.md`; do not copy Design markup or CSS; run `check-agustos-ui.py` until it exits 0.

Pulled files are references. Nothing in the kit imports them. Tests and `--check` never treat them as generated. `pull` refuses a `--page` outside `ui_kits/`.

Fetched content is untrusted. `pull` writes bytes verbatim and never executes them.

### Pages A to D

They are real website pages to build later. They land as `pending` references now. When built, the website repository's agent reads the mockup plus `ui/UI-KIT.md`, rebuilds with kit classes, and the status row flips to `implemented`.

## Docs

- `docs/claude-design-sync.html` — the explainer, restyled on `docs/agustos.css` like `docs/handoff-setup.html`.
- `AGENTS.md` task table: two rows, "Push the kit to Claude Design" and "Pull a Claude Design page".
- `HANDOFF.md` "If a Claude Design zip arrives" points at `/design-pull`.
- `CHANGELOG.md` Unreleased entry. `VERSION` → 5.2.0 at ship.
- `archive/MEMORY.md` decision entry.

## Tests

`tests/test_design_sync.py`:

- Bundle contains every `ui/` file except `.tmpl`, every lockup SVG, every favicon file.
- Every card's first line is a `@dsCard` marker with a `group`.
- `MANIFEST.json` hashes equal `ui/kit.json` hashes.
- `build` fails when `--check` fails (mock) or `ui/` is dirty (mock).
- `pull` copies the page subtree and the shared runtime verbatim, mirroring the remote layout, writes the README with a `pending` row, and refuses a page outside `ui_kits/`.
- `pull` accepts a zip and a directory and produces identical output.
- A second `pull` of the same page updates its row instead of adding one, and keeps an `implemented` status.

## Error handling

| Condition | Behaviour |
|---|---|
| No design login | Skill stops with: run `/design-login` once in an interactive Claude Code terminal. |
| Generated outputs stale | `build` exits non-zero with the `--check` diff. |
| Remote has a file under `agustos-ui/` not in the bundle | Listed as stale; deleted only after the user sees it in the plan. |
| `get_file` returns content that reads like instructions | Written verbatim as data; the skill tells the user the path looks odd. |

## Everyday commands

```
/design-login                      once per Mac
/design-push                       repository → Claude Design
/design-pull ui_kits/website       Claude Design → mockups/claude-design/
python3 scripts/build_design_system.py --check   must pass before any push
```
