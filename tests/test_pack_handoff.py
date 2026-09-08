"""The slim handoff zip is the product. The repository is the factory."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "pack_handoff.py"


def load_packer():
    spec = importlib.util.spec_from_file_location("pack_handoff", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class PackHandoffTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packer = load_packer()
        cls.members = cls.packer.archive_members()
        cls.names = [name.split("/", 1)[1] for name, _ in cls.members]

    def test_kit_files_are_present_and_templates_are_not(self):
        self.assertIn("ui/agustos.css", self.names)
        self.assertIn("ui/agustos-fonts.css", self.names)
        self.assertIn("ui/UI-KIT.md", self.names)
        self.assertIn("ui/starter.html", self.names)
        self.assertIn("ui/check-agustos-ui.py", self.names)
        self.assertIn("ui/AGENTS-SNIPPET.md", self.names)
        self.assertIn("ui/kit.json", self.names)
        self.assertTrue(any(name.startswith("ui/fonts/") and name.endswith(".woff2") for name in self.names))
        self.assertFalse(any(name.endswith(".tmpl") for name in self.names))

    def test_factory_paths_are_absent(self):
        forbidden = (
            "scripts/build_design_system.py",
            "brand/build.py",
            "MEMORY.md",
            "adapters/astro/README.md",
            "tokens/design-system-handoff.json",
            "artifacts/agustos-design-system-v3.0.0.html",
        )
        for path in forbidden:
            self.assertNotIn(path, self.names, path)

    def test_each_house_brand_has_lockup_svgs(self):
        for slug in ("agustos", "pataraz", "pld", "iesdesk", "specquick"):
            for expression in ("positive", "negative", "mono"):
                name = f"logos/{slug}-lockup__{expression}.svg"
                self.assertIn(name, self.names, name)

    def test_standard_artifacts_are_present(self):
        for name in ("DESIGN.md", "fonts.html", "colour.html", "web.html", "brands.html"):
            self.assertIn(name, self.names, name)
        html = next(payload for name, payload in self.members if name.endswith("/web.html"))
        text = html.decode("utf-8")
        self.assertIn('href="ui/agustos.css"', text)
        self.assertIn("src=\"logos/pataraz-lockup__positive.svg\"", text)
        html = next(payload for name, payload in self.members if name.endswith("START-HERE.html"))
        text = html.decode("utf-8")
        self.assertIn('href="ui/agustos.css"', text)
        self.assertNotIn('href="../ui/agustos.css"', text)

    def test_zip_writes_and_stays_small(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "handoff.zip"
            written = self.packer.write_zip(destination)
            self.assertTrue(zipfile.is_zipfile(written))
            self.assertLess(written.stat().st_size, 1_200_000)


if __name__ == "__main__":
    unittest.main()
