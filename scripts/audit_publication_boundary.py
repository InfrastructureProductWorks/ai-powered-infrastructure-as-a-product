#!/usr/bin/env python3
"""Freeze explicit historical disclosures; reject current restricted coordinates."""
from collections import Counter
import hashlib
import html
import os
from urllib.parse import unquote
import json
from pathlib import Path
import re
import posixpath
import subprocess
import stringprep
import sys

ROOT=Path(__file__).resolve().parents[1]
NAMES=('iaap-'+'guard-core','iaap-'+'forge','iaap-'+'console','iaap-'+'assurance','vanguard-'+'suite',
       'backstage-infrastructure-product-'+'storefront-poc','crossplane-multicloud-seed-'+'poc',
       'multicloud-foundation-product-'+'poc','composite-ai-infrastructure-product-'+'poc','multicloud-foundation-poc-'+'integration')
PATTERN=re.compile(r'(?:InfrastructureProductWorks|SAABOLImpactVenture)/(?:'+ '|'.join(map(re.escape,NAMES))+r')(?![\w-])|\"(?:closureSha|workflowRunId|iamRoleArn|secretArn)\"\s*:',re.I)


def normalize_hostnames(text, preserve_url_controls=False):
    controls=str.maketrans({'\t':None,'\n':None,'\r':None})
    if not preserve_url_controls:
        text=re.sub(r'(?is)(\b(?:href|src|action)\s*=\s*)(["\'])(.*?)\2',lambda m:m.group(1)+m.group(2)+m.group(3).translate(controls)+m.group(2),text)
        text=re.sub(r'\]\(([^)]+)\)',lambda m:']('+m.group(1).translate(controls)+')',text)
    text=text.translate(str.maketrans({'。':'.','．':'.','｡':'.'}))
    def host(match):
        hostname=match.group(2) if preserve_url_controls else match.group(2).translate(controls)
        if preserve_url_controls:
            # An ASCII boundary marker prevents a match from restarting after
            # a leading control and stops IDNA from silently erasing it.
            hostname=''.join('_' if c.isspace() or stringprep.in_table_b1(c) or not html.unescape('&#%d;'%ord(c)) else c for c in hostname)
        try:normalized=hostname.encode('idna').decode('ascii')
        except UnicodeError:return match.group(0)
        return match.group(1)+normalized
    return re.sub(r"((?:[A-Za-z][A-Za-z0-9+.-]*:/+|git@))([^/ :?#\"'()<>\[\]]+)",host,text)

def retain_numeric_boundary(match):
    # HTML unescaping can erase numeric controls and noncharacters entirely.
    # Retain them and whitespace for the original-token App-route check.
    try:
        value=chr(int(match.group(1)[1:],16) if match.group(1).lower().startswith('x') else int(match.group(1)))
    except (ValueError,OverflowError):return match.group(0)
    if not html.unescape(match.group(0)):return '_'
    return value if value.isspace() else match.group(0)

def normalization_views(text, preserve_url_controls=False):
    yield text
    for normalization_step in range(9):
        prior=text
        text=unquote(text)
        # Keep wrapper scopes visible before a different decoder can introduce
        # a closing delimiter inside their URL destination.
        if text!=prior:yield text
        if preserve_url_controls:text=re.sub(r'&#(x[0-9a-f]+|[0-9]+);?',retain_numeric_boundary,text,flags=re.I)
        html_source=text
        text=html.unescape(text).replace('\\/', '/')
        if text!=html_source:yield text
        unicode_source=text
        text=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m.group(1),16)),text)
        if text!=unicode_source:yield text
        # A decoded backslash can start another Unicode escape. Preserve it
        # for the next bounded pass instead of destroying it as a path slash.
        text=re.sub(r'\\(?!u[0-9a-fA-F]{4})','/',text)
        text=re.sub(r'/+', '/', text)
        text=normalize_hostnames(text,preserve_url_controls)
        if text==prior:return
        if normalization_step==8:raise ValueError("Publication text exceeds the bounded normalization limit")
        yield text

def normalize(text, preserve_url_controls=False):
    return list(normalization_views(text,preserve_url_controls))[-1]

PUBLIC_REPOSITORIES={'infrastructureproductworks/enterprise-azure-governance', 'saabolimpactventure/iaap-guard', 'infrastructureproductworks/infrastructureproductworks.github.io', 'saabolimpactventure/ai-powered-infrastructure-as-a-product', 'infrastructureproductworks/ai-powered-infrastructure-as-a-product', 'infrastructureproductworks/.github', 'infrastructureproductworks/iaap-guard'}
OWNED_COORDINATE=re.compile('(InfrastructureProductWorks|SAABOLImpactVenture)/([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)',re.I)
GITHUB_COORDINATE=re.compile(r'(?<![A-Za-z0-9_.-])(?:(?:www\.)?github\.dev\.?(?::[0-9]*)?/|vscode\.dev\.?(?::[0-9]*)?/github/|api\.github\.com\.?(?::[0-9]*)?/repos/|(?!docs\.github\.com)(?:[A-Za-z0-9-]+\.)*github\.com\.?(?::[0-9]*)?/|raw\.githubusercontent\.com\.?(?::[0-9]*)?/|(?:[A-Za-z0-9_.-]+@)?(?:ssh\.)?github\.com\.?(?::[0-9]*)?[:/])([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)',re.I)
# Search qualifiers carry repository identities even without a GitHub host.
QUALIFIED_COORDINATE=re.compile(r"(?<![A-Za-z0-9_.-])(?:repo|repository)\s*:\s*[\"']?([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)",re.I)
# A query or fragment can contain a raw coordinate without a repo: qualifier.
# Scan the remainder of its line conservatively, including decoded spaces/quotes.
GITHUB_QUERY=re.compile(r"(?<![A-Za-z0-9_.-])(?:(?:[A-Za-z0-9-]+\.)*github\.(?:com|dev)|raw\.githubusercontent\.com|vscode\.dev)\.?(?::[0-9]*)?/?[^\s<>?#]*[?#]([^\r\n<>]*)",re.I)
QUERY_COORDINATE=re.compile(r"(?<![A-Za-z0-9_.-])([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)")

def query_coordinate_matches(text):
    for query in GITHUB_QUERY.finditer(text):
        for match in QUERY_COORDINATE.finditer(normalize(query.group(1))):yield match

def coordinate_matches(text):
    for match in OWNED_COORDINATE.finditer(text):yield match
    for match in QUALIFIED_COORDINATE.finditer(text):yield match
    yield from query_coordinate_matches(text)
    for match in GITHUB_COORDINATE.finditer(text):
        yield match

def coordinate_key(match):
    return '/'.join(posixpath.normpath(match.group(1)+'/'+match.group(2)).lower().split('/')[:2]).removesuffix('.git')

def coordinate_allowed(match, approved):
    if any(part in {'.','..'} for part in (match.group(1)+'/'+match.group(2)).split('/')):return False
    key=coordinate_key(match)
    if key in approved:return True
    # API search routes are not repositories; their queries are scanned separately.
    if re.fullmatch(r'api\.github\.com\.?/search/(?:code|commits|issues|labels|repositories|topics|users)',match.group(0),re.I):return True
    # The public App is one exact web route, never a repository/query/SCP alias.
    if not re.fullmatch(r'(?:www\.)?'+'github'+r'\.com\.?/apps/'+'iaap-guard'+r'(?:/installations/new)?',match.group(0),re.I):return False
    tail=match.string[match.end():]
    if not tail or tail[0].isspace():return True
    # Permit source markup terminators, never an arbitrary route suffix.
    before=match.string[:match.start()]
    if tail.startswith(')') and re.search(r'\]\((?:https?:/)?$',before,re.I):
        return len(tail)==1 or tail[1].isspace() or tail[1] in '.,;:*_)]'
    attribute=re.search(r"\b(?:href|src|action)\s*=\s*([\"'])(?:https?:/)?$",before,re.I)
    if attribute and tail.startswith(attribute.group(1)):
        return len(tail)==1 or tail[1].isspace() or tail[1] in '/>'
    quoted=re.search(r"([\"'])(?:https?:/)?$",before,re.I)
    if quoted and tail.startswith(quoted.group(1)):
        return len(tail)==1 or tail[1].isspace() or tail[1] in ',)}]'
    if tail.startswith('>') and re.search(r'<(?:https?:/)?$',before,re.I):return True
    return False


MARKDOWN_ESCAPE=re.compile(r'\\([!-/:-@\[-`{-~])')

def restricted(text):
    for view in (text,MARKDOWN_ESCAPE.sub(lambda m:m.group(1),text)):
        # Inspect queries before decoding can introduce a lexical delimiter.
        # Materialize first so the same normalization bound remains fail-closed.
        views=list(normalization_views(view))
        # Preserve original URL-token scope when host and query delimiters are
        # decoded together. Decoded controls/angles cannot truncate that token.
        tokens=re.findall(r'[^\s<>]+',view)
        scoped_urls=[]
        for scoped_view in views:
            scoped_urls.extend(m.group(2) for m in re.finditer(r"(?is)\b(?:href|src|action)\s*=\s*([\"'])(.*?)\1",scoped_view))
            scoped_urls.extend(m.group(2) for m in re.finditer(r"([\"'])((?:https?:/+|github[.]com/).*?)\1",scoped_view,re.I))
            scoped_urls.extend(re.findall(r'\]\(([^)]+)\)',scoped_view))
            scoped_urls.extend(re.findall(r'<([^<>\s]+)>',scoped_view))
        for url in scoped_urls:
            decoded_url=normalize(url.strip())
            for match in GITHUB_COORDINATE.finditer(decoded_url):
                if coordinate_key(match)=='apps/'+'iaap-guard':
                    tail=decoded_url[match.end():]
                    if not coordinate_allowed(match,PUBLIC_REPOSITORIES) or tail:return True
        tokens.extend(scoped_urls)
        for token in tokens:
            if not any(marker in token for marker in ('?', '#', '%', '&', '\\')):continue
            token_view=normalize(token,preserve_url_controls=True)
            browser_view=normalize(token)
            retained_apps=Counter(m.group(0).lower() for m in GITHUB_COORDINATE.finditer(token_view) if coordinate_key(m)=='apps/'+'iaap-guard' and coordinate_allowed(m,PUBLIC_REPOSITORIES))
            browser_apps=Counter(m.group(0).lower() for m in GITHUB_COORDINATE.finditer(browser_view) if coordinate_key(m)=='apps/'+'iaap-guard' and coordinate_allowed(m,PUBLIC_REPOSITORIES))
            # Erasing a character inside the host or App name must not create
            # an allowed route. Differences only in surrounding prose are fine.
            if browser_apps-retained_apps:return True
            # Whitespace created inside an original token is a route suffix,
            # not a harmless boundary between the exact App URL and prose.
            for match in GITHUB_COORDINATE.finditer(token_view):
                tail=token_view[match.end():]
                if coordinate_key(match)=='apps/'+'iaap-guard':
                    if not coordinate_allowed(match,PUBLIC_REPOSITORIES) or (tail and tail[0].isspace()):return True
            query_view=browser_view.translate(str.maketrans({'\r':' ','\n':' ','\t':' ','<':' ','>':' '}))
            if any(not coordinate_allowed(m, PUBLIC_REPOSITORIES) for m in query_coordinate_matches(query_view)):
                return True
        for encoded in views[:-1]:
            if any(not coordinate_allowed(m, PUBLIC_REPOSITORIES) for m in query_coordinate_matches(encoded)):
                return True
        decoded=views[-1]
        if PATTERN.search(decoded) or any(not coordinate_allowed(m, PUBLIC_REPOSITORIES) for m in coordinate_matches(decoded)):
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
