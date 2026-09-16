# EP-08 GHE-04: AI-powered IaaP self-hosted validation

The maintained accelerator has executable boundary, provenance, and evidence validation. Its opt-in self-hosted path runs those checks and builds the documentation strictly. It is included in the portfolio GHE-04 inventory.

Only `repository_dispatch` with type `ghe04-self-hosted-validation` can trigger the workflow. Checkout uses immutable `github.sha`, read-only repository permission, and no persisted credentials. The fixed labels are `[self-hosted, linux, x64, iaap-accelerator-ghe04]`; operators assign the dedicated label only to approved runners. Caller-selected branches, groups, labels, and commands are unsupported.

The operator supplies 64-bit CPython 3.12 with venv support at `/usr/bin/python3`, Bash at `/usr/bin/bash`, and standard Linux tools under `/usr/bin:/bin`. Inherited Bash, Python, Make, and pip controls are cleared. The path verifies the tracked provenance statement without refreshing it, runs fail-closed provenance and workflow tests, validates JSON evidence and the registered phase manifests, then installs the pinned documentation requirements in a per-run temporary environment and runs `mkdocs build --strict`.

Documentation dependencies and generated site files live under a run-specific directory beneath `RUNNER_TEMP`, outside repository scans. Cleanup independently derives that directory in an `always()` step; deletion failures fail the job. Package installation needs an operator-approved reachable package source. This does not establish restricted-egress support.

The hosted CI enforces the complete workflow contract; Make exposes the same contract check. Hosted documentation publication, dependency/security scanning, and provenance attestation remain separate baselines. This bounded path does not publish a site, mint an attestation, install infrastructure, or invoke cloud/AI services.

Implementation and local synthetic validation are not evidence of customer-runner execution or live GHES acceptance. Private CA, proxy, and restricted-network acceptance remain GHE-05/GHE-06 work. No approval, merge, provisioning, cloud, privilege, production, or policy authority is added.

Checkout is limited to 2 minutes, validation to 20 minutes, and workflow-level cleanup to 5 minutes within the 30-minute job. These limits reserve time for cleanup when a validation command stalls; abrupt host loss remains an operator recovery responsibility.
