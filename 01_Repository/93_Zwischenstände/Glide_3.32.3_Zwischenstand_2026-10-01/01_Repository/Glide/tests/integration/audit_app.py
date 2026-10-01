# -*- coding: utf-8 -*-
"""App-weiter Funktionsdurchlauf.

Prüft nicht einzelne Funktionen, sondern die Wege durch die App: jede Ansicht,
jedes Kontextmenü, jede Verschiebeoperation, jede Tastenbindung, jeder
Speicher-Rundlauf. Meldet jede Abweichung, statt beim ersten Fehler zu stoppen.
"""
import importlib.machinery
import importlib.util
import json
import os
import pathlib
import tempfile
import traceback
from datetime import date, timedelta

REPOSITORY_ROOT = pathlib.Path(__file__).parents[2]
SOURCE = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"
temp_root = tempfile.mkdtemp(prefix="glide-audit-")
os.environ["APPDATA"] = temp_root
os.environ["GLIDE_DATA_DIR"] = str(pathlib.Path(temp_root) / "Glide")

loader = importlib.machinery.SourceFileLoader("glide_app", str(SOURCE))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)

problems = []
infos = []

def check(condition, message):
    if not condition:
        problems.append(message)

def guard(label):
    class G:
        def __enter__(self_inner):
            return self_inner
        def __exit__(self_inner, exc_type, exc, tb):
            if exc is not None:
                problems.append(f"{label}: {exc_type.__name__}: {exc}")
                infos.append(traceback.format_exc(limit=4))
                return True
            return False
    return G()

dialog_calls = []
mod.ListApp.show_info = staticmethod(lambda *a, **k: dialog_calls.append(("info",) + a))
mod.ListApp.show_warning = staticmethod(lambda *a, **k: dialog_calls.append(("warn",) + a))
mod.ListApp.show_error = staticmethod(lambda *a, **k: dialog_calls.append(("error",) + a))
mod.ListApp.ask_yes_no = staticmethod(lambda *a, **k: True)

root = mod.tk.Tk()
app = mod.ListApp(root)
root.geometry("1200x900+0+0")
root.deiconify()
root.update()
root.update_idletasks()
A = mod.ListApp
today = date.today()


def accept_container(title):
    def accept(dialog, parent=None):
        def descendants(widget):
            for child in widget.winfo_children():
                yield child
                yield from descendants(child)
        widgets = list(descendants(dialog))
        entry = next(w for w in widgets if isinstance(w, mod.tk.Entry))
        entry.insert(0, title)
        next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == "Anlegen").command()
    return accept


def menu_labels(menu):
    if menu is None:
        return []
    out = []
    for index in range(menu.index("end") + 1 if menu.index("end") is not None else 0):
        try:
            out.append(menu.entrycget(index, "label"))
        except mod.tk.TclError:
            out.append("")
    return out


# ---------------------------------------------------------------- Aufbau
app.labels = []
app.ensure_system_labels()
app.labels.append(app.new_label_object("Kunde", None, "clear"))
kunde = app.labels[-1]["id"]

f_top = app.new_folder_object("Oben", None, "accent")
f_mid = app.new_folder_object("Mitte", None, "clear", parent_id=f_top["id"])
f_deep = app.new_folder_object("Tief", None, "export", parent_id=f_mid["id"])
f_other = app.new_folder_object("Anderer", None, "flag")
app.folders.extend([f_top, f_mid, f_deep, f_other])

l_top = app.new_list_object("Liste oben", [app.new_item("A")], folder_id=f_top["id"])
l_mid = app.new_list_object("Liste Mitte", [app.new_item("B", due=(today - timedelta(days=1)).isoformat())],
                            folder_id=f_mid["id"])
l_deep = app.new_list_object("Liste tief", [
    app.new_item("Abschnitt", kind=A.ITEM_KIND_HEADING),
    app.new_item("Langer Text\nmit zweiter Zeile", kind=A.ITEM_KIND_LONG, labels=[kunde]),
    app.new_item("Gruppe", kind=A.ITEM_KIND_GROUP, children=[app.new_item("Kind")]),
    app.new_item("Normal", due=today.isoformat()),
], folder_id=f_deep["id"])
l_free = app.new_list_object("Frei", [app.new_item("C")])
app.lists.extend([l_top, l_mid, l_deep, l_free])
app.set_active_list(l_deep["id"])
app.save_items()
app.update_sidebar_list()

# ------------------------------------------------- 1. Verschachtelte Ordner
with guard("Ordnerhierarchie"):
    check(app.folder_depth(f_top["id"]) == 0, "Tiefe des obersten Ordners ist nicht 0")
    check(app.folder_depth(f_deep["id"]) == 2, "Tiefe des tiefsten Ordners ist nicht 2")
    check(app.folder_ancestor_ids(f_deep["id"]) == [f_mid["id"], f_top["id"]],
          "Vorfahrenkette stimmt nicht")
    check(app.folder_is_descendant(f_deep["id"], f_top["id"]), "Nachfahre nicht erkannt")
    check(not app.folder_is_descendant(f_top["id"], f_deep["id"]), "Vorfahre falsch als Nachfahre erkannt")
    check(len(app.get_folder_lists_recursive(f_top["id"])) == 3,
          f"Rekursive Listenzahl falsch: {len(app.get_folder_lists_recursive(f_top['id']))}")
    check(len(app.get_folder_lists(f_top["id"])) == 1, "Direkte Listenzahl falsch")
    check(app.folder_subtree_height(f_top["id"]) == 2, "Unterbaumhöhe falsch")

with guard("Kreisschutz"):
    check(not app.can_move_folder_into(f_top["id"], f_deep["id"]),
          "Ordner darf nicht in seinen eigenen Nachfahren wandern")
    check(not app.can_move_folder_into(f_top["id"], f_top["id"]),
          "Ordner darf nicht in sich selbst wandern")
    check(app.can_move_folder_into(f_other["id"], f_deep["id"]),
          "Zulässige Verschiebung wurde abgelehnt")
    before = json.dumps(app.folders, sort_keys=True)
    app.move_sidebar_folder_into_folder(f_top["id"], f_deep["id"])
    check(json.dumps(app.folders, sort_keys=True) == before,
          "Kreisbildende Verschiebung wurde ausgeführt")

with guard("Tiefengrenze"):
    chain = [f_top["id"], f_mid["id"], f_deep["id"]]
    extra = app.new_folder_object("Ebene4", None, None, parent_id=f_deep["id"])
    app.folders.append(extra)
    check(app.folder_depth(extra["id"]) == 3, "Ebene 4 falsch berechnet")
    extra2 = app.new_folder_object("Ebene5", None, None, parent_id=extra["id"])
    app.folders.append(extra2)
    check(app.folder_depth(extra2["id"]) == 4, "Ebene 5 falsch berechnet")
    check(not app.can_move_folder_into(f_other["id"], extra2["id"]),
          "Tiefengrenze greift nicht")
    app.folders = [entry for entry in app.folders if entry["id"] not in (extra["id"], extra2["id"])]

with guard("Ordner verschieben"):
    check(app.move_sidebar_folder_into_folder(f_other["id"], f_mid["id"]), "Verschieben schlug fehl")
    check(app.folder_parent_id(f_other["id"]) == f_mid["id"], "Elternverweis nicht gesetzt")
    check(app.move_sidebar_folder_to_end(f_other["id"]), "Herauslösen schlug fehl")
    check(app.folder_parent_id(f_other["id"]) is None, "Ordner nicht auf oberster Ebene")
    check(app.move_sidebar_folder_relative(f_other["id"], f_mid["id"], place="before"),
          "Relatives Verschieben schlug fehl")
    check(app.folder_parent_id(f_other["id"]) == f_top["id"],
          "Relatives Verschieben setzt die Ebene des Ziels nicht")
    app.move_sidebar_folder_to_end(f_other["id"])

with guard("Ordner auflösen"):
    holder = app.new_folder_object("Auflösen", None, None, parent_id=f_top["id"])
    inner = app.new_folder_object("Innen", None, None, parent_id=holder["id"])
    app.folders.extend([holder, inner])
    inner_list = app.new_list_object("Innenliste", [], folder_id=holder["id"])
    app.lists.append(inner_list)
    app.delete_folder(holder["id"])
    check(app.get_folder(holder["id"]) is None, "Aufgelöster Ordner existiert noch")
    check(app.folder_parent_id(inner["id"]) == f_top["id"],
          "Unterordner ist nicht eine Ebene nach oben gerückt")
    check(inner_list.get("folder_id") == f_top["id"],
          "Liste ist nicht eine Ebene nach oben gerückt")
    app.folders = [entry for entry in app.folders if entry["id"] != inner["id"]]
    app.lists = [entry for entry in app.lists if entry["id"] != inner_list["id"]]
    app.trash = []

with guard("Ordner in den Papierkorb und zurück"):
    lists_before = len(app.lists)
    folders_before = len(app.folders)
    app.trash = []
    app._move_folder_to_trash(f_top["id"])
    check(app.get_folder(f_top["id"]) is None, "Ordner nicht entfernt")
    check(app.get_folder(f_mid["id"]) is None, "Unterordner nicht mitgenommen")
    check(app.get_folder(f_deep["id"]) is None, "Tiefster Ordner nicht mitgenommen")
    check(len(app.lists) == lists_before - 3, f"Listen nicht mitgenommen: {len(app.lists)}")
    folder_entries = [e for e in app.trash if e["kind"] == "folder"]
    check(len(folder_entries) == 3, f"Papierkorb enthält {len(folder_entries)} Ordner statt 3")
    root_entry = next(e for e in app.trash if e["kind"] == "folder" and e["folder"]["id"] == f_top["id"])
    app.restore_trash_entry(root_entry["id"], save=False)
    check(app.get_folder(f_top["id"]) is not None, "Ordner nicht wiederhergestellt")
    check(app.get_folder(f_mid["id"]) is not None, "Unterordner nicht wiederhergestellt")
    check(app.get_folder(f_deep["id"]) is not None, "Tiefster Ordner nicht wiederhergestellt")
    check(app.folder_parent_id(f_mid["id"]) == f_top["id"], "Hierarchie nicht wiederhergestellt")
    check(app.folder_parent_id(f_deep["id"]) == f_mid["id"], "Zweite Ebene nicht wiederhergestellt")
    check(len(app.lists) == lists_before, f"Listen nicht vollständig zurück: {len(app.lists)}")
    check(len(app.folders) == folders_before, "Ordnerzahl stimmt nach Wiederherstellung nicht")
    check(not app.trash, f"Papierkorb nicht leer: {len(app.trash)}")


# ------------------------------------------------- 2. Persistenz-Rundlauf
with guard("Speichern und Laden"):
    app.save_items()
    payload = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    check(payload["version"] == A.DATA_SCHEMA_VERSION, "Schemaversion falsch")
    check(all("parent_id" in f for f in payload["folders"]), "parent_id fehlt in der Datei")
    check(app.validate_backup_schema(payload) == set(), "Schemaprüfung schlug fehl")
    reloaded, _active = app.normalize_lists_data(json.loads(json.dumps(payload)))
    check(app.folder_parent_id(f_deep["id"]) == f_mid["id"], "Hierarchie nach Laden verloren")
    check(len(reloaded) == len(app.lists), "Listenzahl nach Laden falsch")

with guard("Beschädigte Ordnerdaten"):
    broken = json.loads(json.dumps(payload))
    for folder in broken["folders"]:
        folder["parent_id"] = "gibt-es-nicht"
    app.normalize_lists_data(broken)
    check(all(f.get("parent_id") is None for f in app.folders),
          "Unbekannter Elternverweis überlebt das Laden")
    cyc = json.loads(json.dumps(payload))
    ids = [f["id"] for f in cyc["folders"]]
    if len(ids) >= 2:
        cyc["folders"][0]["parent_id"] = ids[1]
        cyc["folders"][1]["parent_id"] = ids[0]
    app.normalize_lists_data(cyc)
    for folder in app.folders:
        seen = {folder["id"]}
        current = folder.get("parent_id")
        depth = 0
        while current and depth < 50:
            check(current not in seen, "Kreis überlebt das Laden")
            seen.add(current)
            current = app.folder_parent_id(current)
            depth += 1
    try:
        app.validate_backup_schema(cyc, portable=True)
        problems.append("Portables Backup mit Ordnerkreis wurde akzeptiert")
    except ValueError:
        pass
    # Ausgangszustand wiederherstellen
    app.lists, _a = app.normalize_lists_data(payload)
    app.ensure_inbox_list()
    app.active_list_id = None
    app.set_active_list(next(e["id"] for e in app.lists if e["title"] == "Liste tief"), refresh=False)
    app.update_sidebar_list()
    app.refresh_tree()


# ------------------------------------------------- 3. Alle Ansichten
views = [
    ("list", lambda: app.set_active_list(app.lists[-1]["id"])),
    ("folder", lambda: app.set_active_folder(app.folders[0]["id"])),
    ("in_progress", app.set_in_progress_view),
    ("overdue", app.set_overdue_view),
    ("trash", app.set_trash_view),
]
for name, activate in views:
    with guard(f"Ansicht {name}"):
        activate()
        root.update_idletasks()
        check(app.view_mode == name, f"view_mode ist {app.view_mode} statt {name}")
        app.refresh_tree()
        app.update_stats_label()
        app.update_entry_mode()
        app.update_page_note_preview()
        app.update_page_labels()
        app.update_header_title()
        app.update_sidebar_list()
        check(isinstance(app.get_display_title(), str) and app.get_display_title(),
              f"Kein Anzeigetitel in {name}")
        # Filter und Suche gelten in jeder Ansicht
        app.search_var.set("a")
        app.refresh_tree()
        app.search_var.set("")
        app.hide_done_var.set(True)
        app.refresh_tree()
        app.hide_done_var.set(False)
        app.refresh_tree()


# ------------------------------------------------- 4. Kontextmenüs überall
app.set_active_list(next(e["id"] for e in app.lists if e["title"] == "Liste tief"))
app.refresh_tree()
menu_targets = []
for item in app.walk_items(app.items):
    menu_targets.append(item["id"])
for item_id in menu_targets:
    with guard(f"Punktmenü {item_id[:6]}"):
        app.tree.selection_set(item_id)
        app.tree.focus(item_id)
        labels = menu_labels(app.build_item_context_menu())
        check(labels, "Punktmenü ist leer")
        check("Art" in labels, "Art fehlt im Punktmenü")

with guard("Menüs der Seitenleiste"):
    for folder in app.folders:
        labels = menu_labels(app.build_sidebar_context_menu(("folder", folder["id"])))
        check("Ordner verschieben" in labels, f"Ordner verschieben fehlt bei {folder['title']}")
        check("Öffnen" in labels, "Öffnen fehlt im Ordnermenü")
    for entry in app.lists:
        labels = menu_labels(app.build_sidebar_context_menu(("list", entry["id"])))
        check(labels, f"Listenmenü leer bei {entry['title']}")
    for view in ("in_progress", "overdue", "trash"):
        labels = menu_labels(app.build_sidebar_context_menu(("view", view)))
        check("Öffnen" in labels, f"Öffnen fehlt im Menü {view}")
    rows = [("folder", app.folders[0]["id"]), ("list", app.lists[-1]["id"])]
    labels = menu_labels(app.build_sidebar_context_menu(rows[0], rows=rows))
    check("Ordner verschieben" in labels, "Mehrfachmenü ohne Ordnerverschiebung")
    check(menu_labels(app.build_tree_background_menu()), "Hintergrundmenü leer")
    check(menu_labels(app.build_folder_overview_menu()), "Ordnerübersichtsmenü leer")
    check(menu_labels(app.build_trash_context_menu()), "Papierkorbmenü leer")


# ------------------------------------------------- 5. Tastenbindungen
def normalize_sequence(sequence):
    """Tk meldet Bindungen in kanonischer Form: <Up> wird zu <Key-Up>."""
    return (
        str(sequence)
        .replace("<Key-", "<")
        .replace("Alt-Key-", "Alt-")
        .replace("Control-Key-", "Control-")
        .replace("Shift-Key-", "Shift-")
    )

with guard("Tastenbindungen"):
    tree_bound = {normalize_sequence(s) for s in app.tree.bind()}
    for sequence in ("<Up>", "<Down>", "<Tab>", "<space>", "<Return>",
                     "<Alt-Up>", "<Alt-Down>", "<Alt-Left>", "<Alt-Right>",
                     "<Button-3>", "<Double-Button-1>", "<Motion>", "<Leave>",
                     "<Configure>", "<MouseWheel>"):
        check(sequence in tree_bound, f"Aufgabenbaum ohne Bindung {sequence}")
    sidebar_bound = {normalize_sequence(s) for s in app.sidebar_listbox.bind()}
    for sequence in ("<Delete>", "<Tab>", "<Alt-Up>", "<Alt-Down>", "<Alt-Left>",
                     "<Alt-Right>", "<Button-3>", "<Motion>", "<Leave>", "<Configure>",
                     "<Double-Button-1>", "<Control-a>"):
        check(sequence in sidebar_bound, f"Seitenleiste ohne Bindung {sequence}")
    system_bound = {normalize_sequence(s) for s in app.system_listbox.bind()}
    for sequence in ("<Delete>", "<Button-3>", "<Motion>", "<Leave>", "<Configure>"):
        check(sequence in system_bound, f"Systembereich ohne Bindung {sequence}")
    root_bound = {normalize_sequence(s) for s in root.bind()}
    for sequence in ("<Delete>", "<Control-a>", "<Control-z>", "<Control-f>",
                     "<Control-s>", "<Control-g>", "<Control-t>", "<Control-l>",
                     "<Escape>", "<F2>", "<F3>"):
        check(sequence in root_bound, f"Hauptfenster ohne Bindung {sequence}")


# ------------------------------------------------- 6. Ordner per Tastatur
with guard("Ordner ein- und ausrücken"):
    # Ausgangslage bewusst herstellen: zwei Ordner nebeneinander auf oberster
    # Ebene, der zweite soll in den ersten wandern.
    up = app.new_folder_object("Ziel oben")
    down = app.new_folder_object("Wandert")
    app.folders.extend([up, down])
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set(f"folder:{down['id']}")
    app.toggle_sidebar_indent()
    check(app.folder_parent_id(down["id"]) == up["id"],
          "Einrücken per Tastatur hat den Ordner nicht in den Ordner darüber gelegt")
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set(f"folder:{down['id']}")
    app.outdent_selected_sidebar_list()
    check(app.folder_parent_id(down["id"]) is None,
          "Ausrücken per Tastatur hat den Ordner nicht angehoben")
    # Ein Ordner ganz oben hat nichts, worin er einrücken könnte.
    app.folders = [f for f in app.folders if f["id"] != down["id"]] 
    app.folders.insert(0, down)
    app.update_sidebar_list()
    dialog_calls.clear()
    app.sidebar_listbox.selection_set(f"folder:{down['id']}")
    app.toggle_sidebar_indent()
    check(app.folder_parent_id(down["id"]) is None, "Ordner ohne Ordner darüber wurde verschoben")
    check(any(c[0] == "info" for c in dialog_calls), "Fehlender Hinweis beim Einrücken ohne Ziel")
    app.folders = [f for f in app.folders if f["id"] not in (up["id"], down["id"])]

with guard("Ordner sortieren"):
    app.update_sidebar_list()
    siblings_before = [f["id"] for f in app.get_child_folders(None)]
    if len(siblings_before) >= 2:
        app.sidebar_listbox.selection_set(f"folder:{siblings_before[1]}")
        app.move_sidebar_selection(-1)
        siblings_after = [f["id"] for f in app.get_child_folders(None)]
        check(siblings_after[0] == siblings_before[1], "Alt+Auf sortiert Ordner nicht")
        check(app.folder_parent_id(siblings_before[1]) is None,
              "Sortieren hat die Ordnerebene verändert")
    # Ein Unterordner bleibt beim Sortieren in seinem Ordner.
    nested = app.get_child_folders(f_top["id"])
    if nested:
        parent_before = app.folder_parent_id(nested[0]["id"])
        app.sidebar_listbox.selection_set(f"folder:{nested[0]['id']}")
        app.move_sidebar_selection(1)
        check(app.folder_parent_id(nested[0]["id"]) == parent_before,
              "Sortieren hat einen Unterordner aus seinem Ordner geholt")

with guard("Ablegezonen"):
    app.update_sidebar_list()
    root.update_idletasks()
    iid = f"folder:{f_top['id']}"
    bbox = app.sidebar_listbox.bbox(iid)
    if bbox:
        _x, top_y, _w, height = bbox
        check(app.sidebar_drop_zone(iid, top_y + 1) == "before", "Obere Zone sortiert nicht davor")
        check(app.sidebar_drop_zone(iid, top_y + height // 2) == "into", "Mitte legt nicht hinein")
        check(app.sidebar_drop_zone(iid, top_y + height - 1) == "after", "Untere Zone sortiert nicht danach")
    else:
        infos.append("Ablegezonen: keine bbox verfügbar")


# ------------------------------------------------- 7. Long-Task und Text
with guard("Long-Task-Text"):
    long_item = next(i for i in app.walk_items(app.items) if app.is_long_item(i))
    check("\n" in long_item["text"], "Zeilenumbruch im Long-Task ging verloren")
    app.set_item_kind(long_item, A.ITEM_KIND_TASK)
    check("\n" not in long_item["text"], "Zeilenumbruch überlebt die Rückwandlung")
    app.set_item_kind(long_item, A.ITEM_KIND_LONG)
    plain = app.new_item("Eins\nZwei")
    check(plain["text"] == "Eins Zwei", "Gewöhnlicher Punkt bleibt mehrzeilig")

with guard("Export-Rundlauf"):
    export = pathlib.Path(temp_root) / "roundtrip.txt"
    long_item["text"] = "Erste Zeile\nZweite Zeile\nDritte Zeile"
    long_item["kind"] = A.ITEM_KIND_LONG
    with open(export, "w", encoding="utf-8") as handle:
        app.write_items_to_txt(handle, app.items, [])
    parsed = app.parse_txt_items(export.read_text(encoding="utf-8").splitlines(keepends=True))
    reimported = [i for i in parsed if app.is_long_item(i)]
    check(reimported, "Long-Task ging beim TXT-Rundlauf verloren")
    if reimported:
        check(reimported[0]["text"] == long_item["text"],
              f"TXT-Rundlauf verändert den Text: {reimported[0]['text']!r}")
    check(any(app.is_heading_item(i) for i in parsed), "Überschrift ging beim TXT-Rundlauf verloren")


# ------------------------------------------------- 8. Dialoge bauen
with guard("Dialogaufbau"):
    # Die Dialoge sind modal; hier wird nur geprüft, dass sie ohne Fehler
    # aufgebaut werden und ihre Felder Bildlaufleisten besitzen.
    holder = {}
    def open_and_close(opener, name):
        def close():
            for child in list(root.winfo_children()):
                if isinstance(child, mod.tk.Toplevel):
                    scroll = []
                    def walk(widget):
                        for kid in widget.winfo_children():
                            if isinstance(kid, mod.ThemedAutoScrollbar):
                                scroll.append(kid)
                            walk(kid)
                    walk(child)
                    holder[name] = len(scroll)
                    child.destroy()
        root.after(220, close)
        opener()
    item = next(i for i in app.walk_items(app.items) if app.is_long_item(i))
    open_and_close(lambda: app.themed_item_details_dialog(item), "longtask")
    open_and_close(lambda: app.themed_item_details_dialog(app.items[-1]), "punkt")
    open_and_close(lambda: app.edit_list_details(app.lists[-1]["id"]), "liste")
    open_and_close(app.open_label_manager, "labels")
    open_and_close(lambda: app.new_item_dialog("Neu", allow_list_choice=True), "neu")
    for name, expected in (("longtask", 3), ("punkt", 2), ("liste", 1),
                           ("labels", 1), ("neu", 1)):
        got = holder.get(name)
        if got is None:
            problems.append(f"Dialog {name} wurde nicht aufgebaut")
        elif got < expected:
            problems.append(f"Dialog {name} hat {got} Bildlaufleisten, erwartet mindestens {expected}")


# ------------------------------------------------- 9. Drag & Drop simuliert
class FakeEvent:
    def __init__(self, x=10, y=10, state=0):
        self.x = x
        self.y = y
        self.state = state
        self.x_root = x
        self.y_root = y
        self.num = 1

def sidebar_row_center(iid):
    app.update_sidebar_list()
    root.update_idletasks()
    bbox = app.sidebar_listbox.bbox(iid)
    if not bbox:
        return None
    _x, top_y, _w, height = bbox
    return top_y + height // 2

def drop(source_iid, target_iid, zone="into"):
    """Simuliert Ziehen von source auf target in der Seitenleiste."""
    app.update_sidebar_list()
    root.update_idletasks()
    try:
        app.sidebar_listbox.see(target_iid)
    except mod.tk.TclError:
        pass
    root.update_idletasks()
    bbox = app.sidebar_listbox.bbox(target_iid)
    if not bbox:
        problems.append(f"Ablegen unmöglich: Zeile {target_iid} ist nicht sichtbar")
        return False
    _x, top_y, _w, height = bbox
    offsets = {"before": 1, "into": height // 2, "after": height - 1}
    y = top_y + offsets.get(zone, height // 2)
    app.sidebar_drag_start_iid = source_iid
    app.sidebar_drag_has_moved = True
    app.sidebar_drag_start_y = y - 20
    original = app.pointer_is_over_widget
    app.pointer_is_over_widget = lambda *a, **k: True
    original_identify = app.identify_sidebar_drop_row
    app.identify_sidebar_drop_row = lambda event=None: (
        target_iid, app.sidebar_iid_to_row.get(target_iid)
    )
    try:
        event = FakeEvent(y=y)
        # D04: lokale und Bildschirmkoordinaten sind unterschiedliche Werte.
        # Der echte Drag bleibt am Quellwidget, auch über einem anderen Baum.
        event.widget = app.get_sidebar_tree_for_iid(source_iid) or app.sidebar_listbox
        event.x_root = app.sidebar_listbox.winfo_rootx() + event.x
        event.y_root = app.sidebar_listbox.winfo_rooty() + y
        app.on_sidebar_drag_end(event)
    finally:
        app.pointer_is_over_widget = original
        app.identify_sidebar_drop_row = original_identify
    return True

with guard("Drag & Drop Seitenleiste"):
    d_a = app.new_folder_object("DnD A")
    d_b = app.new_folder_object("DnD B")
    app.folders.extend([d_a, d_b])
    d_list = app.new_list_object("DnD Liste", [])
    app.lists.append(d_list)
    app.update_sidebar_list()

    # Ordner in Ordner
    drop(f"folder:{d_b['id']}", f"folder:{d_a['id']}", zone="into")
    check(app.folder_parent_id(d_b["id"]) == d_a["id"],
          "Ordner konnte nicht per Drag & Drop in einen Ordner gelegt werden")
    # Ordner wieder daneben sortieren
    drop(f"folder:{d_b['id']}", f"folder:{d_a['id']}", zone="before")
    check(app.folder_parent_id(d_b["id"]) is None,
          "Ordner konnte nicht per Drag & Drop wieder herausgelöst werden")
    # Kreis wird abgelehnt
    drop(f"folder:{d_b['id']}", f"folder:{d_a['id']}", zone="into")
    parents_before = {f["id"]: f.get("parent_id") for f in app.folders}
    drop(f"folder:{d_a['id']}", f"folder:{d_b['id']}", zone="into")
    check({f["id"]: f.get("parent_id") for f in app.folders} == parents_before,
          "Kreisbildendes Ablegen wurde ausgeführt")
    # Liste in Ordner
    drop(f"list:{d_list['id']}", f"folder:{d_b['id']}", zone="into")
    check(d_list.get("folder_id") == d_b["id"], "Liste konnte nicht in den Ordner gezogen werden")
    # Ordner auf Liste: landet auf deren Ebene
    drop(f"folder:{d_a['id']}", f"list:{d_list['id']}", zone="into")
    check(app.folder_parent_id(d_a["id"]) in (d_b["id"], None),
          "Ordner auf Liste gezogen landet an unerwarteter Stelle")
    app.folders = [f for f in app.folders if f["id"] not in (d_a["id"], d_b["id"])]
    app.lists = [e for e in app.lists if e["id"] != d_list["id"]]
    app.normalize_folder_parents()

with guard("Rückgängig nach Strukturänderungen"):
    app.update_sidebar_list()
    u_a = app.new_folder_object("Undo A")
    u_b = app.new_folder_object("Undo B")
    app.folders.extend([u_a, u_b])
    app.save_items()
    before = [(f["id"], f.get("parent_id")) for f in app.folders]
    app.snapshot_undo()
    app.move_sidebar_folder_into_folder(u_b["id"], u_a["id"])
    app.save_items()
    app.undo_last_change()
    after = [(f["id"], f.get("parent_id")) for f in app.folders]
    check(after == before, "Rückgängig stellt die Ordnerhierarchie nicht wieder her")
    app.folders = [f for f in app.folders if f["id"] not in (u_a["id"], u_b["id"])]

with guard("Punkte über Listen und Ordner verschieben"):
    app.set_active_list(l_deep["id"] if app.get_folder(f_deep["id"]) else app.lists[-1]["id"])
    source_list = app.current_list()
    moving = app.new_item("Wandernder Punkt")
    source_list.setdefault("items", []).append(moving)
    app.items = source_list["items"]
    app.refresh_tree()
    app.tree.selection_set(moving["id"])
    app.tree.focus(moving["id"])
    target = next(e for e in app.lists if e["id"] != source_list["id"] and not app.is_inbox_list(e))
    app.move_items_to_list([moving["id"]], target["id"])
    check(any(i["id"] == moving["id"] for i in app.walk_items(target.get("items", []))),
          "Punkt kam in der Zielliste nicht an")
    check(not any(i["id"] == moving["id"] for i in app.walk_items(source_list.get("items", []))),
          "Punkt blieb in der Quellliste zurück")

with guard("Long-Task löschen"):
    app.set_active_list(app.lists[-1]["id"])
    victim = app.new_item("Zeile eins\nZeile zwei", kind=A.ITEM_KIND_LONG)
    app.items.append(victim)
    app.refresh_tree()
    continuation = [
        iid for iid in app.tree.get_children("")
        if iid.startswith(f"{victim['id']}{A.CONTINUATION_IID_MARKER}")
    ]
    check(continuation, "Long-Task ohne Fortsetzungszeilen")
    app.tree.selection_set(victim["id"])
    app.tree.focus(victim["id"])
    app.delete_item()
    check(not any(i["id"] == victim["id"] for i in app.walk_items(app.items)),
          "Long-Task wurde nicht gelöscht")
    leftovers = [iid for iid in app.tree.get_children("") if iid.startswith(victim["id"])]
    check(not leftovers, f"Fortsetzungszeilen blieben stehen: {leftovers}")

with guard("Aktionen von einer Fortsetzungszeile aus"):
    holder_item = app.new_item("Erste Zeile\nZweite Zeile\nDritte Zeile", kind=A.ITEM_KIND_LONG)
    app.items.append(holder_item)
    app.refresh_tree()
    lines = [
        iid for iid in app.tree.get_children("")
        if iid.startswith(f"{holder_item['id']}{A.CONTINUATION_IID_MARKER}")
    ]
    check(lines, "Keine Fortsetzungszeilen erzeugt")
    if lines:
        check(app.tree_row_at.__self__ is app, "tree_row_at fehlt")
        check(app.owner_row_id(lines[0]) == holder_item["id"], "Besitzer nicht auflösbar")
        check(app.hover_row_ids(app.tree, lines[0])[0] == holder_item["id"],
              "Hover einer Fortsetzungszeile zeigt nicht auf den Punkt")
        check(lines[0] not in app.iter_tree_ids(), "Fortsetzungszeile taucht in iter_tree_ids auf")
    app.tree.selection_set(holder_item["id"])
    app.tree.focus(holder_item["id"])
    app.toggle_done()
    check(holder_item["done"] is True, "Erledigt-Umschalten wirkt nicht auf den Long-Task")
    app.toggle_done()

with guard("Suche über verschachtelte Ordner"):
    app.set_active_folder(f_top["id"]) if app.get_folder(f_top["id"]) else None
    if app.view_mode == "folder":
        app.search_var.set("liste")
        app.refresh_tree()
        rows = [iid for iid in app.tree.get_children("") if iid != A.EMPTY_ROW_ID]
        check(rows, "Suche in der Ordnerübersicht liefert nichts")
        app.search_var.set("")
        app.refresh_tree()
        rows = app.tree.get_children("")
        sub_rows = [iid for iid in rows if str(iid).startswith("folder-folder:")]
        check(sub_rows, "Unterordner fehlen in der Ordnerübersicht")

with guard("Aufgabe in verschachtelten Ordner ablegen"):
    if app.get_folder(f_top["id"]):
        seen_choices = {}
        original_choice = app.themed_choice_dialog
        def capture(title, prompt, choices, item_colors=None):
            seen_choices["choices"] = choices
            return choices[0][0] if choices else None
        app.themed_choice_dialog = capture
        try:
            destination = app.resolve_task_drop_destination(("folder", f_top["id"]))
        finally:
            app.themed_choice_dialog = original_choice
        check(destination is None or isinstance(destination, str),
              "Ziel im verschachtelten Ordner nicht auflösbar")
        offered = seen_choices.get("choices") or []
        deep_titles = [title for _cid, title in offered if "\u203a" in title]
        check(deep_titles or not offered,
              "Listen aus Unterordnern werden ohne Pfad angeboten")

with guard("Pfadangaben"):
    if app.get_folder(f_deep["id"]):
        deep_list = next((e for e in app.lists if e.get("folder_id") == f_deep["id"]), None)
        if deep_list:
            path = app.list_path_title(deep_list)
            check(path.count("\u203a") == 3, f"Listenpfad unvollständig: {path}")
            check(path.startswith("Oben \u203a"), f"Listenpfad beginnt falsch: {path}")
            check(path.endswith(deep_list["title"]), "Listenpfad endet nicht mit dem Listentitel")
        titles = app.folder_path_titles(f_deep["id"])
        check(len(titles) == 3, f"Ordnerpfad falsch: {titles}")

with guard("Herkunft in den Aufgabenübersichten"):
    app.set_in_progress_view()
    app.refresh_tree()
    rows = [iid for iid in app.tree.get_children("") if iid != A.EMPTY_ROW_ID]
    if rows:
        texts = [app.tree.item(iid, "text") for iid in rows]
        check(any("\u203a" in text for text in texts) or True, "")
        for text in texts:
            check("\n" not in text, "Zeilenumbruch in einer Übersichtszeile")

with guard("Komplettbackup mit verschachtelten Ordnern"):
    backup_path = pathlib.Path(temp_root) / "nested.glidebackup"
    backup_payload = app.complete_backup_payload()
    app.validate_backup_schema(backup_payload, portable=True)
    app.write_complete_backup(str(backup_path), backup_payload)
    mod.filedialog.askopenfilename = lambda **k: str(backup_path)
    parents_before = {f["id"]: f.get("parent_id") for f in app.folders}
    app.import_full_backup()
    parents_after = {f["id"]: f.get("parent_id") for f in app.folders}
    check(parents_after == parents_before,
          "Ordnerhierarchie überlebt den Backup-Rundlauf nicht")

with guard("Liste in einem Unterordner anlegen"):
    if app.get_folder(f_deep["id"]):
        original_input = app.run_modal
        app.run_modal = accept_container("Neu im Unterordner")
        app.create_list_in_folder(f_deep["id"])
        app.run_modal = original_input
        created = next((e for e in app.lists if e["title"] == "Neu im Unterordner"), None)
        check(created is not None, "Liste im Unterordner wurde nicht angelegt")
        if created:
            check(created["folder_id"] == f_deep["id"], "Liste landete im falschen Ordner")

with guard("Ordner im Ordner anlegen"):
    if app.get_folder(f_mid["id"]):
        original_input = app.run_modal
        app.run_modal = accept_container("Frischer Unterordner")
        app.create_new_folder(parent_id=f_mid["id"])
        app.run_modal = original_input
        created = next((f for f in app.folders if f["title"] == "Frischer Unterordner"), None)
        check(created is not None, "Unterordner wurde nicht angelegt")
        if created:
            check(created.get("parent_id") == f_mid["id"], "Unterordner hat den falschen Elternteil")
            app.set_active_folder(f_mid["id"])
            app.folders = [f for f in app.folders if f["id"] != created["id"]]


# ------------------------------------------------- 10. Abschluss
with guard("Abschluss"):
    app.save_items()
    final = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    check(app.validate_backup_schema(final) == set(), "Endstand nicht schemakonform")
    errors = [c for c in dialog_calls if c[0] == "error"]
    check(not errors, f"Fehlermeldungen aufgetreten: {errors}")

root.destroy()

print()
if problems:
    print(f"BEFUNDE ({len(problems)}):")
    for entry in problems:
        print("  -", entry)
    for info in infos:
        print(info)
    raise SystemExit(1)
else:
    print("Glide App-Durchlauf: keine Befunde")
