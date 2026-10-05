#!/usr/bin/env python3
"""Ağustos UI kit compliance checker — v7.9.0

GENERATED. Do not hand-edit. Regenerate with:
    python3 scripts/build_design_system.py

Run it from the root of a project that uses the kit:

    python3 check-agustos-ui.py .

On a site whose layout fills data-screen at render time (Astro, ERB), build the
site, then check the rendered pages for the screen rules:

    python3 check-agustos-ui.py dist --screens-only

Standard library only, Python 3.9+. It reads files; it never writes them, and it
makes no network call unless you pass --update-check.

Exit codes: 0 clean (or warnings only), 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

KIT_VERSION = "7.9.0"
REPOSITORY = "Agustos-Teknoloji/DESIGN-agustos"
LATEST_KIT_URL = "https://cdn.jsdelivr.net/gh/Agustos-Teknoloji/DESIGN-agustos@latest/ui/kit.json"

# hex value -> the variable that owns it. Injected from the token registry, so a
# vendored copy of this file cannot drift from the system it was cut from.
TOKEN_COLORS = {
    "#fdf5f5": "--cream",
    "#ffffff": "--paper",
    "#ebebeb": "--surface",
    "#15130f": "--ink",
    "#404040": "--ink-soft",
    "#8a8378": "--ink-faint",
    "#e8e4da": "--rule",
    "#cf142a": "--signal",
    "#1f6b4a": "--state-success",
    "#8a5a00": "--state-warning",
    "#b42318": "--state-danger",
    "#1a4d8f": "--state-info",
}

KIT_CLASSES = {
    "type-hero",
    "type-hero-md",
    "type-hero-deck",
    "type-h1",
    "type-h2",
    "type-h3",
    "type-h4",
    "type-body",
    "type-link",
    "type-code",
    "type-blockquote",
    "type-pullquote",
    "type-list-ol",
    "type-list-ul",
    "type-dl",
    "type-figure",
    "type-code-block",
    "type-table",
    "type-spec",
    "type-divider",
    "type-footnote",
    "type-highlight",
    "site-frame",
    "container",
    "container--reading",
    "skip-link",
    "brand-agustos",
    "brand-pataraz",
    "brand-pld",
    "brand-iesdesk",
    "brand-specquick",
    "brand-memregunes",
    "brand-banuucak",
    "paper-white",
    "hero-actions",
    "hero-trust",
    "hero-visual",
    "hero-split",
    "hero-split--media-start",
    "hero-split__media",
    "agustos-section",
    "agustos-section__head",
    "agustos-card-grid",
    "agustos-card",
    "agustos-card--marked",
    "agustos-chrome-link",
    "site-lockup",
    "site-lockup__symbol",
    "site-lockup__logo",
    "site-lockup__logo--light",
    "site-lockup__logo--dark",
    "site-lockup__name",
    "site-sidebar-layout",
    "site-sidebar",
    "site-sidebar__nav",
    "site-sidebar__link",
    "site-sidebar__group",
    "site-sidebar__cta",
    "site-sidebar__utility",
    "site-sidebar__note",
    "site-sidebar-bar",
    "site-sidebar-burger",
    "site-sidebar__close",
    "site-header",
    "site-header__bar",
    "site-header__panel",
    "site-header__nav",
    "site-header__link",
    "site-header__more",
    "site-header__more-menu",
    "site-header__more-link",
    "site-header__more-menu--groups",
    "site-header__more-group",
    "site-header__more-group-title",
    "site-header__more--end",
    "site-header__more-label",
    "site-header__end",
    "site-header__cta",
    "site-header__burger",
    "site-header__close",
    "site-header__utility",
    "site-header__utility--bar",
    "site-header__utility--drawer",
    "site-header__icon-btn",
    "site-header__theme-sun",
    "site-header__theme-moon",
    "agustos-theme-switch",
    "agustos-theme-switch__to-dark",
    "agustos-theme-switch__to-light",
    "agustos-theme-switch__label",
    "site-header__lang-link",
    "site-header__search",
    "site-header__search--desktop",
    "site-header__search--responsive",
    "site-header__search-toggle",
    "site-header__search-panel",
    "site-header__search-field",
    "site-header__search-output",
    "site-header__search-status",
    "site-header__search-results",
    "site-header__search-group",
    "site-header__search-heading",
    "site-header__search-heading-count",
    "site-header__search-list",
    "site-header__search-result",
    "site-header__search-result-title",
    "site-header__search-result-excerpt",
    "site-header__search-row",
    "site-header__search-shell",
    "site-header__noscript-search",
    "site-footer",
    "site-footer__inner",
    "site-footer__brand",
    "site-footer__links",
    "site-footer__link",
    "site-footer__map",
    "site-footer__contact",
    "site-footer__groups",
    "site-footer__group",
    "site-footer__group-title",
    "site-footer__group-links",
    "breadcrumb",
    "breadcrumb__link",
    "stack",
    "cluster",
    "grid-2",
    "grid-3",
    "grid-4",
    "grid-aside",
    "band",
    "band--cream",
    "table-scroll",
    "prose",
    "agustos-fieldset",
    "agustos-field",
    "agustos-field--invalid",
    "agustos-label",
    "agustos-label--required",
    "agustos-input",
    "agustos-textarea",
    "agustos-select",
    "agustos-check",
    "agustos-hint",
    "agustos-error",
    "agustos-button",
    "agustos-button--primary",
    "agustos-button--secondary",
    "agustos-button--quiet",
    "agustos-badge",
    "agustos-badge--success",
    "agustos-badge--warning",
    "agustos-badge--danger",
    "agustos-badge--info",
    "agustos-badge--signal",
    "agustos-notice",
    "agustos-notice__title",
    "agustos-notice--success",
    "agustos-notice--warning",
    "agustos-notice--danger",
    "agustos-notice--info",
    "agustos-tabs",
    "agustos-tab",
    "agustos-tabs__panel",
    "agustos-contents",
    "agustos-contents__toggle",
    "agustos-contents__title",
    "agustos-contents__list",
    "agustos-contents__link",
}

# screen name -> the rules a page under that screen should meet. Injected from the
# screens table for the same reason as TOKEN_COLORS. A page names its screen with
# data-screen on <body>; chrome "sidebar" marks the product sidebar; every screen starts light;
# highlight "one" marks the homepage, which carries the one highlighter stroke.
# The checker guards identity with errors. Taste rules only warn.
SCREENS = {'app-shell': {'theme': 'light-first', 'chrome': 'sidebar', 'column': 'frame', 'highlight': 'at-most-one'}, 'app-top-menu': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'frame', 'highlight': 'at-most-one'}, 'content': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'reading', 'highlight': 'at-most-one'}, 'content-index': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'reading', 'highlight': 'at-most-one'}, 'home': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'frame', 'highlight': 'one'}, 'product': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'frame', 'highlight': 'at-most-one'}, 'product-finder': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'frame', 'highlight': 'at-most-one'}, 'products': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'frame', 'highlight': 'at-most-one'}, 'spec-sheet': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'frame', 'highlight': 'at-most-one'}, 'static': {'theme': 'light-first', 'chrome': 'topbar', 'column': 'reading', 'highlight': 'at-most-one'}}

# #15130f and #ffffff are legitimate as identity ink and as paper. Reported at
# warning level rather than error: too common to fail a build over.
SOFT_COLORS = {"#15130f", "#ffffff"}

STALE_RED = "#d11d2b"
SIGNAL_RED = "#cf142a"
BRAND_CLASSES = ('brand-agustos', 'brand-pataraz', 'brand-pld', 'brand-iesdesk', 'brand-specquick', 'brand-memregunes', 'brand-banuucak', 'brand-heper', 'brand-ligman')

# The kit's own files. agustos.css declares the tokens, and the docs quote them
# on purpose — policing either produces noise, not findings.
KIT_FILES = {
    "agustos.css", "agustos-fonts.css", "starter.html", "kit.json",
    "UI-KIT.md", "AGENTS-SNIPPET.md", "check-agustos-ui.py", "LICENSE",
}

SCAN_SUFFIXES = {
    ".html", ".htm", ".css", ".scss", ".sass", ".astro", ".erb", ".php",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".liquid", ".md",
}
SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", ".astro", ".next", ".cache",
    "vendor", "__pycache__", ".venv", "venv", "coverage",
}

# --screens-only reads built output: rendered pages, nothing else.
RENDERED_SUFFIXES = {".html", ".htm"}

HEX = re.compile(r"#([0-9a-fA-F]{6})\b")
# Page files: anything that can carry a <body>. Partials without one are skipped.
PAGE_SUFFIXES = {".html", ".htm", ".astro", ".erb", ".php", ".liquid", ".vue", ".svelte"}
# Comments, scripts and styles are not markup. Astro inlines a small processed
# script, agustos-chrome.js among them, and its selectors name kit classes.
NOT_MARKUP = re.compile(r"<!--.*?-->|<script\b[^>]*>.*?</script\s*>|<style\b[^>]*>.*?</style\s*>", re.S | re.I)
BODY_TAG = re.compile(r"<body\b([^>]*)>", re.I)
REDIRECT = re.compile(r"<meta\b[^>]*http-equiv\s*=\s*[\"']?refresh", re.I)
DATA_SCREEN = re.compile(r"""data-screen\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
BODY_CLASS = re.compile(r"""\bclass\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
TEMPLATED = re.compile(r"[{<$]")
MAIN_BLOCK = re.compile(r"<main\b.*?</main>", re.S | re.I)
HIGHLIGHT = re.compile(r"\btype-highlight\b")
SIDEBAR = re.compile(r"\bsite-sidebar\b")
# One top-menu item: a site-header__link inside site-header__nav, the More
# toggle included. Items inside More are site-header__more-link and do not
# count; an account list in site-header__end does not count (v7.7.0).
TOP_MENU_ITEM = re.compile(r"""class=["'][^"']*\bsite-header__link\b""")
# The inside of a start tag: a quoted value, an ERB or PHP tag, or any other
# character but a bracket. A template tag may hold ">" (`<%= t(:menu) %>`).
IN_TAG = r"""(?:[^<>"']|"[^"]*"|'[^']*'|<%(?:[^%]|%(?!>))*%>|<\?(?:[^?]|\?(?!>))*\?>)"""
TOP_MENU_NAV = re.compile(
    r"<nav\b" + IN_TAG + r"""*?\bclass\s*=\s*["'][^"']*\bsite-header__nav(?![\w-])[^"']*["']"""
    + IN_TAG + r"*>.*?</nav\s*>", re.S | re.I)
TOP_MENU_LIMIT = 5
# A grouped More holds at most two groups; a third goes past the page edge at 1024px.
MORE_OPEN = re.compile(r"""<details\b[^>]*\bclass\s*=\s*["'][^"']*\bsite-header__more(?![\w-])""", re.I)
DETAILS_END = re.compile(r"</details\s*>", re.I)
MORE_GROUP_LIMIT = 2
# A link start tag and its attributes, for the aria-current check on built pages.
LINK_TAG = re.compile(r"<a\b[^>]*>", re.I)
LINK_ATTRIBUTE = re.compile(r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""")
# A page that is served dark. Only the user's theme switch may set dark, at run time.
HTML_DARK = re.compile(r"<html\b" + IN_TAG + r"""*?\bdata-theme\s*=\s*["']?dark(?![\w-])""", re.S | re.I)
DEVICE_THEME = "prefers-color-scheme"
# The theme switch keeps the user's choice under this key. The kit head script
# reads it and applies a dark choice before the first paint, so it must sit in
# <head> before the first stylesheet. A quoted attribute value may hold a
# template tag, such as nonce="<%= content_security_policy_nonce %>".
THEME_STORAGE_KEY = "agustos:theme"
THEME_SWITCH = re.compile(r"\bdata-agustos-theme\b")
COMMENT = re.compile(r"<!--.*?-->", re.S)
SCRIPT_BLOCK = re.compile(r"""<script\b(?:[^>"']|"[^"]*"|'[^']*')*>(.*?)</script\s*>""", re.S | re.I)
STYLESHEET = re.compile(r"""<link\b(?:[^>"']|"[^"]*"|'[^']*')*?\brel\s*=\s*["']?stylesheet\b|\bstylesheet_link_tag\b""", re.I)
# A Rails javascript_tag, one line or a do ... end block. It counts as the head
# script when it names THEME_SCRIPT or holds the storage key.
JAVASCRIPT_TAG = re.compile(r"<%=\s*javascript_tag\b((?:[^%]|%(?!>))*)%>", re.S)
ERB_END = re.compile(r"<%-?\s*end\s*-?%>")
HEAD_END = re.compile(r"</head\s*>", re.I)
# agustos-chrome.js or agustos/chrome.js, a quoted asset name such as
# javascript_include_tag "agustos-chrome" or import "agustos/chrome", or the
# script inlined by a build (its guard property). A class such as
# agustos-chrome-link is not the script.
CHROME_SCRIPT = re.compile(r"""\bagustos[-/]chrome(?:\.[\w-]+)*\.js\b|["']agustos[-/]chrome["']|\bagustosChrome\b""")
IMPORTMAP_TAGS = re.compile(r"\bjavascript_importmap_tags\b")
ERB_COMMENT = re.compile(r"<%#.*?%>", re.S)
CLASS_ATTRIBUTE = re.compile(r"""\bclass\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
RADIUS = re.compile(r"border-radius:\s*([0-9.]+)px")
GRADIENT = re.compile(r"(linear|radial|conic)-gradient\(")
BACKGROUND = re.compile(r"background(?:-color)?:\s*([^;{}]+)")
# A pseudo-element, or an explicit dimension of 16px or less, means the signal is
# painting a marker rather than a field.
MARKER = re.compile(r"::(?:before|after)|(?:width|height)\s*:\s*(?:[0-9]|1[0-6])px")
# `linear-gradient(var(--rule) 1px, transparent 1px)` draws a rule, not a wash.
HAIRLINE_GRID = re.compile(r"[123]px\s*,\s*transparent")
# Anchor on a rule or declaration boundary, not line start: `:root { --ink: … }`
# on one line is ordinary CSS and must still be caught.
CUSTOM_PROP = re.compile(r"(?:^|[;{])\s*(--(?:display|body|ink|paper|signal|brand|rule))\s*:", re.MULTILINE)
JSDELIVR = re.compile(r"cdn\.jsdelivr\.net/gh/" + re.escape(REPOSITORY) + r"(@[^/\s\"']*)?")
FONT_HINTS = (
    "agustos-fonts.css", "fontsource", "Inter+Tight", "InterTight",
    "@font-face", "inter-tight-variable",
)


class Finding:
    __slots__ = ("rule", "level", "path", "line", "message")

    def __init__(self, rule, level, path, line, message):
        self.rule, self.level, self.path, self.line, self.message = rule, level, path, line, message

    def render(self) -> str:
        where = f"{self.path}:{self.line}" if self.path else "—"
        return f"{self.level.upper():<5} {self.rule} {where:<44} {self.message}"

    def as_dict(self) -> dict:
        return {
            "rule": self.rule, "level": self.level,
            "file": self.path, "line": self.line, "message": self.message,
        }


def near(first: str, second: str) -> int:
    """Squared-ish RGB distance. Catches hand-typed near-misses."""
    a = [int(first[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(second[i:i + 2], 16) for i in (1, 3, 5)]
    return max(abs(x - y) for x, y in zip(a, b))


def scan_files(root: Path, skip_dirs: frozenset[str] = frozenset(SKIP_DIRS), suffixes=SCAN_SUFFIXES):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        # Folders below the root only: a project that lives in a folder named
        # dist or build is still scanned.
        if any(part in skip_dirs for part in path.relative_to(root).parent.parts):
            continue
        if path.name in KIT_FILES:
            continue
        try:
            yield path, path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def line_of(text: str, index: int) -> int:
    return text[:index].count("\n") + 1


def markup(text: str) -> str:
    """The page with comments, scripts and styles blanked. Newlines and offsets
    stay, so the start of a match gives its line in the page as written."""
    return NOT_MARKUP.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), text)


# The kit stretches a link that is a direct child of one of these headings
# over its card, so the card becomes the 44px target.
CARD_HEADINGS = {"h2", "h3", "h4"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class CardScan(HTMLParser):
    """Finds every .agustos-card that has links but none in its heading."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list = []     # open tags as [name, card]; card is a dict or None
        self.stranded: list = []  # start lines of those cards

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        classes = (dict(attrs).get("class") or "").split()
        if tag == "a":
            card = next((entry[1] for entry in reversed(self.stack) if entry[1]), None)
            if card:
                card["links"] += 1
                if self.stack[-1][0] in CARD_HEADINGS:
                    card["heading_link"] = True
        card = {"line": self.getpos()[0], "links": 0, "heading_link": False} if "agustos-card" in classes else None
        self.stack.append([tag, card])

    def handle_startendtag(self, tag, attrs):
        pass  # a self-closing tag holds nothing

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self._settle(self.stack[index:])
                del self.stack[index:]
                return

    def finish(self) -> list:
        self.close()
        self._settle(self.stack)
        self.stack = []
        return sorted(self.stranded)

    def _settle(self, entries) -> None:
        for _name, card in entries:
            if card and card["links"] and not card["heading_link"]:
                self.stranded.append(card["line"])


# Start tags that close an open <p>, as a browser does (HTML "p" end tag
# omission). A page may leave its <p> open before the next block.
P_CLOSERS = {
    "address", "article", "aside", "blockquote", "details", "div", "dl", "fieldset",
    "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6",
    "header", "hgroup", "hr", "main", "menu", "nav", "ol", "p", "pre", "section",
    "table", "ul",
}


class ContentsScan(HTMLParser):
    """Finds each .agustos-contents whose parent is not .container--reading. The
    list takes the side zone from that parent, so anywhere else it lands wrong.
    It reads full pages only: a partial or a component has no parent to check,
    so a site that draws the list from one needs its own page test."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list = []      # open tags as (name, classes)
        self.misplaced: list = []  # start lines of misplaced lists

    def handle_starttag(self, tag, attrs):
        if tag in P_CLOSERS and self.stack and self.stack[-1][0] == "p":
            self.stack.pop()
        if tag in VOID_TAGS:
            return
        classes = (dict(attrs).get("class") or "").split()
        if "agustos-contents" in classes and not (self.stack and "container--reading" in self.stack[-1][1]):
            self.misplaced.append(self.getpos()[0])
        self.stack.append((tag, classes))

    def handle_startendtag(self, tag, attrs):
        pass  # a self-closing tag holds nothing

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                return


def check_cards(rel: str, text: str, findings: list) -> None:
    scan = CardScan()
    try:
        scan.feed(text)
        lines = scan.finish()
    except Exception:
        return  # a template the parser cannot read; the other rules still run
    for number in lines:
        findings.append(Finding(
            "AG013", "warn", rel, number,
            "card has links but none sits in its heading — put the card's main link "
            "directly in an h2, h3 or h4 so the whole card becomes the 44px target",
        ))


def check_screen(rel: str, text: str, findings: list) -> None:
    """The per-screen rules. They read markup only: a header note that mentions
    <body>, a commented-out button or a selector in an inline script does not count."""
    page = markup(text)
    body = BODY_TAG.search(page)
    if not body:
        return
    if REDIRECT.search(page[:body.start()]):
        return  # a redirect stub, such as the one Astro writes, is not a screen
    body_line = line_of(page, body.start())
    attribute = DATA_SCREEN.search(body.group(1))
    if not attribute:
        findings.append(Finding(
            "AG020", "error", rel, body_line,
            "page names no screen — put data-screen=\"<name>\" on <body>; "
            "names: " + ", ".join(SCREENS),
        ))
        return
    name = next(group for group in attribute.groups() if group is not None)
    if TEMPLATED.search(name):
        return  # a layout fills the name at render time; check the rendered pages
    rules = SCREENS.get(name)
    if rules is None:
        findings.append(Finding(
            "AG021", "error", rel, body_line,
            f"unknown screen {name!r} — the screens table knows: " + ", ".join(SCREENS),
        ))
        return
    highlights = list(HIGHLIGHT.finditer(page))
    if len(highlights) > 1:
        findings.append(Finding(
            "AG025", "warn", rel, line_of(page, highlights[1].start()),
            f"{len(highlights)} highlighter strokes on one page — use one, on a few words "
            f"of the main headline",
        ))
    if not highlights and rules["highlight"] == "one":
        findings.append(Finding(
            "AG032", "warn", rel, body_line,
            f"no highlighter on screen {name!r} — wrap one to four words of the main "
            f"headline in <mark class=\"type-highlight\">",
        ))
    sidebar = SIDEBAR.search(page)
    if sidebar and rules["chrome"] != "sidebar":
        findings.append(Finding(
            "AG026", "warn", rel, line_of(page, sidebar.start()),
            f"sidebar on screen {name!r}, whose chrome is the top menu: use site-header, "
            f"or the app-shell screen for a product sidebar",
        ))
    navs = list(TOP_MENU_NAV.finditer(page))
    scope = [(nav.start(), nav.group(0)) for nav in navs] or [(0, page)]
    menu_items = [(offset + match.start()) for offset, block in scope for match in TOP_MENU_ITEM.finditer(block)]
    if len(menu_items) > TOP_MENU_LIMIT:
        findings.append(Finding(
            "AG027", "warn", rel, line_of(page, menu_items[TOP_MENU_LIMIT]),
            f"{len(menu_items)} items in site-header__nav: keep at most {TOP_MENU_LIMIT}, the More "
            f"toggle included; put the rest in one site-header__more",
        ))
    if rules["column"] == "reading":
        for match in CLASS_ATTRIBUTE.finditer(page):
            names = (match.group(1) or match.group(2) or "").split()
            if "container" in names and "container--reading" not in names:
                findings.append(Finding(
                    "AG028", "warn", rel, line_of(page, match.start()),
                    f"full-width container on screen {name!r}: a content page stops its "
                    f"text at the reading line: add container--reading",
                ))
                break
    contents = ContentsScan()
    try:
        contents.feed(text)
        contents.close()
    except Exception:
        contents.misplaced = []  # a template the parser cannot read; the other rules still run
    for number in contents.misplaced:
        findings.append(Finding(
            "AG031", "warn", rel, number,
            "agustos-contents is not a direct child of container--reading: put the list "
            "directly in the page's reading container, so it can take the side zone",
        ))
    dark = HTML_DARK.search(page)
    if dark:
        findings.append(Finding(
            "AG024", "warn", rel, line_of(page, dark.start()),
            "the page starts dark (data-theme=\"dark\" on <html>): every page starts light, "
            "and only the user's theme switch sets dark",
        ))


def theme_script_in(source: str, limit: int) -> bool:
    """True when the source holds the kit head script before offset limit: in a
    <script> block, or in a Rails javascript_tag."""
    if any(THEME_STORAGE_KEY in match.group(1) for match in SCRIPT_BLOCK.finditer(source, 0, limit)):
        return True
    for tag in JAVASCRIPT_TAG.finditer(source, 0, limit):
        arguments = tag.group(1)
        if re.search(r"\bTHEME_SCRIPT\b", arguments) or THEME_STORAGE_KEY in arguments:
            return True
        if arguments.rstrip().endswith("do"):
            end = ERB_END.search(source, tag.end(), limit)
            if end and THEME_STORAGE_KEY in source[tag.end():end.start()]:
                return True
    return False


def check_theme_script(rel: str, text: str, findings: list) -> None:
    """A full page with a theme switch also needs the kit head script in <head>,
    before the first stylesheet. Without it, each new page shows light before it
    turns dark. It reads full pages only: a partial has no <body>, and its layout
    does not show the switch, so a site that renders the switch from a partial
    needs its own page test."""
    page = markup(text)
    body = BODY_TAG.search(page)
    if not body or REDIRECT.search(page[:body.start()]):
        return
    switch = THEME_SWITCH.search(page)
    if not switch:
        return
    head = HEAD_END.search(page, 0, body.start())
    limit = head.start() if head else body.start()
    stylesheet = STYLESHEET.search(page, 0, limit)
    if stylesheet:
        limit = stylesheet.start()
    source = COMMENT.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), text)
    if theme_script_in(source, limit):
        return
    findings.append(Finding(
        "AG034", "warn", rel, line_of(page, switch.start()),
        "theme switch without the kit head script before the stylesheets: put the "
        "themeScript of kit.json in <head>, after the viewport meta, or a dark choice "
        "shows light first on each new page",
    ))


def check_chrome_script(rel: str, text: str, imports_chrome: bool, findings: list) -> None:
    """Only agustos-chrome.js flips the theme. A full page with a theme switch
    that does not load it shows a switch that does nothing. A layout that loads
    the Rails import map passes when a project script imports agustos/chrome.
    Like AG034 it reads full pages only, and the source only: built output
    bundles the script under a hashed name."""
    page = markup(text)
    body = BODY_TAG.search(page)
    if not body or REDIRECT.search(page[:body.start()]):
        return
    switch = THEME_SWITCH.search(page)
    if not switch:
        return
    source = ERB_COMMENT.sub(" ", COMMENT.sub(" ", text))
    if CHROME_SCRIPT.search(source) or (imports_chrome and IMPORTMAP_TAGS.search(source)):
        return
    findings.append(Finding(
        "AG036", "warn", rel, line_of(page, switch.start()),
        "theme switch on a page that does not load agustos-chrome.js: load it once "
        "with defer, or the switch does nothing",
    ))


def check_more_groups(rel: str, text: str, findings: list) -> None:
    """A grouped More holds at most two groups. Each group is at least 200px
    wide, so a third group pushes the menu past the right edge of the page at
    1024px and 1280px. It reads partials too, because a header is often one."""
    page = markup(text)
    for more in MORE_OPEN.finditer(page):
        end = DETAILS_END.search(page, more.end())
        stop = end.start() if end else len(page)
        groups = [match for match in CLASS_ATTRIBUTE.finditer(page, more.end(), stop)
                  if "site-header__more-group" in (match.group(1) or match.group(2) or "").split()]
        if len(groups) > MORE_GROUP_LIMIT:
            findings.append(Finding(
                "AG035", "warn", rel, line_of(page, groups[MORE_GROUP_LIMIT].start()),
                f"{len(groups)} groups in one site-header__more: keep at most "
                f"{MORE_GROUP_LIMIT}. A third group goes past the edge of the page at 1024px",
            ))


def url_path(path: str) -> str:
    """A site path without query, fragment, index.html, .html or trailing slash."""
    path = re.sub(r"[?#].*", "", path)
    path = re.sub(r"(^|/)index\.html?$", r"\1", path)
    path = re.sub(r"\.html?$", "", path)
    return "/" + path.strip("/") if path.strip("/") else "/"


def check_current_links(rel: str, posix: str, text: str, findings: list) -> None:
    """Built output only: the file path is the page's own URL there. A link
    marked aria-current="page" that points to a section above the page (or to
    home from a nested page) makes a screen reader announce the parent as the
    current page. The section takes aria-current="true"."""
    page = markup(text)
    body = BODY_TAG.search(page)
    if not body or REDIRECT.search(page[:body.start()]):
        return
    here = url_path(posix)
    for tag in LINK_TAG.finditer(page):
        attrs = {name.lower(): next((v for v in values if v), "")
                 for name, *values in LINK_ATTRIBUTE.findall(tag.group(0))}
        href = attrs.get("href", "")
        if attrs.get("aria-current", "").lower() != "page" or not href.startswith("/") or href.startswith("//"):
            continue
        target = url_path(href)
        if target != here and (target == "/" or here.startswith(target + "/")):
            findings.append(Finding(
                "AG029", "warn", rel, line_of(page, tag.start()),
                f'aria-current="page" on a link to {href}, a section above this page ({here}): '
                f'use aria-current="true" for the section; "page" belongs to the page itself',
            ))


def check_disabled_links(rel: str, text: str, findings: list) -> None:
    """aria-disabled only tells a screen reader; it does not stop a link. A
    disabled link that keeps its href still opens on a click or Enter. Drop the
    href and add role="link", so the link is inert and still announced."""
    page = markup(text)
    for tag in LINK_TAG.finditer(page):
        attrs = {name.lower(): next((v for v in values if v), "")
                 for name, *values in LINK_ATTRIBUTE.findall(tag.group(0))}
        if attrs.get("aria-disabled", "").lower() == "true" and "href" in attrs:
            findings.append(Finding(
                "AG030", "warn", rel, line_of(page, tag.start()),
                'a link with aria-disabled="true" keeps its href, so it still opens: '
                'drop the href and add role="link"',
            ))


def check(root: Path, skip_dirs=(), screens_only=False) -> tuple[list, int]:
    findings: list = []
    scanned = 0
    corpus: list = []
    pages: list = []  # (rel, text) of each page file, for AG036
    suffixes = RENDERED_SUFFIXES if screens_only else SCAN_SUFFIXES

    for path, text in scan_files(root, frozenset(SKIP_DIRS) | frozenset(skip_dirs), suffixes):
        scanned += 1
        rel = str(path.relative_to(root))
        if screens_only:
            check_screen(rel, text, findings)
            check_theme_script(rel, text, findings)
            check_more_groups(rel, text, findings)
            check_current_links(rel, path.relative_to(root).as_posix(), text, findings)
            check_disabled_links(rel, text, findings)
            continue
        corpus.append(text)
        lines = text.splitlines()

        # Documentation legitimately quotes token values — that is its job. Only
        # the two rules that stay wrong in prose apply to Markdown: a stale red,
        # and an unpinned URL that teaches the reader a bad habit.
        prose = path.suffix.lower() == ".md"

        for number, line in enumerate(lines, 1):
            lowered = line.lower()

            if STALE_RED in lowered:
                findings.append(Finding(
                    "AG001", "error", rel, number,
                    f"stale brand red {STALE_RED} — brand red is {SIGNAL_RED}",
                ))

            for match in (() if prose else HEX.finditer(line)):
                value = "#" + match.group(1).lower()
                if value == STALE_RED:
                    continue
                owner = TOKEN_COLORS.get(value)
                if owner and value in SOFT_COLORS:
                    findings.append(Finding(
                        "AG003", "warn", rel, number,
                        f"{value} is a token value ({owner}); legitimate as identity ink, "
                        f"suspicious as a page color",
                    ))
                elif owner:
                    findings.append(Finding(
                        "AG002", "error", rel, number,
                        f"hardcoded {value} — use var({owner})",
                    ))
                else:
                    for token, name in TOKEN_COLORS.items():
                        if token not in SOFT_COLORS and near(value, token) <= 12:
                            findings.append(Finding(
                                "AG004", "warn", rel, number,
                                f"{value} is a near-miss for {token} — did you mean var({name})?",
                            ))
                            break

            for match in (() if prose else RADIUS.finditer(line)):
                if float(match.group(1)) > 12:
                    findings.append(Finding(
                        "AG010", "warn", rel, number,
                        f"border-radius: {match.group(1)}px exceeds the 12px system maximum",
                    ))

            if GRADIENT.search(line) and not prose and not HAIRLINE_GRID.search(line):
                findings.append(Finding(
                    "AG010", "warn", rel, number,
                    "gradients are on the forbidden list for this system",
                ))

            if not prose and DEVICE_THEME in lowered:
                findings.append(Finding(
                    "AG033", "warn", rel, number,
                    "prefers-color-scheme: the user chooses the theme with a switch, never the device",
                ))

            for match in (() if prose else BACKGROUND.finditer(line)):
                value = match.group(1)
                if SIGNAL_RED not in value.lower() and "var(--signal)" not in value:
                    continue
                if re.search(r"var\(--signal\)\s+([0-9]|10)%", value):
                    continue  # a tint inside color-mix, not a red field
                if MARKER.search(line):
                    continue  # a marker dot or rule bar — what signal red is for
                findings.append(Finding(
                    "AG011", "warn", rel, number,
                    "signal red is for the logo, links, focus, markers and the one highlighter — "
                    "not a background or a button",
                ))

            for match in JSDELIVR.finditer(line):
                pin = match.group(1) or ""
                if not re.fullmatch(r"@v\d+\.\d+\.\d+", pin):
                    findings.append(Finding(
                        "AG008", "error", rel, number,
                        f"unpinned kit URL ('{pin or 'no version'}') — pin it to @v{KIT_VERSION}; "
                        f"an unpinned link restyles this page without review",
                    ))

        if path.suffix.lower() in PAGE_SUFFIXES:
            pages.append((rel, text))
            check_screen(rel, text, findings)
            check_theme_script(rel, text, findings)
            check_more_groups(rel, text, findings)
            check_cards(rel, text, findings)
            check_disabled_links(rel, text, findings)

        if path.suffix.lower() in {".css", ".scss", ".sass"}:
            for match in CUSTOM_PROP.finditer(text):
                number = text[:match.start()].count("\n") + 1
                findings.append(Finding(
                    "AG012", "warn", rel, number,
                    f"redefining {match.group(1)} collides with the kit's own variable",
                ))
            for name in KIT_CLASSES:
                pattern = re.compile(r"^[^@\n]*\." + re.escape(name) + r"(?![\w-])[^\n{]*\{", re.MULTILINE)
                match = pattern.search(text)
                if match:
                    number = text[:match.start()].count("\n") + 1
                    findings.append(Finding(
                        "AG009", "warn", rel, number,
                        f"restyling .{name} — compose a new class instead of overriding the kit",
                    ))
                    break

    if screens_only:
        # Built output bundles the kit under hashed names, so the project-wide
        # rules below would report false findings. The source scan covers them.
        return findings, scanned

    blob = "\n".join(corpus)
    imports_chrome = bool(re.search(r"""\bimport\s+["']agustos/chrome["']""", blob))
    for rel, text in pages:
        check_chrome_script(rel, text, imports_chrome, findings)

    if scanned and "agustos.css" not in blob:
        findings.append(Finding(
            "AG006", "error", "", 0,
            "agustos.css is never referenced — the project does not load the design system",
        ))
    if scanned and not any(hint in blob for hint in FONT_HINTS):
        findings.append(Finding(
            "AG005", "error", "", 0,
            "Inter Tight is in the font stack but never loaded — the page will render in "
            "system sans. Load agustos-fonts.css, or the @fontsource-variable packages",
        ))
    if scanned and not any(name in blob for name in BRAND_CLASSES):
        findings.append(Finding(
            "AG007", "error", "", 0,
            "no brand class found — <body> must carry one of: " + ", ".join(BRAND_CLASSES),
        ))

    return findings, scanned


def fetch_latest() -> str:
    import urllib.request
    with urllib.request.urlopen(LATEST_KIT_URL, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))["version"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a project against the Ağustos UI kit.")
    parser.add_argument("path", nargs="?", default=".", help="directory to scan (default: .)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", action="store_true", dest="as_json", help="machine-readable output")
    parser.add_argument("--update-check", action="store_true", help="ask the CDN for a newer kit")
    parser.add_argument(
        "--skip", action="append", default=[], metavar="DIR",
        help="directory name to leave out of the scan, for frozen or generated files; repeatable",
    )
    parser.add_argument(
        "--screens-only", action="store_true",
        help="run only the screen rules, on the rendered .html pages of a built site (such as dist/)",
    )
    parser.add_argument("--version", action="version", version=f"agustos-ui-kit {KIT_VERSION}")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    if args.update_check:
        try:
            latest = fetch_latest()
        except Exception as error:
            print(f"update check failed: {error}", file=sys.stderr)
            return 2
        if latest == KIT_VERSION:
            print(f"kit v{KIT_VERSION} is current")
        else:
            print(f"kit v{KIT_VERSION} -> v{latest} available")
            print(f"  https://github.com/{REPOSITORY}/releases/tag/v{latest}")
        return 0

    findings, scanned = check(root, args.skip, args.screens_only)
    if scanned == 0:
        # "clean" after scanning nothing is the most dangerous output this tool
        # could produce. Point it at a real project directory.
        if args.screens_only:
            print(f"no rendered .html pages under {root}, so nothing was checked. "
                  f"Build the site first", file=sys.stderr)
        else:
            print(f"no scannable files under {root} — nothing was checked", file=sys.stderr)
        return 2
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warn"]

    if args.as_json:
        print(json.dumps({
            "kitVersion": KIT_VERSION,
            "filesScanned": scanned,
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": [f.as_dict() for f in findings],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"agustos-ui check · kit v{KIT_VERSION} · {scanned} files scanned")
        for finding in errors + warnings:
            print(finding.render())
        if not findings:
            print("clean")
        else:
            print(f"{len(errors)} error(s), {len(warnings)} warning(s)")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
