from pathlib import Path
import ast, shutil, textwrap
BASE = Path(__file__).resolve().parents[2]
P = BASE/'01_Repository/Glide/src/glide/app.pyw'
s = P.read_text(encoding='utf-8-sig')
backup = P.parent/'archiv/app_3.26.0_vor_vervollstaendigung.pyw'
if not backup.exists(): shutil.copy2(P, backup)
def replace(old,new,count=1):
    global s
    assert s.count(old)>=count,old[:150]
    s=s.replace(old,new,count)
def method(cls,name,body):
    global s
    t=ast.parse(s); c=next(c for c in t.body if isinstance(c,ast.ClassDef) and c.name==cls)
    n=next(n for n in c.body if isinstance(n,ast.FunctionDef) and n.name==name)
    lines=s.splitlines(True);lines[n.lineno-1:n.end_lineno]=[textwrap.indent(textwrap.dedent(body).strip(),'    ')+'\n'];s=''.join(lines)

replace('f"{self.ICONS[\'inbox\']}  Eingang \\u00b7 {len(eingang)} ohne Bearbeitungstag"','f"Eingang \\u00b7 {len(eingang)} ohne Bearbeitungstag"')
replace('outline=self.border_color,\n            width=border_width,','outline=fill if (self.active_fill or self.is_hovered) else self.border_color,\n            width=border_width,')
# Preserve ellipses inside menu entries; remove action ellipses at the shared button boundary.
replace('self.text = text\n','self.text = self.action_text(text)\n',2)
pos=s.index('    def set_text(self, text):',s.index('class RoundedButton'))
s=s[:pos]+'''    @staticmethod
    def action_text(text):
        text = str(text)
        if text.strip() in ("…", "..."):
            return "Mehr"
        return re.sub(r"\\s+(?:…|\\.\\.\\.)$", "", text)

'''+s[pos:]
# Actual month rather than rendering mode.
replace('titel = dict(self.HOME_CALENDAR_CHOICES).get(modus, "Kalendervorschau")','titel = self.MONTH_NAMES[date.today().month - 1] if modus == "month" else dict(self.HOME_CALENDAR_CHOICES).get(modus, "Kalendervorschau")')
replace('name = self.settings.get("mascot_name", "")\n        return " ".join(str(name).split())[:24] if isinstance(name, str) else ""','name = self.settings.get("mascot_name", "")\n        return (" ".join(str(name).split())[:24] if isinstance(name, str) else "") or "Gismo"')
replace('"Wie soll der Begleiter heißen? Ein leeres Feld nimmt den Namen wieder weg."','"Wie soll der Begleiter heißen? Ein leeres Feld verwendet Gismo."')
# Keep individual manual tile arrangements, improve the default order.
replace('        ("mascot", "Begleiter", 1, False, True),\n','')
replace('        ("today", "Heute – eingeplant und fällig", 2, False, True),','        ("mascot", "Gismo – Begleiter", 1, False, True),\n        ("today", "Heute – eingeplant und fällig", 2, False, True),')
replace('            if h >= 12:\n                self.create_line(x + 4, y + h / 2, x + w - 4, y + h / 2,\n                                 fill=self.line_color, width=1)\n','')
replace('        verbindungen = []\n        for eintrag in board.get("connections", []) or []:', '''        # A tall or crowded board is condensed explicitly, never silently
        # presented as a faithful spatial miniature.
        self._home_preview_condensed = False
        if flaechen:
            extent_w = max(x+w for x,y,w,h in flaechen) - min(x for x,y,w,h in flaechen)
            extent_h = max(y+h for x,y,w,h in flaechen) - min(y for x,y,w,h in flaechen)
            self._home_preview_condensed = len(karten) > 24 or board.get("layout") == "grid" or extent_h > extent_w * 1.2 or extent_w > extent_h * 6
            if self._home_preview_condensed:
                columns = max(1, math.ceil(math.sqrt(len(flaechen) * 1.4)))
                flaechen = [(i % columns * 110, i // columns * 65, 96, 48) for i in range(len(flaechen))]
        verbindungen = []
        for eintrag in board.get("connections", []) or []:''')
replace('label(tile, f"{karten} Karten · {len(verbindungen)} Verbindungen", color="muted")', '''gesamt_verbindungen = len(self.settings.get("pinboards", {}).get("global", {}).get("connections", []))
                label(tile, f"{karten} Karten · {gesamt_verbindungen} Verbindungen", color="muted")
                if getattr(self, "_home_preview_condensed", False) or len(flaechen) < karten:
                    label(tile, f"Verdichtete Übersicht · {len(flaechen)} von {karten} Karten", color="muted")''')
# Existing edges between selected cards follow the selection dropdown.
replace('            board[key] = value\n        if self.save_view_change(change):','''            board[key] = value
            if key == "connection_style":
                selected = set(self.selection())
                for connection in board.get("connections", []):
                    if connection.get("from") in selected and connection.get("to") in selected:
                        connection["style"] = value
        if self.save_view_change(change):''')
replace('("Auto", board["auto"],','("Auto anheften", board["auto"],')
replace('"Neue Punkte dieser Liste automatisch anheften"','"Neue Punkte dieses Bereichs automatisch anheften; die Kartengröße bleibt unverändert"')
replace('(("Anheften", accept, "confirm"), ("Abbrechen", dialog.destroy, "muted"))','(("Alle auswählen", lambda: tree.selection_set(tree.get_children()), "due_action"), ("Anheften", accept, "confirm"), ("Abbrechen", dialog.destroy, "muted"))')
# Folder creation must restrict both the form and the accepted value.
replace('                default_list_id=vorgabe_liste,\n','                default_list_id=vorgabe_liste,\n                allowed_list_ids={entry["id"] for entry in erlaubte},\n')
replace('        ziel = next((entry for entry in app.lists if entry.get("id") == list_id), None)','        ziel = next((entry for entry in erlaubte if entry.get("id") == list_id), None)')
for name in ('item_form_dialog','new_item_dialog'):
    t=ast.parse(s);cl=next(c for c in t.body if isinstance(c,ast.ClassDef) and c.name=='ListApp');n=next(n for n in cl.body if isinstance(n,ast.FunctionDef) and n.name==name)
    lines=s.splitlines(True);chunk=''.join(lines[n.lineno-1:n.end_lineno]);chunk=chunk.replace('        default_list_id=None,','        default_list_id=None,\n        allowed_list_ids=None,',1)
    if name=='new_item_dialog': chunk=chunk.replace('            default_list_id=default_list_id,','            default_list_id=default_list_id,\n            allowed_list_ids=allowed_list_ids,')
    else:
        chunk=chunk.replace('            for entry in self.lists:\n                list_choices.append','            for entry in self.lists:\n                if allowed_list_ids is not None and entry.get("id") not in allowed_list_ids:\n                    continue\n                list_choices.append',1)
        chunk=chunk.replace('dialog.minsize(ResponsiveColumns.required_width(chrome=2 * self.DIALOG_PAD_X + 40), 620)','dialog.minsize(560, 440)',1)
    lines[n.lineno-1:n.end_lineno]=[chunk+'\n'];s=''.join(lines)
# Minimal themes get an actual color accent, plus selectable neutral contrasts.
replace('base["ui_accent"] = base.get(accent_key, base["accent"])','''base["ui_accent"] = base.get(accent_key, base["accent"])
        if info["layer"] == "minimal":
            base["ui_accent"] = base["text"] if accent_key == "muted" else self.THEMES[info["base"]].get(accent_key, base["accent"])''')
ast.parse(s)
P.write_text(s,encoding='utf-8')
print('Phase 1 applied')
