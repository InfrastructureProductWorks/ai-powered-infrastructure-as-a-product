"""Verify JSON and the registered phase manifests without cloud calls."""
import json
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for path in ROOT.rglob("*.json"):
    if ".git" not in path.relative_to(ROOT).parts:
        json.loads(path.read_text())
expected = {"artifacts/phase-23/MANIFEST.sha256", "artifacts/phase-24/MANIFEST.sha256"}
actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "artifacts").rglob("MANIFEST.sha256")}
if actual != expected:
    raise SystemExit("Phase manifest set is missing, renamed, or unregistered")
for manifest in sorted(expected):
    subprocess.run(["/usr/bin/sha256sum", "--check", manifest], cwd=ROOT, check=True)
print("JSON and phase manifests verified")
