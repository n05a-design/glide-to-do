from pathlib import Path
import ast
p=Path('01_Repository/Glide/src/glide/app.pyw');s=p.read_text(encoding='utf-8')
def r(a,b):
 global s
 assert a in s,a[:100]
 s=s.replace(a,b,1)
r('"object_snap": raw.get("object_snap") is True,','"object_snap": raw.get("object_snap") is True,\n                           "zoom": raw.get("zoom") if raw.get("zoom") in (50,75,100,125,150,200) else 100,')
r('        frame = tk.Frame(self.body, bg=app.theme["card"])\n        frame.pack(fill="both", expand=True)\n        self.canvas = tk.Canvas', '''        zoom_row = tk.Frame(self.body, bg=app.theme["card"])
        zoom_row.pack(fill="x", pady=(0, 4))
        tk.Label(zoom_row, text="Zoom", bg=app.theme["card"], fg=app.theme["muted"], font=app_font(9)).pack(side="left", padx=(0, 8))
        zoom = tk.StringVar(value=f"{board.get('zoom', 100)} %")
        zoom_border, _ = app._make_option_menu(zoom_row, zoom, [f"{value} %" for value in (50,75,100,125,150,200)])
        zoom_border.pack(side="left")
        zoom.trace_add("write", lambda *_: self.configure_board("zoom", int(zoom.get().split()[0])))
        tk.Label(zoom_row, text="Auswahlrechteck: ganze Karten einschließen · Strg/Cmd ergänzt",
                 bg=app.theme["card"], fg=app.theme["muted"], font=app_font(8)).pack(side="left", padx=12)
        frame = tk.Frame(self.body, bg=app.theme["card"])
        frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas''')
r('        available = max(200, canvas.winfo_width()-34)','        available = max(200, (canvas.winfo_width()-34) / self.zoom_factor())')
r('        self.update_scrollregion()\n\n    @staticmethod\n    def border_point', '        self.update_scrollregion()\n\n    @staticmethod\n    def border_point') if False else None
# End of draw_board only.
a=s.index('    def draw_board(self):');b=s.index('\n    @staticmethod',a);chunk=s[a:b];assert '        self.update_scrollregion()' in chunk;chunk=chunk.replace('        self.update_scrollregion()','        self.scale_board_view()\n        self.update_scrollregion()',1);s=s[:a]+chunk+s[b:]
pos=s.index('    def draw_board(self):')
s=s[:pos]+'''    def zoom_factor(self):
        return self.board().get("zoom", 100) / 100.0

    def scale_board_view(self):
        """Nur Darstellungsobjekte skalieren; das gespeicherte Modell bleibt logisch."""
        canvas, factor = self.canvas, self.zoom_factor()
        self._zoom_fonts = []
        if factor == 1:
            return
        canvas.scale("all", 0, 0, factor, factor)
        self.card_boxes = {identity: tuple(value*factor for value in box)
                           for identity, box in self.card_boxes.items()}
        images = {str(value): value for value in self._card_images}
        numerator = int(round(factor*4))
        for element in canvas.find_all():
            kind = canvas.type(element)
            if kind == "text":
                font = tkfont.Font(root=canvas, font=canvas.itemcget(element, "font"))
                size = font.actual("size")
                font.configure(size=(1 if size >= 0 else -1)*max(1, round(abs(size)*factor)))
                self._zoom_fonts.append(font)
                canvas.itemconfigure(element, font=font,
                                     width=float(canvas.itemcget(element, "width"))*factor)
            elif kind == "image":
                source = images.get(canvas.itemcget(element, "image"))
                if source is not None:
                    image = source.zoom(numerator).subsample(4)
                    self._card_images.append(image)
                    canvas.itemconfigure(element, image=image)
            if kind in ("line", "polygon", "rectangle", "oval"):
                canvas.itemconfigure(element, width=max(0.5, float(canvas.itemcget(element, "width"))*factor))
            if kind == "line":
                shape = canvas.tk.splitlist(canvas.itemcget(element, "arrowshape"))
                canvas.itemconfigure(element, arrowshape=tuple(float(v)*factor for v in shape))

''' +s[pos:]
r('self._context_point = (x, y)','self._context_point = (x / self.zoom_factor(), y / self.zoom_factor())')
r('return self.create_card_item(x, y)','return self.create_card_item(x / self.zoom_factor(), y / self.zoom_factor())')
r('self.store_position(identity, x, y, reveal=False, apply_grid=not self.board().get("object_snap"))','self.store_position(identity, x / self.zoom_factor(), y / self.zoom_factor(), reveal=False, apply_grid=not self.board().get("object_snap"))')
r('ziel_x = max(0, min(20000, left+dx))','ziel_x = max(0, min(20000*self.zoom_factor(), left+dx))')
r('ziel_y = max(0, min(20000, top+dy))','ziel_y = max(0, min(20000*self.zoom_factor(), top+dy))')
# Width of live selection frames is also expressed in display coordinates.
a=s.index('    def paint_selection(');b=s.index('\n    def ',a+8);chunk=s[a:b].replace('width=4 if anker else 3 if ausgewaehlt else 1','width=(4 if anker else 3 if ausgewaehlt else 1)*self.zoom_factor()');s=s[:a]+chunk+s[b:]
ast.parse(s);p.write_text(s,encoding='utf-8');print('Canvas zoom integrated')
