#!/usr/bin/env python3
"""Generate every machine-readable and web-facing v3 design-system adapter.

The hand-edited inputs are:
  - tokens/design-tokens.json (cross-medium foundations, semantics, recipes)
  - brand/brands.json         (brand identity values)
  - tokens/web.css.tmpl       (platform-neutral web behavior)

Generated files are committed so consumer repositories can vendor them without
depending on this repository at deploy time. Use --check in CI to reject drift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TOKEN_SOURCE = ROOT / "tokens" / "design-tokens.json"
BRAND_SOURCE = ROOT / "brand" / "brands.json"
WEB_TEMPLATE = ROOT / "tokens" / "web.css.tmpl"
SYMBOL_SOURCE = ROOT / "laz-gunesi-amblem" / "svg" / "master.svg"

CSS_OUTPUTS = {
    ROOT / "tokens" / "agustos.css": "canonical platform-neutral CSS",
    ROOT / "adapters" / "astro" / "src" / "styles" / "tokens.css": "Astro adapter CSS",
    ROOT / "adapters" / "rails" / "app" / "assets" / "stylesheets" / "agustos" / "tokens.css": "Rails adapter CSS",
    ROOT / "adapters" / "wordpress" / "assets" / "css" / "agustos.css": "WordPress adapter CSS",
}

PLACEHOLDER = re.compile(r"\{\{\s*([a-zA-Z0-9_.-]+)\s*\}\}")
ALIAS = re.compile(r"^\{([a-zA-Z0-9_.-]+)\}$")


class TokenError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def lookup(data: dict[str, Any], path: str) -> Any:
    node: Any = data
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            raise TokenError(f"unknown token path: {path}")
        node = node[part]
    return node


def resolve_token(tokens: dict[str, Any], path: str, stack: tuple[str, ...] = ()) -> Any:
    if path in stack:
        raise TokenError(f"circular token alias: {' -> '.join((*stack, path))}")
    node = lookup(tokens, path)
    value = node.get("$value") if isinstance(node, dict) and "$value" in node else node
    if isinstance(value, str):
        match = ALIAS.match(value)
        if match:
            alias = match.group(1)
            if alias == "brand.color":
                return "var(--brand)"
            return resolve_token(tokens, alias, (*stack, path))
    return value


def resolve_tree(tokens: dict[str, Any], node: Any) -> Any:
    if isinstance(node, dict) and "$value" in node:
        value = node["$value"]
        match = ALIAS.match(value) if isinstance(value, str) else None
        if match:
            alias = match.group(1)
            return "{brand.color}" if alias == "brand.color" else resolve_token(tokens, alias)
        return value
    if isinstance(node, dict):
        return {
            key: resolve_tree(tokens, value)
            for key, value in node.items()
            if not key.startswith("$") and key not in {"description", "meta", "compatibility"}
        }
    if isinstance(node, list):
        return [resolve_tree(tokens, item) for item in node]
    return node


def css_easing(value: Any) -> str:
    if isinstance(value, list) and len(value) == 4:
        return "cubic-bezier(" + ", ".join(str(part) for part in value) + ")"
    return str(value)


def css_frame_measure(tokens: dict[str, Any]) -> str:
    """Return content measure plus two gutters without relying on CSS multiplication."""
    content = str(resolve_token(tokens, "foundations.measure.content"))
    gutter = str(resolve_token(tokens, "foundations.measure.gutter"))
    pixel = re.compile(r"^([0-9]+(?:\.[0-9]+)?)px$")
    content_match = pixel.match(content)
    gutter_match = pixel.match(gutter)
    if content_match and gutter_match:
        width = float(content_match.group(1)) + (2 * float(gutter_match.group(1)))
        return f"{width:g}px"
    return f"calc({content} + {gutter} + {gutter})"


def render_web_css(tokens: dict[str, Any], brands: dict[str, Any], label: str) -> str:
    template = WEB_TEMPLATE.read_text(encoding="utf-8")
    version = tokens["version"]
    header = (
        f"AĞUSTOS DESIGN SYSTEM v{version} · GENERATED {label.upper()}\n"
        "   Sources: tokens/design-tokens.json + brand/brands.json + tokens/web.css.tmpl\n"
        "   Do not hand-edit this file. Run: python3 scripts/build_design_system.py"
    )

    def replace(match: re.Match[str]) -> str:
        path = match.group(1)
        if path == "generated_header":
            return header
        if path == "css.easing.standard":
            return css_easing(resolve_token(tokens, "foundations.easing.standard"))
        if path == "css.measure.frame":
            return css_frame_measure(tokens)
        if path.startswith("brands."):
            return str(lookup({"brands": brands["brands"]}, path))
        value = resolve_token(tokens, path)
        if isinstance(value, (dict, list)):
            raise TokenError(f"CSS placeholder must resolve to a scalar: {path}")
        return str(value)

    rendered = PLACEHOLDER.sub(replace, template)
    leftovers = PLACEHOLDER.findall(rendered)
    if leftovers:
        raise TokenError(f"unresolved CSS placeholders: {', '.join(leftovers)}")
    return rendered.rstrip() + "\n"


def wordpress_theme(tokens: dict[str, Any], brands: dict[str, Any]) -> dict[str, Any]:
    color = lambda path: resolve_token(tokens, f"foundations.color.{path}")
    font = lambda path: resolve_token(tokens, f"foundations.fontFamily.{path}")
    size = lambda path: resolve_token(tokens, f"foundations.fontSize.{path}")
    space = lambda path: resolve_token(tokens, f"foundations.spacing.{path}")
    palette = [
        {"slug": "paper", "name": "Paper Cream", "color": color("paperCream")},
        {"slug": "paper-white", "name": "Paper White", "color": color("paperWhite")},
        {"slug": "ink", "name": "Ink", "color": color("ink")},
        {"slug": "ink-soft", "name": "Ink Soft", "color": color("inkSoft")},
        {"slug": "ink-faint", "name": "Ink Faint", "color": color("inkFaint")},
        {"slug": "rule", "name": "Rule", "color": color("ruleCream")},
        {"slug": "rule-white", "name": "Rule White", "color": color("ruleWhite")},
        {"slug": "signal", "name": "Shared Signal Red", "color": color("signalRed")},
    ]
    palette.extend(
        {"slug": f"brand-{slug}", "name": brand["title"], "color": brand["color"]}
        for slug, brand in brands["brands"].items()
    )
    return {
        "$schema": "https://schemas.wp.org/trunk/theme.json",
        "version": 3,
        "settings": {
            "appearanceTools": True,
            "color": {"custom": False, "defaultPalette": False, "palette": palette},
            "layout": {
                "contentSize": resolve_token(tokens, "foundations.measure.content"),
                "wideSize": resolve_token(tokens, "foundations.measure.wide"),
            },
            "spacing": {
                "customSpacingSize": False,
                "spacingSizes": [
                    {"slug": slug, "name": slug.upper(), "size": space(slug)}
                    for slug in ("2xs", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl")
                ],
                "units": ["px", "rem", "em", "%", "vh", "vw"],
            },
            "typography": {
                "customFontSize": False,
                "defaultFontSizes": False,
                "fontFamilies": [
                    {
                        "slug": "display",
                        "name": font("display"),
                        "fontFamily": f"'{font('display')}', '{font('body')}', sans-serif",
                    },
                    {
                        "slug": "body",
                        "name": font("body"),
                        "fontFamily": f"'{font('body')}', sans-serif",
                    },
                    {
                        "slug": "mono",
                        "name": font("mono"),
                        "fontFamily": f"'{font('mono')}', monospace",
                    },
                ],
                "fontSizes": [
                    {"slug": "footnote", "name": "Footnote", "size": size("footnote")},
                    {"slug": "body-compact", "name": "Body Compact", "size": size("bodyCompact")},
                    {"slug": "body", "name": "Body", "size": size("body")},
                    {"slug": "heading-3", "name": "Heading 3", "size": size("h3")},
                    {"slug": "heading-2", "name": "Heading 2", "size": size("h2")},
                    {"slug": "heading-1", "name": "Heading 1", "size": size("h1")},
                    {"slug": "hero-medium", "name": "Hero Medium", "size": size("heroMedium")},
                    {"slug": "hero", "name": "Hero", "size": size("hero")},
                ],
            },
            "custom": {
                "agustos": {
                    "radius": {
                        "small": resolve_token(tokens, "foundations.radius.small"),
                        "medium": resolve_token(tokens, "foundations.radius.medium"),
                        "large": resolve_token(tokens, "foundations.radius.large"),
                    },
                    "motion": {
                        "duration": resolve_token(tokens, "foundations.duration.micro"),
                        "easing": css_easing(resolve_token(tokens, "foundations.easing.standard")),
                    },
                }
            },
        },
        "styles": {
            "color": {"background": "var:preset|color|paper-white", "text": "var:preset|color|ink"},
            "spacing": {
                "padding": {
                    "left": "var:preset|spacing|xl",
                    "right": "var:preset|spacing|xl",
                }
            },
            "typography": {"fontFamily": "var:preset|font-family|body", "lineHeight": "1.65"},
            "elements": {
                "heading": {"typography": {"fontFamily": "var:preset|font-family|display", "fontWeight": "500"}},
                "link": {
                    "color": {"text": "var:preset|color|signal"},
                    "typography": {"fontWeight": "600", "textDecoration": "underline"},
                },
            },
        },
    }


def handoff_contract(resolved: dict[str, Any], tokens: dict[str, Any]) -> dict[str, Any]:
    """Build the self-contained contract intended for another coding system."""
    return {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "name": resolved["name"],
        "version": resolved["version"],
        "instruction": (
            "Use this file as the authority for Ağustos-family visual decisions. Select a brand, apply "
            "semantic roles and recipes, then translate them into native platform structures. Do not "
            "generate repository artifacts during a consumer deployment and do not copy web components "
            "literally into documents or slides."
        ),
        "contract": {
            "authority": "This generated handoff is authoritative; agustos.com is a reference implementation.",
            "recognitionGoal": (
                "Create clear family resemblance across brands and media through shared hierarchy, alignment, "
                "surface, spacing, and signal logic. Pixel-identical output is neither required nor preferred."
            ),
            "invariants": [
                "Use the exact Laz Güneşi asset. Never redraw or approximate the symbol.",
                "Keep every wordmark lowercase, Inter Tight weight 650, and free of taglines.",
                "Ağustos alone owns red as identity ink; Pataraz, PLD Türkiye, Photometric, and future house brands use neutral black/white identity ink by default.",
                "Use shared signal red for links, focus, markers, and small emphasis across every brand; never use it to recolor a non-Ağustos logo.",
                "Default working interfaces to white paper, dark ink, restrained rules, and small radii.",
                "Align primary content to one 920px frame on the web; preserve the same alignment logic in other media.",
                "Prefer large typographic openings, quiet chrome, bordered groups, and generous section rhythm.",
            ],
            "forbidden": [
                "Inventing a new logo expression or approximate sun symbol",
                "Two-row or sidebar-first website chrome unless the product requirement makes it necessary",
                "Purple gradients, decorative blobs, large uniform radii, or centered generic SaaS feature grids",
                "Giving a non-Ağustos house brand its own chromatic identity color without an explicit governance change",
                "Using signal red as an unrestricted background or decoration",
                "Hard-coding values that already exist in foundations, semantic roles, or recipes",
            ],
            "implementationOrder": [
                "Select a brand and medium.",
                "Apply foundations through semantic roles rather than raw values.",
                "Choose the closest recipe for each composition.",
                "Translate that recipe into native platform structure.",
                "Run the medium adapter's tests plus the acceptance checks in this file.",
            ],
            "mediums": {
                "web": "One-row header, shared frame, editorial hero, restrained bordered groups, short motion.",
                "document": "Native named styles, generous opening space, exact lockup header, thin signal rule, editable tables.",
                "presentation": "Editable 16:9 layouts; red or neutral identity section fields; shared red signals; quiet cream or white content slides.",
            },
            "acceptance": [
                "The selected brand's identity ink, wordmark, and lockup expression match the brand registry.",
                "Links, focus, markers, and small emphasis use shared signal red regardless of selected brand.",
                "Display, body, and mono type roles use the declared families and hierarchy.",
                "Content aligns to one dominant frame or margin system.",
                "Interactive elements have visible focus states and motion respects reduced-motion preferences.",
                "No generated value or adapter has drifted from this contract.",
                "If the referenced logo asset is unavailable, request it instead of recreating it.",
            ],
        },
        "distribution": {
            "primaryArtifact": "tokens/design-system-handoff.json",
            "consumerRule": "Vendor or attach this file as context. Consumer builds read it; they do not run this repository's generators.",
            "regenerationRule": "Regenerate checked-in CSS, Office, and brand assets only when canonical token, brand, template, or symbol sources change.",
        },
        "colorModel": {
            "identity": "Ağustos uses red; every other house brand uses neutral black/white.",
            "interactionSignal": resolved["foundations"]["color"]["signalRed"],
            "rule": "Identity ink names the brand. Signal red communicates action and emphasis across the family.",
        },
        "assets": {
            "symbol": {
                "path": "laz-gunesi-amblem/svg/master.svg",
                "sha256": hashlib.sha256(SYMBOL_SOURCE.read_bytes()).hexdigest(),
                "svg": SYMBOL_SOURCE.read_text(encoding="utf-8"),
                "embeddedColor": resolved["brands"]["agustos"]["color"],
                "usageRule": (
                    "Preserve the embedded path geometry exactly. For Ağustos, use the SVG unchanged. "
                    "For another house brand, replace only the fill color with that brand's registered "
                    "identity ink; never substitute signal red or redraw the paths."
                ),
            },
            "lockupPattern": "brand/exports/<brand>/lockup/<brand>-lockup__positive.svg",
            "negativeLockupPattern": "brand/exports/<brand>/lockup/<brand>-lockup__negative.svg",
        },
        "compatibility": tokens.get("compatibility", {}),
        "system": resolved,
    }


def expected_outputs() -> dict[Path, str]:
    tokens = load_json(TOKEN_SOURCE)
    brands = load_json(BRAND_SOURCE)
    outputs: dict[Path, str] = {}
    for path, label in CSS_OUTPUTS.items():
        outputs[path] = render_web_css(tokens, brands, label)

    resolved = {
        "name": tokens["name"],
        "version": tokens["version"],
        "foundations": resolve_tree(tokens, tokens["foundations"]),
        "semantic": resolve_tree(tokens, tokens["semantic"]),
        "themes": resolve_tree(tokens, tokens["themes"]),
        "recipes": resolve_tree(tokens, tokens["recipes"]),
        "brands": brands["brands"],
        "signal": brands["signal"],
    }
    outputs[ROOT / "tokens" / "resolved.json"] = json.dumps(
        resolved, ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    outputs[ROOT / "tokens" / "design-system-handoff.json"] = json.dumps(
        handoff_contract(resolved, tokens), ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    outputs[ROOT / "adapters" / "wordpress" / "theme.json"] = json.dumps(
        wordpress_theme(tokens, brands), ensure_ascii=False, indent=2
    ) + "\n"

    source_hash = hashlib.sha256(
        TOKEN_SOURCE.read_bytes() + BRAND_SOURCE.read_bytes() + WEB_TEMPLATE.read_bytes() + SYMBOL_SOURCE.read_bytes()
    ).hexdigest()
    manifest = {
        "system": tokens["name"],
        "version": tokens["version"],
        "source_sha256": source_hash,
        "outputs": {
            str(path.relative_to(ROOT)): hashlib.sha256(content.encode("utf-8")).hexdigest()
            for path, content in sorted(outputs.items(), key=lambda item: str(item[0]))
        },
    }
    outputs[ROOT / "tokens" / "generated-manifest.json"] = json.dumps(
        manifest, ensure_ascii=False, indent=2, sort_keys=True
    ) + "\n"
    return outputs


def write_or_check(outputs: dict[Path, str], check: bool) -> int:
    drift: list[str] = []
    for path, content in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        if check:
            drift.append(str(path.relative_to(ROOT)))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"generated {path.relative_to(ROOT)}")
    if drift:
        print("generated design-system drift:", file=sys.stderr)
        for path in drift:
            print(f"  - {path}", file=sys.stderr)
        print("run: python3 scripts/build_design_system.py", file=sys.stderr)
        return 1
    if check:
        print(f"design-system outputs are current ({len(outputs)} files)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed generated outputs differ")
    args = parser.parse_args()
    try:
        return write_or_check(expected_outputs(), args.check)
    except (TokenError, KeyError, json.JSONDecodeError) as error:
        print(f"design-system generation failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
