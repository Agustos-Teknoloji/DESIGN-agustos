#!/usr/bin/env python3
"""Build the slim zip another coding agent should receive.

The whole repository is the factory. This zip is the product.
Consumer agents copy ui/ and stop. They do not run generators.
"""

from __future__ import annotations

import argparse
import io
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
UI_DIR = ROOT / "ui"
LOCKUP_GLOB = "brand/exports/*/lockup/*.svg"
DOCS_HTML = ROOT / "docs" / "handoff-setup.html"
HANDOFF = ROOT / "HANDOFF.md"
SCREENS_DIR = ROOT / "screens"
FAVICON = ROOT / "laz-gunesi-amblem" / "favicon" / "favicon.svg"
ASSET_REF = re.compile(r"\.\./brand/datasheet-assets/([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)")

ZIP_README = """# Ağustos UI kit v{version}

Five standard artifacts sit at the root of this zip. Read them before you write markup.

1. `DESIGN.md` — contract: direction, colour, type, brands, principles.
2. `fonts.html` — type families and rules.
3. `colour.html` — substrate, ink, signal, identity, dark theme.
4. `web.html` — one live frame per screen type, with that screen's rules. The pages are in `screens/`.
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
    html = html.replace('href="agustos-fonts.css"', 'href="ui/agustos-fonts.css"')
    html = html.replace('href="agustos.css"', 'href="ui/agustos.css"')
    html = html.replace('href="../ui/agustos-fonts.css"', 'href="ui/agustos-fonts.css"')
    html = html.replace('href="../ui/agustos.css"', 'href="ui/agustos.css"')
    html = html.replace('href="../DESIGN.md"', 'href="DESIGN.md"')
    for slug in ("agustos", "pataraz", "pld", "iesdesk", "specquick"):
        html = html.replace(f"../brand/exports/{slug}/lockup/", "logos/")
    html = html.replace('src="../screens/', 'src="screens/').replace('href="../screens/', 'href="screens/')
    return html


def rewrite_setup_html(html: str) -> str:
    """Point kit stylesheets at the zip-root ui/ folder."""
    ver = version()
    return (
        html.replace('href="agustos-fonts.css"', 'href="ui/agustos-fonts.css"')
        .replace('href="agustos.css"', 'href="ui/agustos.css"')
        .replace('href="../ui/agustos-fonts.css"', 'href="ui/agustos-fonts.css"')
        .replace('href="../ui/agustos.css"', 'href="ui/agustos.css"')
        .replace('href="../ui/UI-KIT.md"', 'href="ui/UI-KIT.md"')
        .replace("python3 scripts/pack_handoff.py", "this zip is already packed")
        .replace(f"dist/agustos-ui-handoff-v{ver}.zip", "the archive you opened")
    )


def screen_files(root: Path = ROOT) -> list[Path]:
    return sorted((root / "screens").glob("*.html"))


def rewrite_screen_html(html: str) -> str:
    """Point a screen at the zip's logos/ and assets/ folders. The ui/ path already resolves."""
    html = html.replace('href="../laz-gunesi-amblem/favicon/favicon.svg"', 'href="../logos/favicon.svg"')
    return ASSET_REF.sub(r"../assets/\2", html)


def referenced_assets(root: Path = ROOT) -> list[Path]:
    """Every datasheet asset a screen references, from any brand, not just pataraz.

    Raises instead of silently dropping a reference whose file does not exist, so a broken
    <img> never ships quietly inside the handoff zip.
    """
    asset_root = root / "brand" / "datasheet-assets"
    refs: set[tuple[str, str]] = set()
    for path in screen_files(root):
        refs.update(ASSET_REF.findall(path.read_text(encoding="utf-8")))
    missing = sorted(f"{brand}/{name}" for brand, name in refs if not (asset_root / brand / name).is_file())
    if missing:
        raise FileNotFoundError(
            "screens reference datasheet assets that do not exist: " + ", ".join(missing)
        )
    brands_by_name: dict[str, set[str]] = {}
    for brand, name in refs:
        brands_by_name.setdefault(name, set()).add(brand)
    duplicates = sorted(name for name, brands in brands_by_name.items() if len(brands) > 1)
    if duplicates:
        raise ValueError(
            "datasheet asset filenames collide across brands in the flat assets/ zip folder: "
            + ", ".join(duplicates)
        )
    return sorted(asset_root / brand / name for brand, name in refs)


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
    members.append((f"{prefix}/logos/favicon.svg", FAVICON.read_bytes()))
    for path in screen_files(root):
        members.append((f"{prefix}/screens/{path.name}", rewrite_screen_html(path.read_text(encoding="utf-8")).encode("utf-8")))
    for path in referenced_assets(root):
        members.append((f"{prefix}/assets/{path.name}", path.read_bytes()))
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
