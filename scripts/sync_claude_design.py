#!/usr/bin/env python3
"""Keep the Claude Design project "Ağustos" in step with this repository.

The repository owns the rules: tokens, the generated kit, fonts, the symbol,
the favicon, the lockups. `build` packs them into dist/claude-design/agustos-ui/
so Claude can push that folder into the Design project with the DesignSync tool,
and one card per screen.

The Design project owns the drawings: page compositions and explorations.
`pull` copies one page subtree, plus the shared runtime it needs, into
screens/design/ as a reference. Nothing in the kit imports it.

This script never talks to the network. Claude makes the DesignSync calls,
following .claude/skills/design-push/SKILL.md and .claude/skills/design-pull/SKILL.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from datetime import date
from pathlib import Path
from typing import NamedTuple


ROOT = Path(__file__).resolve().parents[1]
LOCKUP_GLOB = "*/lockup/*.svg"
DIST_DIR = ROOT / "dist" / "claude-design"

SYSTEM_NAME = "Ağustos Design System"
SOURCE_REPO = "Agustos-Teknoloji/DESIGN-agustos"
REMOTE_PREFIX = "agustos-ui"
PROJECT_ID = "7fee69d5-01ee-4727-beaf-cb6c5bd923c4"
PROJECT_URL = f"https://claude.ai/design/p/{PROJECT_ID}"


# --- Bundle -----------------------------------------------------------------


def version(root: Path = ROOT) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def kit_files(root: Path = ROOT) -> list[Path]:
    """Every shipped kit file. Templates stay in the factory."""
    files: list[Path] = []
    for path in sorted((root / "ui").rglob("*")):
        if path.is_file() and path.suffix != ".tmpl":
            files.append(path)
    return files


def lockup_svgs(root: Path = ROOT) -> list[Path]:
    return sorted((root / "brand" / "exports").glob(LOCKUP_GLOB))


def favicon_files(root: Path = ROOT) -> list[Path]:
    folder = root / "laz-gunesi-amblem" / "favicon"
    return sorted(p for p in folder.iterdir() if p.is_file() and p.name != "README.md")


def bundle_members(root: Path = ROOT) -> list[tuple[str, bytes]]:
    """(path under agustos-ui/, payload) for the kit, logos, and favicon."""
    members: list[tuple[str, bytes]] = []
    ui_dir = root / "ui"
    for path in kit_files(root):
        members.append((path.relative_to(ui_dir).as_posix(), path.read_bytes()))
    for path in lockup_svgs(root):
        members.append((f"logos/{path.name}", path.read_bytes()))
    for path in favicon_files(root):
        members.append((f"favicon/{path.name}", path.read_bytes()))
    return members


def manifest(members: list[tuple[str, bytes]], version: str, commit: str) -> dict:
    """Hashes for every bundled file, so a later push can diff without reading remote content."""
    files = {
        name: {"bytes": len(payload), "sha256": sha256(payload)}
        for name, payload in sorted(members)
    }
    return {
        "system": SYSTEM_NAME,
        "source": SOURCE_REPO,
        "version": version,
        "commit": commit,
        "remotePrefix": REMOTE_PREFIX,
        "files": files,
    }


# --- Cards ------------------------------------------------------------------
# Each card is one full HTML document. Line 1 is the @dsCard marker the Design
# System pane indexes. Cards load the pushed kit by relative path, fonts first.


class Card(NamedTuple):
    slug: str
    group: str
    width: int
    height: int
    name: str
    subtitle: str
    body: str
    body_class: str = "brand-agustos paper-white"


HOUSE_BRANDS = ("agustos", "pataraz", "pld", "iesdesk", "specquick")

CARDS: tuple[Card, ...] = (
    Card(
        "type",
        "Type",
        700,
        300,
        "Type scale",
        "Inter Tight display · Inter body · JetBrains Mono code",
        """
<p class="type-hero-md">Light, placed with intent.</p>
<h2 class="type-h2">Headings weigh 300 to 400</h2>
<p class="type-body">Body is Inter at a 65ch measure. <a class="type-link" href="#">A content link</a> carries the red rule. Code is <code class="type-code">JetBrains Mono</code>.</p>
""",
    ),
    Card(
        "colours",
        "Colours",
        700,
        170,
        "Six colours",
        "White paper · cream band · light gray · dark gray · off-black · red",
        """
<div class="agustos-card-grid" style="grid-template-columns: repeat(6, 1fr)">
  <div class="agustos-card" style="background: var(--paper-white)"><p class="type-h4">white</p></div>
  <div class="agustos-card" style="background: var(--cream)"><p class="type-h4">cream</p></div>
  <div class="agustos-card" style="background: var(--surface)"><p class="type-h4">light gray</p></div>
  <div class="agustos-card" style="background: var(--ink-soft); color: var(--paper-white)"><p class="type-h4">dark gray</p></div>
  <div class="agustos-card" style="background: var(--ink); color: var(--paper-white)"><p class="type-h4">off-black</p></div>
  <div class="agustos-card" style="background: var(--signal); color: var(--paper-white)"><p class="type-h4">red</p></div>
</div>
""",
    ),
    Card(
        "actions",
        "Actions",
        700,
        200,
        "Action tiers",
        "Primary · secondary · quiet · content link — one 44px size",
        """
<div class="hero-actions">
  <a class="agustos-button agustos-button--primary" href="#">Request pricing</a>
  <a class="agustos-button agustos-button--secondary" href="#">See products</a>
  <a class="agustos-button agustos-button--quiet" href="#">Contact</a>
</div>
<p class="type-body">Inline, <a class="type-link" href="#">a content link</a> keeps the red rule.</p>
""",
    ),
    Card(
        "brand-marks",
        "Brand",
        700,
        260,
        "House lockups",
        "One symbol · lowercase wordmark · only ağustos is red",
        "\n".join(
            f'<p><img src="../logos/{slug}-lockup__positive.svg" alt="{slug} lockup" style="height: 40px"></p>'
            for slug in HOUSE_BRANDS
        ),
    ),
    Card(
        "favicon",
        "Brand",
        700,
        150,
        "Shared favicon",
        "One red Laz Güneşi tab icon for every house site",
        """
<div class="hero-actions" style="align-items: center">
  <img src="../favicon/favicon.svg" alt="Laz Güneşi favicon" style="width: 64px; height: 64px">
  <img src="../favicon/favicon.svg" alt="" style="width: 32px; height: 32px">
  <img src="../favicon/favicon.svg" alt="" style="width: 16px; height: 16px">
  <p class="type-body">Canonical file: <code class="type-code">laz-gunesi-amblem/favicon/favicon.svg</code>. Same artwork on every site.</p>
</div>
""",
    ),
    Card(
        "chrome-sidebar",
        "Chrome",
        1280,
        640,
        "Sidebar chrome",
        "agustos · iesdesk · specquick — fixed 240px column, drawer below 1024px",
        """
<header class="site-sidebar-bar">
  <a class="site-lockup" href="/" aria-label="ağustos">
    <svg class="site-lockup__symbol" viewBox="-57.9197 -57.9197 115.8395 115.8395" aria-hidden="true" focusable="false">
      <g fill="currentColor">
        <path d="M 24.0215 4.2070 C 34.0762 5.8086 48.3340 21.1562 34.5645 38.4922 C 37.3145 23.6016 33.7988 10.1367 24.0215 4.2070 Z"/><path d="M 21.1309 12.1719 C 30.0332 17.1133 38.1816 36.4102 19.3145 47.9922 C 26.9941 34.9414 28.2910 21.0820 21.1309 12.1719 Z"/><path d="M 15.6934 18.6641 C 22.3691 26.3516 23.4238 47.2734 1.7363 51.7031 C 13.4121 42.0625 19.3730 29.4883 15.6934 18.6641 Z"/><path d="M 8.3652 22.9062 C 12.0059 32.4141 5.8418 52.4336 -16.0566 49.1797 C -1.7832 44.1133 8.1191 34.3359 8.3652 22.9062 Z"/><path d="M 0.0254 24.3867 C 0.1934 34.5664 -12.4434 51.2695 -31.9082 40.7187 C -16.7637 40.8437 -4.1152 35.0430 0.0254 24.3867 Z"/><path d="M -8.3184 22.9219 C -11.6387 32.5469 -29.2324 43.9219 -43.9121 27.3516 C -29.7246 32.6484 -15.8535 31.5195 -8.3184 22.9219 Z"/><path d="M -15.6582 18.6953 C -22.0684 26.6016 -42.4902 31.2734 -50.6191 10.6836 C -39.0996 20.5117 -25.6777 24.1953 -15.6582 18.6953 Z"/><path d="M -21.1074 12.2109 C -29.8379 17.4492 -50.6230 14.8555 -51.2207 -7.2734 C -43.7559 5.8984 -32.4043 13.9531 -21.1074 12.2109 Z"/><path d="M -24.0137 4.2539 C -34.0059 6.1914 -52.6543 -3.3555 -45.6426 -24.3516 C -43.1348 -9.4219 -35.2246 2.0312 -24.0137 4.2539 Z"/><path d="M -24.0215 -4.2148 C -34.0762 -5.8125 -48.3301 -21.1602 -34.5605 -38.4961 C -37.3145 -23.6055 -33.7949 -10.1406 -24.0215 -4.2148 Z"/><path d="M -21.1309 -12.1758 C -30.0332 -17.1172 -38.1777 -36.4141 -19.3105 -47.9961 C -26.9902 -34.9453 -28.2871 -21.0859 -21.1309 -12.1758 Z"/><path d="M -15.6934 -18.6680 C -22.3652 -26.3594 -23.4238 -47.2773 -1.7324 -51.7031 C -13.4121 -42.0664 -19.3730 -29.4922 -15.6934 -18.6680 Z"/><path d="M -8.3613 -22.9102 C -12.0059 -32.4180 -5.8418 -52.4336 16.0566 -49.1797 C 1.7832 -44.1172 -8.1191 -34.3398 -8.3613 -22.9102 Z"/><path d="M -0.0254 -24.3867 C -0.1934 -34.5703 12.4434 -51.2695 31.9043 -40.7188 C 16.7637 -40.8477 4.1152 -35.0430 -0.0254 -24.3867 Z"/><path d="M 8.3184 -22.9297 C 11.6387 -32.5547 29.2285 -43.9297 43.9121 -27.3594 C 29.7246 -32.6523 15.8535 -31.5273 8.3184 -22.9297 Z"/><path d="M 15.6582 -18.7031 C 22.0684 -26.6094 42.4902 -31.2813 50.6191 -10.6875 C 39.0996 -20.5195 25.6777 -24.2031 15.6582 -18.7031 Z"/><path d="M 21.1074 -12.2188 C 29.8418 -17.4570 50.6270 -14.8633 51.2207 7.2695 C 43.7559 -5.9063 32.4082 -13.9609 21.1074 -12.2188 Z"/><path d="M 24.0137 -4.2617 C 34.0098 -6.1953 52.6543 3.3477 45.6465 24.3477 C 43.1387 9.4141 35.2285 -2.0352 24.0137 -4.2617 Z"/>
      </g>
    </svg>
    <span class="site-lockup__name">ağustos</span>
  </a>
  <button type="button" class="site-sidebar-burger" popovertarget="site-sidebar" aria-label="Menüyü aç">
    <svg width="18" height="14" viewBox="0 0 18 14" aria-hidden="true" focusable="false"><path d="M0 1h18M0 7h18M0 13h18" stroke="currentColor" stroke-width="1.5"/></svg>
  </button>
</header>
<aside id="site-sidebar" class="site-sidebar" popover aria-label="Site menüsü">
  <a class="site-lockup" href="/" aria-label="ağustos">
    <svg class="site-lockup__symbol" viewBox="-57.9197 -57.9197 115.8395 115.8395" aria-hidden="true" focusable="false">
      <g fill="currentColor">
        <path d="M 24.0215 4.2070 C 34.0762 5.8086 48.3340 21.1562 34.5645 38.4922 C 37.3145 23.6016 33.7988 10.1367 24.0215 4.2070 Z"/><path d="M 21.1309 12.1719 C 30.0332 17.1133 38.1816 36.4102 19.3145 47.9922 C 26.9941 34.9414 28.2910 21.0820 21.1309 12.1719 Z"/><path d="M 15.6934 18.6641 C 22.3691 26.3516 23.4238 47.2734 1.7363 51.7031 C 13.4121 42.0625 19.3730 29.4883 15.6934 18.6641 Z"/><path d="M 8.3652 22.9062 C 12.0059 32.4141 5.8418 52.4336 -16.0566 49.1797 C -1.7832 44.1133 8.1191 34.3359 8.3652 22.9062 Z"/><path d="M 0.0254 24.3867 C 0.1934 34.5664 -12.4434 51.2695 -31.9082 40.7187 C -16.7637 40.8437 -4.1152 35.0430 0.0254 24.3867 Z"/><path d="M -8.3184 22.9219 C -11.6387 32.5469 -29.2324 43.9219 -43.9121 27.3516 C -29.7246 32.6484 -15.8535 31.5195 -8.3184 22.9219 Z"/><path d="M -15.6582 18.6953 C -22.0684 26.6016 -42.4902 31.2734 -50.6191 10.6836 C -39.0996 20.5117 -25.6777 24.1953 -15.6582 18.6953 Z"/><path d="M -21.1074 12.2109 C -29.8379 17.4492 -50.6230 14.8555 -51.2207 -7.2734 C -43.7559 5.8984 -32.4043 13.9531 -21.1074 12.2109 Z"/><path d="M -24.0137 4.2539 C -34.0059 6.1914 -52.6543 -3.3555 -45.6426 -24.3516 C -43.1348 -9.4219 -35.2246 2.0312 -24.0137 4.2539 Z"/><path d="M -24.0215 -4.2148 C -34.0762 -5.8125 -48.3301 -21.1602 -34.5605 -38.4961 C -37.3145 -23.6055 -33.7949 -10.1406 -24.0215 -4.2148 Z"/><path d="M -21.1309 -12.1758 C -30.0332 -17.1172 -38.1777 -36.4141 -19.3105 -47.9961 C -26.9902 -34.9453 -28.2871 -21.0859 -21.1309 -12.1758 Z"/><path d="M -15.6934 -18.6680 C -22.3652 -26.3594 -23.4238 -47.2773 -1.7324 -51.7031 C -13.4121 -42.0664 -19.3730 -29.4922 -15.6934 -18.6680 Z"/><path d="M -8.3613 -22.9102 C -12.0059 -32.4180 -5.8418 -52.4336 16.0566 -49.1797 C 1.7832 -44.1172 -8.1191 -34.3398 -8.3613 -22.9102 Z"/><path d="M -0.0254 -24.3867 C -0.1934 -34.5703 12.4434 -51.2695 31.9043 -40.7188 C 16.7637 -40.8477 4.1152 -35.0430 -0.0254 -24.3867 Z"/><path d="M 8.3184 -22.9297 C 11.6387 -32.5547 29.2285 -43.9297 43.9121 -27.3594 C 29.7246 -32.6523 15.8535 -31.5273 8.3184 -22.9297 Z"/><path d="M 15.6582 -18.7031 C 22.0684 -26.6094 42.4902 -31.2813 50.6191 -10.6875 C 39.0996 -20.5195 25.6777 -24.2031 15.6582 -18.7031 Z"/><path d="M 21.1074 -12.2188 C 29.8418 -17.4570 50.6270 -14.8633 51.2207 7.2695 C 43.7559 -5.9063 32.4082 -13.9609 21.1074 -12.2188 Z"/><path d="M 24.0137 -4.2617 C 34.0098 -6.1953 52.6543 3.3477 45.6465 24.3477 C 43.1387 9.4141 35.2285 -2.0352 24.0137 -4.2617 Z"/>
      </g>
    </svg>
    <span class="site-lockup__name">ağustos</span>
  </a>
  <nav class="site-sidebar__nav" aria-label="Ana menü">
    <a class="site-sidebar__link" href="/aydinlatma">Aydınlatma</a>
    <a class="site-sidebar__link" href="/danismanlik">Danışmanlık</a>
    <a class="site-sidebar__link" href="/blog">Yazılar</a>
    <a class="site-sidebar__link" href="/biz-kimiz">Biz kimiz</a>
    <a class="site-sidebar__link" href="/gecmis-markalar">Geçmiş markalar</a>
  </nav>
  <details class="site-sidebar__group">
    <summary>Sosyal</summary>
    <a class="site-sidebar__link" href="https://www.linkedin.com/company/agustostek/" rel="noopener">LinkedIn</a>
    <a class="site-sidebar__link" href="https://www.instagram.com/agustostek/" rel="noopener">Instagram</a>
    <a class="site-sidebar__link" href="https://www.youtube.com/c/AgustosTek" rel="noopener">YouTube</a>
  </details>
  <details class="site-sidebar__group">
    <summary>Yasal</summary>
    <a class="site-sidebar__link" href="/cerez-politikasi">Çerez ve yerel depolama</a>
    <a class="site-sidebar__link" href="/gizlilik-politikasi">Gizlilik ve KVKK metni</a>
  </details>
  <a class="agustos-button agustos-button--primary site-sidebar__cta" href="/bize-ulasin">İletişim</a>
  <div class="site-sidebar__utility">
    <a class="agustos-chrome-link" href="/ara">Ara</a>
    <a class="agustos-chrome-link" href="/en" hreflang="en">English</a>
  </div>
  <p class="site-sidebar__note">© Ağustos Teknoloji, 1996–2026</p>
</aside>
<main id="main" class="container">
  <h1 class="type-h1">Sidebar chrome</h1>
  <p class="type-body prose">The brand's registered chrome for agustos, iesdesk, and specquick. Below 1024px the bar and burger open it as a drawer.</p>
</main>
""",
        "brand-agustos paper-white site-sidebar-layout",
    ),
    Card(
        "chrome-topbar",
        "Chrome",
        1280,
        640,
        "Topbar chrome and footer",
        "pataraz · pld — sticky one-row header, structured footer, drawer below 1024px",
        """
<header class="site-header">
  <div class="site-header__bar site-frame">
    <a class="site-lockup" href="/" aria-label="pataraz">
      <svg class="site-lockup__symbol" viewBox="-57.9197 -57.9197 115.8395 115.8395" aria-hidden="true" focusable="false">
        <g fill="currentColor">
          <path d="M 24.0215 4.2070 C 34.0762 5.8086 48.3340 21.1562 34.5645 38.4922 C 37.3145 23.6016 33.7988 10.1367 24.0215 4.2070 Z"/><path d="M 21.1309 12.1719 C 30.0332 17.1133 38.1816 36.4102 19.3145 47.9922 C 26.9941 34.9414 28.2910 21.0820 21.1309 12.1719 Z"/><path d="M 15.6934 18.6641 C 22.3691 26.3516 23.4238 47.2734 1.7363 51.7031 C 13.4121 42.0625 19.3730 29.4883 15.6934 18.6641 Z"/><path d="M 8.3652 22.9062 C 12.0059 32.4141 5.8418 52.4336 -16.0566 49.1797 C -1.7832 44.1133 8.1191 34.3359 8.3652 22.9062 Z"/><path d="M 0.0254 24.3867 C 0.1934 34.5664 -12.4434 51.2695 -31.9082 40.7187 C -16.7637 40.8437 -4.1152 35.0430 0.0254 24.3867 Z"/><path d="M -8.3184 22.9219 C -11.6387 32.5469 -29.2324 43.9219 -43.9121 27.3516 C -29.7246 32.6484 -15.8535 31.5195 -8.3184 22.9219 Z"/><path d="M -15.6582 18.6953 C -22.0684 26.6016 -42.4902 31.2734 -50.6191 10.6836 C -39.0996 20.5117 -25.6777 24.1953 -15.6582 18.6953 Z"/><path d="M -21.1074 12.2109 C -29.8379 17.4492 -50.6230 14.8555 -51.2207 -7.2734 C -43.7559 5.8984 -32.4043 13.9531 -21.1074 12.2109 Z"/><path d="M -24.0137 4.2539 C -34.0059 6.1914 -52.6543 -3.3555 -45.6426 -24.3516 C -43.1348 -9.4219 -35.2246 2.0312 -24.0137 4.2539 Z"/><path d="M -24.0215 -4.2148 C -34.0762 -5.8125 -48.3301 -21.1602 -34.5605 -38.4961 C -37.3145 -23.6055 -33.7949 -10.1406 -24.0215 -4.2148 Z"/><path d="M -21.1309 -12.1758 C -30.0332 -17.1172 -38.1777 -36.4141 -19.3105 -47.9961 C -26.9902 -34.9453 -28.2871 -21.0859 -21.1309 -12.1758 Z"/><path d="M -15.6934 -18.6680 C -22.3652 -26.3594 -23.4238 -47.2773 -1.7324 -51.7031 C -13.4121 -42.0664 -19.3730 -29.4922 -15.6934 -18.6680 Z"/><path d="M -8.3613 -22.9102 C -12.0059 -32.4180 -5.8418 -52.4336 16.0566 -49.1797 C 1.7832 -44.1172 -8.1191 -34.3398 -8.3613 -22.9102 Z"/><path d="M -0.0254 -24.3867 C -0.1934 -34.5703 12.4434 -51.2695 31.9043 -40.7188 C 16.7637 -40.8477 4.1152 -35.0430 -0.0254 -24.3867 Z"/><path d="M 8.3184 -22.9297 C 11.6387 -32.5547 29.2285 -43.9297 43.9121 -27.3594 C 29.7246 -32.6523 15.8535 -31.5273 8.3184 -22.9297 Z"/><path d="M 15.6582 -18.7031 C 22.0684 -26.6094 42.4902 -31.2813 50.6191 -10.6875 C 39.0996 -20.5195 25.6777 -24.2031 15.6582 -18.7031 Z"/><path d="M 21.1074 -12.2188 C 29.8418 -17.4570 50.6270 -14.8633 51.2207 7.2695 C 43.7559 -5.9063 32.4082 -13.9609 21.1074 -12.2188 Z"/><path d="M 24.0137 -4.2617 C 34.0098 -6.1953 52.6543 3.3477 45.6465 24.3477 C 43.1387 9.4141 35.2285 -2.0352 24.0137 -4.2617 Z"/>
        </g>
      </svg>
      <span class="site-lockup__name">pataraz</span>
    </a>
    <div id="site-header-panel" class="site-header__panel" popover>
      <nav class="site-header__nav" aria-label="Ana menü">
        <a class="site-header__link" href="/urunler">Ürünler</a>
        <a class="site-header__link" href="/urun-bul">Ürün bul</a>
        <a class="site-header__link" href="/seriler">Seriler</a>
        <a class="site-header__link" href="/hakkinda">Hakkında</a>
      </nav>
      <div class="site-header__end">
        <a class="agustos-chrome-link" href="/en" hreflang="en">EN</a>
        <a class="agustos-button agustos-button--primary site-header__cta" href="/iletisim">Fiyat isteyin</a>
      </div>
    </div>
    <button type="button" class="site-header__burger" popovertarget="site-header-panel" aria-label="Menüyü aç">
      <svg width="18" height="14" viewBox="0 0 18 14" aria-hidden="true" focusable="false"><path d="M0 1h18M0 7h18M0 13h18" stroke="currentColor" stroke-width="1.5"/></svg>
    </button>
  </div>
</header>
<main id="main" class="container">
  <h1 class="type-h1">Topbar chrome</h1>
  <p class="type-body prose">The brand's registered chrome for pataraz and pld. The footer never follows the theme flip.</p>
</main>
<footer class="site-footer">
  <div class="site-footer__inner site-frame">
    <div class="site-footer__brand">
      <a class="site-lockup" href="/" aria-label="pataraz">
        <svg class="site-lockup__symbol" viewBox="-57.9197 -57.9197 115.8395 115.8395" aria-hidden="true" focusable="false">
          <g fill="currentColor">
            <path d="M 24.0215 4.2070 C 34.0762 5.8086 48.3340 21.1562 34.5645 38.4922 C 37.3145 23.6016 33.7988 10.1367 24.0215 4.2070 Z"/><path d="M 21.1309 12.1719 C 30.0332 17.1133 38.1816 36.4102 19.3145 47.9922 C 26.9941 34.9414 28.2910 21.0820 21.1309 12.1719 Z"/><path d="M 15.6934 18.6641 C 22.3691 26.3516 23.4238 47.2734 1.7363 51.7031 C 13.4121 42.0625 19.3730 29.4883 15.6934 18.6641 Z"/><path d="M 8.3652 22.9062 C 12.0059 32.4141 5.8418 52.4336 -16.0566 49.1797 C -1.7832 44.1133 8.1191 34.3359 8.3652 22.9062 Z"/><path d="M 0.0254 24.3867 C 0.1934 34.5664 -12.4434 51.2695 -31.9082 40.7187 C -16.7637 40.8437 -4.1152 35.0430 0.0254 24.3867 Z"/><path d="M -8.3184 22.9219 C -11.6387 32.5469 -29.2324 43.9219 -43.9121 27.3516 C -29.7246 32.6484 -15.8535 31.5195 -8.3184 22.9219 Z"/><path d="M -15.6582 18.6953 C -22.0684 26.6016 -42.4902 31.2734 -50.6191 10.6836 C -39.0996 20.5117 -25.6777 24.1953 -15.6582 18.6953 Z"/><path d="M -21.1074 12.2109 C -29.8379 17.4492 -50.6230 14.8555 -51.2207 -7.2734 C -43.7559 5.8984 -32.4043 13.9531 -21.1074 12.2109 Z"/><path d="M -24.0137 4.2539 C -34.0059 6.1914 -52.6543 -3.3555 -45.6426 -24.3516 C -43.1348 -9.4219 -35.2246 2.0312 -24.0137 4.2539 Z"/><path d="M -24.0215 -4.2148 C -34.0762 -5.8125 -48.3301 -21.1602 -34.5605 -38.4961 C -37.3145 -23.6055 -33.7949 -10.1406 -24.0215 -4.2148 Z"/><path d="M -21.1309 -12.1758 C -30.0332 -17.1172 -38.1777 -36.4141 -19.3105 -47.9961 C -26.9902 -34.9453 -28.2871 -21.0859 -21.1309 -12.1758 Z"/><path d="M -15.6934 -18.6680 C -22.3652 -26.3594 -23.4238 -47.2773 -1.7324 -51.7031 C -13.4121 -42.0664 -19.3730 -29.4922 -15.6934 -18.6680 Z"/><path d="M -8.3613 -22.9102 C -12.0059 -32.4180 -5.8418 -52.4336 16.0566 -49.1797 C 1.7832 -44.1172 -8.1191 -34.3398 -8.3613 -22.9102 Z"/><path d="M -0.0254 -24.3867 C -0.1934 -34.5703 12.4434 -51.2695 31.9043 -40.7188 C 16.7637 -40.8477 4.1152 -35.0430 -0.0254 -24.3867 Z"/><path d="M 8.3184 -22.9297 C 11.6387 -32.5547 29.2285 -43.9297 43.9121 -27.3594 C 29.7246 -32.6523 15.8535 -31.5273 8.3184 -22.9297 Z"/><path d="M 15.6582 -18.7031 C 22.0684 -26.6094 42.4902 -31.2813 50.6191 -10.6875 C 39.0996 -20.5195 25.6777 -24.2031 15.6582 -18.7031 Z"/><path d="M 21.1074 -12.2188 C 29.8418 -17.4570 50.6270 -14.8633 51.2207 7.2695 C 43.7559 -5.9063 32.4082 -13.9609 21.1074 -12.2188 Z"/><path d="M 24.0137 -4.2617 C 34.0098 -6.1953 52.6543 3.3477 45.6465 24.3477 C 43.1387 9.4141 35.2285 -2.0352 24.0137 -4.2617 Z"/>
          </g>
        </svg>
        <span class="site-lockup__name">pataraz</span>
      </a>
      <p class="type-footnote">Belirtilmiş armatürler. Net veri. © 2026 Pataraz</p>
    </div>
    <div class="site-footer__cols">
      <nav class="site-footer__col" aria-label="Ürünler">
        <p class="type-h4 site-footer__col-heading">Ürünler</p>
        <ul class="site-footer__list">
          <li><a class="site-footer__link" href="/seriler/pl">PL serisi</a></li>
          <li><a class="site-footer__link" href="/seriler/px">PX serisi</a></li>
          <li><a class="site-footer__link" href="/seriler/py">PY serisi</a></li>
        </ul>
      </nav>
      <nav class="site-footer__col" aria-label="Destek">
        <p class="type-h4 site-footer__col-heading">Destek</p>
        <ul class="site-footer__list">
          <li><a class="site-footer__link" href="/urun-bul">Ürün bul</a></li>
          <li><a class="site-footer__link" href="/teknik-foyler">Teknik föyler</a></li>
          <li><a class="site-footer__link" href="/hakkinda">Hakkında</a></li>
        </ul>
      </nav>
      <a class="agustos-button agustos-button--primary site-footer__cta" href="/iletisim">İletişim</a>
    </div>
  </div>
</footer>
""",
        "brand-pataraz paper-white",
    ),
)


def card_html(card: Card, version: str) -> str:
    marker = (
        f'<!-- @dsCard group="Kit · {card.group}" viewport="{card.width}x{card.height}" '
        f'name="{card.name}" subtitle="{card.subtitle}" -->'
    )
    return f"""{marker}
<!doctype html>
<html lang="tr" data-theme="light">
<head>
<meta charset="utf-8">
<title>{card.name} — Ağustos UI kit v{version}</title>
<link rel="stylesheet" href="../agustos-fonts.css">
<link rel="stylesheet" href="../agustos.css">
<style>body {{ margin: 0; padding: 24px 28px; }}</style>
</head>
<body class="{card.body_class}">
{card.body.strip()}
<p class="type-footnote">Ağustos UI kit v{version} · pushed from the repository. Edit the source there, not here.</p>
</body>
</html>
"""


def card_members(version: str) -> list[tuple[str, bytes]]:
    return [(f"cards/{card.slug}.html", card_html(card, version).encode("utf-8")) for card in CARDS]


SCREEN_CARD_VIEWPORT = (1280, 900)


def screen_card_members(root: Path = ROOT, version: str | None = None) -> list[tuple[str, bytes]]:
    """One card per screen, straight from screens/, with the kit paths rewritten to the bundle."""
    kit = json.loads((root / "ui" / "kit.json").read_text(encoding="utf-8"))
    width, height = SCREEN_CARD_VIEWPORT
    members: list[tuple[str, bytes]] = []
    for name, screen in kit["screens"].items():
        html = (root / "screens" / screen["file"]).read_text(encoding="utf-8")
        title = name.replace("-", " ").capitalize()
        family = "product UI" if screen["family"] == "product-ui" else screen["family"]
        theme = "dark allowed" if screen["theme"] == "dark-allowed" else screen["theme"]
        marker = (
            f'<!-- @dsCard group="Kit · Screens" viewport="{width}x{height}" '
            f'name="{title}" subtitle="{family} · {screen["chrome"]} · {theme}" -->'
        )
        html = (
            html.replace('href="../ui/agustos-fonts.css"', 'href="../agustos-fonts.css"')
            .replace('href="../ui/agustos.css"', 'href="../agustos.css"')
            .replace('href="../laz-gunesi-amblem/favicon/favicon.svg"', 'href="../favicon/favicon.svg"')
        )
        members.append((f"cards/screen-{name}.html", (marker + "\n" + html).encode("utf-8")))
    return members


# --- Build ------------------------------------------------------------------


class GuardError(RuntimeError):
    """A precondition for a push failed. The message says what to run."""


def generated_outputs_are_current(root: Path = ROOT) -> tuple[bool, str]:
    result = subprocess.run(
        ["python3", "scripts/build_design_system.py", "--check"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def ui_is_clean(root: Path = ROOT) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", "ui"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip() == ""


def git_commit(root: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def build_bundle(
    destination: Path = DIST_DIR,
    root: Path = ROOT,
    *,
    check=generated_outputs_are_current,
    clean=ui_is_clean,
    commit=git_commit,
) -> Path:
    """Write <destination>/agustos-ui/ from the generated kit. Refuse if the kit is stale or dirty."""
    ok, output = check(root)
    if not ok:
        message = (
            "Generated outputs are stale. Run `python3 scripts/build_design_system.py` and commit, "
            "then run `python3 scripts/build_design_system.py --check` until it passes."
        )
        if output:
            message = f"{message}\n{output}"
        raise GuardError(message)
    if not clean(root):
        raise GuardError("ui/ has uncommitted changes. Commit or discard them before a push.")
    ver = version(root)
    members = bundle_members(root) + card_members(ver) + screen_card_members(root, ver)
    data = manifest(members, version=ver, commit=commit(root))
    payload = (json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    members.append(("MANIFEST.json", payload))

    folder = destination / REMOTE_PREFIX
    if folder.exists():
        shutil.rmtree(folder)
    for name, content in members:
        target = folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return folder


# --- Pull -------------------------------------------------------------------
# A Design page is React + JSX loaded by relative paths from the project root.
# Mirroring the remote layout keeps every link intact. The page is a reference;
# nothing in the kit imports it.

RUNTIME_PATHS: tuple[str, ...] = (
    "styles.css",
    "_ds_bundle.js",
    "tokens/fonts.css",
    "tokens/colors.css",
    "tokens/spacing.css",
    "tokens/typography.css",
    "tokens/base.css",
)
SCREENS_DIR = ROOT / "screens"
DESIGN_DIR = SCREENS_DIR / "design"
CANVAS_SUFFIX = ".dc.html"
STATUS_HEADER = "| Reference | Remote path | Pulled | Target screen | Status | Built in |"
STATUS_DIVIDER = "|---|---|---|---|---|---|"

README_TEMPLATE = """# Claude Design references

Pages pulled verbatim from the Claude Design project "Ağustos". Each one is a reference for a
screen under `screens/`, or for a new screen.

- Project: {url}
- Project ID: `{project_id}`
- Pulled by: `python3 scripts/sync_claude_design.py pull` (see `.claude/skills/design-pull/SKILL.md`)
- Repository commit at pull: `{commit}`

These files are references, not kit sources. Nothing in `ui/` or `screens/*.html` imports them.
A built page keeps its remote folder layout here so its relative links resolve; the shared runtime
at this folder's root (`styles.css`, `_ds_bundle.js`, `tokens/`) is overwritten on every pull, and
a pull replaces a page folder except its `index.png`. A canvas page (`*.dc.html`) lands under
`canvas/`; its runtime is not exported, so it does not render here and has no screenshot.

## When you build one of these

1. Open the reference beside your editor. Open `index.png` when it exists.
2. Rebuild `screens/<target>.html` on kit classes. Do not copy the Design markup or CSS.
3. Run `python3 ui/check-agustos-ui.py screens --skip design` until it exits 0.
4. Change the row below to `implemented` and record where it shipped.
5. Run `/design-push` so the updated screen card reaches Claude Design.

## Status

{header}
{divider}
{rows}
"""


def remote_path(page: str) -> str:
    """A path inside the Design project. No escapes, no dotfiles, no absolute paths."""
    raw = page.strip()
    if not raw or raw.startswith("/"):
        raise ValueError(f"page must be a path inside the Design project, got {page!r}")
    page = raw.strip("/")
    parts = page.split("/")
    if ".." in parts or any(part.startswith(".") for part in parts):
        raise ValueError(f"page must be a path inside the Design project, got {page!r}")
    return page


def is_canvas(page: str) -> bool:
    return page.endswith(CANVAS_SUFFIX)


def reference_slug(page: str) -> str:
    """The last path segment, lower-case, without the canvas suffix: 'Product page.dc.html' -> 'product-page'."""
    name = page.strip("/").rsplit("/", 1)[-1]
    if name.endswith(CANVAS_SUFFIX):
        name = name[: -len(CANVAS_SUFFIX)]
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        raise ValueError(f"cannot derive a reference name from {page!r}")
    return slug


def _status_rows(existing: str | None) -> dict[str, list[str]]:
    """Parse the status table into {remote path: [reference, path, pulled, target, status, built in]}.

    Rows written before v6 had four cells (path, pulled, status, built in); they migrate in place.
    """
    rows: dict[str, list[str]] = {}
    if not existing:
        return rows
    for line in existing.splitlines():
        if not line.startswith("| ") or line in (STATUS_HEADER, STATUS_DIVIDER) or line.startswith("| Remote path |") or line.startswith("| Reference |"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and "/" in cells[1]:
            rows[cells[1]] = cells
        elif len(cells) == 4 and "/" in cells[0]:
            rows[cells[0]] = [reference_slug(cells[0]), cells[0], cells[1], "new", cells[2], cells[3]]
    return rows


def update_readme(existing: str | None, page: str, today: str, commit: str, target: str | None = None) -> str:
    """Add or refresh the page's row. Keep its status, target, and 'built in' unless a new target is given."""
    rows = _status_rows(existing)
    current = rows.get(page, [reference_slug(page), page, today, "new", "pending", "—"])
    current[2] = today
    if target:
        current[3] = target
    rows[page] = current
    body = "\n".join("| " + " | ".join(cells) + " |" for _, cells in sorted(rows.items()))
    return README_TEMPLATE.format(
        url=PROJECT_URL,
        project_id=PROJECT_ID,
        commit=commit,
        header=STATUS_HEADER,
        divider=STATUS_DIVIDER,
        rows=body,
    )


def _source_root(source: Path, scratch: Path) -> Path:
    """A directory as-is, or a zip extracted into scratch. Unwrap a single top-level folder."""
    if source.is_dir():
        root = source
    else:
        with zipfile.ZipFile(source) as archive:
            archive.extractall(scratch)
        root = scratch
    entries = [p for p in root.iterdir() if not p.name.startswith(".")]
    if len(entries) == 1 and entries[0].is_dir() and not (root / "styles.css").exists():
        root = entries[0]
    return root


def _clear_page_folder(page_destination: Path) -> None:
    if not page_destination.is_dir():
        return
    entries = sorted(page_destination.rglob("*"))
    for path in entries:
        if path.is_file() and path.name != "index.png":
            path.unlink()
    for path in sorted((p for p in entries if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def pull(
    source: Path,
    page: str,
    destination: Path = DESIGN_DIR,
    *,
    today: str,
    commit: str,
    target: str | None = None,
) -> list[Path]:
    """Copy one Design page folder (plus the shared runtime) or one canvas file into destination."""
    page = remote_path(page)
    written: list[Path] = []
    with tempfile.TemporaryDirectory() as scratch:
        root = _source_root(source, Path(scratch))
        if is_canvas(page):
            src = root / page
            if not src.is_file():
                raise FileNotFoundError(f"{page} is not a file in {source}")
            target_path = destination / "canvas" / f"{reference_slug(page)}{CANVAS_SUFFIX}"
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(src.read_bytes())
            written.append(target_path)
        else:
            page_dir = root / page
            if not page_dir.is_dir():
                raise FileNotFoundError(f"{page} is not a folder in {source}")
            _clear_page_folder(destination / page)
            wanted: list[Path] = [p for p in sorted(page_dir.rglob("*")) if p.is_file()]
            wanted += [root / rel for rel in RUNTIME_PATHS if (root / rel).is_file()]
            for path in wanted:
                out = destination / path.relative_to(root)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(path.read_bytes())
                written.append(out)
    readme = destination / "README.md"
    existing = readme.read_text(encoding="utf-8") if readme.exists() else None
    readme.write_text(update_readme(existing, page, today, commit, target), encoding="utf-8")
    written.append(readme)
    return written


# --- CLI --------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="print the bundle paths and sizes")
    listing.set_defaults(func=cmd_list)
    build = sub.add_parser("build", help="write dist/claude-design/agustos-ui/ after the guards pass")
    build.add_argument("-o", "--output", type=Path, default=DIST_DIR, help="destination folder (default: dist/claude-design)")
    build.set_defaults(func=cmd_build)
    pulling = sub.add_parser("pull", help="copy one Design page folder or canvas file into screens/design/")
    pulling.add_argument("--from", dest="source", type=Path, required=True, help="directory or zip that mirrors the Design project layout")
    pulling.add_argument("--page", required=True, help="remote path, for example ui_kits/website or uploads/<chat>/Product page.dc.html")
    pulling.add_argument("--target", default=None, help="the screen this reference updates (a name from the screens table), or new")
    pulling.set_defaults(func=cmd_pull)
    args = parser.parse_args()
    return args.func(args)


def cmd_list(args: argparse.Namespace) -> int:
    members = bundle_members()
    for name, payload in members:
        print(f"{len(payload):8}  {REMOTE_PREFIX}/{name}")
    print(f"{len(members)} files")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    try:
        folder = build_bundle(args.output)
    except GuardError as error:
        print(f"refused: {error}")
        return 1
    count = sum(1 for p in folder.rglob("*") if p.is_file())
    print(f"wrote {folder.relative_to(ROOT) if folder.is_relative_to(ROOT) else folder} ({count} files)")
    return 0


def cmd_pull(args: argparse.Namespace) -> int:
    try:
        written = pull(args.source, args.page, today=date.today().isoformat(), commit=git_commit(), target=args.target)
    except (ValueError, FileNotFoundError) as error:
        print(f"refused: {error}")
        return 1
    for path in written:
        print(path.relative_to(ROOT).as_posix())
    print(f"{len(written)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
