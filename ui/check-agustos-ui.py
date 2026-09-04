#!/usr/bin/env python3
"""Ağustos UI kit compliance checker — v3.1.0

GENERATED. Do not hand-edit. Regenerate with:
    python3 scripts/build_design_system.py

Run it from the root of a project that uses the kit:

    python3 check-agustos-ui.py .

Standard library only, Python 3.9+. It reads files; it never writes them, and it
makes no network call unless you pass --update-check.

Exit codes: 0 clean (or warnings only), 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

KIT_VERSION = "3.1.0"
REPOSITORY = "Agustos-Teknoloji/DESIGN-agustos"
LATEST_KIT_URL = "https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@latest/ui/kit.json"

# hex value -> the variable that owns it. Injected from the token registry, so a
# vendored copy of this file cannot drift from the system it was cut from.
TOKEN_COLORS = {
    "#fefcf2": "--paper",
    "#ffffff": "--paper-white",
    "#1a1a1a": "--ink",
    "#4a4a4a": "--ink-soft",
    "#8a8a8a": "--ink-faint",
    "#e8e3d0": "--rule",
    "#e8e8e8": "--rule-white",
    "#16140f": "--paper",
    "#f0ebd8": "--ink",
    "#cf142a": "--signal",
    "#1f6b4a": "--state-success",
    "#8a5a00": "--state-warning",
    "#b42318": "--state-danger",
    "#1a4d8f": "--state-info",
}

KIT_CLASSES = {
    "type-hero",
    "type-hero-md",
    "type-hero-deck",
    "type-h1",
    "type-h2",
    "type-h3",
    "type-h4",
    "type-body",
    "type-link",
    "type-code",
    "type-blockquote",
    "type-pullquote",
    "type-list-ol",
    "type-list-ul",
    "type-dl",
    "type-figure",
    "type-code-block",
    "type-table",
    "type-divider",
    "type-footnote",
    "site-frame",
    "container",
    "skip-link",
    "brand-agustos",
    "brand-pataraz",
    "brand-pld",
    "brand-iesdesk",
    "brand-specquick",
    "paper-white",
    "hero-links",
    "hero-link",
    "hero-link--primary",
    "hero-link--secondary",
    "hero-actions",
    "hero-action",
    "hero-action--primary",
    "hero-action--secondary",
    "hero-trust",
    "hero-visual",
    "agustos-section",
    "agustos-section__head",
    "agustos-card-grid",
    "agustos-card",
    "agustos-card--marked",
    "agustos-chrome-link",
    "agustos-fieldset",
    "agustos-field",
    "agustos-field--invalid",
    "agustos-label",
    "agustos-label--required",
    "agustos-input",
    "agustos-textarea",
    "agustos-select",
    "agustos-check",
    "agustos-hint",
    "agustos-error",
    "agustos-button",
    "agustos-button--primary",
    "agustos-button--secondary",
    "agustos-button--quiet",
    "agustos-badge",
    "agustos-badge--success",
    "agustos-badge--warning",
    "agustos-badge--danger",
    "agustos-badge--info",
    "agustos-badge--signal",
    "agustos-notice",
    "agustos-notice__title",
    "agustos-notice--success",
    "agustos-notice--warning",
    "agustos-notice--danger",
    "agustos-notice--info",
    "agustos-tabs",
    "agustos-tab",
    "agustos-tabs__panel",
}

# #1a1a1a and #ffffff are legitimate as identity ink and as paper. Reported at
# warning level rather than error: too common to fail a build over.
SOFT_COLORS = {"#1a1a1a", "#ffffff"}

STALE_RED = "#d11d2b"
SIGNAL_RED = "#cf142a"
BRAND_CLASSES = ("brand-agustos", "brand-pataraz", "brand-pld", "brand-iesdesk", "brand-specquick")

# The kit's own files. agustos.css declares the tokens, and the docs quote them
# on purpose — policing either produces noise, not findings.
KIT_FILES = {
    "agustos.css", "agustos-fonts.css", "starter.html", "kit.json",
    "UI-KIT.md", "AGENTS-SNIPPET.md", "check-agustos-ui.py", "LICENSE",
}

SCAN_SUFFIXES = {
    ".html", ".htm", ".css", ".scss", ".sass", ".astro", ".erb", ".php",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".liquid", ".md",
}
SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", ".astro", ".next", ".cache",
    "vendor", "__pycache__", ".venv", "venv", "coverage",
}

HEX = re.compile(r"#([0-9a-fA-F]{6})\b")
RADIUS = re.compile(r"border-radius:\s*([0-9.]+)px")
GRADIENT = re.compile(r"(linear|radial|conic)-gradient\(")
BACKGROUND = re.compile(r"background(?:-color)?:\s*([^;{}]+)")
# A pseudo-element, or an explicit dimension of 16px or less, means the signal is
# painting a marker rather than a field.
MARKER = re.compile(r"::(?:before|after)|(?:width|height)\s*:\s*(?:[0-9]|1[0-6])px")
# `linear-gradient(var(--rule) 1px, transparent 1px)` draws a rule, not a wash.
HAIRLINE_GRID = re.compile(r"[123]px\s*,\s*transparent")
# Anchor on a rule or declaration boundary, not line start: `:root { --ink: … }`
# on one line is ordinary CSS and must still be caught.
CUSTOM_PROP = re.compile(r"(?:^|[;{])\s*(--(?:display|body|ink|paper|signal|brand|rule))\s*:", re.MULTILINE)
JSDELIVR = re.compile(r"cdn\.jsdelivr\.net/gh/" + re.escape(REPOSITORY) + r"(@[^/\s\"']*)?")
FONT_HINTS = (
    "agustos-fonts.css", "fontsource", "Inter+Tight", "InterTight",
    "@font-face", "inter-tight-variable",
)


class Finding:
    __slots__ = ("rule", "level", "path", "line", "message")

    def __init__(self, rule, level, path, line, message):
        self.rule, self.level, self.path, self.line, self.message = rule, level, path, line, message

    def render(self) -> str:
        where = f"{self.path}:{self.line}" if self.path else "—"
        return f"{self.level.upper():<5} {self.rule} {where:<44} {self.message}"

    def as_dict(self) -> dict:
        return {
            "rule": self.rule, "level": self.level,
            "file": self.path, "line": self.line, "message": self.message,
        }


def near(first: str, second: str) -> int:
    """Squared-ish RGB distance. Catches hand-typed near-misses."""
    a = [int(first[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(second[i:i + 2], 16) for i in (1, 3, 5)]
    return max(abs(x - y) for x, y in zip(a, b))


def scan_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in KIT_FILES:
            continue
        try:
            yield path, path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def check(root: Path) -> tuple[list, int]:
    findings: list = []
    scanned = 0
    corpus: list = []

    for path, text in scan_files(root):
        scanned += 1
        rel = str(path.relative_to(root))
        corpus.append(text)
        lines = text.splitlines()

        # Documentation legitimately quotes token values — that is its job. Only
        # the two rules that stay wrong in prose apply to Markdown: a stale red,
        # and an unpinned URL that teaches the reader a bad habit.
        prose = path.suffix.lower() == ".md"

        for number, line in enumerate(lines, 1):
            lowered = line.lower()

            if STALE_RED in lowered:
                findings.append(Finding(
                    "AG001", "error", rel, number,
                    f"stale brand red {STALE_RED} — brand red is {SIGNAL_RED}",
                ))

            for match in (() if prose else HEX.finditer(line)):
                value = "#" + match.group(1).lower()
                if value == STALE_RED:
                    continue
                owner = TOKEN_COLORS.get(value)
                if owner and value in SOFT_COLORS:
                    findings.append(Finding(
                        "AG003", "warn", rel, number,
                        f"{value} is a token value ({owner}); legitimate as identity ink, "
                        f"suspicious as a page color",
                    ))
                elif owner:
                    findings.append(Finding(
                        "AG002", "error", rel, number,
                        f"hardcoded {value} — use var({owner})",
                    ))
                else:
                    for token, name in TOKEN_COLORS.items():
                        if token not in SOFT_COLORS and near(value, token) <= 12:
                            findings.append(Finding(
                                "AG004", "warn", rel, number,
                                f"{value} is a near-miss for {token} — did you mean var({name})?",
                            ))
                            break

            for match in (() if prose else RADIUS.finditer(line)):
                if float(match.group(1)) > 10:
                    findings.append(Finding(
                        "AG010", "warn", rel, number,
                        f"border-radius: {match.group(1)}px exceeds the 10px system maximum",
                    ))

            if GRADIENT.search(line) and not prose and not HAIRLINE_GRID.search(line):
                findings.append(Finding(
                    "AG010", "warn", rel, number,
                    "gradients are on the forbidden list for this system",
                ))

            for match in (() if prose else BACKGROUND.finditer(line)):
                value = match.group(1)
                if SIGNAL_RED not in value.lower() and "var(--signal)" not in value:
                    continue
                if re.search(r"var\(--signal\)\s+([0-9]|10)%", value):
                    continue  # a tint inside color-mix, not a red field
                if MARKER.search(line):
                    continue  # a marker dot or rule bar — what signal red is for
                findings.append(Finding(
                    "AG011", "warn", rel, number,
                    "signal red is for links, focus, markers and small emphasis — "
                    "not a background",
                ))

            for match in JSDELIVR.finditer(line):
                pin = match.group(1) or ""
                if not re.fullmatch(r"@v\d+\.\d+\.\d+", pin):
                    findings.append(Finding(
                        "AG008", "error", rel, number,
                        f"unpinned kit URL ('{pin or 'no version'}') — pin it to @v{KIT_VERSION}; "
                        f"an unpinned link restyles this page without review",
                    ))

        if path.suffix.lower() in {".css", ".scss", ".sass"}:
            for match in CUSTOM_PROP.finditer(text):
                number = text[:match.start()].count("\n") + 1
                findings.append(Finding(
                    "AG012", "warn", rel, number,
                    f"redefining {match.group(1)} collides with the kit's own variable",
                ))
            for name in KIT_CLASSES:
                pattern = re.compile(r"^[^@\n]*\." + re.escape(name) + r"(?![\w-])[^\n{]*\{", re.MULTILINE)
                match = pattern.search(text)
                if match:
                    number = text[:match.start()].count("\n") + 1
                    findings.append(Finding(
                        "AG009", "warn", rel, number,
                        f"restyling .{name} — compose a new class instead of overriding the kit",
                    ))
                    break

    blob = "\n".join(corpus)

    if scanned and "agustos.css" not in blob:
        findings.append(Finding(
            "AG006", "error", "", 0,
            "agustos.css is never referenced — the project does not load the design system",
        ))
    if scanned and not any(hint in blob for hint in FONT_HINTS):
        findings.append(Finding(
            "AG005", "error", "", 0,
            "Inter Tight is in the font stack but never loaded — the page will render in "
            "system sans. Load agustos-fonts.css, or the @fontsource-variable packages",
        ))
    if scanned and not any(name in blob for name in BRAND_CLASSES):
        findings.append(Finding(
            "AG007", "error", "", 0,
            "no brand class found — <body> must carry one of: " + ", ".join(BRAND_CLASSES),
        ))

    return findings, scanned


def fetch_latest() -> str:
    import urllib.request
    with urllib.request.urlopen(LATEST_KIT_URL, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))["version"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a project against the Ağustos UI kit.")
    parser.add_argument("path", nargs="?", default=".", help="directory to scan (default: .)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", action="store_true", dest="as_json", help="machine-readable output")
    parser.add_argument("--update-check", action="store_true", help="ask the CDN for a newer kit")
    parser.add_argument("--version", action="version", version=f"agustos-ui-kit {KIT_VERSION}")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    if args.update_check:
        try:
            latest = fetch_latest()
        except Exception as error:
            print(f"update check failed: {error}", file=sys.stderr)
            return 2
        if latest == KIT_VERSION:
            print(f"kit v{KIT_VERSION} is current")
        else:
            print(f"kit v{KIT_VERSION} -> v{latest} available")
            print(f"  https://github.com/{REPOSITORY}/releases/tag/v{latest}")
        return 0

    findings, scanned = check(root)
    if scanned == 0:
        # "clean" after scanning nothing is the most dangerous output this tool
        # could produce. Point it at a real project directory.
        print(f"no scannable files under {root} — nothing was checked", file=sys.stderr)
        return 2
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warn"]

    if args.as_json:
        print(json.dumps({
            "kitVersion": KIT_VERSION,
            "filesScanned": scanned,
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": [f.as_dict() for f in findings],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"agustos-ui check · kit v{KIT_VERSION} · {scanned} files scanned")
        for finding in errors + warnings:
            print(finding.render())
        if not findings:
            print("clean")
        else:
            print(f"{len(errors)} error(s), {len(warnings)} warning(s)")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
