#!/usr/bin/env python3
"""Freeze explicit historical disclosures; reject current restricted coordinates."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
NAMES=('iaap-'+'guard-core','iaap-'+'forge','iaap-'+'console','iaap-'+'assurance','vanguard-'+'suite',
       'backstage-infrastructure-product-'+'storefront-poc','crossplane-multicloud-seed-'+'poc',
       'multicloud-foundation-product-'+'poc','composite-ai-infrastructure-product-'+'poc','multicloud-foundation-poc-'+'integration')
PATTERN=re.compile(r'(?:InfrastructureProductWorks|SAABOLImpactVenture)/(?:'+ '|'.join(map(re.escape,NAMES))+r')(?![\w.-])|\"(?:closureSha|workflowRunId|iamRoleArn|secretArn)\"\s*:',re.I)

def audit(root):
    exceptions=json.loads((root/'config/publication-history.json').read_text())
    errors=[]
    for name in subprocess.check_output(['git','ls-files'],cwd=root,text=True).splitlines():
        path=root/name
        if not path.is_file():continue
        raw=path.read_bytes()
        if PATTERN.search(raw.decode('utf-8',errors='replace')):
            if exceptions.get(name)!=hashlib.sha256(raw).hexdigest():
                errors.append(name+': restricted coordinates are not an unchanged historical disclosure')
    return errors

if __name__=='__main__':
    errors=audit(ROOT)
    for error in errors:print(error)
    print('Public publication boundary: '+('FAIL' if errors else 'PASS'))
    sys.exit(bool(errors))
