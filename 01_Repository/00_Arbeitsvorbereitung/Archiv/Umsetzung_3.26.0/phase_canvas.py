from pathlib import Path
import ast
p=Path('01_Repository/Glide/src/glide/app.pyw');s=p.read_text(encoding='utf-8')
def r(a,b):
 global s
 assert a in s,a[:100]
 s=s.replace(a,b,1)
r('"snap": raw.get("snap") is not False,','"snap": raw.get("snap") is not False,\n                           "object_snap": raw.get("object_snap") is True,')
r('        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)\n        identity = self.card_at(x, y)', '        self._lasso = None\n        self.canvas.delete("layer:interaction")\n        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)\n        identity = self.card_at(x, y)')
r('        if self.selected_ids:\n            self.select_card(None)\n        self._drag = None\n        return "break"', '''        previous = list(self.selected_ids) if self.app.selection_modifier_pressed(event) else []
        if not previous:
            self.select_card(None)
        self._lasso = (x, y, previous)
        self._drag = None
        self.canvas.focus_set()
        return "break"''')
r('        if not self._drag or self.board()["layout"] != "free":', '''        if getattr(self, "_lasso", None) is not None:
            x, y, _previous = self._lasso
            self.canvas.delete("layer:interaction")
            self.canvas.create_rectangle(x, y, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y),
                                         outline=self.app.theme["ui_accent"], dash=(4, 3), width=2,
                                         tags=("layer:interaction",))
            return "break"
        if not self._drag or self.board()["layout"] != "free":''')
r('        aktuell_x, aktuell_y, breite, hoehe = self.card_boxes[identity]\n', '''        self.canvas.delete("layer:guides")
        aktuell_x, aktuell_y, breite, hoehe = self.card_boxes[identity]
        if self.board().get("object_snap") and not event.state & 0x0008:
            xs, ys = [], []
            for other, (ox, oy, ow, oh) in self.card_boxes.items():
                if other == identity:
                    continue
                xs.extend((target - source, target) for target in (ox, ox+ow/2, ox+ow)
                          for source in (ziel_x, ziel_x+breite/2, ziel_x+breite))
                ys.extend((target - source, target) for target in (oy, oy+oh/2, oy+oh)
                          for source in (ziel_y, ziel_y+hoehe/2, ziel_y+hoehe))
            for axis, candidates in (("x", xs), ("y", ys)):
                if not candidates:
                    continue
                delta, guide = min(candidates, key=lambda value: abs(value[0]))
                if abs(delta) <= 6:
                    if axis == "x":
                        ziel_x += delta
                        coords = (guide, 0, guide, max(2000, ziel_y+hoehe))
                    else:
                        ziel_y += delta
                        coords = (0, guide, max(2000, ziel_x+breite), guide)
                    self.canvas.create_line(*coords, fill=self.app.theme["ui_accent"], dash=(3, 4),
                                            tags=("layer:guides",))
''')
r('    def card_release(self, event):\n', '''    def card_release(self, event):
        self.canvas.delete("layer:guides")
        if getattr(self, "_lasso", None) is not None:
            x, y, previous = self._lasso
            self._lasso = None
            self.canvas.delete("layer:interaction")
            end_x, end_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            if abs(end_x-x) > 3 or abs(end_y-y) > 3:
                left, right = sorted((x, end_x))
                top, bottom = sorted((y, end_y))
                selected = [key for key, (cx, cy, cw, ch) in self.card_boxes.items()
                            if left <= cx and top <= cy and cx+cw <= right and cy+ch <= bottom]
                old = set(self.selected_ids)
                self.selected_ids = list(dict.fromkeys(previous + selected))
                self.selected_id = self.selected_ids[-1] if self.selected_ids else None
                self.paint_selection(old | set(self.selected_ids))
                self.update_selection_notice()
            return "break"
''')
# Object snapping must remain optional and reachable even in a compact toolbar.
r('        menu.add_command(label="   Aktionen", command=self.show_board_actions_menu)', '''        menu.add_checkbutton(label="An Karten ausrichten", onvalue=True, offvalue=False,
                             variable=tk.BooleanVar(value=self.board().get("object_snap", False)),
                             command=lambda: self.configure_board("object_snap", not self.board().get("object_snap", False)))
        menu.add_command(label="   Aktionen", command=self.show_board_actions_menu)''')
# Semantic canvas layers augment existing per-card tags without changing hit testing.
r('        self.draw_connections()\n        if not cards:', '''        self.draw_connections()
        for element in canvas.find_all():
            tags = canvas.gettags(element)
            layer = "connections" if "connection" in tags else "labels" if canvas.type(element) == "text" else "cards"
            canvas.addtag_withtag("layer:" + layer, element)
        if not cards:''')
ast.parse(s);p.write_text(s,encoding='utf-8');print('Lasso and optional alignment applied')
