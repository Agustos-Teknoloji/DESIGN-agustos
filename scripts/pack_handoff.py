#!/usr/bin/env python3
"""Build the slim zip another coding agent should receive.

The whole repository is the factory. This zip is the product.
Consumer agents copy ui/ and stop. They do not run generators.
"""

from __future__ import annotations

import argparse
import io
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
UI_DIR = ROOT / "ui"
LOCKUP_GLOB = "brand/exports/*/lockup/*.svg"
DOCS_HTML = ROOT / "docs" / "handoff-setup.html"
HANDOFF = ROOT / "HANDOFF.md"

ZIP_README = """# Ağustos UI kit v{version}

Five standard artifacts sit at the root of this zip. Read them before you write markup.

1. `DESIGN.md` — contract: direction, colour, type, brands, principles.
2. `fonts.html` — type families and rules.
3. `colour.html` — substrate, ink, signal, identity, dark theme.
4. `web.html` — header, footer, homepage, listing, finder, product page, spec sheet.
5. `brands.html` — house brands and lockup expressions.

Then copy `ui/` to `vendor/agustos-ui/` and commit it.
Load `agustos-fonts.css` then `agustos.css`. Put a `brand-*` class on `<body>`.
Run `python3 vendor/agustos-ui/check-agustos-ui.py .`

Logos are in `logos/`. Do not redraw the sun. Do not run any build script.
"""

HANDBOOK = (
    ROOT / "docs" / "fonts.html",
    ROOT / "docs" / "colour.html",
    ROOT / "docs" / "web.html",
    ROOT / "docs" / "brands.html",
)


def version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def kit_files(root: Path = ROOT) -> list[Path]:
    files: list[Path] = []
    for path in sorted((root / "ui").rglob("*")):
        if path.is_file() and path.suffix != ".tmpl":
            files.append(path)
    return files


def lockup_svgs(root: Path = ROOT) -> list[Path]:
    return sorted((root / "brand" / "exports").glob("*/lockup/*.svg"))


def rewrite_handbook_html(html: str) -> str:
    """Point kit and lockup paths at the zip root."""
    html = html.replace('href="../ui/agustos-fonts.css"', 'href="ui/agustos-fonts.css"')
    html = html.replace('href="../ui/agustos.css"', 'href="ui/agustos.css"')
    html = html.replace('href="../DESIGN.md"', 'href="DESIGN.md"')
    for slug in ("agustos", "pataraz", "pld", "iesdesk", "specquick"):
        html = html.replace(f"../brand/exports/{slug}/lockup/", "logos/")
    return html


def rewrite_setup_html(html: str) -> str:
    """Point kit stylesheets at the zip-root ui/ folder."""
    return (
        html.replace('href="../ui/agustos-fonts.css"', 'href="ui/agustos-fonts.css"')
        .replace('href="../ui/agustos.css"', 'href="ui/agustos.css"')
        .replace('href="../ui/UI-KIT.md"', 'href="ui/UI-KIT.md"')
        .replace("python3 scripts/pack_handoff.py", "this zip is already packed")
        .replace("dist/agustos-ui-handoff-v5.0.0.zip", "the archive you opened")
    )


def archive_members(root: Path = ROOT) -> list[tuple[str, bytes]]:
    """Return (archive path, payload) pairs for the slim zip."""
    ver = version()
    prefix = f"agustos-ui-handoff-v{ver}"
    members: list[tuple[str, bytes]] = [
        (f"{prefix}/README.md", ZIP_README.format(version=ver).encode("utf-8")),
        (f"{prefix}/VERSION", f"{ver}\n".encode("utf-8")),
        (f"{prefix}/DESIGN.md", (ROOT / "DESIGN.md").read_bytes()),
        (f"{prefix}/HANDOFF.md", HANDOFF.read_bytes()),
        (
            f"{prefix}/START-HERE.html",
            rewrite_setup_html(DOCS_HTML.read_text(encoding="utf-8")).encode("utf-8"),
        ),
    ]
    for path in HANDBOOK:
        members.append((f"{prefix}/{path.name}", rewrite_handbook_html(path.read_text(encoding="utf-8")).encode("utf-8")))
    for path in kit_files(root):
        members.append((f"{prefix}/{path.relative_to(root).as_posix()}", path.read_bytes()))
    for path in lockup_svgs(root):
        members.append((f"{prefix}/logos/{path.name}", path.read_bytes()))
    return members


def write_zip(destination: Path | None = None) -> Path:
    ver = version()
    if destination is None:
        destination = ROOT / "dist" / f"agustos-ui-handoff-v{ver}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    members = archive_members()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload in members:
            archive.writestr(name, payload)
    destination.write_bytes(buffer.getvalue())
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list",
        action="store_true",
        help="print archive paths instead of writing a zip",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="zip path (default: dist/agustos-ui-handoff-v<VERSION>.zip)",
    )
    args = parser.parse_args()
    members = archive_members()
    if args.list:
        for name, payload in members:
            print(f"{len(payload):8}  {name}")
        print(f"{len(members)} files")
        return 0
    path = write_zip(args.output)
    size = path.stat().st_size
    print(f"wrote {path.relative_to(ROOT)} ({size} bytes, {len(members)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
