"""Verify that all GitHub Actions workflow references remain SHA-pinned."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = ROOT / ".github" / "workflows"

BLOCK_USES_LINE_PATTERN = re.compile(
    r"^\s*(?:-\s*)*(?:uses|\"uses\"|'uses')\s*:\s*(.+?)\s*$"
)
FLOW_USES_PATTERN = re.compile(
    r"(?:^|[\s,{])(?:uses|\"uses\"|'uses')\s*:\s*(?P<value>\"[^\"]*\"|'[^']*'|[^,}\]]+)"
)
IMMUTABLE_REF_PATTERN = re.compile(
    r"^(?P<action>[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+)@(?P<sha>[0-9a-f]{40})$"
)
PERMISSIONS_LINE_PATTERN = re.compile(
    r"^(?P<indent>[ \t]*)(?:-\s+)?(?:permissions|\"permissions\"|'permissions')\s*:(?P<rest>.*)$"
)
FLOW_PERMISSIONS_PATTERN = re.compile(
    r"(?:^|[\s,{])(?:permissions|\"permissions\"|'permissions')\s*:\s*(?P<value>\{[^}]*\}|\"[^\"]*\"|'[^']*'|[^,}\]]+)"
)
PERMISSION_ENTRY_PATTERN = re.compile(
    r"^[ \t]+([a-z][a-z0-9-]*)\s*:\s*(read|write|none)\s*$"
)
FLOW_PERMISSION_ENTRY_PATTERN = re.compile(
    r"^(?:[a-z][a-z0-9-]*|\"[a-z][a-z0-9-]*\"|'[a-z][a-z0-9-]*')\s*:\s*(?:read|write|none|\"(?:read|write|none)\"|'(?:read|write|none)')$"
)
BLOCK_SCALAR_HEADER_PATTERN = re.compile(
    r"^(?P<indent>[ \t]*)(?:-\s+)?[^:#][^:]*:\s*[|>][+-]?\d*\s*$"
)

EXPECTED_STANDARD_WORKFLOW_PINS = {
    "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/setup-python": "6d4fd22b20465ccc0f7354476588e8df7c9ca0e0",
    "actions/upload-artifact": "cf430e030ddbb5b0abf93d22962f4752f3646cd9",
    "actions/dependency-review-action": "bbc44d14a204704ccc493733616cd1e93a0321ec",
    "actions/upload-pages-artifact": "fc324d3547104276b827a68afc52ff2a11cc49c9",
}


def iter_workflow_files(workflows_dir: Path = WORKFLOWS_DIR) -> list[Path]:
    """Return all `.yml` and `.yaml` workflow files in deterministic order."""
    return sorted(
        path
        for path in workflows_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".yml", ".yaml"}
    )


def _strip_yaml_comment(line: str) -> str:
    """Remove trailing YAML `#` comments while preserving `#` inside quotes."""
    in_single = False
    in_double = False
    escaped = False
    for index, ch in enumerate(line):
        if escaped:
            escaped = False
            continue
        if in_double and ch == "\\":
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            if index == 0 or line[index - 1].isspace():
                return line[:index]
    return line


def _unquote_yaml_scalar(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and (
        (stripped[0] == "'" and stripped[-1] == "'")
        or (stripped[0] == '"' and stripped[-1] == '"')
    ):
        return stripped[1:-1].strip()
    return stripped


def _iter_non_scalar_lines(workflow_text: str) -> list[tuple[int, str]]:
    """Return (1-based line_number, comment-stripped line) skipping block scalar bodies."""
    result: list[tuple[int, str]] = []
    scalar_parent_indent: int | None = None
    for line_number, raw_line in enumerate(workflow_text.splitlines(), start=1):
        stripped_ws = raw_line.strip()
        if scalar_parent_indent is not None:
            if not stripped_ws:
                continue
            current_indent = len(raw_line) - len(raw_line.lstrip(" \t"))
            if current_indent > scalar_parent_indent:
                continue
            scalar_parent_indent = None
        cleaned = _strip_yaml_comment(raw_line).rstrip()
        result.append((line_number, cleaned))
        header_match = BLOCK_SCALAR_HEADER_PATTERN.match(cleaned)
        if header_match:
            scalar_parent_indent = len(header_match.group("indent"))
    return result


def extract_uses_references(workflow_text: str) -> list[tuple[int, str]]:
    """Return (line_number, reference) for every block or flow-mapping `uses:` entry."""
    references: list[tuple[int, str]] = []
    for line_number, cleaned in _iter_non_scalar_lines(workflow_text):
        if not cleaned.strip():
            continue
        block_match = BLOCK_USES_LINE_PATTERN.match(cleaned)
        if block_match:
            references.append((line_number, _unquote_yaml_scalar(block_match.group(1))))
            continue
        if "{" in cleaned or "[" in cleaned:
            for flow_match in FLOW_USES_PATTERN.finditer(cleaned):
                references.append(
                    (line_number, _unquote_yaml_scalar(flow_match.group("value")))
                )
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
            normalized = reference.replace("\\", "/")
            parts = normalized.split("/")
            if (
                ".." in parts
                or normalized in {"./", "./."}
                or any(part == "" for part in parts[1:])
            ):
                errors.append(
                    f"{label}:{line_number}: local action reference contains "
                    f"invalid path traversal: {reference}"
                )
            continue
        if not IMMUTABLE_REF_PATTERN.fullmatch(reference):
            errors.append(
                f"{label}:{line_number}: action reference is not pinned to a "
                f"40-char lowercase commit SHA: {reference}"
            )
    return errors


def _validate_flow_permissions_mapping(
    raw_mapping: str, label: str, line_number: int, scope_label: str
) -> list[str]:
    inner = raw_mapping[1:-1].strip()
    if not inner:
        return []
    errors: list[str] = []
    for item in inner.split(","):
        entry = item.strip()
        if not FLOW_PERMISSION_ENTRY_PATTERN.fullmatch(entry):
            errors.append(
                f"{label}:{line_number}: invalid {scope_label} permissions entry: {entry!r}"
            )
    return errors


def validate_workflow_permissions(workflow_text: str, label: str) -> list[str]:
    """Fail closed on missing/duplicate top-level or broad job-level `permissions:` blocks."""
    errors: list[str] = []
    non_scalar_lines = _iter_non_scalar_lines(workflow_text)
    top_level_count = 0

    for idx, (line_number, cleaned) in enumerate(non_scalar_lines):
        if not cleaned.strip():
            continue
        match = PERMISSIONS_LINE_PATTERN.match(cleaned)
        if match:
            indent_len = len(match.group("indent"))
            is_top_level = indent_len == 0
            scope_label = "top-level" if is_top_level else "job-level"
            if is_top_level:
                top_level_count += 1
                if top_level_count > 1:
                    errors.append(
                        f"{label}:{line_number}: duplicate top-level permissions block"
                    )
            inline_value = match.group("rest").strip()
            if inline_value == "{}":
                continue
            if inline_value.startswith("{") and inline_value.endswith("}"):
                errors.extend(
                    _validate_flow_permissions_mapping(
                        inline_value, label, line_number, scope_label
                    )
                )
                continue
            if inline_value:
                errors.append(
                    f"{label}:{line_number}: {scope_label} permissions must be an explicit "
                    f"scope mapping, not {inline_value!r}"
                )
                continue
            entries = 0
            for sub_line_number, sub_cleaned in non_scalar_lines[idx + 1 :]:
                sub_stripped = sub_cleaned.strip()
                if not sub_stripped:
                    continue
                sub_indent = len(sub_cleaned) - len(sub_cleaned.lstrip(" \t"))
                if sub_indent <= indent_len:
                    break
                if not PERMISSION_ENTRY_PATTERN.match(sub_cleaned):
                    errors.append(
                        f"{label}:{sub_line_number}: invalid {scope_label} permissions entry: {sub_stripped!r}"
                    )
                entries += 1
            if entries == 0:
                errors.append(
                    f"{label}:{line_number}: {scope_label} permissions block is empty"
                )
            continue

        if "{" in cleaned:
            for flow_match in FLOW_PERMISSIONS_PATTERN.finditer(cleaned):
                inline_value = flow_match.group("value").strip()
                if inline_value == "{}":
                    continue
                if inline_value.startswith("{") and inline_value.endswith("}"):
                    errors.extend(
                        _validate_flow_permissions_mapping(
                            inline_value, label, line_number, "job-level"
                        )
                    )
                else:
                    errors.append(
                        f"{label}:{line_number}: job-level permissions must be an explicit "
                        f"scope mapping, not {inline_value!r}"
                    )

    if top_level_count == 0:
        errors.append(f"{label}: missing top-level permissions block")
    return errors


class WorkflowActionPinningTests(unittest.TestCase):
    def test_all_repository_workflows_are_sha_pinned(self):
        workflow_files = iter_workflow_files()
        self.assertTrue(workflow_files, "expected GitHub Actions workflows")
        for workflow_path in workflow_files:
            with self.subTest(workflow=workflow_path.name):
                errors = validate_workflow_pinning(
                    workflow_path.read_text(encoding="utf-8"),
                    workflow_path.name,
                )
                self.assertEqual(errors, [])

    def test_all_repository_workflows_declare_explicit_permissions(self):
        workflow_files = iter_workflow_files()
        self.assertTrue(workflow_files, "expected GitHub Actions workflows")
        for workflow_path in workflow_files:
            with self.subTest(workflow=workflow_path.name):
                errors = validate_workflow_permissions(
                    workflow_path.read_text(encoding="utf-8"),
                    workflow_path.name,
                )
                self.assertEqual(errors, [])

    def test_iter_workflow_files_discovers_both_yml_and_yaml(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            (tmp_dir / "alpha.yml").write_text("name: a\n", encoding="utf-8")
            (tmp_dir / "beta.yaml").write_text("name: b\n", encoding="utf-8")
            (tmp_dir / "README.md").write_text("ignore\n", encoding="utf-8")
            discovered = [p.name for p in iter_workflow_files(tmp_dir)]
            self.assertEqual(discovered, ["alpha.yml", "beta.yaml"])

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
            "./../outside",
            "./actions/../outside",
            "./..\\outside",
            "./",
            "./.",
        ]
        for bad_ref in invalid_references:
            with self.subTest(reference=bad_ref):
                workflow_yaml = f"jobs:\n  test:\n    steps:\n      - uses: {bad_ref}\n"
                errors = validate_workflow_pinning(workflow_yaml, "synthetic.yml")
                self.assertTrue(errors, f"expected fail-closed rejection for {bad_ref}")

        valid_local = "jobs:\n  test:\n    steps:\n      - uses: ./.github/actions/local-check\n"
        self.assertEqual(validate_workflow_pinning(valid_local, "valid-local.yml"), [])

    def test_flow_mapping_unpinned_uses_fails_closed_even_with_pinned_sibling(self):
        flow_cases = {
            "inline_step_mapping": (
                "jobs:\n  test:\n    steps:\n"
                "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n"
                "      - { uses: actions/checkout@v7 }\n"
            ),
            "named_flow_mapping": (
                "jobs:\n  test:\n    steps:\n"
                "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1\n"
                "      - { name: Unpinned, uses: 'actions/setup-python@v7', with: { python-version: '3.12' } }\n"
            ),
            "flow_sequence_mixed": (
                "jobs:\n  test:\n    steps: [\n"
                "      { uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 },\n"
                "      { uses: ./../outside }\n"
                "    ]\n"
            ),
        }
        for case, workflow_yaml in flow_cases.items():
            with self.subTest(case=case):
                errors = validate_workflow_pinning(workflow_yaml, f"{case}.yaml")
                self.assertTrue(errors, f"expected fail-closed rejection for {case}")

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
            "duplicate_top_level_permissions": (
                "name: synthetic\npermissions:\n  contents: read\n"
                "permissions: write-all\njobs: {}\n"
            ),
            "duplicate_valid_top_level_permissions": (
                "name: synthetic\npermissions:\n  contents: read\n"
                "permissions:\n  contents: read\njobs: {}\n"
            ),
            "job_level_write_all": (
                "name: synthetic\npermissions:\n  contents: read\njobs:\n  build:\n"
                "    runs-on: ubuntu-latest\n    permissions: write-all\n"
            ),
            "job_level_read_all": (
                "name: synthetic\npermissions:\n  contents: read\njobs:\n  build:\n"
                "    runs-on: ubuntu-latest\n    permissions: read-all\n"
            ),
            "job_level_invalid_scope": (
                "name: synthetic\npermissions:\n  contents: read\njobs:\n  build:\n"
                "    runs-on: ubuntu-latest\n    permissions:\n      contents: admin\n"
            ),
            "job_level_flow_write_all": (
                "name: synthetic\npermissions:\n  contents: read\njobs:\n"
                "  build: { runs-on: ubuntu-latest, permissions: write-all }\n"
            ),
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

    def test_valid_job_level_permissions_block_passes(self):
        workflow_yaml = (
            "name: synthetic\n"
            "permissions:\n"
            "  contents: read\n"
            "jobs:\n"
            "  attest:\n"
            "    runs-on: ubuntu-latest\n"
            "    permissions:\n"
            "      contents: read\n"
            "      id-token: write\n"
        )
        self.assertEqual(validate_workflow_permissions(workflow_yaml, "valid-job.yaml"), [])


if __name__ == "__main__":
    unittest.main()
