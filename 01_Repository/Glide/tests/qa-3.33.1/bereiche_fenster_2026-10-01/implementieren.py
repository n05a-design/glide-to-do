from pathlib import Path
p=Path('src/glide/app.pyw');s=p.read_text()
def rep(a,b,n=1):
 global s
 assert s.count(a)>=n,(a[:100],s.count(a),n)
 s=s.replace(a,b,n)
def method(name,body):
 global s
 start=s.index('    def '+name+'(');end=s.find('\n    def ',start+5)
 # Preserve decorators on the next method.
 dec=s.rfind('\n    @',start,end)
 if dec>start:end=dec
 s=s[:start]+body.rstrip()+'\n'+s[end:]
rep('import logo as glide_logo  # noqa: E402','import logo as glide_logo  # noqa: E402\nimport sidebar_policy as glide_sidebar  # noqa: E402')
rep('    NOTES_VIEW = "notes"','    NOTES_VIEW = "notes"\n    DRAWINGS_VIEW = "drawings"')
s=s.replace('self.PAGES_VIEW, self.NOTES_VIEW,','self.PAGES_VIEW, self.NOTES_VIEW, self.DRAWINGS_VIEW,').replace('app.PAGES_VIEW, app.NOTES_VIEW,','app.PAGES_VIEW, app.NOTES_VIEW, app.DRAWINGS_VIEW,')
rep('("views", "pinned", "pages", "lists", "notes")','("views", "pinned", "pages", "lists", "notes", "drawings")')
rep('        zu = result.get("sidebar_sections_closed")','        result["sidebar_sections_visible"] = glide_sidebar.normalize_visibility(result.get("sidebar_sections_visible"))\n        result["sidebar_locations"] = glide_sidebar.normalize_locations(result.get("sidebar_locations"))\n        zu = result.get("sidebar_sections_closed")')
rep('        self.create_notes_sidebar()','        self.create_notes_sidebar()\n        self.create_drawings_sidebar()')
rep('getattr(self, "notes_listbox", None)) if baum is not None]','getattr(self, "notes_listbox", None), getattr(self, "drawings_listbox", None)) if baum is not None]')
s=s.replace('("system_listbox", "pages_listbox", "notes_listbox", "sidebar_listbox")','("system_listbox", "pages_listbox", "notes_listbox", "drawings_listbox", "sidebar_listbox")').replace('("system_listbox", "sidebar_listbox", "pages_listbox", "notes_listbox")','("system_listbox", "sidebar_listbox", "pages_listbox", "notes_listbox", "drawings_listbox")')
rep('        for bereich in (getattr(self, "pages_listbox", None), getattr(self, "notes_listbox", None)):','        for bereich in (getattr(self, "pages_listbox", None), getattr(self, "notes_listbox", None),\n                        getattr(self, "drawings_listbox", None)):')
rep('            for bereich in (seitenbaum, notizbaum):','            zeichnungsbaum = getattr(self, "drawings_listbox", None)\n            for bereich in (seitenbaum, notizbaum, zeichnungsbaum):')
rep('            for bereich in (seitenbaum, notizbaum):','            for bereich in (seitenbaum, notizbaum, zeichnungsbaum):')
rep('        self.update_notes_heading()\n        self.refresh_sidebar_row_texts()','        self.update_notes_heading()\n        self.update_drawings_heading()\n        self.refresh_sidebar_row_texts()')
rep('    def build_sidebar_section(','''    def create_drawings_sidebar(self):
        (self.drawings_title_row, self.drawings_heading_frame, self.drawings_heading_icon, self.drawings_title,
         self.add_drawings_button, self.drawings_listbox) = self.build_sidebar_section(
            "drawings", "Zeichnungen", self.set_drawings_view, "Alle Zeichnungen",
            self.show_drawings_add_menu, "Neue Zeichnung oder Ordner", self.SIDEBAR_LISTS_GAP)

    def sidebar_policy(self):
        return self.render_cached("sidebar_policy", lambda: glide_sidebar.SidebarPolicy(
            self.lists, self.folders, self.settings.get("sidebar_locations"),
            self.settings.get("sidebar_sections_visible")))

    def sidebar_section_for(self, kind, identifier):
        return self.sidebar_policy().section(kind, identifier)

    def sidebar_section_for_tree(self, tree):
        return next((key for key, name in (("pages", "pages_listbox"), ("notes", "notes_listbox"),
                     ("drawings", "drawings_listbox")) if tree is getattr(self, name, None)), "lists")

    def locate_sidebar_root(self, kind, identifier, section):
        if section in glide_sidebar.SECTIONS:
            self.settings.setdefault("sidebar_locations", {})[f"{kind}:{identifier}"] = section
            self.clear_render_cache()

    def sidebar_accepts(self, kind, identifier, section):
        policy = self.sidebar_policy()
        if kind == "folder":
            return policy.subtree_accepts(identifier, section)
        entry = policy.entries.get(identifier)
        return bool(entry and glide_sidebar.accepts(section, kind, entry.get("list_kind", "tasks")))

    def sidebar_section_visible(self, key):
        return glide_sidebar.normalize_visibility(self.settings.get("sidebar_sections_visible")).get(key, True)

    def apply_sidebar_visibility(self):
        # Hide only navigation. Documents remain reachable through Lists and search.
        for key in ("pages", "notes", "drawings"):
            row = getattr(self, f"{key}_title_row", None)
            if row is None:
                continue
            if not self.sidebar_section_visible(key):
                row.pack_forget()
            elif not row.winfo_manager():
                before = next((getattr(self, f"{later}_title_row", None) for later in glide_sidebar.SECTIONS[
                    glide_sidebar.SECTIONS.index(key)+1:] if getattr(self, f"{later}_title_row", None) is not None
                    and getattr(self, f"{later}_title_row").winfo_manager()), None)
                if key == "pages":
                    before = self.sidebar_title_row
                row.pack(fill="x", pady=(self.SIDEBAR_SECTION_GAP if key == "pages" else self.SIDEBAR_LISTS_GAP, 8),
                         **({"before": before} if before else {}))

    def show_drawings_add_menu(self, event=None):
        menu = self._new_themed_popup_menu()
        menu.add_command(label="Neue Zeichnung", command=self.create_new_drawing)
        menu.add_command(label="Neuer Ordner …", command=lambda: self.create_container_dialog(
            "folder", sidebar_section="drawings"))
        self._popup_at_widget(menu, self.add_drawings_button)
        return "break"

    def set_drawings_view(self, refresh=True):
        self._activate_system_view(self.DRAWINGS_VIEW, refresh=refresh)
        return "break"

    def render_drawings_page(self):
        for widget in self.home_content.winfo_children():
            widget.destroy()
        card = self.make_rounded_container(self.home_content, fill_key="card", outline_key="line",
                                          radius=18, padding=10, register=False, auto_height=True)
        card.pack(fill="x")
        body = tk.Frame(card.inner, bg=self.theme["card"])
        body.pack(fill="both", expand=True, padx=14, pady=12)
        self._make_dialog_button(body, "Neue Zeichnung", self.create_new_drawing, "confirm").pack(anchor="w", pady=(0, 12))
        entries = sorted((e for e in self.lists if self.is_drawing_list(e) and not self.is_archived_entry(e)),
                         key=lambda e: str(e.get("title", "")).casefold())
        rows = [(None, e.get("title") or "Zeichnung", lambda lid=e["id"]: self.set_active_list(lid),
                 self.drawing_summary(e)) for e in entries]
        self.render_overview_sections(body, [("Alle Zeichnungen", rows, "Noch keine Zeichnungen. „Neue Zeichnung“ legt eine an.")])
        self._bind_home_wheel(card)

    def build_sidebar_section(''')
method('sidebar_tree_for_entry','''    def sidebar_tree_for_entry(self, entry):
        key = self.sidebar_section_for("list", entry.get("id"))
        return getattr(self, {"pages": "pages_listbox", "notes": "notes_listbox", "drawings": "drawings_listbox"}.get(
            key, "sidebar_listbox"), getattr(self, "sidebar_listbox", None))''')
method('sidebar_tree_for_folder','''    def sidebar_tree_for_folder(self, folder):
        key = self.sidebar_section_for("folder", folder.get("id"))
        return getattr(self, {"pages": "pages_listbox", "notes": "notes_listbox", "drawings": "drawings_listbox"}.get(
            key, "sidebar_listbox"), getattr(self, "sidebar_listbox", None))''')
rep('("notes", getattr(self, "notes_listbox", None), getattr(self, "notes_title_row", None)))','("notes", getattr(self, "notes_listbox", None), getattr(self, "notes_title_row", None)),\n            ("drawings", getattr(self, "drawings_listbox", None), getattr(self, "drawings_title_row", None)))')
rep('self.visible_tree_rows(baum) if self.sidebar_section_open(schluessel) else 0','self.visible_tree_rows(baum) if self.sidebar_section_open(schluessel) and self.sidebar_section_visible(schluessel) else 0')
rep('        theme = self.theme\n        kopf = getattr(self, "views_collapsed_header", None)','        self.apply_sidebar_visibility()\n        theme = self.theme\n        kopf = getattr(self, "views_collapsed_header", None)')
rep('(getattr(self, "notes_heading_icon", None), "notes"))','(getattr(self, "notes_heading_icon", None), "notes"),\n                                  (getattr(self, "drawings_heading_icon", None), "drawings"))')
rep('getattr(self, "pages_title_row", None) or titelzeile','(getattr(self, "pages_title_row", None) if self.sidebar_section_visible("pages") else None) or titelzeile')
rep('    def update_section_heading(self, key, hover=False):\n','    def update_section_heading(self, key, hover=False):\n        if key == "drawings":\n            return self.update_drawings_heading(hover=hover)\n')
rep('    def update_notes_heading(self, hover=False):','    def update_drawings_heading(self, hover=False):\n        self._paint_section_heading("drawings", self.view_mode == self.DRAWINGS_VIEW, hover)\n\n    def update_notes_heading(self, hover=False):')
rep('        self.update_notes_heading()\n        # Der Seitentitel','        self.update_notes_heading()\n        self.update_drawings_heading()\n        # Der Seitentitel')
# New view follows existing overview paths, including restart and Undo.
rep('        if self.view_mode == self.NOTES_VIEW:\n            return "Notizen"','        if self.view_mode == self.DRAWINGS_VIEW:\n            return "Zeichnungen"\n        if self.view_mode == self.NOTES_VIEW:\n            return "Notizen"')
rep('        if self.view_mode == self.NOTES_VIEW:\n            self.set_note_preview','        if self.view_mode == self.DRAWINGS_VIEW:\n            self.set_note_preview(text="Deine Zeichnungen · Zeile anklicken zum Öffnen")\n            return\n        if self.view_mode == self.NOTES_VIEW:\n            self.set_note_preview')
rep('        if self.view_mode == self.NOTES_VIEW:\n            self.tree.selection_remove', '        if self.view_mode == self.DRAWINGS_VIEW:\n            self.tree.selection_remove(self.tree.selection())\n            self.render_drawings_page()\n            return\n        if self.view_mode == self.NOTES_VIEW:\n            self.tree.selection_remove') if '        if self.view_mode == self.NOTES_VIEW:\n            self.tree.selection_remove' in s else None
rep('        if self.view_mode == self.NOTES_VIEW:\n            self.update_stats_label()', '        if self.view_mode == self.DRAWINGS_VIEW:\n            self.update_stats_label()\n            self.tree.selection_remove(self.tree.selection())\n            self.render_drawings_page()\n            return\n        if self.view_mode == self.NOTES_VIEW:\n            self.update_stats_label()')
# Snapshot UI locations so root Drag-and-drop can be reverted together with data.
rep('                "lists": PackedState(self.lists),','                "sidebar_locations": copy.deepcopy(self.settings.get("sidebar_locations", {})),\n                "lists": PackedState(self.lists),')
rep('        self.lists = unpack_state(snapshot.get("lists"))','        self.settings["sidebar_locations"] = copy.deepcopy(snapshot.get("sidebar_locations", {}))\n        self.save_settings()\n        self.lists = unpack_state(snapshot.get("lists"))')
rep('        change.saved = self.save_items()\n        if change.saved and feedback:', '        change.saved = self.save_items()\n        self.save_settings()\n        if change.saved and feedback:')
# Visibility settings, persisted and applied without deleting anything.
rep('        animationen = tk.BooleanVar(value=self.settings.get("animations_enabled", True))','        animationen = tk.BooleanVar(value=self.settings.get("animations_enabled", True))\n        sidebar_visibility = {key: tk.BooleanVar(value=self.sidebar_section_visible(key))\n                              for key in ("pages", "notes", "drawings")}')
rep('        tk.Label(personal, text="Ansicht beim Öffnen",', '''        tk.Label(appearance, text="Bereiche der Seitenleiste", bg=self.theme["bg"], fg=self.theme["muted"],
                 font=app_font(10), anchor="w").pack(fill="x", pady=(8, 4))
        for key, variable in sidebar_visibility.items():
            tk.Checkbutton(appearance, text=glide_sidebar.TITLES[key], variable=variable,
                           name=f"setting_sidebar_{key}", bg=self.theme["bg"], fg=self.theme["text"],
                           activebackground=self.theme["bg"], activeforeground=self.theme["text"],
                           selectcolor=self.theme["input"], anchor="w", font=app_font(10)).pack(fill="x", pady=3)
        tk.Label(appearance, text="Listen bleibt immer sichtbar. Ausgeblendete Inhalte findest du dort weiterhin.",
                 bg=self.theme["bg"], fg=self.theme["muted"], font=app_font(9), wraplength=300,
                 justify="left", anchor="w").pack(fill="x", pady=(0, 8))
        tk.Label(personal, text="Ansicht beim Öffnen",''')
rep('            self.settings.update(profile_name=name.get(), profile_logo=clean_logo,','            self.settings.update(sidebar_sections_visible={"lists": True, **{key: value.get() for key, value in sidebar_visibility.items()}},\n                                 profile_name=name.get(), profile_logo=clean_logo,')
rep('            self.apply_theme()\n            self.update_header_title()\n            self.refresh_tree()','            self.apply_theme()\n            self.update_sidebar_list()\n            self.update_header_title()\n            self.refresh_tree()')
# Section creation: ordinary folders keep their area through UI settings.
rep('def create_container_dialog(self, kind="list", parent_id=None, list_kind=None, folder_kind=None):','def create_container_dialog(self, kind="list", parent_id=None, list_kind=None, folder_kind=None, sidebar_section=None):')
rep('        is_list = kind == "list"\n        eltern =', '        is_list = kind == "list"\n        section = sidebar_section or (self.sidebar_section_for("folder", parent_id) if parent_id else "lists")\n        eltern =')
rep('[info["label"] for info in self.LIST_KINDS.values()] + [self.BOARD_KIND_LABEL]', '[info["label"] for key, info in self.LIST_KINDS.items() if glide_sidebar.accepts(section, "list", key)]\n                + ([self.BOARD_KIND_LABEL] if section == "lists" else [])')
# Folder selection and templates are validated at submit, before any creation.
rep('            chosen_kind = self.LIST_KIND_BY_LABEL.get(list_kind_var.get(), self.LIST_KIND_TASKS)','''            chosen_kind = self.LIST_KIND_BY_LABEL.get(list_kind_var.get(), self.LIST_KIND_TASKS)
            chosen_folder_kind = self.FOLDER_KIND_BY_LABEL.get(folder_kind_var.get(), "standard")
            target_section = self.sidebar_section_for("folder", parent) if parent else section
            candidate_kind = chosen_kind if is_list else chosen_folder_kind
            if template_id:
                template = self.template_by_id(template_id) or {}
                candidate_kind = template.get("list_kind", "tasks") if is_list else template.get("folder_kind", "standard")
            if not glide_sidebar.accepts(target_section, kind, candidate_kind):
                error.configure(text=f"Diese Art gehört nicht in den Bereich {glide_sidebar.TITLES[target_section]}.")
                return''')
rep('                holder["folder_id" if is_list else "parent_id"] = parent','                holder["folder_id" if is_list else "parent_id"] = parent\n                if not parent:\n                    self.locate_sidebar_root(kind, holder["id"], section)')
rep('        menu.add_command(label="Neue Bibliothek …",','        menu.add_command(label="Neuer Ordner …", command=lambda: self.create_container_dialog("folder", sidebar_section="pages"))\n        menu.add_command(label="Neue Bibliothek …",')
rep('"folder", parent_id=None, folder_kind="library"))','"folder", parent_id=None, folder_kind="library", sidebar_section="pages"))')
rep('        menu.add_command(label="Neues Notizbuch …",','        menu.add_command(label="Neuer Ordner …", command=lambda: self.create_container_dialog("folder", sidebar_section="notes"))\n        menu.add_command(label="Neues Notizbuch …",')
rep('"folder", parent_id=None, folder_kind="journal"))','"folder", parent_id=None, folder_kind="journal", sidebar_section="notes"))')
# Replace folder quick menu with section-wide policy; Lists permits every kind.
start=s.index('        ordnerart = ',s.index('    def folder_quick_add_menu('));end=s.index('        if folder_id is None:',start)
s=s[:start]+'''        section = self.sidebar_section_for("folder", folder_id) if folder_id else "lists"
        ordnerart = (self.get_folder(folder_id) or {}).get("folder_kind")
        if section == "lists":
            menu.add_command(label="Neue Liste …", command=lambda: self.create_container_dialog("list", parent_id=folder_id))
        if section in ("pages", "lists"):
            menu.add_command(label="Neue Seite", command=lambda: self.create_in_sidebar_section("page", folder_id, section))
            menu.add_cascade(label="Seite aus Vorlage", menu=self.page_template_menu(menu, folder_id))
        if section in ("notes", "lists"):
            if ordnerart == "journal":
                menu.add_command(label="Neue Tagesnotiz", command=lambda: self.create_journal_entry(folder_id))
            menu.add_command(label="Neue Notiz …", command=lambda: self.create_container_dialog(
                "list", parent_id=folder_id, list_kind=self.LIST_KIND_NOTE, sidebar_section=section))
        if section == "lists":
            menu.add_command(label="Neue Pinnwand …", command=lambda: self.create_container_dialog(
                "list", parent_id=folder_id, list_kind="board"))
            menu.add_command(label="Neue Galerie", command=lambda: self.create_new_gallery(folder_id))
        if section in ("drawings", "lists"):
            menu.add_command(label="Neue Zeichnung", command=lambda: self.create_in_sidebar_section("drawing", folder_id, section))
        for key, info in self.FOLDER_KINDS.items():
            if glide_sidebar.accepts(section, "folder", key):
                menu.add_command(label=("Neuer Unterordner …" if folder_id else "Neuer Ordner …") if key == "standard"
                                 else f"Neue {info['label']} …" if key == "library" else "Neues Notizbuch …",
                                 command=lambda k=key: self.create_container_dialog(
                                     "folder", parent_id=folder_id, folder_kind=k, sidebar_section=section))
'''+s[end:]
# Context wrapper applies a root preference inside the creation mutation, before save/render.
rep('    def create_new_drawing(self, folder_id=None, event=None, size=glide_drawing.WIDTH):','''    def create_in_sidebar_section(self, list_kind, folder_id, section):
        previous = getattr(self, "_creating_sidebar_section", None)
        self._creating_sidebar_section = section
        try:
            method = self.create_new_drawing if list_kind == "drawing" else self.create_new_page
            return method(folder_id)
        finally:
            self._creating_sidebar_section = previous

    def create_new_drawing(self, folder_id=None, event=None, size=glide_drawing.WIDTH):''')
# Existing creation sites have the same append entry invariant; only page/drawing methods get it.
for name in ('create_new_drawing','create_new_page'):
 start=s.index('    def '+name+'(');end=s.find('\n    def ',start+5);part=s[start:end]
 target='            self.lists.append(entry)'
 assert target in part,name
 part=part.replace(target,'''            if not entry.get("folder_id") and getattr(self, "_creating_sidebar_section", None):
                self.locate_sidebar_root("list", entry["id"], self._creating_sidebar_section)
            self.lists.append(entry)''');s=s[:start]+part+s[end:]
# Drops validate against the destination section and complete subtree; dates/kinds stay untouched.
rep('        if not self.ensure_journal_moment(list_entry, folder_id):','        if not self.sidebar_accepts("list", list_id, self.sidebar_section_for("folder", folder_id)):\n            return False\n        if not self.ensure_journal_moment(list_entry, folder_id):')
rep('        if not self.ensure_journal_moment(source, target.get("folder_id")):','        target_section = self.sidebar_section_for("list", target_id)\n        if not self.sidebar_accepts("list", source_id, target_section):\n            return False\n        if not target.get("folder_id"):\n            self.locate_sidebar_root("list", source_id, target_section)\n        if not self.ensure_journal_moment(source, target.get("folder_id")):')
rep('        if self.folder_is_descendant(target_id, folder_id):\n            return False','        if self.folder_is_descendant(target_id, folder_id):\n            return False\n        if not self.sidebar_accepts("folder", folder_id, self.sidebar_section_for("folder", target_id)):\n            return False')
rep('        new_parent = target.get("parent_id")\n        if not self.can_move_folder_into','        new_parent = target.get("parent_id")\n        target_section = self.sidebar_section_for("folder", target_id)\n        if not self.sidebar_accepts("folder", source_id, target_section):\n            return False\n        if not new_parent:\n            self.locate_sidebar_root("folder", source_id, target_section)\n        if not self.can_move_folder_into')
start=s.index('        # Eine freie Fläche gehört',s.index('    def on_sidebar_drag_end'));end=s.index('        # Mehrfachauswahl:',start)
s=s[:start]+'''        target_section = self.sidebar_section_for_tree(target_tree)
        if not target_row and not self.sidebar_accepts(source_row[0], source_row[1], target_section):
            return "break"

'''+s[end:]
rep('            if source_row[0] == "list":\n                self.drop_sidebar_list','            if not target_row:\n                self.locate_sidebar_root(source_row[0], source_row[1], target_section)\n            if source_row[0] == "list":\n                self.drop_sidebar_list')
# Relative root moves can move compatible content to Lists without conversion.
rep('self.sidebar_tree_for_entry(dict(source, folder_id=None)) is not self.get_sidebar_tree_for_iid(target_iid)', 'not self.sidebar_accepts("list", list_id, self.sidebar_section_for_tree(self.get_sidebar_tree_for_iid(target_iid)))')
# Root-only insertion: previously section selection assumed all section entries were root entries.
rep('if entry.get("archived") or self.sidebar_tree_for_entry(entry) is not bereich:', 'if entry.get("archived") or entry.get("folder_id") in assigned_folder_ids or self.sidebar_tree_for_entry(entry) is not bereich:')
# Logo starts at the cap height rather than the padded title row edge.
method('header_logo_height','''    def header_logo_height(self):
        font = self.cached_font("_header_subtitle_font", app_font(9, "bold"))
        line = font.metrics("linespace") if font is not None else 18
        return max(24, self.title_row.winfo_reqheight() + max(self.page_chip_row.winfo_reqheight(), line + 6)
                   - self.header_logo_top_inset())

    def header_logo_top_inset(self):
        font = self.cached_font("_header_cap_font", self.header_title_font())
        if font is None:
            return 4
        pixels = abs(font.actual("size")) * float(self.root.tk.call("tk", "scaling"))
        return max(2, round(font.metrics("ascent") - pixels * 0.72) + CanvasLabel.LABEL_INSET_Y + 1)''')
rep('anchor="nw", padx=(0, self.HEADER_LOGO_GAP), before=self.title_block','anchor="nw", padx=(0, self.HEADER_LOGO_GAP), pady=(self.header_logo_top_inset(), 0), before=self.title_block')
rep('            hoehe = self.header_logo_height()','            if leinwand.winfo_manager():\n                leinwand.pack_configure(pady=(self.header_logo_top_inset(), 0))\n            hoehe = self.header_logo_height()')
rep('            self._sidebar_row_font = None','            self._header_cap_font = None\n            self._header_subtitle_font = None\n            self._sidebar_row_font = None')
p.write_text(s)
print('app geändert',len(s.splitlines()))
