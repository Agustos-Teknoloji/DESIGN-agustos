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

DARK_PAPER = "#15130f"
LIGHT_SUBSTRATES = ("#ffffff", "#fdf5f5", "#ebebeb")


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

        A small share inside color-mix is a tint, not a red field. The one
        approved solid fill is the dark-theme primary CTA.
        """
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        exception = re.search(
            r'html\[data-theme="dark"\] \.hero-action--primary,.*?'
            r'html\[data-theme="dark"\] \.agustos-button--primary:hover \{.*?\}',
            css,
            flags=re.S,
        )
        self.assertIsNotNone(exception, "dark-theme primary CTA exception is missing")
        self.assertIn("var(--signal)", exception.group(0))
        remainder = css[: exception.start()] + css[exception.end() :]
        for declaration in re.findall(r"\n\s*background(?:-color)?:\s*([^;]+);", remainder):
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


class SixColourPaletteTest(unittest.TestCase):
    """v5 locks six identity colours. Dark theme reuses them. No new hexes."""

    SIX = {"#ffffff", "#fdf5f5", "#ebebeb", "#404040", "#15130f", "#cf142a"}
    SUPPORT = {"#e8e4da", "#8a8378"}

    def _color(self, name: str) -> str:
        return TOKENS["foundations"]["color"][name]["$value"].lower()

    def test_light_roles_are_the_locked_six(self):
        self.assertEqual(self._color("paperWhite"), "#ffffff")
        self.assertEqual(self._color("paperCream"), "#fdf5f5")
        self.assertEqual(self._color("paperGray"), "#ebebeb")
        self.assertEqual(self._color("inkSoft"), "#404040")
        self.assertEqual(self._color("ink"), "#15130f")
        self.assertEqual(self._color("signalRed"), "#cf142a")

    def test_dark_roles_reuse_the_six_or_support_values(self):
        allowed = self.SIX | self.SUPPORT
        for name in (
            "paperDark",
            "inkDark",
            "inkSoftDark",
            "inkFaintDark",
            "ruleDark",
            "creamDark",
            "surfaceDark",
        ):
            with self.subTest(name=name):
                self.assertIn(self._color(name), allowed)

    def test_dark_ink_soft_meets_contrast_on_dark_paper(self):
        self.assertGreaterEqual(
            contrast_ratio(self._color("inkSoftDark"), self._color("paperDark")),
            4.5,
        )


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
        self.assertLessEqual(len(lines), 200, "UI-KIT.md is the one file an agent reads in full")

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

    def test_kit_json_registers_each_brand_and_its_chrome(self):
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {slug: entry["chrome"] for slug, entry in kit["brands"].items()},
            {"agustos": "sidebar", "pataraz": "topbar", "pld": "topbar", "iesdesk": "sidebar", "specquick": "sidebar"},
        )
        self.assertEqual(kit["brands"]["agustos"]["wordmark"], "ağustos")
        self.assertEqual(kit["brands"]["pataraz"]["color"], "#15130f")

    def test_kit_json_publishes_the_screens_table(self):
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        self.assertEqual(len(kit["screens"]), 9)
        product = kit["screens"]["product"]
        self.assertEqual(product["file"], "product.html")
        self.assertEqual(product["family"], "catalog")
        self.assertEqual(product["chrome"], "topbar")
        self.assertEqual(product["theme"], "light")
        self.assertEqual(product["primaryCtaMax"], 2)
        self.assertFalse(product["quotes"])
        self.assertEqual(kit["screens"]["app-shell"]["theme"], "dark-allowed")

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

    def test_checker_passes_on_the_reference_screens(self):
        """If our own reference pages fail our own checker, everything
        downstream is noise. The screens are what a consuming site looks
        like; starter.html is a specimen sheet and is skipped by name."""
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for page in sorted((ROOT / "screens").glob("*.html")):
                shutil.copyfile(page, project / page.name)
            result = self._run(project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_checker_carries_the_screens_table(self):
        """The screen rules are baked in like the token table, so a vendored
        checker cannot disagree with the kit it was cut from."""
        # compile + exec, not importlib: an import would write ui/__pycache__/*.pyc,
        # and the kit-scanning tests would then find "@latest" and the stale red in
        # the bytecode. The namespace carries __name__ so the main guard stays quiet.
        namespace: dict = {"__name__": "agustos_checker"}
        exec(compile(self.CHECKER.read_text(encoding="utf-8"), str(self.CHECKER), "exec"), namespace)
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        expected = {
            name: {"primaryCtaMax": row["primaryCtaMax"], "quotes": row["quotes"], "theme": row["theme"]}
            for name, row in kit["screens"].items()
        }
        self.assertEqual(namespace["SCREENS"], expected)

    SCREEN_PAGE = (
        '<!doctype html><html lang="tr"{html_attrs}><head>\n'
        '<link rel="stylesheet" href="/vendor/agustos-ui/agustos-fonts.css">\n'
        '<link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">\n'
        '</head><body class="brand-pataraz"{body_attrs}>\n'
        '<header class="site-header">{chrome}</header>\n'
        '<main id="main">{main}</main>\n'
        '</body></html>\n'
    )

    def _screen_page(self, screen=None, main="", chrome="", html_attrs=""):
        body_attrs = f' data-screen="{screen}"' if screen is not None else ""
        return self.SCREEN_PAGE.format(html_attrs=html_attrs, body_attrs=body_attrs, chrome=chrome, main=main)

    def test_checker_enforces_the_screen_rules(self):
        """Per-screen rules come from the screens table, keyed on data-screen:
        a page names its screen, the name exists, primaries inside <main> stay
        within the limit, quotes appear only where the row allows them, and
        data-theme appears only on product UI."""
        import tempfile
        primary = '<a class="agustos-button agustos-button--primary" href="#">Request pricing</a>'
        quote = '<blockquote class="type-blockquote">Quiet.</blockquote>'
        pages = {
            "no-screen.html": self._screen_page(None, main=primary),
            "unknown.html": self._screen_page("landing", main=primary),
            "too-many.html": self._screen_page("products", main=primary + primary),
            "quoted.html": self._screen_page("products", main=primary + quote),
            "dark.html": self._screen_page("home", main=primary, html_attrs=' data-theme="dark"'),
            "chrome-primary.html": self._screen_page("products", main=primary, chrome=primary),
            "fine.html": self._screen_page("app-shell", main=primary, html_attrs=' data-theme="dark"'),
        }
        expected = {
            "no-screen.html": {"AG020"},
            "unknown.html": {"AG021"},
            "too-many.html": {"AG022"},
            "quoted.html": {"AG023"},
            "dark.html": {"AG024"},
            "chrome-primary.html": set(),
            "fine.html": set(),
        }
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for name, text in pages.items():
                (project / name).write_text(text, encoding="utf-8")
            result = self._run(project, "--json")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            findings = json.loads(result.stdout)["findings"]
            by_file: dict[str, set[str]] = {name: set() for name in pages}
            for finding in findings:
                if finding["rule"].startswith("AG02"):
                    by_file[finding["file"]].add(finding["rule"])
                    self.assertEqual(finding["level"], "error", finding)
            for name, rules in expected.items():
                with self.subTest(page=name):
                    self.assertEqual(by_file[name], rules)

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


class ChromeTest(unittest.TestCase):
    CSS = (ROOT / "ui" / "agustos.css").read_text(encoding="utf-8")

    def test_both_chromes_and_the_lockup_are_published(self):
        declared = TOKENS["compatibility"]["cssClasses"]
        for name in (
            "site-lockup", "site-lockup__symbol", "site-lockup__name",
            "site-sidebar-layout", "site-sidebar", "site-sidebar__nav", "site-sidebar__link",
            "site-sidebar__group", "site-sidebar__cta", "site-sidebar__utility", "site-sidebar__note",
            "site-sidebar-bar", "site-sidebar-burger",
            "site-header", "site-header__bar", "site-header__panel", "site-header__nav",
            "site-header__link", "site-header__end", "site-header__cta", "site-header__burger",
            "site-footer", "site-footer__inner", "site-footer__brand", "site-footer__cols",
            "site-footer__col", "site-footer__col-heading", "site-footer__list", "site-footer__link",
            "site-footer__cta", "breadcrumb", "breadcrumb__link",
        ):
            self.assertIn(name, declared, name)

    def test_drawers_are_native_popovers_and_the_sidebar_is_forced_open_on_desktop(self):
        self.assertIn(".site-sidebar:not(:popover-open) { display: none; }", self.CSS)
        self.assertIn(".site-header__panel:popover-open { display: flex; }", self.CSS)
        self.assertIn("::backdrop", self.CSS)
        self.assertNotIn("data-nav-open", self.CSS)

    def test_sidebar_width_comes_from_the_chrome_recipe(self):
        self.assertIn("--sidebar-width: 240px", self.CSS)
        self.assertIn("padding-inline-start: var(--sidebar-width)", self.CSS)

    def test_footer_primary_button_ignores_the_dark_flip(self):
        self.assertIn('html[data-theme="dark"] .site-footer .agustos-button--primary', self.CSS)

    def test_house_brand_lockups_turn_white_on_dark_and_agustos_stays_red(self):
        self.assertIn('html[data-theme="dark"] .site-lockup { color: var(--ink); }', self.CSS)
        self.assertIn('html[data-theme="dark"] .brand-agustos .site-lockup { color: var(--brand); }', self.CSS)

    def test_layout_layer_is_published(self):
        declared = TOKENS["compatibility"]["cssClasses"]
        for name in ("stack", "cluster", "grid-2", "grid-3", "grid-4", "grid-aside", "band", "band--cream", "prose"):
            self.assertIn(name, declared, name)
        self.assertIn(".grid-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }", self.CSS)
        self.assertIn(".band--cream { background: var(--cream);", self.CSS)
        self.assertIn(".prose { max-width: var(--measure-body); }", self.CSS)
        self.assertIn(".grid-aside { display: grid; grid-template-columns: minmax(240px, 1fr) minmax(0, 3fr);", self.CSS)
        self.assertIn(".stack { display: flex; flex-direction: column; gap: var(--space-md); }", self.CSS)
        self.assertIn(".stack > * { margin-block: 0; }", self.CSS)
        self.assertIn(".cluster { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-sm); }", self.CSS)
        self.assertIn(".grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }", self.CSS)
        self.assertIn(".grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }", self.CSS)
        self.assertIn(".band { padding-block: var(--space-3xl); }", self.CSS)
        self.assertIn("@media (max-width: 759px) {\n  .grid-2,\n  .grid-3,\n  .grid-4,\n  .grid-aside { grid-template-columns: minmax(0, 1fr); }\n}", self.CSS)

    def test_entry_point_carries_the_screens_table_and_brand_chrome(self):
        text = (ROOT / "ui" / "UI-KIT.md").read_text(encoding="utf-8")
        self.assertIn("| `product` | catalog | topbar | light | at most 2 | no |", text)
        self.assertIn("| `app-shell` | product UI | sidebar | dark allowed | at most 1 | no |", text)
        self.assertIn("| ağustos | `brand-agustos` | sidebar |", text)
        self.assertIn("| pataraz | `brand-pataraz` | topbar |", text)
        self.assertIn("The kit is plain CSS. Do not add Tailwind, Bootstrap, or another utility framework.", text)
        self.assertNotIn("Tailwind preflight", text)
        for name in ("home", "static", "content", "products", "product-finder", "product", "spec-sheet", "app-shell"):
            self.assertIn(f"| `{name}` |", text)

    def test_reference_render_uses_the_sidebar_chrome_and_shows_the_topbar(self):
        text = (ROOT / "ui" / "starter.html").read_text(encoding="utf-8")
        self.assertIn('class="brand-agustos paper-white site-sidebar-layout"', text)
        self.assertIn('<aside id="site-sidebar" class="site-sidebar" popover', text)
        self.assertIn('popovertarget="site-sidebar"', text)
        self.assertIn('<header class="site-header">', text)
        self.assertIn('<footer class="site-footer">', text)
        self.assertIn('class="breadcrumb"', text)
        for name in ("stack", "cluster", "grid-3", "band band--cream", "type-body prose"):
            self.assertIn(f'class="{name}"', text)


if __name__ == "__main__":
    unittest.main()
