# SPDX-License-Identifier: MPL-2.0
"""E02: drei fachlich verschiedene neutrale Hosts auf derselben Shell und demselben Bento (T377).

Läuft im Checkpoint (nur `glide_shell` und `glide_bento` im Suchpfad, `-I`).
Keine Musik-, Schach- oder Glide-Fachlogik; Daten sind künstlich.

- Host A „Notizen“: text- und listenorientierte Arbeitsbereiche, Suchfeld filtert eine Liste.
- Host B „Zeichenfläche“: Canvas-Arbeitsbereich mit gruppierter Werkzeugleiste; Werkzeuge zeichnen.
- Host C „Übersicht“: Bento-Karten, Tabelle und Detailansicht mit Auswahl.

Belegt je Host: Start über `AppHost` mit Startprüfung, Navigation über `WorkspaceHost`
(Klick, Kürzel, Strg+Tab), Theme über `ThemeProvider` (hell, dunkel, eigene Markenfarbe),
modaler Dialog mit Fokusrückgabe, Einstellungen über `SettingsRegistry` (Shell- und
Host-Einstellungen), Eingabe, Canvas, responsives Verhalten (Werkzeugleiste bricht um,
Bento-Spalten), Ressourcenfreigabe (keine offenen Zeitgeber) und geordnetes Beenden.
"""
import sys
import tkinter as tk
from tkinter import ttk

from glide_shell import app_host, color_roles, controls, modal_session, settings_registry, window_lifetime, workspaces
import glide_bento as b

VERBOTEN = ("app", "ui_design", "i18n", "planning", "ai_workspace", "data_lock", "chapters")
assert not any(m in sys.modules for m in VERBOTEN), sorted(m for m in VERBOTEN if m in sys.modules)


def pump(root, n=4):
    for _ in range(n):
        root.update()


class Host:
    """Gemeinsamer Rahmen; die drei Hosts unterscheiden sich nur in ihren Arbeitsbereichen."""

    def __init__(self, name, accent, workspaces_fn, host_settings):
        self.name, self.events = name, []
        self.provider = color_roles.ThemeProvider(mode="light", accent=accent)
        self.settings = settings_registry.SettingsRegistry(settings_registry.shell_settings() + host_settings)
        self.werte, probleme = self.settings.normalize({"shell.theme_mode": "dark", "shell.font_scale": 7})
        assert probleme and self.werte["shell.font_scale"] == 1.0 and self.werte["shell.theme_mode"] == "dark"
        self.host = app_host.AppHost(preflight=(lambda _w: None,), on_callback_error=self._fehler)
        self.root = None
        self._workspaces_fn = workspaces_fn

    def _fehler(self, *exc):
        self.events.append(("error", repr(exc[1])))

    def controller(self, root):
        self.root = root
        root.geometry("980x640+40+40")
        self.platform = app_host.platform_of(root.tk.call("tk", "windowingsystem"))
        self.registry = workspaces.WorkspaceRegistry(self._workspaces_fn(self))
        self.ws = workspaces.WorkspaceHost(root, self.registry, self.provider.roles(),
                                           on_change=lambda w: self.events.append(("show", w)))
        self.ws.pack(fill="both", expand=True)
        self.ws.bind_shortcuts(root, self.platform)
        self.provider.subscribe(self.ws.set_theme)
        self.host.add_shutdown(self.ws.close)
        app_host.install_close(root, self.host.shutdown, self.platform, quit_command=False)
        self.ws.show(self.registry.ids()[0])
        return self

    def start(self):
        self.host.run(self.controller, mainloop=False)
        pump(self.root)
        return self

    def dialog_probe(self):
        """Modaler Dialog über dem Hauptfenster; Fokus kehrt zurück."""
        ziel = self.ws.nav_buttons[self.ws.current]
        ziel.focus_force()
        pump(self.root)
        dialog = modal_session.create_dialog(self.root, f"{self.name}: Einstellungen")
        knopf = controls.ShellButton(dialog, "OK", dialog.destroy, self.provider.roles(), variant="primary")
        knopf.pack(padx=20, pady=20)
        window_lifetime.scope_for(dialog).after(50, knopf.invoke)
        modal_session.run_modal(self.root, dialog)
        pump(self.root)
        return not dialog.winfo_exists()

    def theme_probe(self):
        hell = self.ws.cget("bg")
        self.provider.set_mode("dark")
        pump(self.root)
        dunkel = self.ws.cget("bg")
        self.provider.set_mode("light")
        pump(self.root)
        return hell != dunkel and self.ws.cget("bg") == hell

    def beenden(self):
        root = self.root
        fehler = self.host.shutdown()
        assert not fehler, fehler
        assert not root.winfo_exists() if _alive(root) else True
        return True


def _alive(root):
    try:
        return bool(root.winfo_exists())
    except tk.TclError:
        return False


# --- Host A: Notizen (Text und Listen) ------------------------------------------------------------------------
def host_a(h):
    notizen = ["Einkauf planen", "Probe vorbereiten", "Buch lesen", "Plan prüfen"]

    def liste(master, ws_host):
        rahmen = tk.Frame(master, bg=h.provider.roles()["bg"])
        box = tk.Listbox(rahmen, height=6)
        def filtern(text):
            box.delete(0, "end")
            for n in notizen:
                if text.lower() in n.lower():
                    box.insert("end", n)
            ws_host.set_status(f"{box.size()} Treffer")
        rahmen.suche = controls.SearchField(rahmen, h.provider.roles(), placeholder="Notizen suchen", on_change=filtern, delay_ms=1)
        rahmen.suche.pack(fill="x", padx=8, pady=8)
        box.pack(fill="both", expand=True, padx=8)
        rahmen.box = box
        filtern("")
        rahmen.on_close = lambda: h.events.append(("close", "liste"))
        return rahmen

    def text(master, _ws):
        rahmen = tk.Frame(master)
        feld = tk.Text(rahmen, height=8)
        feld.insert("1.0", "Freier Text")
        feld.pack(fill="both", expand=True)
        rahmen.feld = feld
        return rahmen
    return [workspaces.Workspace("liste", "Liste", liste, group="Notizen", shortcut="1"),
            workspaces.Workspace("text", "Text", text, group="Notizen", shortcut="2", keep_alive=False)]


# --- Host B: Zeichenfläche (Canvas und Werkzeugleiste) -----------------------------------------------------------
def host_b(h):
    def flaeche(master, _ws):
        rahmen = tk.Frame(master)
        rahmen.leiste = controls.Toolbar(rahmen, h.provider.roles())
        rahmen.leiste.pack(fill="x")
        canvas = tk.Canvas(rahmen, bg=h.provider.roles()["card"], highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        rahmen.canvas = canvas
        formen = rahmen.leiste.add_group("Formen")
        for name, zeichnen in (("Kreis", lambda: canvas.create_oval(10, 10, 60, 60, tags="form")),
                               ("Rechteck", lambda: canvas.create_rectangle(80, 10, 140, 60, tags="form")),
                               ("Linie", lambda: canvas.create_line(10, 90, 200, 90, tags="form"))):
            formen.add_button(name, zeichnen, size="small")
        rahmen.leiste.add_group("Bearbeiten").add_button("Leeren", lambda: canvas.delete("form"), size="small", variant="danger")
        ansicht = rahmen.leiste.add_group("Ansicht")
        for name in ("Raster", "Zoom +", "Zoom −", "Anpassen"):
            ansicht.add_button(name, lambda: None, size="small")
        return rahmen
    return [workspaces.Workspace("flaeche", "Zeichenfläche", flaeche, shortcut="1",
                                 actions=(("Exportieren", lambda: h.events.append(("action", "export"))),)),
            workspaces.Workspace("ebenen", "Ebenen", lambda m, _w: tk.Label(m, text="Ebenen"), shortcut="2")]


# --- Host C: Übersicht (Bento, Tabelle, Detail) ---------------------------------------------------------------------
def host_c(h):
    zeilen = [("A-1", "offen", 3), ("A-2", "fertig", 5), ("B-1", "offen", 8)]

    def karten(master, _ws):
        ctx = b.BentoContext.for_host(theme_provider=h.provider.roles)
        grid = b.BentoGrid(master, context=ctx)
        for spec in (b.BentoCardSpec("summe", span=2, weight=3), b.BentoCardSpec("offen"), b.BentoCardSpec("fertig")):
            karte = b.BentoCard(grid, context=ctx, title=spec.key, spec=spec)
            b.BentoEmptyState(karte.body, context=ctx, title=spec.key, description="künstlich").pack(fill="x")
            grid.add_card(karte)
        grid.set_theme = lambda roles: (ctx.refresh_from_host(), grid.update_theme(ctx))
        return grid

    def tabelle(master, ws_host):
        rahmen = tk.Frame(master)
        baum = ttk.Treeview(rahmen, columns=("status", "wert"), show="headings", height=5)
        for spalte in ("status", "wert"):
            baum.heading(spalte, text=spalte)
        for kennung, status, wert in zeilen:
            baum.insert("", "end", iid=kennung, values=(status, wert))
        detail = tk.Label(rahmen, text="—", anchor="w")
        baum.bind("<<TreeviewSelect>>", lambda _e: (detail.configure(text=f"Detail {baum.selection()[0]}"),
                                                    ws_host.set_status(f"Auswahl {baum.selection()[0]}")))
        baum.pack(fill="x")
        detail.pack(fill="x")
        rahmen.baum, rahmen.detail = baum, detail
        return rahmen
    return [workspaces.Workspace("karten", "Karten", karten, group="Übersicht", shortcut="1"),
            workspaces.Workspace("tabelle", "Tabelle", tabelle, group="Daten", shortcut="2")]


def pruefen_a():
    h = Host("Notizen", "#7B2CBF", host_a, [settings_registry.Setting("notes.sort", "choice", "titel", "notes", "Sortierung",
                                                                          choices=("titel", "datum"))]).start()
    liste = h.ws.view("liste")
    liste.suche.set("pl")
    liste.suche.flush()
    pump(h.root)
    assert liste.box.size() == 2 and "2 Treffer" in h.ws.status.cget("text"), liste.box.size()
    h.root.event_generate("<Control-2>")
    pump(h.root)
    assert h.ws.current == "text" and h.ws.view("text").feld.get("1.0", "end").strip() == "Freier Text"
    h.ws.next(1)
    pump(h.root)
    assert h.ws.current == "liste" and h.ws.view("text") is None, "keep_alive=False nicht abgebaut"
    assert h.theme_probe() and h.dialog_probe()
    return h


def pruefen_b():
    h = Host("Zeichenfläche", "#0F766E", host_b, [settings_registry.Setting("draw.grid", "bool", True, "draw", "Raster")]).start()
    flaeche = h.ws.view("flaeche")
    for gruppe in flaeche.leiste.groups[:1]:
        for knopf in gruppe.buttons:
            knopf.invoke()
    pump(h.root)
    assert len(flaeche.canvas.find_withtag("form")) == 3
    flaeche.leiste.groups[1].buttons[0].invoke()
    assert not flaeche.canvas.find_withtag("form")
    breit = flaeche.leiste.rows
    h.root.geometry("420x640")
    pump(h.root, 8)
    flaeche.leiste._relayout()
    pump(h.root)
    assert flaeche.leiste.rows > breit, (breit, flaeche.leiste.rows)
    h.ws.actionbar.winfo_children()[0].invoke()
    assert ("action", "export") in h.events
    assert h.theme_probe() and h.dialog_probe()
    return h


def pruefen_c():
    h = Host("Übersicht", "#B45309", host_c, [settings_registry.Setting("view.rows", "int", 20, "view", "Zeilen", minimum=5, maximum=200)]).start()
    grid = h.ws.view("karten")
    pump(h.root)
    grid.reflow()
    pump(h.root)
    breit = grid.current_columns
    h.root.geometry("460x640")
    pump(h.root, 8)
    grid.reflow()
    pump(h.root)
    assert grid.current_columns < breit, (breit, grid.current_columns)
    h.ws.show("tabelle")
    tabelle = h.ws.view("tabelle")
    tabelle.baum.selection_set("A-2")
    pump(h.root)
    assert tabelle.detail.cget("text") == "Detail A-2" and "A-2" in h.ws.status.cget("text")
    assert h.theme_probe() and h.dialog_probe()
    return h


ergebnisse = []
for name, probe in (("A", pruefen_a), ("B", pruefen_b), ("C", pruefen_c)):
    h = probe()
    root = h.root
    scope = window_lifetime.scope_for(root)
    scope.after(60000, lambda: h.events.append(("error", "Zeitgeber nach dem Beenden")))
    h.beenden()
    assert not _alive(root), f"Host {name}: Fenster nicht beendet"
    assert scope.closed and not scope.pending(), f"Host {name}: Zeitgeber nicht freigegeben"
    assert h.ws._closed and not h.ws.live_views(), f"Host {name}: Ansichten nicht abgebaut"
    assert not [e for e in h.events if e[0] == "error"], h.events
    ergebnisse.append(f"{name}: {len(h.registry)} Bereiche, {sum(1 for e in h.events if e[0] == 'show')} Wechsel")
assert not any(m in sys.modules for m in VERBOTEN)
print("Referenzhosts OK – " + "; ".join(ergebnisse) +
      " – Start, Navigation, Kürzel, Theme hell/dunkel/Marke, Dialog, Einstellungen, Eingabe, Canvas, "
      "responsive Leiste und Bento-Spalten, Tabelle/Detail, Abbau ohne Fehler")
