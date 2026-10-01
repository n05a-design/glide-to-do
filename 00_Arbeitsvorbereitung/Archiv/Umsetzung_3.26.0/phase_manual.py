from pathlib import Path
import ast
p=Path('01_Repository/Glide/src/glide/app.pyw');s=p.read_text(encoding='utf-8')
def r(a,b):
 global s
 assert a in s,a[:100]
 s=s.replace(a,b,1)
r('        "replaced": "Bestand ersetzt",','        "replaced": "Bestand ersetzt",\n        "imported": "importiert", "exported": "exportiert", "backup": "gesichert",')
pos=s.index('    def record_history_events(')
s=s[:pos]+'''    def record_data_operation(self, action, path):
        if self.history_enabled():
            self.record_history_events([{"kind": "data", "action": action,
                                         "target": os.path.basename(str(path)), "list": ""}])
            return self.save_items(record_activity=False)
        return True

''' +s[pos:]
# Only successful user-facing operations create records; low-level writers remain pure.
for name,action in [('export_as_txt','exported'),('export_as_markdown','exported'),('export_as_csv','exported'),('export_full_backup','backup'),('export_partial_backup','backup'),('export_app_backup','backup')]:
 a=s.index('    def '+name+'(');b=s.index('\n    def ',a+8);c=s[a:b];idx=c.index('            self.show_info',c.index('        try:'));c=c[:idx]+f'            self.record_data_operation("{action}", path)\n'+c[idx:];s=s[:a]+c+s[b:]
# Include plain rich-note content in text-oriented exports without pretending to preserve styles.
for name in ['export_as_txt','export_as_markdown']:
 a=s.index('    def '+name+'(');b=s.index('\n    def ',a+8);c=s[a:b];c=c.replace('        note = str(self.current_list().get("note") or "").strip()', '''        self.flush_rich_note()
        note = "\\n\\n".join(value for value in (str(self.current_list().get("note") or "").strip(),
                           self.current_list().get("rich_note", {}).get("text", "")) if value)''');s=s[:a]+c+s[b:]
# Flush drafts before user backup payloads are built.
for name in ['export_full_backup','export_partial_backup','export_app_backup','show_exchange_export_dialog']:
 a=s.index('    def '+name+'(');b=s.index('\n    def ',a+8);c=s[a:b];idx=c.find('        self.sync_current_list_reference()')
 if idx>=0:c=c[:idx]+'        self.flush_rich_note()\n'+c[idx:]
 s=s[:a]+c+s[b:]
pos=s.index('    def show_manual_dialog(')
s=s[:pos]+'''    def manual_html(self):
        from html import escape
        sections = []
        for title, entries in self.MANUAL_SECTIONS:
            rows = ''.join('<tr><th>'+escape(name)+'</th><td>'+escape(purpose)+'</td><td>'+escape(place)+'</td></tr>'
                           for name, purpose, place in entries)
            sections.append('<section><h2>'+escape(title)+'</h2><table>'+rows+'</table></section>')
        return ('<!doctype html><html lang="de"><meta charset="utf-8"><title>Glide Handbuch</title>'
                '<style>body{font:11pt system-ui;max-width:1050px;margin:2em auto;padding:1em;color:#111}'
                'table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #bbb;padding:.6em}'
                'th{width:22%}tr{break-inside:avoid}@media print{body{margin:0;max-width:none}.print{display:none}}</style>'
                '<button class="print" onclick="window.print()">Drucken / als PDF speichern</button>'
                '<h1>Glide – Handbuch</h1><p>Version '+escape(APP_VERSION)+'</p>'+''.join(sections)+'</html>')

    def export_manual(self, open_for_print=False):
        if open_for_print:
            descriptor, path = tempfile.mkstemp(prefix="glide-handbuch-", suffix=".html")
            os.close(descriptor)
        else:
            path = filedialog.asksaveasfilename(title="Handbuch speichern", defaultextension=".html",
                                              initialfile=f"Glide-Handbuch-{APP_VERSION}.html",
                                              filetypes=[("HTML-Dokument", "*.html")])
        if not path:
            return "break"
        try:
            self.validate_backup_target(os.path.abspath(path))
            with open(path, "w", encoding="utf-8") as output:
                output.write(self.manual_html())
            if open_for_print:
                self.open_external_path(path)
            else:
                self.show_info("Handbuch gespeichert", path)
        except (OSError, ValueError) as error:
            self.show_error("Handbuch", str(error))
        return "break"

''' +s[pos:]
a=s.index('    def show_manual_dialog(');b=s.index('\n    def ',a+8);c=s[a:b];# Place action bar before expandable content.
idx=c.index('        suche = tk.StringVar')
c=c[:idx]+'''        manual_actions = ButtonFlow(dialog, bg=self.theme["bg"])
        manual_actions.pack(side="bottom", fill="x", padx=24, pady=10)
        manual_actions.add(self._make_dialog_button(manual_actions, "Als HTML speichern", self.export_manual, "export"))
        manual_actions.add(self._make_dialog_button(manual_actions, "Öffnen und drucken", lambda: self.export_manual(True), "import"))
''' +c[idx:];s=s[:a]+c+s[b:]
r("            tag, start, end = span.get('tag'), span.get('start'), span.get('end')", "            tag, start, end = span.get('tag'), span.get('start'), span.get('end')\n            if not isinstance(tag, str):\n                raise ValueError('Ungültige Formatierung.')")
ast.parse(s);p.write_text(s,encoding='utf-8');print('Manual export and operation history integrated')
