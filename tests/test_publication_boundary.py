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
