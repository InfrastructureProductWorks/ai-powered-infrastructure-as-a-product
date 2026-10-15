import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_publication_boundary import audit, restricted, normalize

class PublicationBoundaryTests(unittest.TestCase):
    def test_repository_search_and_query_coordinates(self):
        from urllib.parse import quote
        private=''.join(('PrivatePartner/', 'secret-repo'))
        public='InfrastructureProductWorks/iaap-guard'
        forms=[
            'repo:{coordinate}', 'repository: "{coordinate}"',
            'https://github.com/search?q=repo:{coordinate}',
            'https://github.com/search?q=repo:%22{coordinate}%22&type=code',
            'https://github.com/search?q={coordinate}',
            'https://github.com/search?repository={coordinate}',
            'https://github.com/search#q={coordinate}',
            'https://api.github.com/search/code?q=repo:{coordinate}',
            'https://api.github.com/search/repositories?q=repo:{coordinate}',
            'https://github.dev/?repo={coordinate}',
            'https://vscode.dev/github?repository={coordinate}',
            'https://github.com/search?q=label:bug+repo:{coordinate}',
        ]
        for form in forms:
            for coordinate in [private, private+'.git', 'InfrastructureProductWorks/iaap-guard'+'/../../'+private, private+'/../../'+'InfrastructureProductWorks/iaap-guard']:
                text=form.format(coordinate=coordinate)
                for _ in range(4):
                    with self.subTest(text=text):self.assertTrue(restricted(text))
                    text=quote(text,safe='')
            public_text=form.format(coordinate=public)
            for _ in range(4):
                with self.subTest(public=public_text):self.assertFalse(restricted(public_text))
                public_text=quote(public_text,safe='')

    def test_encoded_query_delimiters_do_not_hide_coordinates(self):
        from urllib.parse import quote
        private=''.join(('PrivatePartner/','secret-repo'))
        for host in ['https://github.com','https://github.com/search','https://api.github.com/search/code']:
            for delimiter in ['%0A','%0D','%09','%3C','%3E','%22','%27']:
                text=host+'?q='+delimiter+private
                for _ in range(4):
                    with self.subTest(text=text):self.assertTrue(restricted(text))
                    text=quote(text,safe='')
                from urllib.parse import unquote
                text=quote(host+'?q='+unquote(delimiter)+private,safe='')
                for _ in range(4):
                    with self.subTest(encoded_host=text):self.assertTrue(restricted(text))
                    text=quote(text,safe='')

    def test_quoted_url_scope_survives_literal_angles(self):
        private=''.join(('PrivatePartner/','secret-repo'))
        for delimiter in ['<','>','\r','\n','\t']:
            url='https://github.com/search?q='+delimiter+private
            for text in ['<a href="'+url+'">Search</a>', "<a href='"+url+"'>Search</a>", '[Search]('+url+')']:
                with self.subTest(text=text):self.assertTrue(restricted(text))

    def test_app_exception_is_an_exact_web_route(self):
        for host in ['github.com','www.github.com','github.com.']:
            for suffix in ['', '/installations/new']:
                self.assertFalse(restricted('https://'+host+'/apps/iaap-guard'+suffix))
        app='apps/'+'iaap-guard'
        for text in [
            'github.com:'+'apps/iaap-guard', 'git@github.com:'+'apps/iaap-guard',
            'https://github.com/apps/iaap-guard'+'/secret-repo',
            'repo:'+app, 'https://github.com/search?q='+app,
        ]:
            self.assertTrue(restricted(text),text)
        self.assertTrue(restricted('https://api.github.com/'+''.join(('PrivatePartner/','secret-repo'))))

    def test_query_disclosure_is_rejected_by_trusted_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir();(root/'scripts').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            (root/'config/publication-history.json').write_text('{}')
            (root/'scripts/audit_publication_boundary.py').write_text('raise SystemExit(0)')
            value='https://github.com/search?q=repo%3A'+''.join(('PrivatePartner%2F','secret-repo'))
            (root/'new.md').write_text(value)
            subprocess.run(['git','add','.'],cwd=root,check=True)
            self.assertTrue(audit(root))

    def test_trusted_workflow_keeps_candidate_data_only(self):
        workflow=(Path(__file__).resolve().parents[1]/'.github/workflows/trusted-publication-boundary.yml').read_text()
        candidate=workflow.split('- name: Check out candidate bytes without executing them')[1].split('- name:')[0]
        trusted=workflow.split('- name: Check out independently anchored validator')[1].split('- name:')[0]
        self.assertIn('allow-unsafe-pr-checkout: true',candidate)
        self.assertIn('persist-credentials: false',candidate)
        self.assertIn('persist-credentials: false',trusted)
        self.assertIn('contents: read',workflow)
        self.assertNotIn('write',workflow)
        self.assertRegex(trusted,r'ref: [a-f0-9]{40}\n')
        self.assertIn("python3 -I - <<'PY'",workflow)
        self.assertIn("pathlib.Path('trusted/scripts/audit_publication_boundary.py')",workflow)
        self.assertNotIn('uses: ./candidate',workflow)
        self.assertNotIn('working-directory: candidate',workflow)

    def test_pinned_validator_matches_reviewed_detector(self):
        import re
        root=Path(__file__).resolve().parents[1]
        workflow=(root/'.github/workflows/trusted-publication-boundary.yml').read_text()
        trusted=workflow.split('- name: Check out independently anchored validator')[1].split('- name:')[0]
        revision=re.search(r'ref: ([a-f0-9]{40})\n',trusted).group(1)
        pinned=subprocess.check_output(['git','show',revision+':scripts/audit_publication_boundary.py'],cwd=root)
        self.assertEqual(pinned,(root/'scripts/audit_publication_boundary.py').read_bytes())

    def test_optional_ssh_username(self):
        for prefix in ['github.com:','alice@github.com:']:
            self.assertTrue(restricted(prefix+''.join(('PrivatePartner/','secret-repo.git'))))

    def test_candidate_validator_tampering_cannot_disable_trusted_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir();(root/'scripts').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            (root/'config/publication-history.json').write_text('{}')
            (root/'scripts/audit_publication_boundary.py').write_text('raise SystemExit(0)')
            (root/'new.md').write_text('https://github.com/'+''.join(('PrivatePartner/','secret-repo')))
            subprocess.run(['git','add','.'],cwd=root,check=True)
            self.assertTrue(audit(root))

    def test_historical_exception_requires_exact_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            path=root/'historical.md'
            path.write_text('InfrastructureProductWorks/'+'iaap-'+'forge')
            (root/'config/publication-history.json').write_text(json.dumps({'historical.md':hashlib.sha256(path.read_bytes()).hexdigest()}))
            subprocess.run(['git','add','.'],cwd=root,check=True)
            self.assertEqual(audit(root),[])
            path.write_text(path.read_text()+' new detail')
            self.assertTrue(audit(root))
            path.write_text('Public product guidance')
            self.assertTrue(audit(root))
    def test_new_reference_has_no_inherited_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            (root/'config/publication-history.json').write_text('{}')
            (root/'new.md').write_text('SAABOLImpactVenture/'+'iaap-'+'console')
            subprocess.run(['git','add','.'],cwd=root,check=True)
            self.assertTrue(audit(root))

    def test_exception_cannot_be_added_or_changed_with_disclosure(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            policy=root/'config/publication-history.json';policy.write_text('{}')
            subprocess.run(['git','add','.'],cwd=root,check=True)
            subprocess.run(['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','base'],cwd=root,check=True)
            value=root/'new.md';value.write_text('InfrastructureProductWorks/'+'iaap-'+'forge.git')
            policy.write_text(json.dumps({'new.md':hashlib.sha256(value.read_bytes()).hexdigest()}))
            subprocess.run(['git','add','.'],cwd=root,check=True)
            self.assertTrue(audit(root,'HEAD'))

    def test_clone_and_encoded_coordinates_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            (root/'config/publication-history.json').write_text('{}')
            value=root/'new.md';value.touch()
            subprocess.run(['git','add','.'],cwd=root,check=True)
            name='InfrastructureProductWorks/'+'iaap-'+'forge.git'
            for text in ['https://github.com/'+name,'git@github.com:'+name,'https://github.com/'+name.replace('/', '\\'),name.replace('/','%2F'),'https://github.com/'+''.join(('InfrastructureProductWorks/','iaap-guard/../','private-','producer')),name.replace('/', '\\/'),''.join('\\u%04x'%ord(c) for c in name)]:
                value.write_text(text)
                self.assertTrue(audit(root),text)

    def test_historical_artifact_and_exception_cannot_both_disappear(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            artifact=root/'historical.json';artifact.write_text('retained evidence')
            policy=root/'config/publication-history.json'
            policy.write_text(json.dumps({'historical.json':hashlib.sha256(artifact.read_bytes()).hexdigest()}))
            subprocess.run(['git','add','.'],cwd=root,check=True)
            subprocess.run(['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','base'],cwd=root,check=True)
            artifact.unlink();policy.write_text('{}')
            subprocess.run(['git','add','-A'],cwd=root,check=True)
            self.assertTrue(audit(root,'HEAD'))

    def test_foreign_and_wrong_owner_repository_urls_are_rejected(self):
        self.assertTrue(restricted('https://github.com/'+''.join(('PrivatePartner/','secret-repo'))))
        self.assertTrue(restricted('https://github.com./'+''.join(('PrivatePartner/','secret-repo'))))
        self.assertTrue(restricted('ssh://git@ssh.github.com:443/'+''.join(('PrivatePartner/','secret-repo.git'))))
        self.assertTrue(restricted(''.join(('SAABOLImpactVenture/','infrastructureproductworks.github.io'))))
        self.assertTrue(restricted(''.join(('https://github.com/','apps/../','PrivatePartner/','secret-repo'))))
        self.assertTrue(restricted(r'[private](https://github\.com/'+''.join(('PrivatePartner/','secret-repo'))+')'))
        for separator in ['。','．','｡']:
            self.assertTrue(restricted('https://github'+separator+'com/'+''.join(('PrivatePartner/','secret-repo'))))
        for prefix in ['https://github.dev/','https://vscode.dev/github/']:
            self.assertTrue(restricted(prefix+''.join(('PrivatePartner/','secret-repo'))))
        self.assertTrue(restricted('<a href="https://git&#x0A;hub.com/'+''.join(('PrivatePartner/','secret-repo'))+'">link</a>'))
        self.assertFalse(restricted('InfrastructureProductWorks/iaap-guard'))

    def test_over_encoded_text_fails_closed(self):
        from urllib.parse import quote
        text='https://github.com/'+''.join(('PrivatePartner/','secret-repo'))
        for _ in range(9):text=quote(text,safe='')
        with self.assertRaises(ValueError):normalize(text)

    def test_dangling_symlink_discloses_its_target_blob(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            (root/'config/publication-history.json').write_text('{}')
            (root/'link').symlink_to('InfrastructureProductWorks/'+'iaap-'+'forge')
            subprocess.run(['git','add','.'],cwd=root,check=True)
            self.assertTrue(audit(root))

    def test_bom_marked_text_is_scanned(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            (root/'config/publication-history.json').write_text('{}')
            path=root/'encoded.md';path.touch()
            subprocess.run(['git','add','.'],cwd=root,check=True)
            text='https://github.com/'+''.join(('PrivatePartner/','secret-repo'))
            for encoding in ['utf-16','utf-32','utf-8-sig']:
                path.write_bytes(text.encode(encoding));self.assertTrue(audit(root),encoding)
            for encoding in ['utf-16-le','utf-16-be','utf-32-le','utf-32-be']:
                path.write_bytes(text.encode(encoding))
                with self.assertRaises(ValueError):audit(root)

    def test_relative_submodules_and_lfs_payloads_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'config').mkdir()
            subprocess.run(['git','init','-q',directory],check=True)
            (root/'config/publication-history.json').write_text('{}')
            module=root/'.gitmodules';module.write_text('[submodule "engine"]\n path = engine\n url = ../'+''.join(('iaap-','forge'))+'\n')
            subprocess.run(['git','add','.'],cwd=root,check=True)
            self.assertTrue(audit(root))
            module.unlink();subprocess.run(['git','rm','--cached','.gitmodules'],cwd=root,check=True,stdout=subprocess.DEVNULL)
            (root/'.gitattributes').write_text('hidden.md filter=lfs\n')
            (root/'hidden.md').write_text('ordinary visible text')
            subprocess.run(['git','add','.gitattributes','hidden.md'],cwd=root,check=True)
            self.assertTrue(audit(root))

if __name__=='__main__':unittest.main()
