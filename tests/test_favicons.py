"""Tab icons are a transparent Laz Güneşi. Apple touch and PWA icons stay white.

MEMORY.md 2026-10-15 transparent-tab-favicons. Ağustos is red #cf142a.
Every other brand is black #15130f. Symbol paths come from master.svg, verbatim.
"""

from __future__ import annotations

import json
import re
import struct
import zlib
from pathlib import Path

import unittest

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "laz-gunesi-amblem" / "svg" / "master.svg"
CANONICAL = ROOT / "laz-gunesi-amblem" / "favicon"
EXPORTS = ROOT / "brand" / "exports"
ASTRO = ROOT / "adapters" / "astro" / "public" / "favicon.svg"
RED = "#cf142a"
BLACK = "#15130f"
WHITE = (255, 255, 255, 255)
CLEAR = (0, 0, 0, 0)

# Living docs that tell a consumer what a tab icon is. Historical logs stay out.
LIVING_DOCS = (
    "AGENTS.md",
    "ASSETS.md",
    "DESIGN.md",
    "PATARAZ.md",
    "brand/README.md",
    "docs/brands.html",
    "laz-gunesi-amblem/favicon/README.md",
    "brand/build_guidelines.py",
    "scripts/sync_claude_design.py",
)


def master_paths():
    text = MASTER.read_text(encoding="utf-8")
    return re.findall(r'<path[^>]*\bd="([^"]+)"', text)


def _paeth(left, up, up_left):
    estimate = left + up - up_left
    if abs(estimate - left) <= abs(estimate - up) and abs(estimate - left) <= abs(estimate - up_left):
        return left
    if abs(estimate - up) <= abs(estimate - up_left):
        return up
    return up_left


def png_rgba(blob: bytes):
    """Return (width, height, rows of RGBA bytes) for a non-interlaced 8-bit PNG."""
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError("not a PNG")
    pos = 8
    width = height = color = None
    idat = b""
    while pos + 8 <= len(blob):
        length = struct.unpack(">I", blob[pos:pos + 4])[0]
        kind = blob[pos + 4:pos + 8]
        chunk = blob[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            width, height, depth, color = struct.unpack(">IIBB", chunk[:10])
            interlace = chunk[12]
            if depth != 8 or color not in (2, 6) or interlace != 0:
                raise AssertionError(f"unsupported PNG depth={depth} color={color}")
        elif kind == b"IDAT":
            idat += chunk
        elif kind == b"IEND":
            break
        pos += 12 + length
    channels = 4 if color == 6 else 3
    stride = width * channels
    raw = zlib.decompress(idat)
    rows = []
    prev = bytearray(stride)
    index = 0
    for _y in range(height):
        filt = raw[index]
        index += 1
        row = bytearray(raw[index:index + stride])
        index += stride
        for x in range(stride):
            left = row[x - channels] if x >= channels else 0
            up = prev[x]
            up_left = prev[x - channels] if x >= channels else 0
            if filt == 0:
                extra = 0
            elif filt == 1:
                extra = left
            elif filt == 2:
                extra = up
            elif filt == 3:
                extra = (left + up) // 2
            elif filt == 4:
                extra = _paeth(left, up, up_left)
            else:
                raise AssertionError(f"bad PNG filter {filt}")
            row[x] = (row[x] + extra) & 255
        if color == 2:
            expanded = bytearray()
            for x in range(0, stride, 3):
                expanded += row[x:x + 3] + b"\xff"
            row = expanded
        prev = row
        rows.append(bytes(row))
    return width, height, rows


def rgba_at(rows, x, y):
    i = x * 4
    return tuple(rows[y][i:i + 4])


def png_corner(path: Path):
    width, height, rows = png_rgba(path.read_bytes())
    return (width, height), rgba_at(rows, 0, 0)


def ico_frames(path: Path):
    data = path.read_bytes()
    _reserved, kind, count = struct.unpack_from("<HHH", data, 0)
    if kind != 1:
        raise AssertionError(f"{path} is not an ICO")
    frames = []
    for i in range(count):
        width, height, _colors, _res, _planes, _bits, size, offset = struct.unpack_from(
            "<BBBBHHII", data, 6 + i * 16
        )
        width = 256 if width == 0 else width
        height = 256 if height == 0 else height
        frames.append((width, height, png_rgba(data[offset:offset + size])))
    return frames


class FaviconKitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        cls.paths = master_paths()

    def test_every_brand_tab_svg_has_no_tile_and_the_right_ink(self):
        self.assertEqual(len(self.paths), 18)
        seen = []
        for slug, brand in self.reg["brands"].items():
            svg_path = EXPORTS / slug / "favicon" / "favicon.svg"
            text = svg_path.read_text(encoding="utf-8")
            ink = RED if slug == "agustos" else BLACK
            with self.subTest(slug=slug):
                self.assertEqual(brand["color"].lower(), ink)
                self.assertNotIn("<rect", text)
                self.assertIn(f'<g fill="{ink}"', text)
                self.assertNotIn("#ffffff", text.lower())
                for d in self.paths:
                    self.assertIn(f'd="{d}"', text)
            seen.append(text)
        self.assertEqual(seen[0], (CANONICAL / "favicon.svg").read_text(encoding="utf-8"))
        black = seen[1:]
        self.assertGreaterEqual(len(black), 7)
        self.assertTrue(all(item == black[0] for item in black))

    def test_astro_default_is_the_black_transparent_tab_icon(self):
        text = ASTRO.read_text(encoding="utf-8")
        pataraz = (EXPORTS / "pataraz" / "favicon" / "favicon.svg").read_text(encoding="utf-8")
        agustos = (EXPORTS / "agustos" / "favicon" / "favicon.svg").read_text(encoding="utf-8")
        self.assertEqual(text, pataraz)
        self.assertNotEqual(text, agustos)
        self.assertIn(f'<g fill="{BLACK}"', text)
        self.assertNotIn("<rect", text)

    def test_ico_files_hold_16_32_and_48_with_transparency(self):
        folders = [CANONICAL] + [EXPORTS / slug / "favicon" for slug in self.reg["brands"]]
        for folder in folders:
            path = folder / "favicon.ico"
            frames = ico_frames(path)
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertEqual([(w, h) for w, h, _image in frames], [(16, 16), (32, 32), (48, 48)])
                for _w, _h, (_pw, _ph, rows) in frames:
                    self.assertEqual(rgba_at(rows, 0, 0), CLEAR)
                    self.assertTrue(any(row[i + 3] for row in rows for i in range(0, len(row), 4)))

    def test_apple_and_pwa_icons_are_white_backed(self):
        per_brand = {
            "apple-touch-icon.png": (180, 180),
            "favicon-192.png": (192, 192),
            "favicon-512.png": (512, 512),
        }
        for slug in self.reg["brands"]:
            folder = EXPORTS / slug / "favicon"
            for name, size in per_brand.items():
                with self.subTest(slug=slug, name=name):
                    got_size, pixel = png_corner(folder / name)
                    self.assertEqual(got_size, size)
                    self.assertEqual(pixel, WHITE)
        canonical = {
            "apple-touch-icon.png": (180, 180),
            "icon-192.png": (192, 192),
            "icon-512.png": (512, 512),
        }
        for name, size in canonical.items():
            got_size, pixel = png_corner(CANONICAL / name)
            self.assertEqual(got_size, size, name)
            self.assertEqual(pixel, WHITE, name)

    def test_tab_pngs_are_transparent(self):
        for slug in self.reg["brands"]:
            folder = EXPORTS / slug / "favicon"
            for name, size in (("favicon-16.png", (16, 16)), ("favicon-32.png", (32, 32))):
                with self.subTest(slug=slug, name=name):
                    got_size, pixel = png_corner(folder / name)
                    self.assertEqual(got_size, size)
                    self.assertEqual(pixel, CLEAR)
        for name, size in (("favicon-16.png", (16, 16)), ("favicon-32.png", (32, 32))):
            got_size, pixel = png_corner(CANONICAL / name)
            self.assertEqual(got_size, size, name)
            self.assertEqual(pixel, CLEAR, name)

    def test_living_docs_state_the_transparent_rule(self):
        stale = (
            "white tile with the",
            "red sun on white",
            "red sun on the white",
            "symbol on a white tile",
            "on a white square tile",
            "White tile, red",
        )
        for rel in LIVING_DOCS:
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("2026-10-15", text)
                self.assertIn("transparent", text.lower())
                for phrase in stale:
                    self.assertNotIn(phrase, text, phrase)


if __name__ == "__main__":
    unittest.main()
