from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_portfolio_provenance.py"
SPEC = importlib.util.spec_from_file_location("portfolio_provenance", SCRIPT)
assert SPEC and SPEC.loader
provenance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(provenance)


class PortfolioProvenanceTests(unittest.TestCase):
    def copied_root(self, temporary_directory: str) -> Path:
        target = Path(temporary_directory)
        relative_paths = set(provenance.EXPECTED_COVERED_PATHS)
        relative_paths.update(provenance.PROVENANCE_SURFACES)
        for relative in relative_paths:
            source = ROOT / relative
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        return target

    def load_manifest(self, root: Path) -> dict:
        return json.loads((root / provenance.MANIFEST_RELATIVE).read_text())

    def write_manifest(self, root: Path, manifest: dict) -> None:
        unsigned = {
            key: value for key, value in manifest.items() if key != "integrity"
        }
        manifest["integrity"]["digest"] = provenance.hashlib.sha256(
            provenance.canonical_json(unsigned)
        ).hexdigest()
        (root / provenance.MANIFEST_RELATIVE).write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_current_gate_verifies_offline(self):
        result = provenance.verify(ROOT)
        self.assertEqual(result["result"], "PASS")
        self.assertFalse(result["networkUsed"])
        self.assertFalse(result["authorityAdded"])

    def test_covered_artifact_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            with (root / "README.md").open("a", encoding="utf-8") as handle:
                handle.write("\ntampered\n")
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)

    def test_ci_workflow_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            with (root / ".github/workflows/ci.yml").open(
                "a", encoding="utf-8"
            ) as handle:
                handle.write("\n# unrefreshed workflow change\n")
            with self.assertRaisesRegex(
                provenance.ProvenanceError,
                r"artifact digest changed: \.github/workflows/ci\.yml",
            ):
                provenance.verify(root)

    def test_ci_workflow_refresh_then_verify_passes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            with (root / ".github/workflows/ci.yml").open(
                "a", encoding="utf-8"
            ) as handle:
                handle.write("\n# authorized workflow update\n")
            provenance.refresh_manifest(root)
            result = provenance.verify(root)
            self.assertEqual(result["result"], "PASS")
            self.assertFalse(result["networkUsed"])
            self.assertFalse(result["authorityAdded"])

    def test_modernization_visual_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            visual = (
                root
                / "docs/assets/showcase/progressive-legacy-modernization.svg"
            )
            with visual.open("a", encoding="utf-8") as handle:
                handle.write("\n<!-- tampered -->\n")
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)

    def test_verifier_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            with (root / "scripts/verify_portfolio_provenance.py").open(
                "a", encoding="utf-8"
            ) as handle:
                handle.write("\n# tampered\n")
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)

    def test_recomputed_marker_substitution_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            manifest = self.load_manifest(root)
            manifest["fingerprint"]["marker"] = "COPIED-PORTFOLIO"
            manifest["fingerprint"]["markerSha256"] = provenance.hashlib.sha256(
                b"COPIED-PORTFOLIO"
            ).hexdigest()
            self.write_manifest(root, manifest)
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)

    def test_recomputed_author_substitution_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            manifest = self.load_manifest(root)
            manifest["authorship"]["assertedAuthor"] = "Substitute Author"
            self.write_manifest(root, manifest)
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)

    def test_refresh_refuses_author_substitution(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            manifest = self.load_manifest(root)
            manifest["authorship"]["assertedAuthor"] = "Substitute Author"
            self.write_manifest(root, manifest)
            with self.assertRaises(provenance.ProvenanceError):
                provenance.refresh_manifest(root)

    def test_recomputed_origin_substitution_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            manifest = self.load_manifest(root)
            manifest["origin"]["canonicalRepository"] = "https://example.com/copy"
            self.write_manifest(root, manifest)
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)

    def test_recomputed_ai_disruption_claim_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            manifest = self.load_manifest(root)
            manifest["claims"]["aiSafety"]["modelDisruptionIntent"] = True
            self.write_manifest(root, manifest)
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)

    def test_invisible_unicode_cannot_be_refreshed(self):
        for character in ("\u00ad", "\u180e", "\u200b", "\ufe0f"):
            with self.subTest(codepoint=f"U+{ord(character):04X}"):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = self.copied_root(temporary_directory)
                    with (root / "docs/PORTFOLIO-PROVENANCE.md").open(
                        "a", encoding="utf-8"
                    ) as handle:
                        handle.write(character)
                    with self.assertRaises(provenance.ProvenanceError):
                        provenance.refresh_manifest(root)

    def test_encoded_invisible_unicode_cannot_be_refreshed(self):
        for payload in ("&#x200B;", "&#x202E;", "&lrm;", "&#173;"):
            with self.subTest(payload=payload):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = self.copied_root(temporary_directory)
                    with (root / "docs/PORTFOLIO-PROVENANCE.md").open(
                        "a", encoding="utf-8"
                    ) as handle:
                        handle.write(payload)
                    with self.assertRaises(provenance.ProvenanceError):
                        provenance.refresh_manifest(root)

    def test_executable_html_cannot_be_refreshed(self):
        payloads = (
            "<!-- hidden -->",
            '<img src="x" onerror="alert(1)">',
            '<svg onload="alert(1)"></svg>',
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = self.copied_root(temporary_directory)
                    with (root / "docs/PORTFOLIO-PROVENANCE.md").open(
                        "a", encoding="utf-8"
                    ) as handle:
                        handle.write(payload)
                    with self.assertRaises(provenance.ProvenanceError):
                        provenance.refresh_manifest(root)

    def test_markdown_resources_cannot_be_refreshed(self):
        payloads = (
            "![pixel](https://example.test/collect)",
            "![pixel](//example.test/collect)",
            "![pixel][collector]\n\n[collector]: https://example.test/collect",
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = self.copied_root(temporary_directory)
                    with (root / "docs/PORTFOLIO-PROVENANCE.md").open(
                        "a", encoding="utf-8"
                    ) as handle:
                        handle.write(payload)
                    with self.assertRaises(provenance.ProvenanceError):
                        provenance.refresh_manifest(root)

    def test_markdown_attributes_cannot_be_refreshed(self):
        payloads = (
            '[text](#){style="background-image:url(https://example.test/collect)"}',
            'text\n{: style="list-style-image:url(//example.test/collect)"}',
            '[text](#){src="https://example.test/collect"}',
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = self.copied_root(temporary_directory)
                    with (root / "docs/PORTFOLIO-PROVENANCE.md").open(
                        "a", encoding="utf-8"
                    ) as handle:
                        handle.write(payload)
                    with self.assertRaises(provenance.ProvenanceError):
                        provenance.refresh_manifest(root)

    def test_active_markdown_cannot_be_refreshed(self):
        payloads = (
            "```mermaid\nflowchart LR\nA --> B\n```",
            "1. ```mermaid\n   flowchart LR\n   A --> B\n   ```",
            "> ~~~mermaid\n> flowchart LR\n> A --> B\n> ~~~",
            "[run](javascript:alert(1))",
            "[run](java&#x0A;script:alert(1))",
            "[run](java&#13;script:alert(1))",
            "[run](java&Tab;script:alert(1))",
            "[payload](d&#x61;ta:text/plain,active)",
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = self.copied_root(temporary_directory)
                    with (root / "docs/PORTFOLIO-PROVENANCE.md").open(
                        "a", encoding="utf-8"
                    ) as handle:
                        handle.write(payload)
                    with self.assertRaises(provenance.ProvenanceError):
                        provenance.refresh_manifest(root)

    def test_schema_claim_flag_reduction_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            schema_path = root / provenance.SCHEMA_RELATIVE
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["$defs"]["aiSafetyFlags"]["required"].pop()
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            with self.assertRaises(provenance.ProvenanceError):
                provenance.validate_schema(root)

    def test_schema_identity_substitution_cannot_be_refreshed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            schema_path = root / provenance.SCHEMA_RELATIVE
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["authorship"]["properties"]["assertedAuthor"][
                "const"
            ] = "Substitute Author"
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            with self.assertRaises(provenance.ProvenanceError):
                provenance.refresh_manifest(root)

    def test_malformed_citation_cannot_be_refreshed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            with (root / "CITATION.cff").open("a", encoding="utf-8") as handle:
                handle.write("[")
            with self.assertRaises(provenance.ProvenanceError):
                provenance.refresh_manifest(root)

    def test_citation_author_substitution_cannot_be_refreshed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            citation_path = root / "CITATION.cff"
            citation = json.loads(citation_path.read_text(encoding="utf-8"))
            citation["authors"][0]["given-names"] = "Substitute"
            citation_path.write_text(json.dumps(citation), encoding="utf-8")
            with self.assertRaises(provenance.ProvenanceError):
                provenance.refresh_manifest(root)

    def test_duplicate_json_keys_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            path = root / provenance.MANIFEST_RELATIVE
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    "{\n",
                    '{\n  "schemaVersion": "substitution",\n',
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)

    def test_recomputed_path_set_reduction_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = self.copied_root(temporary_directory)
            manifest = self.load_manifest(root)
            manifest["coveredArtifacts"].pop()
            self.write_manifest(root, manifest)
            with self.assertRaises(provenance.ProvenanceError):
                provenance.verify(root)


if __name__ == "__main__":
    unittest.main()
