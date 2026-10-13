import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_publication_boundary import audit

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
            self.assertEqual(audit(root),[])
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
            for text in ['https://github.com/'+name,'git@github.com:'+name,name.replace('/','%2F'),''.join('\\u%04x'%ord(c) for c in name)]:
                value.write_text(text)
                self.assertTrue(audit(root),text)

if __name__=='__main__':unittest.main()
