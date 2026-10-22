import ast
import copy
import json
from pathlib import Path
import sys
import unittest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'src/glide'))
import exchange_recipes as recipes
import exchange_patch as patch


def builtins():
    return recipes.catalog(json.loads((REPO / 'src/glide/resources/exchange_recipes.json').read_text(encoding='utf-8')))


class RecipeTests(unittest.TestCase):
    def test_five_versioned_presets(self):
        values = builtins()
        self.assertEqual([r['id'] for r in values], ['split-note', 'plan-project', 'summarize', 'prioritize', 'suggest-labels'])
        self.assertEqual([r['mode'] for r in values], ['create', 'create', 'patch', 'patch', 'patch'])
        self.assertIn('unveränderten Originaltext', values[2]['instruction'])

    def test_without_choice_exactly_same_independent_payload(self):
        payload = patch.build_context([], {}, created_at='fixed', application_version='3.43.1')
        self.assertEqual(recipes.prepare(payload), payload)
        result = recipes.prepare(payload)
        result['items'].append('changed')
        self.assertEqual(payload['items'], [])

    def test_patch_extends_only_instructions_not_checksums(self):
        payload = patch.build_context([({'id': 'list'}, {'id': 'task', 'description': 'Original'}, None)], {})
        original = copy.deepcopy(payload)
        for recipe in builtins()[2:]:
            result = recipes.prepare(payload, recipe)
            self.assertTrue(result['instructions'].startswith(payload['instructions']))
            self.assertIn(recipe['title'], result['instructions'])
            self.assertEqual({k: v for k, v in result.items() if k != 'instructions'},
                             {k: v for k, v in payload.items() if k != 'instructions'})
        self.assertEqual(payload, original)

    def test_create_uses_existing_notes_no_unknown_root(self):
        original = dict(format='glide.exchange', format_version=2, mode='create', lists=[])
        result = recipes.prepare(original, builtins()[0])
        self.assertEqual(set(result) - set(original), {'notes'})
        self.assertIn('"mode":"create"', result['notes'])
        self.assertEqual(json.loads(recipes.clipboard_text(result)), result)

    def test_wrong_mode_rejected(self):
        with self.assertRaises(ValueError):
            recipes.prepare(dict(format='glide.context'), builtins()[0])
        with self.assertRaises(ValueError):
            recipes.prepare(dict(format='glide.exchange', mode='create'), builtins()[2])

    def test_bounds_types_and_duplicate_identity(self):
        valid = dict(id='own-one', title=' Eigen  ', mode='patch', instruction=' Text ', fields=['description'])
        self.assertEqual(recipes.normalize(valid)['title'], 'Eigen')
        for field, bad in [('id', '../path'), ('title', ' '), ('title', 'x' * 81), ('instruction', 'x' * 12001),
                           ('instruction', None), ('mode', 'network'), ('fields', ['unknown']), ('fields', [])]:
            with self.subTest(field=field, bad=str(bad)[:20]), self.assertRaises(ValueError):
                recipes.normalize({**valid, field: bad})
        for values in ([valid] * 2, [valid, {**valid, 'id': 'own-two'}], [valid] * 51, None):
            with self.assertRaises(ValueError):
                recipes.records(values)

    def test_catalog_does_not_override_builtin_and_checks_version(self):
        preset = builtins()[0]
        with self.assertRaises(ValueError):
            recipes.catalog(dict(format_version=1, recipes=[preset]), [preset])
        with self.assertRaises(ValueError):
            recipes.catalog(dict(format_version=2, recipes=[]))
        with self.assertRaises(ValueError):
            recipes.catalog(dict(format_version=1, recipes=[]), None)

    def test_no_network_tk_process_or_dynamic_imports(self):
        tree = ast.parse((REPO / 'src/glide/exchange_recipes.py').read_text(encoding='utf-8'))
        imports = {alias.name.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        imports.update(node.module.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom))
        self.assertEqual(imports, {'copy', 'json', 're', 'exchange_patch'})
        self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                             and n.func.id in {'__import__', 'eval', 'exec'} for n in ast.walk(tree)))


if __name__ == '__main__':
    unittest.main()
