#!/usr/bin/env python3
"""
Ağustos brand kit: brand guidelines (A4 PDF, 13 pages, English).

Writes exports/<brand>/guidelines/<brand>-brand-guidelines.html from brands.json and
tokens/resolved.json. With --pdf it also renders the PDF through the gstack browse tool.
Every value comes from the registry; the page states nothing the system does not record.

Run after build.py (it reuses the generated lockups).

  python3 brand/build_guidelines.py [--brand <slug>] [--pdf]
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import subprocess
from pathlib import Path

BRAND_DIR = Path(__file__).resolve().parent
ROOT = BRAND_DIR.parent
REGISTRY = BRAND_DIR / "brands.json"
TOKENS = ROOT / "tokens" / "resolved.json"
SYMBOL = ROOT / "laz-gunesi-amblem" / "svg" / "master.svg"
BROWSE = Path.home() / ".claude/skills/gstack/browse/dist/browse"

# Page titles, in order. The cover and back cover have no title.
SECTIONS = [
    "Introduction",
    "In every medium",
    "The symbol",
    "The logo",
    "Clear space and minimum size",
    "Logo misuse",
    "Colour",
    "Colour in use",
    "Typography",
    "Emphasis",
    "Which file to use",
]


def hexrgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def tinted(path: Path, color: str) -> str:
    """The SVG as a data URI, with every fill set to one colour. The symbol and lockups use one fill."""
    svg = re.sub(r'fill="#[0-9a-fA-F]{3,6}"', f'fill="{color}"', path.read_text(encoding="utf-8"))
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def tr_upper(text: str) -> str:
    """Turkish capitals: the dotted i becomes İ, not I."""
    return text.replace("i", "İ").upper()


def six_colours(colors: dict, signal: str) -> list[tuple[str, str, str]]:
    """The locked six-colour palette: name, value, role."""
    return [
        ("White", colors["paperWhite"], "Paper for every page and screen."),
        ("Pale red", colors["paperCream"], "The one closing band of a page."),
        ("Light gray", colors["paperGray"], "Quiet surfaces, panels, and hover and pressed fills."),
        ("Dark gray", colors["inkSoft"], "Secondary text."),
        ("Off-black", colors["ink"], "Body text, headings and buttons."),
        ("Red", signal, "Identity and signal: the Ağustos logo, the 2px link rule, keyboard focus, one highlighter stroke. Never a button."),
    ]


def px(size: str) -> str:
    """The largest pixel value of a registry size, so clamp(43px, 4.6vw, 55px) reads 55px."""
    values = [float(v) for v in re.findall(r"([0-9.]+)px", size)]
    return f"{max(values):g}px"


def states_html(rows: list[dict]) -> str:
    """The registry states table: a swatch of each pair and its contrast ratio, light and dark."""

    def cell(pair: dict, kind: str) -> str:
        ratio = "exempt" if kind == "exempt" else f"{pair['ratio']:.2f}"
        return (f'<td><span class="pair" style="color:{pair["foreground"]};background:{pair["background"]};">Aa</span>'
                f'<span class="ratio">{ratio}</span></td>')

    body = "".join(
        f'<tr><td>{html.escape(row["element"])}</td><td class="st">{html.escape(row["state"])}</td>'
        f'{cell(row["light"], row["kind"])}{cell(row["dark"], row["kind"])}</tr>'
        for row in rows
    )
    return ('<table class="states"><thead><tr><th>Element</th><th>State</th><th>Light</th><th>Dark</th></tr></thead>'
            f'<tbody>{body}</tbody></table>')


def intro_html(title: str, is_parent: bool, family: list[str]) -> str:
    if is_parent:
        others = [f for f in family if f != title]
        opening = f"{title} is the parent company of {', '.join(others[:-1])} and {others[-1]}."
    else:
        opening = f"{title} is part of the Ağustos family: {', '.join(family[:-1])} and {family[-1]}."
    return f"""
  <p>{opening}
     Every brand shares one symbol, the Laz Güneşi, an 18-blade sun. Ağustos alone uses red.
     The other brands use black or white, and their wordmark tells them apart.</p>
  <p>Our design direction is İskandivvian: Scandinavian restraint filtered through Mediterranean
     warmth. In practice, that means white paper, few colours, clear type and plain language.
     Every element must be useful. Nothing is there for decoration.</p>
  <p>This guide covers the basics: the logo, colour, type and the right file for each job.
     Use it when you make anything that carries the {title} name.</p>"""


def gen_guidelines_html(slug: str, brand: dict, reg: dict, design: dict, out: Path,
                        lk_dir: Path, version: str) -> None:
    colors = design["foundations"]["color"]
    signal = design["semantic"]["color"]["signal"]
    radius = design["foundations"]["radius"]["medium"]
    identity = brand["color"]
    is_red = identity.lower() == signal.lower()
    title = html.escape(brand["title"])
    wordmark = html.escape(brand["wordmark"])
    domain = html.escape(brand.get("domain", ""))
    family = [html.escape(b["title"]) for b in reg["brands"].values()]
    family_html = '<h2>The family</h2><table class="files">' + "".join(
        f'<tr><td><span class="wm" style="font-size:17px;color:{b["color"]};">{html.escape(b["wordmark"])}</span></td>'
        f'<td>{html.escape(b["title"])}</td><td class="path">{html.escape(b.get("domain", ""))}</td></tr>'
        for b in reg["brands"].values()
    ) + "</table>"

    ink, soft, faint = colors["ink"], colors["inkSoft"], colors["inkFaint"]
    paper, cream, gray, rule = colors["paperWhite"], colors["paperCream"], colors["paperGray"], colors["ruleCream"]
    danger = colors["stateDanger"]
    sizes = design["foundations"]["fontSize"]
    weights = design["foundations"]["fontWeight"]
    # The one type table (recipes.typeRoles): the same rows as the web kit and UI-KIT.md.
    roles = {row["role"]: row for row in design["typeRoles"]}

    def type_sample(role: str, face: str, text: str, extra: str = "") -> str:
        r = roles[role]
        tracking = f"letter-spacing:{r['tracking']};" if r.get("tracking") else ""
        return (f'<div style="font-family:\'{face}\';font-weight:{r["weight"]};font-size:{px(r["size"])};'
                f'{tracking}line-height:{r["lineHeight"]};{extra}">{text}</div>')
    # The wrong colour in the recolour example: red for a black brand, blue for Ağustos.
    wrong = colors["stateInfo"] if is_red else signal

    fonts = BRAND_DIR / "fonts"
    f_it = (fonts / "inter-tight" / "InterTight[wght].ttf").as_uri()
    f_in = (fonts / "inter" / "Inter[opsz,wght].ttf").as_uri()
    f_mo = (fonts / "jetbrains-mono" / "JetBrainsMono[wght].ttf").as_uri()
    pos = (lk_dir / f"{slug}-lockup__positive.svg").as_uri()
    neg = (lk_dir / f"{slug}-lockup__negative.svg").as_uri()
    mono = (lk_dir / f"{slug}-lockup__mono.svg").as_uri()
    sym = tinted(SYMBOL, identity)

    def page(head: str, content: str) -> str:
        num = SECTIONS.index(head) + 1  # section 1 is on page 3
        return (f'<section class="page"><h1><span class="n">{num}</span>{head}</h1>{content}'
                f'<div class="foot"><span>{title} brand guidelines</span><span>{num + 2}</span></div></section>')

    contents = "".join(
        f'<li><span>{i + 1}&nbsp;&nbsp;{s}</span><span class="pg">{i + 3}</span></li>'
        for i, s in enumerate(SECTIONS)
    )

    usage = [
        ("Positive", pos, paper, "Default. Light backgrounds, about 90% of uses."),
        ("Negative", neg, identity, "On the identity colour, dark colours and photographs."),
        ("Mono", mono, paper, "One ink only: stamps, engraving, single-colour print."),
    ]
    usage_html = "".join(
        f'<div class="card"><div class="stage" style="background:{bg};">'
        f'<img src="{src}" style="max-height:44px;max-width:86%;"></div>'
        f'<div class="cap"><b>{name}</b><br>{text}</div></div>'
        for name, src, bg, text in usage
    )

    misuse = [
        ("Do not stretch or squash the logo.",
         f'<img src="{pos}" style="height:34px;transform:scaleX(1.45);">'),
        ("Do not recolour the logo.",
         f'<img src="{tinted(lk_dir / f"{slug}-lockup__positive.svg", wrong)}" style="height:34px;">'),
        ("Do not rotate the logo.",
         f'<img src="{pos}" style="height:34px;transform:rotate(-14deg);">'),
        ("Do not set the wordmark in capitals.",
         f'<span class="lock"><img src="{sym}" style="height:30px;">'
         f'<span class="wm" style="color:{identity};">{tr_upper(wordmark)}</span></span>'),
        ("Do not add a tagline or other text.",
         f'<span class="lock-col"><img src="{pos}" style="height:30px;">'
         f'<span class="tag">Tagline text</span></span>'),
        ("Do not add shadows or effects.",
         f'<img src="{pos}" style="height:34px;filter:drop-shadow(3px 4px 3px {faint});">'),
    ]
    misuse_html = "".join(
        f'<div class="card"><div class="stage">{art}</div><div class="cap"><span class="no">Don\'t</span> {text.removeprefix("Do not ")}</div></div>'
        for text, art in misuse
    )

    ident_text = (
        f"The {title} identity colour is red, {identity.upper()}. Only the Ağustos logo is red. "
        f"Red fills a surface in one place only: the identity tile behind the negative logo."
        if is_red else
        f"The {title} identity colour is off-black, {identity.upper()}. Red belongs to Ağustos. "
        f"Never make the {title} logo red."
    )
    swatches = "".join(
        f'<div class="sw"><div class="chip" style="background:{hx};"></div>'
        f'<div class="swn">{name}</div>'
        f'<div class="swv">HEX {hx.upper()}<br>RGB {" ".join(str(c) for c in hexrgb(hx))}</div>'
        f'<div class="swr">{role}</div></div>'
        for name, hx, role in six_colours(colors, signal)
    )

    files = [
        ("Logo for a website or app", "lockup/…-lockup__positive.svg"),
        ("Logo on a dark or photo background", "lockup/…-lockup__negative.svg"),
        ("Logo in one ink", "lockup/…-lockup__mono.svg"),
        ("Logo for print", "lockup/…-lockup__positive.pdf"),
        ("Logo for slides or social posts", "lockup/…-lockup__positive.png"),
        ("Favicon or app icon (symbol on a white tile)", "favicon/favicon.svg"),
        ("Profile picture", "social/…-avatar-1000.png"),
        ("Link preview image", "social/…-og.png"),
        ("Colour swatches", "swatches/….ase (Adobe), ….clr (Apple)"),
        ("Presentation", "office/…-template.pptx"),
        ("Letter or document", "office/…-letterhead.docx, …-document-template.docx"),
        ("Email signature", "email/…-signature.html"),
    ]
    files_html = "".join(
        f"<tr><td>{need}</td><td class='path'>{path.replace('…', slug)}</td></tr>"
        for need, path in files
    )

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{title} brand guidelines</title><style>
@font-face {{ font-family:'Inter Tight'; src:url('{f_it}'); font-weight:100 900; }}
@font-face {{ font-family:'Inter'; src:url('{f_in}'); font-weight:100 900; }}
@font-face {{ font-family:'JetBrains Mono'; src:url('{f_mo}'); font-weight:100 900; }}
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
body {{ margin:0; font-family:'Inter',sans-serif; color:{ink}; background:{paper}; }}
.page {{ width:210mm; height:297mm; padding:24mm 20mm 26mm; page-break-after:always; position:relative; overflow:hidden; }}
.page:last-child {{ page-break-after:auto; }}
h1 {{ font-family:'Inter Tight'; font-weight:{roles['h1']['weight']}; font-size:38px; letter-spacing:{roles['h1']['tracking']}; line-height:1.1; margin:0 0 18px; }}
h1 .n {{ color:{faint}; margin-right:14px; font-variant-numeric:tabular-nums; }}
h2 {{ font-family:'Inter Tight'; font-weight:{roles['h3']['weight']}; font-size:17px; margin:30px 0 10px; }}
p {{ font-size:13px; line-height:1.65; max-width:64ch; color:{soft}; margin:0 0 12px; }}
.foot {{ position:absolute; bottom:12mm; left:20mm; right:20mm; font-size:9.5px; color:{faint};
         border-top:1px solid {rule}; padding-top:6px; display:flex; justify-content:space-between; }}
.grid3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:20px; }}
.grid2 {{ display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin-top:20px; }}
.card {{ border:1px solid {rule}; border-radius:{radius}; overflow:hidden; }}
.stage {{ height:120px; display:flex; align-items:center; justify-content:center; background:{paper}; }}
.cap {{ font-size:11px; line-height:1.5; color:{soft}; padding:10px 12px; border-top:1px solid {rule}; }}
.cap b {{ font-family:'Inter Tight'; font-weight:600; color:{ink}; font-size:12px; }}
.no {{ font-weight:700; color:{danger}; }}
.lock {{ display:inline-flex; align-items:center; gap:9px; }}
.lock-col {{ display:inline-flex; flex-direction:column; align-items:flex-start; gap:4px; }}
.wm {{ font-family:'Inter Tight'; font-weight:650; font-size:26px; line-height:1; }}
.tag {{ font-size:12px; color:{soft}; padding-left:40px; }}

/* cover and back cover */
.cover {{ display:flex; flex-direction:column; }}
.cover img {{ height:64px; align-self:flex-start; margin-top:70mm; }}
.cover .t {{ font-family:'Inter Tight'; font-weight:650; font-size:54px; letter-spacing:-0.025em; margin:34mm 0 6px; }}
.cover .s {{ font-size:15px; color:{soft}; }}
.back {{ background:{identity}; display:flex; align-items:center; justify-content:center; }}
.back img {{ height:60px; }}
.back .foot {{ border-color:rgba(255,255,255,.25); color:rgba(255,255,255,.75); }}

/* contents */
ol.toc {{ list-style:none; padding:0; margin:26px 0 0; max-width:120mm; }}
ol.toc li {{ display:flex; justify-content:space-between; font-size:15px; padding:11px 0; border-bottom:1px solid {rule}; }}
ol.toc .pg {{ color:{faint}; font-variant-numeric:tabular-nums; }}

/* symbol */
.symbol-hero {{ display:flex; gap:22px; align-items:center; margin:26px 0 8px; }}
.symbol-hero .big {{ padding:30px; border:1px solid {rule}; border-radius:{radius}; }}
.symbol-sizes {{ display:flex; gap:26px; align-items:flex-end; margin-top:20px; }}
.symbol-sizes div {{ font-size:10px; color:{faint}; text-align:center; }}

/* clear space */
.clear {{ display:inline-block; position:relative; padding:56px; border:1px dashed {faint}; margin-top:18px; }}
.clear img {{ height:56px; display:block; outline:1px solid {rule}; }}
.clear .x {{ position:absolute; font-size:11px; color:{faint}; font-family:'JetBrains Mono'; }}
.minrow {{ display:flex; gap:40px; align-items:flex-end; margin-top:16px; }}
.minrow div {{ font-size:11px; color:{soft}; }}

/* colour */
.ident {{ display:flex; gap:18px; align-items:center; margin:20px 0 6px; }}
.ident .chip {{ width:120px; height:78px; }}
.swatches {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px 14px; margin-top:12px; }}
.chip {{ height:60px; border-radius:{radius}; border:1px solid {rule}; }}
.swn {{ font-family:'Inter Tight'; font-weight:650; font-size:13px; margin-top:8px; }}
.swv {{ font-family:'JetBrains Mono'; font-size:10px; color:{soft}; line-height:1.6; margin-top:2px; }}
.swr {{ font-size:10.5px; color:{faint}; line-height:1.45; margin-top:4px; }}
.note {{ background:{cream}; border-radius:{radius}; padding:12px 14px; font-size:11.5px; color:{soft}; margin-top:18px; line-height:1.55; }}

/* type */
.spec {{ border-top:1px solid {rule}; padding:14px 0; display:grid; grid-template-columns:44mm 1fr; gap:12px; align-items:baseline; }}
.spec .k {{ font-size:10.5px; color:{faint}; line-height:1.5; }}
.spec .k b {{ font-family:'Inter Tight'; font-weight:600; color:{ink}; font-size:12px; display:block; }}

/* colour in use */
.rules {{ margin:14px 0 0; padding:0; list-style:none; }}
.rules li {{ font-size:11px; line-height:1.5; color:{soft}; padding:3px 0; border-top:1px solid {rule}; }}
.rules b {{ font-family:'Inter Tight'; font-weight:600; color:{ink}; }}
table.states {{ width:100%; border-collapse:collapse; margin-top:12px; font-size:9.5px; }}
table.states th {{ text-align:left; font-family:'Inter Tight'; font-weight:600; color:{ink}; padding:0 0 5px; border-bottom:1px solid {ink}; }}
table.states td {{ padding:1.5px 0; border-bottom:1px solid {rule}; color:{soft}; vertical-align:middle; }}
table.states td.st {{ color:{faint}; }}
.pair {{ display:inline-block; width:30px; text-align:center; border:1px solid {rule}; border-radius:4px;
         font-family:'Inter Tight'; font-weight:600; font-size:10px; line-height:14px; margin-right:6px; }}
.ratio {{ font-family:'JetBrains Mono'; font-size:9.5px; color:{ink}; }}

/* emphasis */
.em-row {{ border-top:1px solid {rule}; padding:12px 0; display:grid; grid-template-columns:40mm 1fr; gap:14px; }}
.em-row .k {{ font-family:'Inter Tight'; font-weight:600; font-size:12.5px; color:{ink}; }}
.em-row .ex {{ font-size:14px; line-height:1.5; color:{ink}; margin-bottom:5px; }}
.em-row .use, .em-row .never {{ font-size:11px; line-height:1.5; color:{soft}; }}
.em-row .never::before {{ content:"Never: "; font-weight:600; color:{danger}; }}
mark.hl {{ color:inherit; background:linear-gradient(transparent 55%, color-mix(in srgb, {signal} 18%, transparent) 55%); padding:0 2px; }}
.link {{ font-weight:600; text-decoration:underline; text-decoration-color:{signal}; text-decoration-thickness:2px; text-underline-offset:3px; }}
.pairs {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:16px; }}
.pairs .card {{ padding:12px 14px; font-size:12px; line-height:1.55; color:{soft}; }}
.pairs .label {{ font-family:'Inter Tight'; font-weight:600; font-size:11px; margin-bottom:6px; }}
.pairs .h {{ font-family:'Inter Tight'; font-weight:300; font-size:24px; line-height:1.1; color:{ink}; margin-bottom:8px; }}

/* files */
table.files {{ width:100%; border-collapse:collapse; margin-top:18px; font-size:11.5px; }}
table.files td {{ padding:8px 0; border-bottom:1px solid {rule}; vertical-align:top; color:{soft}; }}
table.files td.path {{ font-family:'JetBrains Mono'; font-size:10px; color:{ink}; padding-left:14px; }}
table.medium {{ font-size:10px; line-height:1.4; }}
table.medium th {{ text-align:left; font-weight:600; color:{ink}; padding:0 10px 8px 0; border-bottom:1px solid {rule}; }}
table.medium td {{ padding:8px 10px 8px 0; }}
table.medium td b {{ font-weight:600; color:{ink}; }}
</style></head><body>

<section class="page cover">
  <img src="{pos}" alt="{wordmark}">
  <div class="t">Brand guidelines</div>
  <div class="s">{title}</div>
  <div class="foot"><span>{domain}</span><span>Ağustos Design System {version}</span></div>
</section>

<section class="page">
  <h1>Contents</h1>
  <ol class="toc">{contents}</ol>
  <div class="foot"><span>{title} brand guidelines</span><span>2</span></div>
</section>

{page("Introduction", intro_html(title, slug == "agustos", family) + family_html)}

{page("In every medium", f'''
  <p>A website, a datasheet and a LinkedIn post cannot look the same, but they must read as one brand.
     These rules hold everywhere. Test a new piece by covering its logo: the reader must still know whose it is.</p>
  <table class="files medium">
    <tr><th>Rule</th><th>Website</th><th>Datasheet</th><th>LinkedIn</th></tr>
    {"".join(f"<tr><td><b>{html.escape(r['rule'])}</b></td><td>{html.escape(r['web'])}</td><td>{html.escape(r['datasheet'])}</td><td>{html.escape(r['linkedin'])}</td></tr>" for r in design["designDirection"]["invariants"])}
  </table>''')}

{page("The symbol", f'''
  <p>The Laz Güneşi is an 18-blade sun. Every brand in the family uses this one symbol.
     Use the supplied artwork only. Never redraw, simplify or rearrange the blades.</p>
  <div class="symbol-hero"><div class="big"><img src="{sym}" style="height:150px;"></div></div>
  <h2>Colour of the symbol</h2>
  <p>In the {title} logo, the symbol is {"red" if is_red else "off-black"}, like the wordmark.
     On a dark background, it is white. As a favicon or app icon, the symbol stands alone,
     {"red" if is_red else "off-black"} on a white square tile.</p>
  <div class="symbol-sizes">
    <div><img src="{sym}" style="height:64px;"><br>64px</div>
    <div><img src="{sym}" style="height:32px;"><br>32px</div>
    <div><img src="{sym}" style="height:16px;"><br>16px, smallest</div>
  </div>''')}

{page("The logo", f'''
  <p>The logo is the symbol with the wordmark "{wordmark}", set in Inter Tight at weight 650,
     always lowercase. The two parts are one unit. Do not move them apart or use the
     wordmark without the symbol.</p>
  <h2>Three versions</h2>
  <p>Pick the version by the background. There is no fourth version.</p>
  <div class="grid3">{usage_html}</div>''')}

{page("Clear space and minimum size", f'''
  <p>Keep an empty area around the logo. Its width, x, is equal to the height of the symbol.
     No text, image or page edge can go into this area.</p>
  <div class="clear"><img src="{pos}">
    <span class="x" style="top:20px;left:50%;">x</span>
    <span class="x" style="bottom:20px;left:50%;">x</span>
    <span class="x" style="left:24px;top:50%;">x</span>
    <span class="x" style="right:24px;top:50%;">x</span>
  </div>
  <h2>Minimum size</h2>
  <p>Below these heights, the wordmark is hard to read. For smaller spaces, use the symbol alone.</p>
  <div class="minrow">
    <div><img src="{pos}" style="height:24px;display:block;margin-bottom:8px;">On screen: 24px tall</div>
    <div><img src="{pos}" style="height:8mm;display:block;margin-bottom:8px;">In print: 8mm tall</div>
  </div>''')}

{page("Logo misuse", f'''
  <p>The logo works only when it looks the same everywhere. These are the most common mistakes.</p>
  <div class="grid2">{misuse_html}</div>''')}

{page("Colour", f'''
  <p>{ident_text}</p>
  <div class="ident"><div class="chip" style="background:{identity};"></div>
    <div><div class="swn">Identity colour</div>
    <div class="swv">HEX {identity.upper()}<br>RGB {" ".join(str(c) for c in hexrgb(identity))}</div></div></div>
  <h2>The six colours</h2>
  <p>Every house brand uses the same six colours. White is the paper. In layouts, red is a signal, not a fill.</p>
  <div class="swatches">{swatches}</div>
  <div class="note">For print, match these colours against a printer proof. CMYK and Pantone values
     are not registered yet. Do not convert the screen values yourself.</div>''')}

{page("Colour in use", f'''
  <p>On screens, colour follows the state of each element. Every pair below clears the WCAG 2.2 AA floor:
     4.5:1 for text, 3:1 for borders, logos and the focus ring. The same pairs hold in the light and the dark theme.</p>
  <ul class="rules">
    <li><b>Red is identity and signal, never action.</b> Buttons are black in every brand. Red marks the Ağustos logo,
        the 2px link rule, the current menu item, keyboard focus and one highlighter stroke.</li>
    <li><b>Hover.</b> On light paper a link turns red. On dark paper red text is too faint (3.35:1), so the text dims
        and the red rule stays. The Ağustos logo turns off-black (white on dark); every other logo turns red.</li>
    <li><b>Pressed and disabled.</b> A pressed button moves 1px down. A disabled control turns gray and does not react.</li>
    <li><b>Light islands.</b> The footer and the closing band stay light in the dark theme.</li>
  </ul>
  {states_html(design["states"])}''')}

{page("Typography", f'''
  <p>Three typefaces, all free and open source. Headings are thin and large; weight, not colour, sets the order.
     Write in sentence case. Sizes follow one scale: the {sizes["body"]} body times 1.272 per step, so every
     second step is the golden ratio.</p>
  <div style="margin-top:14px;">
  <div class="spec"><div class="k"><b>Hero, Inter Tight {roles["hero"]["weight"]}</b>{px(roles["hero"]["size"])} on screen. One per page.</div>
    {type_sample("hero", "Inter Tight", "Light")}</div>
  <div class="spec"><div class="k"><b>H1, Inter Tight {roles["h1"]["weight"]}</b>{px(roles["h1"]["size"])}. Page titles.</div>
    {type_sample("h1", "Inter Tight", "Right light")}</div>
  <div class="spec"><div class="k"><b>H2, Inter Tight {roles["h2"]["weight"]}</b>{px(roles["h2"]["size"])}. Sections.</div>
    {type_sample("h2", "Inter Tight", "Product range")}</div>
  <div class="spec"><div class="k"><b>H3, Inter Tight {roles["h3"]["weight"]}</b>{px(roles["h3"]["size"])}. Cards and subsections.</div>
    {type_sample("h3", "Inter Tight", "Specifications")}</div>
  <div class="spec"><div class="k"><b>Body, Inter {roles["body"]["weight"]}</b>{px(roles["body"]["size"])}, line height {roles["body"]["lineHeight"]}, about 75 characters a line at most.</div>
    {type_sample("body", "Inter", "Body text is set at a comfortable size with generous line spacing.", f"color:{soft};")}</div>
  <div class="spec"><div class="k"><b>Small print, Inter {roles["footnote"]["weight"]}</b>{px(roles["footnote"]["size"])}. Footnotes and captions.</div>
    {type_sample("footnote", "Inter", "Prices exclude VAT.", f"color:{soft};")}</div>
  <div class="spec"><div class="k"><b>Spec values, JetBrains Mono</b>Data with units, on the web, the datasheet and LinkedIn. Labels stay in Inter Tight.</div>
    {type_sample("spec", "JetBrains Mono", "PX22 · 160 W · 4200 lm")}</div>
  <div class="spec"><div class="k"><b>Wordmark, Inter Tight {weights["wordmark"]}</b>The logo only. Never for text.</div>
    <div class="wm" style="color:{identity};">{wordmark}</div></div>
  </div>
  <p style="margin-top:12px;">Four text weights: {weights["light"]}, {weights["regular"]}, {weights["medium"]} and {weights["semibold"]}. Every face supports Turkish:
     ağustos · İstanbul · ışık · Güneş. Documents and slides use the same faces at the sizes their templates carry.</p>''')}

{page("Emphasis", f'''
  <p>Emphasis is rationed. Each tool has one job, and they are never combined. When everything stands out, nothing does.</p>
  <div style="margin-top:12px;">
  <div class="em-row"><div class="k">Red highlighter</div><div>
    <div class="ex" style="font-family:'Inter Tight';font-weight:300;font-size:24px;">Light for <mark class="hl">architecture</mark></div>
    <div class="use">Once per page, on one to four words of the main headline. The sentence must read the same without it.</div>
    <div class="never">body text, links, buttons, numbers, product screens, or a second stroke.</div></div></div>
  <div class="em-row"><div class="k">Bold ({weights["semibold"]})</div><div>
    <div class="ex">Delivery takes <b style="font-weight:{weights["semibold"]};">four weeks</b> from the order.</div>
    <div class="use">A fact the reader scans for: a value, a deadline, a term at its first use. At most once per paragraph.</div>
    <div class="never">whole sentences, headings inside running text, or next to the highlighter.</div></div></div>
  <div class="em-row"><div class="k">Italic</div><div>
    <div class="ex">The symbol is the <i>Laz Güneşi</i>, shown in <i>Lighting Journal</i>.</div>
    <div class="use">Names of publications and projects, foreign terms, and quoted phrases.</div>
    <div class="never">to stress a word, in headings, or in buttons.</div></div></div>
  <div class="em-row"><div class="k">Underline</div><div>
    <div class="ex">Read the <span class="link">installation guide</span>.</div>
    <div class="use">Links only. On screens it is a 2px red rule.</div>
    <div class="never">for emphasis, in print or on screen.</div></div></div>
  <div class="em-row"><div class="k">Colour and capitals</div><div>
    <div class="use">Text stays off-black or dark gray. Headings and labels are in sentence case.</div>
    <div class="never">coloured text, all-capital labels, or small labels above a heading.</div></div></div>
  </div>
  <div class="pairs">
    <div class="card"><div class="label" style="color:{colors["stateSuccess"]};">Do</div>
      <div class="h">Light for <mark class="hl">architecture</mark></div>
      Our fittings ship in <b style="font-weight:{weights["semibold"]};">four weeks</b>. See the <span class="link">product range</span>.</div>
    <div class="card"><div class="label" style="color:{danger};">Don't</div>
      <div style="font-size:10px;letter-spacing:.12em;color:{signal};font-weight:600;margin-bottom:4px;">NEW COLLECTION</div>
      <div class="h" style="font-weight:700;">Light for <mark class="hl">architecture</mark></div>
      Our <b><i>fittings</i></b> ship in <mark class="hl"><b>four weeks</b></mark>. <u>Call us today</u>.</div>
  </div>''')}

{page("Which file to use", f'''
  <p>Use the finished files. Do not redraw the logo or copy it from a website or a PDF.
     Every file below is in the {title} brand kit, in the folder named in the right column.</p>
  <table class="files">{files_html}</table>
  <p style="margin-top:16px;">Fonts: Inter Tight, Inter and JetBrains Mono, with their licences, are in the fonts folder of the kit.</p>''')}

<section class="page back">
  <img src="{neg}" alt="{wordmark}">
  <div class="foot"><span>{domain}</span><span>{len(SECTIONS) + 3}</span></div>
</section>

</body></html>"""
    out.write_text(doc, encoding="utf-8")


def render_pdf(html_path: Path, pdf: Path) -> None:
    if not BROWSE.exists():
        raise SystemExit(f"browse tool not found at {BROWSE}; cannot render {pdf.name}")
    subprocess.run([str(BROWSE), "goto", html_path.resolve().as_uri()], check=True, capture_output=True)
    subprocess.run([str(BROWSE), "pdf", str(pdf), "--prefer-css-page-size", "--print-background"],
                   check=True, capture_output=True)
    print(f"    rendered {pdf.relative_to(ROOT)}")


def build_brand(slug: str, brand: dict, reg: dict, design: dict, want_pdf: bool = False) -> Path:
    base = BRAND_DIR / "exports" / slug
    lk = base / "lockup"
    if not (lk / f"{slug}-lockup__positive.svg").exists():
        raise SystemExit(f"missing lockups for {slug}; run build.py --brand {slug} first")
    gl = base / "guidelines"
    gl.mkdir(parents=True, exist_ok=True)
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    out = gl / f"{slug}-brand-guidelines.html"
    gen_guidelines_html(slug, brand, reg, design, out, lk, version)
    print(f"    wrote {out.relative_to(ROOT)}")
    if want_pdf:
        render_pdf(out, out.with_suffix(".pdf"))
    return out


def main() -> None:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    design = json.loads(TOKENS.read_text(encoding="utf-8"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand")
    ap.add_argument("--pdf", action="store_true", help="also render the PDF through browse")
    args = ap.parse_args()
    brands = reg["brands"]
    if args.brand and args.brand not in brands:
        raise SystemExit(f"unknown brand '{args.brand}'")
    # Guidelines ship with the full kit, the same brands as the Office files.
    targets = [args.brand] if args.brand else [s for s, b in brands.items() if b.get("office", False)]
    for slug in targets:
        build_brand(slug, brands[slug], reg, design, args.pdf)


if __name__ == "__main__":
    main()
