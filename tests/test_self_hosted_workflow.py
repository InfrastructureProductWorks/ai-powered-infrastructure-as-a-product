"""Regress the self-hosted trust boundary and Make recipe interpreter."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ghe04_contract", ROOT / "scripts/validate_self_hosted_workflow.py")
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)

class SelfHostedContractTests(unittest.TestCase):
    def test_accepted_contract(self):
        self.assertEqual(contract.main(), 0)

    def test_workflow_mutations_fail_closed(self):
        accepted = contract.WORKFLOW.read_text()
        substitutions = [
            ("timeout-minutes: 20", "timeout-minutes: 30"),
            ("timeout-minutes: 2", "timeout-minutes: 30"),
            ("repository_dispatch:", "workflow_dispatch:"),
            ("contents: read", "contents: write"),
            ("ref: ${{ github.sha }}", "ref: main"),
            ("persist-credentials: false", "persist-credentials: true"),
            ("self-hosted, linux, x64", "ubuntu-latest"),
            ("if: always()", "if: success()"),
        ]
        for before, after in substitutions:
            with self.subTest(before=before):
                self.assertIn(before, accepted)
                with tempfile.TemporaryDirectory() as directory:
                    candidate = Path(directory) / "workflow.yml"
                    candidate.write_text(accepted.replace(before, after))
                    with patch.object(contract, "WORKFLOW", candidate):
                        with self.assertRaises(SystemExit):
                            contract.main()

if __name__ == "__main__":
    unittest.main()
