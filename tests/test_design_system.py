from __future__ import annotations

import importlib.util
import copy
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_design_system.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_design_system", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class DesignSystemGenerationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_builder()
        cls.tokens = json.loads((ROOT / "tokens" / "design-tokens.json").read_text(encoding="utf-8"))

    def test_aliases_resolve_to_canonical_foundations(self):
        self.assertEqual(
            self.builder.resolve_token(self.tokens, "semantic.color.paper"),
            "#fefcf2",
        )

    def test_unknown_token_path_is_rejected(self):
        with self.assertRaisesRegex(self.builder.TokenError, "unknown token path"):
            self.builder.resolve_token(self.tokens, "foundations.color.missing")

    def test_circular_alias_is_rejected(self):
        tokens = copy.deepcopy(self.tokens)
        tokens["cycle"] = {
            "first": {"$value": "{cycle.second}"},
            "second": {"$value": "{cycle.first}"},
        }
        with self.assertRaisesRegex(self.builder.TokenError, "circular token alias"):
            self.builder.resolve_token(tokens, "cycle.first")

    def test_identity_and_signal_aliases_are_separate(self):
        self.assertEqual(
            self.builder.resolve_token(self.tokens, "semantic.color.brandMark"),
            "var(--brand)",
        )
        self.assertEqual(
            self.builder.resolve_token(self.tokens, "semantic.color.signal"),
            "#cf142a",
        )
        self.assertEqual(
            self.builder.resolve_token(self.tokens, "semantic.color.focus"),
            "#cf142a",
        )

    def test_resolved_tree_filters_registry_metadata(self):
        tree = self.builder.resolve_tree(
            self.tokens,
            {
                "$type": "dimension",
                "description": "not a token",
                "meta": {"owner": "system"},
                "compatibility": ["legacy"],
                "value": {"$value": "{foundations.spacing.md}"},
                "list": [1, {"$value": "{foundations.spacing.sm}"}],
            },
        )
        self.assertEqual(tree, {"value": "16px", "list": [1, "12px"]})

    def test_easing_supports_cubic_bezier_and_literal_fallback(self):
        self.assertEqual(
            self.builder.css_easing([0.2, 0, 0, 1]),
            "cubic-bezier(0.2, 0, 0, 1)",
        )
        self.assertEqual(self.builder.css_easing("linear"), "linear")

    def test_frame_measure_supports_pixel_and_calculated_units(self):
        self.assertEqual(self.builder.css_frame_measure(self.tokens), "968px")
        tokens = copy.deepcopy(self.tokens)
        tokens["foundations"]["measure"]["content"]["$value"] = "58rem"
        tokens["foundations"]["measure"]["gutter"]["$value"] = "1.5rem"
        self.assertEqual(
            self.builder.css_frame_measure(tokens),
            "calc(58rem + 1.5rem + 1.5rem)",
        )

    def test_render_web_css_resolves_headers_brands_and_tokens(self):
        brands = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            template = Path(directory) / "web.css.tmpl"
            template.write_text(
                "/* {{generated_header}} */\n.x{color:{{brands.agustos.color}};gap:{{foundations.spacing.md}}}",
                encoding="utf-8",
            )
            with mock.patch.object(self.builder, "WEB_TEMPLATE", template):
                rendered = self.builder.render_web_css(self.tokens, brands, "test adapter")
        self.assertIn("GENERATED TEST ADAPTER", rendered)
        self.assertIn("color:#cf142a", rendered)
        self.assertIn("gap:16px", rendered)

    def test_render_web_css_rejects_non_scalar_placeholder(self):
        brands = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            template = Path(directory) / "web.css.tmpl"
            template.write_text("{{foundations.spacing}}", encoding="utf-8")
            with mock.patch.object(self.builder, "WEB_TEMPLATE", template):
                with self.assertRaisesRegex(self.builder.TokenError, "must resolve to a scalar"):
                    self.builder.render_web_css(self.tokens, brands, "test")
        self.assertEqual(
            self.builder.resolve_token(self.tokens, "semantic.layout.contentMeasure"),
            "920px",
        )

    def test_expected_outputs_cover_all_web_adapters(self):
        relative = {str(path.relative_to(ROOT)) for path in self.builder.expected_outputs()}
        self.assertIn("tokens/agustos.css", relative)
        self.assertIn("adapters/astro/src/styles/tokens.css", relative)
        self.assertIn("adapters/rails/app/assets/stylesheets/agustos/tokens.css", relative)
        self.assertIn("adapters/wordpress/assets/css/agustos.css", relative)
        self.assertIn("adapters/wordpress/theme.json", relative)
        self.assertIn("tokens/design-system-handoff.json", relative)

    def test_resolved_registry_stays_platform_neutral(self):
        resolved = self.builder.resolve_tree(self.tokens, self.tokens["semantic"])
        self.assertEqual(resolved["color"]["brandMark"], "{brand.color}")
        self.assertEqual(resolved["color"]["signal"], "#cf142a")
        self.assertEqual(resolved["color"]["focus"], "#cf142a")

    def test_wordpress_theme_exposes_required_system_contract(self):
        brands = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        theme = self.builder.wordpress_theme(self.tokens, brands)
        palette = {item["slug"]: item["color"] for item in theme["settings"]["color"]["palette"]}
        self.assertEqual(theme["version"], 3)
        self.assertEqual(theme["settings"]["layout"]["contentSize"], "920px")
        self.assertEqual(palette["brand-agustos"], "#cf142a")
        self.assertEqual(palette["brand-pataraz"], "#1a1a1a")
        self.assertEqual(palette["signal"], "#cf142a")
        self.assertEqual(
            theme["styles"]["elements"]["link"]["color"]["text"],
            "var:preset|color|signal",
        )
        self.assertEqual(theme["styles"]["color"]["background"], "var:preset|color|paper-white")

    def test_handoff_contract_is_self_contained_and_platform_aware(self):
        brands = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        resolved = {
            "name": self.tokens["name"],
            "version": self.tokens["version"],
            "foundations": self.builder.resolve_tree(self.tokens, self.tokens["foundations"]),
            "semantic": self.builder.resolve_tree(self.tokens, self.tokens["semantic"]),
            "themes": self.builder.resolve_tree(self.tokens, self.tokens["themes"]),
            "recipes": self.builder.resolve_tree(self.tokens, self.tokens["recipes"]),
            "brands": brands["brands"],
        }
        handoff = self.builder.handoff_contract(resolved, self.tokens)
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(handoff["system"]["version"], version)
        self.assertIn("web", handoff["contract"]["mediums"])
        self.assertIn("document", handoff["contract"]["mediums"])
        self.assertIn("presentation", handoff["contract"]["mediums"])
        self.assertIn("family resemblance", handoff["contract"]["recognitionGoal"])
        self.assertIn("Pixel-identical", handoff["contract"]["recognitionGoal"])
        self.assertTrue(any("Never redraw" in rule for rule in handoff["contract"]["invariants"]))
        self.assertEqual(handoff["colorModel"]["interactionSignal"], "#cf142a")
        self.assertIn("<svg", handoff["assets"]["symbol"]["svg"])
        self.assertEqual(len(handoff["assets"]["symbol"]["sha256"]), 64)
        self.assertEqual(handoff["assets"]["symbol"]["embeddedColor"], "#cf142a")
        self.assertIn("replace only the fill color", handoff["assets"]["symbol"]["usageRule"])
        self.assertIn("do not run", handoff["distribution"]["consumerRule"])
        self.assertIn("cssClasses", handoff["compatibility"])

    def test_write_or_check_detects_drift_and_writes_nested_files(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            output = Path(directory) / "nested" / "generated.txt"
            outputs = {output: "expected\n"}
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(self.builder.write_or_check(outputs, check=True), 1)
            self.assertIn("generated design-system drift", stderr.getvalue())
            self.assertEqual(self.builder.write_or_check(outputs, check=False), 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "expected\n")
            self.assertEqual(self.builder.write_or_check(outputs, check=True), 0)

    def test_main_reports_token_errors_without_traceback(self):
        with mock.patch.object(self.builder, "expected_outputs", side_effect=self.builder.TokenError("bad token")):
            with mock.patch.object(sys, "argv", [str(SCRIPT), "--check"]):
                with contextlib.redirect_stderr(io.StringIO()) as stderr:
                    self.assertEqual(self.builder.main(), 2)
        self.assertIn("design-system generation failed: bad token", stderr.getvalue())

    def test_committed_outputs_do_not_drift(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
