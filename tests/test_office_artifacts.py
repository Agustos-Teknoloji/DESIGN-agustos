from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_office_artifacts.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_office_artifacts", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class OfficeArtifactContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = load_checker()
        cls.brands = cls.checker.office_brands(ROOT)

    def test_registry_declares_exact_office_coverage(self):
        self.assertEqual(self.brands, ["agustos", "pataraz", "pld"])

    def test_office_manifest_is_current(self):
        self.assertEqual(self.checker.check_manifest(ROOT), [])
        manifest = self.checker.expected_manifest(ROOT)
        self.assertEqual(manifest["version"], "3.0.0")
        self.assertEqual(len(manifest["artifacts"]), 9)

    def test_office_manifest_cli_passes(self):
        result = subprocess.run(
            [sys.executable, str(CHECKER_PATH), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_manifest_detects_artifact_and_source_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tokens").mkdir()
            (root / "scripts").mkdir()
            (root / "brand" / "exports" / "sample" / "office").mkdir(parents=True)
            (root / "brand" / "exports" / "sample" / "lockup").mkdir(parents=True)
            (root / "tokens" / "resolved.json").write_text('{"name":"Test","version":"1"}', encoding="utf-8")
            (root / "brand" / "brands.json").write_text('{"brands":{"sample":{"office":true}}}', encoding="utf-8")
            (root / "brand" / "build_templates.py").write_text("# source\n", encoding="utf-8")
            (root / "brand" / "build_presentation.mjs").write_text("// source\n", encoding="utf-8")
            (root / "brand" / "package.json").write_text("{}\n", encoding="utf-8")
            (root / "brand" / "package-lock.json").write_text("{}\n", encoding="utf-8")
            (root / "scripts" / "check_office_artifacts.py").write_text("# checker\n", encoding="utf-8")
            for expression in ("positive", "negative"):
                (root / "brand" / "exports" / "sample" / "lockup" / f"sample-lockup__{expression}.png").write_bytes(expression.encode())
            for suffix in self.checker.OFFICE_SUFFIXES:
                (root / "brand" / "exports" / "sample" / "office" / f"sample-{suffix}").write_bytes(suffix.encode())
            manifest = root / "brand" / "exports" / "office-manifest.json"
            self.checker.write_manifest(root, manifest)
            self.assertEqual(self.checker.check_manifest(root, manifest), [])
            artifact = root / "brand" / "exports" / "sample" / "office" / "sample-template.pptx"
            artifact.write_bytes(b"changed")
            self.assertIn(str(artifact.relative_to(root)), self.checker.check_manifest(root, manifest))
            self.checker.write_manifest(root, manifest)
            (root / "brand" / "build_templates.py").write_text("# changed source\n", encoding="utf-8")
            self.assertIn("Office generator sources", self.checker.check_manifest(root, manifest))

    def test_manifest_detects_lockup_source_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tokens").mkdir()
            (root / "scripts").mkdir()
            (root / "brand" / "exports" / "sample" / "office").mkdir(parents=True)
            (root / "brand" / "exports" / "sample" / "lockup").mkdir(parents=True)
            (root / "tokens" / "resolved.json").write_text('{"name":"Test","version":"1"}', encoding="utf-8")
            (root / "brand" / "brands.json").write_text('{"brands":{"sample":{"office":true}}}', encoding="utf-8")
            (root / "brand" / "build_templates.py").write_text("# source\n", encoding="utf-8")
            (root / "brand" / "build_presentation.mjs").write_text("// source\n", encoding="utf-8")
            (root / "brand" / "package.json").write_text("{}\n", encoding="utf-8")
            (root / "brand" / "package-lock.json").write_text("{}\n", encoding="utf-8")
            (root / "scripts" / "check_office_artifacts.py").write_text("# checker\n", encoding="utf-8")
            for suffix in self.checker.OFFICE_SUFFIXES:
                (root / "brand" / "exports" / "sample" / "office" / f"sample-{suffix}").write_bytes(suffix.encode())
            for expression in ("positive", "negative"):
                (root / "brand" / "exports" / "sample" / "lockup" / f"sample-lockup__{expression}.png").write_bytes(expression.encode())
            manifest = root / "brand" / "exports" / "office-manifest.json"
            self.checker.write_manifest(root, manifest)
            lockup = root / "brand" / "exports" / "sample" / "lockup" / "sample-lockup__positive.png"
            lockup.write_bytes(b"changed")
            self.assertIn("Office generator sources", self.checker.check_manifest(root, manifest))

    def test_missing_office_artifact_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tokens").mkdir()
            (root / "brand").mkdir()
            (root / "tokens" / "resolved.json").write_text('{"name":"Test","version":"1"}', encoding="utf-8")
            (root / "brand" / "brands.json").write_text('{"brands":{"sample":{"office":true}}}', encoding="utf-8")
            with self.assertRaisesRegex(self.checker.ArtifactError, "missing Office artifact"):
                self.checker.expected_manifest(root)

    def test_docx_templates_have_native_styles_headers_and_tables(self):
        for slug in self.brands:
            for kind in ("letterhead", "document-template"):
                path = ROOT / "brand" / "exports" / slug / "office" / f"{slug}-{kind}.docx"
                with self.subTest(slug=slug, kind=kind), zipfile.ZipFile(path) as archive:
                    styles = archive.read("word/styles.xml").decode("utf-8")
                    header = archive.read("word/header1.xml").decode("utf-8")
                    document = archive.read("word/document.xml").decode("utf-8")
                    self.assertIn('w:styleId="Title"', styles)
                    self.assertIn('w:styleId="Heading1"', styles)
                    self.assertIn("Inter Tight", styles)
                    self.assertIn("w:tcBorders", header)
                    self.assertIn("w:drawing", header)
                    if kind == "document-template":
                        self.assertIn("w:tbl", document)
                        self.assertIn("Structured information", document)

    def test_pptx_templates_have_five_editable_named_slides(self):
        required_names = ("presentation-title", "section-title", "content-title", "data-title", "closing-domain")
        for slug in self.brands:
            path = ROOT / "brand" / "exports" / slug / "office" / f"{slug}-template.pptx"
            with self.subTest(slug=slug), zipfile.ZipFile(path) as archive:
                slides = sorted(
                    name for name in archive.namelist()
                    if name.startswith("ppt/slides/slide") and name.endswith(".xml")
                )
                self.assertEqual(len(slides), 5)
                combined = "\n".join(archive.read(name).decode("utf-8") for name in slides)
                for name in required_names:
                    self.assertIn(name, combined)
                self.assertIn("Presentation title", combined)

    def test_office_templates_preserve_identity_and_shared_signal_colors(self):
        for slug in self.brands:
            identity = "CF142A" if slug == "agustos" else "1A1A1A"
            for kind in ("letterhead", "document-template"):
                path = ROOT / "brand" / "exports" / slug / "office" / f"{slug}-{kind}.docx"
                with self.subTest(slug=slug, kind=kind), zipfile.ZipFile(path) as archive:
                    xml = "\n".join(
                        archive.read(name).decode("utf-8")
                        for name in archive.namelist()
                        if name.endswith(".xml")
                    ).upper()
                    self.assertIn(identity, xml)
                    self.assertIn("CF142A", xml)

            path = ROOT / "brand" / "exports" / slug / "office" / f"{slug}-template.pptx"
            with self.subTest(slug=slug, kind="presentation"), zipfile.ZipFile(path) as archive:
                xml = "\n".join(
                    archive.read(name).decode("utf-8")
                    for name in archive.namelist()
                    if name.endswith(".xml")
                ).upper()
                self.assertIn(identity, xml)
                self.assertIn("CF142A", xml)


if __name__ == "__main__":
    unittest.main()
