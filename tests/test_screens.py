"""screens/ holds one reference page per row of the screens table, on kit classes only."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
KIT = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
CLASS_ATTR = re.compile(r'class="([^"]+)"')
SCRIPT = re.compile(r"<script[^>]*>(.*?)</script>", re.S)
MAIN = re.compile(r"<main\b.*?</main>", re.S)
PRIMARY = re.compile(r"\b(?:agustos-button--primary|hero-action--primary)\b")
FIRST_BLADE = '<path d="M 24.0215 4.2070'


def built() -> dict[str, str]:
    pages: dict[str, str] = {}
    for name, row in KIT["screens"].items():
        path = SCREENS / row["file"]
        if path.is_file():
            pages[name] = path.read_text(encoding="utf-8")
    return pages


class ScreensTableTest(unittest.TestCase):
    def test_every_row_has_a_file_and_every_file_has_a_row(self):
        files = sorted(p.name for p in SCREENS.glob("*.html"))
        rows = sorted(row["file"] for row in KIT["screens"].values())
        self.assertEqual(files, rows)


class ScreenFileTest(unittest.TestCase):
    def setUp(self):
        self.pages = built()
        self.assertTrue(self.pages, "no screen is built yet")

    def test_document_head_and_body_switches(self):
        for name, text in self.pages.items():
            row = KIT["screens"][name]
            with self.subTest(screen=name):
                lang = "en" if name == "app-shell" else "tr"
                self.assertIn(f'<html lang="{lang}">', text)
                self.assertLess(text.index('href="../ui/agustos-fonts.css"'), text.index('href="../ui/agustos.css"'))
                self.assertIn('href="../laz-gunesi-amblem/favicon/favicon.svg"', text)
                # The header comment (before <html>) mentions the <body> tag in prose, so
                # anchor the body-tag search past <html> to skip that false match.
                after_html = text.split("<html", 1)[1]
                body = re.search(r"<body\b([^>]*)>", after_html).group(1)
                self.assertIn(f"brand-{row['brand']}", body)
                self.assertIn(f'data-screen="{name}"', body)
                self.assertEqual("site-sidebar-layout" in body, row["chrome"] == "sidebar")
                self.assertIn("reference screen", text.split("<html", 1)[0])
                self.assertNotIn('data-theme="dark"', after_html.split("<body", 1)[0])

    def test_chrome_matches_the_brand(self):
        for name, text in self.pages.items():
            row = KIT["screens"][name]
            with self.subTest(screen=name):
                if row["chrome"] == "sidebar":
                    self.assertIn('class="site-sidebar" popover', text)
                    self.assertIn('popovertarget="site-sidebar"', text)
                    self.assertNotIn('class="site-header"', text)
                else:
                    self.assertIn('<header class="site-header">', text)
                    self.assertIn('<footer class="site-footer">', text)
                    self.assertIn('popovertarget="site-header-panel"', text)
                    self.assertNotIn("site-sidebar", text)
                self.assertEqual(text.count(FIRST_BLADE), text.count('class="site-lockup"'))
                self.assertGreaterEqual(text.count('class="site-lockup"'), 1)

    def test_kit_classes_only_and_no_inline_styling(self):
        kit_classes = set(KIT["cssClasses"])
        for name, text in self.pages.items():
            with self.subTest(screen=name):
                self.assertNotIn("<style", text)
                self.assertNotIn(" style=", text)
                used: set[str] = set()
                for value in CLASS_ATTR.findall(text):
                    used.update(value.split())
                self.assertEqual(used - kit_classes, set())
                self.assertNotRegex(text, r'src="https?://')
                self.assertNotRegex(text, r'href="https?://[^"]*\.(?:css|js)"')

    def test_scripts_only_in_the_app_shell_and_short(self):
        for name, text in self.pages.items():
            scripts = SCRIPT.findall(text)
            with self.subTest(screen=name):
                if name == "app-shell":
                    self.assertEqual(len(scripts), 1)
                    lines = [line for line in scripts[0].strip().splitlines() if line.strip()]
                    self.assertLessEqual(len(lines), 5)
                else:
                    self.assertEqual(scripts, [])

    def test_primary_cta_limit_and_quote_rule(self):
        for name, text in self.pages.items():
            row = KIT["screens"][name]
            main = MAIN.search(text).group(0)
            with self.subTest(screen=name):
                self.assertLessEqual(len(PRIMARY.findall(main)), row["primaryCtaMax"])
                if not row["quotes"]:
                    self.assertNotRegex(text, r"type-blockquote|type-pullquote")

    def test_checker_scores_the_folder_clean(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "ui" / "check-agustos-ui.py"), str(SCREENS), "--skip", "design"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
