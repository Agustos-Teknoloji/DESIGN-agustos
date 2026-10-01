from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "brand" / "build_guidelines.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_guidelines", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class GuidelinesContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_builder()
        cls.reg = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        cls.design = json.loads((ROOT / "tokens" / "resolved.json").read_text(encoding="utf-8"))
        cls.pages = {}
        with tempfile.TemporaryDirectory() as tmp:
            for slug, brand in cls.reg["brands"].items():
                if not brand.get("office", False):
                    continue
                out = Path(tmp) / f"{slug}.html"
                lockups = ROOT / "brand" / "exports" / slug / "lockup"
                cls.builder.gen_guidelines_html(slug, brand, cls.reg, cls.design, out, lockups, "0.0.0")
                cls.pages[slug] = out.read_text(encoding="utf-8")

    def test_every_full_kit_brand_has_guidelines(self):
        self.assertEqual(sorted(self.pages), ["agustos", "pataraz", "pld"])

    def test_fourteen_pages_with_every_section(self):
        # v7.6.0 adds "In every medium" after the introduction.
        self.assertEqual(len(self.builder.SECTIONS), 11)
        for slug, page in self.pages.items():
            with self.subTest(slug=slug):
                self.assertEqual(page.count('<section class="page'), 14)
                for number, title in enumerate(self.builder.SECTIONS, start=1):
                    self.assertIn(f'<h1><span class="n">{number}</span>{title}</h1>', page)

    def test_colours_come_from_the_registry(self):
        allowed = {v.lower() for v in self.design["foundations"]["color"].values()}
        allowed.add(self.design["semantic"]["color"]["signal"].lower())
        allowed |= {b["color"].lower() for b in self.reg["brands"].values()}
        for slug, page in self.pages.items():
            with self.subTest(slug=slug):
                used = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}\b", page)}
                self.assertEqual(used - allowed, set())

    def test_follows_the_writing_and_kit_rules(self):
        for slug, page in self.pages.items():
            with self.subTest(slug=slug):
                self.assertNotIn("\u2014", page, "no em dash")
                self.assertNotIn("uppercase", page, "no uppercase labels")
                self.assertNotIn("eyebrow", page, "no eyebrow headings")

    def test_colour_in_use_shows_every_registry_state(self):
        """v7.0.1: the states table reaches partners, not only developers."""
        for slug, page in self.pages.items():
            with self.subTest(slug=slug):
                self.assertEqual(page.count('<span class="pair"'), 2 * len(self.design["states"]))
                self.assertIn("Red is identity and signal, never action.", page)

    def test_typography_shows_the_thin_headings_from_the_registry(self):
        """v7.0.1: the page said headings were 650 while the web set them at 300 and 400."""
        weights = self.design["foundations"]["fontWeight"]
        for slug, page in self.pages.items():
            with self.subTest(slug=slug):
                self.assertNotIn("Wordmark, display, headings", page)
                self.assertIn(f"<b>Hero, Inter Tight {weights['light']}</b>89px", page)
                self.assertIn(f"<b>H2, Inter Tight {weights['regular']}</b>43px", page)
                self.assertIn(f"<b>Wordmark, Inter Tight {weights['wordmark']}</b>The logo only.", page)

    def test_emphasis_page_covers_every_tool(self):
        for slug, page in self.pages.items():
            with self.subTest(slug=slug):
                for tool in ("Red highlighter", "Bold (600)", "Italic", "Underline", "Colour and capitals"):
                    self.assertIn(f'<div class="k">{tool}</div>', page)

    def test_black_brands_warn_against_a_red_logo(self):
        signal = self.design["semantic"]["color"]["signal"].lower()
        for slug in ("pataraz", "pld"):
            with self.subTest(slug=slug):
                self.assertNotEqual(self.reg["brands"][slug]["color"].lower(), signal)
                self.assertIn(f"Never make the {self.reg['brands'][slug]['title']} logo red.", self.pages[slug])


if __name__ == "__main__":
    unittest.main()
