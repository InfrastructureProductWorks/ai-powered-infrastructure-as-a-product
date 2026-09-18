#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "config/ghe06-restricted-profile.json"

def main():
    data = json.loads(PROFILE.read_text(encoding="utf-8"))
    assert data["schemaVersion"] == "accelerator-ghe06-restricted-profile/v1"
    assert data["supportClaim"] is False
    assert data["executionClaimed"] is True
    for path in data["acceptedCore"]:
        assert (ROOT / path).is_file(), path
    for field in (
        "documentationToolchainDisposition",
        "opaCliDisposition",
        "mermaidCdnDisposition",
        "githubPagesDisposition",
        "attestationServiceDisposition",
        "githubActionsDisposition",
        "externalModelDisposition",
        "telemetryDisposition",
    ):
        assert data[field].startswith(("disabled", "hosted_orchestration_only")), field
    assert data["liveCloudDisposition"] == "fixture_only_or_disabled"

    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    assert 'opa not installed; CI performs policy validation' in makefile
    assert 'mkdocs not installed; CI performs docs validation' in makefile
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "https://unpkg.com/mermaid@" in mkdocs
    print("Accelerator GHE-06 restricted core profile verified")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
