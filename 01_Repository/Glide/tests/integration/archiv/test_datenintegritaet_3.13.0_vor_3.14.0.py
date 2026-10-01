# -*- coding: utf-8 -*-
"""Datenintegritaet: Umbauaktionen duerfen keinen Punkt verlieren.

Der Schwerpunkt liegt auf der Gruppenfunktion, weil dort ein Datenverlust
gemeldet wurde. Geprueft werden drei Ebenen:

1. Der Bestandswaechter greift und stellt den vorherigen Stand her.
2. Gruppieren und Aufloesen erhalten jeden Punkt in jeder Konstellation.
3. Der Baum zeigt danach genau das, was in den Daten steht.

Der Test isoliert den Datenordner ueber GLIDE_DATA_DIR und fasst echte
Nutzerdaten nie an.
"""
import importlib.machinery
import importlib.util
import itertools
import os
import pathlib
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve()
SOURCE = HERE.parents[2] / "src" / "glide" / "app.pyw"

temp_root = tempfile.mkdtemp(prefix="glide-integritaet-")
os.environ["APPDATA"] = temp_root
os.environ["GLIDE_DATA_DIR"] = str(pathlib.Path(temp_root) / "Glide")

loader = importlib.machinery.SourceFileLoader("glide_app", str(SOURCE))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)

dialogs = []
mod.ListApp.show_info = staticmethod(lambda *a, **k: dialogs.append(("info",) + a[:1]))
mod.ListApp.show_warning = staticmethod(lambda *a, **k: dialogs.append(("warn",) + a[:1]))
mod.ListApp.show_error = staticmethod(lambda *a, **k: dialogs.append(("error",) + a[:1]))
mod.ListApp.ask_yes_no = staticmethod(lambda *a, **k: dialogs.append(("ask",) + a[:1]) or True)

root = mod.tk.Tk()
app = mod.ListApp(root)
root.geometry("1200x900+0+0")
root.update_idletasks()
# Windows verarbeitet das native Mapping erst in der Ereignisschleife.
# Die folgenden Mauskoordinaten brauchen einen tatsächlich sichtbaren Baum.
root.update()
app.themed_input_dialog = lambda *a, **k: "Gruppe"


# --------------------------------------------------------------- Hilfsmittel
def texts(items):
    """Alle Punkttexte in Baumreihenfolge – der Wahrheitsbeweis."""
    out = []
    for item in items:
        out.append(item["text"])
        out.extend(texts(item.get("children", [])))
    return out


def tree_ids():
    """Jede echte Zeile im Baum, auch in zugeklappten Zweigen."""
    out = set()
    stack = list(app.tree.get_children(""))
    while stack:
        row = stack.pop()
        stack.extend(app.tree.get_children(row))
        if row == app.EMPTY_ROW_ID or app.is_synthetic_row(row):
            continue
        out.add(row)
    return out


def visible_ids():
    """Zeilen, die der Nutzer ohne Klick auf einen Klapppfeil sieht."""
    out = []

    def walk(parent):
        for row in app.tree.get_children(parent):
            if row == app.EMPTY_ROW_ID or app.is_synthetic_row(row):
                continue
            out.append(row)
            if app.tree.item(row, "open"):
                walk(row)

    walk("")
    return out


def setup(spec):
    """Baut eine Liste aus einer kurzen Beschreibung auf.

    spec: Folge von (Text, Art, [Unterpunkte]).
    """
    app.items.clear()
    app.trash.clear()
    app.undo_stack.clear()
    app.expanded_ids = set()
    app.collapsed_item_ids = set()

    def build(entries):
        built = []
        for text, kind, children in entries:
            item = app.new_item(text, False, kind=kind)
            if children:
                item["children"] = build(children)
            built.append(item)
        return built

    app.items.extend(build(spec))
    app.refresh_tree()
    return [item["id"] for item in app.items]


def leaf(text, kind="task"):
    return (text, kind, [])


failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


# ------------------------------------------------- 1 Der Bestandswaechter
# Eine absichtlich fehlerhafte Aktion muss zurueckgerollt und gemeldet werden.
setup([leaf("A"), leaf("B"), leaf("C")])
before = texts(app.items)
dialogs.clear()
with app.guarded_structural_change("Testaktion"):
    app.snapshot_undo()
    app.items.pop(1)          # verliert absichtlich einen Punkt
    app.save_items()
check(texts(app.items) == before, f"Waechter hat nicht zurueckgerollt: {texts(app.items)}")
check(any(kind == "error" for kind, *_ in dialogs), "Waechter hat den Verlust nicht gemeldet")

# Eine Aktion, die nur umsortiert, darf der Waechter nicht anfassen.
dialogs.clear()
with app.guarded_structural_change("Testaktion"):
    app.snapshot_undo()
    app.items.append(app.items.pop(0))
    app.save_items()
check(texts(app.items) == ["B", "C", "A"], f"Waechter hat eine gueltige Aktion zurueckgerollt: {texts(app.items)}")
check(not dialogs, "Waechter meldet bei einer gueltigen Aktion")

# DataIntegrityError bricht sauber ab, ohne die Anwendung zu stoppen.
setup([leaf("A"), leaf("B")])
dialogs.clear()
with app.guarded_structural_change("Testaktion"):
    app.snapshot_undo()
    app.items.clear()
    raise mod.DataIntegrityError("absichtlich")
check(texts(app.items) == ["A", "B"], "DataIntegrityError wurde nicht zurueckgerollt")

# Der Waechter zaehlt den Papierkorb mit: Loeschen ist kein Verlust.
setup([leaf("A"), leaf("B"), leaf("C")])
ids_before = app.data_item_ids()
app.tree.selection_set(app.items[1]["id"])
app.tree.focus(app.items[1]["id"])
app.delete_item()
check(
    ids_before <= app.data_item_ids(),
    "Ein geloeschter Punkt taucht im Papierkorb nicht mehr auf",
)


# ------------------------------- 1b Der Papierkorb nimmt auch einzelne Punkte
app.trash.clear()
setup([leaf("A"), ("B", "task", [leaf("B1"), leaf("B2")]), leaf("C")])
deleted_id = app.items[1]["id"]
app.tree.selection_set(deleted_id)
app.tree.focus(deleted_id)
app.delete_item()
check(texts(app.items) == ["A", "C"], f"Punkt wurde nicht entfernt: {texts(app.items)}")
entry = next((e for e in app.trash if e.get("kind") == app.TRASH_KIND_ITEM), None)
check(entry is not None, "Geloeschter Punkt liegt nicht im Papierkorb")
if entry:
    check(app.trash_entry_title(entry) == "B", f"Papierkorb zeigt den falschen Titel: {app.trash_entry_title(entry)}")
    check(app.collect_item_ids([app.trash_entry_payload(entry)]) >= {deleted_id},
          "Unterpunkte fehlen im Papierkorbeintrag")

    # Wiederherstellen setzt den Punkt an seinen alten Platz zurueck.
    app.restore_trash_entry(entry["id"])
    check(texts(app.items) == ["A", "B", "B1", "B2", "C"],
          f"Punkt kam nicht an seinen Platz zurueck: {texts(app.items)}")
    check(not any(e.get("kind") == app.TRASH_KIND_ITEM for e in app.trash),
          "Papierkorbeintrag blieb nach dem Wiederherstellen stehen")

# Der Papierkorb-Punkt uebersteht Speichern und Laden.
setup([leaf("A"), leaf("B")])
app.trash.clear()
app.tree.selection_set(app.items[0]["id"])
app.tree.focus(app.items[0]["id"])
app.delete_item()
app.save_items()
app.load_items()
restored_entry = next((e for e in app.trash if e.get("kind") == app.TRASH_KIND_ITEM), None)
check(restored_entry is not None, "Geloeschter Punkt uebersteht das Speichern nicht")
if restored_entry:
    check(app.trash_entry_title(restored_entry) == "A",
          f"Titel nach dem Laden falsch: {app.trash_entry_title(restored_entry)}")
    check(app.validate_backup_schema(app.complete_backup_payload(), portable=True) is not None,
          "Backup akzeptiert den Papierkorb-Punkt nicht")

# Ist die Herkunftsliste verschwunden, landet der Punkt trotzdem irgendwo.
setup([leaf("A"), leaf("B")])
app.trash.clear()
app.tree.selection_set(app.items[0]["id"])
app.tree.focus(app.items[0]["id"])
app.delete_item()
orphan = next(e for e in app.trash if e.get("kind") == app.TRASH_KIND_ITEM)
orphan["origin"]["list_id"] = "gibt-es-nicht"
orphan["origin"]["parent_item_id"] = "gibt-es-auch-nicht"
orphan["origin"]["index"] = 99
check(app.restore_trash_entry(orphan["id"]), "Punkt ohne Herkunft liess sich nicht wiederherstellen")
check("A" in texts(app.items), f"Punkt ohne Herkunft ging verloren: {texts(app.items)}")


# --------------------------------- 2 Gruppieren und Aufloesen, alle Formen
KIND_SETS = [
    [leaf("A"), leaf("B"), leaf("C"), leaf("D"), leaf("E")],
    [leaf("A"), leaf("B", "heading"), leaf("C"), leaf("D", "long"), leaf("E")],
    [leaf("A", "long"), leaf("B"), leaf("C", "heading"), leaf("D"), leaf("E", "long")],
    [
        ("A", "task", [leaf("A1"), leaf("A2")]),
        leaf("B"),
        ("C", "task", [leaf("C1")]),
        leaf("D"),
        leaf("E"),
    ],
    [
        leaf("A"),
        ("B", "heading", [leaf("B1"), leaf("B2", "long")]),
        leaf("C"),
        ("D", "task", [("D1", "task", [leaf("D1a")])]),
        leaf("E"),
    ],
]

# Jede Auswahl von zwei bis fuenf benachbarten oder verstreuten Punkten.
selections = []
for size in range(2, 6):
    selections.extend(itertools.combinations(range(5), size))

for spec_index, spec in enumerate(KIND_SETS):
    for picks in selections:
        ids = setup(spec)
        expected = sorted(texts(app.items))
        chosen = [ids[i] for i in picks]
        app.tree.selection_set(chosen)
        app.tree.focus(chosen[0])
        dialogs.clear()
        app.group_selected_items()

        after_group = sorted(t for t in texts(app.items) if t != "Gruppe")
        if after_group != expected:
            failures.append(
                f"Aufbau {spec_index}, Auswahl {picks}: Gruppieren verliert Punkte. "
                f"erwartet={expected} erhalten={after_group}"
            )
            continue

        # Alles, was in den Daten steht, muss auch im Baum stehen …
        app.refresh_tree()
        data_ids = app.collect_item_ids(app.items)
        if data_ids - tree_ids():
            failures.append(f"Aufbau {spec_index}, Auswahl {picks}: Baum unvollstaendig nach Gruppieren")
            continue
        # … und ohne Zutun sichtbar sein, nicht hinter einem Klapppfeil.
        if data_ids - set(visible_ids()):
            hidden = sorted(data_ids - set(visible_ids()))
            failures.append(
                f"Aufbau {spec_index}, Auswahl {picks}: {len(hidden)} Punkt(e) nach dem "
                "Gruppieren nur zugeklappt sichtbar"
            )
            continue

        group = next((item for item in app.items if app.is_group_item(item)), None)
        if group is None:
            failures.append(f"Aufbau {spec_index}, Auswahl {picks}: keine Gruppe entstanden")
            continue

        app.tree.selection_set(group["id"])
        app.tree.focus(group["id"])
        dialogs.clear()
        app.dissolve_selected_group()

        after_dissolve = sorted(texts(app.items))
        if after_dissolve != expected:
            failures.append(
                f"Aufbau {spec_index}, Auswahl {picks}: Aufloesen verliert Punkte. "
                f"erwartet={expected} erhalten={after_dissolve}"
            )
            continue
        if any(kind == "error" for kind, *_ in dialogs):
            failures.append(f"Aufbau {spec_index}, Auswahl {picks}: Aufloesen meldete einen Fehler")
            continue
        app.refresh_tree()
        if app.collect_item_ids(app.items) - set(visible_ids()):
            failures.append(f"Aufbau {spec_index}, Auswahl {picks}: Punkte nach dem Aufloesen unsichtbar")


# Verschachtelte Gruppen: aussen aufloesen darf die innere nicht antasten.
ids = setup([leaf("A"), leaf("B"), leaf("C"), leaf("D")])
app.tree.selection_set([ids[1], ids[2]])
app.tree.focus(ids[1])
app.group_selected_items()
inner = next(item for item in app.items if app.is_group_item(item))
app.refresh_tree()
app.tree.selection_set([app.items[0]["id"], inner["id"]])
app.tree.focus(app.items[0]["id"])
app.group_selected_items()
outer = next(item for item in app.items if app.is_group_item(item))
check(outer["id"] != inner["id"], "Aeussere Gruppe wurde nicht angelegt")
app.refresh_tree()
app.tree.selection_set(outer["id"])
app.tree.focus(outer["id"])
app.dissolve_selected_group()
check(sorted(texts(app.items)) == sorted(["A", "B", "C", "D", "Gruppe"]),
      f"Verschachtelte Gruppe: {texts(app.items)}")

# Aufloesen einer leeren Gruppe entfernt genau die Huelle.
setup([leaf("A"), leaf("B")])
app.tree.selection_set(app.items[0]["id"])
app.tree.focus(app.items[0]["id"])
app.group_selected_items()
group = next(item for item in app.items if app.is_group_item(item))
group["children"] = []
app.refresh_tree()
app.tree.selection_set(group["id"])
app.tree.focus(group["id"])
dialogs.clear()
app.dissolve_selected_group()
check(not any(app.is_group_item(item) for item in app.items), "Leere Gruppe blieb stehen")
check(not any(kind == "error" for kind, *_ in dialogs), "Leere Gruppe loeste einen Fehler aus")


# ---------------------------------------------- 3 Ziehen mit Mehrfachauswahl
class FakeEvent:
    """Ereignis mit stimmigen Fenster- und Bildschirmkoordinaten.

    Die Ablagelogik fragt x_root/y_root ab, die Trefferpruefung x/y. Beide
    muessen zusammenpassen, sonst prueft der Test etwas anderes als die App tut.
    """

    def __init__(self, x=0, y=0, state=0, widget=None):
        self.widget = widget if widget is not None else app.tree
        self.x, self.y, self.state = x, y, state
        self.x_root = self.widget.winfo_rootx() + x
        self.y_root = self.widget.winfo_rooty() + y


def center(row_id):
    app.tree.see(row_id)
    root.update_idletasks()
    bbox = app.tree.bbox(row_id)
    return (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2) if bbox else None


def drag(source_ids, target_id, shift=False, place="after"):
    """Zieht eine Auswahl auf einen Zielpunkt – wie mit der Maus."""
    app.tree.selection_set(list(source_ids))
    app.tree.focus(source_ids[0])
    start = center(source_ids[0])
    app.on_drag_start(FakeEvent(*start))
    bbox = app.tree.bbox(target_id)
    x = bbox[0] + bbox[2] // 2
    y = bbox[1] + 1 if place == "before" else bbox[1] + bbox[3] - 1
    state = 0x0001 if shift else 0
    app.on_drag_motion(FakeEvent(x, y, state))
    app.on_drag_end(FakeEvent(x, y, state))


ids = setup([leaf("A"), leaf("B"), leaf("C"), leaf("D"), leaf("E")])
drag([ids[0], ids[1]], ids[4])
check(texts(app.items) == ["C", "D", "E", "A", "B"],
      f"Ziehen bewegt nicht die ganze Auswahl: {texts(app.items)}")

# Die Reihenfolge der Auswahl bleibt auch beim Einfuegen davor erhalten.
ids = setup([leaf("A"), leaf("B"), leaf("C"), leaf("D"), leaf("E")])
drag([ids[0], ids[1]], ids[4], place="before")
check(texts(app.items) == ["C", "D", "A", "B", "E"],
      f"Ziehen vor das Ziel haelt die Reihenfolge nicht: {texts(app.items)}")

# Shift + Ziehen macht die ganze Auswahl zu Unterpunkten.
ids = setup([leaf("A"), leaf("B"), leaf("C"), leaf("D")])
drag([ids[0], ids[1]], ids[3], shift=True)
check(sorted(texts(app.items)) == ["A", "B", "C", "D"], f"Shift-Ziehen verliert Punkte: {texts(app.items)}")
check(len(app.items) == 2 and len(app.items[1].get("children", [])) == 2,
      f"Shift-Ziehen hat nicht die ganze Auswahl eingehaengt: {texts(app.items)}")

# Ein Punkt kann nicht in den eigenen Unterbereich wandern.
ids = setup([("A", "task", [leaf("A1")]), leaf("B")])
app.refresh_tree()
child_id = app.items[0]["children"][0]["id"]
before = texts(app.items)
drag([ids[0]], child_id)
check(texts(app.items) == before, f"Punkt wurde in den eigenen Unterbereich gezogen: {texts(app.items)}")


# ------------------------------------- 4 Drop auf die Seitenleiste fragt nach
second = app.new_list_object("Zweite Liste", [])
app.lists.append(second)
app.update_sidebar_list()
ids = setup([leaf("A"), leaf("B"), leaf("C")])
dialogs.clear()
moved = app.drop_items_on_list([ids[0]], second["id"])
check(moved, "Drop auf eine Liste hat nichts verschoben")
check(any(kind == "ask" for kind, *_ in dialogs), "Drop auf eine Liste fragt nicht nach")
check(texts(app.items) == ["B", "C"], f"Punkt blieb in der Quelle: {texts(app.items)}")
check("A" in texts(second.get("items", [])), "Punkt kam im Ziel nicht an")

# Abgelehnte Rueckfrage laesst alles stehen.
mod.ListApp.ask_yes_no = staticmethod(lambda *a, **k: False)
before = texts(app.items)
check(not app.drop_items_on_list([app.items[0]["id"]], second["id"]), "Ablehnung verschiebt trotzdem")
check(texts(app.items) == before, "Ablehnung hat die Liste veraendert")
mod.ListApp.ask_yes_no = staticmethod(lambda *a, **k: dialogs.append(("ask",) + a[:1]) or True)


# --------------------------------- 5 Strg+Klick bleibt der Mehrfachauswahl
for widget_name in ("tree", "sidebar_listbox", "system_listbox"):
    widget = getattr(app, widget_name)
    bound = set(str(seq) for seq in widget.bind())
    has_ctrl_click = any("Control" in seq and "Button-1" in seq for seq in bound)
    if mod.IS_MACOS:
        check(has_ctrl_click, f"{widget_name}: macOS braucht Strg+Klick fuer das Kontextmenue")
    else:
        check(not has_ctrl_click,
              f"{widget_name}: Strg+Klick ist noch belegt und blockiert die Mehrfachauswahl")

# Der Zusatz fuer die Mehrfachauswahl passt zur Plattform.
check(app.selection_modifier_pressed(FakeEvent(state=0x0008 if mod.IS_MACOS else 0x0004)),
      "Zusatztaste fuer die Mehrfachauswahl wird nicht erkannt")
check(not app.selection_modifier_pressed(FakeEvent(state=0x0001)),
      "Shift wird faelschlich als Mehrfachauswahl gewertet")

# Strg+Klick waehlt tatsaechlich hinzu und wieder ab.
ids = setup([leaf("A"), leaf("B"), leaf("C")])
modifier = 0x0008 if mod.IS_MACOS else 0x0004
app.tree.selection_set(ids[0])
app.tree.focus(ids[0])
second_center = center(ids[1])
app.on_drag_start(FakeEvent(second_center[0], second_center[1], modifier))
check(set(app.tree.selection()) == {ids[0], ids[1]},
      f"Strg+Klick erweitert die Auswahl nicht: {app.tree.selection()}")
app.on_drag_start(FakeEvent(second_center[0], second_center[1], modifier))
check(set(app.tree.selection()) == {ids[0]},
      f"Strg+Klick hebt die Auswahl nicht wieder auf: {app.tree.selection()}")


# ------------------------------- 6 Eine Maske fuer Anlegen und Bearbeiten
# Beide Wege muessen dieselben Felder anbieten. Geprueft wird das an der
# Rueckgabe, nicht am Aussehen: Wer ein Feld vergisst, faellt hier auf.
FORM_KEYS = {
    "text", "kind", "importance", "color", "due", "due_time", "repeat",
    "labels", "description", "attachments", "list_id", "reminder",
}


def open_form(opener, fill):
    """Oeffnet ein Formular, fuellt es ueber einen Rueckruf und schliesst ab."""
    captured = {}

    def work():
        for child in list(root.winfo_children()):
            if isinstance(child, mod.tk.Toplevel):
                captured["dialog"] = child
                fill(child)
                return

    root.after(200, work)
    return opener(), captured


def find_widgets(widget, cls, out=None):
    out = [] if out is None else out
    for child in widget.winfo_children():
        if isinstance(child, cls):
            out.append(child)
        find_widgets(child, cls, out)
    return out


def fill_and_submit(dialog, title_text, date_text=None, time_text=None):
    entries = find_widgets(dialog, mod.tk.Entry)
    texts = find_widgets(dialog, mod.tk.Text)
    if entries:
        entries[0].delete(0, mod.tk.END)
        entries[0].insert(0, title_text)
    elif texts:
        texts[0].delete("1.0", mod.tk.END)
        texts[0].insert("1.0", title_text)
    due = find_widgets(dialog, mod.DueField)
    if due and date_text is not None:
        due[0].date_entry.delete(0, mod.tk.END)
        due[0].date_entry.insert(0, date_text)
    if due and time_text is not None:
        due[0].time_entry.delete(0, mod.tk.END)
        due[0].time_entry.insert(0, time_text)
    buttons = [b for b in find_widgets(dialog, mod.RoundedButton) if b.text in ("Anlegen", "Speichern")]
    check(bool(buttons), "Formular hat keine Bestaetigungsschaltflaeche")
    if buttons:
        buttons[0].command()


setup([leaf("A")])
created, _ = open_form(
    lambda: app.new_item_dialog("Neuer Punkt", allow_list_choice=True),
    lambda dlg: fill_and_submit(dlg, "Angelegt mit allem", "24.12.2026", "18:00"),
)
check(isinstance(created, dict), "Anlage-Maske lieferte nichts zurueck")
if isinstance(created, dict):
    check(set(created) == FORM_KEYS, f"Anlage-Maske: Felder weichen ab: {sorted(set(created) ^ FORM_KEYS)}")
    check(created["text"] == "Angelegt mit allem", created["text"])
    check(created["due"] == "2026-12-24", created["due"])
    check(created["due_time"] == "18:00", created["due_time"])
    check(created["repeat"] is None, f"Ohne Auswahl darf keine Wiederholung entstehen: {created['repeat']}")
    built = app.build_item_from_dialog(created)
    check(built["due"] == "2026-12-24" and built["due_time"] == "18:00",
          f"Uhrzeit kam nicht am Punkt an: {built.get('due')} {built.get('due_time')}")
    check(built["repeat"] is None, "Wiederholung ohne Auswahl kam am Punkt an")

# Wiederholungen: Rechenregel, Vorruecken beim Abhaken und Ende der Reihe.
from datetime import date as _date

_wdh = app.normalize_repeat({"art": "tage", "abstand": 3}, default_start="2026-03-01")
check(_wdh == {"art": "tage", "abstand": 3, "start": "2026-03-01", "ende": None}, str(_wdh))
check(app.normalize_repeat({"art": "tage", "abstand": 0}) is None, "Abstand 0 muss verworfen werden")
check(app.normalize_repeat({"art": "wochentage", "tage": []}) is None, "Leere Wochentage muessen verworfen werden")
check(app.normalize_repeat({"art": "unbekannt"}) is None, "Unbekannte Art muss verworfen werden")
check(app.next_repeat_date({"art": "taeglich"}, _date(2026, 3, 1)) == _date(2026, 3, 2), "taeglich")
check(app.next_repeat_date({"art": "wochentage", "tage": [0, 4]}, _date(2026, 3, 2)) == _date(2026, 3, 6), "wochentage Mo->Fr")
check(app.next_repeat_date({"art": "monatlich"}, _date(2026, 1, 31), _date(2026, 1, 31)) == _date(2026, 2, 28), "monatlich 31.01")
check(app.next_repeat_date({"art": "monatlich"}, _date(2026, 2, 28), _date(2026, 1, 31)) == _date(2026, 3, 31), "monatlich zurueck auf 31.")
check(app.next_repeat_date({"art": "taeglich", "ende": "2026-03-01"}, _date(2026, 3, 1)) is None, "Ende der Reihe")
check(app.describe_repeat({"art": "wochentage", "tage": [0, 2]}) == "jeden Mo, Mi", app.describe_repeat({"art": "wochentage", "tage": [0, 2]}))
check(app.parse_repeat_text("jeden Mo, Mi") == {"art": "wochentage", "tage": [0, 2]}, "TXT-Rueckweg")

setup([leaf("Wiederkehrend")])
_serie = app.items[0]
_serie["due"] = "2026-03-01"
_serie["repeat"] = app.normalize_repeat({"art": "tage", "abstand": 3}, default_start="2026-03-01")
app.refresh_tree()
app.tree.selection_set(_serie["id"])
app.toggle_done()
check(_serie["due"] == "2026-03-04", f"Vorruecken fehlgeschlagen: {_serie['due']}")
check(_serie["done"] is False, "Ein vorgerueckter Punkt muss wieder offen stehen")
app.undo_last_change()
_serie = app.find_item(_serie["id"])[0]
check(_serie["due"] == "2026-03-01" and _serie["done"] is False,
      f"Rueckgaengig stellte den Termin nicht her: {_serie['due']} {_serie['done']}")

_serie["repeat"] = app.normalize_repeat({"art": "taeglich", "ende": "2026-03-01"}, default_start="2026-03-01")
app.refresh_tree()
app.tree.selection_set(_serie["id"])
app.toggle_done()
_serie = app.find_item(_serie["id"])[0]
check(_serie["done"] is True, "Am Ende der Reihe bleibt der Punkt erledigt")
check(_serie["repeat"] is None, "Am Ende der Reihe faellt die Regel weg")

edit_target = app.new_item("Zu bearbeiten", due="2026-01-05")
app.items.append(edit_target)
app.refresh_tree()
edited, _ = open_form(
    lambda: app.themed_item_details_dialog(edit_target),
    lambda dlg: fill_and_submit(dlg, "Umbenannt", "06.01.2026", "07:30"),
)
check(isinstance(edited, dict), "Detail-Maske lieferte nichts zurueck")
if isinstance(edited, dict):
    check(set(edited) == FORM_KEYS, f"Detail-Maske: Felder weichen ab: {sorted(set(edited) ^ FORM_KEYS)}")
    check(app.apply_item_details(edit_target, edited), "Aenderung wurde nicht uebernommen")
    check(edit_target["text"] == "Umbenannt", edit_target["text"])
    check(edit_target["due"] == "2026-01-06" and edit_target["due_time"] == "07:30",
          f"Fälligkeit nicht uebernommen: {edit_target.get('due')} {edit_target.get('due_time')}")
    # Ein zweiter Durchlauf mit denselben Werten darf nichts mehr aendern.
    check(not app.apply_item_details(edit_target, edited), "Unveraenderte Uebernahme meldet eine Aenderung")

# Ohne Datum gibt es keine Uhrzeit.
edit_target["due_time"] = "07:30"
app.apply_item_details(edit_target, dict(edited, due=None, due_time="07:30"))
check(edit_target["due"] is None and edit_target["due_time"] is None,
      f"Uhrzeit ohne Datum blieb stehen: {edit_target.get('due_time')}")

# Eine unlesbare Uhrzeit haelt das Formular offen, statt sie zu verwerfen.
dialogs.clear()
rejected, _ = open_form(
    lambda: app.new_item_dialog("Neuer Punkt"),
    lambda dlg: (fill_and_submit(dlg, "Mit Murks", "24.12.2026", "25:99"), dlg.destroy()),
)
check(rejected is None, "Unlesbare Uhrzeit wurde stillschweigend uebernommen")
check(any(kind == "warn" for kind, *_ in dialogs), "Unlesbare Uhrzeit wurde nicht gemeldet")

# Erweiterte Eingabe: uebernimmt, was in der Schnelleingabe steht.
setup([leaf("A")])
app.entry_placeholder_active = False
app.entry.delete(0, mod.tk.END)
app.entry.insert(0, "Aus der Schnelleingabe")
open_form(
    app.add_item_advanced,
    lambda dlg: fill_and_submit(dlg, "Aus der Schnelleingabe", "01.02.2027"),
)
check(any(item["text"] == "Aus der Schnelleingabe" for item in app.items),
      f"Erweiterte Eingabe hat den Punkt nicht angelegt: {texts(app.items)}")
check(not app.get_entry_text(), "Schnelleingabe wurde nach dem Anlegen nicht geleert")

# Uhrzeit ueberlebt den TXT-Rundlauf.
setup([leaf("A")])
app.items[0]["due"] = "2026-12-24"
app.items[0]["due_time"] = "18:45"
import io as _io
buffer = _io.StringIO()
app.write_items_to_txt(buffer, app.items, [])
lines = buffer.getvalue().splitlines(keepends=True)
roundtrip = app.parse_txt_items(lines)
check(bool(roundtrip) and roundtrip[0].get("due") == "2026-12-24",
      f"Datum ueberlebt den TXT-Rundlauf nicht: {roundtrip[:1]}")
check(bool(roundtrip) and roundtrip[0].get("due_time") == "18:45",
      f"Uhrzeit ueberlebt den TXT-Rundlauf nicht: {roundtrip[:1]}")

# Und den Speicher-Rundlauf.
app.save_items()
app.load_items()
saved = next((item for item in app.items if item.get("due_time")), None)
check(saved is not None and saved["due_time"] == "18:45",
      "Uhrzeit ueberlebt Speichern und Laden nicht")


# ------------------------------------------------------------------ Ergebnis
if failures:
    print(f"BEFUNDE ({len(failures)}):")
    for entry in failures[:25]:
        print(" -", entry)
    if len(failures) > 25:
        print(f"   … und {len(failures) - 25} weitere")
    sys.exit(1)

print(
    f"Glide v{mod.APP_VERSION} Datenintegritaet: Bestandswaechter, Papierkorb fuer Punkte, "
    f"Gruppieren/Aufloesen ({len(KIND_SETS) * len(selections)} Kombinationen), Ziehen, "
    "Listenwechsel, Mehrfachauswahl, gemeinsame Eingabemaske und Uhrzeit: OK"
)
root.destroy()
