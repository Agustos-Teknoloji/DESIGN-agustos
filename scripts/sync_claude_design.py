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
from pathlib import Path


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


# --- CLI --------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="print the bundle paths and sizes")
    listing.set_defaults(func=cmd_list)
    args = parser.parse_args()
    return args.func(args)


def cmd_list(args: argparse.Namespace) -> int:
    members = bundle_members()
    for name, payload in members:
        print(f"{len(payload):8}  {REMOTE_PREFIX}/{name}")
    print(f"{len(members)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
