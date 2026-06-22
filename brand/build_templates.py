#!/usr/bin/env python3
"""
Ağustos brand kit — office documents, swatches, email signature, guidelines source.

Sibling to build.py (which makes the visual logo assets). This generates the
"working document" deliverables from the same registry, so they stay in sync:

  exports/<brand>/swatches/    <brand>.ase (Adobe) + <brand>.clr (Apple)
  exports/<brand>/email/       <brand>-signature.html (email-safe, self-contained)
  exports/<brand>/office/      <brand>-letterhead.docx + <brand>-template.pptx
  exports/<brand>/guidelines/  <brand>-brand-guidelines.html (rendered to PDF by browse)

Run after build.py (it reuses the generated lockup PNGs).

  ../.venv/bin/python build_templates.py [--brand <slug>]
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import struct
from pathlib import Path

from PIL import Image

BRAND_DIR = Path(__file__).resolve().parent
ROOT = BRAND_DIR.parent
REGISTRY = BRAND_DIR / "brands.json"


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def b64_png(path: Path, width: int) -> str:
    """Resize a PNG to `width` and return a base64 data URI (for self-contained email)."""
    im = Image.open(path).convert("RGBA")
    h = round(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ----------------------------------------------------------------------------
# Color swatches
# ----------------------------------------------------------------------------

def palette(brand, reg):
    """The brand's working palette: brand color + neutrals from the system."""
    sub = reg["substrate"]
    return [
        (brand["title"], brand["color"]),
        ("Ink", "#1a1a1a"),
        ("Ink Soft", "#4a4a4a"),
        ("Ink Faint", "#8a8a8a"),
        ("Paper (Cream)", sub["paper"]),
        ("Paper White", sub["paper_white"]),
        ("Rule", "#e8e3d0"),
    ]


def write_ase(colors, out: Path):
    """Adobe Swatch Exchange (.ase) — opens in Illustrator, Photoshop, InDesign,
    Affinity, Figma (via plugin). Big-endian binary."""
    blob = b"ASEF" + struct.pack(">HH", 1, 0) + struct.pack(">I", len(colors))
    for name, hx in colors:
        r, g, b = (c / 255 for c in hexrgb(hx))
        nm = name.encode("utf-16-be") + b"\x00\x00"
        body = struct.pack(">H", len(name) + 1) + nm + b"RGB " + struct.pack(">fff", r, g, b) + struct.pack(">H", 2)
        blob += struct.pack(">H", 1) + struct.pack(">I", len(body)) + body
    out.write_bytes(blob)


def write_clr(colors, list_name, out: Path):
    """Apple Color List (.clr) — drops into the macOS system color picker.
    Uses AppKit (PyObjC); macOS only."""
    from AppKit import NSColorList, NSColor
    from Foundation import NSURL
    cl = NSColorList.alloc().initWithName_(list_name)
    for name, hx in colors:
        r, g, b = (c / 255 for c in hexrgb(hx))
        cl.setColor_forKey_(NSColor.colorWithSRGBRed_green_blue_alpha_(r, g, b, 1.0), name)
    cl.writeToURL_error_(NSURL.fileURLWithPath_(str(out)), None)


# ----------------------------------------------------------------------------
# Email signature (email-safe HTML: table layout, inline styles, web-safe font)
# ----------------------------------------------------------------------------

def gen_email_signature(slug, brand, reg, out: Path, lockup_png: Path):
    logo = b64_png(lockup_png, 320)
    color = brand["color"]
    title = brand["title"]
    tagline = brand.get("tagline", "")
    domain = brand.get("domain", "")
    html = f"""<!-- {title} email signature. Paste into your mail client's signature editor.
     Self-contained (logo embedded). Replace {{{{NAME}}}}, {{{{ROLE}}}}, {{{{PHONE}}}}. -->
<table cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,Helvetica,sans-serif;color:#1a1a1a;">
  <tr>
    <td style="padding-right:18px;vertical-align:middle;">
      <img src="{logo}" width="150" alt="{title}" style="display:block;border:0;">
    </td>
    <td style="border-left:2px solid {color};padding-left:18px;vertical-align:middle;line-height:1.5;">
      <div style="font-size:15px;font-weight:bold;color:#1a1a1a;">{{{{NAME}}}}</div>
      <div style="font-size:13px;color:#4a4a4a;">{{{{ROLE}}}} &middot; {title}</div>
      <div style="font-size:12px;color:{color};padding:2px 0 6px;">{tagline}</div>
      <div style="font-size:12px;color:#4a4a4a;">
        {{{{PHONE}}}} &nbsp;|&nbsp;
        <a href="mailto:hello@{domain}" style="color:#4a4a4a;text-decoration:none;">hello@{domain}</a> &nbsp;|&nbsp;
        <a href="https://{domain}" style="color:{color};text-decoration:none;font-weight:bold;">{domain}</a>
      </div>
    </td>
  </tr>
</table>
"""
    out.write_text(html, encoding="utf-8")


# ----------------------------------------------------------------------------
# Word letterhead (.docx)
# ----------------------------------------------------------------------------

def _bottom_border(paragraph, color, size="18"):
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", size), ("w:space", "6"), ("w:color", color)):
        bottom.set(qn(k), v)
    pBdr.append(bottom)
    pPr.append(pBdr)


def gen_letterhead_docx(slug, brand, reg, out: Path, lockup_png: Path):
    import docx
    from docx.shared import Cm, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    color = RGBColor(*hexrgb(brand["color"]))
    ink_soft = RGBColor(0x4a, 0x4a, 0x4a)
    title, domain, tagline = brand["title"], brand.get("domain", ""), brand.get("tagline", "")

    doc = docx.Document()
    doc.styles["Normal"].font.name = "Inter"
    doc.styles["Normal"].font.size = Pt(11)
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)  # A4
    for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, m, Cm(2.2))

    # Header: lockup + brand-red rule
    hdr = sec.header
    hp = hdr.paragraphs[0]
    hp.add_run().add_picture(str(lockup_png), width=Cm(4.6))
    rule = hdr.add_paragraph()
    _bottom_border(rule, brand["color"].lstrip("#"))

    # Footer: contact line
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run(f"{title}  ·  {tagline}  ·  {domain}")
    r.font.size = Pt(8.5)
    r.font.color.rgb = ink_soft

    # Body sample
    h = doc.add_paragraph()
    hr = h.add_run("Letter title")
    hr.font.name = "Inter Tight"
    hr.font.size = Pt(20)
    hr.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)
    doc.add_paragraph(
        "Replace this with your letter body. The header logo, the brand rule, and the "
        "footer contact line are part of the letterhead — type your content here. Body "
        "text is set in Inter; install the bundled fonts so it renders correctly."
    )
    doc.save(str(out))


# ----------------------------------------------------------------------------
# PowerPoint template (.pptx)  — also the basis for a Google Slides import
# ----------------------------------------------------------------------------

def gen_pptx(slug, brand, reg, out: Path, pos_png: Path, neg_png: Path):
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    cream = RGBColor(*hexrgb(reg["substrate"]["paper"]))
    brand_c = RGBColor(*hexrgb(brand["color"]))
    ink = RGBColor(0x1a, 0x1a, 0x1a)
    ink_soft = RGBColor(0x4a, 0x4a, 0x4a)
    title, tagline, domain = brand["title"], brand.get("tagline", ""), brand.get("domain", "")

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    W, H = prs.slide_width, prs.slide_height
    blank = prs.slide_layouts[6]

    def bg(slide, rgb):
        f = slide.background.fill
        f.solid()
        f.fore_color.rgb = rgb

    def textbox(slide, x, y, w, h, text, size, font, rgb, bold=False, align=PP_ALIGN.LEFT):
        tb = slide.shapes.add_textbox(x, y, w, h)
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = align
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.name = font
        run.font.bold = bold
        run.font.color.rgb = rgb
        return tb

    def add_logo(slide, png, width_in, x, y):
        pic = slide.shapes.add_picture(str(png), x, y, width=Inches(width_in))
        return pic

    # 1 — Title (cream)
    s = prs.slides.add_slide(blank); bg(s, cream)
    add_logo(s, pos_png, 3.2, Inches(0.9), Inches(0.8))
    textbox(s, Inches(0.9), Inches(3.0), Inches(11.5), Inches(2.0),
            "Presentation title", 54, "Inter Tight", ink, bold=True)
    textbox(s, Inches(0.92), Inches(4.4), Inches(10), Inches(1),
            tagline, 20, "Inter", ink_soft)

    # 2 — Section divider (brand color, reversed lockup)
    s = prs.slides.add_slide(blank); bg(s, brand_c)
    add_logo(s, neg_png, 3.0, Inches(0.9), Inches(0.7))
    textbox(s, Inches(0.9), Inches(3.1), Inches(11.5), Inches(1.6),
            "Section title", 44, "Inter Tight", cream, bold=True)

    # 3 — Content (cream)
    s = prs.slides.add_slide(blank); bg(s, cream)
    textbox(s, Inches(0.9), Inches(0.7), Inches(11), Inches(1),
            "Content slide", 32, "Inter Tight", ink, bold=True)
    body = s.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(11.2), Inches(4.6)).text_frame
    body.word_wrap = True
    for i, line in enumerate(["First point in Inter body type.",
                              "Second point — keep it tight.",
                              "Third point, with a brand-red accent on links."]):
        p = body.paragraphs[0] if i == 0 else body.add_paragraph()
        run = p.add_run(); run.text = "•  " + line
        run.font.size = Pt(20); run.font.name = "Inter"; run.font.color.rgb = ink
        p.space_after = Pt(10)

    # 4 — Closing (cream)
    s = prs.slides.add_slide(blank); bg(s, cream)
    add_logo(s, pos_png, 3.0, Inches(0.9), Inches(2.6))
    textbox(s, Inches(0.92), Inches(4.1), Inches(10), Inches(1),
            f"{domain}", 18, "Inter Tight", brand_c, bold=True)

    prs.save(str(out))


# ----------------------------------------------------------------------------
# Brand guidelines (HTML — rendered to PDF by browse)
# ----------------------------------------------------------------------------

def gen_guidelines_html(slug, brand, reg, out: Path, lk_dir: Path, fav_dir: Path):
    color = brand["color"]
    title, tagline, domain = brand["title"], brand.get("tagline", ""), brand.get("domain", "")
    fonts = BRAND_DIR / "fonts"
    pal = palette(brand, reg)
    sw = "".join(
        f'<div class="sw"><div class="chip" style="background:{hx};'
        f'{"border:1px solid #e8e3d0;" if hx.lower() in ("#fefcf2","#ffffff") else ""}"></div>'
        f'<div class="swn">{name}</div><div class="swh">{hx.upper()}</div></div>'
        for name, hx in pal
    )
    # file:// URLs to the bundled fonts so the PDF renders in real brand type.
    it = (fonts / "inter-tight" / "InterTight[wght].ttf").as_uri()
    inr = (fonts / "inter" / "Inter[opsz,wght].ttf").as_uri()
    pos = (lk_dir / f"{slug}-lockup__positive.svg").as_uri()
    neg = (lk_dir / f"{slug}-lockup__negative.svg").as_uri()
    mono = (lk_dir / f"{slug}-lockup__mono.svg").as_uri()
    fav = (fav_dir / "favicon.svg").as_uri()

    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'IT'; src:url('{it}'); }}
@font-face {{ font-family:'IN'; src:url('{inr}'); }}
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
body {{ margin:0; font-family:'IN',sans-serif; color:#1a1a1a; background:#fefcf2; }}
.page {{ width:210mm; min-height:297mm; padding:22mm 20mm; page-break-after:always; position:relative; }}
.page:last-child {{ page-break-after:auto; }}
h1 {{ font-family:'IT'; font-weight:650; font-size:46px; letter-spacing:-0.03em; margin:0 0 6px; }}
h2 {{ font-family:'IT'; font-weight:650; font-size:13px; text-transform:uppercase; letter-spacing:0.14em; color:#8a8a8a; margin:34px 0 14px; }}
p {{ font-size:13.5px; line-height:1.65; max-width:62ch; color:#4a4a4a; }}
.cover-mark {{ width:230px; margin:48mm 0 10mm; }}
.eyebrow {{ font-family:'IT'; font-weight:650; font-size:12px; text-transform:uppercase; letter-spacing:0.16em; color:{color}; }}
.foot {{ position:absolute; bottom:14mm; left:20mm; right:20mm; font-size:10px; color:#8a8a8a; border-top:1px solid #e8e3d0; padding-top:6px; display:flex; justify-content:space-between; }}
.row {{ display:flex; gap:18px; flex-wrap:wrap; align-items:flex-end; }}
.card {{ border:1px solid #e8e3d0; border-radius:6px; padding:18px; }}
.card.dark {{ background:{color}; border-color:{color}; }}
.card img {{ height:38px; display:block; }}
.lbl {{ font-family:'IT'; font-weight:650; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#8a8a8a; margin-top:12px; }}
.swatches {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }}
.chip {{ height:64px; border-radius:6px; }}
.swn {{ font-family:'IT'; font-weight:650; font-size:12px; margin-top:8px; }}
.swh {{ font-size:11px; color:#8a8a8a; font-variant-numeric:tabular-nums; }}
.type-it {{ font-family:'IT'; }}
.spec {{ font-size:32px; }}
.do {{ color:#1f6b4a; font-weight:bold; }} .dont {{ color:{color}; font-weight:bold; }}
ul.rules {{ font-size:12.5px; line-height:1.7; color:#4a4a4a; padding-left:18px; }}
.clearbox {{ display:inline-block; border:1px dashed {color}; padding:14px; }}
.clearbox img {{ height:46px; display:block; }}
</style></head><body>

<section class="page">
  <div class="eyebrow">Brand Guidelines</div>
  <img class="cover-mark" src="{pos}">
  <h1>{title}</h1>
  <p style="font-size:16px;color:#1a1a1a;">{tagline}</p>
  <div class="foot"><span>{domain}</span><span>v1 · generated from the Ağustos Design System</span></div>
</section>

<section class="page">
  <div class="eyebrow">01</div><h1>The logo</h1>
  <p>The mark is the Laz Güneşi symbol locked up with the wordmark. Three expressions cover every
     surface. Use the positive form first — it works on cream and dark backgrounds alike.</p>
  <div class="row" style="margin-top:18px;">
    <div class="card"><img src="{pos}"><div class="lbl">Positive — primary</div></div>
    <div class="card dark"><img src="{neg}"><div class="lbl" style="color:rgba(255,255,255,.7)">Negative — on brand</div></div>
    <div class="card"><img src="{mono}"><div class="lbl">Mono — single colour</div></div>
  </div>
  <h2>Clear space &amp; minimum size</h2>
  <p>Keep clear space around the lockup equal to the symbol height. Never place type or edges inside it.
     Minimum size: 24px tall on screen, 8mm in print, so the wordmark stays legible.</p>
  <div class="clearbox"><img src="{pos}"></div>
  <div class="foot"><span>{title} — Brand Guidelines</span><span>{domain}</span></div>
</section>

<section class="page">
  <div class="eyebrow">02</div><h1>Colour</h1>
  <p>One brand colour, used as a signal — on links, rules, and accents — never as flat decoration.
     Everything else is the cream substrate and the ink neutrals.</p>
  <div class="swatches" style="margin-top:18px;">{sw}</div>
  <h2>Do &amp; don't</h2>
  <ul class="rules">
    <li><span class="do">Do</span> set the wordmark in Inter Tight Semibold, lowercase, in the brand colour.</li>
    <li><span class="dont">Don't</span> recolour the symbol, stretch the lockup, or add a tagline beside it.</li>
    <li><span class="do">Do</span> keep the brand colour for emphasis; <span class="dont">don't</span> fill large areas with it except the negative lockup tile.</li>
  </ul>
  <div class="foot"><span>{title} — Brand Guidelines</span><span>{domain}</span></div>
</section>

<section class="page">
  <div class="eyebrow">03</div><h1>Typography</h1>
  <p>Two families, one skeleton. Inter Tight for display and the wordmark; Inter for body. JetBrains Mono for code and data.</p>
  <div style="margin-top:22px;">
    <div class="type-it spec" style="font-weight:650;">Inter Tight Semibold</div>
    <div class="lbl">Display · wordmark · headings</div>
  </div>
  <div style="margin-top:26px;">
    <div class="spec">Inter — body text</div>
    <div class="lbl">Paragraphs · captions · tables</div>
  </div>
  <p style="margin-top:30px;">The Turkish locale is first-class: <span class="type-it" style="font-weight:650;">ağustos</span>,
     <span class="type-it" style="font-weight:650;">İstanbul</span>, <span class="type-it" style="font-weight:650;">ışık</span> —
     the dotted/dotless i and the ğ breve all render correctly.</p>
  <div class="foot"><span>{title} — Brand Guidelines</span><span>{domain}</span></div>
</section>

</body></html>"""
    out.write_text(html, encoding="utf-8")


# ----------------------------------------------------------------------------

def build_brand(slug, brand, reg):
    base = BRAND_DIR / "exports" / slug
    lk = base / "lockup"
    fav = base / "favicon"
    pos_png = lk / f"{slug}-lockup__positive.png"
    neg_png = lk / f"{slug}-lockup__negative.png"
    if not pos_png.exists():
        raise SystemExit(f"missing {pos_png} — run build.py --brand {slug} first")

    sw_dir = base / "swatches"; sw_dir.mkdir(parents=True, exist_ok=True)
    em_dir = base / "email"; em_dir.mkdir(parents=True, exist_ok=True)
    of_dir = base / "office"; of_dir.mkdir(parents=True, exist_ok=True)
    gl_dir = base / "guidelines"; gl_dir.mkdir(parents=True, exist_ok=True)

    pal = palette(brand, reg)
    write_ase(pal, sw_dir / f"{slug}.ase")
    try:
        write_clr(pal, brand["title"], sw_dir / f"{slug}.clr")
    except Exception as e:
        print(f"    (skipped .clr: {e})")
    gen_email_signature(slug, brand, reg, em_dir / f"{slug}-signature.html", pos_png)
    gen_letterhead_docx(slug, brand, reg, of_dir / f"{slug}-letterhead.docx", pos_png)
    gen_pptx(slug, brand, reg, of_dir / f"{slug}-template.pptx", pos_png, neg_png)
    gen_guidelines_html(slug, brand, reg, gl_dir / f"{slug}-brand-guidelines.html", lk, fav)

    n = sum(1 for _ in base.rglob("*") if _.is_file())
    print(f"  ✓ {slug}: office + extras done ({n} files total in exports/{slug})")


def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand")
    args = ap.parse_args()
    brands = reg["brands"]
    if args.brand and args.brand not in brands:
        raise SystemExit(f"unknown brand '{args.brand}'")
    targets = {args.brand: brands[args.brand]} if args.brand else brands
    print(f"Building office/extras for {len(targets)} brand(s)...")
    for slug, brand in targets.items():
        build_brand(slug, brand, reg)
    print("Done. (Render guidelines HTML -> PDF with browse; see templates/README.md)")


if __name__ == "__main__":
    main()
