"""The release tagger: which versions get a tag, and on which commit.

Tags used to be pushed by the session that made the release. A cloud session
cannot push tags, so v7.0.0 and v7.0.1 shipped untagged; the workflow now tags
every release when it reaches main (MEMORY.md 2026-09-30 release-tags-on-main).
"""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_tags.py"
WORKFLOW = ROOT / ".github" / "workflows" / "tag-release.yml"


def load_tagger():
    spec = importlib.util.spec_from_file_location("release_tags", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


CHANGELOG = """# Changelog

## Unreleased

## [2.1.0] - 2026-09-30

## [2.0.0] - 2026-09-29

## [1.9.0] - 2026-09-28

## [1.0.0] - 2026-01-01
"""


class PendingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tagger = load_tagger()

    def test_versions_newer_than_the_newest_tag_are_pending_oldest_first(self):
        self.assertEqual(self.tagger.pending(CHANGELOG, "2.1.0", ["v1.9.0", "v1.0.0"]), ["2.0.0", "2.1.0"])

    def test_old_untagged_history_is_never_retagged(self):
        # 1.0.0 has no tag, but it is older than the newest tag.
        self.assertEqual(self.tagger.pending(CHANGELOG, "2.1.0", ["v1.9.0"]), ["2.0.0", "2.1.0"])

    def test_nothing_is_pending_once_the_current_version_is_tagged(self):
        self.assertEqual(self.tagger.pending(CHANGELOG, "2.1.0", ["v2.1.0", "v2.0.0"]), [])

    def test_a_version_without_a_changelog_section_is_refused(self):
        with self.assertRaisesRegex(self.tagger.ReleaseError, "no '## \\[2.2.0\\]' section"):
            self.tagger.pending(CHANGELOG, "2.2.0", ["v2.1.0"])

    def test_the_real_changelog_names_the_real_version(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(version, self.tagger.changelog_versions(changelog))


class ReleaseCommitTest(unittest.TestCase):
    """The tag lands on the first-parent commit that set VERSION: the merge that shipped it."""

    def test_the_tag_goes_on_the_merge_that_shipped_the_version(self):
        tagger = load_tagger()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)

            def git(*args: str) -> str:
                return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()

            def commit(version: str, message: str) -> None:
                (repo / "VERSION").write_text(version + "\n", encoding="utf-8")
                git("add", "VERSION")
                git("commit", "--quiet", "-m", message)

            git("init", "--quiet", "--initial-branch=main")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.com")
            commit("1.0.0", "release 1.0.0")
            git("checkout", "--quiet", "-b", "feature")
            commit("1.1.0", "bump on the branch")
            (repo / "notes.txt").write_text("more\n", encoding="utf-8")
            git("add", "notes.txt")
            git("commit", "--quiet", "-m", "later branch work")
            git("checkout", "--quiet", "main")
            git("merge", "--quiet", "--no-ff", "feature", "-m", "merge 1.1.0")
            merge = git("rev-parse", "HEAD")

            with mock.patch.object(tagger, "ROOT", repo):
                self.assertEqual(tagger.release_commit("1.1.0", "HEAD"), merge)
                self.assertEqual(tagger.release_commit("1.0.0", "HEAD"), git("rev-list", "--max-parents=0", "HEAD"))
                with self.assertRaisesRegex(tagger.ReleaseError, "no commit on HEAD sets VERSION to 9.9.9"):
                    tagger.release_commit("9.9.9", "HEAD")


class WorkflowTest(unittest.TestCase):
    TEXT = WORKFLOW.read_text(encoding="utf-8")

    def test_it_runs_on_main_and_only_tags(self):
        self.assertIn("branches: [main]", self.TEXT)
        self.assertIn("contents: write", self.TEXT)
        self.assertIn("python3 scripts/release_tags.py --push", self.TEXT)

    def test_it_uses_no_third_party_action(self):
        self.assertNotIn("uses:", self.TEXT)

    def test_it_is_the_only_workflow(self):
        """Fleet rule: no GitHub Actions CI. This one tags; the pre-push hook stays the CI."""
        self.assertEqual(sorted(p.name for p in WORKFLOW.parent.iterdir()), ["tag-release.yml"])


if __name__ == "__main__":
    unittest.main()
