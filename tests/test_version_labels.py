"""Hand-written files that name the kit version must match VERSION.

The generator stamps VERSION into every generated file. DESIGN.md and the
hand-written handbook pages are not generated, so their version labels and
CDN pins drifted to 6.1.0 and 6.0.0 while VERSION moved on.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
HAND_WRITTEN_DOCS = sorted(
    path for path in (ROOT / "docs").glob("*.html") if path.name != "web.html"
)


class VersionLabelTest(unittest.TestCase):
    def test_design_md_names_the_current_version(self):
        text = (ROOT / "DESIGN.md").read_text(encoding="utf-8")
        self.assertIn(f"**Version {VERSION}**", text)
        self.assertIn(f"This is **v{VERSION}**.", text)

    def test_handbook_labels_and_pins_name_the_current_version(self):
        patterns = (
            r"Design System v(\d+\.\d+\.\d+)",
            r"DESIGN-agustos@v(\d+\.\d+\.\d+)",
            r"agustos-ui-handoff-v(\d+\.\d+\.\d+)",
        )
        for path in HAND_WRITTEN_DOCS:
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                for found in re.findall(pattern, text):
                    with self.subTest(file=path.name, pattern=pattern):
                        self.assertEqual(found, VERSION)


if __name__ == "__main__":
    unittest.main()
