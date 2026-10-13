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


def normalize_hostnames(text):
    controls=str.maketrans({'\t':None,'\n':None,'\r':None})
    text=re.sub(r'(?is)(\b(?:href|src|action)\s*=\s*)(["\'])(.*?)\2',lambda m:m.group(1)+m.group(2)+m.group(3).translate(controls)+m.group(2),text)
    text=re.sub(r'\]\(([^)]+)\)',lambda m:']('+m.group(1).translate(controls)+')',text)
    text=text.translate(str.maketrans({'。':'.','．':'.','｡':'.'}))
    def host(match):
        try:normalized=match.group(2).translate(controls).encode('idna').decode('ascii')
        except UnicodeError:return match.group(0)
        return match.group(1)+normalized
    return re.sub(r"((?:[A-Za-z][A-Za-z0-9+.-]*:/+|git@))([^/ :?#\"'()<>\[\]]+)",host,text)

def normalize(text):
    for normalization_step in range(9):
        prior=text
        text=html.unescape(unquote(text)).replace('\\/', '/')
        text=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m.group(1),16)),text)
        text=text.replace('\\', '/')
        text=re.sub(r'/+', '/', text)
        text=normalize_hostnames(text)
        if text==prior:break
        if normalization_step==8:raise ValueError("Publication text exceeds the bounded normalization limit")
    return text

PUBLIC_REPOSITORIES={'infrastructureproductworks/enterprise-azure-governance', 'saabolimpactventure/iaap-guard', 'infrastructureproductworks/infrastructureproductworks.github.io', 'saabolimpactventure/ai-powered-infrastructure-as-a-product', 'infrastructureproductworks/ai-powered-infrastructure-as-a-product', 'infrastructureproductworks/.github', 'infrastructureproductworks/iaap-guard'}
OWNED_COORDINATE=re.compile('(InfrastructureProductWorks|SAABOLImpactVenture)/([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)',re.I)
GITHUB_COORDINATE=re.compile(r'(?<![A-Za-z0-9_.-])(?:(?:www\.)?github\.dev\.?(?::[0-9]*)?/|vscode\.dev\.?(?::[0-9]*)?/github/|api\.github\.com\.?(?::[0-9]*)?/repos/|(?!docs\.github\.com)(?:[A-Za-z0-9-]+\.)*github\.com\.?(?::[0-9]*)?/|raw\.githubusercontent\.com\.?(?::[0-9]*)?/|(?:[A-Za-z0-9_.-]+@)?(?:ssh\.)?github\.com\.?(?::[0-9]*)?[:/])([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)',re.I)
PUBLIC_UI_COORDINATES={'apps/iaap-guard'}

def coordinate_matches(text):
    for match in OWNED_COORDINATE.finditer(text):yield match
    for match in GITHUB_COORDINATE.finditer(text):
        yield match

def coordinate_key(match):
    return '/'.join(posixpath.normpath(match.group(1)+'/'+match.group(2)).lower().split('/')[:2]).removesuffix('.git')

def coordinate_allowed(match, approved):
    key=coordinate_key(match)
    return key in approved or match.group(0).lower().startswith(('github.com','www.github.com')) and key in PUBLIC_UI_COORDINATES


MARKDOWN_ESCAPE=re.compile(r'\\([!-/:-@\[-`{-~])')

def restricted(text):
    for view in (text,MARKDOWN_ESCAPE.sub(lambda m:m.group(1),text)):
        view=normalize(view)
        if PATTERN.search(view) or any(not coordinate_allowed(m, PUBLIC_REPOSITORIES) for m in coordinate_matches(view)):
            return True
    return False

def public_text(raw, path=None):
    if raw.startswith((b'\xff\xfe\x00\x00',b'\x00\x00\xfe\xff')):return raw.decode('utf-32')
    if raw.startswith((b'\xff\xfe',b'\xfe\xff')):return raw.decode('utf-16')
    if b'\x00' in raw and path and Path(path).suffix.lower() not in {'.png','.jpg','.jpeg','.webp','.gif','.ico','.pdf'}:
        raise ValueError('NUL-bearing text without a supported BOM is not publishable')
    return raw.decode('utf-8-sig',errors='replace')

def public_bytes(path):
    if path.is_symlink():return os.readlink(path).encode('utf-8')
    if path.is_file():return path.read_bytes()
    return None

def audit(root, base_ref=None):
    format_errors=[]
    entries=subprocess.check_output(['git','ls-files','--stage','-z'],cwd=root,text=True).split('\0')
    for entry in entries:
        if entry and entry.startswith('160000 '):format_errors.append('Submodules are not part of the public thesis surface')
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=root,text=True)
    attributes=subprocess.check_output(['git','check-attr','--stdin','-z','filter'],cwd=root,input=tracked,text=True).split('\0')
    for index in range(0,len(attributes)-2,3):
        if attributes[index+2]=='lfs':format_errors.append('Git LFS payloads require a different reviewed publication path')
    exceptions=json.loads((root/'config/publication-history.json').read_text())
    errors=list(format_errors)
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
                if hashlib.sha256(old).hexdigest()!=digest or not restricted(public_text(old,name)):
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
        if path.name=='.gitmodules':errors.append(name+': submodule coordinates are not publishable')
        if raw.startswith(b'version https://' + b'git-lfs.github.com' + b'/spec/v1'):
            errors.append(name+': opaque Git LFS pointer is not publishable')
        if restricted(public_text(raw,name)):
            if exceptions.get(name)!=hashlib.sha256(raw).hexdigest():
                errors.append(name+': restricted coordinates are not an unchanged historical disclosure')
    return errors

if __name__=='__main__':
    base=os.environ.get('PUBLICATION_BASE_SHA')
    errors=audit(ROOT,base) if base or os.environ.get('GITHUB_ACTIONS')!='true' else ['trusted publication baseline is required in CI']
    for error in errors:print(error)
    print('Public publication boundary: '+('FAIL' if errors else 'PASS'))
    sys.exit(bool(errors))
