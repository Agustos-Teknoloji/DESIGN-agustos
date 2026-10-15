"""The positive social avatar is a black sun on a white tile.

brand/build.py writes it for every non-Ağustos brand that already has a dark-tile
avatar. The paths match that avatar. Only the inks change. Ağustos has no
positive file. Its red sun is the transparent tab icon.
"""

from __future__ import annotations

import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "brand" / "exports"
MASTER = ROOT / "laz-gunesi-amblem" / "svg" / "master.svg"
WHITE = "#ffffff"
INK = "#15130f"


def svg_parts(text):
    rect = re.search(r'<rect[^>]*\bfill="(#[0-9a-fA-F]+)"', text)
    group = re.search(r'<g\b[^>]*\bfill="(#[0-9a-fA-F]+)"', text)
    paths = re.findall(r'<path\b[^>]*\bd="([^"]+)"', text)
    transform = re.search(r'transform="([^"]+)"', text)
    return rect.group(1).lower(), group.group(1).lower(), paths, transform.group(1)


def png_size(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{path} is not a PNG")
    return struct.unpack(">II", data[16:24])


class PositiveAvatarTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        cls.master_paths = re.findall(r'<path\b[^>]*\bd="([^"]+)"', MASTER.read_text(encoding="utf-8"))

    def test_engine_emits_the_positive_avatar_from_the_social_build(self):
        text = (ROOT / "brand" / "build.py").read_text(encoding="utf-8")
        self.assertIn("def positive_avatar_jobs", text)
        self.assertIn("png_jobs.extend(positive_avatar_jobs(slug, brand, reg))", text)
        self.assertIn('if slug == "agustos":\n        return []', text)

    def test_each_non_agustos_avatar_has_a_black_sun_on_white(self):
        seen = []
        for slug, brand in self.reg["brands"].items():
            social = EXPORTS / slug / "social"
            dark_path = social / f"{slug}-avatar.svg"
            pos_path = social / f"{slug}-avatar-positive.svg"
            with self.subTest(slug=slug):
                if slug == "agustos" or not dark_path.is_file():
                    self.assertFalse(pos_path.exists(), pos_path)
                    for size in (400, 1000):
                        self.assertFalse((social / f"{slug}-avatar-positive-{size}.png").exists())
                    continue
                seen.append(slug)
                self.assertEqual(brand["color"], INK)
                dark = svg_parts(dark_path.read_text(encoding="utf-8"))
                pos = svg_parts(pos_path.read_text(encoding="utf-8"))
                self.assertEqual(dark[0], INK)
                self.assertEqual(dark[1], WHITE)
                self.assertEqual(pos[0], WHITE)
                self.assertEqual(pos[1], INK)
                self.assertEqual(pos[2], dark[2])
                self.assertEqual(pos[2], self.master_paths)
                self.assertEqual(pos[3], dark[3])
                for size in (400, 1000):
                    png = social / f"{slug}-avatar-positive-{size}.png"
                    self.assertEqual(png_size(png), (size, size))
        self.assertEqual(seen, ["pataraz", "pld", "iesdesk", "specquick", "selimgunes"])


if __name__ == "__main__":
    unittest.main()
