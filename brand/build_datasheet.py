#!/usr/bin/env python3
"""
Ağustos brand kit — lighting product datasheet ("teknik föy") template.

Sibling to build.py (logos) and build_templates.py (office/working docs). This
generates a print-ready A4 product datasheet per brand, populated with one sample
luminaire so the field structure is self-documenting. Same generate-don't-maintain
contract as the rest of the kit: the brand chrome (lockup, colour, footer) resolves
from brands.json; you fill in the product data.

  exports/<brand>/datasheet/<product-key>.html   source (embeds fonts + lockup)
  exports/<brand>/datasheet/<product-key>.pdf     rendered by browse (with --pdf)

A datasheet is half template, half data. The brand half comes from brands.json; the
product half is the PRODUCTS dict below — a flat registry keyed by product (e.g.
"pataraz-px22"), each entry naming its brand. That is the one place to edit field
labels, add spec rows, or document a new luminaire. A brand can hold any number of
products; each emits its own sheet named after its key. Labels are Turkish; lang="tr"
is set so İ/ı capitalisation renders correctly.

Run after build.py (it reuses the generated lockup SVGs).

  python3 build_datasheet.py [--brand <slug>] [--product <key>] [--pdf]
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import re
import subprocess
from pathlib import Path

BRAND_DIR = Path(__file__).resolve().parent
ROOT = BRAND_DIR.parent
REGISTRY = BRAND_DIR / "brands.json"
FONTS = BRAND_DIR / "fonts"
BROWSE = Path.home() / ".claude/skills/gstack/browse/dist/browse"


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ----------------------------------------------------------------------------
# Product data — THE place to edit. A flat registry keyed by product; each entry
# names its `brand` (the slug in brands.json). A brand may hold many products —
# every entry emits its own A4 sheet named after its key (e.g. pataraz-px22.pdf).
#
# Field labels are Turkish. To document a new product, copy a block, give it a new
# key, set `brand`, and replace the values; to change which specs appear, edit the
# `specs` groups (the group title becomes the brand-coloured section label). Order
# matters — rows render top-to-bottom, groups flow into 2 columns.
# ----------------------------------------------------------------------------

PRODUCTS = {
    # Real product — data transcribed from pataraz.com/pl-serisi/pl22 (2026-06-23).
    # Fields the public product page does not publish are left as "—" placeholders;
    # fill them from the manufacturer's full spec sheet. The PL series is Pataraz's
    # ultra-thin artificial-skylight ("tavan penceresi") panel — a tunable-white
    # daylight-effect ceiling product, so it has no beam angle / ordering variants.
    "pataraz-pl22": {
        "brand": "pataraz",
        "name": "PL22",
        "series": "PL serisi · ultra ince tavan penceresi",
        "code": "PL22",
        "doc_type": "Teknik Föy",
        "rev": "Rev. 01 · 2026-06",
        "photo": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "pl22-urun.jpg"),
        "drawing": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "pl22-drawing.png"),
        "description": (
            "Gökyüzü penceresi etkisi yaratan ultra ince tavan paneli. 2100–7500 K "
            "ayarlanabilir beyaz ışığıyla gün ışığının ritmini iç mekâna taşır; yüksek "
            "renksel geriverim (Ra 93) ile renkleri doğal gösterir. Sıva üstü montaj, "
            "Bluetooth ve DALI ile kontrol."
        ),
        "dim_note": "B × D × Y: 1236 × 636 × 70 mm",
        "specs": {
            "Elektriksel": [
                ("Güç", "160 W"),
                ("Kontrol sistemi", "Bluetooth · DALI"),
            ],
            "Fotometrik": [
                ("Işık çıkışı", "4200 lm"),
                ("Renk sıcaklığı", "2100–7500 K (ayarlanabilir)"),
                ("Renksel geriverim", "Ra 93"),
            ],
            "Fiziksel": [
                ("Boyutlar", "1236 × 636 × 70 mm"),
                ("Ağırlık", "29,8 kg"),
                ("Montaj şekli", "Sıva üstü"),
                ("Montaj yeri", "Tavan"),
            ],
            "Koruma & Ortam": [
                ("Koruma sınıfı (IP)", "IP20"),
                ("Ortam sıcaklığı (ta)", "−20 … +40 °C"),
                ("İzolasyon sınıfı", "Class II"),
            ],
            "Ömür & Garanti": [
                ("Ömür", "L70B50 @ 30.000 saat"),
                ("Garanti", "2 yıl"),
            ],
        },
        # No ordering matrix / certifications published for PL22 — sections omitted.
    },
    # Real product — data transcribed from pataraz.com/px-serisi/px22 (2026-06-23),
    # the wall-mounted ("duvar penceresi") sibling of PL22. Shares PL22's electrical /
    # photometric / control core identically (160 W, BT+DALI, 2100–7500 K, Ra 93,
    # 4200 lm), differing only in size, weight and mounting. The 5 fields the public
    # page omits (IP, ta, izolasyon, ömür, garanti) are carried over from PL22 as a
    # same-platform assumption — confirm against the manufacturer's full spec sheet.
    "pataraz-px22": {
        "brand": "pataraz",
        "name": "PX22",
        "series": "PX serisi · ultra ince duvar penceresi",
        "code": "PX22",
        "doc_type": "Teknik Föy",
        "rev": "Rev. 01 · 2026-06",
        "photo": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "px22-urun.jpg"),
        "drawing": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "px22-drawing.png"),
        "description": (
            "Duvar penceresi etkisi yaratan ultra ince ışık paneli. 2100–7500 K "
            "ayarlanabilir beyaz ışığıyla gün ışığının ritmini penceresiz iç mekânlara "
            "taşır; yüksek renksel geriverim (Ra 93) ile renkleri doğal gösterir. Sıva "
            "altı veya sıva üstü montaj, Bluetooth ve DALI ile kontrol."
        ),
        # Width is 781 mm (confirmed by the product owner). The supplied technical
        # drawing mislabels it as 718 (a 781↔718 transposition); the drawing PNG was
        # corrected to 781 to match. Height 1332 and depth 66 agree across sources.
        "dim_note": "G × Y × D: 781 × 1332 × 66 mm",
        "specs": {
            "Elektriksel": [
                ("Güç", "160 W"),
                ("Kontrol sistemi", "Bluetooth · DALI"),
            ],
            "Fotometrik": [
                ("Işık çıkışı", "4200 lm"),
                ("Renk sıcaklığı", "2100–7500 K (ayarlanabilir)"),
                ("Renksel geriverim", "Ra 93"),
            ],
            "Fiziksel": [
                ("Boyutlar", "781 × 1332 × 66 mm"),
                ("Ağırlık", "29,4 kg"),
                ("Montaj şekli", "Sıva altı · sıva üstü"),
                ("Montaj yeri", "Duvar"),
            ],
            "Koruma & Ortam": [
                ("Koruma sınıfı (IP)", "IP20"),
                ("Ortam sıcaklığı (ta)", "−20 … +40 °C"),
                ("İzolasyon sınıfı", "Class II"),
            ],
            "Ömür & Garanti": [
                ("Ömür", "L70B50 @ 30.000 saat"),
                ("Garanti", "2 yıl"),
            ],
        },
        # IP / ta / izolasyon / ömür / garanti carried over from PL22 (same platform);
        # no ordering matrix — a single tunable SKU with no published variants.
    },
    # Real products — PY serisi, data transcribed from pataraz.com/py-serisi/py300600,
    # /py600600, /py6001200 (2026-08-10). Three sizes of the same recessed ceiling
    # panel ("ışık paneli") sharing PL/PX's tuning platform (Bluetooth+DALI,
    # 2100–7500 K, Ra 93) — differ by power, output, size, and weight. IP / ta /
    # izolasyon / ömür / garanti are not published for this series; per explicit
    # product-owner direction (2026-08-10) they are carried over from PL22/PX22
    # (IP20, −20…+40 °C, Class II, L70B50 @ 30.000 saat, 2 yıl) as a same-platform
    # assumption across all three PY sizes — confirm against the manufacturer's
    # full PY spec sheet when published.
    #
    # PY300600 and PY6001200 use pataraz.com's identical product render — both are
    # 1:2 elongated-rectangle panels (300:600 and 600:1200 reduce to the same
    # ratio), so the shared illustrative image is dimensionally consistent, not a
    # site error. Each entry still points at its own downloaded copy.
    #
    # Thickness corrected 36→43 mm (owner-confirmed, 2026-08-10): the site's 36mm is
    # the flat panel alone; 43mm is the true installed depth including the mounting
    # clips shown in the owner-supplied technical drawing. Applied to all three
    # sizes on the assumption the clip hardware is shared across the PY family
    # (same edge/frame system, only the panel area changes) — confirm if any size
    # uses a different clip. NOTE: pataraz.com itself still shows 36mm; the owner
    # is updating the live site separately, this fix only corrects the datasheet.
    # Drawings generated in-house (side profile + front elevation, matching the
    # owner-supplied reference style) since pataraz.com publishes none for this
    # series — see datasheet-assets/pataraz/py*-drawing.svg.
    "pataraz-py300600": {
        "brand": "pataraz",
        "name": "PY300600",
        "series": "PY serisi · ultra ince ışık paneli",
        "code": "PY300600",
        "doc_type": "Teknik Föy",
        "rev": "Rev. 01 · 2026-08",
        "photo": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "py300600.png"),
        "drawing": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "py300600-drawing.svg"),
        "description": (
            "Gökyüzü etkisi yaratan ultra ince ışık paneli, PY serisinin kompakt "
            "ölçüsü. 2100–7500 K ayarlanabilir beyaz ışığıyla gün ışığının ritmini "
            "iç mekâna taşır; yüksek renksel geriverim (Ra 93) ile renkleri doğal "
            "gösterir. Sıva altı montaj, Bluetooth ve DALI ile kontrol."
        ),
        "dim_note": "G × U × Y: 300 × 600 × 43 mm",
        "specs": {
            "Elektriksel": [
                ("Güç", "40 W"),
                ("Kontrol sistemi", "Bluetooth · DALI"),
            ],
            "Fotometrik": [
                ("Işık çıkışı", "1050 lm"),
                ("Renk sıcaklığı", "2100–7500 K (ayarlanabilir)"),
                ("Renksel geriverim", "Ra 93"),
            ],
            "Fiziksel": [
                ("Boyutlar", "300 × 600 × 43 mm"),
                ("Gökyüzü boyutu", "527 × 227 mm"),
                ("Ağırlık", "2,84 kg"),
                ("Montaj şekli", "Sıva altı"),
                ("Montaj yeri", "Tavan"),
            ],
            "Koruma & Ortam": [
                ("Koruma sınıfı (IP)", "IP20"),
                ("Ortam sıcaklığı (ta)", "−20 … +40 °C"),
                ("İzolasyon sınıfı", "Class II"),
            ],
            "Ömür & Garanti": [
                ("Ömür", "L70B50 @ 30.000 saat"),
                ("Garanti", "2 yıl"),
            ],
        },
        # No ordering matrix / certifications published for PY300600.
    },
    "pataraz-py600600": {
        "brand": "pataraz",
        "name": "PY600600",
        "series": "PY serisi · ultra ince ışık paneli",
        "code": "PY600600",
        "doc_type": "Teknik Föy",
        "rev": "Rev. 01 · 2026-08",
        "photo": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "py600600.png"),
        "drawing": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "py600600-drawing.svg"),
        "description": (
            "Gökyüzü etkisi yaratan ultra ince ışık paneli, PY serisinin kare "
            "ölçüsü. 2100–7500 K ayarlanabilir beyaz ışığıyla gün ışığının ritmini "
            "iç mekâna taşır; yüksek renksel geriverim (Ra 93) ile renkleri doğal "
            "gösterir. Sıva altı montaj, Bluetooth ve DALI ile kontrol."
        ),
        "dim_note": "G × U × Y: 600 × 600 × 43 mm",
        "specs": {
            "Elektriksel": [
                ("Güç", "60 W"),
                ("Kontrol sistemi", "Bluetooth · DALI"),
            ],
            "Fotometrik": [
                ("Işık çıkışı", "2100 lm"),
                ("Renk sıcaklığı", "2100–7500 K (ayarlanabilir)"),
                ("Renksel geriverim", "Ra 93"),
            ],
            "Fiziksel": [
                ("Boyutlar", "600 × 600 × 43 mm"),
                ("Gökyüzü boyutu", "527 × 527 mm"),
                ("Ağırlık", "4,8 kg"),
                ("Montaj şekli", "Sıva altı"),
                ("Montaj yeri", "Tavan"),
            ],
            "Koruma & Ortam": [
                ("Koruma sınıfı (IP)", "IP20"),
                ("Ortam sıcaklığı (ta)", "−20 … +40 °C"),
                ("İzolasyon sınıfı", "Class II"),
            ],
            "Ömür & Garanti": [
                ("Ömür", "L70B50 @ 30.000 saat"),
                ("Garanti", "2 yıl"),
            ],
        },
        # No ordering matrix / certifications published for PY600600.
    },
    "pataraz-py6001200": {
        "brand": "pataraz",
        "name": "PY6001200",
        "series": "PY serisi · ultra ince ışık paneli",
        "code": "PY6001200",
        "doc_type": "Teknik Föy",
        "rev": "Rev. 01 · 2026-08",
        "photo": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "py6001200.png"),
        "drawing": str(BRAND_DIR / "datasheet-assets" / "pataraz" / "py6001200-drawing.svg"),
        "description": (
            "Gökyüzü etkisi yaratan ultra ince ışık paneli, PY serisinin geniş "
            "ölçüsü. 2100–7500 K ayarlanabilir beyaz ışığıyla gün ışığının ritmini "
            "iç mekâna taşır; yüksek renksel geriverim (Ra 93) ile renkleri doğal "
            "gösterir. Sıva altı montaj, Bluetooth ve DALI ile kontrol."
        ),
        "dim_note": "G × U × Y: 1200 × 600 × 43 mm",
        "specs": {
            "Elektriksel": [
                ("Güç", "100 W"),
                ("Kontrol sistemi", "Bluetooth · DALI"),
            ],
            "Fotometrik": [
                ("Işık çıkışı", "2700 lm"),
                ("Renk sıcaklığı", "2100–7500 K (ayarlanabilir)"),
                ("Renksel geriverim", "Ra 93"),
            ],
            "Fiziksel": [
                ("Boyutlar", "1200 × 600 × 43 mm"),
                ("Gökyüzü boyutu", "1127 × 227 mm"),
                ("Ağırlık", "8 kg"),
                ("Montaj şekli", "Sıva altı"),
                ("Montaj yeri", "Tavan"),
            ],
            "Koruma & Ortam": [
                ("Koruma sınıfı (IP)", "IP20"),
                ("Ortam sıcaklığı (ta)", "−20 … +40 °C"),
                ("İzolasyon sınıfı", "Class II"),
            ],
            "Ömür & Garanti": [
                ("Ömür", "L70B50 @ 30.000 saat"),
                ("Garanti", "2 yıl"),
            ],
        },
        # No ordering matrix / certifications published for PY6001200.
    },
    "agustos-pro-spot-28": {
        "brand": "agustos",
        "name": "Pro Spot 28",
        "series": "Pro seri · 3-fazlı ray spotu",
        "code": "AGT-PRS28",
        "doc_type": "Teknik Föy",
        "rev": "Rev. 01 · 2026-06",
        "description": (
            "Yüksek renksel geriverimli, dar ışın açılı ray spotu. Döküm alüminyum gövde "
            "ve hassas reflektör optiği ile mağaza, galeri ve sergi alanlarında vurgu "
            "aydınlatması için tasarlanmıştır. 3-fazlı ray adaptörü ile konumlandırması "
            "esnek, değiştirilebilir optikleri ile sahaya uyarlanabilir."
        ),
        "dim_note": "Ø × Y: 75 × 180 mm (ray adaptörü dahil)",
        "specs": {
            "Elektriksel": [
                ("Güç", "28 W"),
                ("Besleme gerilimi", "220–240 V AC · 50/60 Hz"),
                ("Sürücü", "Dahili, TRIAC dimlenebilir"),
                ("Güç faktörü", "> 0,90"),
                ("Giriş akımı", "130 mA"),
            ],
            "Fotometrik": [
                ("Işık akısı (armatür)", "2.600 lm"),
                ("Etkinlik", "93 lm/W"),
                ("Renk sıcaklığı", "3000 K"),
                ("Renksel geriverim", "Ra ≥ 95"),
                ("Renk toleransı", "≤ 2 SDCM"),
                ("Işın açısı", "24° (15°/24°/36° seçenekli)"),
                ("Optik", "Değiştirilebilir reflektör"),
            ],
            "Fiziksel": [
                ("Boyutlar", "Ø 75 × 180 mm"),
                ("Ağırlık", "0,8 kg"),
                ("Gövde", "Döküm alüminyum"),
                ("Yüzey / Renk", "RAL 9005 mat siyah"),
                ("Dönüş / Eğim", "355° / 90°"),
                ("Montaj", "3-fazlı ray adaptörü"),
            ],
            "Koruma & Ortam": [
                ("Koruma sınıfı", "IP20"),
                ("Darbe dayanımı", "IK05"),
                ("Ortam sıcaklığı (ta)", "−10 … +35 °C"),
                ("İzolasyon sınıfı", "Class I"),
                ("Fotobiyolojik güvenlik", "RG0"),
            ],
            "Ömür & Garanti": [
                ("Ömür", "L90B10 @ 50.000 saat"),
                ("Garanti", "5 yıl"),
            ],
        },
        "certifications": ["CE", "RoHS"],
        "ordering": {
            "columns": ["Sipariş kodu", "Renk sıcaklığı", "Işın açısı", "Işık akısı", "Güç", "Yüzey"],
            "rows": [
                ["AGT-PRS28-3015", "3000 K", "15°", "2.450 lm", "28 W", "Siyah"],
                ["AGT-PRS28-3024", "3000 K", "24°", "2.600 lm", "28 W", "Siyah"],
                ["AGT-PRS28-3036", "3000 K", "36°", "2.700 lm", "28 W", "Siyah"],
                ["AGT-PRS28-3024-W", "3000 K", "24°", "2.600 lm", "28 W", "Beyaz"],
            ],
        },
    },
}

# Brands without a bespoke sample fall back to a generic luminaire block so the
# template still generates. (Only agustos + pataraz were requested.)
GENERIC = {
    "name": "Ürün Adı",
    "series": "Seri · ürün ailesi",
    "code": "KOD-000",
    "doc_type": "Teknik Föy",
    "rev": "Rev. 01 · 2026-06",
    "description": "Ürün açıklamasını buraya yazın. Bir-iki cümlede ürünün tipini, "
                   "uygulamasını ve öne çıkan özelliğini belirtin.",
    "dim_note": "L × G × Y: — × — × — mm",
    "specs": {
        "Elektriksel": [("Güç", "— W"), ("Besleme gerilimi", "220–240 V AC"),
                        ("Sürücü", "Dahili"), ("Güç faktörü", "> 0,90")],
        "Fotometrik": [("Işık akısı (armatür)", "— lm"), ("Etkinlik", "— lm/W"),
                       ("Renk sıcaklığı", "3000 K"), ("Renksel geriverim", "Ra ≥ 90"),
                       ("Işın açısı", "—°")],
        "Fiziksel": [("Boyutlar", "— mm"), ("Ağırlık", "— kg"),
                     ("Gövde", "Alüminyum"), ("Montaj", "—")],
        "Koruma & Ortam": [("Koruma sınıfı", "IP20"), ("Ortam sıcaklığı (ta)", "—  °C"),
                           ("İzolasyon sınıfı", "Class I")],
        "Ömür & Garanti": [("Ömür", "L80B10 @ 50.000 saat"), ("Garanti", "— yıl")],
    },
    "certifications": ["CE", "RoHS"],
    "ordering": {
        "columns": ["Sipariş kodu", "Renk sıcaklığı", "Işın açısı", "Işık akısı", "Güç", "Yüzey"],
        "rows": [["KOD-000-3024", "3000 K", "24°", "— lm", "— W", "Siyah"]],
    },
}


# ----------------------------------------------------------------------------
# HTML fragments
# ----------------------------------------------------------------------------

def _img_data_uri(path: Path) -> str:
    """Base64 data URI so the datasheet HTML stays self-contained and portable
    (the image travels inside the file, like the embedded fonts and lockup)."""
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    if mime == "image/svg+xml":  # SVG: reference by file URI (vector, stays crisp)
        return path.resolve().as_uri()
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{data}"


def _visual_slot(label, sub, img_path):
    """A photo/drawing slot: real image if given, else a dashed placeholder."""
    if img_path and Path(img_path).exists():
        inner = f'<img src="{_img_data_uri(Path(img_path))}" alt="{label}">'
        cls = "slot has-img"
    else:
        inner = (f'<div class="ph"><div class="ph-mark">+</div>'
                 f'<div class="ph-lbl">{label}</div><div class="ph-sub">{sub}</div></div>')
        cls = "slot"
    return f'<div class="{cls}"><div class="slot-cap">{label}</div>{inner}</div>'


def _spec_groups(specs):
    blocks = []
    for title, rows in specs.items():
        r = "".join(
            f'<div class="srow"><span class="sk">{k}</span>'
            f'<span class="sv">{v}</span></div>'
            for k, v in rows
        )
        blocks.append(f'<div class="group"><div class="glabel">{title}</div>{r}</div>')
    return "".join(blocks)


def _ordering(order):
    head = "".join(f"<th>{c}</th>" for c in order["columns"])
    body = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
        for row in order["rows"]
    )
    return (f'<table class="order"><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table>')


def gen_datasheet_html(slug, brand, reg, product, out: Path, lk_dir: Path):
    color = brand["color"]
    title, domain = brand["title"], brand.get("domain", "")
    it = (FONTS / "inter-tight" / "InterTight[wght].ttf").as_uri()
    inr = (FONTS / "inter" / "Inter[opsz,wght].ttf").as_uri()
    mono = (FONTS / "jetbrains-mono" / "JetBrainsMono[wght].ttf").as_uri()
    pos = (lk_dir / f"{slug}-lockup__positive.svg").as_uri()

    photo = _visual_slot("Ürün görseli", "ürün fotoğrafını buraya ekleyin",
                         product.get("photo"))
    drawing = _visual_slot("Teknik çizim", product.get("dim_note", "ölçüler — mm"),
                          product.get("drawing"))

    # Ordering matrix + certifications are optional — omit the section when the
    # product has none (e.g. a single tunable SKU with no published variants).
    order = product.get("ordering")
    ordering_html = (f'<div class="section-label">Sipariş matrisi</div>{_ordering(order)}'
                     if order and order.get("rows") else "")
    cert_list = product.get("certifications") or []
    certs_html = (f'<div class="certs"><b>Sertifikalar</b>{"  ·  ".join(cert_list)}</div>'
                  if cert_list else "")

    html = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<title>{title} — {product['name']} · {product['doc_type']}</title><style>
@font-face {{ font-family:'IT'; src:url('{it}'); }}
@font-face {{ font-family:'IN'; src:url('{inr}'); }}
@font-face {{ font-family:'JB'; src:url('{mono}'); }}
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
:root {{ --brand:{color}; --ink:#1a1a1a; --soft:#4a4a4a; --faint:#8a8a8a;
         --paper:#fefcf2; --rule:#e8e3d0; }}
body {{ margin:0; font-family:'IN',sans-serif; color:var(--ink); background:var(--paper);
        font-feature-settings:"locl" on,"kern" on; }}
.page {{ width:210mm; height:297mm; overflow:hidden; padding:12mm 13mm 12mm; position:relative; }}

/* Header */
.head {{ display:flex; justify-content:space-between; align-items:flex-end;
         padding-bottom:8px; border-bottom:2px solid var(--brand); }}
.head img {{ height:30px; display:block; }}
.head .doc {{ text-align:right; }}
.doc-type {{ font-family:'IT'; font-weight:650; font-size:11px; text-transform:uppercase;
             letter-spacing:0.16em; color:var(--brand); }}
.doc-code {{ font-family:'JB'; font-size:11px; color:var(--soft); margin-top:3px;
             font-variant-numeric:tabular-nums; }}

/* Title block */
.title {{ margin-top:12px; }}
h1 {{ font-family:'IT'; font-weight:650; font-size:30px; letter-spacing:-0.02em; margin:0; }}
.series {{ font-size:13px; color:var(--soft); margin-top:2px; }}

/* Visual slots */
.visuals {{ display:grid; grid-template-columns:1fr 1fr; gap:8mm; margin-top:11px; }}
.slot {{ position:relative; }}
.slot-cap {{ font-family:'IT'; font-weight:650; font-size:9.5px; text-transform:uppercase;
             letter-spacing:0.12em; color:var(--faint); margin-bottom:5px; }}
.slot .ph, .slot.has-img img {{ width:100%; aspect-ratio:3/2; border-radius:5px; }}
.slot .ph {{ border:1.5px dashed var(--rule); display:flex; flex-direction:column;
             align-items:center; justify-content:center; background:#fff; }}
.slot.has-img img {{ object-fit:contain; border:1px solid var(--rule); background:#fff; }}
.ph-mark {{ font-family:'IT'; font-weight:300; font-size:30px; color:var(--brand);
            line-height:1; opacity:0.55; }}
.ph-lbl {{ font-family:'IT'; font-weight:650; font-size:12px; color:var(--soft); margin-top:6px; }}
.ph-sub {{ font-size:10px; color:var(--faint); margin-top:2px; }}

/* Description */
.desc {{ font-size:12px; line-height:1.6; color:var(--soft); max-width:64ch; margin:13px 0 2px; }}

/* Spec grid — groups packed into 2 columns */
.section-label {{ font-family:'IT'; font-weight:650; font-size:10px; text-transform:uppercase;
                  letter-spacing:0.14em; color:var(--ink); margin:16px 0 9px;
                  padding-bottom:5px; border-bottom:1px solid var(--rule); }}
.specs {{ columns:2; column-gap:12mm; }}
.group {{ break-inside:avoid; -webkit-column-break-inside:avoid; display:inline-block;
          width:100%; margin-bottom:11px; }}
.glabel {{ font-family:'IT'; font-weight:650; font-size:9.5px; text-transform:uppercase;
           letter-spacing:0.1em; color:var(--brand); margin-bottom:5px;
           padding-left:8px; border-left:2px solid var(--brand); }}
.srow {{ display:flex; justify-content:space-between; gap:8px; align-items:baseline;
         padding:2.5px 0; border-bottom:1px solid rgba(0,0,0,0.045); }}
.sk {{ font-size:10px; color:var(--soft); flex:1 1 auto; }}
.sv {{ font-family:'JB'; font-size:10px; color:var(--ink); text-align:right;
       white-space:nowrap; font-variant-numeric:tabular-nums; }}

/* Ordering matrix */
.order {{ width:100%; border-collapse:collapse; margin-top:6px; border-top:2px solid var(--brand); }}
.order th {{ font-family:'IT'; font-weight:650; font-size:9px; text-transform:uppercase;
            letter-spacing:0.08em; color:var(--ink); text-align:left;
            padding:6px 8px; border-bottom:1px solid var(--rule); }}
.order td {{ font-family:'JB'; font-size:10px; color:var(--ink); padding:5px 8px;
            border-bottom:1px solid var(--rule); font-variant-numeric:tabular-nums; }}
.order tbody tr:nth-child(even) {{ background:rgba(0,0,0,0.02); }}
.order td:first-child {{ color:var(--brand); }}

/* Certifications */
.certs {{ margin-top:11px; font-size:10px; color:var(--soft); }}
.certs b {{ font-family:'IT'; font-weight:650; font-size:9px; text-transform:uppercase;
            letter-spacing:0.12em; color:var(--faint); margin-right:8px; }}

/* Footer */
.foot {{ position:absolute; left:13mm; right:13mm; bottom:9mm; display:flex;
         justify-content:space-between; align-items:flex-end; gap:12px;
         border-top:1px solid var(--rule); padding-top:6px;
         font-size:9px; color:var(--faint); }}
.foot .brand {{ font-family:'IT'; font-weight:650; color:var(--soft); }}
.foot .disc {{ flex:1; text-align:center; }}
.foot .rev {{ font-family:'JB'; font-variant-numeric:tabular-nums; }}
</style></head><body>
<section class="page">

  <div class="head">
    <img src="{pos}" alt="{title}">
    <div class="doc">
      <div class="doc-type">{product['doc_type']}</div>
      <div class="doc-code">{product['code']}</div>
    </div>
  </div>

  <div class="title">
    <h1>{product['name']}</h1>
    <div class="series">{product['series']}</div>
  </div>

  <div class="visuals">{photo}{drawing}</div>

  <p class="desc">{product['description']}</p>

  <div class="section-label">Teknik özellikler</div>
  <div class="specs">{_spec_groups(product['specs'])}</div>

  {ordering_html}

  {certs_html}

  <div class="foot">
    <span class="brand">{title}</span>
    <span class="disc">Teknik özellikler haber verilmeksizin değiştirilebilir.</span>
    <span class="rev">{domain} · {product['rev']}</span>
  </div>

</section>
</body></html>"""
    out.write_text(html, encoding="utf-8")


def render_pdf(html: Path, pdf: Path):
    if not BROWSE.exists():
        print(f"    (skipped PDF: browse tool not found at {BROWSE})")
        return
    subprocess.run([str(BROWSE), "goto", html.resolve().as_uri()], check=True,
                   capture_output=True)
    subprocess.run([str(BROWSE), "pdf", str(pdf), "--prefer-css-page-size",
                    "--print-background"], check=True, capture_output=True)
    print(f"    ✓ rendered {pdf.name}")


# ----------------------------------------------------------------------------

def _build(key, slug, brand, reg, product, want_pdf):
    base = BRAND_DIR / "exports" / slug
    lk = base / "lockup"
    pos = lk / f"{slug}-lockup__positive.svg"
    if not pos.exists():
        raise SystemExit(f"missing {pos} — run build.py --brand {slug} first")

    ds_dir = base / "datasheet"
    ds_dir.mkdir(parents=True, exist_ok=True)
    html = ds_dir / f"{key}.html"
    gen_datasheet_html(slug, brand, reg, product, html, lk)
    print(f"  ✓ {slug}: {product['name']} → {html.relative_to(ROOT)}")
    if want_pdf:
        render_pdf(html, ds_dir / f"{key}.pdf")


def build_product(key, product, reg, want_pdf):
    slug = product["brand"]
    if slug not in reg["brands"]:
        raise SystemExit(f"product '{key}' names unknown brand '{slug}'")
    _build(key, slug, reg["brands"][slug], reg, product, want_pdf)


def build_generic(slug, brand, reg, want_pdf):
    """A brand with no product entry still gets a sheet — a generic blank form."""
    _build(f"{slug}-datasheet-template", slug, brand, reg, GENERIC, want_pdf)


# Fields gen_datasheet_html / build_product read by hard subscript. Optional keys
# (photo, drawing, dim_note, ordering, certifications) use .get() and are not listed.
REQUIRED_FIELDS = ("brand", "name", "series", "code", "doc_type", "rev",
                   "description", "specs")
_KEY_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def _validate_products(reg):
    """Fail loudly and early on a malformed PRODUCTS entry, rather than a bare
    KeyError mid-build or a key that escapes the datasheet/ dir as a filename.
    The registry is meant to grow, so a new entry's mistakes surface here."""
    brands = reg["brands"]
    for key, product in PRODUCTS.items():
        if not _KEY_RE.match(key):
            raise SystemExit(f"product key '{key}' is not slug-safe "
                             f"(lowercase letters, digits, single hyphens)")
        missing = [f for f in REQUIRED_FIELDS if f not in product]
        if missing:
            raise SystemExit(f"product '{key}' missing field(s): {', '.join(missing)}")
        slug = product["brand"]
        if slug not in brands:
            raise SystemExit(f"product '{key}' names unknown brand '{slug}'")
        if not key.startswith(f"{slug}-"):
            raise SystemExit(f"product key '{key}' must start with its brand "
                             f"'{slug}-' (keeps the output filename brand-scoped)")


def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", help="all products for one brand slug")
    ap.add_argument("--product", help="single product key, e.g. pataraz-px22")
    ap.add_argument("--pdf", action="store_true", help="also render PDF via browse")
    args = ap.parse_args()
    brands = reg["brands"]

    if args.brand and args.product:
        raise SystemExit("--brand and --product are mutually exclusive — "
                         "pass one or neither (no flag builds all products)")
    _validate_products(reg)

    if args.product:
        if args.product not in PRODUCTS:
            raise SystemExit(f"unknown product '{args.product}' — "
                             f"choices: {', '.join(PRODUCTS)}")
        print("Building 1 datasheet...")
        build_product(args.product, PRODUCTS[args.product], reg, args.pdf)
    elif args.brand:
        if args.brand not in brands:
            raise SystemExit(f"unknown brand '{args.brand}'")
        prods = {k: v for k, v in PRODUCTS.items() if v["brand"] == args.brand}
        print(f"Building datasheet(s) for {args.brand}...")
        if prods:
            for k, v in prods.items():
                build_product(k, v, reg, args.pdf)
        else:
            build_generic(args.brand, brands[args.brand], reg, args.pdf)
    else:
        print(f"Building {len(PRODUCTS)} datasheet(s)...")
        for k, v in PRODUCTS.items():
            build_product(k, v, reg, args.pdf)
    print("Done." + ("" if args.pdf else "  (add --pdf to render PDFs)"))


if __name__ == "__main__":
    main()
