from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "brand" / "build_social_posts.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_social_posts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def rule(page: str, selector: str) -> str:
    """The body of the first CSS rule for one selector."""
    match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", page)
    assert match, f"no CSS rule for {selector}"
    return match.group(1)


class SocialPostsContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_builder()
        cls.reg = json.loads((ROOT / "brand" / "brands.json").read_text(encoding="utf-8"))
        cls.design = json.loads((ROOT / "tokens" / "resolved.json").read_text(encoding="utf-8"))
        cls.social = cls.design["recipes"]["social"]
        cls.roles = {row["role"]: row for row in cls.design["typeRoles"]}
        cls.builder.validate_posts(cls.reg)
        cls.pages = {}
        with tempfile.TemporaryDirectory() as tmp:
            for key, post in cls.builder.POSTS.items():
                for path in cls.builder.build_post(key, post, cls.reg, cls.design, out_root=Path(tmp)):
                    cls.pages[path.stem] = path.read_text(encoding="utf-8")

    def scaled(self, role: str) -> str:
        return f"{self.builder.px(self.roles[role]['size']) * self.social['scale']:g}px"

    def test_one_sample_post_per_full_kit_brand(self):
        brands = sorted({post["brand"] for post in self.builder.POSTS.values()})
        self.assertEqual(brands, ["agustos", "pataraz", "pld"])
        self.assertEqual(len(self.pages), 2 * len(self.builder.POSTS))

    def test_pataraz_sample_is_the_px22(self):
        post = self.builder.POSTS["pataraz-px22"]
        self.assertIn("PX22", post["deck"])
        self.assertEqual(dict(post["specs"]), {
            "Güç": "160 W", "Işık çıkışı": "4200 lm", "Renk sıcaklığı": "2100–7500 K"})

    def test_canvas_matches_the_recipe(self):
        for name, page in self.pages.items():
            fmt = name.rsplit("-", 1)[1]
            size = self.social[fmt]
            with self.subTest(page=name):
                body = rule(page, ".post")
                self.assertIn(f"width:{size['width']}px", body)
                self.assertIn(f"height:{size['height']}px", body)
                self.assertIn(f"padding:{self.social['margin']}", body)
                self.assertIn(f"height:{self.social['lockupHeight']}", rule(page, ".foot img"))

    def test_text_sizes_are_the_role_size_times_the_scale(self):
        for name, page in self.pages.items():
            with self.subTest(page=name):
                headline = rule(page, ".headline")
                self.assertIn(f"font-size:{self.scaled(self.social['headlineRole'])}", headline)
                self.assertIn(f"font-weight:{self.roles[self.social['headlineRole']]['weight']}", headline)
                self.assertIn(f"letter-spacing:{self.roles[self.social['headlineRole']]['tracking']}", headline)
                self.assertIn(f"font-size:{self.scaled(self.social['deckRole'])}", rule(page, ".deck"))
                self.assertIn(f"font-size:{self.scaled(self.social['dataRole'])}", rule(page, ".specs dd"))
                self.assertIn("font-family:'JetBrains Mono'", rule(page, ".specs dd"))
                self.assertIn("font-family:'Inter Tight'", rule(page, ".specs dt"))

    def test_house_rules(self):
        for name, page in self.pages.items():
            with self.subTest(page=name):
                self.assertIn('<html lang="tr">', page)
                self.assertNotIn("uppercase", page)
                self.assertNotIn("—", page, "no em dash")
                self.assertNotRegex(page, r"font-weight:\s*650", "650 is the wordmark weight, never text")
                self.assertLessEqual(page.count("<mark"), 1, "one highlighter stroke at most")
                self.assertNotIn("<img", page.split('<div class="foot">')[0], "text never on a photograph")

    def test_red_is_only_the_logo_and_the_highlighter(self):
        signal = self.design["semantic"]["color"]["signal"].lower()
        for name, page in self.pages.items():
            with self.subTest(page=name):
                styles = page.split("<style>")[1].split("</style>")[0].lower()
                # Every use of the signal colour sits inside a color-mix of the mark rule.
                self.assertEqual(styles.count(signal), styles.count(f"color-mix(in srgb, {signal}"))
                self.assertEqual(styles.count(signal), 5)

    def test_highlight_is_inside_the_headline(self):
        for key, post in self.builder.POSTS.items():
            page = self.pages[f"{key}-portrait"]
            headline = re.search(r'<h1 class="headline">(.*?)</h1>', page).group(1)
            with self.subTest(post=key):
                if post.get("highlight"):
                    self.assertIn(f"<mark>{post['highlight']}</mark>", headline)
                    self.assertLessEqual(len(post["highlight"].split()), 4)
                else:
                    self.assertNotIn("<mark", page)

    def test_colours_come_from_the_registry(self):
        allowed = {v.lower() for v in self.design["foundations"]["color"].values()}
        allowed.add(self.design["semantic"]["color"]["signal"].lower())
        for name, page in self.pages.items():
            with self.subTest(page=name):
                used = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}\b", page)}
                self.assertEqual(used - allowed, set())
                self.assertNotRegex(page, r"rgba?\(|hsla?\(")

    def test_bad_posts_stop_the_build(self):
        for bad in (
            {"brand": "pataraz", "headline": "Bir fikir.", "deck": "x", "highlight": "iki fikir"},
            {"brand": "pataraz", "headline": "Bir iki üç dört beş.", "deck": "x", "highlight": "Bir iki üç dört beş"},
            {"brand": "pataraz", "headline": "Bir fikir.", "deck": "x", "specs": [("a", "1")] * 5},
        ):
            with self.subTest(bad=bad):
                saved = dict(self.builder.POSTS)
                try:
                    self.builder.POSTS.clear()
                    self.builder.POSTS["pataraz-bad"] = bad
                    with self.assertRaises(SystemExit):
                        self.builder.validate_posts(self.reg)
                finally:
                    self.builder.POSTS.clear()
                    self.builder.POSTS.update(saved)


if __name__ == "__main__":
    unittest.main()
