from __future__ import annotations

import json
import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = ROOT / "adapters"
RETIRED_CLASSES = re.compile(
    r"\b(site-footer__(?:cols|col|col-heading|list|cta)|hero-links?|hero-link--(?:primary|secondary)"
    r"|hero-action|hero-action--(?:primary|secondary))(?![\w-])"
)


def adapter_sources():
    """Hand-written adapter files: components, layouts, partials, examples, previews, docs.
    Generated CSS and theme.json come from the build and are checked there. The
    adapters' own tests name retired classes to assert their absence, so they are left out."""
    generated = {
        ADAPTERS / "astro" / "src" / "styles" / "tokens.css",
        ADAPTERS / "rails" / "app" / "assets" / "stylesheets" / "agustos" / "tokens.css",
        ADAPTERS / "wordpress" / "assets" / "css" / "agustos.css",
        ADAPTERS / "wordpress" / "theme.json",
    }
    suffixes = {".astro", ".ts", ".mjs", ".erb", ".rb", ".html", ".css", ".js", ".md", ".example"}
    for path in sorted(ADAPTERS.rglob("*")):
        if {"node_modules", "dist", "test", "tests"} & set(path.parts) or path in generated:
            continue
        if path.is_file() and path.suffix in suffixes:
            yield path, path.read_text(encoding="utf-8")


class AdapterContractTest(unittest.TestCase):
    def test_generated_css_adapters_share_v3_primitives(self):
        paths = [
            ROOT / "tokens" / "agustos.css",
            ROOT / "adapters" / "astro" / "src" / "styles" / "tokens.css",
            ROOT / "adapters" / "rails" / "app" / "assets" / "stylesheets" / "agustos" / "tokens.css",
            ROOT / "adapters" / "wordpress" / "assets" / "css" / "agustos.css",
        ]
        required = (
            "--measure-content: 1180px",
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
        self.assertIn("aria-current={currentState(item.href, pathname)}", header)
        self.assertIn('class="site-header__bar site-frame"', header)
        self.assertIn("config.theme === true", header)
        self.assertIn("agustos-button agustos-button--primary site-header__cta", header)
        self.assertIn('class="site-header__panel" popover', header)
        self.assertIn('popovertarget="site-header-panel"', header)
        self.assertNotIn("nav-backdrop", header)
        self.assertNotIn("data-nav-open", header)
        for selector in (
            ".site-header {", ".site-header__bar {", ".site-header__nav {", ".site-header__link {",
            ".site-header__end {", ".site-header__cta {", ".site-header__burger {", ".site-header__panel {",
        ):
            self.assertNotIn(selector, header, selector)

    def test_astro_footer_has_no_chrome_styles(self):
        footer = (ROOT / "adapters" / "astro" / "src" / "components" / "Footer.astro").read_text(encoding="utf-8")
        self.assertIn('<footer class="site-footer">', footer)
        self.assertIn('class="site-footer__inner site-frame"', footer)
        self.assertNotIn("<style>", footer)
        self.assertIn('class="site-lockup"', footer)
        self.assertNotIn("BrandLockup", footer)
        # v7: the footer lockup simply uses the brand ink; the kit no longer
        # special-cases it. The footer is one note and one row of links.
        self.assertIn('<div class="site-footer__brand">', footer)
        self.assertIn('<p class="type-footnote">{note}</p>', footer)
        self.assertIn('<ul class="site-footer__links">', footer)
        self.assertIn('class="site-footer__link"', footer)
        self.assertNotIn("agustos-button", footer, "the footer holds no button")

    def test_footer_offers_the_optional_site_map(self):
        """Emre, 2026-09-30: an address block and at most three short groups
        above the bottom row. The config key is groups, never columns."""
        types = (ADAPTERS / "astro" / "src" / "types" / "chrome.ts").read_text(encoding="utf-8")
        self.assertIn("address?: string[];", types)
        self.assertIn("groups?: FooterGroup[];", types)
        self.assertIn("contact?: ChromeLink[];", types)
        helper = (ADAPTERS / "rails" / "app" / "helpers" / "agustos_theme_helper.rb").read_text(encoding="utf-8")
        self.assertIn("def agustos_footer_groups", helper)
        self.assertIn("def agustos_footer_address", helper)
        self.assertIn("def agustos_footer_contact", helper)
        for footer in (
            (ADAPTERS / "astro" / "src" / "components" / "Footer.astro").read_text(encoding="utf-8"),
            (ADAPTERS / "rails" / "app" / "views" / "agustos" / "shared" / "_footer.html.erb").read_text(encoding="utf-8"),
        ):
            order = [footer.find(marker) for marker in (
                '<div class="site-footer__map site-frame">', '<div class="site-footer__contact">', "<address>",
                '<nav class="site-footer__groups"', '<h2 class="site-footer__group-title">',
                '<ul class="site-footer__group-links">', '<div class="site-footer__inner site-frame">',
            )]
            self.assertNotIn(-1, order)
            self.assertEqual(order, sorted(order))

    def test_footer_is_one_note_and_one_row_of_links(self):
        types = (ADAPTERS / "astro" / "src" / "types" / "chrome.ts").read_text(encoding="utf-8")
        self.assertIn("note?: string;", types)
        self.assertIn("links?: ChromeLink[];", types)
        self.assertNotIn("FooterColumn", types)
        self.assertNotIn("columns", types)
        helper = (ADAPTERS / "rails" / "app" / "helpers" / "agustos_theme_helper.rb").read_text(encoding="utf-8")
        self.assertIn("def agustos_footer_note", helper)
        self.assertIn("def agustos_footer_links", helper)
        self.assertNotIn("columns", helper)
        self.assertNotIn("footer_cta", helper)
        for footer in (
            (ADAPTERS / "astro" / "src" / "components" / "Footer.astro").read_text(encoding="utf-8"),
            (ADAPTERS / "rails" / "app" / "views" / "agustos" / "shared" / "_footer.html.erb").read_text(encoding="utf-8"),
        ):
            # The bottom row, read from its own start: the optional site map above it also holds links.
            self.assertLess(footer.find('<footer class="site-footer">'), footer.find('<div class="site-footer__inner site-frame">'))
            row = footer[footer.find('<div class="site-footer__inner site-frame">'):]
            order = [row.find(marker) for marker in (
                '<div class="site-footer__inner site-frame">',
                '<div class="site-footer__brand">', 'class="type-footnote"', "<nav aria-label=",
                '<ul class="site-footer__links">', "site-footer__link",
            )]
            self.assertNotIn(-1, order)
            self.assertEqual(order, sorted(order))

    def test_top_menu_moves_items_beyond_five_under_more(self):
        types = (ADAPTERS / "astro" / "src" / "types" / "chrome.ts").read_text(encoding="utf-8")
        self.assertIn("export const NAV_LIMIT = 5;", types)
        self.assertIn("items.slice(0, NAV_LIMIT - 1), items.slice(NAV_LIMIT - 1)", types)
        self.assertIn("more: 'Daha fazla'", types)
        self.assertIn("more: 'More'", types)
        helper = (ADAPTERS / "rails" / "app" / "helpers" / "agustos_theme_helper.rb").read_text(encoding="utf-8")
        self.assertIn("NAV_LIMIT = 5", helper)
        self.assertIn("[items.first(NAV_LIMIT - 1), items.drop(NAV_LIMIT - 1)]", helper)
        self.assertIn('more: "Daha fazla"', helper)
        for header in (
            (ADAPTERS / "astro" / "src" / "components" / "Header.astro").read_text(encoding="utf-8"),
            (ADAPTERS / "rails" / "app" / "views" / "agustos" / "shared" / "_header.html.erb").read_text(encoding="utf-8"),
        ):
            nav = header[header.index('<nav class="site-header__nav"'):header.index("</nav>")]
            more = nav.index('<details class="site-header__more">')
            self.assertLess(nav.index("site-header__link"), more)
            self.assertRegex(nav[more:], r'<summary class="site-header__link">.+?</summary>\s*<div class="site-header__more-menu">')
            self.assertIn("site-header__more-link", nav[more:])
            self.assertTrue(nav.rstrip().endswith("</details>") or nav.rstrip().endswith(")}") or nav.rstrip().endswith("<% end %>"),
                            "More is the last child of site-header__nav")
        preview = (ADAPTERS / "rails" / "preview" / "marketing.html").read_text(encoding="utf-8")
        nav = preview[preview.index('<nav class="site-header__nav"'):preview.index("</nav>")]
        self.assertEqual(nav.count('class="site-header__link"'), 5, "four links plus the More summary")
        self.assertTrue(nav.rstrip().endswith("</details>"))

    def test_adapters_use_no_retired_v6_classes(self):
        for path, text in adapter_sources():
            if path.suffix == ".md":
                continue  # the READMEs name the retired classes to explain the migration
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsNone(RETIRED_CLASSES.search(text))

    def test_chrome_follows_the_screen_family_not_the_brand(self):
        for path, text in adapter_sources():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotRegex(text, r"BRAND_CHROME|brandChrome|chrome_for_brand|chromeForBrand|brands\.json")
                if "site-sidebar" in text and path.suffix in {".astro", ".html", ".erb"}:
                    rel = path.relative_to(ADAPTERS).as_posix()
                    self.assertIn(rel, {
                        "rails/app/views/agustos/shared/_sidebar.html.erb",
                        "rails/preview/product-ui.html",
                        "rails/app/views/agustos/examples/product.html.erb",
                        "rails/app/views/layouts/agustos.html.erb",
                    }, "only product UI renders the sidebar")

    def test_examples_use_kit_hero_buttons_and_one_highlighter(self):
        for rel in (
            "astro/src/pages/index.astro",
            "rails/app/views/agustos/examples/show.html.erb",
            "rails/preview/marketing.html",
        ):
            page = (ADAPTERS / rel).read_text(encoding="utf-8")
            with self.subTest(page=rel):
                self.assertEqual(page.count('<mark class="type-highlight">'), 1)
                self.assertRegex(page, r'<h1[^>]*class="type-hero"[^>]*>[^<]*<mark class="type-highlight">(\S+(?: \S+){0,3})</mark>')
                actions = page[page.index('<div class="hero-actions">'):]
                actions = actions[:actions.index("</div>")]
                self.assertEqual(actions.count("agustos-button agustos-button--primary"), 1)
                self.assertEqual(actions.count("agustos-button agustos-button--secondary"), 1)
                self.assertIn("band band--cream", page)

    def test_astro_layout_has_no_legacy_sidebar_contract(self):
        layout = (ROOT / "adapters" / "astro" / "src" / "layouts" / "BaseLayout.astro").read_text(encoding="utf-8")
        self.assertIn("<Header", layout)
        self.assertIn("<Footer", layout)
        self.assertNotIn("Sidebar", layout)
        self.assertNotIn("MobileHeader", layout)

    def test_rails_helper_defaults_to_white_and_preserves_brand_fallbacks(self):
        helper = (ROOT / "adapters" / "rails" / "app" / "helpers" / "agustos_theme_helper.rb").read_text(encoding="utf-8")
        self.assertIn("substrate: :white", helper)
        self.assertIn("shell: :marketing", helper)
        self.assertIn("theme: false", helper)
        self.assertNotIn("color_scheme", helper)
        self.assertIn('classes << "paper-white" if config[:substrate] == :white', helper)
        self.assertIn("BRAND_CLASSES.fetch(config[:brand], BRAND_CLASSES[:agustos])", helper)
        self.assertIn("BRAND_WORDMARKS.fetch(agustos_theme_config[:brand], BRAND_WORDMARKS[:agustos])", helper)

    def test_rails_layout_uses_kit_chrome_without_a_nav_controller(self):
        layout = (ROOT / "adapters" / "rails" / "app" / "views" / "layouts" / "agustos.html.erb").read_text(encoding="utf-8")
        header = (ROOT / "adapters" / "rails" / "app" / "views" / "agustos" / "shared" / "_header.html.erb").read_text(encoding="utf-8")
        footer = (ROOT / "adapters" / "rails" / "app" / "views" / "agustos" / "shared" / "_footer.html.erb").read_text(encoding="utf-8")
        helper = (ROOT / "adapters" / "rails" / "app" / "helpers" / "agustos_theme_helper.rb").read_text(encoding="utf-8")
        self.assertIn("agustos/shared/header", layout)
        product_branch, website_branch = layout.split("<% else %>", 1)
        self.assertIn("agustos_product_shell?", product_branch)
        self.assertIn("agustos/shared/sidebar", product_branch)
        self.assertNotIn("sidebar", website_branch, "websites never render the sidebar")
        self.assertIn('classes << (agustos_product_shell? ? "site-sidebar-layout" : "agustos-layout")', helper)
        self.assertNotIn("agustos-nav", layout)
        self.assertNotIn("agustos-nav", helper)
        self.assertIn("agustos_theme_toggle?", layout)
        self.assertRegex(layout, r'<body\s+data-screen="<%= agustos_screen %>"')
        self.assertIn('<header class="site-header">', header)
        self.assertIn("agustos-button agustos-button--primary site-header__cta", header)
        self.assertIn('popovertarget="site-header-panel"', header)
        self.assertNotIn("agustos-header", header)
        self.assertNotIn("agustos-nav-backdrop", header)
        self.assertIn('<footer class="site-footer">', footer)
        self.assertNotIn("agustos-footer", footer)
        self.assertFalse((ROOT / "adapters" / "rails" / "app" / "javascript" / "controllers" / "agustos_nav_controller.js").exists())

    def test_rails_product_ui_uses_the_kit_sidebar(self):
        page = (ROOT / "adapters" / "rails" / "app" / "views" / "agustos" / "examples" / "product.html.erb").read_text(encoding="utf-8")
        preview = (ROOT / "adapters" / "rails" / "preview" / "product-ui.html").read_text(encoding="utf-8")
        sidebar = (ROOT / "adapters" / "rails" / "app" / "views" / "agustos" / "shared" / "_sidebar.html.erb").read_text(encoding="utf-8")
        self.assertIn("shell: :product", page)
        self.assertIn("screen: :app_shell", page)
        self.assertIn("Validation run", page)
        self.assertIn("Export dataset", page)
        self.assertNotIn("pq-", page)
        for name in ("site-sidebar-bar", "site-sidebar-burger", 'class="site-sidebar"', "site-sidebar__nav",
                     "site-sidebar__link", "site-sidebar__utility", "site-sidebar__note"):
            self.assertIn(name, sidebar)
            self.assertIn(name, preview)
        self.assertIn('class="brand-iesdesk paper-white site-sidebar-layout"', preview)
        self.assertIn('data-screen="app-shell"', preview)
        self.assertIn("Validation run", preview)
        self.assertNotIn('data-theme="dark"', preview)
        self.assertNotIn("pq-", preview)
        self.assertNotIn("site-header", preview)
        self.assertFalse((ROOT / "adapters" / "rails" / "app" / "assets" / "stylesheets" / "agustos" / "product.css").exists())

    def test_adapters_use_the_kit_theme_switch_and_one_handler(self):
        """v7.7.0: agustos-chrome.js is the one theme handler. A second handler on the
        same button would flip the theme twice per click."""
        script = 'try{if(localStorage.getItem("agustos:theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}'
        astro_utility = (ROOT / "adapters/astro/src/components/HeaderUtility.astro").read_text(encoding="utf-8")
        astro_header = (ROOT / "adapters/astro/src/components/Header.astro").read_text(encoding="utf-8")
        astro_layout = (ROOT / "adapters/astro/src/layouts/BaseLayout.astro").read_text(encoding="utf-8")
        rails_utility = (ROOT / "adapters/rails/app/views/agustos/shared/_header_utility.html.erb").read_text(encoding="utf-8")
        rails_layout = (ROOT / "adapters/rails/app/views/layouts/agustos.html.erb").read_text(encoding="utf-8")
        rails_helper = (ROOT / "adapters/rails/app/helpers/agustos_theme_helper.rb").read_text(encoding="utf-8")
        for name, text in (("astro utility", astro_utility), ("rails utility", rails_utility)):
            with self.subTest(file=name):
                self.assertIn("agustos-theme-switch", text)
                self.assertIn("data-agustos-theme", text)
                self.assertNotIn("data-theme-toggle", text)
                self.assertNotIn("agustos-theme#toggle", text)
        self.assertNotIn("data-theme-toggle", astro_header)
        self.assertIn(script, astro_layout)
        self.assertIn(script, rails_helper)
        self.assertIn("javascript_tag AgustosThemeHelper::THEME_SCRIPT, nonce: true", rails_layout)
        self.assertFalse((ROOT / "adapters/rails/app/javascript/controllers/agustos_theme_controller.js").exists())

    def test_adapters_never_render_a_page_dark_on_the_server(self):
        """v7.7.0: every page starts light. Only the theme switch sets data-theme."""
        astro_layout = (ROOT / "adapters/astro/src/layouts/BaseLayout.astro").read_text(encoding="utf-8")
        typography = (ROOT / "adapters/astro/src/pages/typography.astro").read_text(encoding="utf-8")
        rails_layout = (ROOT / "adapters/rails/app/views/layouts/agustos.html.erb").read_text(encoding="utf-8")
        rails_helper = (ROOT / "adapters/rails/app/helpers/agustos_theme_helper.rb").read_text(encoding="utf-8")
        rails_sidebar = (ROOT / "adapters/rails/app/views/agustos/shared/_sidebar.html.erb").read_text(encoding="utf-8")
        preview = (ROOT / "adapters/rails/preview/product-ui.html").read_text(encoding="utf-8")
        self.assertNotIn("data-theme={", astro_layout)
        self.assertNotIn("theme?: 'light' | 'dark'", astro_layout)
        self.assertNotIn("theme-inspect", typography)
        self.assertNotIn("dataset.theme", typography)
        self.assertNotIn("data-theme", rails_layout)
        self.assertNotIn("color_scheme", rails_helper)
        self.assertNotIn("agustos_dark?", rails_helper + rails_layout + rails_sidebar)
        for name, text in (("rails sidebar", rails_sidebar), ("rails preview", preview)):
            with self.subTest(file=name):
                self.assertIn("agustos-button agustos-button--quiet agustos-theme-switch", text)
                self.assertIn("data-agustos-theme", text)
        self.assertNotIn('id="theme"', preview)
        self.assertNotIn('setAttribute("data-theme"', preview.split("</head>", 1)[1])

    def test_rails_lockup_contains_exact_eighteen_blades(self):
        lockup = (ROOT / "adapters" / "rails" / "app" / "views" / "agustos" / "shared" / "_brand_lockup.html.erb").read_text(encoding="utf-8")
        self.assertEqual(lockup.count("<path"), 18)
        self.assertIn("agustos_wordmark", lockup)
        self.assertIn("site-lockup", lockup)
        self.assertNotIn("agustos-lockup", lockup)

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
        self.assertEqual(theme["settings"]["layout"], {"contentSize": "1180px", "wideSize": "1180px"})

    def test_local_gate_enforces_web_office_and_unit_contracts(self):
        gate = (ROOT / "scripts" / "ci.sh").read_text(encoding="utf-8")
        steps = (
            "scripts/build_design_system.py --check",
            "scripts/check_office_artifacts.py --check",
            "-m unittest discover -s tests",
        )
        for step in steps:
            self.assertIn(step, gate)
        positions = [gate.find(step) for step in steps]
        self.assertEqual(positions, sorted(positions), "scripts/ci.sh must run its steps in this order")
        hook = (ROOT / ".githooks" / "pre-push").read_text(encoding="utf-8")
        self.assertRegex(hook, r"(?m)^\s*(?:if\s+!?\s*)?scripts/ci\.sh\b", "the pre-push hook must run scripts/ci.sh")

    def test_single_file_handoff_contains_tokens_rules_and_brand_registry(self):
        handoff = json.loads((ROOT / "tokens" / "design-system-handoff.json").read_text(encoding="utf-8"))
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(handoff["version"], version)
        self.assertEqual(handoff["system"]["brands"]["agustos"]["color"], "#cf142a")
        self.assertEqual(handoff["system"]["brands"]["pataraz"]["color"], "#15130f")
        self.assertEqual(handoff["system"]["brands"]["pld"]["color"], "#15130f")
        self.assertEqual(handoff["system"]["brands"]["iesdesk"]["color"], "#15130f")
        self.assertEqual(handoff["system"]["brands"]["specquick"]["color"], "#15130f")
        self.assertEqual(handoff["system"]["semantic"]["color"]["signal"], "#cf142a")
        self.assertEqual(handoff["system"]["recipes"]["chrome"]["contentMeasure"], "1180px")
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
            "pataraz": "#15130f",
            "pld": "#15130f",
            "iesdesk": "#15130f",
            "specquick": "#15130f",
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

    def test_brand_favicons_are_a_white_tile_with_the_identity_ink_symbol(self):
        """MEMORY.md 2026-09-29 per-brand-favicons: red sun for Ağustos, #15130f for the rest."""
        registry = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        white = registry["substrate"]["paper_white"].lower()
        master = (ROOT / "laz-gunesi-amblem" / "svg" / "master.svg").read_text(encoding="utf-8")
        paths = re.findall(r'<path[^>]*\bd="([^"]+)"', master)
        self.assertEqual(len(paths), 18)
        for slug, brand in registry["brands"].items():
            folder = ROOT / "brand" / "exports" / slug / "favicon"
            if not folder.is_dir():
                continue
            ink = brand["color"].lower()
            svg = (folder / "favicon.svg").read_text(encoding="utf-8").lower()
            manifest = json.loads((folder / "site.webmanifest").read_text(encoding="utf-8"))
            with self.subTest(slug=slug):
                self.assertEqual(ink, "#cf142a" if slug == "agustos" else "#15130f")
                self.assertRegex(svg, rf'<rect [^>]*fill="{white}"')
                self.assertIn(f'<g fill="{ink}"', svg)
                self.assertEqual(set(re.findall(r'fill="(#[0-9a-f]{6})"', svg)), {white, ink})
                for d in paths:
                    self.assertIn(f'd="{d.lower()}"', svg)
                self.assertEqual(manifest["theme_color"].lower(), ink)
                self.assertEqual(manifest["background_color"].lower(), white)
                for name in ("favicon.ico", "apple-touch-icon.png", "favicon-16.png", "favicon-192.png", "favicon-512.png"):
                    self.assertTrue((folder / name).is_file(), name)
        canonical = ROOT / "laz-gunesi-amblem" / "favicon" / "favicon.svg"
        self.assertEqual(
            canonical.read_bytes(),
            (ROOT / "brand" / "exports" / "agustos" / "favicon" / "favicon.svg").read_bytes(),
            "the canonical favicon is the Ağustos favicon",
        )


if __name__ == "__main__":
    unittest.main()
