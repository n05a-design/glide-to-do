import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
import unittest
import compiled_contract as contract

class CompiledTests(unittest.TestCase):
    def test_build_path_is_irrelevant_but_no_code_executes(self):
        raw=b'raise RuntimeError("nie ausfuehren")\n'
        result=contract.compare({'app':raw},lambda _name:compile(raw,'anderer/baupfad.py','exec'))
        self.assertEqual(set(result),{'app'})
        self.assertEqual(len(result['app']),64)

    def test_nested_change_and_optimized_assertions_are_detected(self):
        source=b'assert allowed\ndef action():\n    return "Speichern"\n'
        for candidate in (compile(source.replace(b'Speichern',b'Loeschen'),'x.py','exec'),
                          compile(source,'x.py','exec',optimize=1),None):
            with self.subTest(candidate=candidate),self.assertRaisesRegex(ValueError,'app'):
                contract.compare({'app':source},lambda _name:candidate)

    def test_missing_module_and_syntax_failure_are_reported_together(self):
        def missing(_name):raise KeyError('fehlend')
        with self.assertRaisesRegex(ValueError,'app, helper'):
            contract.compare({'app':b'x=1','helper':b'def('},missing)

if __name__=='__main__':unittest.main()
