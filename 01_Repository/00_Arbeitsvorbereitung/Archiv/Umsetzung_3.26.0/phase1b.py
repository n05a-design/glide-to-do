from pathlib import Path
import ast
p=Path('01_Repository/Glide/src/glide/app.pyw');s=p.read_text(encoding='utf-8')
def r(a,b):
 global s
 assert a in s,a[:90]
 s=s.replace(a,b,1)
r('    LIST_COLOR_KEYS = [key for _label, key in LIST_COLOR_CHOICES]', '    ACCENT_COLOR_CHOICES = LIST_COLOR_CHOICES + [("Kontrastgrau", "muted")]\n    LIST_COLOR_KEYS = [key for _label, key in LIST_COLOR_CHOICES]')
r('accent if accent in cls.LIST_COLOR_KEYS else "accent"','accent if accent in dict((key, label) for label, key in cls.ACCENT_COLOR_CHOICES) else "accent"')
r('self.LABEL_COLOR_NAMES.get(self.settings.get("accent_color", "accent"), "Lila")','dict((key, label) for label, key in self.ACCENT_COLOR_CHOICES).get(self.settings.get("accent_color", "accent"), "Lila")')
r('appearance, accent, [label for label, key in self.LIST_COLOR_CHOICES],\n            option_colors={label: key for label, key in self.LIST_COLOR_CHOICES}', 'appearance, accent, [label for label, key in self.ACCENT_COLOR_CHOICES],\n            option_colors={label: key for label, key in self.ACCENT_COLOR_CHOICES}')
r('accent_color=next((key for label, key in self.LIST_COLOR_CHOICES','accent_color=next((key for label, key in self.ACCENT_COLOR_CHOICES')
r('return re.sub(r"\\s+(?:…|\\.\\.\\.)$", "", text)', 'text = re.sub(r"\\s*(?:…|\\.\\.\\.)$", "", text) if text.endswith((" …", " ...")) else text\n        return {"Punkte anheften": "Anheften", "Weitere Aktionen": "Aktionen"}.get(text, text)')
r('            return [(rand + x * nutz_b, rand + y * nutz_h, w * nutz_b, h * nutz_h)\n                    for x, y, w, h in self.PLACEHOLDER]', '            return []')
r('        if stufe == getattr(self, "_header_density", None):', '        if stufe == getattr(self, "_header_density", None):')
r('        self._header_density = stufe\n', '''        self._header_density = stufe
        actions = getattr(self, "actions_button", None)
        if actions is not None:
            actions.set_text(self.ICONS["actions"] if stufe == "minimal" else "Aktionen")
            actions.configure(width=44 if stufe == "minimal" else 94)
            self.add_tooltip(actions, "Aktionen durchsuchen")
        self.update_stats_label()
''')
r('    ICONS = {', '    ICONS = {\n        "actions": "☷",\n        "details": "≡",\n        "advanced": "✎",')
r('            self.stats_label.configure(text=kurz)', '            self.stats_label.configure(text="" if stufe == "minimal" else kurz)')
r('knopf.set_text("Anzeige")\n                    knopf.configure(width=96)', 'knopf.set_text(self.ICONS["details"])\n                    knopf.configure(width=44)\n                    self.add_tooltip(knopf, f"Anzeige: {self.detail_mode_name()}")')
# Keep the expanded entry form reachable in narrow layouts.
r('        should_show = width <= 50 or width >= self.advanced_button_min_width()', '''        compact = 50 < width < self.advanced_button_min_width()
        button.set_text(self.ICONS["advanced"] if compact else "Erweitert")
        button.configure(width=44 if compact else 108)
        self.add_tooltip(button, "Erweiterte Punkteingabe")
        should_show = width <= 50 or width >= 260''')
# An independently switchable companion; hiding its tile is still available.
r('("show_seconds", True), ("reminder_attention", True), ("history_enabled", True)', '("show_seconds", True), ("reminder_attention", True), ("history_enabled", True), ("mascot_playful", True)')
start=s.index('            def beruehren(_event=None):',s.index('        def kachel_mascot(parent):'))
end=s.index('            action(tile, "Benennen',start)
s=s[:start]+'''            def react(feed=False):
                if not self.settings.get("mascot_playful", True):
                    return "break"
                figur.react("freut" if feed else "winkt")
                pool = [satz, "Ein Schritt nach dem anderen.", "Ich bin hier, wenn du eine Pause brauchst."]
                if zustand == "sorgt":
                    pool += ["Du entscheidest, was heute dran ist.", "Auch Umplanen ist erlaubt."]
                elif zustand == "freut":
                    pool += ["Zeit, kurz durchzuatmen.", "Das darf sich gut anfühlen."]
                elif zustand == "schlaeft":
                    pool += ["Heute darf es ruhig sein.", "Ich halte hier die Stellung."]
                hinweis.configure(text="Danke für den kleinen Snack!" if feed else random.choice(pool),
                                  relief="solid", borderwidth=1, padx=8, pady=8)
                return "break"

            def beruehren(_event=None):
                return react()

            def streicheln(_event=None):
                if self.settings.get("mascot_playful", True):
                    figur.react("freut", schritte=5)

            for sequenz in ("<Button-1>", "<Return>", "<space>"):
                figur.bind(sequenz, beruehren)
            figur.bind("<Enter>", streicheln)
            if self.settings.get("mascot_playful", True):
                action(tile, "Füttern", lambda: react(feed=True), "confirm")

            def toggle_play():
                before = self.settings.get("mascot_playful", True)
                self.settings["mascot_playful"] = not before
                if self.save_settings():
                    self.refresh_home()
                else:
                    self.settings["mascot_playful"] = before
            action(tile, "Spielereien aus" if self.settings.get("mascot_playful", True) else "Spielereien an",
                   toggle_play, "muted")
''' +s[end:]
# No idle animation when play is disabled.
r('        if not self.app.animations_enabled():\n            return\n        self._schedule_blink()', '        if not self.app.animations_enabled() or not self.app.settings.get("mascot_playful", True):\n            return\n        self._schedule_blink()')
ast.parse(s);p.write_text(s,encoding='utf-8')
print('Phase 1b applied')
