"""Namenszählung bewahrt die bisherige lexikalische Bedeutung."""
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import analyse_statisch as analyse


class UsageCountsTests(unittest.TestCase):
    def count(self, text, names):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory)/'first.py', Path(directory)/'second.py'
            first.write_text(text, encoding='utf-8')
            second.write_text('foo', encoding='utf-8')
            paths = [first, Path(directory)/'missing.py', second]
            with patch.object(analyse, 'USAGE_SEARCH', paths):
                result = analyse.usage_counts(names)
            return result, text+'\nfoo'

    def test_definitions_comments_strings_unicode_and_boundaries(self):
        names = {'foo', 'foo2', '_foo', 'foobar', 'ändern', 'missing'}
        result, _ = self.count('def foo(): pass\n# foo foo2 _foo foobar\n"ändern ändern"\nself.foo', names)
        self.assertEqual(result, {'foo': 4, 'foo2': 1, '_foo': 1, 'foobar': 1, 'ändern': 2, 'missing': 0})

    def test_unusual_names_preserve_original_literal_regex_semantics(self):
        names = {'foo.bar', 'foo-bar', 'e\u0301x', '', ' foo ', 'foo', '123'}
        result, text = self.count('foo.bar foo-bar e\u0301x foo 123\nfoo', names)
        expected = {name: len(re.findall(rf'\b{re.escape(name)}\b', text)) for name in names}
        self.assertEqual(result, expected)

    def test_empty_selection_and_duplicate_names(self):
        self.assertEqual(self.count('foo', [])[0], {})
        self.assertEqual(self.count('foo', ['foo', 'foo'])[0], {'foo': 2})


if __name__ == '__main__':
    unittest.main()
