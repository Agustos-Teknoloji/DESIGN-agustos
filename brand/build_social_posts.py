#!/usr/bin/env python3
"""
Ağustos brand kit: LinkedIn post templates, one image per idea.

Writes exports/<brand>/social/<post-key>-portrait.html and -square.html from brands.json
and tokens/resolved.json. With --png it also renders each page to a PNG at the exact canvas
size through the gstack browse tool. A post must read as the same brand as the website and
the datasheet, so every size, colour and face comes from the registry:

  recipes.social        canvas sizes, scale, margin, the type roles and the lockup height
  typeRoles             size, weight, line height and tracking of each role
  foundations           colours, font families and spacing

Text size on a post is the largest px value of the role times recipes.social.scale.
The house rules hold: white paper, ink text, a deck in inkSoft, sentence case, no capitals,
no label above the headline, no red text and no red fills. The only red is the Ağustos logo
and at most one highlighter stroke behind one to four words of the headline.

Run after build.py (it reuses the generated positive lockup).

  python3 brand/build_social_posts.py [--brand <slug>] [--post <key>] [--png]
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

BRAND_DIR = Path(__file__).resolve().parent
ROOT = BRAND_DIR.parent
REGISTRY = BRAND_DIR / "brands.json"
TOKENS = ROOT / "tokens" / "resolved.json"
FONTS = BRAND_DIR / "fonts"
EXPORTS = BRAND_DIR / "exports"
BROWSE = Path.home() / ".claude/skills/gstack/browse/dist/browse"

FORMATS = ("portrait", "square")
# recipes.social names no role for the spec labels. The web product page and the
# datasheet set labels in the display face at a small group-title size, which is h4.
LABEL_ROLE = "h4"
MAX_SPECS = 4
MAX_HIGHLIGHT_WORDS = 4

# ----------------------------------------------------------------------------
# Post data: THE place to edit. A flat registry keyed by post. Each entry names its
# `brand` (the slug in brands.json), and the key starts with that slug.
#
#   headline   one idea, sentence case, no capitals. It is set in the h1 role.
#   highlight  optional. One to four words that are a substring of the headline.
#              The builder draws one marker stroke behind them. Use it at most once.
#   deck       one short line under the headline, in inkSoft.
#   specs      optional. Up to four (label, value) pairs. Put the unit in the value.
#   lang       optional. The page language. The default is "tr".
#
# Every entry gives two images: <key>-portrait (1080x1350) and <key>-square (1200x1200).
# ----------------------------------------------------------------------------

POSTS = {
    # The same product, data and wording as screens/product.html and the PX22 datasheet.
    "pataraz-px22": {
        "brand": "pataraz",
        "headline": "Penceresiz odaya gün ışığı.",
        "highlight": "gün ışığı",
        "deck": "PX22 · ultra ince duvar penceresi",
        "specs": [
            ("Güç", "160 W"),
            ("Işık çıkışı", "4200 lm"),
            ("Renk sıcaklığı", "2100–7500 K"),
        ],
    },
    # A company line for the parent brand. It has no spec row.
    "agustos-company": {
        "brand": "agustos",
        "headline": "Her proje için doğru ışık.",
        "highlight": "doğru ışık",
        "deck": "Ağustos Teknoloji, mimari aydınlatma ürünlerini ve yazılımlarını tek çatı altında sunar.",
    },
    # An editorial line for PLD Türkiye. It has no highlight and no spec row.
    "pld-editorial": {
        "brand": "pld",
        "headline": "İyi ışık fark edilmez, hissedilir.",
        "deck": "PLD Türkiye · aydınlatma tasarımı üzerine yazılar",
    },
}

_KEY_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def px(size: str) -> float:
    """The largest pixel value of a registry size, so clamp(43px, 4.6vw, 55px) reads 55."""
    values = [float(v) for v in re.findall(r"([0-9.]+)px", str(size))]
    if not values:
        raise SystemExit(f"registry size '{size}' has no px value")
    return max(values)


def fmt(value: float) -> str:
    """A CSS pixel length without a trailing .0."""
    return f"{value:g}px"


def validate_posts(reg: dict) -> None:
    """Stop on a malformed POSTS entry before any file is written."""
    brands = reg["brands"]
    for key, post in POSTS.items():
        if not _KEY_RE.match(key):
            raise SystemExit(f"post key '{key}' is not slug-safe")
        for field in ("brand", "headline", "deck"):
            if not post.get(field):
                raise SystemExit(f"post '{key}' has no '{field}'")
        slug = post["brand"]
        if slug not in brands:
            raise SystemExit(f"post '{key}' names unknown brand '{slug}'")
        if not key.startswith(f"{slug}-"):
            raise SystemExit(f"post key '{key}' must start with '{slug}-'")
        mark = post.get("highlight")
        if mark:
            if post["headline"].count(mark) != 1:
                raise SystemExit(f"post '{key}': the highlight must occur once in the headline")
            if not 1 <= len(mark.split()) <= MAX_HIGHLIGHT_WORDS:
                raise SystemExit(f"post '{key}': the highlight must be 1 to {MAX_HIGHLIGHT_WORDS} words")
        if len(post.get("specs", [])) > MAX_SPECS:
            raise SystemExit(f"post '{key}': {MAX_SPECS} spec values at most")


def headline_html(post: dict) -> str:
    """The headline, with one <mark> behind the highlight phrase when the post has one."""
    text, mark = post["headline"], post.get("highlight")
    if not mark:
        return html.escape(text)
    before, after = text.split(mark, 1)
    return f'{html.escape(before)}<mark>{html.escape(mark)}</mark>{html.escape(after)}'


def rel_url(target: Path, out_dir: Path) -> str:
    """A URL for target relative to out_dir, so the HTML works from any folder or machine."""
    return quote(Path(os.path.relpath(target.resolve(), out_dir.resolve())).as_posix())


def gen_post_html(key: str, post: dict, brand: dict, design: dict, fmt_name: str, out: Path,
                  lockup: Path) -> None:
    social = design["recipes"]["social"]
    scale = float(social["scale"])
    width, height = social[fmt_name]["width"], social[fmt_name]["height"]
    margin = px(social["margin"])
    colors = design["foundations"]["color"]
    families = design["foundations"]["fontFamily"]
    spacing = design["foundations"]["spacing"]
    signal = design["semantic"]["color"]["signal"]
    roles = {row["role"]: row for row in design["typeRoles"]}
    paper, ink, soft, rule = colors["paperWhite"], colors["ink"], colors["inkSoft"], colors["ruleCream"]
    hairline = max(1, round(px(design["foundations"]["border"]["hairline"]) * scale))

    def sp(name: str) -> str:
        """A registry space, scaled for the post canvas."""
        return fmt(px(spacing[name]) * scale)

    def role_css(name: str) -> str:
        """Face, weight, size, line height and tracking of one type role, scaled."""
        r = roles[name]
        tracking = f" letter-spacing:{r['tracking']};" if r.get("tracking") else ""
        return (f"font-family:'{families[r['family']]}'; font-weight:{r['weight']}; "
                f"font-size:{fmt(px(r['size']) * scale)}; line-height:{r['lineHeight']};{tracking}")

    headline = roles[social["headlineRole"]]
    deck_gap = fmt(px(headline.get("after", spacing["2xl"])) * scale)
    out_dir = out.parent
    f_display = rel_url(FONTS / "inter-tight" / "InterTight[wght].ttf", out_dir)
    f_body = rel_url(FONTS / "inter" / "Inter[opsz,wght].ttf", out_dir)
    f_mono = rel_url(FONTS / "jetbrains-mono" / "JetBrainsMono[wght].ttf", out_dir)

    specs = post.get("specs", [])
    specs_html = ""
    if specs:
        items = "".join(
            f'<div><dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd></div>'
            for label, value in specs
        )
        specs_html = f'<dl class="specs" style="grid-template-columns:repeat({len(specs)},auto);">{items}</dl>'

    lang = post.get("lang", "tr")
    doc = f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width={width}">
<title>{html.escape(brand['title'])} · {html.escape(key)} · {fmt_name}</title>
<!-- Generated by brand/build_social_posts.py. Edit POSTS in that script, then run it again. -->
<style>
@font-face {{ font-family:'{families['display']}'; src:url('{f_display}'); font-weight:100 900; }}
@font-face {{ font-family:'{families['body']}'; src:url('{f_body}'); font-weight:100 900; }}
@font-face {{ font-family:'{families['mono']}'; src:url('{f_mono}'); font-weight:100 900; }}
* {{ box-sizing:border-box; }}
html, body {{ margin:0; background:{paper}; }}
.post {{ width:{width}px; height:{height}px; padding:{fmt(margin)}; overflow:hidden;
         display:flex; flex-direction:column; background:{paper}; color:{ink}; }}
.text {{ flex:1; }}
.headline {{ {role_css(social["headlineRole"])} color:{ink}; margin:0; }}
.deck {{ {role_css(social["deckRole"])} color:{soft}; margin:{deck_gap} 0 0; }}
/* The kit highlighter (mark.type-highlight in tokens/web.css.tmpl): signal red at low
   strength behind the words. The text stays ink. */
mark {{
  color:inherit;
  padding:0 0.06em;
  margin:0 -0.02em;
  border-radius:0.12em 0.3em 0.16em 0.35em;
  background:
    linear-gradient(100deg,
      color-mix(in srgb, {signal} 0%, transparent) 0%,
      color-mix(in srgb, {signal} 20%, transparent) 1.5%,
      color-mix(in srgb, {signal} 15%, transparent) 50%,
      color-mix(in srgb, {signal} 19%, transparent) 97%,
      color-mix(in srgb, {signal} 0%, transparent) 100%)
    0 62% / 100% 52% no-repeat;
  -webkit-box-decoration-break:clone;
  box-decoration-break:clone;
}}
.specs {{ display:grid; justify-content:start; column-gap:{sp("5xl")}; margin:0;
          padding-top:{sp("xl")}; border-top:{hairline}px solid {rule}; }}
.specs dt {{ {role_css(LABEL_ROLE)} color:{soft}; }}
.specs dd {{ {role_css(social["dataRole"])} color:{ink}; margin:{sp("xs")} 0 0; white-space:nowrap; }}
.foot {{ margin-top:{sp("4xl")}; }}
.foot img {{ display:block; height:{social["lockupHeight"]}; width:auto; }}
</style></head><body>
<div class="post">
  <div class="text">
    <h1 class="headline">{headline_html(post)}</h1>
    <p class="deck">{html.escape(post["deck"])}</p>
  </div>
  {specs_html}
  <div class="foot"><img src="{rel_url(lockup, out_dir)}" alt="{html.escape(brand['wordmark'])}"></div>
</div>
</body></html>
"""
    out.write_text(doc, encoding="utf-8")


def render_png(page: Path, png: Path, width: int, height: int) -> None:
    """Render the page at the exact canvas size. The page waits for its fonts first."""
    if not BROWSE.exists():
        raise SystemExit(f"browse tool not found at {BROWSE}; cannot render {png.name}")
    run = lambda *args: subprocess.run([str(BROWSE), *args], check=True, capture_output=True)
    run("viewport", f"{width}x{height}")
    run("goto", page.resolve().as_uri())
    run("js", "document.fonts.ready.then(() => document.fonts.size)")
    run("screenshot", "--viewport", str(png))
    print(f"    rendered {png.relative_to(ROOT) if png.is_relative_to(ROOT) else png}")


def build_post(key: str, post: dict, reg: dict, design: dict, want_png: bool = False,
               out_root: Path = EXPORTS) -> list[Path]:
    slug = post["brand"]
    lockup = EXPORTS / slug / "lockup" / f"{slug}-lockup__positive.svg"
    if not lockup.exists():
        raise SystemExit(f"missing {lockup}; run build.py --brand {slug} first")
    out_dir = out_root / slug / "social"
    out_dir.mkdir(parents=True, exist_ok=True)
    pages = []
    for fmt_name in FORMATS:
        out = out_dir / f"{key}-{fmt_name}.html"
        gen_post_html(key, post, reg["brands"][slug], design, fmt_name, out, lockup)
        print(f"    wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
        if want_png:
            size = design["recipes"]["social"][fmt_name]
            render_png(out, out.with_suffix(".png"), size["width"], size["height"])
        pages.append(out)
    return pages


def main() -> None:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    design = json.loads(TOKENS.read_text(encoding="utf-8"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", help="all posts of one brand slug")
    ap.add_argument("--post", help="one post key, for example pataraz-px22")
    ap.add_argument("--png", action="store_true", help="also render the PNGs through browse")
    args = ap.parse_args()
    if args.brand and args.post:
        raise SystemExit("use --brand or --post, not both")
    validate_posts(reg)
    if args.post:
        if args.post not in POSTS:
            raise SystemExit(f"unknown post '{args.post}'; choices: {', '.join(POSTS)}")
        targets = {args.post: POSTS[args.post]}
    elif args.brand:
        if args.brand not in reg["brands"]:
            raise SystemExit(f"unknown brand '{args.brand}'")
        targets = {k: v for k, v in POSTS.items() if v["brand"] == args.brand}
        if not targets:
            raise SystemExit(f"no post for '{args.brand}'; add one to POSTS")
    else:
        targets = POSTS
    for key, post in targets.items():
        build_post(key, post, reg, design, args.png)


if __name__ == "__main__":
    main()
