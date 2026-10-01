"""The datasheet, guidelines and social-post HTML must reference fonts and images by paths
relative to the HTML file. An absolute file:/// URL names the folder that ran the
build, so the page falls back to system fonts on any other machine, in the handoff
zip, or after that folder is deleted."""

from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "brand"
REFERENCE = re.compile(r"""(?:url\(\s*['"]?|src=")([^'")]+)""")


def load(name):
    spec = importlib.util.spec_from_file_location(name, BRAND / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class ExportPathsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = json.loads((BRAND / "brands.json").read_text(encoding="utf-8"))
        design = json.loads((ROOT / "tokens" / "resolved.json").read_text(encoding="utf-8"))
        datasheet, guidelines = load("build_datasheet"), load("build_guidelines")
        social = load("build_social_posts")
        cls.builders = (datasheet, guidelines, social)
        cls.pages = {}
        cls.tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls.tmp.name)
        for key, product in datasheet.PRODUCTS.items():
            slug = product["brand"]
            out = tmp / "datasheet" / f"{key}.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            datasheet.gen_datasheet_html(slug, cls.reg["brands"][slug], cls.reg, product, design, out,
                                         BRAND / "exports" / slug / "lockup")
            cls.pages[out] = out.read_text(encoding="utf-8")
        for slug, brand in cls.reg["brands"].items():
            if not brand.get("office", False):
                continue
            out = tmp / "guidelines" / f"{slug}.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            guidelines.gen_guidelines_html(slug, brand, cls.reg, design, out,
                                           BRAND / "exports" / slug / "lockup", "0.0.0")
            cls.pages[out] = out.read_text(encoding="utf-8")
        for key, post in social.POSTS.items():
            for out in social.build_post(key, post, cls.reg, design, out_root=tmp / "social"):
                cls.pages[out] = out.read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_no_absolute_file_urls(self):
        for out, page in self.pages.items():
            with self.subTest(page=out.name):
                self.assertEqual(re.findall(r"file:[^'\")]*", page)[:1], [])

    def test_every_reference_resolves_from_the_html_file(self):
        for out, page in self.pages.items():
            refs = [r for r in REFERENCE.findall(page) if not r.startswith("data:")]
            with self.subTest(page=out.name):
                self.assertTrue(refs, "expected font and lockup references")
                for ref in refs:
                    self.assertFalse(Path(unquote(ref)).is_absolute(), ref)
                    self.assertTrue((out.parent / unquote(ref)).resolve().is_file(), ref)

    def test_paths_from_the_export_folder_reach_the_fonts(self):
        """From brand/exports/<brand>/datasheet/, the fonts sit three folders up."""
        for builder in self.builders:
            with self.subTest(builder=builder.__name__):
                out_dir = BRAND / "exports" / "pataraz" / "datasheet"
                url = builder.rel_url(BRAND / "fonts" / "inter" / "Inter[opsz,wght].ttf", out_dir)
                self.assertEqual(unquote(url), "../../../fonts/inter/Inter[opsz,wght].ttf")


if __name__ == "__main__":
    unittest.main()
