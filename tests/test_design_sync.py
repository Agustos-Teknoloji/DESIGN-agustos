"""The sync script pushes the generated kit up and pulls Design pages down. It never edits either side's sources."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sync_claude_design.py"


def load_sync():
    spec = importlib.util.spec_from_file_location("sync_claude_design", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class BundleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sync = load_sync()
        cls.members = cls.sync.bundle_members()
        cls.names = [name for name, _ in cls.members]

    def test_kit_files_are_present_and_templates_are_not(self):
        for name in (
            "agustos.css",
            "agustos-fonts.css",
            "UI-KIT.md",
            "starter.html",
            "check-agustos-ui.py",
            "AGENTS-SNIPPET.md",
            "kit.json",
            "LICENSE",
        ):
            self.assertIn(name, self.names, name)
        self.assertTrue(any(n.startswith("fonts/") and n.endswith(".woff2") for n in self.names))
        self.assertFalse(any(n.endswith(".tmpl") for n in self.names))

    def test_each_house_brand_has_lockup_svgs_under_logos(self):
        for slug in ("agustos", "pataraz", "pld", "iesdesk", "specquick"):
            for expression in ("positive", "negative", "mono"):
                self.assertIn(f"logos/{slug}-lockup__{expression}.svg", self.names)

    def test_shared_favicon_kit_is_present(self):
        for name in ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "site.webmanifest"):
            self.assertIn(f"favicon/{name}", self.names, name)

    def test_favicon_svg_is_the_master_symbol(self):
        payload = dict(self.members)["favicon/favicon.svg"]
        master = (ROOT / "laz-gunesi-amblem" / "svg" / "master.svg").read_bytes()
        self.assertEqual(payload, master)

    def test_no_factory_paths(self):
        for name in self.names:
            self.assertFalse(name.startswith("tokens/"), name)
            self.assertFalse(name.startswith("scripts/"), name)
            self.assertFalse(name.startswith("brand/"), name)


class ManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sync = load_sync()
        cls.members = cls.sync.bundle_members()
        cls.manifest = cls.sync.manifest(cls.members, version="9.9.9", commit="abc1234")

    def test_manifest_hashes_match_kit_json(self):
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        for name, entry in kit["files"].items():
            self.assertEqual(self.manifest["files"][name]["sha256"], entry["sha256"], name)
            self.assertEqual(self.manifest["files"][name]["bytes"], entry["bytes"], name)

    def test_manifest_header(self):
        self.assertEqual(self.manifest["system"], "Ağustos Design System")
        self.assertEqual(self.manifest["version"], "9.9.9")
        self.assertEqual(self.manifest["commit"], "abc1234")
        self.assertEqual(self.manifest["remotePrefix"], "agustos-ui")
        self.assertEqual(self.manifest["source"], "Agustos-Teknoloji/DESIGN-agustos")

    def test_manifest_is_deterministic(self):
        again = self.sync.manifest(self.members, version="9.9.9", commit="abc1234")
        self.assertEqual(json.dumps(self.manifest, sort_keys=True), json.dumps(again, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
