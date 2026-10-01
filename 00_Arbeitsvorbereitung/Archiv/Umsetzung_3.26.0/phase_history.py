from pathlib import Path
import ast
p=Path('01_Repository/Glide/src/glide/app.pyw');s=p.read_text(encoding='utf-8')
def r(a,b,count=1):
 global s
 assert a in s,a[:90]
 s=s.replace(a,b,count)
r('MAX_HISTORY_ENTRIES = 4000','MAX_HISTORY_ENTRIES = 15\n    HISTORY_RETENTION_DAYS = 15')
r('        for value in raw[-cls.MAX_HISTORY_ENTRIES:]:','        for value in raw:')
r('            if not isinstance(at, str) or not at.strip():\n                continue','''            if not isinstance(at, str) or not at.strip():
                continue
            try:
                age = datetime.now().timestamp() - datetime.fromisoformat(at).timestamp()
                if age > cls.HISTORY_RETENTION_DAYS * 86400:
                    continue
            except (ValueError, OverflowError, OSError):
                continue''')
r('            entries.append(entry)\n        return entries','            entries.append(entry)\n        entries.sort(key=lambda entry: datetime.fromisoformat(entry["at"]).timestamp())\n        return entries[-cls.MAX_HISTORY_ENTRIES:]')
r('            self.update_history()\n            backup_warning', '            self.update_history()\n            self.history = self.normalize_history_entries(self.history)\n            backup_warning')
r('        if len(self.history) > self.MAX_HISTORY_ENTRIES:\n            del self.history[:len(self.history) - self.MAX_HISTORY_ENTRIES]', '        self.history = self.normalize_history_entries(self.history)')
r('for entry in reversed(getattr(self, "history", []) or []):', 'for entry in reversed(self.normalize_history_entries(getattr(self, "history", []))):')
r('    TEMPLATE_VIEW = "templates"', '    HISTORY_VIEW = "history"\n    TEMPLATE_VIEW = "templates"')
s=s.replace('self.HOME_VIEW, self.TEMPLATE_VIEW, self.LIBRARY_VIEW', 'self.HOME_VIEW, self.HISTORY_VIEW, self.TEMPLATE_VIEW, self.LIBRARY_VIEW')
s=s.replace('app.HOME_VIEW, app.TEMPLATE_VIEW, app.LIBRARY_VIEW', 'app.HOME_VIEW, app.HISTORY_VIEW, app.TEMPLATE_VIEW, app.LIBRARY_VIEW')
r('            self.sidebar_iid_to_row[self.TEMPLATE_ROW_ID] = ("view", self.TEMPLATE_VIEW)', '''            self.sidebar_iid_to_row[self.TEMPLATE_ROW_ID] = ("view", self.TEMPLATE_VIEW)
            self.system_listbox.insert("", "end", iid="smart:history", text="Verlauf",
                                       values=(self.ICONS["history"], ""), tags=("system",))
            self.sidebar_rows.append(("view", self.HISTORY_VIEW))
            self.sidebar_iid_to_row["smart:history"] = ("view", self.HISTORY_VIEW)
            self.system_listbox.configure(height=7)''')
r('        elif row == ("view", self.TEMPLATE_VIEW) and self.view_mode != self.TEMPLATE_VIEW:', '        elif row == ("view", self.HISTORY_VIEW) and self.view_mode != self.HISTORY_VIEW:\n            self._activate_system_view(self.HISTORY_VIEW)\n        elif row == ("view", self.TEMPLATE_VIEW) and self.view_mode != self.TEMPLATE_VIEW:')
r('        if self.view_mode == self.LIBRARY_VIEW:\n            self.tree.selection_remove(self.tree.selection())', '''        if self.view_mode == self.HISTORY_VIEW:
            self.tree.selection_remove(self.tree.selection())
            for widget in self.home_content.winfo_children():
                widget.destroy()
            self.show_history_dialog(embedded=True)
            return
        if self.view_mode == self.LIBRARY_VIEW:
            self.tree.selection_remove(self.tree.selection())''')
r('    def show_history_dialog(self, event=None):', '    def show_history_dialog(self, event=None, embedded=False):')
a=s.index('    def show_history_dialog(');b=s.index('\n    def ',a+8);c=s[a:b];c=c.replace('        dialog = tk.Toplevel(self.root)\n        dialog.title("Änderungsverlauf")\n        dialog.transient(self.root)','''        dialog = tk.Frame(self.home_content) if embedded else tk.Toplevel(self.root)
        if embedded:
            dialog.pack(fill="both", expand=True)
        else:
            dialog.title("Änderungsverlauf")
            dialog.transient(self.root)''').replace('        dialog.minsize(ResponsiveColumns.required_width(gap=12, chrome=88), 440)','        if not embedded:\n            dialog.minsize(560, 440)').replace('flow, "Schließen", dialog.destroy,','flow, "Zur Startseite" if embedded else "Schließen", self.set_home_view if embedded else dialog.destroy,').replace('        self._center_dialog(dialog, min_width=860, min_height=640)\n        self._schedule_windows_chrome_theme(dialog)\n        feld.focus_set()\n        self.run_modal(dialog)','''        if not embedded:
            self._center_dialog(dialog, min_width=860, min_height=640)
            self._schedule_windows_chrome_theme(dialog)
            feld.focus_set()
            self.run_modal(dialog)''');s=s[:a]+c+s[b:]
r('    def get_display_title(self):','    def get_display_title(self):\n        if self.view_mode == self.HISTORY_VIEW:\n            return "Änderungsverlauf"')
# Existing central symbol may already exist.
if '"history":' not in s[s.index('    ICONS = {'):s.index('    ICONS = {')+4000]:r('    ICONS = {','    ICONS = {\n        "history": "↶",')
ast.parse(s);p.write_text(s,encoding='utf-8');print('History retention and sidebar view applied')
