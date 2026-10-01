from pathlib import Path

p = Path(__file__).resolve().parents[2] / '01_Repository/Glide/src/glide/app.pyw'
s = p.read_text(encoding='utf-8')
start = s.index('        # Punkt 20 (3.23.0): Alles ab hier')
end = s.index('        kind_names =', start)
s = s[:start] + '''        # Gemeinsame Zeilen halten Feldkanten auch bei längeren Labels bündig.
        # Bei weniger als 720 Pixeln werden die Feldpaare untereinander angeordnet.
        grid = FieldPairGrid(inner, bg=self.theme["bg"], gap=16,
                             uniform="item_form_fields", responsive=True)
        grid.pack(fill="x")
        details_grid = FieldPairGrid(inner, bg=self.theme["bg"], gap=16,
                                     uniform="item_form_details", responsive=True)
        details_grid.pack(fill="x", pady=(14, 0))

''' + s[end:]
a = s.index('        # --- Fälligkeit mit Kalender und Uhrzeit ---', start)
b = s.index('        def submit(event=None):', a)
chunk = s[a:b]
def change(old, new):
    global chunk
    assert old in chunk, old[:100]
    chunk = chunk.replace(old, new, 1)
change('''        due_block = tk.Frame(links, bg=self.theme["bg"])
        due_block.pack(fill="x", pady=(14, 0))
        self._make_field_label(due_block, "Fälligkeit").pack(anchor="w", pady=(0, self.FIELD_LABEL_GAP))''', '''        due_label, due_block = details_grid.cell(0, 0)
        self._make_field_label(due_label, "Fälligkeit").pack(side="bottom", fill="x", pady=(0, self.FIELD_LABEL_GAP))''')
change('''        repeat_block = tk.Frame(links, bg=self.theme["bg"])
        repeat_block.pack(fill="x", pady=(14, 0))
        self._make_field_label(repeat_block, "Wiederholung").pack(
            anchor="w", pady=(0, self.FIELD_LABEL_GAP)
        )''', '''        repeat_label, repeat_block = details_grid.cell(0, 1, pady=(14, 0))
        self._make_field_label(repeat_label, "Wiederholung").pack(
            side="bottom", fill="x", pady=(0, self.FIELD_LABEL_GAP))''')
change('''        reminder_block, read_reminder = self.make_reminder_editor(links, dialog, source)

        plan_block = tk.Frame(links, bg=self.theme["bg"])
        plan_block.pack(fill="x", pady=(14, 0))''', '''        reminder_label, reminder_cell = details_grid.cell(0, 2, pady=(14, 0))
        reminder_block, read_reminder = self.make_reminder_editor(reminder_cell, dialog, source)
        reminder_block.pack(fill="x")

        _plan_label, plan_block = details_grid.cell(0, 3, pady=(14, 0))''')
change('''        label_block = tk.Frame(rechts, bg=self.theme["bg"])
        label_block.pack(fill="x", pady=(14, 0))
        # Der Anker steht ganz unten in der linken Spalte, ohne eigene Höhe.
        links_anker.pack(fill="x", side="bottom")
        spalten.pack(fill="both", expand=True)
        self._make_field_label(label_block, "Labels (Mehrfachauswahl)").pack(
            anchor="w", pady=(0, self.FIELD_LABEL_GAP)
        )''', '''        label_heading, label_block = details_grid.cell(1, 0)
        self._make_field_label(label_heading, "Labels (Mehrfachauswahl)").pack(
            side="bottom", fill="x", pady=(0, self.FIELD_LABEL_GAP))''')
x = chunk.index('            if schedulable:\n                right.grid()')
y = chunk.index('            hint_label.configure(', x)
chunk = chunk[:x] + '''            grid.set_cell_visible(1, 0, schedulable)
            for row in range(4):
                details_grid.set_cell_visible(0, row, schedulable)
            details_grid.set_cell_visible(1, 2, schedulable)
''' + chunk[y:]
change('''        self._make_field_label(rechts, "Beschreibung").pack(anchor="w", pady=(14, self.FIELD_LABEL_GAP))
        description_border, description_field = self._make_field(rechts)''', '''        description_heading, description_cell = details_grid.cell(1, 1, pady=(14, 0))
        self._make_field_label(description_heading, "Beschreibung").pack(side="bottom", fill="x", pady=(0, self.FIELD_LABEL_GAP))
        description_border, description_field = self._make_field(description_cell)''')
change('''        checklist_block = tk.Frame(rechts, bg=self.theme["bg"])
        if schedulable:
            checklist_block.pack(fill="x")''', '''        _checklist_heading, checklist_block = details_grid.cell(1, 2, pady=(14, 0))
        details_grid.set_cell_visible(1, 2, schedulable)''')
change('''        attachment_heading = tk.Frame(rechts, bg=self.theme["bg"])
        attachment_heading.pack(fill="x", pady=(14, self.FIELD_LABEL_GAP))''', '''        attachment_heading, attachment_cell = details_grid.cell(1, 3, pady=(14, 0))''')
change('''        self._make_attachment_editor(rechts, dialog, attachments)''', '''        self._make_attachment_editor(attachment_cell, dialog, attachments)''')
chunk = chunk.replace('''        # Wechselt die Art später auf „Aufgabe", muss die Checkliste wieder an
        # ihre Stelle zwischen Beschreibung und Anhängen zurückfinden.
        form_state["checklist_anchor"] = attachment_heading
''', '')
s = s[:a] + chunk + s[b:]
p.write_text(s, encoding='utf-8')
print('Punktmaske auf gemeinsame responsive Feldraster umgestellt.')
