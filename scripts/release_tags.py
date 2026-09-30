#!/usr/bin/env python3
"""Tag every release that reached main and has no tag yet.

A release is a dated `## [x.y.z]` section in CHANGELOG.md. Its tag `vx.y.z`
goes on the first commit of main's first-parent history where VERSION reads
x.y.z: the merge that shipped it. Only versions newer than the newest existing
tag are considered, so old history is never retagged.

The GitHub workflow .github/workflows/tag-release.yml runs this on every push
to main, so a release is tagged the same way whether a local or a cloud
session made it. Nobody tags by hand.

  python3 scripts/release_tags.py --dry-run   print the plan, change nothing
  python3 scripts/release_tags.py             create the tags locally
  python3 scripts/release_tags.py --push      create them and push them to origin
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)
TAG = re.compile(r"^v(\d+\.\d+\.\d+)$")


class ReleaseError(RuntimeError):
    pass


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise ReleaseError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def parse(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def changelog_versions(changelog: str) -> list[str]:
    return RELEASE_HEADING.findall(changelog)


def tagged_versions(tags: list[str]) -> list[str]:
    return [match.group(1) for tag in tags if (match := TAG.match(tag))]


def pending(changelog: str, version: str, tags: list[str]) -> list[str]:
    """Released versions newer than the newest tag, oldest first."""
    released = changelog_versions(changelog)
    if version not in released:
        raise ReleaseError(f"VERSION is {version}, but CHANGELOG.md has no '## [{version}]' section")
    tagged = tagged_versions(tags)
    floor = max((parse(v) for v in tagged), default=(0, 0, 0))
    return sorted({v for v in released if parse(v) > floor and v not in tagged}, key=parse)


def release_commit(version: str, ref: str) -> str:
    """The first commit on ref's first-parent history whose VERSION reads `version`."""
    for commit in git("log", "--first-parent", "--reverse", "--format=%H", ref, "--", "VERSION").split():
        if git("show", f"{commit}:VERSION").strip() == version:
            return commit
    raise ReleaseError(f"no commit on {ref} sets VERSION to {version}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--ref", default="HEAD", help="the main-branch commit to read (default HEAD)")
    parser.add_argument("--dry-run", action="store_true", help="print the plan and change nothing")
    parser.add_argument("--push", action="store_true", help="push the new tags to origin")
    args = parser.parse_args()

    version = git("show", f"{args.ref}:VERSION").strip()
    changelog = git("show", f"{args.ref}:CHANGELOG.md")
    tags = git("tag", "--list", "v*").split()
    try:
        todo = pending(changelog, version, tags)
    except ReleaseError as error:
        print(f"release_tags: {error}", file=sys.stderr)
        return 1
    if not todo:
        print(f"release_tags: every release up to v{version} is tagged")
        return 0

    for release in todo:
        commit = release_commit(release, args.ref)
        name = f"v{release}"
        if args.dry_run:
            print(f"would tag {name} at {commit[:7]}")
            continue
        git("tag", "--annotate", name, commit, "--message", f"Ağustos Design System {name}")
        print(f"tagged {name} at {commit[:7]}")
    if args.push and not args.dry_run:
        git("push", "origin", *(f"refs/tags/v{release}" for release in todo))
        print(f"pushed {', '.join(f'v{release}' for release in todo)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
