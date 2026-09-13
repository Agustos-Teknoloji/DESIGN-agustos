#!/usr/bin/env python3
"""Keep the Claude Design project "Ağustos" in step with this repository.

The repository owns the rules: tokens, the generated kit, fonts, the symbol,
the favicon, the lockups. `build` packs them into dist/claude-design/agustos-ui/
so Claude can push that folder into the Design project with the DesignSync tool.

The Design project owns the drawings: page compositions and explorations.
`pull` copies one page subtree, plus the shared runtime it needs, into
mockups/claude-design/ as a reference. Nothing in the kit imports it.

This script never talks to the network. Claude makes the DesignSync calls,
following .claude/skills/design-push/SKILL.md and .claude/skills/design-pull/SKILL.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from datetime import date
from pathlib import Path
from typing import NamedTuple


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
UI_DIR = ROOT / "ui"
FAVICON_DIR = ROOT / "laz-gunesi-amblem" / "favicon"
LOCKUP_GLOB = "*/lockup/*.svg"
DIST_DIR = ROOT / "dist" / "claude-design"

SYSTEM_NAME = "Ağustos Design System"
SOURCE_REPO = "Agustos-Teknoloji/DESIGN-agustos"
REMOTE_PREFIX = "agustos-ui"
PROJECT_ID = "7fee69d5-01ee-4727-beaf-cb6c5bd923c4"
PROJECT_URL = f"https://claude.ai/design/p/{PROJECT_ID}"


# --- Bundle -----------------------------------------------------------------


def version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def kit_files(root: Path = ROOT) -> list[Path]:
    """Every shipped kit file. Templates stay in the factory."""
    files: list[Path] = []
    for path in sorted((root / "ui").rglob("*")):
        if path.is_file() and path.suffix != ".tmpl":
            files.append(path)
    return files


def lockup_svgs(root: Path = ROOT) -> list[Path]:
    return sorted((root / "brand" / "exports").glob(LOCKUP_GLOB))


def favicon_files(root: Path = ROOT) -> list[Path]:
    folder = root / "laz-gunesi-amblem" / "favicon"
    return sorted(p for p in folder.iterdir() if p.is_file() and p.name != "README.md")


def bundle_members(root: Path = ROOT) -> list[tuple[str, bytes]]:
    """(path under agustos-ui/, payload) for the kit, logos, and favicon."""
    members: list[tuple[str, bytes]] = []
    ui_dir = root / "ui"
    for path in kit_files(root):
        members.append((path.relative_to(ui_dir).as_posix(), path.read_bytes()))
    for path in lockup_svgs(root):
        members.append((f"logos/{path.name}", path.read_bytes()))
    for path in favicon_files(root):
        members.append((f"favicon/{path.name}", path.read_bytes()))
    return members


def manifest(members: list[tuple[str, bytes]], version: str, commit: str) -> dict:
    """Hashes for every bundled file, so a later push can diff without reading remote content."""
    files = {
        name: {"bytes": len(payload), "sha256": sha256(payload)}
        for name, payload in sorted(members)
    }
    return {
        "system": SYSTEM_NAME,
        "source": SOURCE_REPO,
        "version": version,
        "commit": commit,
        "remotePrefix": REMOTE_PREFIX,
        "files": files,
    }


# --- Cards ------------------------------------------------------------------
# Each card is one full HTML document. Line 1 is the @dsCard marker the Design
# System pane indexes. Cards load the pushed kit by relative path, fonts first.


class Card(NamedTuple):
    slug: str
    group: str
    width: int
    height: int
    name: str
    subtitle: str
    body: str


HOUSE_BRANDS = ("agustos", "pataraz", "pld", "iesdesk", "specquick")

CARDS: tuple[Card, ...] = (
    Card(
        "type",
        "Type",
        700,
        300,
        "Type scale",
        "Inter Tight display · Inter body · JetBrains Mono code",
        """
<p class="type-hero-md">Light, placed with intent.</p>
<h2 class="type-h2">Headings weigh 300 to 400</h2>
<p class="type-body">Body is Inter at a 65ch measure. <a class="type-link" href="#">A content link</a> carries the red rule. Code is <code class="type-code">JetBrains Mono</code>.</p>
""",
    ),
    Card(
        "colours",
        "Colours",
        700,
        170,
        "Six colours",
        "White paper · cream band · light gray · dark gray · off-black · red",
        """
<div class="agustos-card-grid" style="grid-template-columns: repeat(6, 1fr)">
  <div class="agustos-card" style="background: var(--paper-white)"><p class="type-h4">white</p></div>
  <div class="agustos-card" style="background: var(--cream)"><p class="type-h4">cream</p></div>
  <div class="agustos-card" style="background: var(--surface)"><p class="type-h4">light gray</p></div>
  <div class="agustos-card" style="background: var(--ink-soft); color: var(--paper-white)"><p class="type-h4">dark gray</p></div>
  <div class="agustos-card" style="background: var(--ink); color: var(--paper-white)"><p class="type-h4">off-black</p></div>
  <div class="agustos-card" style="background: var(--signal); color: var(--paper-white)"><p class="type-h4">red</p></div>
</div>
""",
    ),
    Card(
        "actions",
        "Actions",
        700,
        200,
        "Action tiers",
        "Primary · secondary · quiet · content link — one 44px size",
        """
<div class="hero-actions">
  <a class="agustos-button agustos-button--primary" href="#">Request pricing</a>
  <a class="agustos-button agustos-button--secondary" href="#">See products</a>
  <a class="agustos-button agustos-button--quiet" href="#">Contact</a>
</div>
<p class="type-body">Inline, <a class="type-link" href="#">a content link</a> keeps the red rule.</p>
""",
    ),
    Card(
        "brand-marks",
        "Brand",
        700,
        260,
        "House lockups",
        "One symbol · lowercase wordmark · only ağustos is red",
        "\n".join(
            f'<p><img src="../logos/{slug}-lockup__positive.svg" alt="{slug} lockup" style="height: 40px"></p>'
            for slug in HOUSE_BRANDS
        ),
    ),
    Card(
        "favicon",
        "Brand",
        700,
        150,
        "Shared favicon",
        "One red Laz Güneşi tab icon for every house site",
        """
<div class="hero-actions" style="align-items: center">
  <img src="../favicon/favicon.svg" alt="Laz Güneşi favicon" style="width: 64px; height: 64px">
  <img src="../favicon/favicon.svg" alt="" style="width: 32px; height: 32px">
  <img src="../favicon/favicon.svg" alt="" style="width: 16px; height: 16px">
  <p class="type-body">Canonical file: <code class="type-code">laz-gunesi-amblem/favicon/favicon.svg</code>. Same artwork on every site.</p>
</div>
""",
    ),
)


def card_html(card: Card, version: str) -> str:
    marker = (
        f'<!-- @dsCard group="Kit · {card.group}" viewport="{card.width}x{card.height}" '
        f'name="{card.name}" subtitle="{card.subtitle}" -->'
    )
    return f"""{marker}
<!doctype html>
<html lang="tr" data-theme="light">
<head>
<meta charset="utf-8">
<title>{card.name} — Ağustos UI kit v{version}</title>
<link rel="stylesheet" href="../agustos-fonts.css">
<link rel="stylesheet" href="../agustos.css">
<style>body {{ margin: 0; padding: 24px 28px; }}</style>
</head>
<body class="brand-agustos paper-white">
{card.body.strip()}
<p class="type-footnote">Ağustos UI kit v{version} · pushed from the repository. Edit the source there, not here.</p>
</body>
</html>
"""


def card_members(version: str) -> list[tuple[str, bytes]]:
    return [(f"cards/{card.slug}.html", card_html(card, version).encode("utf-8")) for card in CARDS]


# --- Build ------------------------------------------------------------------


class GuardError(RuntimeError):
    """A precondition for a push failed. The message says what to run."""


def generated_outputs_are_current(root: Path = ROOT) -> bool:
    result = subprocess.run(
        ["python3", "scripts/build_design_system.py", "--check"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def ui_is_clean(root: Path = ROOT) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "ui"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip() == ""


def git_commit(root: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def build_bundle(
    destination: Path = DIST_DIR,
    root: Path = ROOT,
    *,
    check=generated_outputs_are_current,
    clean=ui_is_clean,
    commit=git_commit,
) -> Path:
    """Write <destination>/agustos-ui/ from the generated kit. Refuse if the kit is stale or dirty."""
    if not check(root):
        raise GuardError(
            "Generated outputs are stale. Run `python3 scripts/build_design_system.py` and commit, "
            "then run `python3 scripts/build_design_system.py --check` until it passes."
        )
    if not clean(root):
        raise GuardError("ui/ has uncommitted changes. Commit or discard them before a push.")
    ver = version()
    members = bundle_members(root) + card_members(ver)
    data = manifest(members, version=ver, commit=commit(root))
    payload = (json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    members.append(("MANIFEST.json", payload))

    folder = destination / REMOTE_PREFIX
    if folder.exists():
        shutil.rmtree(folder)
    for name, content in members:
        target = folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return folder


# --- Pull -------------------------------------------------------------------
# A Design page is React + JSX loaded by relative paths from the project root.
# Mirroring the remote layout keeps every link intact. The page is a reference;
# nothing in the kit imports it.

RUNTIME_PATHS: tuple[str, ...] = (
    "styles.css",
    "_ds_bundle.js",
    "tokens/fonts.css",
    "tokens/colors.css",
    "tokens/spacing.css",
    "tokens/typography.css",
    "tokens/base.css",
)
MOCKUPS_DIR = ROOT / "mockups" / "claude-design"
PAGE_PREFIX = "ui_kits/"
STATUS_HEADER = "| Remote path | Pulled | Status | Built in |"
STATUS_DIVIDER = "|---|---|---|---|"

README_TEMPLATE = """# Claude Design references

Pages pulled verbatim from the Claude Design project "Ağustos".

- Project: {url}
- Project ID: `{project_id}`
- Pulled by: `python3 scripts/sync_claude_design.py pull` (see `.claude/skills/design-pull/SKILL.md`)

These files are references, not kit sources. Nothing in `ui/` imports them.
The shared runtime at this folder's root (`styles.css`, `_ds_bundle.js`, `tokens/`) is
overwritten on every pull. Each page folder holds the page and an `index.png` screenshot.

## When you build one of these pages

1. Open the page folder and `index.png` beside your editor.
2. Rebuild the layout in the website repository with `ui/UI-KIT.md` and the kit classes.
3. Do not copy the Design markup or CSS. The kit is generated from the three sources.
4. Run `python3 vendor/agustos-ui/check-agustos-ui.py .` until it exits 0.
5. Change the row below to `implemented` and record the repository and commit.

## Status

{header}
{divider}
{rows}
"""


def _page_is_allowed(page: str) -> str:
    page = page.strip("/")
    if not page.startswith(PAGE_PREFIX) or ".." in page.split("/") or page == PAGE_PREFIX.rstrip("/"):
        raise ValueError(f"page must be a folder under {PAGE_PREFIX}, got {page!r}")
    return page


def _status_rows(existing: str | None) -> dict[str, list[str]]:
    """Parse the status table into {remote path: [path, pulled, status, built in]}."""
    rows: dict[str, list[str]] = {}
    if not existing:
        return rows
    for line in existing.splitlines():
        if not line.startswith("| ") or line in (STATUS_HEADER, STATUS_DIVIDER):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].startswith(PAGE_PREFIX):
            rows[cells[0]] = cells
    return rows


def update_readme(existing: str | None, page: str, today: str, commit: str) -> str:
    """Add or refresh the page's row. Keep a row's status and 'built in' when it exists."""
    rows = _status_rows(existing)
    current = rows.get(page, [page, today, "pending", "—"])
    current[1] = today
    rows[page] = current
    body = "\n".join("| " + " | ".join(cells) + " |" for _, cells in sorted(rows.items()))
    return README_TEMPLATE.format(
        url=PROJECT_URL,
        project_id=PROJECT_ID,
        header=STATUS_HEADER,
        divider=STATUS_DIVIDER,
        rows=body,
    )


def _source_root(source: Path, scratch: Path) -> Path:
    """A directory as-is, or a zip extracted into scratch. Unwrap a single top-level folder."""
    if source.is_dir():
        root = source
    else:
        with zipfile.ZipFile(source) as archive:
            archive.extractall(scratch)
        root = scratch
    entries = [p for p in root.iterdir() if not p.name.startswith(".")]
    if len(entries) == 1 and entries[0].is_dir() and not (root / "styles.css").exists():
        root = entries[0]
    return root


def pull(
    source: Path,
    page: str,
    destination: Path = MOCKUPS_DIR,
    *,
    today: str,
    commit: str,
) -> list[Path]:
    """Copy one page subtree and the shared runtime from source into destination, mirroring paths."""
    page = _page_is_allowed(page)
    written: list[Path] = []
    with tempfile.TemporaryDirectory() as scratch:
        root = _source_root(source, Path(scratch))
        page_dir = root / page
        if not page_dir.is_dir():
            raise FileNotFoundError(f"{page} is not a folder in {source}")
        wanted: list[Path] = [p for p in sorted(page_dir.rglob("*")) if p.is_file()]
        wanted += [root / rel for rel in RUNTIME_PATHS if (root / rel).is_file()]
        for path in wanted:
            target = destination / path.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
            written.append(target)
    readme = destination / "README.md"
    existing = readme.read_text(encoding="utf-8") if readme.exists() else None
    readme.write_text(update_readme(existing, page, today, commit), encoding="utf-8")
    written.append(readme)
    return written


# --- CLI --------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="print the bundle paths and sizes")
    listing.set_defaults(func=cmd_list)
    build = sub.add_parser("build", help="write dist/claude-design/agustos-ui/ after the guards pass")
    build.add_argument("-o", "--output", type=Path, default=DIST_DIR, help="destination folder (default: dist/claude-design)")
    build.set_defaults(func=cmd_build)
    pulling = sub.add_parser("pull", help="copy one Design page into mockups/claude-design/")
    pulling.add_argument("--from", dest="source", type=Path, required=True, help="directory or zip that mirrors the Design project layout")
    pulling.add_argument("--page", required=True, help="remote folder, for example ui_kits/website")
    pulling.set_defaults(func=cmd_pull)
    args = parser.parse_args()
    return args.func(args)


def cmd_list(args: argparse.Namespace) -> int:
    members = bundle_members()
    for name, payload in members:
        print(f"{len(payload):8}  {REMOTE_PREFIX}/{name}")
    print(f"{len(members)} files")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    try:
        folder = build_bundle(args.output)
    except GuardError as error:
        print(f"refused: {error}")
        return 1
    count = sum(1 for p in folder.rglob("*") if p.is_file())
    print(f"wrote {folder.relative_to(ROOT) if folder.is_relative_to(ROOT) else folder} ({count} files)")
    return 0


def cmd_pull(args: argparse.Namespace) -> int:
    try:
        written = pull(args.source, args.page, today=date.today().isoformat(), commit=git_commit())
    except (ValueError, FileNotFoundError) as error:
        print(f"refused: {error}")
        return 1
    for path in written:
        print(path.relative_to(ROOT).as_posix())
    print(f"{len(written)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
