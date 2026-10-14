"""Die beobachtete PyGObject-Namenskollision ohne GUI/gi nachstellen."""
import unittest

from pruefe_native_atspi import text_values


class AtspiConsumer(unittest.TestCase):
    def test_text_interface_is_selected_despite_accessible_method_collision(self):
        class Accessible:
            value = '🏠 Ä\nZeile'
            def get_text(self):
                raise AssertionError('Accessible.get_text hat keine Offsetparameter')
        class Text:
            @staticmethod
            def get_text(accessible, start, end):
                return accessible.value[start:None if end == -1 else end]
            @staticmethod
            def get_character_count(accessible):
                return len(accessible.value)
            @staticmethod
            def get_caret_offset(accessible):
                return 2
        accessible = Accessible()
        self.assertEqual(text_values(Text, accessible), (accessible.value, len(accessible.value), 2, '🏠 '))


if __name__ == '__main__':
    unittest.main()
