#!/usr/bin/env python3
"""Subset the master variable fonts into web woff2 for the ui/ distribution kit.

This script is deliberately NOT part of scripts/build_design_system.py. It needs
fonttools[woff2], which CI does not install, and the generated binaries change
only when the master fonts change. Same posture as brand/build.py: run it when
the sources move, then commit the output.

    ./.venv/bin/python scripts/build_ui_fonts.py

scripts/build_design_system.py only hashes the resulting files, so --check stays
dependency-free. Do not move this logic into that script.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "brand" / "fonts"
TARGET_DIR = ROOT / "ui" / "fonts"

# Unicode coverage. Latin-1 and Latin Extended-A carry every Turkish letter
# (ğĞıİşŞ live in Extended-A; çÇöÖüÜ in Latin-1). General Punctuation carries the
# typographic quotes and dashes the type scale assumes. U+20BA is the lira sign —
# non-negotiable for a Turkish company.
UNICODES = ",".join([
    "U+0000-00FF",   # Basic Latin + Latin-1 Supplement
    "U+0100-017F",   # Latin Extended-A (Turkish)
    "U+0180-024F",   # Latin Extended-B
    "U+0300-036F",   # Combining diacritical marks
    "U+2000-206F",   # General Punctuation — “ ” ‘ ’ — – …
    "U+20A0-20BF",   # Currency symbols, including ₺ (U+20BA)
    "U+2122",        # ™
    "U+2190-2193",   # arrows used in chrome and tables
    "U+2212",        # true minus
    "U+25CF",        # bullet used by list markers
])

# locl is mandatory: it is what makes Turkish capitalization correct, and the
# generated CSS already switches it on. kern and ss01 are likewise referenced by
# `font-feature-settings` in the reset.
LAYOUT_FEATURES = "locl,kern,ss01,liga,clig,calt,tnum,frac,sups,subs,zero,ccmp,mark,mkmk"

FONTS = [
    ("inter-tight/InterTight[wght].ttf",             "inter-tight-variable.woff2"),
    ("inter-tight/InterTight-Italic[wght].ttf",      "inter-tight-variable-italic.woff2"),
    ("inter/Inter[opsz,wght].ttf",                   "inter-variable.woff2"),
    ("inter/Inter-Italic[opsz,wght].ttf",            "inter-variable-italic.woff2"),
    ("jetbrains-mono/JetBrainsMono[wght].ttf",       "jetbrains-mono-variable.woff2"),
]

# The OFL requires its text to travel with the fonts.
LICENSES = [
    ("inter-tight/OFL.txt",    "OFL-inter-tight.txt"),
    ("inter/OFL.txt",          "OFL-inter.txt"),
    ("jetbrains-mono/OFL.txt", "OFL-jetbrains-mono.txt"),
]


def main() -> int:
    try:
        from fontTools import subset
    except ImportError:
        print(
            "fonttools is required. Install it into the repo venv:\n"
            "  python3 -m venv .venv && ./.venv/bin/pip install -r brand/requirements.txt\n"
            "then run: ./.venv/bin/python scripts/build_ui_fonts.py",
            file=sys.stderr,
        )
        return 2

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    for relative, name in FONTS:
        source = SOURCE_DIR / relative
        if not source.exists():
            print(f"missing master font: {relative}", file=sys.stderr)
            return 2
        target = TARGET_DIR / name
        subset.main([
            str(source),
            f"--output-file={target}",
            "--flavor=woff2",
            f"--unicodes={UNICODES}",
            f"--layout-features={LAYOUT_FEATURES}",
            # Keep every variable axis at full range. Instancing here would
            # silently cost the wordmark its 650 weight.
            "--drop-tables+=DSIG",
            "--name-IDs=*",
            "--no-hinting",
            "--desubroutinize",
        ])
        saved = 100 - (target.stat().st_size * 100 // source.stat().st_size)
        print(f"generated ui/fonts/{name}  ({target.stat().st_size // 1024} KB, -{saved}%)")

    for relative, name in LICENSES:
        (TARGET_DIR / name).write_bytes((SOURCE_DIR / relative).read_bytes())
        print(f"copied    ui/fonts/{name}")

    print("\nNow run: python3 scripts/build_design_system.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
