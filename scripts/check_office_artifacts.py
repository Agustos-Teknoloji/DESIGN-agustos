#!/usr/bin/env python3
"""Write or verify the deterministic Office artifact manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "brand" / "exports" / "office-manifest.json"
SOURCE_PATHS = (
    "tokens/resolved.json",
    "brand/brands.json",
    "brand/build_templates.py",
    "brand/build_presentation.mjs",
    "brand/package.json",
    "brand/package-lock.json",
    "scripts/check_office_artifacts.py",
)
OFFICE_SUFFIXES = (
    "letterhead.docx",
    "document-template.docx",
    "template.pptx",
)


class ArtifactError(ValueError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def office_brands(root: Path) -> list[str]:
    registry = json.loads((root / "brand" / "brands.json").read_text(encoding="utf-8"))
    return sorted(slug for slug, brand in registry["brands"].items() if brand.get("office", False))


def artifact_paths(root: Path) -> list[Path]:
    return [
        root / "brand" / "exports" / slug / "office" / f"{slug}-{suffix}"
        for slug in office_brands(root)
        for suffix in OFFICE_SUFFIXES
    ]


def source_digest(root: Path) -> str:
    digest = hashlib.sha256()
    source_paths = list(SOURCE_PATHS)
    source_paths.extend(
        f"brand/exports/{slug}/lockup/{slug}-lockup__{expression}.png"
        for slug in office_brands(root)
        for expression in ("positive", "negative")
    )
    for relative in source_paths:
        path = root / relative
        if not path.exists():
            raise ArtifactError(f"missing Office source: {relative}")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def expected_manifest(root: Path = ROOT) -> dict[str, Any]:
    resolved = json.loads((root / "tokens" / "resolved.json").read_text(encoding="utf-8"))
    files: dict[str, str] = {}
    for path in artifact_paths(root):
        relative = str(path.relative_to(root))
        if not path.exists():
            raise ArtifactError(f"missing Office artifact: {relative}")
        files[relative] = sha256(path)
    return {
        "system": resolved["name"],
        "version": resolved["version"],
        "source_sha256": source_digest(root),
        "artifacts": files,
    }


def write_manifest(root: Path = ROOT, manifest_path: Path | None = None) -> None:
    destination = manifest_path or (root / MANIFEST.relative_to(ROOT))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(expected_manifest(root), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def check_manifest(root: Path = ROOT, manifest_path: Path | None = None) -> list[str]:
    destination = manifest_path or (root / MANIFEST.relative_to(ROOT))
    if not destination.exists():
        return [str(destination.relative_to(root))]
    actual = json.loads(destination.read_text(encoding="utf-8"))
    expected = expected_manifest(root)
    drift: list[str] = []
    if actual.get("source_sha256") != expected["source_sha256"]:
        drift.append("Office generator sources")
    actual_files = actual.get("artifacts", {})
    for relative, digest in expected["artifacts"].items():
        if actual_files.get(relative) != digest:
            drift.append(relative)
    for relative in sorted(set(actual_files) - set(expected["artifacts"])):
        drift.append(f"unexpected artifact: {relative}")
    return drift


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_manifest()
            print(f"generated {MANIFEST.relative_to(ROOT)}")
            return 0
        drift = check_manifest()
    except (ArtifactError, KeyError, json.JSONDecodeError) as error:
        print(f"Office artifact validation failed: {error}", file=sys.stderr)
        return 2
    if drift:
        print("Office artifact drift:", file=sys.stderr)
        for item in drift:
            print(f"  - {item}", file=sys.stderr)
        print("run: python3 brand/build_templates.py", file=sys.stderr)
        return 1
    print(f"Office artifacts are current ({len(artifact_paths(ROOT))} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
