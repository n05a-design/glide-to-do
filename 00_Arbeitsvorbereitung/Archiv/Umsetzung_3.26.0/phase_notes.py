from pathlib import Path
import ast
p=Path('01_Repository/Glide/src/glide/app.pyw');s=p.read_text(encoding='utf-8')
def r(a,b,count=1):
 global s
 assert a in s,a[:120]
 s=s.replace(a,b,count)
editor=Path('00_Arbeitsvorbereitung/Umsetzung_3.26.0/rich_editor.txt').read_text(encoding='utf-8')
editor=editor.replace("wrap='word', undo=False,", "wrap='word', undo=False, exportselection=False,")
editor=editor.replace("prefix = '• ' if tag == 'bullet' else", "prefix = self.app.ICONS['bullet'] + ' ' if tag == 'bullet' else")
s=s.replace('class ListApp:',editor+'class ListApp:',1)
r('    DATA_SCHEMA_VERSION = 16','    DATA_SCHEMA_VERSION = 17')
r('    ICONS = {','    ICONS = {\n        "bullet": "•",')
# Extend list data without changing positional arguments used by previous versions.
start=s.index('    def new_list_object(');end=s.index('\n    def ',start+8)
chunk=s[start:end].replace('        attachments=None,','        attachments=None,\n        list_kind="tasks",\n        rich_note=None,').replace('            "note": str(note or ""),','            "note": str(note or ""),\n            "list_kind": "note" if list_kind == "note" else "tasks",\n            "rich_note": RichNoteEditor.normalize(rich_note),');s=s[:start]+chunk+s[end:]
r('list_labels, entry.get("attachments"))','list_labels, entry.get("attachments"), entry.get("list_kind"), entry.get("rich_note"))')
r('            attachments=copy.deepcopy(entry.get("attachments", [])),','            attachments=copy.deepcopy(entry.get("attachments", [])),\n            list_kind=entry.get("list_kind"), rich_note=copy.deepcopy(entry.get("rich_note")),')
r('                restored.get("attachments"),','                restored.get("attachments"),\n                restored.get("list_kind"), restored.get("rich_note"),')
r('                    payload.get("attachments"),','                    payload.get("attachments"),\n                    payload.get("list_kind"), payload.get("rich_note"),')
# Every lifecycle reset of the migration guard includes the new format.
s=s.replace('        self._schema16_backup_checked = False','        self._schema16_backup_checked = False\n        self._schema17_backup_checked = False')
t=ast.parse(s);cl=next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name=='ListApp');n=next(n for n in cl.body if isinstance(n,ast.FunctionDef) and n.name=='ensure_schema16_backup');lines=s.splitlines(True);migration=''.join(lines[n.lineno-1:n.end_lineno]).replace('16','17');r('    def ensure_schema16_backup(self):',migration+'\n\n    def ensure_schema16_backup(self):')
r('            self.ensure_schema16_backup()','            self.ensure_schema16_backup()\n            self.ensure_schema17_backup()')
# List properties keep notes while switching back to the task-only presentation.
r('for key in ("title", "note", "color", "labels", "attachments")}','for key in ("title", "note", "color", "labels", "attachments", "list_kind")}')
r('        attachments = copy.deepcopy(page.get("attachments", [])) if page is not None else []', '''        list_kind_var = tk.StringVar(value="Notiz" if page and page.get("list_kind") == "note" else "Aufgaben")
        is_list_page = page is not None and "items" in page and not self.is_inbox_list(page)
        attachments = copy.deepcopy(page.get("attachments", [])) if page is not None else []''')
r('            self._make_field_label(right, "Farbe").pack', '''            if is_list_page:
                self._make_field_label(right, "Listenart").pack(anchor="w", pady=(0, self.FIELD_LABEL_GAP))
                kind_frame, _ = self._make_option_menu(right, list_kind_var, ["Aufgaben", "Notiz"])
                kind_frame.pack(fill="x", pady=(0, 12))
            self._make_field_label(right, "Farbe").pack''')
r('            result["value"] = details\n            dialog.destroy()', '''            if is_list_page:
                details["list_kind"] = "note" if list_kind_var.get() == "Notiz" else "tasks"
            result["value"] = details
            dialog.destroy()''')
r('        title_var, color_var = tk.StringVar(), tk.StringVar(value="Keine Farbe")','''        list_kind_var = tk.StringVar(value="Aufgaben")
        if is_list:
            label("Listenart")
            kind_frame, _ = self._make_option_menu(primary, list_kind_var, ["Aufgaben", "Notiz"])
            kind_frame.pack(fill="x")
        title_var, color_var = tk.StringVar(), tk.StringVar(value="Keine Farbe")''')
r('                holder.update(title=title, note=note.get("1.0", "end-1c"), color=color)','''                holder.update(title=title, note=note.get("1.0", "end-1c"), color=color)
                if is_list:
                    holder["list_kind"] = "note" if list_kind_var.get() == "Notiz" else "tasks"''')
# A separate pane beneath the limited task area owns its own text scrolling.
r('        if ready:\n            workspace.refresh()','        if ready:\n            workspace.refresh()\n        self.sync_rich_note_view()')
r('    def on_close(self):','    def on_close(self):\n        self.flush_rich_note()')
r('        self.expanded_ids = set()\n        self.collapsed_item_ids = set()\n        self.selection_anchor_id = None\n        self.update_window_title()', '        self.flush_rich_note()\n        self.expanded_ids = set()\n        self.collapsed_item_ids = set()\n        self.selection_anchor_id = None\n        self.update_window_title()')
pos=s.index('    def _refresh_tree(self,')
s=s[:pos]+'''    def flush_rich_note(self):
        editor = getattr(self, "rich_note_editor", None)
        if editor is not None and editor.winfo_exists():
            editor.flush()

    def store_rich_note(self, list_id, document):
        entry = next((entry for entry in self.lists if entry.get("id") == list_id), None)
        if entry is None:
            return False
        if entry.get("rich_note") != document:
            with self.sidebar_change() as change:
                entry["rich_note"] = copy.deepcopy(document)
                change.mark()
        return not self.dirty

    def sync_rich_note_view(self):
        if not hasattr(self, "list_frame"):
            return
        entry = self.current_list() if self.view_mode == "list" else None
        visible = bool(entry and entry.get("list_kind") == "note" and not getattr(self.workspace, "visible", False))
        editor = getattr(self, "rich_note_editor", None)
        identity = entry.get("id") if visible else None
        signature = (identity, tuple(sorted(self.theme.items())))
        if editor is not None and (not visible or getattr(self, "_rich_note_signature", None) != signature):
            editor.flush()
            editor.destroy()
            self.rich_note_editor = editor = None
        if not visible:
            self.tree.configure(height=10)
            if not getattr(self.workspace, "visible", False):
                self.list_frame.pack_configure(fill="both", expand=True)
            return
        self.tree.configure(height=6)
        self.list_frame.pack_configure(fill="x", expand=False)
        if editor is None:
            self._rich_note_signature = signature
            editor = RichNoteEditor(self.list_frame_outer.inner, self, entry.get("rich_note"),
                                    on_change=lambda document, lid=identity: self.store_rich_note(lid, document))
            editor.pack(fill="both", expand=True, pady=(8, 0))
            self.rich_note_editor = editor
        elif editor._last != entry.get("rich_note"):
            editor.load(entry.get("rich_note"))
            editor._last = editor.document()
        query = self.current_search_query()
        editor.text.tag_remove("search_match", "1.0", "end")
        if query:
            editor.text.tag_configure("search_match", background=self.theme["selection"], foreground=self.theme["selection_text"])
            start = "1.0"
            while True:
                found = editor.text.search(query, start, stopindex="end", nocase=True)
                if not found:
                    break
                end = editor.text.index(f"{found}+{len(query)}c")
                editor.text.tag_add("search_match", found, end)
                start = end

''' +s[pos:]
# Observe document changes without copying the note content into history records.
r('lists[list_id] = {"title": title, "folder": entry.get("folder_id")}','lists[list_id] = {"title": title, "folder": entry.get("folder_id"),\n                              "note": self.history_value(entry, "rich_note"), "kind": entry.get("list_kind")}')
r('                schluessel = "folder" if kind == "list" else "parent"','''                if kind == "list" and (alt.get("note") != neu.get("note") or alt.get("kind") != neu.get("kind")):
                    ereignis(kind, "updated", neu["title"])
                schluessel = "folder" if kind == "list" else "parent"''')
# Preserve rich notes in exchanges, including lists toggled back to tasks.
r('EXCHANGE_LIST_FIELDS = {"key", "title", "description", "folder", "labels", "items"}', 'EXCHANGE_LIST_FIELDS = {"key", "title", "description", "folder", "labels", "items", "list_kind", "rich_note"}')
r('            listen.append(darstellung)', '''            if eintrag.get("list_kind") == "note" or eintrag.get("rich_note", {}).get("text"):
                darstellung["list_kind"] = eintrag.get("list_kind", "tasks")
                darstellung["rich_note"] = RichNoteEditor.normalize(eintrag.get("rich_note"))
            listen.append(darstellung)''')
r('titel, punkte, note=str(eintrag.get("description") or ""),','titel, punkte, note=str(eintrag.get("description") or ""),\n                list_kind=eintrag.get("list_kind"), rich_note=eintrag.get("rich_note"),')
ast.parse(s);p.write_text(s,encoding='utf-8');print('Rich notes and schema 17 integrated')
