"""Verify that all GitHub Actions workflow references remain SHA-pinned."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = ROOT / ".github" / "workflows"

USES_LINE_PATTERN = re.compile(r"^\s*(?:-\s*)?uses:\s*(.+?)\s*$")
IMMUTABLE_REF_PATTERN = re.compile(
    r"^(?P<action>[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+)@(?P<sha>[0-9a-f]{40})$"
)
TOP_LEVEL_PERMISSIONS_PATTERN = re.compile(r"^permissions:(.*)$")
PERMISSION_ENTRY_PATTERN = re.compile(
    r"^[ \t]+([a-z][a-z0-9-]*):\s*(read|write|none)\s*(?:#.*)?$"
)

EXPECTED_STANDARD_WORKFLOW_PINS = {
    "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/setup-python": "6d4fd22b20465ccc0f7354476588e8df7c9ca0e0",
    "actions/upload-artifact": "cf430e030ddbb5b0abf93d22962f4752f3646cd9",
    "actions/dependency-review-action": "bbc44d14a204704ccc493733616cd1e93a0321ec",
    "actions/upload-pages-artifact": "fc324d3547104276b827a68afc52ff2a11cc49c9",
}


def extract_uses_references(workflow_text: str) -> list[tuple[int, str]]:
    """Return (line_number, reference_without_comment) for every `uses:` line."""
    references: list[tuple[int, str]] = []
    for line_number, line in enumerate(workflow_text.splitlines(), start=1):
        match = USES_LINE_PATTERN.match(line)
        if not match:
            continue
        raw_value = match.group(1).split("#", 1)[0].strip()
        if (raw_value.startswith("'") and raw_value.endswith("'")) or (
            raw_value.startswith('"') and raw_value.endswith('"')
        ):
            raw_value = raw_value[1:-1].strip()
        references.append((line_number, raw_value))
    return references


def validate_workflow_pinning(workflow_text: str, label: str) -> list[str]:
    """Fail closed if any `uses:` entry is not pinned to a 40-hex commit SHA."""
    errors: list[str] = []
    references = extract_uses_references(workflow_text)
    if not references:
        errors.append(f"{label}: no workflow uses: references found")
        return errors
    for line_number, reference in references:
        if reference.startswith("./"):
            continue
        if not IMMUTABLE_REF_PATTERN.fullmatch(reference):
            errors.append(
                f"{label}:{line_number}: action reference is not pinned to a "
                f"40-char lowercase commit SHA: {reference}"
            )
    return errors


def validate_workflow_permissions(workflow_text: str, label: str) -> list[str]:
    """Fail closed if a workflow omits an explicit top-level `permissions:` block."""
    lines = workflow_text.splitlines()
    for index, line in enumerate(lines):
        match = TOP_LEVEL_PERMISSIONS_PATTERN.match(line)
        if not match:
            continue
        inline_value = match.group(1).split("#", 1)[0].strip()
        if inline_value == "{}":
            return []
        if inline_value:
            return [
                f"{label}:{index + 1}: top-level permissions must be an explicit "
                f"scope mapping, not {inline_value!r}"
            ]
        entries = 0
        for sub_index in range(index + 1, len(lines)):
            sub_line = lines[sub_index]
            stripped = sub_line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if not sub_line[0].isspace():
                break
            if not PERMISSION_ENTRY_PATTERN.match(sub_line):
                return [
                    f"{label}:{sub_index + 1}: invalid permissions entry: {stripped!r}"
                ]
            entries += 1
        if entries == 0:
            return [f"{label}:{index + 1}: top-level permissions block is empty"]
        return []
    return [f"{label}: missing top-level permissions block"]


class WorkflowActionPinningTests(unittest.TestCase):
    def test_all_repository_workflows_are_sha_pinned(self):
        workflow_files = sorted(WORKFLOWS_DIR.glob("*.yml"))
        self.assertTrue(workflow_files, "expected GitHub Actions workflows")
        for workflow_path in workflow_files:
            with self.subTest(workflow=workflow_path.name):
                errors = validate_workflow_pinning(
                    workflow_path.read_text(encoding="utf-8"),
                    workflow_path.name,
                )
                self.assertEqual(errors, [])

    def test_all_repository_workflows_declare_explicit_permissions(self):
        workflow_files = sorted(WORKFLOWS_DIR.glob("*.yml"))
        self.assertTrue(workflow_files, "expected GitHub Actions workflows")
        for workflow_path in workflow_files:
            with self.subTest(workflow=workflow_path.name):
                errors = validate_workflow_permissions(
                    workflow_path.read_text(encoding="utf-8"),
                    workflow_path.name,
                )
                self.assertEqual(errors, [])

    def test_standard_workflows_pin_expected_upgraded_action_shas(self):
        standard_workflows = [
            "agents-security.yml",
            "ci.yml",
            "dependency-review.yml",
            "docs-pages.yml",
            "trusted-publication-boundary.yml",
        ]
        observed_actions: set[str] = set()
        for name in standard_workflows:
            text = (WORKFLOWS_DIR / name).read_text(encoding="utf-8")
            for _, reference in extract_uses_references(text):
                match = IMMUTABLE_REF_PATTERN.fullmatch(reference)
                self.assertIsNotNone(match, f"{name}: unpinned {reference}")
                action = match.group("action")
                sha = match.group("sha")
                if action in EXPECTED_STANDARD_WORKFLOW_PINS:
                    observed_actions.add(action)
                    self.assertEqual(
                        sha,
                        EXPECTED_STANDARD_WORKFLOW_PINS[action],
                        f"{name}: unexpected SHA for {action}",
                    )
        self.assertEqual(
            observed_actions,
            set(EXPECTED_STANDARD_WORKFLOW_PINS),
            "every upgraded action pin must be exercised in standard workflows",
        )

    def test_mutable_and_malformed_action_refs_fail_closed(self):
        invalid_references = [
            "actions/checkout@v7",
            "actions/checkout@v7.0.1",
            "actions/setup-python@main",
            "actions/upload-artifact@cf430e0",
            "actions/dependency-review-action@BBC44D14A204704CCC493733616CD1E93A0321EC",
            "actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49cz",
            "actions/checkout",
            "docker://alpine:latest",
        ]
        for bad_ref in invalid_references:
            with self.subTest(reference=bad_ref):
                workflow_yaml = f"jobs:\n  test:\n    steps:\n      - uses: {bad_ref}\n"
                errors = validate_workflow_pinning(workflow_yaml, "synthetic.yml")
                self.assertTrue(errors, f"expected fail-closed rejection for {bad_ref}")

    def test_empty_workflow_without_uses_fails_closed(self):
        errors = validate_workflow_pinning("name: empty\njobs: {}\n", "empty.yml")
        self.assertTrue(errors)

    def test_missing_or_broad_permissions_fail_closed(self):
        invalid_workflows = {
            "missing_permissions": (
                "name: synthetic\non:\n  pull_request:\njobs:\n  test:\n"
                "    runs-on: ubuntu-latest\n    steps:\n"
                "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n"
            ),
            "write_all": "name: synthetic\npermissions: write-all\njobs: {}\n",
            "read_all": "name: synthetic\npermissions: read-all\njobs: {}\n",
            "empty_mapping": "name: synthetic\npermissions:\njobs: {}\n",
            "invalid_scope_value": "name: synthetic\npermissions:\n  contents: admin\njobs: {}\n",
        }
        for case, workflow_yaml in invalid_workflows.items():
            with self.subTest(case=case):
                errors = validate_workflow_permissions(workflow_yaml, f"{case}.yml")
                self.assertTrue(errors, f"expected fail-closed rejection for {case}")

    def test_empty_explicit_permissions_object_passes(self):
        errors = validate_workflow_permissions(
            "name: synthetic\npermissions: {}\njobs: {}\n",
            "explicit-empty.yml",
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
