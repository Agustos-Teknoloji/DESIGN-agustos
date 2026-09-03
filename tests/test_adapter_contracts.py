from __future__ import annotations

import json
import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AdapterContractTest(unittest.TestCase):
    def test_generated_css_adapters_share_v3_primitives(self):
        paths = [
            ROOT / "tokens" / "agustos.css",
            ROOT / "adapters" / "astro" / "src" / "styles" / "tokens.css",
            ROOT / "adapters" / "rails" / "app" / "assets" / "stylesheets" / "agustos" / "tokens.css",
            ROOT / "adapters" / "wordpress" / "assets" / "css" / "agustos.css",
        ]
        required = (
            "--measure-content: 920px",
            "--paper-white:",
            "#ffffff",
            "--signal: #cf142a",
            ".agustos-section",
            ".agustos-card-grid",
            ".agustos-chrome-link",
        )
        for path in paths:
            css = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                for primitive in required:
                    self.assertIn(primitive, css)
                self.assertIn("text-decoration-color: var(--signal)", css)
                self.assertNotIn("text-decoration-color: var(--brand)", css)
                self.assertNotRegex(css, r"\{\{[^}]+\}\}")

    def test_astro_uses_shared_frame_header_and_active_navigation(self):
        header = (ROOT / "adapters" / "astro" / "src" / "components" / "Header.astro").read_text(encoding="utf-8")
        self.assertIn('<header class="site-header">', header)
        self.assertIn("aria-current={isCurrent(item.href) ? 'page' : undefined}", header)
        self.assertIn('class="site-header__bar site-frame"', header)
        self.assertIn("@media (max-width: 1023px)", header)
        self.assertIn("(max-width: 1366px) and (hover: none) and (pointer: coarse)", header)

    def test_astro_layout_has_no_legacy_sidebar_contract(self):
        layout = (ROOT / "adapters" / "astro" / "src" / "layouts" / "BaseLayout.astro").read_text(encoding="utf-8")
        self.assertIn("<Header", layout)
        self.assertIn("<Footer", layout)
        self.assertNotIn("Sidebar", layout)
        self.assertNotIn("MobileHeader", layout)

    def test_rails_helper_defaults_to_white_and_preserves_brand_fallbacks(self):
        helper = (ROOT / "adapters" / "rails" / "app" / "helpers" / "agustos_theme_helper.rb").read_text(encoding="utf-8")
        self.assertIn("substrate: :white", helper)
        self.assertIn('classes << "paper-white" if config[:substrate] == :white', helper)
        self.assertIn("BRAND_CLASSES.fetch(config[:brand], BRAND_CLASSES[:agustos])", helper)
        self.assertIn("BRAND_WORDMARKS.fetch(agustos_theme_config[:brand], BRAND_WORDMARKS[:agustos])", helper)

    def test_rails_layout_uses_header_not_sidebar(self):
        layout = (ROOT / "adapters" / "rails" / "app" / "views" / "layouts" / "agustos.html.erb").read_text(encoding="utf-8")
        self.assertIn('agustos/shared/header', layout)
        self.assertNotIn('agustos/shared/sidebar', layout)

    def test_rails_lockup_contains_exact_eighteen_blades(self):
        lockup = (ROOT / "adapters" / "rails" / "app" / "views" / "agustos" / "shared" / "_brand_lockup.html.erb").read_text(encoding="utf-8")
        self.assertEqual(lockup.count("<path"), 18)
        self.assertIn("agustos_wordmark", lockup)

    def test_wordpress_bootstrap_enqueues_css_and_preserves_body_classes(self):
        functions = (ROOT / "adapters" / "wordpress" / "functions.php.example").read_text(encoding="utf-8")
        self.assertIn("wp_enqueue_style", functions)
        self.assertIn("$classes[] = 'brand-agustos'", functions)
        self.assertIn("$classes[] = 'paper-white'", functions)
        self.assertNotIn("$classes = array(", functions)

    def test_wordpress_theme_disables_uncontrolled_palette_values(self):
        theme = json.loads((ROOT / "adapters" / "wordpress" / "theme.json").read_text(encoding="utf-8"))
        self.assertFalse(theme["settings"]["color"]["custom"])
        self.assertFalse(theme["settings"]["color"]["defaultPalette"])
        self.assertFalse(theme["settings"]["typography"]["customFontSize"])
        self.assertEqual(theme["settings"]["layout"], {"contentSize": "920px", "wideSize": "1200px"})

    def test_ci_enforces_web_office_and_unit_contracts(self):
        workflow = (ROOT / ".github" / "workflows" / "design-system.yml").read_text(encoding="utf-8")
        self.assertIn("scripts/build_design_system.py --check", workflow)
        self.assertIn("scripts/check_office_artifacts.py --check", workflow)
        self.assertIn("unittest discover -s tests", workflow)

    def test_single_file_handoff_contains_tokens_rules_and_brand_registry(self):
        handoff = json.loads((ROOT / "tokens" / "design-system-handoff.json").read_text(encoding="utf-8"))
        self.assertEqual(handoff["version"], "3.0.0")
        self.assertEqual(handoff["system"]["brands"]["agustos"]["color"], "#cf142a")
        self.assertEqual(handoff["system"]["brands"]["pataraz"]["color"], "#1a1a1a")
        self.assertEqual(handoff["system"]["brands"]["pld"]["color"], "#1a1a1a")
        self.assertEqual(handoff["system"]["brands"]["iesdesk"]["color"], "#1a1a1a")
        self.assertEqual(handoff["system"]["brands"]["specquick"]["color"], "#1a1a1a")
        self.assertEqual(handoff["system"]["semantic"]["color"]["signal"], "#cf142a")
        self.assertEqual(handoff["system"]["recipes"]["chrome"]["contentMeasure"], "920px")
        self.assertGreaterEqual(len(handoff["contract"]["invariants"]), 6)
        self.assertGreaterEqual(len(handoff["contract"]["acceptance"]), 6)

    def test_single_file_handoff_embeds_the_canonical_symbol_exactly(self):
        handoff = json.loads((ROOT / "tokens" / "design-system-handoff.json").read_text(encoding="utf-8"))
        symbol = (ROOT / "laz-gunesi-amblem" / "svg" / "master.svg").read_text(encoding="utf-8")
        embedded = handoff["assets"]["symbol"]
        self.assertEqual(embedded["svg"], symbol)
        self.assertEqual(embedded["sha256"], hashlib.sha256(symbol.encode("utf-8")).hexdigest())
        self.assertIn("Preserve the embedded path geometry exactly", embedded["usageRule"])

    def test_active_brand_exports_use_red_only_for_agustos_identity(self):
        expected = {
            "agustos": "#cf142a",
            "pataraz": "#1a1a1a",
            "pld": "#1a1a1a",
            "iesdesk": "#1a1a1a",
            "specquick": "#1a1a1a",
        }
        retired = ("#1a24cc", "#0000ff", "#1f6b4a")
        for slug, color in expected.items():
            path = ROOT / "brand" / "exports" / slug / "lockup" / f"{slug}-lockup__positive.svg"
            svg = path.read_text(encoding="utf-8").lower()
            with self.subTest(slug=slug):
                self.assertIn(color, svg)
                if slug != "agustos":
                    for old_color in retired:
                        self.assertNotIn(old_color, svg)


if __name__ == "__main__":
    unittest.main()
