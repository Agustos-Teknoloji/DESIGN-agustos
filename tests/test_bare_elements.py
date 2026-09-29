"""UI-KIT.md promises that bare HTML elements are styled without classes.

Markdown and CMS output is bare HTML, so a missing element selector leaves a
consumer page in browser defaults. Every element that the promise names must
share its rule with the matching class, so that `<h3>` and `.type-h3` look the
same.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT_CSS = (ROOT / "ui" / "agustos.css").read_text(encoding="utf-8")
UI_KIT = (ROOT / "ui" / "UI-KIT.md").read_text(encoding="utf-8")

# The class that each bare element must match.
PAIRS = {
    "h1": ".type-h1",
    "h2": ".type-h2",
    "h3": ".type-h3",
    "h4": ".type-h4",
    "p": ".type-body",
    "a": ".type-link",
    "code": ".type-code",
    "ul": ".type-list-ul",
    "ol": ".type-list-ol",
    "dl": ".type-dl",
    "table": ".type-table",
    "blockquote": ".type-blockquote",
    "pre": ".type-code-block",
    "hr": ".type-divider",
}


def promised_elements() -> set[str]:
    line = next(l for l in UI_KIT.splitlines() if l.startswith("Bare HTML elements are styled"))
    names = set(re.findall(r"`([a-z0-9]+)`", line))
    # The doc writes a heading range as `h1`–`h4`.
    for first, last in re.findall(r"`h(\d)`–`h(\d)`", line):
        names.update(f"h{n}" for n in range(int(first), int(last) + 1))
    return names


def top_level_parts(selector: str) -> set[str]:
    """Split a selector list on commas outside `:is()` and other parentheses."""
    parts, depth, start = set(), 0, 0
    for i, char in enumerate(selector):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.add(selector[start:i].strip())
            start = i + 1
    parts.add(selector[start:].strip())
    return parts


def selector_lists() -> list[set[str]]:
    return [
        top_level_parts(match.group(1))
        for match in re.finditer(r"(?m)^([^\s@/{}][^{}]*)\{", KIT_CSS)
    ]


class BareElementTest(unittest.TestCase):
    def test_every_promised_element_has_a_pair(self):
        self.assertEqual(promised_elements() - PAIRS.keys(), set())

    def test_bare_element_shares_the_class_rule(self):
        lists = selector_lists()
        for element in sorted(promised_elements()):
            with self.subTest(element=element):
                cls = PAIRS[element]
                self.assertTrue(
                    any(element in s and cls in s for s in lists),
                    f"no rule styles bare {element} together with {cls}",
                )


if __name__ == "__main__":
    unittest.main()
