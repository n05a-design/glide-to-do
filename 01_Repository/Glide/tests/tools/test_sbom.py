# SPDX-License-Identifier: MPL-2.0
"""Fehlende/mehrdeutige Bestände und veränderte CycloneDX-Nachweise zurückweisen."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'packaging/paket'))
from sbom import make_bom, validate_bom


class SbomTests(unittest.TestCase):
    def test_package_staging_includes_and_hashes_the_generated_bom(self):
        from baue_paket import stage_licenses
        with tempfile.TemporaryDirectory() as folder:
            source, stage = Path(folder) / 'input', Path(folder) / 'stage'
            source.mkdir()
            records = []
            names = ('Python','Tcl','Tk','PyInstaller','PyInstaller-Hooks','tkinterdnd2','tkdnd','Glide','Glide-Schriften')
            for name in names:
                text = ('Künstlicher Lizenzbeleg für ' + name).encode('utf-8')
                filename = name + '.txt'
                (source / filename).write_bytes(text)
                records.append(dict(name=name,version='1',source='Testfixture',files={filename:hashlib.sha256(text).hexdigest()}))
            (source / 'manifest.json').write_text(json.dumps(dict(runtime=self.runtime,components=records)),encoding='utf-8')
            proof = stage_licenses(source,stage,self.runtime)
            bom = stage / 'licenses/Glide.cdx.json'
            self.assertTrue(bom.is_file())
            self.assertEqual(proof['sha256'][bom.name],hashlib.sha256(bom.read_bytes()).hexdigest())
            validate_bom(json.loads(bom.read_text(encoding='utf-8')),records,self.runtime)

    def setUp(self):
        self.runtime = {'python': '3.14.7', 'tcl': '9.1.0'}
        self.records = [dict(name='Glide', version='3.50.7', license='MPL-2.0',
            source='https://example.invalid/tree/fixed', files={'Glide-MPL-2.0.txt': 'a'*64}),
            dict(name='Example', version='1.0', source='Originalbeleg', files={'Example-LICENSE.txt':'b'*64})]

    def test_inventory_is_deterministic_explicitly_incomplete_and_preserves_original_evidence(self):
        original = copy.deepcopy(self.records)
        bom = make_bom(self.records, self.runtime)
        self.assertEqual(validate_bom(bom,self.records,self.runtime),bom)
        self.assertEqual(make_bom(list(reversed(self.records)),self.runtime),bom)
        self.assertEqual(bom['metadata']['component']['licenses'],[{'license':{'id':'MPL-2.0'}}])
        self.assertIn('Example-LICENSE.txt',bom['components'][0]['licenses'][0]['license']['name'])
        self.assertNotIn('hashes',bom['components'][0], 'Lizenzhash ist kein Binärhash')
        self.assertEqual(bom['compositions'],[{'aggregate':'incomplete'}])
        self.assertEqual(self.records,original)

    def test_duplicate_missing_main_and_empty_runtime_fail(self):
        for records,runtime in ((self.records*2,self.runtime),(self.records[1:],self.runtime),(self.records,{})):
            with self.subTest(records=len(records),runtime=runtime), self.assertRaises(ValueError):
                make_bom(records,runtime)

    def test_bad_evidence_and_unproven_license_id_fail(self):
        for change in ({'files':{'../escape':'a'*64}}, {'files':{'a':'not-a-hash'}},
                       {'version':''}, {'source':''}, {'license':'guessed-license'}):
            records=copy.deepcopy(self.records); records[1].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                make_bom(records,self.runtime)

    def test_tampered_version_omitted_component_or_runtime_drift_fail_validation(self):
        bom=make_bom(self.records,self.runtime)
        changed=copy.deepcopy(bom);changed['metadata']['component']['version']='wrong'
        missing=copy.deepcopy(bom);missing['components']=[]
        for document in (changed,missing):
            with self.assertRaises(ValueError):validate_bom(document,self.records,self.runtime)
        with self.assertRaises(ValueError):validate_bom(bom,self.records,{'python':'other'})


if __name__=='__main__':unittest.main()
