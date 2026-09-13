"""The sync script pushes the generated kit up and pulls Design pages down. It never edits either side's sources."""

from __future__ import annotations

import importlib.util
import json
import re
import tempfile
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


class CardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sync = load_sync()
        cls.members = cls.sync.card_members(version="9.9.9")
        cls.texts = {name: payload.decode("utf-8") for name, payload in cls.members}

    def test_minimum_card_set(self):
        for slug in ("type", "colours", "actions", "brand-marks", "favicon"):
            self.assertIn(f"cards/{slug}.html", self.texts)

    def test_line_one_is_a_dscard_marker_with_kit_group(self):
        marker = re.compile(r'^<!-- @dsCard group="Kit · [^"]+" viewport="\d+x\d+" name="[^"]+" subtitle="[^"]+" -->$')
        for name, text in self.texts.items():
            first = text.splitlines()[0]
            self.assertRegex(first, marker, name)

    def test_cards_load_the_kit_by_relative_path_fonts_first(self):
        for name, text in self.texts.items():
            fonts = text.index('href="../agustos-fonts.css"')
            system = text.index('href="../agustos.css"')
            self.assertLess(fonts, system, name)

    def test_cards_carry_the_version(self):
        for name, text in self.texts.items():
            self.assertIn("v9.9.9", text, name)

    def test_favicon_card_points_at_the_bundled_favicon(self):
        self.assertIn('src="../favicon/favicon.svg"', self.texts["cards/favicon.html"])

    def test_brand_card_shows_every_house_lockup(self):
        text = self.texts["cards/brand-marks.html"]
        for slug in ("agustos", "pataraz", "pld", "iesdesk", "specquick"):
            self.assertIn(f'src="../logos/{slug}-lockup__positive.svg"', text)


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sync = load_sync()

    def build(self, **overrides):
        kwargs = dict(check=lambda root: True, clean=lambda root: True, commit=lambda root: "abc1234")
        kwargs.update(overrides)
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return self.sync.build_bundle(Path(temp.name), **kwargs)

    def test_build_writes_kit_cards_and_manifest_under_agustos_ui(self):
        folder = self.build()
        self.assertEqual(folder.name, "agustos-ui")
        self.assertTrue((folder / "agustos.css").is_file())
        self.assertTrue((folder / "logos" / "agustos-lockup__positive.svg").is_file())
        self.assertTrue((folder / "favicon" / "favicon.svg").is_file())
        self.assertTrue((folder / "cards" / "favicon.html").is_file())
        data = json.loads((folder / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(data["commit"], "abc1234")
        self.assertIn("cards/favicon.html", data["files"])
        self.assertIn("agustos.css", data["files"])

    def test_build_refuses_stale_generated_outputs(self):
        with self.assertRaises(self.sync.GuardError) as caught:
            self.build(check=lambda root: False)
        self.assertIn("build_design_system.py --check", str(caught.exception))

    def test_build_refuses_a_dirty_ui_folder(self):
        with self.assertRaises(self.sync.GuardError) as caught:
            self.build(clean=lambda root: False)
        self.assertIn("ui/", str(caught.exception))

    def test_build_replaces_a_previous_bundle(self):
        folder = self.build()
        stray = folder / "cards" / "old.html"
        stray.write_text("stale", encoding="utf-8")
        self.sync.build_bundle(folder.parent, check=lambda r: True, clean=lambda r: True, commit=lambda r: "abc1234")
        self.assertFalse(stray.exists())

    def test_real_guards_run_against_this_repository(self):
        self.assertTrue(self.sync.generated_outputs_are_current())
        self.assertRegex(self.sync.git_commit(), r"^[0-9a-f]{7,}$")


if __name__ == "__main__":
    unittest.main()
