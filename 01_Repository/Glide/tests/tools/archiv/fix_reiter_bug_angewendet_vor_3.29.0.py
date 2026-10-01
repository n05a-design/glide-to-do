import pathlib

p = pathlib.Path('src/glide/app.pyw')
text = p.read_text(encoding='utf-8')

# Bug 5.4 Fix: Reiter-Dropdown reparieren
old_code = """        choices = []
        ids = {}
        for index, tab in enumerate(self.app.settings["open_tabs"], 1):
            found = self.app.find_item_in_lists(tab["item_id"])
            if found:
                label = f"{index}. {found[3].get('title', '')} · {self.app.item_display_text(found[0])}"
                choices.append(label); ids[label] = tab["item_id"]
        if not choices:
            return self.app.show_info("Reiter", "Noch keine Punktreiter geöffnet. Einen Punkt auswählen und „Als Reiter öffnen“ benutzen.")
        chosen = self.app.themed_choice_dialog("Offene Reiter", "Reiter auswählen", choices)
        if chosen in ids:
            self.open_tab(ids[chosen])"""

new_code = """        choices = []
        for index, tab in enumerate(self.app.settings["open_tabs"], 1):
            found = self.app.find_item_in_lists(tab["item_id"])
            if found:
                label = f"{index}. {found[3].get('title', '')} · {self.app.item_display_text(found[0])}"
                choices.append((tab["item_id"], label))
        if not choices:
            return self.app.show_info("Reiter", "Noch keine Punktreiter geöffnet. Einen Punkt auswählen und „Als Reiter öffnen“ benutzen.")
        chosen = self.app.themed_choice_dialog("Offene Reiter", "Reiter auswählen", choices)
        if chosen:
            self.open_tab(chosen)"""

# In case the special characters are slightly different, use a robust replacement:
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'def tab_overview(self):' in line:
        start_idx = i
        break
for i in range(start_idx, start_idx + 25):
    if 'choices.append(label); ids[label] = tab["item_id"]' in lines[i]:
        # found it
        lines[i] = lines[i].replace('choices.append(label); ids[label] = tab["item_id"]', 'choices.append((tab["item_id"], label))')
    elif 'ids = {}' in lines[i]:
        lines[i] = ''
    elif 'if chosen in ids:' in lines[i]:
        lines[i] = lines[i].replace('if chosen in ids:', 'if chosen:')
    elif 'self.open_tab(ids[chosen])' in lines[i]:
        lines[i] = lines[i].replace('self.open_tab(ids[chosen])', 'self.open_tab(chosen)')

p.write_text('\n'.join(lines), encoding='utf-8')
print("Bug 5.4 behoben")
