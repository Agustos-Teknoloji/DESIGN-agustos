"""Tests for the v3.1 UI primitives and the ui/ distribution kit.

The class-list test is the important one: `compatibility.cssClasses` is the
public API this system publishes to other codebases, and until v3.1 nothing
verified that a listed class actually existed in the generated CSS.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "tokens" / "design-tokens.json").read_text(encoding="utf-8"))

CSS_OUTPUTS = (
    ROOT / "tokens" / "agustos.css",
    ROOT / "adapters" / "astro" / "src" / "styles" / "tokens.css",
    ROOT / "adapters" / "rails" / "app" / "assets" / "stylesheets" / "agustos" / "tokens.css",
    ROOT / "adapters" / "wordpress" / "assets" / "css" / "agustos.css",
)

DARK_PAPER = "#16140f"
LIGHT_SUBSTRATES = ("#ffffff", "#fefcf2")


def _relative_luminance(hex_color: str) -> float:
    value = hex_color.lstrip("#")
    channels = []
    for index in (0, 2, 4):
        channel = int(value[index:index + 2], 16) / 255
        channels.append(channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: str, background: str) -> float:
    first, second = _relative_luminance(foreground), _relative_luminance(background)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


class PublishedClassListTest(unittest.TestCase):
    def test_every_declared_class_exists_in_every_generated_stylesheet(self):
        declared = TOKENS["compatibility"]["cssClasses"]
        self.assertGreater(len(declared), 60, "the published class list looks truncated")
        for path in CSS_OUTPUTS:
            css = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                for name in declared:
                    self.assertRegex(
                        css,
                        r"\." + re.escape(name) + r"(?![\w-])",
                        f"{name} is published but has no rule in {path.name}",
                    )

    def test_declared_class_list_has_no_duplicates(self):
        declared = TOKENS["compatibility"]["cssClasses"]
        self.assertEqual(len(declared), len(set(declared)))

    def test_handoff_republishes_the_same_class_list(self):
        handoff = json.loads((ROOT / "tokens" / "design-system-handoff.json").read_text(encoding="utf-8"))
        self.assertEqual(
            handoff["compatibility"]["cssClasses"],
            TOKENS["compatibility"]["cssClasses"],
        )


class PrimitiveTest(unittest.TestCase):
    GROUPS = (
        ".agustos-input", ".agustos-textarea", ".agustos-select", ".agustos-check",
        ".agustos-label", ".agustos-hint", ".agustos-error",
        ".agustos-button", ".agustos-badge", ".agustos-notice", ".agustos-tab",
    )

    def test_primitives_reach_every_adapter(self):
        for path in CSS_OUTPUTS:
            css = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                for selector in self.GROUPS:
                    self.assertIn(selector, css)

    def test_button_aliases_the_hero_action_definition(self):
        """One visual definition. A second rule block would drift."""
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        self.assertIn(".hero-action,\n.agustos-button {", css)
        self.assertIn(".hero-action--primary,\n.agustos-button--primary {", css)

    def test_controls_meet_the_minimum_target_size(self):
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        for block in (".agustos-input,", ".agustos-check {", ".agustos-tab {"):
            start = css.index(block)
            self.assertIn("min-height: var(--control-min)", css[start:start + 700], block)

    def test_inputs_do_not_trigger_ios_focus_zoom(self):
        """Below 16px iOS Safari zooms the viewport on focus."""
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        start = css.index(".agustos-input,\n.agustos-textarea,\n.agustos-select {")
        self.assertIn("font-size: 16px", css[start:start + 900])

    def test_reduced_motion_is_honoured(self):
        """The handoff contract's acceptance list promises this."""
        for path in CSS_OUTPUTS:
            css = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("@media (prefers-reduced-motion: reduce)", css)

    def test_no_radius_exceeds_the_system_maximum(self):
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        for raw in re.findall(r"border-radius:\s*([0-9.]+)px", css):
            self.assertLessEqual(float(raw), 10.0, "10px is the largest radius in this system")

    def test_signal_red_is_never_a_solid_background(self):
        """`forbidden`: signal red as unrestricted background or decoration.

        A small share inside color-mix is a tint, not a red field — the primary
        button's hover has warmed ink with 8% signal since v3.0. Anything above
        10% is a red background wearing a function call.
        """
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        for declaration in re.findall(r"\n\s*background(?:-color)?:\s*([^;]+);", css):
            if "var(--signal)" not in declaration and "#cf142a" not in declaration.lower():
                continue
            share = re.search(r"var\(--signal\)\s+(\d+)%", declaration)
            self.assertIsNotNone(share, f"signal used as a solid background: {declaration}")
            self.assertLessEqual(int(share.group(1)), 10, declaration)


class StateColorContrastTest(unittest.TestCase):
    """The four light-substrate state colors score 2.19-3.11 on dark paper.

    They were unused before v3.1, so the failure was latent. The moment a badge
    or notice consumes them, dark theme ships unreadable text.
    """

    ROLES = ("Success", "Warning", "Danger", "Info")

    def _color(self, name: str) -> str:
        return TOKENS["foundations"]["color"][name]["$value"]

    def test_light_state_colors_pass_on_both_light_substrates(self):
        for role in self.ROLES:
            color = self._color(f"state{role}")
            for substrate in LIGHT_SUBSTRATES:
                with self.subTest(role=role, substrate=substrate):
                    self.assertGreaterEqual(contrast_ratio(color, substrate), 4.5)

    def test_dark_state_colors_exist_and_pass_on_dark_paper(self):
        self.assertEqual(TOKENS["foundations"]["color"]["paperDark"]["$value"], DARK_PAPER)
        for role in self.ROLES:
            color = self._color(f"state{role}Dark")
            with self.subTest(role=role):
                self.assertGreaterEqual(contrast_ratio(color, DARK_PAPER), 4.5)

    def test_dark_theme_block_overrides_every_state_color(self):
        for path in CSS_OUTPUTS:
            css = path.read_text(encoding="utf-8")
            start = css.index('html[data-theme="dark"] {')
            block = css[start:css.index("}", start)]
            with self.subTest(path=path.relative_to(ROOT)):
                for role in self.ROLES:
                    self.assertIn(f"--state-{role.lower()}:", block)


class VersionTest(unittest.TestCase):
    def test_version_sources_agree_and_are_three_segment_semver(self):
        version_file = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        handoff = json.loads((ROOT / "tokens" / "design-system-handoff.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "tokens" / "generated-manifest.json").read_text(encoding="utf-8"))
        self.assertRegex(version_file, r"^\d+\.\d+\.\d+$")
        self.assertEqual(TOKENS["version"], version_file)
        self.assertEqual(handoff["version"], version_file)
        self.assertEqual(manifest["version"], version_file)


class StaleValueTest(unittest.TestCase):
    def test_no_stale_red_in_generated_output(self):
        for path in CSS_OUTPUTS:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("d11d2b", path.read_text(encoding="utf-8").lower())


class DistributionKitTest(unittest.TestCase):
    KIT = ROOT / "ui"

    def test_kit_css_matches_the_canonical_stylesheet_except_its_header(self):
        canonical = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8").splitlines()
        kit = (self.KIT / "agustos.css").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(canonical), len(kit))
        differences = [i for i, (a, b) in enumerate(zip(canonical, kit)) if a != b]
        self.assertEqual(differences, [0], "only the generated header label may differ")

    def test_font_css_declares_every_registry_font_under_both_stack_names(self):
        css = (self.KIT / "agustos-fonts.css").read_text(encoding="utf-8")
        for entry in TOKENS["distribution"]["fonts"]:
            with self.subTest(file=entry["file"]):
                self.assertIn(f"url('./fonts/{entry['file']}')", css)
                for family in entry["families"]:
                    self.assertIn(f"font-family: '{family}';", css)

    def test_font_urls_are_relative_so_cdn_and_vendored_both_resolve(self):
        css = (self.KIT / "agustos-fonts.css").read_text(encoding="utf-8")
        for url in re.findall(r"url\('([^']+)'\)", css):
            self.assertTrue(url.startswith("./fonts/"), url)
            self.assertTrue((self.KIT / url[2:]).exists(), f"{url} does not exist")

    def test_every_shipped_font_is_a_real_woff2(self):
        for entry in TOKENS["distribution"]["fonts"]:
            path = self.KIT / "fonts" / entry["file"]
            with self.subTest(file=entry["file"]):
                self.assertTrue(path.exists())
                self.assertEqual(path.read_bytes()[:4], b"wOF2")

    def test_font_licenses_travel_with_the_binaries(self):
        """The OFL requires it."""
        licenses = list((self.KIT / "fonts").glob("OFL-*.txt"))
        self.assertEqual(len(licenses), 3, "one OFL per font family")

    def test_font_face_families_match_the_heads_of_the_css_stacks(self):
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        declared = {
            family
            for entry in TOKENS["distribution"]["fonts"]
            for family in entry["families"]
        }
        for variable in ("--display", "--body", "--mono"):
            stack = re.search(rf"{variable}:\s*([^;]+);", css).group(1)
            head = re.findall(r"'([^']+)'", stack)[:2]
            for family in head:
                with self.subTest(variable=variable, family=family):
                    self.assertIn(family, declared, f"{family} leads {variable} but has no @font-face")

    def test_every_cdn_url_in_the_kit_is_version_pinned(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        pattern = re.compile(r"cdn\.jsdelivr\.net/gh/[\w.-]+/[\w.-]+(@[^/\s\"']*)?")
        for path in sorted(self.KIT.rglob("*")):
            if not path.is_file() or path.suffix in {".woff2", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for line_number, line in enumerate(text.splitlines(), 1):
                for match in pattern.finditer(line):
                    pin = match.group(1) or ""
                    if pin == "@latest" and re.search(r"latest_?[kK]it_?[uU]rl", line, re.I):
                        continue  # the one documented exception: data, not a stylesheet
                    with self.subTest(path=path.name, line=line_number):
                        self.assertEqual(pin, f"@v{version}", line.strip())

    def test_entry_point_stays_short_enough_to_be_read_whole(self):
        lines = (self.KIT / "UI-KIT.md").read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(lines), 170, "UI-KIT.md is the one file an agent reads in full")

    def test_entry_point_documents_every_published_class(self):
        text = (self.KIT / "UI-KIT.md").read_text(encoding="utf-8")
        for name in TOKENS["compatibility"]["cssClasses"]:
            with self.subTest(name=name):
                stem = name.split("--")[0] if name.startswith("agustos-") else name
                self.assertTrue(
                    name in text or stem in text,
                    f"{name} is published but never mentioned in the entry point",
                )

    def test_kit_json_hashes_match_what_is_on_disk(self):
        import hashlib
        kit = json.loads((self.KIT / "kit.json").read_text(encoding="utf-8"))
        for name, meta in kit["files"].items():
            path = self.KIT / name
            with self.subTest(name=name):
                self.assertTrue(path.exists())
                payload = path.read_bytes()
                self.assertEqual(len(payload), meta["bytes"])
                self.assertEqual(hashlib.sha256(payload).hexdigest(), meta["sha256"])

    def test_kit_json_head_snippet_loads_fonts_before_the_system(self):
        kit = json.loads((self.KIT / "kit.json").read_text(encoding="utf-8"))
        snippet = kit["headSnippet"]
        self.assertLess(
            snippet.index("agustos-fonts.css"),
            snippet.index("agustos.css\""),
            "fonts must load first or the page renders in system sans",
        )

    def test_stale_red_appears_only_where_it_is_named_as_stale(self):
        """The checker and the docs must say the word; nothing may use the value."""
        for path in sorted(self.KIT.rglob("*")):
            if not path.is_file() or path.suffix in {".woff2", ".txt"}:
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if "d11d2b" not in line.lower():
                    continue
                with self.subTest(path=path.name, line=number):
                    self.assertIn(
                        "stale", line.lower(),
                        f"{path.name}:{number} uses the retired red as a value",
                    )


class SourceHashTest(unittest.TestCase):
    def test_version_participates_in_the_source_hash(self):
        """Without this, a version bump without a rebuild leaves every pinned
        URL in the kit stale while --check still reports clean."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "build_design_system", ROOT / "scripts" / "build_design_system.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        before = json.loads(module.expected_outputs()[ROOT / "tokens" / "generated-manifest.json"])
        version_file = ROOT / "VERSION"
        original = version_file.read_bytes()
        try:
            version_file.write_text("9.9.9\n", encoding="utf-8")
            with self.assertRaises(module.TokenError):
                module.expected_outputs()
        finally:
            version_file.write_bytes(original)

        after = json.loads(module.expected_outputs()[ROOT / "tokens" / "generated-manifest.json"])
        self.assertEqual(before["source_sha256"], after["source_sha256"])
        self.assertIn("VERSION", (ROOT / "scripts" / "build_design_system.py").read_text(encoding="utf-8"))


class CheckerTest(unittest.TestCase):
    CHECKER = ROOT / "ui" / "check-agustos-ui.py"

    def _run(self, directory: Path, *flags: str):
        import subprocess, sys as _sys
        return subprocess.run(
            [_sys.executable, str(self.CHECKER), str(directory), *flags],
            capture_output=True, text=True,
        )

    def test_checker_passes_on_the_reference_render(self):
        """If our own reference page fails our own checker, everything
        downstream is noise."""
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            # starter.html is excluded as a kit file; a consuming project would
            # name it something of its own.
            shutil.copyfile(ROOT / "ui" / "starter.html", project / "index.html")
            result = self._run(project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_checker_reports_each_rule_on_a_deliberately_bad_project(self):
        import tempfile
        bad_html = (
            '<!doctype html><html lang="tr"><head>\n'
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/'
            'Agustos-Teknoloji/DESIGN-agustos@main/ui/agustos.css">\n'
            '</head><body>\n'
            '<h1 style="color: #D11D2B">stale</h1>\n'
            '<p style="color: #cf142a">hardcoded</p>\n'
            '<span style="color: #cf142b">near miss</span>\n'
            '<div style="background: linear-gradient(#123456, #654321); border-radius: 24px"></div>\n'
            "</body></html>\n"
        )
        bad_css = (
            ":root { --display: 'Comic Sans'; }\n"
            ".agustos-card { border: 3px dashed currentColor; }\n"
            ".hero { background: var(--signal); }\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "index.html").write_text(bad_html, encoding="utf-8")
            (project / "app.css").write_text(bad_css, encoding="utf-8")
            result = self._run(project, "--json")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            rules = {finding["rule"] for finding in json.loads(result.stdout)["findings"]}
            for rule in ("AG001", "AG002", "AG004", "AG005", "AG007", "AG008",
                         "AG009", "AG010", "AG011", "AG012"):
                with self.subTest(rule=rule):
                    self.assertIn(rule, rules)

    def test_checker_refuses_to_report_clean_when_it_scanned_nothing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(Path(tmp))
            self.assertEqual(result.returncode, 2)
            self.assertIn("nothing was checked", result.stderr)

    def test_checker_makes_no_network_call_during_a_normal_run(self):
        source = self.CHECKER.read_text(encoding="utf-8")
        before = source.index("def fetch_latest")
        self.assertNotIn("urllib", source[:before], "urllib is imported lazily, inside fetch_latest")


if __name__ == "__main__":
    unittest.main()
