from pathlib import Path
p=Path('src/glide/app.pyw');s=p.read_text()
def rep(a,b,n=1):
 global s
 assert a in s,a[:90];s=s.replace(a,b,n)
rep('    def sidebar_section_trees(self):','    SIDEBAR_LISTS_MIN_ROWS = 5\n\n    def sidebar_section_trees(self):')
rep('        dialog.geometry(f"{width}x{height}+{x}+{y}")','        dialog.geometry(f"{width}x{height}+{x}+{y}")\n        dialog._glide_layout_measured = True')
rep('            dialog.update_idletasks()\n            breite, hoehe = dialog.minsize()','            if not getattr(dialog, "_glide_layout_measured", False):\n                dialog.update_idletasks()\n            breite, hoehe = dialog.minsize()')
rep('    def refresh_sidebar_row_texts(self, event=None):\n        with self.render_pass():','''    def refresh_sidebar_row_texts(self, event=None):
        if event is not None:
            signature = tuple((str(tree), tree.winfo_width(), tree.column("#0", "width"))
                              for tree in [self.system_listbox] + self.sidebar_trees())
            if signature == getattr(self, "_sidebar_width_signature", None):
                return
            self._sidebar_width_signature = signature
        with self.render_pass():''')
rep('        menu.add_command(label="Neue Zeichnung", command=self.create_new_drawing)\n        menu.add_command(label="Neuer Ordner …", command=lambda: self.create_container_dialog(', '        menu.add_command(label="Neue Zeichnung", command=lambda: self.create_in_sidebar_section("drawing", None, "drawings"))\n        menu.add_command(label="Neuer Ordner …", command=lambda: self.create_container_dialog(')
rep('        self._make_dialog_button(body, "Neue Zeichnung", self.create_new_drawing, "confirm")','        self._make_dialog_button(body, "Neue Zeichnung", lambda: self.create_in_sidebar_section("drawing", None, "drawings"), "confirm")')
rep('        if folder_id is None and self.view_mode == "folder" and self.get_folder(self.active_folder_id):','        if folder_id is None and not getattr(self, "_creating_sidebar_section", None) and self.view_mode == "folder" and self.get_folder(self.active_folder_id):')
for name,kind in [('create_new_drawing','drawing'),('create_new_page','page'),('create_new_note','note'),('create_new_gallery','gallery')]:
 start=s.index('    def '+name+'(');end=s.find('\n    def ',start+5);part=s[start:end]
 if '        self.flush_rich_note()' not in part:continue
 part=part.replace('        self.flush_rich_note()',f'''        if folder_id and not glide_sidebar.accepts(self.sidebar_section_for("folder", folder_id), "list", "{kind}"):
            self.show_info("Anlegen", "Diese Dokumentart gehört nicht in diesen Bereich.")
            return "break"
        self.flush_rich_note()''',1)
 # Drawing has an implicit active folder; validate after resolution as well.
 if name=='create_new_drawing':
  part=part.replace('        folder = self.get_folder(folder_id) if folder_id else None', '''        if folder_id and not glide_sidebar.accepts(self.sidebar_section_for("folder", folder_id), "list", "drawing"):
            self.show_info("Anlegen", "Zeichnungen gehören in Zeichnungen oder Listen.")
            return "break"
        folder = self.get_folder(folder_id) if folder_id else None''')
 s=s[:start]+part+s[end:]
rep('        ordner = self.active_folder_id if self.view_mode == "folder" and self.get_folder(self.active_folder_id) else None','        ordner = self.active_folder_id if self.view_mode == "folder" and self.get_folder(self.active_folder_id) and self.sidebar_section_for("folder", self.active_folder_id) == "lists" else None')
# Default creation kind follows area, even for ordinary folders.
rep('        if is_list and list_kind is None and eltern is not None:', '''        if is_list and list_kind is None and section != "lists":
            list_kind = {"pages": "page", "notes": "note", "drawings": "drawing"}[section]
        if is_list and list_kind is None and eltern is not None:''')
# Filter folder kind selector, preserving identifiers and widget methods.
start=s.index('    def create_container_dialog(');end=s.index('\n    def ',start+5);part=s[start:end]
part=part.replace('[info["label"] for info in self.FOLDER_KINDS.values()]','[info["label"] for key, info in self.FOLDER_KINDS.items() if glide_sidebar.accepts(section, "folder", key)]')
# Templates match the section; folder templates may include nested incompatible documents.
part=part.replace('if template["kind"] == kind:', 'if template["kind"] == kind and self.sidebar_template_allowed(template, section):')
s=s[:start]+part+s[end:]
rep('    def create_in_sidebar_section(', '''    def sidebar_template_allowed(self, template, section):
        if section == "lists":
            return True
        if template.get("kind") == "list":
            return glide_sidebar.accepts(section, "list", template.get("list_kind", "tasks"))
        return glide_sidebar.accepts(section, "folder", template.get("folder_kind", "standard")) and all(
            glide_sidebar.accepts(section, "list", entry.get("list_kind", "tasks"))
            for entry in template.get("lists", []) if isinstance(entry, dict)) and all(
            self.sidebar_template_allowed(dict(child, kind="folder"), section)
            for child in template.get("folders", []) if isinstance(child, dict))

    def create_in_sidebar_section(''')
# Root context menu matches the entry's area rather than adding unrelated kinds.
start=s.index('        create_menu = self._new_themed_popup_menu(menu)',s.index('    def build_list_context_menu') if '    def build_list_context_menu' in s else s.index('        menu.add_command(label="Öffnen", command=lambda: self.set_active_list(list_id))'))
end=s.index('        move_menu = ',start)
s=s[:start]+'''        create_menu = self.folder_quick_add_menu(entry.get("folder_id")) if entry.get("folder_id") else self._new_themed_popup_menu(menu)
        if not entry.get("folder_id"):
            section = self.sidebar_section_for("list", list_id)
            for key, info in self.LIST_KINDS.items():
                if glide_sidebar.accepts(section, "list", key):
                    create_menu.add_command(label=f"Neue {info['label']} …", command=lambda k=key: self.create_container_dialog(
                        "list", list_kind=k, sidebar_section=section))
            create_menu.add_command(label="Neuer Ordner …", command=lambda: self.create_container_dialog(
                "folder", sidebar_section=section))
        menu.add_cascade(label="Neu anlegen", menu=create_menu)

'''+s[end:]
# Folder context uses the identical policy menu.
start=s.index('        menu.add_command(\n            label="Neue Liste in diesem Ordner …"');end=s.index('        move_menu = ',start) if '        move_menu = ' in s[start:start+2300] else -1
if end!=-1:
 part=s[start:end]; sep=part.rfind('        menu.add_separator()')
 s=s[:start]+'''        menu.add_cascade(label="Neu anlegen", menu=self.folder_quick_add_menu(folder_id))
        menu.add_separator()
'''+s[end:]
rep('if folder.get("id") != entry.get("folder_id")\n        ]','if folder.get("id") != entry.get("folder_id")\n            and self.sidebar_accepts("list", list_id, self.sidebar_section_for("folder", folder["id"]))\n        ]')
# Correct stats and overview selection.
rep('        if self.view_mode == self.NOTES_VIEW:\n            count = ', '        if self.view_mode == self.DRAWINGS_VIEW:\n            count = sum(1 for entry in self.lists if self.is_drawing_list(entry) and not self.is_archived_entry(entry))\n            self._set_stats_text("1 Zeichnung" if count == 1 else f"{count} Zeichnungen")\n            return\n        if self.view_mode == self.NOTES_VIEW:\n            count = ')
p.write_text(s)
# Ship the pure policy module in both runtime copies.
for f in ['scripts/pflege/abgleich_07.py','packaging/macos/baue_app.py']:
 p=Path(f);arc=p.parent/'archiv';arc.mkdir(exist_ok=True);a=arc/(p.stem+'_3.33.0_vor_3.33.1'+p.suffix)
 if not a.exists():a.write_bytes(p.read_bytes())
 p.write_text(p.read_text().replace('"schema_backups.py"','"schema_backups.py", "sidebar_policy.py"'))
