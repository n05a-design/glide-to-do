from pathlib import Path
p = Path(__file__).resolve().parents[2] / '01_Repository/Glide/src/glide/app.pyw'
s = p.read_text(encoding='utf-8')
a = s.index('    def board_print_geometry(self):')
b = s.index('    def print_board(self):', a)
part = s[a:b]
part = part.replace('self.card_boxes', 'boxes')
part = part.replace('''        if not boxes:
''', '''        boxes = self.logical_card_boxes()
        if not boxes:
''', 1)
part = part.replace('''        app = self.app
        geometrie''', '''        app = self.app
        boxes = self.logical_card_boxes()
        geometrie''', 1)
part = '''    def logical_card_boxes(self):
        """Druck und Modellberechnungen verwenden unskalierte Geometrie."""
        factor = self.zoom_factor()
        return {identity: tuple(value / factor for value in box)
                for identity, box in self.card_boxes.items()}

''' + part
s = s[:a] + part + s[b:]
p.write_text(s, encoding='utf-8')
