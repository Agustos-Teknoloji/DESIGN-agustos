"""Hard rule 5: anything clickable is at least 44px.

Breadcrumb links fill their 44px list item. A card whose heading holds a link
becomes the target: the link stretches over the card, and the other links in
the card stay above it. The checker warns (AG013) when a card has links but
none sits in a heading, because that card cannot become a target.
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT_CSS = (ROOT / "ui" / "agustos.css").read_text(encoding="utf-8")
CHECKER = ROOT / "ui" / "check-agustos-ui.py"


def rule_body(selector_pattern: str) -> str:
    match = re.search(selector_pattern + r"\s*\{([^}]*)\}", KIT_CSS)
    return match.group(1) if match else ""


class TargetCssTest(unittest.TestCase):
    def test_breadcrumb_link_fills_its_row(self):
        body = rule_body(r"\n\.breadcrumb__link")
        self.assertIn("min-height: var(--control-min)", body)
        self.assertIn("display: inline-flex", body)

    def test_card_heading_link_stretches_over_the_card(self):
        self.assertIn("position: relative", rule_body(r"\n\.agustos-card"))
        stretch = rule_body(r"\.agustos-card :is\(h2, h3, h4\) > a::after")
        self.assertIn('content: ""', stretch)
        self.assertIn("position: absolute", stretch)
        self.assertIn("inset: 0", stretch)

    def test_other_card_links_stay_clickable(self):
        lifted = rule_body(r"\.agustos-card a:not\(:is\(h2, h3, h4\) > a\)")
        self.assertIn("position: relative", lifted)
        self.assertIn("z-index: 1", lifted)

    def test_focus_ring_moves_to_the_card(self):
        ring = rule_body(r"\.agustos-card:has\(:is\(h2, h3, h4\) > a:focus-visible\)")
        self.assertIn("outline:", ring)
        self.assertIn("var(--signal)", ring)


class CardCheckerTest(unittest.TestCase):
    PAGE = (
        '<!doctype html><html lang="tr"><head>\n'
        '<link rel="stylesheet" href="/vendor/agustos-ui/agustos-fonts.css">\n'
        '<link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">\n'
        '</head><body class="brand-pataraz" data-screen="products">\n'
        '<main id="main">\n{cards}\n</main>\n</body></html>\n'
    )

    def _findings(self, pages: dict) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for name, cards in pages.items():
                (project / name).write_text(self.PAGE.format(cards=cards), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(project), "--json"],
                capture_output=True, text=True,
            )
            found = {name: [] for name in pages}
            for finding in json.loads(result.stdout)["findings"]:
                if finding["rule"] == "AG013":
                    found[finding["file"]].append(finding)
            return found

    def test_ag013_flags_cards_whose_links_sit_outside_a_heading(self):
        pages = {
            "heading-link.html": '<article class="agustos-card"><h3><a href="/a">A</a></h3><p>Text</p></article>',
            "heading-and-extra.html": (
                '<article class="agustos-card"><div><h2 class="type-h3"><a href="/a">A</a></h2>'
                '<p>Stock · <a href="/a.pdf">Sheet</a></p></div></article>'
            ),
            "body-link-only.html": '<article class="agustos-card"><h3>A</h3><p><a href="/a">More</a></p></article>',
            "no-links.html": '<div class="agustos-card"><p class="type-h4">Files</p><p>4,218</p></div>',
            "grid-only.html": '<div class="agustos-card-grid"><p><a href="/a">Loose</a></p></div>',
            "marked.html": '<article class="agustos-card agustos-card--marked"><p><a href="/a">More</a></p></article>',
        }
        found = self._findings(pages)
        expected = {
            "heading-link.html": 0,
            "heading-and-extra.html": 0,
            "body-link-only.html": 1,
            "no-links.html": 0,
            "grid-only.html": 0,
            "marked.html": 1,
        }
        for name, count in expected.items():
            with self.subTest(page=name):
                self.assertEqual(len(found[name]), count, found[name])
                for finding in found[name]:
                    self.assertEqual(finding["level"], "warn")
                    self.assertEqual(finding["line"], 6)

    def test_reference_screens_raise_no_ag013(self):
        pages = {page.name: page.read_text(encoding="utf-8") for page in (ROOT / "screens").glob("*.html")}
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for name, text in pages.items():
                (project / name).write_text(text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(project), "--json"],
                capture_output=True, text=True,
            )
            rules = [f for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG013"]
            self.assertEqual(rules, [])


if __name__ == "__main__":
    unittest.main()
