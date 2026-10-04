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

    def test_one_button_definition_and_it_is_black(self):
        """v7.0.0: the hero-action aliases are gone; one button, black, never red."""
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\.hero-action(?!s)", css))
        self.assertIsNone(re.search(r"\.hero-link", css))
        start = css.index(".agustos-button--primary {")
        block = css[start:css.index("}", start)]
        # v7.8.0: a client brand file may set --action; a house brand never does, so the fill stays ink.
        self.assertIn("background: var(--action, var(--ink));", block)
        self.assertNotIn("--signal", block)

    def test_controls_meet_the_minimum_target_size(self):
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        for block in (".agustos-input,", ".agustos-check {", ".agustos-tab {"):
            start = css.index(block)
            self.assertIn("min-height: var(--control-min)", css[start:start + 700], block)

    def test_spec_values_use_the_mono_face(self):
        """v7.6.0: a spec value is data in every medium: mono, with the label in the display face."""
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        self.assertIn(".type-spec th, .type-spec dt { font-family: var(--display); }", css)
        start = css.index(".type-spec td, .type-spec dd {")
        self.assertIn("font-family: var(--mono);", css[start:start + 200])
        for screen in ("product", "spec-sheet"):
            html = (ROOT / "screens" / f"{screen}.html").read_text(encoding="utf-8")
            self.assertIn("type-spec", html, screen)

    def test_inputs_do_not_trigger_ios_focus_zoom(self):
        """Below 16px iOS Safari zooms the viewport on focus."""
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        start = css.index(".agustos-input,\n.agustos-textarea,\n.agustos-select {")
        self.assertIn("font-size: var(--size-form-field)", css[start:start + 900])
        self.assertIn("--size-form-field: 16px;", css)

    def test_reduced_motion_is_honoured(self):
        """The handoff contract's acceptance list promises this."""
        for path in CSS_OUTPUTS:
            css = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn("@media (prefers-reduced-motion: reduce)", css)

    def test_no_radius_exceeds_the_system_maximum(self):
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        for raw in re.findall(r"border-radius:\s*([0-9.]+)px", css):
            self.assertLessEqual(float(raw), 12.0, "12px is the largest radius in this system")

    def test_signal_red_is_never_a_solid_background(self):
        """`forbidden`: signal red as a button, a fill or decoration.

        A small share inside color-mix is a tint, not a red field. The one
        stronger tint is the highlighter stroke, at most 20%. There is no
        solid red fill anywhere, not even in the dark theme (v7.0.0).
        """
        css = (ROOT / "tokens" / "agustos.css").read_text(encoding="utf-8")
        highlighter = css[css.index("mark.type-highlight,"):]
        highlighter = highlighter[: highlighter.index("}")]
        shares = [int(value) for value in re.findall(r"var\(--signal\)\s+(\d+)%", highlighter)]
        self.assertTrue(shares)
        self.assertLessEqual(max(shares), 20)
        remainder = css.replace(highlighter, "")
        for declaration in re.findall(r"\n\s*background(?:-color)?:\s*([^;]+);", remainder):
            if "var(--signal)" not in declaration and "#cf142a" not in declaration.lower():
                continue
            found = re.findall(r"var\(--signal\)\s+(\d+)%", declaration)
            self.assertTrue(found, f"signal used as a solid background: {declaration}")
            self.assertLessEqual(max(int(value) for value in found), 10, declaration)


class TypeContractTest(unittest.TestCase):
    """v7.6.0: one type table feeds every medium (MEMORY.md 2026-10-01 one-brand-every-medium)."""

    CSS = (ROOT / "ui" / "agustos.css").read_text(encoding="utf-8")
    KIT = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))

    def test_every_role_is_published_with_resolved_values(self):
        roles = {row["role"]: row for row in self.KIT["typeRoles"]}
        expected = {"hero", "h1", "deck", "h2", "h3", "h4", "body", "compact", "control",
                    "quote", "pullquote", "footnote", "spec"}
        self.assertEqual(set(roles), expected)
        for role, row in roles.items():
            with self.subTest(role=role):
                for field in ("size", "weight", "lineHeight"):
                    self.assertNotIn("{", str(row[field]), f"{role}.{field} is an unresolved alias")
        self.assertEqual(roles["spec"]["family"], "mono")

    def test_every_size_is_a_variable(self):
        """A consumer cannot follow "never retype a token value" without a name for each size."""
        sizes = TOKENS["foundations"]["fontSize"]
        for key, name in (("hero", "hero"), ("h1", "h1"), ("h2", "h2"), ("h3", "h3"), ("h4", "h4"),
                          ("heroDeck", "deck"), ("body", "body"), ("bodyCompact", "body-compact"),
                          ("formField", "form-field"), ("footnote", "footnote")):
            with self.subTest(size=key):
                self.assertIn(f"--size-{name}: {sizes[key]['$value']};", self.CSS)

    def test_no_type_size_is_typed_by_hand(self):
        """The six off-scale sizes (13.5, 15, 16, 20 except the logo, 22, 26px) mapped to the scale."""
        rules = self.CSS[self.CSS.index("/* -- 2. Per-brand application"):]
        literals = re.findall(r"font-size:\s*(\d+(?:\.\d+)?px)", rules)
        self.assertEqual(literals, ["20px"], "only the site lockup keeps a pixel size")

    def test_a_breadcrumb_opens_close_under_the_menu(self):
        """v7.6.0: the hero padding (up to 112px) above a 13px trail read as an empty band."""
        self.assertIn(".container:has(> nav:first-child > .breadcrumb) {\n  padding-block-start: 16px;\n}", self.CSS)
        self.assertIn(".site-frame > nav:first-child:has(> .breadcrumb) {\n  padding-block-start: 16px;\n}", self.CSS)

    def test_the_meta_line_sits_under_the_deck(self):
        """v7.6.0, option D: breadcrumb, title, deck, then the date; no label above the title."""
        self.assertIn("nav:has(> .breadcrumb) {\n  margin-block-end: 24px;\n}", self.CSS)
        self.assertIn(".type-hero-deck + .type-footnote {\n  margin: 12px 0 var(--space-xl);\n}", self.CSS)
        # v7.6.1: the 1em rule after a deck is more specific, so it must skip the meta line.
        # It did not, and the line sat 13px (1em of the footnote) under the deck.
        self.assertIn(":not(.stack) > .type-hero-deck + :not(.hero-actions, .hero-trust, .hero-visual, .type-footnote) {", self.CSS)
        # v7.6.2: a page with no deck puts the meta line under the title, and the
        # text starts 24px below it, as after a deck. agustos.com showed 13px.
        self.assertIn(":not(.stack) > :is(h1, .type-h1, .type-hero, .type-hero-md) + .type-footnote {\n  margin-block-end: var(--space-xl);\n}", self.CSS)
        # A stack is a flex column, so margins add up there: 24px on the meta line
        # plus the 16px gap gave 40px. Both rules skip a stack, and the stack sets
        # the same spaces. A heading below keeps its break (:where, same weight, earlier).
        self.assertIn(":not(.stack) > .type-hero-deck + .type-footnote {", self.CSS)
        self.assertIn(".stack > .type-hero-deck + .type-footnote { --stack-space: 12px; }", self.CSS)
        meta = ".stack > :where(h1, .type-h1, .type-hero, .type-hero-md, .type-hero-deck) + .type-footnote + * { --stack-space: var(--space-xl); }"
        self.assertIn(meta, self.CSS)
        self.assertLess(self.CSS.index(meta), self.CSS.index(".stack > :is(h2, .type-h2) { --stack-space: var(--space-before-h2); }"))
        for screen in sorted((ROOT / "screens").glob("*.html")):
            html = screen.read_text(encoding="utf-8")
            with self.subTest(screen=screen.name):
                # The line before each H1 is the breadcrumb or nothing, never a label.
                self.assertNotRegex(html, r'<p class="type-(h4|footnote)"[^>]*>[^\n]*</p>\s*(</div>\s*)?<h1')

    def test_the_stack_uses_the_heading_rhythm(self):
        """v7.6.0: a title sits 32px above its deck inside a stack too, even on an h2 element."""
        after_h2 = self.CSS.index(".stack > :is(h2, .type-h2) + * { --stack-space: var(--space-after-h2); }")
        title = self.CSS.index(".stack > :is(.type-hero, .type-hero-md, h1, .type-h1) + * { --stack-space: var(--space-after-title); }")
        self.assertLess(after_h2, title, "the title rule must win over the h2 rule at equal weight")
        self.assertIn(".stack > :is(h2, .type-h2) { --stack-space: var(--space-before-h2); }", self.CSS)

    def test_entry_point_prints_the_type_table(self):
        text = (ROOT / "ui" / "UI-KIT.md").read_text(encoding="utf-8")
        self.assertIn("## Type and spacing", text)
        self.assertIn("| spec | `type-spec` | mono |", text)


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


class InteractionStateTest(unittest.TestCase):
    """v7.0.1: every state in both themes clears its floor, and the CSS carries the fixes.

    A browser probe of v7.0.0 found white-on-light-gray (1.19) in the dark More
    menu, footer links that vanished on hover in dark (1.00), red hover text on
    off-black (3.35), a dead dark logo hover, 1.27 field borders, no pressed
    state, and disabled buttons that still reacted to hover.
    """

    CSS = (ROOT / "ui" / "agustos.css").read_text(encoding="utf-8")
    FLOORS = {"text": 4.5, "graphic": 3.0, "exempt": 0.0}

    def test_every_state_row_clears_its_floor_in_both_themes(self):
        colors = TOKENS["foundations"]["color"]
        rows = TOKENS["states"]["rows"]
        self.assertGreater(len(rows), 20, "the states table looks truncated")
        for row in rows:
            for theme in ("light", "dark"):
                foreground, background = (colors[key]["$value"] for key in row[theme])
                with self.subTest(element=row["element"], state=row["state"], theme=theme):
                    self.assertGreaterEqual(contrast_ratio(foreground, background), self.FLOORS[row["kind"]])

    def test_states_table_is_published_to_docs_and_kit_json(self):
        docs = (ROOT / "docs" / "web.html").read_text(encoding="utf-8")
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        self.assertEqual(len(kit["states"]), len(TOKENS["states"]["rows"]))
        self.assertIn('id="states"', docs)
        for row in TOKENS["states"]["rows"]:
            with self.subTest(element=row["element"]):
                self.assertIn(f'<th scope="row">{row["element"]}</th>', docs.replace("&#x27;", "'"))

    def test_dark_hover_dims_the_ink_instead_of_turning_it_red(self):
        self.assertIn(':where(html[data-theme="dark"]) a:hover,', self.CSS)
        self.assertIn(':where(html[data-theme="dark"]) .agustos-button--quiet:hover { color: var(--ink-soft); }', self.CSS)

    def test_footer_and_band_follow_the_dark_theme(self):
        """v7.7.0: the footer and the closing band turn dark with the page (Emre,
        2026-10-03: "Footer should change too"). The light islands are gone."""
        # The print block holds an indented copy; the top-level line stays unique.
        self.assertEqual(self.CSS.count('\nhtml[data-theme="dark"] {\n'), 1)
        dark = self.CSS[self.CSS.index('html[data-theme="dark"] {'):]
        dark = dark[:dark.index("}")]
        self.assertIn("--footer-paper:", dark)
        self.assertIn("--footer-ink:", dark)
        self.assertIn("--footer-cta-hover:", dark)
        self.assertNotIn('html[data-theme="dark"] .site-footer,', self.CSS)
        band = self.CSS[self.CSS.index('html[data-theme="dark"] .band--cream {'):]
        band = band[:band.index("}")]
        # Decision 1 (B2): the dark paper between two hairline rules, so every
        # pair inside the band is a page pair and red keeps 3.35:1.
        self.assertIn("background: var(--paper);", band)
        self.assertIn("border-block-start:", band)
        self.assertNotIn("border-block:", band)
        self.assertNotIn("color-scheme: light", band)
        # The footer draws its own top hairline, so a band that is the last
        # child of main draws no bottom rule: one line, never two.
        last = self.CSS[self.CSS.index('html[data-theme="dark"] .band--cream:not(:last-child) {'):]
        self.assertIn("border-block-end:", last[:last.index("}")])

    def test_print_is_light_in_the_dark_theme(self):
        """A printer drops backgrounds, so dark-theme ink would print white on white."""
        start = self.CSS.index("@media print {")
        block = self.CSS[start:self.CSS.index("\n}\n", start)]
        reset = block[block.index('html[data-theme="dark"] {'):]
        reset = reset[:reset.index("}")]
        # Every custom property that the dark theme sets, print sets back.
        dark = self.CSS[self.CSS.index('\nhtml[data-theme="dark"] {\n'):]
        dark = dark[:dark.index("}")]
        roles = re.findall(r"^\s*(--[\w-]+):", dark, re.MULTILINE)
        self.assertIn("--footer-cta-hover", roles)
        for role in roles:
            with self.subTest(role=role):
                self.assertRegex(reset, rf"(?m)^\s*{re.escape(role)}:")
        self.assertIn("color-scheme: light;", reset)

    def test_states_cover_the_dark_footer_and_band(self):
        rows = {(row["element"], row["state"]): row for row in TOKENS["states"]["rows"]}
        self.assertEqual(rows[("Footer link", "rest")]["dark"], ["inkSoftDark", "paperDark"])
        self.assertEqual(rows[("Closing band text", "rest")]["dark"], ["inkDark", "paperDark"])
        self.assertEqual(rows[("Closing band secondary text", "rest")]["dark"], ["inkSoftDark", "paperDark"])
        self.assertEqual(rows[("Keyboard focus ring in the closing band", "focus")]["dark"], ["signalRed", "paperDark"])
        self.assertNotIn("stays light", " ".join(row["element"] for row in TOKENS["states"]["rows"]))

    def test_more_menu_hover_uses_the_functional_gray(self):
        self.assertIn('.site-header__more-link:is([aria-current="page"], [aria-current="true"]) { background: var(--surface);', self.CSS)

    def test_more_list_holds_titled_groups_as_columns(self):
        """v7.7.0: a More may hold titled groups, in columns on a wide screen and
        stacked in the drawer (IESDesk Tools: one file, many files)."""
        groups = self.CSS[self.CSS.index(".site-header__more-menu--groups {"):]
        self.assertIn("flex-direction: row;", groups[:groups.index("}")])
        title = self.CSS[self.CSS.index(".site-header__more-group-title {"):]
        title = title[:title.index("}")]
        self.assertIn("font-size: var(--size-footnote);", title)
        self.assertIn("color: var(--ink-soft);", title)
        self.assertNotIn("text-transform", title)
        drawer = self.CSS[self.CSS.index("@media (max-width: 1023px) {", self.CSS.index(".site-header__panel {")):]
        drawer = drawer[:drawer.index("\n}\n")]  # the drawer block only
        self.assertIn(".site-header__more-menu--groups { flex-direction: column;", drawer)
        self.assertIn("a More may hold up to two titled groups", self.CSS)
        for name in ("site-header__more-menu--groups", "site-header__more-group", "site-header__more-group-title"):
            with self.subTest(name=name):
                self.assertIn(name, TOKENS["compatibility"]["cssClasses"])

    def test_account_list_sits_at_the_end_and_truncates(self):
        """v7.7.0: the account list is a More in site-header__end. It opens from
        the right edge, its email label ends with an ellipsis, and a sign-out
        form button reads like the links around it (IESDesk)."""
        end = self.CSS[self.CSS.index(".site-header__more--end .site-header__more-menu {"):]
        end = end[:end.index("}")]
        self.assertIn("inset-inline-start: auto;", end)
        self.assertIn("inset-inline-end:", end)
        label = self.CSS[self.CSS.index(".site-header__more-label {"):]
        label = label[:label.index("}")]
        for rule in ("text-overflow: ellipsis;", "overflow: hidden;", "white-space: nowrap;", "max-inline-size:"):
            with self.subTest(rule=rule):
                self.assertIn(rule, label)
        button = self.CSS[self.CSS.index("button.site-header__more-link {"):]
        button = button[:button.index("}")]
        for rule in ("border: 0;", "background: transparent;", "width: 100%;", "text-align: start;", "cursor: pointer;"):
            with self.subTest(rule=rule):
                self.assertIn(rule, button)
        self.assertIn(".site-header__more-menu > form { display: contents; }", self.CSS)
        drawer = self.CSS[self.CSS.index("@media (max-width: 1023px) {", self.CSS.index(".site-header__panel {")):]
        drawer = drawer[:drawer.index("\n}\n")]  # the drawer block only
        self.assertIn(".site-header__more--end .site-header__more-menu { inset-inline-end: auto; }", drawer)
        # In the drawer the email stops at the drawer edge with its ellipsis; it never scrolls the page sideways.
        self.assertIn(".site-header__more-label { max-inline-size: 100%; }", drawer)
        self.assertNotIn("max-inline-size: none", drawer)
        # The summary is inline-flex and grows to its text, so it needs the same bound.
        self.assertIn(".site-header__more--end > summary { max-inline-size: 100%; }", drawer)
        for name in ("site-header__more--end", "site-header__more-label"):
            with self.subTest(name=name):
                self.assertIn(name, TOKENS["compatibility"]["cssClasses"])

    def test_form_fields_clear_the_non_text_floor(self):
        self.assertIn("solid var(--ink-faint);", self.CSS)
        placeholder = self.CSS[self.CSS.index(".agustos-textarea::placeholder {"):]
        self.assertIn("color: var(--ink-soft);", placeholder[:placeholder.index("}")])

    def test_buttons_have_pressed_and_disabled_states(self):
        self.assertIn('.agustos-button:active:not(:disabled, [aria-disabled="true"]) { transform: translateY(1px); }', self.CSS)
        self.assertIn('.agustos-button:is(:disabled, [aria-disabled="true"]):hover', self.CSS)

    def test_design_review_fixes_hold(self):
        """Design review 2026-09-30 (v7.3.3), each measured in a browser first."""
        # A dark search excerpt on the hover fill was #8a8378 on #404040, 2.76:1.
        self.assertIn(".site-header__search-result a:is(:hover, :focus-visible) .site-header__search-result-excerpt { color: var(--ink); }", self.CSS)
        # The footer has no current page, so its hover never draws the red rule.
        footer = self.CSS[self.CSS.index(".site-footer__link:hover {"):]
        footer = footer[:footer.index("}")]
        self.assertIn("text-decoration-color: var(--ink-faint);", footer)
        self.assertNotIn("--signal", footer)
        # Browsers center a caption; the spec-sheet group labels sat centered.
        self.assertIn(".type-table caption, table caption { padding-inline: 0.75em; text-align: start; }", self.CSS)
        # Native parts follow the theme. The footer and the band follow it too (v7.7.0).
        self.assertIn(":root { color-scheme: light; }", self.CSS)
        dark = self.CSS[self.CSS.index('html[data-theme="dark"] {'):]
        self.assertIn("color-scheme: dark;", dark[:dark.index("}")])
        self.assertNotIn("light islands", self.CSS.lower())
        # One duration token stops every transition, so none can be missed.
        motion = self.CSS[self.CSS.index("@media (prefers-reduced-motion: reduce) {"):]
        self.assertIn(":root { --dur: 0s; }", motion[:motion.index("\n}\n")])
        transitions = re.findall(r"transition:\s*([^;]+);", self.CSS)
        self.assertTrue(transitions)
        for value in transitions:
            for part in value.split(","):
                self.assertIn("var(--dur)", part, value)


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
        # Three house families, plus Montserrat and Roboto for the client brands (v7.8.0).
        self.assertEqual(len(licenses), 5, "one OFL per font family")

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
        # 220 since v7.6.0: the type table (one row per role) joined the file.
        # 230 since v7.8.0: the client brand section and its table joined the file.
        self.assertLessEqual(len(lines), 230, "UI-KIT.md is the one file an agent reads in full")

    def test_entry_point_states_the_v7_7_rules(self):
        text = (self.KIT / "UI-KIT.md").read_text(encoding="utf-8")
        for phrase in ("every page starts light", "never the device", "AG033", "data-agustos-unfold",
                       "site-header__more--end", "app-top-menu", "Print is always light",
                       "covers the whole width below 640px"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        for gone in ("product UI only; same six colours", "The footer and the closing band stay light",
                     "The footer is light:", "`data-theme` outside product UI",
                     "Theme, chrome and column follow the family"):
            with self.subTest(gone=gone):
                self.assertNotIn(gone, text)

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

    def test_kit_json_registers_each_brand(self):
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        self.assertEqual(
            set(kit["brands"]), {"agustos", "pataraz", "pld", "iesdesk", "specquick", "memregunes"},
        )
        for entry in kit["brands"].values():
            self.assertNotIn("chrome", entry)
        self.assertEqual(kit["brands"]["agustos"]["wordmark"], "ağustos")
        self.assertEqual(kit["brands"]["pataraz"]["color"], "#15130f")

    def test_kit_json_publishes_the_screens_table(self):
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        self.assertEqual(len(kit["screens"]), 10)
        product = kit["screens"]["product"]
        self.assertEqual(product["file"], "product.html")
        self.assertEqual(product["family"], "catalog")
        self.assertEqual(product["chrome"], "topbar")
        self.assertEqual(product["theme"], "light-first")
        self.assertNotIn("primaryCtaMax", product)
        self.assertNotIn("quotes", product)
        self.assertEqual(kit["screens"]["app-shell"]["theme"], "light-first")
        self.assertEqual(kit["screens"]["app-shell"]["chrome"], "sidebar")
        self.assertEqual(kit["screens"]["home"]["chrome"], "topbar")

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
            name: {"theme": row["theme"], "chrome": row["chrome"], "column": row["column"], "highlight": row["highlight"]}
            for name, row in kit["screens"].items()
        }
        self.assertEqual(namespace["SCREENS"], expected)
        self.assertNotIn("BRAND_SCREEN_RULES", namespace)

    SCREEN_PAGE = (
        '<!doctype html><html lang="tr"{html_attrs}><head>\n'
        '<link rel="stylesheet" href="/vendor/agustos-ui/agustos-fonts.css">\n'
        '<link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">\n'
        '</head><body class="brand-{brand}"{body_attrs}>\n'
        '<header class="site-header">{chrome}</header>\n'
        '<main id="main">{main}</main>\n'
        '</body></html>\n'
    )

    def _screen_page(self, screen=None, main="", chrome="", html_attrs="", brand="pataraz"):
        body_attrs = f' data-screen="{screen}"' if screen is not None else ""
        return self.SCREEN_PAGE.format(
            html_attrs=html_attrs, body_attrs=body_attrs, chrome=chrome, main=main, brand=brand,
        )

    def test_checker_enforces_the_screen_rules(self):
        """Per-screen rules come from the screens table, keyed on data-screen.
        Errors guard integrity: a page names its screen, and the name exists.
        Taste rules only warn: a page that starts dark (AG024), more than
        one highlighter (AG025), a sidebar on a top-menu screen (AG026), more than five
        items in site-header__nav (AG027, the More toggle counts, its items and an
        account list in site-header__end do not; v7.7.0), a
        full-width container on a content screen (AG028, v7.2.0), an
        `agustos-contents` that is not a direct child of `container--reading`
        (AG031, v7.4.0), a homepage with no highlighter (AG032, v7.5.0). Button counts
        and quotes are no longer checked (v7.0.0)."""
        import tempfile
        primary = '<a class="agustos-button agustos-button--primary" href="#">Request pricing</a>'
        quote = '<blockquote class="type-blockquote">Quiet.</blockquote>'
        mark = '<mark class="type-highlight">clear</mark>'
        head = f"<h1>{mark}</h1>"  # the homepage's one stroke, so AG032 stays quiet
        sidebar = '<aside id="site-sidebar" class="site-sidebar" popover></aside>'
        item = '<a class="site-header__link" href="/{0}">Item {0}</a>'
        more = ('<details class="site-header__more"><summary class="site-header__link">Daha fazla</summary>'
                '<div class="site-header__more-menu">'
                + ''.join(f'<a class="site-header__more-link" href="/m{n}">M{n}</a>' for n in range(4))
                + '</div></details>')
        nav = '<nav class="site-header__nav">{0}</nav>'
        erb_nav = '<nav aria-label="<%= t(:menu) %>" <%= "hidden" if bare? %> class="site-header__nav">{0}</nav>'
        account = ('<div class="site-header__end"><details class="site-header__more site-header__more--end">'
                   '<summary class="site-header__link"><span class="site-header__more-label">a@b.com</span></summary>'
                   '<div class="site-header__more-menu"><form action="/s" method="post">'
                   '<button type="submit" class="site-header__more-link">Sign out</button></form></div></details></div>')
        pages = {
            "no-screen.html": (self._screen_page(None, main=primary), {"AG020": "error"}),
            "unknown.html": (self._screen_page("landing", main=primary), {"AG021": "error"}),
            "many-and-quoted.html": (self._screen_page("products", main=primary * 4 + quote), {}),
            "dark.html": (self._screen_page("home", main=head + primary, html_attrs=' data-theme="dark"'), {"AG024": "warn"}),
            "two-marks.html": (self._screen_page("home", main=f"<h1>{mark}</h1><p>{mark}</p>"), {"AG025": "warn"}),
            "one-mark.html": (self._screen_page("home", main=f"<h1>{mark}</h1>"), {}),
            "sidebar-site.html": (self._screen_page("home", main=head, chrome=sidebar), {"AG026": "warn"}),
            "six-items.html": (self._screen_page("home", main=head, chrome=nav.format("".join(item.format(n) for n in range(6)))), {"AG027": "warn"}),
            "four-and-more.html": (self._screen_page("home", main=head, chrome=nav.format("".join(item.format(n) for n in range(4)) + more)), {}),
            "five-and-account.html": (self._screen_page("home", main=head, chrome=nav.format("".join(item.format(n) for n in range(5))) + account), {}),
            "six-no-nav.html": (self._screen_page("home", main=head, chrome="".join(item.format(n) for n in range(6))), {"AG027": "warn"}),
            "app.html": (self._screen_page("app-shell", main=primary, chrome=sidebar, html_attrs=' data-theme="dark"'), {"AG024": "warn"}),
            "light-attr.html": (self._screen_page("home", main=head, html_attrs=' data-theme="light"'), {}),
            "switch-script.html": (self._screen_page("home", main=head + '<script>try{if(localStorage.getItem("agustos:theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}</script>'), {}),
            "templated.html": (self._screen_page("home", main=head, html_attrs=' data-theme="<%= theme %>"'), {}),
            "wide-policy.html": (self._screen_page("static", main='<div class="container"><h1>Gizlilik</h1></div>'), {"AG028": "warn"}),
            "reading-policy.html": (self._screen_page("static", main="<article class='container container--reading'><h1>Gizlilik</h1></article>"), {}),
            "wide-home.html": (self._screen_page("home", main=f'<section class="container">{head}</section>'), {}),
            "no-mark-home.html": (self._screen_page("home", main="<h1>Işık</h1>"), {"AG032": "warn"}),
            "no-mark-products.html": (self._screen_page("products", main="<h1>Ürünler</h1>"), {}),
            "contents-nested.html": (self._screen_page("static", main='<div class="container container--reading"><div><details class="agustos-contents"></details></div></div>'), {"AG031": "warn"}),
            "contents-direct.html": (self._screen_page("static", main='<div class="container container--reading"><details class="agustos-contents"></details></div>'), {}),
            "contents-after-open-p.html": (self._screen_page("static", main='<div class="container container--reading"><p>Intro<details class="agustos-contents"></details></div>'), {}),
            "sidebar-top-app.html": (self._screen_page("app-top-menu", main="", chrome=sidebar), {"AG026": "warn"}),
            "top-app.html": (self._screen_page("app-top-menu", main=""), {}),
            # ERB in an earlier attribute: the scan steps over quoted values and template tags.
            "erb-dark.html.erb": (self._screen_page("home", main=head, html_attrs=' dir="<%= dir %>"<% if dark? %> data-theme="dark"<% end %>'), {"AG024": "warn"}),
            "dark-blue.html": (self._screen_page("home", main=head, html_attrs=' data-theme="dark-blue"'), {}),
            "erb-nav.html.erb": (self._screen_page("home", main=head, chrome=erb_nav.format("".join(item.format(n) for n in range(4)) + more) + account), {}),
            "erb-nav-six.html.erb": (self._screen_page("home", main=head, chrome=erb_nav.format("".join(item.format(n) for n in range(6)))), {"AG027": "warn"}),
            "nav-suffix.html": (self._screen_page("home", main=head, chrome=nav.format("".join(item.format(n) for n in range(5))) + '<nav class="site-header__nav-extra">' + item.format(8) + "</nav>"), {}),
        }
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for name, (text, _) in pages.items():
                (project / name).write_text(text, encoding="utf-8")
            result = self._run(project, "--json")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            findings = json.loads(result.stdout)["findings"]
            by_file: dict[str, dict[str, str]] = {name: {} for name in pages}
            for finding in findings:
                if finding["rule"].startswith(("AG02", "AG031", "AG032")):
                    by_file[finding["file"]][finding["rule"]] = finding["level"]
            for name, (_, expected) in pages.items():
                with self.subTest(page=name):
                    self.assertEqual(by_file[name], expected)

    def test_checker_warns_when_the_device_picks_the_theme(self):
        """v7.7.0: the user chooses the theme, never the device (Emre, 2026-10-03)."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "site.css").write_text("@media (prefers-color-scheme: dark) { body { color: var(--ink); } }\n", encoding="utf-8")
            (project / "theme.js").write_text("const dark = matchMedia('(prefers-color-scheme: dark)').matches;\n", encoding="utf-8")
            (project / "notes.md").write_text("Never read prefers-color-scheme.\n", encoding="utf-8")
            result = self._run(project, "--json")
            findings = [f for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG033"]
            self.assertEqual(sorted(f["file"] for f in findings), ["site.css", "theme.js"])
            self.assertTrue(all(f["level"] == "warn" for f in findings))

    def test_checker_warns_on_a_switch_without_the_head_script(self):
        """v7.7.0: the switch keeps a dark choice, and only the head script applies
        it before the first paint. Without the script, or with the script after a
        stylesheet, each new page shows light first (AG034)."""
        import tempfile
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        script = f"<script>{kit['themeScript']}</script>"
        switch = ('<button type="button" class="site-header__icon-btn agustos-theme-switch" data-agustos-theme>'
                  '<span class="agustos-theme-switch__to-dark"><span class="agustos-theme-switch__label">Dark theme</span></span>'
                  '<span class="agustos-theme-switch__to-light"><span class="agustos-theme-switch__label">Light theme</span></span></button>')
        links = ('<link rel="stylesheet" href="/vendor/agustos-ui/agustos-fonts.css">\n'
                 '<link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">\n')

        def page(head, body=switch):
            return ('<!doctype html><html lang="en"><head>\n<meta charset="utf-8">\n'
                    f'{head}</head><body class="brand-agustos" data-screen="static">\n'
                    f'<header class="site-header">{body}</header>\n<main id="main"></main>\n</body></html>\n')

        nonce = kit["themeScript"].join(('<script nonce="<%= content_security_policy_nonce %>">', "</script>\n"))
        rails_css = '<%= stylesheet_link_tag "agustos" %>\n'
        pages = {
            "script-first.html": (page(script + "\n" + links), []),
            "no-script.html": (page(links), ["AG034"]),
            "script-after-css.html": (page(links + script + "\n"), ["AG034"]),
            "script-in-comment.html": (page("<!-- " + script + " -->\n" + links), ["AG034"]),
            "no-switch.html": (page(links, body=""), []),
            "layout.html.erb": (page(nonce + '<%= stylesheet_link_tag "agustos" %>\n'), []),
            "helper-first.html.erb": (page('<%= stylesheet_link_tag "agustos" %>\n' + nonce), ["AG034"]),
            "_header.html.erb": (switch + "\n", []),
            # A Rails javascript_tag counts when it carries the script or the storage key.
            "javascript-tag.html.erb": (page('<%= javascript_tag AgustosThemeHelper::THEME_SCRIPT, nonce: true %>\n' + rails_css), []),
            "javascript-tag-key.html.erb": (page(f"<%= javascript_tag '{kit['themeScript']}', nonce: true %>\n" + rails_css), []),
            "javascript-tag-block.html.erb": (page(f"<%= javascript_tag nonce: true do %>\n{kit['themeScript']}\n<% end %>\n" + rails_css), []),
            "javascript-tag-late.html.erb": (page(rails_css + '<%= javascript_tag AgustosThemeHelper::THEME_SCRIPT, nonce: true %>\n'), ["AG034"]),
            "javascript-tag-other.html.erb": (page('<%= javascript_tag "window.ready = true", nonce: true %>\n' + rails_css), ["AG034"]),
        }
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for name, (text, _) in pages.items():
                (project / name).write_text(text, encoding="utf-8")
            result = self._run(project, "--json")
            findings = [f for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG034"]
            self.assertTrue(all(f["level"] == "warn" for f in findings))
            for name, (_, expected) in pages.items():
                with self.subTest(page=name):
                    self.assertEqual([f["rule"] for f in findings if f["file"] == name], expected)
            # Built output is a page too.
            result = self._run(project, "--json", "--screens-only")
            found = sorted(f["file"] for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG034")
            self.assertEqual(found, ["no-script.html", "script-after-css.html", "script-in-comment.html"])
        # AG034 reads full pages only. A partial is never checked through its layout.
        self.assertIn("AG034 reads a full page; a site that renders the switch from a partial needs its own page test.",
                      (ROOT / "ui" / "UI-KIT.md").read_text(encoding="utf-8"))
        self.assertNotIn("its layout is checked instead", self.CHECKER.read_text(encoding="utf-8"))

    def test_checker_warns_on_a_switch_without_the_chrome_script(self):
        """v7.7.0: only agustos-chrome.js flips the theme. A full page with a
        theme switch that does not load the script gets a switch that does
        nothing (AG036). A class name such as agustos-chrome-link is not the
        script. Built output bundles the script under a hashed name, so the
        rule reads the source only."""
        import tempfile
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        switch = ('<button type="button" class="site-header__icon-btn agustos-theme-switch" data-agustos-theme>'
                  '<span class="agustos-theme-switch__to-dark"><span class="agustos-theme-switch__label">Dark theme</span></span>'
                  '<span class="agustos-theme-switch__to-light"><span class="agustos-theme-switch__label">Light theme</span></span></button>')

        def page(scripts, body=switch):
            return ('<!doctype html><html lang="en"><head>\n<meta charset="utf-8">\n'
                    f'<script>{kit["themeScript"]}</script>\n'
                    '<link rel="stylesheet" href="/vendor/agustos-ui/agustos.css">\n'
                    f'{scripts}</head><body class="brand-agustos" data-screen="static">\n'
                    f'<header class="site-header">{body}</header>\n<main id="main"></main>\n</body></html>\n')

        pages = {
            "with-chrome.html": (page('<script src="/vendor/agustos-ui/agustos-chrome.js" defer></script>\n'), []),
            "no-chrome.html": (page(""), ["AG036"]),
            "chrome-link-class.html": (page("", body=switch + '<a class="agustos-chrome-link" href="/en">EN</a>'), ["AG036"]),
            "commented.html": (page('<!-- <script src="/agustos-chrome.js" defer></script> -->\n'), ["AG036"]),
            "erb-commented.html.erb": (page('<%# javascript_include_tag "agustos/chrome" %>\n'), ["AG036"]),
            "include-tag.html.erb": (page('<%= javascript_include_tag "agustos/chrome", defer: true %>\n'), []),
            "include-tag-dash.html.erb": (page('<%= javascript_include_tag "agustos-chrome", defer: true %>\n'), []),
            "inline-chrome.html": (page("", body=switch + "<script>(()=>{if(document.agustosChrome)return;document.agustosChrome=true})()</script>"), []),
            "no-switch.html": (page("", body=""), []),
            "_header.html.erb": (switch + "\n", []),
        }
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for name, (text, _) in pages.items():
                (project / name).write_text(text, encoding="utf-8")
            result = self._run(project, "--json")
            findings = [f for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG036"]
            self.assertTrue(all(f["level"] == "warn" for f in findings))
            for name, (_, expected) in pages.items():
                with self.subTest(page=name):
                    self.assertEqual([f["rule"] for f in findings if f["file"] == name], expected)
            no_chrome = next(f for f in findings if f["file"] == "no-chrome.html")
            self.assertEqual(no_chrome["line"], 6)  # the line of the switch
            result = self._run(project, "--json", "--screens-only")
            self.assertEqual([f for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG036"], [])
        # A layout that loads the import map passes when a project script imports the chrome.
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "application.html.erb").write_text(page("<%= javascript_importmap_tags %>\n"), encoding="utf-8")
            result = self._run(project, "--json")
            self.assertEqual([f["file"] for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG036"],
                             ["application.html.erb"])
            (project / "application.js").write_text('import "agustos/chrome"\n', encoding="utf-8")
            result = self._run(project, "--json")
            self.assertEqual([f for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG036"], [])
        self.assertIn("a theme switch on a page that does not load `agustos-chrome.js` (AG036)",
                      (ROOT / "ui" / "UI-KIT.md").read_text(encoding="utf-8"))

    def test_checker_warns_on_a_more_with_three_groups(self):
        """v7.7.0: a grouped More holds at most two groups. A third group pushes
        the menu past the right edge of the page at 1024px and 1280px (AG035).
        The rule reads partials too, because a header is often one."""
        import tempfile

        def more(count):
            groups = "".join(
                f'<div class="site-header__more-group" role="group" aria-labelledby="g{n}">'
                f'<p class="site-header__more-group-title" id="g{n}">Group {n}</p>'
                f'<a class="site-header__more-link" href="/g{n}">Link {n}</a></div>\n'
                for n in range(count))
            return ('<details class="site-header__more"><summary class="site-header__link">Tools</summary>\n'
                    f'<div class="site-header__more-menu site-header__more-menu--groups">\n{groups}</div></details>\n')

        # The account list (v7.7.0) is a More with no groups: AG035 never counts it.
        account = ('<div class="site-header__end"><details class="site-header__more site-header__more--end">\n'
                   '<summary class="site-header__link"><span class="site-header__more-label">a@b.com</span></summary>\n'
                   '<div class="site-header__more-menu"><a class="site-header__more-link" href="/account">Account</a>\n'
                   '<form action="/s" method="post"><button type="submit" class="site-header__more-link">Sign out</button></form>\n'
                   '</div></details></div>\n')
        pages = {
            "two-groups.html": (self._screen_page("home", main="<h1><mark class=\"type-highlight\">Clear</mark></h1>", chrome=more(2)), []),
            "three-groups.html": (self._screen_page("home", main="<h1><mark class=\"type-highlight\">Clear</mark></h1>", chrome=more(3)), ["AG035"]),
            "_header.html.erb": (more(3), ["AG035"]),
            "_two.html.erb": (more(2), []),
            "commented.html.erb": ("<!-- " + more(3) + " -->\n", []),
            "_account.html.erb": (account, []),
        }
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for name, (text, _) in pages.items():
                (project / name).write_text(text, encoding="utf-8")
            result = self._run(project, "--json")
            findings = [f for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG035"]
            self.assertTrue(all(f["level"] == "warn" for f in findings))
            for name, (_, expected) in pages.items():
                with self.subTest(page=name):
                    self.assertEqual([f["rule"] for f in findings if f["file"] == name], expected)
            third = next(f for f in findings if f["file"] == "_header.html.erb")
            self.assertEqual(third["line"], 5)  # lines 1-2 open the More; groups start on line 3
            result = self._run(project, "--json", "--screens-only")
            found = sorted(f["file"] for f in json.loads(result.stdout)["findings"] if f["rule"] == "AG035")
            self.assertEqual(found, ["three-groups.html"])

    def test_kit_never_reads_the_device_theme(self):
        for name in ("agustos.css", "agustos-chrome.js", "starter.html"):
            with self.subTest(file=name):
                self.assertNotIn("prefers-color-scheme", (ROOT / "ui" / name).read_text(encoding="utf-8"))

    def test_retired_screen_rules_stay_retired(self):
        """AG022 (button count) and AG023 (quotes) policed copy on our own sites."""
        source = self.CHECKER.read_text(encoding="utf-8")
        self.assertNotIn('"AG022"', source)
        self.assertNotIn('"AG023"', source)

    def test_skip_dirs_match_below_the_scan_root_only(self):
        """A project that lives in a folder named dist, build or vendor must
        still be scanned. Only folders below the root are skipped."""
        import tempfile
        page = self._screen_page("products", main="<p>Catalog</p>")
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "dist"
            (project / "node_modules").mkdir(parents=True)
            (project / "index.html").write_text(page, encoding="utf-8")
            (project / "node_modules" / "bad.html").write_text(
                self._screen_page("landing"), encoding="utf-8")
            result = self._run(project, "--json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["filesScanned"], 1)

    def test_screens_only_checks_the_rendered_pages_of_a_build(self):
        """An Astro layout fills data-screen at render time, so the source scan
        skips the screen rules. --screens-only runs them on the built HTML and
        nothing else: the kit CSS is bundled under hashed names in _astro/, so
        the project-wide rules would report false findings there."""
        import tempfile
        primary = '<a class="agustos-button agustos-button--primary" href="#">Request pricing</a>'
        rendered = (
            '<!doctype html><html lang="en"><head>'
            '<link rel="stylesheet" href="/_astro/index.3f9a1c.css"></head>'
            '<body class="brand-memregunes" data-screen="{screen}">'
            '<main id="main">{main}</main></body></html>'
        )
        redirect = (
            '<!doctype html><title>Redirecting to: /about/</title>'
            '<meta http-equiv="refresh" content="0;url=/about/">'
            '<body><a href="/about/">Redirecting to <code>/about/</code></a></body>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            build = Path(tmp) / "dist"
            (build / "_astro").mkdir(parents=True)
            (build / "tr").mkdir()
            (build / "_astro" / "index.3f9a1c.css").write_text(
                ".hero { color: #cf142a; }", encoding="utf-8")
            (build / "index.html").write_text(
                rendered.format(screen="home", main='<h1><mark class="type-highlight">Light</mark></h1>' + primary),
                encoding="utf-8")
            (build / "tr" / "index.html").write_text(
                rendered.format(screen="landing", main=primary), encoding="utf-8")
            (build / "old-about.html").write_text(redirect, encoding="utf-8")

            result = self._run(build, "--screens-only", "--json")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["filesScanned"], 3)
            self.assertEqual(
                [(f["rule"], f["file"]) for f in report["findings"]],
                [("AG021", str(Path("tr") / "index.html"))],
            )

            (build / "tr" / "index.html").write_text(
                rendered.format(screen="products", main=primary), encoding="utf-8")
            self.assertEqual(self._run(build, "--screens-only").returncode, 0)

    def test_screen_rules_read_markup_not_inline_scripts_or_styles(self):
        """v7.4.1: Astro inlines a small processed script, so a site that imports
        agustos-chrome.js gets its selector `.site-sidebar[popover]` in every
        page. Class names and attributes inside <script> and <style> are code,
        not markup: they must not fire a screen rule. A real sidebar still warns,
        at its own line."""
        import tempfile
        chrome = (ROOT / "ui" / "agustos-chrome.js").read_text(encoding="utf-8")
        self.assertIn(".site-sidebar", chrome)  # the case this test guards
        menu = "".join(f'<a class="site-header__link" href="/{n}">Item {n}</a>' for n in range(4))
        page = (
            '<!doctype html><html lang="tr"><head>\n'
            '<link rel="stylesheet" href="/_astro/index.css">\n'
            '<style>[data-theme="dark"] .site-sidebar { color: red }\n'
            '.type-highlight, .type-highlight { }</style>\n'
            '</head><body class="brand-pld" data-screen="content">\n'
            '<header class="site-header"><nav class="site-header__nav">' + menu + '</nav></header>\n'
            '<script type="module">' + chrome + '\n'
            'const tpl = `<a class="site-header__link"></a>`.repeat(6) + \'<div class="container">\';\n'
            'document.body.insertAdjacentHTML("beforeend", \'<mark class="type-highlight"></mark>\'.repeat(2));\n'
            '</script>\n'
            '<main id="main"><div class="container container--reading"><p>Metin</p></div></main>\n'
            '@EXTRA@</body></html>\n'
        )
        with tempfile.TemporaryDirectory() as tmp:
            build = Path(tmp) / "dist"
            build.mkdir()
            (build / "index.html").write_text(page.replace("@EXTRA@", ""), encoding="utf-8")
            report = json.loads(self._run(build, "--screens-only", "--json").stdout)
            self.assertEqual(report["findings"], [])

            real = '<aside id="site-sidebar" class="site-sidebar" popover></aside>\n'
            text = page.replace("@EXTRA@", real)
            (build / "index.html").write_text(text, encoding="utf-8")
            report = json.loads(self._run(build, "--screens-only", "--json").stdout)
            self.assertEqual(
                [(f["rule"], f["line"]) for f in report["findings"]],
                [("AG026", text[:text.find(real)].count("\n") + 1)],
            )

    def test_screens_only_warns_on_a_parent_marked_as_the_current_page(self):
        """AG029 (v7.3.2): in built output the file path is the page's own URL,
        so a link marked aria-current="page" that points above the page is a
        parent section announced as the current page. It warns only."""
        import tempfile
        page = (
            '<!doctype html><html lang="tr"><head>'
            '<link rel="stylesheet" href="/_astro/index.css"></head>'
            '<body class="brand-agustos" data-screen="content">'
            '<header class="site-header"><nav class="site-header__nav">{links}</nav></header>'
            '<main id="main"><div class="container container--reading"><p>Metin</p></div></main></body></html>'
        )
        link = '<a class="site-header__link" href="{0}" aria-current="{1}">x</a>'
        cases = {
            # file: (links, expected AG029 count)
            "haberler/guncel/index.html": (link.format("/haberler/", "page"), 1),
            "haberler/eski.html": (link.format("/haberler", "page"), 1),
            "blog/post/index.html": (link.format("/", "page"), 1),
            "haberler/index.html": (link.format("/haberler/", "page"), 0),
            "about.html": (link.format("/about/", "page"), 0),
            "index.html": (link.format("/", "page"), 0),
            "urunler/px22/index.html": (link.format("/urunler/", "true"), 0),
            "haberciler/index.html": (link.format("/haber", "page"), 0),
            "app/index.html": (link.format("#validation", "page"), 0),
        }
        with tempfile.TemporaryDirectory() as tmp:
            build = Path(tmp) / "dist"
            for name, (links, _) in cases.items():
                target = build / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(page.format(links=links), encoding="utf-8")
            result = self._run(build, "--screens-only", "--json")
            report = json.loads(result.stdout)
            found: dict[str, int] = {}
            for finding in report["findings"]:
                if finding["rule"] == "AG029":
                    self.assertEqual(finding["level"], "warn")
                    key = Path(finding["file"]).as_posix()
                    found[key] = found.get(key, 0) + 1
            for name, (_, expected) in cases.items():
                with self.subTest(file=name):
                    self.assertEqual(found.get(name, 0), expected)
            # A warning alone never fails the build.
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_warns_on_a_disabled_link_that_keeps_its_href(self):
        """AG030 (v7.3.3): aria-disabled does not stop a link. A disabled link
        drops its href; one that keeps it warns, in source and in built pages."""
        import tempfile
        page = (
            '<!doctype html><html lang="tr"><head>'
            '<link rel="stylesheet" href="/_astro/index.css"></head>'
            '<body class="brand-agustos" data-screen="static">'
            '<main id="main"><div class="container">{links}</div></main></body></html>'
        )
        cases = {
            # file: (links, expected AG030 count)
            "kept.html": ('<a class="agustos-button" href="/teklif" aria-disabled="true">Teklif</a>', 1),
            "single.html": ("<a href='/teklif' aria-disabled='TRUE'>Teklif</a>", 1),
            "dropped.html": ('<a class="agustos-button" role="link" aria-disabled="true">Teklif</a>', 0),
            "enabled.html": ('<a class="agustos-button" href="/teklif" aria-disabled="false">Teklif</a>', 0),
            "button.html": ('<button class="agustos-button" type="button" disabled>Teklif</button>', 0),
            "comment.html": ('<!-- <a href="/x" aria-disabled="true">x</a> --><p>Metin</p>', 0),
        }
        with tempfile.TemporaryDirectory() as tmp:
            build = Path(tmp) / "dist"
            build.mkdir()
            for name, (links, _) in cases.items():
                (build / name).write_text(page.format(links=links), encoding="utf-8")
            for flags in ((), ("--screens-only",)):
                with self.subTest(flags=flags):
                    report = json.loads(self._run(build, *flags, "--json").stdout)
                    found: dict[str, int] = {}
                    for finding in report["findings"]:
                        if finding["rule"] == "AG030":
                            self.assertEqual(finding["level"], "warn")
                            key = Path(finding["file"]).as_posix()
                            found[key] = found.get(key, 0) + 1
                    for name, (_, expected) in cases.items():
                        self.assertEqual(found.get(name, 0), expected, name)

    def test_source_scan_skips_the_current_link_rule(self):
        """In a source tree the file path is not the URL, so AG029 stays quiet."""
        source = self.CHECKER.read_text(encoding="utf-8")
        self.assertIn("check_current_links(rel, path.relative_to(root).as_posix(), text, findings)", source)
        call = source.index("check_current_links(rel, path")
        self.assertLess(source.rfind("if screens_only:", 0, call), call)
        self.assertLess(call, source.index("continue", call))

    def test_screens_only_refuses_to_report_clean_without_rendered_pages(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "Layout.astro").write_text(
                "<body data-screen={screen}><slot /></body>", encoding="utf-8")
            result = self._run(Path(tmp), "--screens-only")
            self.assertEqual(result.returncode, 2)
            self.assertIn("nothing was checked", result.stderr)

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
            "site-header__link", "site-header__more", "site-header__more-menu", "site-header__more-link",
            "site-header__end", "site-header__cta", "site-header__burger",
            "site-footer", "site-footer__inner", "site-footer__brand", "site-footer__links", "site-footer__link",
            "breadcrumb", "breadcrumb__link",
        ):
            self.assertIn(name, declared, name)
        for retired in ("site-footer__cols", "site-footer__col", "site-footer__col-heading",
                        "site-footer__list", "site-footer__cta", "hero-links", "hero-link", "hero-action"):
            self.assertNotIn(retired, declared, retired)

    def test_drawers_are_native_popovers_and_the_sidebar_is_forced_open_on_desktop(self):
        self.assertIn(".site-sidebar:not(:popover-open) { display: none; }", self.CSS)
        self.assertIn(".site-header__panel:popover-open { display: flex; }", self.CSS)
        self.assertIn("::backdrop", self.CSS)
        self.assertNotIn("data-nav-open", self.CSS)

    def test_sidebar_width_comes_from_the_chrome_recipe(self):
        self.assertIn("--sidebar-width: 240px", self.CSS)
        self.assertIn("padding-inline-start: var(--sidebar-width)", self.CSS)

    def test_footer_is_light_and_carries_no_button(self):
        self.assertIn("--footer-paper: #ffffff;", self.CSS)
        self.assertNotIn(".site-footer .agustos-button", self.CSS)

    def test_logo_hover_swaps_the_ink(self):
        """Ağustos red turns black on hover; every other house brand turns red."""
        self.assertIn(".site-lockup:hover { color: var(--signal); text-decoration: none; }", self.CSS)
        self.assertIn(".brand-agustos .site-lockup:hover { color: var(--ink); }", self.CSS)

    def test_more_menu_and_highlighter_ship(self):
        self.assertIn(".site-header__more-menu {", self.CSS)
        self.assertIn("mark.type-highlight,", self.CSS)

    def test_anchor_lands_below_the_sticky_sidebar_bar(self):
        # The bar and the scroll offset read one variable, built from tokens.
        self.assertIn("--sidebar-bar-height: calc(var(--control-min) + 2 * var(--space-xs) + 1px);", self.CSS)
        self.assertIn("min-height: var(--sidebar-bar-height);", self.CSS)
        rule = "html:has(.site-sidebar-bar) { scroll-padding-top: calc(var(--sidebar-bar-height) + var(--anchor-snap)); }"
        self.assertEqual(self.CSS.count("scroll-padding-top"), 4, "the sidebar bar, the top menu, its phone search row and the print reset")
        # Only below 1024px, where the bar is sticky. Desktop has no bar.
        drawers = self.CSS.index("@media (max-width: 1023px) {\n  /* An in-page anchor")
        self.assertIn(rule, self.CSS[drawers:self.CSS.index("\n}\n", drawers)])

    def test_anchor_lands_below_the_sticky_top_menu(self):
        # v7.0.2: the top menu is sticky at every width, so its offset sits outside any media query.
        self.assertIn("--site-header-height: calc(var(--control-min) + 2 * 10px + 1px);", self.CSS)
        self.assertIn("min-height: var(--site-header-height);", self.CSS)
        rule = "html:has(.site-header) { scroll-padding-top: calc(var(--site-header-height) + var(--anchor-snap)); }"
        self.assertIn(rule, self.CSS)
        self.assertLess(self.CSS.index(rule), self.CSS.index("@media (max-width: 1023px) {\n  /* An in-page anchor"))

    def test_search_results_keep_the_focus_ring(self):
        # v7.0.2 fixed a removed ring in both adapters; v7.3.0 moves the rule into the kit once.
        self.assertIn(".site-header__search-result a:focus-visible { background: var(--surface); color: var(--ink); outline: 2px solid var(--focus, var(--signal));", self.CSS)
        self.assertNotRegex(self.CSS, r"search-result a:focus-visible\s*\{[^}]*outline:\s*(0|none)")

    def test_search_and_language_are_styled_in_the_kit_only(self):
        """B2 (v7.3.0): the adapters carry no copy of the search or language styles."""
        for path in ("adapters/astro/src/components/Header.astro",
                     "adapters/astro/src/components/HeaderSearch.astro",
                     "adapters/astro/src/components/HeaderUtility.astro",
                     "adapters/rails/app/assets/stylesheets/agustos/components.css"):
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertNotRegex(text, r"\.site-header__(search|lang-link|utility|icon-btn)[\w-]*\s*[{,]")
        # Text in the search reads at 4.5:1 or better: --ink-soft, never --ink-faint.
        start = self.CSS.index("/* --- Header search and utility")
        block = self.CSS[start:self.CSS.index("/* --- Footer.", start)]
        self.assertNotRegex(block, r"(?<!-)color:\s*var\(--ink-faint\)")
        self.assertIn("font-size: var(--size-form-field);", block)

    def test_starter_renders_the_search_and_language_classes(self):
        """UI-KIT.md says copy the chrome from starter.html (Codex, PR #71)."""
        import re
        html = (ROOT / "ui" / "starter.html").read_text(encoding="utf-8")
        used = {c for value in re.findall(r'class="([^"]+)"', html) for c in value.split()}
        for name in TOKENS["compatibility"]["cssClasses"]:
            if re.match(r"site-header__(search|lang-link|utility|icon-btn|theme|noscript)", name):
                with self.subTest(name=name):
                    self.assertIn(name, used)

    def test_phone_anchor_offset_includes_the_search_row(self):
        self.assertIn("--site-header-search-height: calc(var(--control-min) + 2 * var(--space-xs) + 1px);", self.CSS)
        self.assertIn("html:has(.site-header__search-row) { scroll-padding-top: calc(var(--site-header-height) + var(--site-header-search-height) + var(--anchor-snap)); }", self.CSS)

    def test_chrome_heights_equal_the_rendered_chrome(self):
        """v7.3.2: a Chromium probe of ui/starter.html measured the top menu at
        65px at 1440 and 375px, and the header with its phone search row at
        126px (65 + 61). The variables add up to the same numbers from the tokens."""
        chrome = TOKENS["recipes"]["chrome"]
        px = lambda value: float(str(value).removesuffix("px"))
        control = px(TOKENS["foundations"]["measure"]["controlMinimum"]["$value"])
        padding = px(chrome["paddingBlock"]["$value"])
        rule = px(TOKENS["foundations"]["border"]["hairline"]["$value"])
        self.assertRegex(self.CSS, r"--space-xs:\s+8px;")
        self.assertEqual(control + 2 * padding + rule, 65)
        self.assertEqual(control + 2 * 8 + rule, 61)
        self.assertIn(f"--site-header-height: calc(var(--control-min) + 2 * {padding:g}px + {rule:g}px);", self.CSS)

    def test_anchor_offsets_add_one_pixel_for_whole_pixel_scrolling(self):
        """A browser scrolls to whole pixels, so a target at a fractional
        position stopped up to 0.5px under the 65px header in the probe (64.5 to
        65.5px). Every anchor offset adds --anchor-snap, so no target stops under it."""
        import re
        self.assertIn("--anchor-snap: 1px;", self.CSS)
        offsets = re.findall(r"scroll-padding-top: ([^;]+);", self.CSS)
        self.assertEqual(len(offsets), 4)
        for value in offsets:
            with self.subTest(value=value):
                self.assertTrue(value == "0" or value.endswith("+ var(--anchor-snap))"), value)

    def test_top_menu_stays_on_one_row(self):
        """Long Turkish labels wrapped the menu to two rows at 1024px (v7.1.0)."""
        self.assertIn("flex-wrap: nowrap; justify-content: center; align-items: center; gap: 28px; }", self.CSS)
        self.assertIn("white-space: nowrap;", self.CSS[self.CSS.index(".site-header__link {"):])
        small = self.CSS.index("@media (min-width: 1024px) and (max-width: 1279px) {")
        self.assertIn(".site-header__nav { gap: var(--space-lg); }", self.CSS[small:small + 400])

    def test_hover_is_a_gray_rule_and_red_marks_the_current_page(self):
        """Emre chose option C (2026-09-30): hover darkens the ink over a 1px
        gray rule; the 2px red rule means the current page alone."""
        for hover in (".site-header__link:hover {", ".site-sidebar__link:hover {", ".agustos-chrome-link:hover {"):
            block = self.CSS[self.CSS.index(hover):]
            block = block[:block.index("}")]
            with self.subTest(rule=hover):
                self.assertIn("var(--ink-faint)", block)
                self.assertNotIn("var(--signal)", block)
        self.assertIn('.site-header__more:has([aria-current="page"], [aria-current="true"]) > summary {', self.CSS)
        self.assertIn('.site-sidebar__group:not([open]):has([aria-current="page"], [aria-current="true"]) > summary { border-inline-start-color: var(--signal); }', self.CSS)

    def test_the_red_rule_marks_the_current_page_and_its_section(self):
        """v7.3.2: a parent item on a nested route carries aria-current="true",
        not "page", so a screen reader does not announce it as the current page.
        Every chrome selector that highlights "page" highlights "true" too.
        Breadcrumbs keep "page" only: their last item is the page itself."""
        import re
        both = '[aria-current="page"], [aria-current="true"]'
        for selector in (
            f".agustos-chrome-link:is({both}) {{",
            f".site-sidebar__link:is({both}) {{",
            f".site-sidebar__group:has({both}) > summary {{ color: var(--ink); }}",
            f".site-sidebar__group:not([open]):has({both}) > summary {{ border-inline-start-color: var(--signal); }}",
            f".site-sidebar__link:hover:not({both}) {{",
            f".site-header__link:is({both}),\n.site-header__more:has({both}) > summary {{",
            f".site-header__more-link:is({both}) {{ background: var(--surface);",
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, self.CSS)
        # No chrome selector matches "page" alone; only the breadcrumb does.
        page_only = [line for line in self.CSS.splitlines()
                     if re.search(r'\[aria-current="page"\](?!, \[aria-current="true"\])', line)]
        self.assertEqual(page_only, ['.breadcrumb [aria-current="page"] { color: var(--ink); }'])
        # The header rule draws the 2px red rule for both states.
        start = self.CSS.index(f".site-header__link:is({both}),")
        block = self.CSS[start:self.CSS.index("}", start)]
        self.assertIn("border-block-end-color: var(--signal);", block)

    def test_nested_screens_mark_the_parent_section_true(self):
        """A post and a product sit below the menu item they belong to."""
        for screen, href in (("content", "/blog"), ("product", "/urunler"), ("spec-sheet", "/urunler")):
            html = (ROOT / "screens" / f"{screen}.html").read_text(encoding="utf-8")
            with self.subTest(screen=screen):
                self.assertIn(f'<a class="site-header__link" href="{href}" aria-current="true">', html)
                self.assertNotIn(f'href="{href}" aria-current="page"', html)

    def test_drawers_close_from_inside_and_hold_the_page_still(self):
        drawers = self.CSS.index("@media (max-width: 1023px) {\n  /* An in-page anchor")
        block = self.CSS[drawers:self.CSS.index("\n}\n", drawers)]
        self.assertIn("html:has(.site-header__panel:popover-open),\n  html:has(.site-sidebar:popover-open) { overflow: hidden; }", block)
        self.assertIn(".site-header__close {\n    display: inline-flex;", block)
        self.assertIn(".site-sidebar__close {\n    display: inline-flex;", block)
        # Hidden on desktop: they share the burger rule, which starts at display: none.
        self.assertIn(".site-sidebar-burger,\n.site-header__burger,\n.site-sidebar__close,\n.site-header__close {\n  display: none;", self.CSS)

    def test_print_drops_the_chrome(self):
        start = self.CSS.index("@media print {")
        block = self.CSS[start:self.CSS.index("\n}\n", start)]
        for selector in (".site-header", ".site-sidebar,", ".site-sidebar-bar", ".site-footer nav"):
            self.assertIn(selector, block)

    def test_chrome_script_ships_and_closes_more_and_drawers(self):
        """JavaScript only when it is the logical choice (Emre, 2026-09-30). A native
        popover does not close when focus leaves it, so the script closes an open
        drawer then; focus never lands on the page behind it (v7.3.3)."""
        script = (ROOT / "ui" / "agustos-chrome.js").read_text(encoding="utf-8")
        self.assertIn("details.site-header__more[open]", script)
        self.assertIn("'.site-header__panel[popover], .site-sidebar[popover]'", script)
        self.assertIn("drawer.hidePopover()", script)
        for event in ("'keydown'", "'click'", "'focusout'"):
            self.assertIn(event, script)
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        self.assertIn("agustos-chrome.js", kit["files"])

    def test_drawer_opens_every_more_by_script(self):
        """v7.7.0: below 1024px the drawer shows every More open (model: turso.tech
        phone menu). CSS cannot open a closed details, so the script does it when
        the drawer opens, and the close rules skip those menus."""
        script = (ROOT / "ui" / "agustos-chrome.js").read_text(encoding="utf-8")
        self.assertIn("matchMedia('(max-width: 1023px)')", script)
        self.assertIn("details.site-header__more[open]:not([data-agustos-unfold])", script)
        self.assertIn("addEventListener('toggle'", script)
        self.assertIn("}, true);", script)  # toggle does not bubble: listen in the capture phase
        self.assertIn("dataset.agustosUnfold", script)
        self.assertIn("setAttribute('tabindex', '-1')", script)

    def test_chrome_script_clears_stale_unfold_marks(self):
        """A Turbo snapshot or a page from the back-forward cache can bring back a
        More that the drawer marked. On a wide screen no close rule closes it and
        the keyboard cannot reach its summary. The script clears the marks before
        Turbo caches the page, and on start, on pageshow and on a toggle when the
        screen is 1024px or wider (IESDesk uses Turbo)."""
        script = (ROOT / "ui" / "agustos-chrome.js").read_text(encoding="utf-8")
        self.assertIn("document.addEventListener('turbo:before-cache', () => unfold(false));", script)
        self.assertIn("window.addEventListener('pageshow', heal);", script)
        heal = script[script.index("function heal()"):]
        self.assertIn("if (!DRAWER_MODE.matches) unfold(false);", heal[:heal.index("\n")])
        import shutil
        import subprocess
        node = shutil.which("node")
        if not node:
            self.skipTest("node is not installed: the behaviour half of this test needs it")
        harness = r"""
const source = require('fs').readFileSync(process.argv[1], 'utf8');
function run(wide, premarked) {
  const listeners = {}, winListeners = {}, media = { matches: !wide, addEventListener() {} };
  const summary = () => { const attrs = {}; return { attrs, setAttribute(k, v) { attrs[k] = v; }, removeAttribute(k) { delete attrs[k]; }, focus() {} }; };
  const menus = [0, 1].map(() => ({ dataset: {}, open: false, summary: summary(), querySelector() { return this.summary; },
    matches(selector) { return selector === 'details[data-agustos-unfold]' ? 'agustosUnfold' in this.dataset : false; } }));
  if (premarked) menus.forEach((menu) => { menu.dataset.agustosUnfold = ''; menu.open = true; menu.summary.attrs.tabindex = '-1'; });
  const panel = { matches(selector) { return selector === '.site-header__panel[popover]' || selector === ':popover-open'; } };
  const document = { documentElement: {}, addEventListener(name, fn) { (listeners[name] ||= []).push(fn); },
    querySelectorAll(selector) { return selector === '.site-header__panel details.site-header__more' ? menus : []; } };
  const window = { matchMedia: () => media, addEventListener(name, fn) { (winListeners[name] ||= []).push(fn); } };
  new Function('document', 'window', 'localStorage', source)(document, window, {});
  const fire = (bag, name, event = {}) => (bag[name] || []).forEach((fn) => fn(event));
  const marked = () => menus.filter((menu) => 'agustosUnfold' in menu.dataset || menu.open || menu.summary.attrs.tabindex).length;
  return { media, menus, panel, marked, doc: (n, e) => fire(listeners, n, e), win: (n, e) => fire(winListeners, n, e) };
}
const out = {};
let page = run(true, true);
out.start = page.marked();
page = run(false, false);
page.doc('toggle', { target: page.panel });
out.drawer = page.marked();
page.doc('turbo:before-cache');
out.beforeCache = page.marked();
page.doc('toggle', { target: page.panel });
page.media.matches = false;
page.win('pageshow', { persisted: true });
out.pageshow = page.marked();
page.media.matches = true;
page.doc('toggle', { target: page.panel });
page.media.matches = false;
page.menus[0].open = false;
page.doc('toggle', { target: page.menus[0] });
out.toggle = page.marked();
console.log(JSON.stringify(out));
"""
        result = subprocess.run([node, "-e", harness, str(ROOT / "ui" / "agustos-chrome.js")],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout),
                         {"start": 0, "drawer": 2, "beforeCache": 0, "pageshow": 0, "toggle": 0})

    def test_unfold_css_needs_the_script(self):
        """Without the script each More folds and opens on a tap, as before."""
        drawer = self.CSS[self.CSS.index("@media (max-width: 1023px) {", self.CSS.index(".site-header__panel {")):]
        drawer = drawer[:drawer.index("\n}\n")]
        self.assertIn(".site-header__more[data-agustos-unfold] > summary {", drawer)
        self.assertIn(".site-header__more[data-agustos-unfold] > summary::after { display: none; }", drawer)
        self.assertNotIn(".site-header__more > summary { display: none", drawer)

    def test_drawer_fills_a_phone_screen(self):
        """v7.7.0 (Emre, 2026-10-03): below 640px the drawer covers the whole
        screen width, like the turso.tech phone menu."""
        start = self.CSS.index("@media (max-width: 639px) {")
        block = self.CSS[start:self.CSS.index("\n}\n", start)]
        self.assertIn(".site-header__panel", block)
        self.assertIn("width: 100%", block)

    def test_sidebar_drawer_fills_a_phone_screen_too(self):
        """One drawer rule for every site: the sidebar drawer of the product UI
        gets the same full width below 640px as the top-menu panel."""
        start = self.CSS.index("@media (max-width: 639px) {")
        block = self.CSS[start:self.CSS.index("\n}\n", start)]
        self.assertIn(".site-sidebar", block)
        self.assertIn("width: 100%; max-width: none;", block)
        # From 640px to 1023px both drawers keep the narrow width.
        drawer = self.CSS[self.CSS.index("@media (max-width: 1023px) {\n  /* An in-page anchor"):]
        drawer = drawer[:drawer.index("\n}\n")]
        self.assertIn(".site-sidebar { width: min(320px, 86vw); }", drawer)
        self.assertIn("width: min(320px, 86vw);", drawer[drawer.index(".site-header__panel {"):])
        # The phone rule comes after the drawer block, so it wins at equal weight.
        self.assertLess(self.CSS.index("@media (max-width: 1023px) {\n  /* An in-page anchor"), start)

    THEME_SCRIPT = 'try{if(localStorage.getItem("agustos:theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}'

    def test_theme_script_is_published_once_and_used_everywhere(self):
        """The no-flash head script has one source: the builder. It only sets dark;
        a page with no stored choice stays light (v7.7.0)."""
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        self.assertEqual(kit["themeScript"], self.THEME_SCRIPT)
        self.assertEqual(kit["themeStorageKey"], "agustos:theme")
        self.assertIn(self.THEME_SCRIPT, (ROOT / "ui" / "UI-KIT.md").read_text(encoding="utf-8"))
        starter = (ROOT / "ui" / "starter.html").read_text(encoding="utf-8")
        self.assertEqual(starter.count(self.THEME_SCRIPT), 1)
        self.assertLess(starter.index(f"<script>{self.THEME_SCRIPT}</script>"), starter.index('href="./agustos-fonts.css"'))
        # One switch behaviour: no demo button sets data-theme on its own.
        self.assertNotIn("dataset.theme", starter)
        # The demo account list is open, and the chrome script closes it on an outside click.
        self.assertIn("The list below is shown open; a click outside closes it.", starter)
        self.assertNotIn("data-agustos-unfold", starter)

    def test_chrome_script_flips_and_keeps_the_theme(self):
        script = (ROOT / "ui" / "agustos-chrome.js").read_text(encoding="utf-8")
        self.assertIn("'[data-agustos-theme]'", script)
        self.assertIn("'agustos:theme'", script)
        self.assertIn("removeAttribute('data-theme')", script)
        self.assertIn("setAttribute('data-theme', 'dark')", script)
        # Blocked storage must never break the switch.
        flip = script[script.index("function flipTheme"):]
        flip = flip[:flip.index("\n  }\n")]
        self.assertIn("try {", flip)
        self.assertNotIn("prefers-color-scheme", script)

    def test_theme_switch_label_is_css_driven(self):
        """Both labels are in the markup; CSS shows the one the button switches to,
        so a swapped page body needs no repaint and the name never lags."""
        self.assertIn(".agustos-theme-switch__to-light,\nhtml[data-theme=\"dark\"] .agustos-theme-switch__to-dark { display: none; }", self.CSS)
        self.assertIn('html[data-theme="dark"] .agustos-theme-switch__to-light { display: inline-flex; }', self.CSS)
        # In the bar the label is hidden but stays the accessible name; the drawer shows it.
        bar = self.CSS[self.CSS.index(".site-header__icon-btn .agustos-theme-switch__label {"):]
        self.assertIn("clip-path: inset(50%);", bar[:bar.index("}")])
        self.assertNotIn("display: none", bar[:bar.index("}")])
        drawer = self.CSS[self.CSS.index("@media (max-width: 1023px) {", self.CSS.index(".site-header__panel {")):]
        self.assertIn(".site-header__panel .site-header__icon-btn .agustos-theme-switch__label", drawer)
        # The drawer switch starts on the same line as the drawer links, which have no inline padding.
        self.assertIn(".site-header__panel .site-header__icon-btn.agustos-theme-switch { width: auto; justify-content: flex-start; padding-inline: 0; }", drawer)
        for name in ("agustos-theme-switch", "agustos-theme-switch__to-dark", "agustos-theme-switch__to-light", "agustos-theme-switch__label"):
            with self.subTest(name=name):
                self.assertIn(name, TOKENS["compatibility"]["cssClasses"])

    def test_house_brand_lockups_turn_white_on_dark_and_agustos_stays_red(self):
        # `:where` keeps these below the hover rules, so the hover swap works in dark too (v7.0.1).
        self.assertIn('html[data-theme="dark"] :where(.site-lockup) { color: var(--ink); }', self.CSS)
        self.assertIn('html[data-theme="dark"] :where(.brand-agustos .site-lockup) { color: var(--brand); }', self.CSS)

    def test_contents_list_is_published(self):
        """v7.4.0: the On this page list. A folded line below 1280px; at 1280px
        and wider it is open in the side zone and stays in view. No script."""
        declared = TOKENS["compatibility"]["cssClasses"]
        for name in ("agustos-contents", "agustos-contents__toggle", "agustos-contents__title",
                     "agustos-contents__list", "agustos-contents__link"):
            self.assertIn(name, declared, name)
        self.assertIn(".container--reading {\n  position: relative;\n}", self.CSS)
        # v7.4.2: 24px above the folded line, so it does not hug the page opening.
        self.assertIn(".agustos-contents {\n  margin: var(--space-xl) 0 var(--space-2xl);", self.CSS)
        self.assertIn(".agustos-contents__title {\n  display: none;", self.CSS)
        self.assertIn("min-height: var(--control-min);\n  padding-inline-start: var(--space-md);", self.CSS)
        self.assertIn("@media (min-width: 1280px) {\n  .agustos-contents {\n    position: absolute;", self.CSS)
        self.assertIn("inset-inline-start: calc(var(--measure-gutter) + var(--measure-body) + var(--space-xl));", self.CSS)
        # v7.6.2: a page that opens with a breadcrumb starts 16px under the menu,
        # so the list starts under the trail (16 + 44 + 24px) to sit level with the H1.
        self.assertIn(
            "  .container--reading:has(> nav:first-child > .breadcrumb) > .agustos-contents {\n"
            "    padding-block-start: calc(16px + var(--control-min) + 24px);\n  }",
            self.CSS,
        )
        self.assertIn("@supports selector(::details-content) {", self.CSS)
        self.assertIn("    .agustos-contents::details-content {\n      display: block;\n      content-visibility: visible;\n      position: sticky;", self.CSS)
        self.assertIn("max-block-size: calc(100vh - var(--site-header-height) - 2 * var(--space-xl));", self.CSS)
        # Final review: the kit's bare ol and p rules set body size, so the list
        # and the title inherit the compact size of the component.
        self.assertIn(".agustos-contents__title {\n  display: none;\n  margin: 0 0 var(--space-xs);\n  color: var(--ink);\n  font-family: var(--display);", self.CSS)
        self.assertRegex(self.CSS, r"\.agustos-contents__title \{[^}]*font-size: inherit;")
        self.assertRegex(self.CSS, r"\.agustos-contents__list \{[^}]*font-size: inherit;")
        # A printed page has no use for the list.
        start = self.CSS.index("@media print {")
        self.assertIn(".agustos-contents", self.CSS[start:start + 400])

    def test_audit_defects_stay_fixed(self):
        """v7.5.1, from the 2026-10-01 kit audit. Each one was measured in a
        browser before and after the fix."""
        # A kit class that sets display outweighed the browser's [hidden] rule.
        self.assertIn('[hidden]:not([hidden="until-found"]) { display: none !important; }', self.CSS)
        # A card without a link does not answer the pointer; a marked card keeps its rule.
        self.assertNotIn(".agustos-card:hover {", self.CSS)
        self.assertIn(".agustos-card:has(:is(h2, h3, h4) > a):hover {", self.CSS)
        self.assertIn(".agustos-card--marked:has(:is(h2, h3, h4) > a):hover {\n  border-left-color: var(--ink);\n}", self.CSS)
        # a:hover turned the skip link red on its ink box (3.35:1).
        self.assertIn(".skip-link:hover { color: var(--paper); }", self.CSS)
        # A printer drops backgrounds: code and the primary button print as outlines.
        print_block = self.CSS[self.CSS.index("@media print {"):]
        self.assertIn("  .agustos-button--primary {\n    background: none;\n    color: var(--ink);\n  }", print_block)
        self.assertIn(".type-code-block { border: 1px solid var(--ink-faint); }", print_block)

    def test_layout_layer_is_published(self):
        declared = TOKENS["compatibility"]["cssClasses"]
        for name in ("stack", "cluster", "grid-2", "grid-3", "grid-4", "grid-aside", "band", "band--cream", "prose"):
            self.assertIn(name, declared, name)
        self.assertIn(".grid-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }", self.CSS)
        self.assertIn(".band--cream { background: var(--cream);", self.CSS)
        self.assertIn(".prose { max-width: var(--measure-body); }", self.CSS)
        # v7.3.1: one reading line in rem. The text of a content page and the
        # footer contact block end on it; the side zone starts after --space-xl.
        self.assertIn("--measure-body: 41rem;", self.CSS)
        self.assertIn(".container--reading > * {\n  max-width: var(--measure-body);\n}", self.CSS)
        self.assertNotIn("calc(var(--measure-body) + 2 * var(--measure-gutter))", self.CSS)
        # v7.3.4: a reading page is one article. A section and an H2 take one
        # 40px break, a margin that collapses with the last margin above it.
        self.assertIn(".container--reading .agustos-section {\n  padding-block: 0;\n  margin-top: var(--space-3xl);\n}", self.CSS)
        # v7.3.5: two steps above a heading, on every page. An H2 takes 40px,
        # an H3 and an H4 take 32px; 2.5em of the heading size gave 108px
        # and 53px, so a subheading took more space than a section (issue 75).
        self.assertNotIn("margin: 2.5em 0 1em;\n  color: var(--ink", self.CSS)
        # v7.6.0: the space below a heading is a fixed step, smaller than the
        # space above, so the heading binds to its text (1em gave 55px under an
        # H1 and 43px under an H2).
        self.assertIn("  margin: var(--space-before-h2) 0 var(--space-after-h2);\n  color: var(--ink);\n}", self.CSS)
        self.assertIn("  margin: var(--space-before-h3) 0 var(--space-after-h3);\n", self.CSS)
        self.assertIn("  margin: var(--space-before-h3) 0 var(--space-after-h4);\n", self.CSS)
        self.assertIn("  margin: 0 0 var(--space-after-title);\n  color: var(--ink);\n}", self.CSS)
        for name, value in (("before-h2", "40px"), ("before-h3", "32px"), ("after-title", "32px"),
                            ("after-h2", "20px"), ("after-h3", "12px"), ("after-h4", "8px")):
            self.assertIn(f"--space-{name}: {value};", self.CSS)
        self.assertNotIn(".container--reading > :is(h2, .type-h2)", self.CSS)
        # A <section> inside a section is a subsection: its heading keeps the
        # break of its level (the IESDesk privacy notice H3s showed 16px).
        self.assertIn(".agustos-section section > :is(h2, .type-h2):first-child {\n  margin-top: var(--space-3xl);\n}", self.CSS)
        self.assertIn(".agustos-section section > :is(h3, h4, .type-h3, .type-h4):first-child {\n  margin-top: var(--space-2xl);\n}", self.CSS)
        self.assertIn("grid-template-columns: minmax(0, var(--measure-body)) minmax(0, 1fr);\n  gap: var(--space-2xl) var(--space-xl);", self.CSS)
        self.assertIn("@media (max-width: 1279px) {\n  .site-footer__map { grid-template-columns: minmax(0, 1fr); }\n}", self.CSS)
        self.assertIn(".grid-aside { display: grid; grid-template-columns: minmax(240px, 1fr) minmax(0, 3fr);", self.CSS)
        self.assertIn(".stack { display: flex; flex-direction: column; }", self.CSS)
        self.assertIn(".stack > * { margin-block: 0; }", self.CSS)
        self.assertIn(".stack > * + * { margin-block-start: var(--stack-space, var(--space-md)); }", self.CSS)
        self.assertIn('@property --stack-space { syntax: "*"; inherits: false; }', self.CSS)
        self.assertIn(".cluster { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-sm); }", self.CSS)
        self.assertIn(".grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }", self.CSS)
        self.assertIn(".grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }", self.CSS)
        self.assertIn(".band { padding-block: var(--section-space); }", self.CSS)
        self.assertIn("@media (max-width: 759px) {\n  .grid-2,\n  .grid-3,\n  .grid-4,\n  .grid-aside { grid-template-columns: minmax(0, 1fr); }\n}", self.CSS)

    def test_entry_point_carries_the_screens_table_and_brand_chrome(self):
        text = (ROOT / "ui" / "UI-KIT.md").read_text(encoding="utf-8")
        self.assertIn("| `product` | catalog | topbar | frame | light first, dark by choice |", text)
        self.assertIn("| `home` | marketing | topbar | frame | light first, dark by choice |", text)
        self.assertIn("| `static` | content | topbar | reading | light first, dark by choice |", text)
        self.assertIn("| `app-shell` | product UI | sidebar | frame | light first, dark by choice |", text)
        self.assertIn("| ağustos | `brand-agustos` | red | black |", text)
        self.assertIn("| pataraz | `brand-pataraz` | black | red |", text)
        self.assertNotIn("at most 2", text)
        self.assertIn("The kit is plain CSS. Do not add Tailwind, Bootstrap, or another utility framework.", text)
        self.assertNotIn("Tailwind preflight", text)
        for name in ("home", "static", "content", "products", "product-finder", "product", "spec-sheet", "app-shell"):
            self.assertIn(f"| `{name}` |", text)

    def test_reference_render_uses_the_website_chrome(self):
        text = (ROOT / "ui" / "starter.html").read_text(encoding="utf-8")
        self.assertIn('class="brand-agustos paper-white"', text)
        self.assertNotIn("site-sidebar", text)
        self.assertIn('popovertarget="site-header-panel"', text)
        self.assertIn('<details class="site-header__more">', text)
        self.assertIn('<mark class="type-highlight">', text)
        self.assertIn('<header class="site-header">', text)
        self.assertIn('<footer class="site-footer">', text)
        self.assertIn('class="breadcrumb"', text)
        for name in ("stack", "cluster", "grid-3", "band band--cream", "type-body prose"):
            self.assertIn(f'class="{name}"', text)
        self.assertIn('<details class="agustos-contents">', text)
        self.assertIn('<a class="agustos-contents__link" href="#contents-demo-data">', text)
        # v7.4.2: the nav label names the list; the visible title is hidden from screen readers.
        self.assertIn('<p class="agustos-contents__title" aria-hidden="true">On this page</p>', text)
        self.assertIn('<div class="container container--reading">\n      <p class="type-body">A long legal page', text)


class MemregunesBrandTest(unittest.TestCase):
    """The personal brand of Emre Güneş. Its website adopts the v7 top menu later."""

    def test_registry_entry(self):
        brands = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))["brands"]
        entry = brands["memregunes"]
        self.assertEqual(entry["wordmark"], "emre güneş")
        self.assertEqual(entry["color"], "#15130f")
        self.assertEqual(entry["domain"], "memregunes.com")
        self.assertNotIn("chrome", entry)
        self.assertNotIn("screenOverrides", entry)

    def test_generated_outputs_carry_the_brand(self):
        css = (ROOT / "ui" / "agustos.css").read_text(encoding="utf-8")
        self.assertIn(".brand-memregunes", css)
        self.assertIn("--brand-memregunes:", css)
        kit = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))
        self.assertIn("brand-memregunes", kit["brandClasses"])
        self.assertEqual(kit["brands"]["memregunes"]["domain"], "memregunes.com")

    def test_checker_brand_list_is_generated(self):
        template = (ROOT / "ui" / "check-agustos-ui.py.tmpl").read_text(encoding="utf-8")
        self.assertIn("BRAND_CLASSES = {{ui.brandClasses}}", template)
        checker = (ROOT / "ui" / "check-agustos-ui.py").read_text(encoding="utf-8")
        self.assertIn("'brand-memregunes'", checker)


class ClientBrandTest(unittest.TestCase):
    """v7.8.0: brands Ağustos builds for (HEPER, LIGMAN). Light only; own logo, colours and fonts."""

    REGISTRY = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
    CLIENTS = REGISTRY["clients"]
    KIT = json.loads((ROOT / "ui" / "kit.json").read_text(encoding="utf-8"))

    def _client_vars(self, slug):
        css = (ROOT / "ui" / "brands" / f"{slug}.css").read_text(encoding="utf-8")
        block = css[css.index(f".brand-{slug} {{"):]
        return css, dict(re.findall(r"(--[\w-]+):\s*([^;]+);", block[:block.index("}")]))

    def test_heper_and_ligman_are_registered(self):
        self.assertEqual(set(self.CLIENTS), {"heper", "ligman"})
        self.assertFalse(set(self.CLIENTS) & set(self.REGISTRY["brands"]), "a client is not a house brand")

    def test_each_client_gets_a_stylesheet_and_a_logo(self):
        for slug in self.CLIENTS:
            with self.subTest(client=slug):
                css, variables = self._client_vars(slug)
                self.assertTrue((ROOT / "ui" / "brands" / f"{slug}.svg").read_text(encoding="utf-8").lstrip().startswith("<"))
                self.assertIn("brand-" + slug, self.KIT["brandClasses"])
                self.assertEqual(self.KIT["clients"][slug]["theme"], "light")
                self.assertNotIn("data-theme", css, "client brands are light only")
                self.assertNotIn(":root", css, "a client file sets variables on its own class only")
                self.assertIn("--display", variables)
                self.assertIn("--body", variables)
                self.assertIn('font-feature-settings: "locl" on, "kern" on;', css)
                self.assertNotIn('"ss01" on', css, "ss01 picks Montserrat's alternate letters")

    def test_client_text_and_controls_meet_contrast(self):
        for slug in self.CLIENTS:
            with self.subTest(client=slug):
                _, v = self._client_vars(slug)
                action = v.get("--action", v.get("--ink"))
                self.assertGreaterEqual(contrast_ratio(v.get("--action-ink", "#ffffff"), action), 4.5)
                self.assertGreaterEqual(contrast_ratio(v["--ink"], "#ffffff"), 4.5)
                self.assertGreaterEqual(contrast_ratio(v.get("--focus", v["--signal"]), "#ffffff"), 3.0)
                self.assertGreaterEqual(contrast_ratio(v.get("--signal-text", v["--signal"]), "#ffffff"), 3.0)

    def test_house_brands_keep_the_black_button_and_red_ring(self):
        css = (ROOT / "ui" / "agustos.css").read_text(encoding="utf-8")
        for name in ("--action", "--action-ink", "--action-hover", "--focus", "--signal-text"):
            with self.subTest(variable=name):
                self.assertNotRegex(css, rf"(?m)^\s*{name}:", "the kit reads it with a fallback and never sets it")


if __name__ == "__main__":
    unittest.main()
