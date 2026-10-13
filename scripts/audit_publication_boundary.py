#!/usr/bin/env python3
"""Freeze explicit historical disclosures; reject current restricted coordinates."""
import hashlib
import html
import os
from urllib.parse import unquote
import json
from pathlib import Path
import re
import posixpath
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
NAMES=('iaap-'+'guard-core','iaap-'+'forge','iaap-'+'console','iaap-'+'assurance','vanguard-'+'suite',
       'backstage-infrastructure-product-'+'storefront-poc','crossplane-multicloud-seed-'+'poc',
       'multicloud-foundation-product-'+'poc','composite-ai-infrastructure-product-'+'poc','multicloud-foundation-poc-'+'integration')
PATTERN=re.compile(r'(?:InfrastructureProductWorks|SAABOLImpactVenture)/(?:'+ '|'.join(map(re.escape,NAMES))+r')(?![\w-])|\"(?:closureSha|workflowRunId|iamRoleArn|secretArn)\"\s*:',re.I)

def normalize(text):
    for _ in range(8):
        prior=text
        text=html.unescape(unquote(text)).replace('\\/', '/')
        text=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m.group(1),16)),text)
        text=text.replace('\\', '/')
        text=re.sub(r'/+', '/', text)
        if text==prior:break
    return text

PUBLIC_SLUGS={'infrastructureproductworks.github.io','ai-powered-infrastructure-as-a-product','iaap-guard','enterprise-azure-governance','.github'}
OWNED_COORDINATE=re.compile(r'(?:InfrastructureProductWorks|SAABOLImpactVenture)/([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)',re.I)

def restricted(text):
    text=normalize(text)
    return bool(PATTERN.search(text)) or any(posixpath.normpath(m.group(1)).split('/')[0].lower().rstrip('.').removesuffix('.git') not in PUBLIC_SLUGS for m in OWNED_COORDINATE.finditer(text))

def public_bytes(path):
    if path.is_symlink():return os.readlink(path).encode('utf-8')
    if path.is_file():return path.read_bytes()
    return None

def audit(root, base_ref=None):
    exceptions=json.loads((root/'config/publication-history.json').read_text())
    errors=[]
    if base_ref:
        try:
            subprocess.check_output(['git','rev-parse','--verify',base_ref+'^{commit}'],cwd=root,stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            return ['trusted publication baseline could not be resolved']
        try:
            prior=json.loads(subprocess.check_output(['git','show',base_ref+':config/publication-history.json'],cwd=root,stderr=subprocess.DEVNULL))
        except subprocess.CalledProcessError:
            prior=None
        if prior is not None and set(prior)-set(exceptions):
            errors.append('historical exception entries were removed')
        for name,digest in exceptions.items():
            if prior is not None:
                if prior.get(name)!=digest:errors.append(name+': historical exception changed or added in this change')
            else:
                # First adoption may grandfather only bytes already present in the trusted base.
                try:old=subprocess.check_output(['git','show',base_ref+':'+name],cwd=root,stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:old=b''
                if hashlib.sha256(old).hexdigest()!=digest or not restricted(old.decode('utf-8',errors='replace')):
                    errors.append(name+': exception was not a pre-existing public disclosure')
    for name,digest in exceptions.items():
        raw=public_bytes(root/name)
        if raw is None or hashlib.sha256(raw).hexdigest()!=digest:
            errors.append(name+': historical evidence bytes changed or disappeared')
    for name in subprocess.check_output(['git','ls-files','-z'],cwd=root,text=True).split('\0'):
        if not name:continue
        path=root/name
        raw=public_bytes(path)
        if raw is None:continue
        if restricted(raw.decode('utf-8',errors='replace')):
            if exceptions.get(name)!=hashlib.sha256(raw).hexdigest():
                errors.append(name+': restricted coordinates are not an unchanged historical disclosure')
    return errors

if __name__=='__main__':
    base=os.environ.get('PUBLICATION_BASE_SHA')
    errors=audit(ROOT,base) if base or os.environ.get('GITHUB_ACTIONS')!='true' else ['trusted publication baseline is required in CI']
    for error in errors:print(error)
    print('Public publication boundary: '+('FAIL' if errors else 'PASS'))
    sys.exit(bool(errors))
