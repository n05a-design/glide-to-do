import ctypes
import importlib.machinery
import importlib.util
import csv
import io
import json
import os
import pathlib
import re
import tempfile
import time
import zipfile
from datetime import date as datetime_date
from datetime import timedelta as datetime_timedelta
from types import SimpleNamespace


REPOSITORY_ROOT = pathlib.Path(__file__).parents[2]
SOURCE = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"


def load_module():
    loader = importlib.machinery.SourceFileLoader("glide_app", str(SOURCE))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def read_windows_dark_caption_value(root):
    """Liest den realen DWM-Dark-Mode-Wert des gemappten Hauptfensters."""
    if os.name != "nt":
        return None
    try:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)
        user32.GetParent.argtypes = [ctypes.c_void_p]
        user32.GetParent.restype = ctypes.c_void_p
        hwnd = root.winfo_id()
        hwnd = user32.GetParent(ctypes.c_void_p(hwnd)) or hwnd
        value = ctypes.c_int(-1)
        for attribute in (20, 19):
            result = dwmapi.DwmGetWindowAttribute(
                ctypes.c_void_p(hwnd),
                attribute,
                ctypes.byref(value),
                ctypes.sizeof(value),
            )
            if result == 0:
                return value.value
    except Exception:
        return None
    return None


def pump_tk(root, milliseconds):
    """Verarbeitet Tk-Callbacks, ohne eine plattformabhängige Sleep-Schleife."""
    completed = root.tk.call("after", milliseconds, "set", "::glide_test_wait", "1")
    del completed
    root.tk.call("vwait", "::glide_test_wait")
    root.update_idletasks()


def close_test_app(app):
    """Löst Timer des isolierten Interpreters vor einem Tk-Neustart."""
    app.cancel_pending_callbacks()
    app.release_data_lock()
    for job in app.root.tk.call("after", "info"):
        app.root.tk.call("after", "cancel", job)
    app.root.destroy()


with tempfile.TemporaryDirectory(prefix="glide-test-") as temp_root:
    # GLIDE_DATA_DIR isoliert den Nutzerdatenordner auf allen Plattformen.
    # APPDATA allein wirkt nur unter Windows; unter macOS und Linux würde der
    # Test sonst die echten Daten in ~/Library/Application Support/Glide bzw.
    # ~/.local/share/Glide benutzen und überschreiben (AGENTS.md, Regel 5).
    os.environ["APPDATA"] = temp_root
    os.environ["GLIDE_DATA_DIR"] = str(pathlib.Path(temp_root) / "Glide")
    mod = load_module()
    assert pathlib.Path(mod.BASE_DIR).resolve() == (
        pathlib.Path(temp_root) / "Glide"
    ).resolve(), mod.BASE_DIR
    pathlib.Path(mod.SETTINGS_FILE).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(mod.SETTINGS_FILE).write_text(
        json.dumps({"theme": "dark"}, ensure_ascii=False),
        encoding="utf-8",
    )

    # Dialoge in diesem automatischen Test niemals interaktiv anzeigen.
    dialog_errors = []
    mod.ListApp.show_info = staticmethod(lambda *args, **kwargs: None)
    mod.ListApp.show_warning = staticmethod(lambda *args, **kwargs: None)
    mod.ListApp.show_error = staticmethod(lambda *args, **kwargs: dialog_errors.append(args))
    mod.ListApp.ask_yes_no = staticmethod(lambda *args, **kwargs: True)

    root = mod.tk.Tk()
    root.withdraw()
    app = mod.ListApp(root)
    root.update_idletasks()

    assert mod.APP_VERSION == "3.37.0"
    assert (REPOSITORY_ROOT / "VERSION").read_text(encoding="utf-8").strip() == mod.APP_VERSION
    assert len([entry for entry in app.lists if entry.get("system_role") == "inbox"]) == 1
    inbox = next(entry for entry in app.lists if entry.get("system_role") == "inbox")
    assert app.lists[0] is inbox
    assert inbox["folder_id"] is None
    inbox_iid = f"list:{inbox['id']}"
    # Seit 3.22 gibt es für den Tag nur noch eine Zeile: „Mein Tag“ führt die
    # Aufgaben mit Bearbeitungstag, die frühere Doppelung ist entfallen.
    assert app.TODAY_PLAN_ROW_ID == app.PLAN_DAY_ROW_ID
    assert app.TODAY_PLAN_VIEW == app.PLAN_DAY_VIEW
    # Punkte 1 und 2 (3.24.0): Der Systembereich zeigt sechs Zeilen. Eingang
    # und „Verspätet“ sind keine eigenen Zeilen mehr, sondern Abschnitte in
    # „Mein Tag“ beziehungsweise „In Bearbeitung“. Die Ansichten selbst und
    # die Eingangsliste bleiben über Menü und App-Aktionen erreichbar.
    # 26.09.2026: „In Bearbeitung“ ist ein Abschnitt von „Mein Tag“, der
    # Änderungsverlauf ein Knopf in der Kopfzeile – beide ohne eigene Zeile.
    # 27.09.2026: „Seiten“ ist ein eigener Bereich über den Listen.
    assert app.system_listbox.get_children("") == (
        app.HOME_ROW_ID,
        app.PLAN_DAY_ROW_ID,
        app.LABELS_ROW_ID,
        app.TEMPLATE_ROW_ID,
        app.TRASH_ROW_ID,
    )
    assert not app.system_listbox.exists(app.IN_PROGRESS_ROW_ID)
    assert not app.system_listbox.exists("smart:history")
    assert not app.history_button.winfo_manager()
    assert any("history" in action["id"] for action in app.app_action_entries())
    assert app.SYSTEM_NESTED_VIEWS == ()
    assert app.system_row_depth(("view", "overdue")) == 0
    assert app.system_row_depth(("view", app.PLAN_DAY_VIEW)) == 0
    assert not app.system_listbox.exists(inbox_iid)
    assert not app.system_listbox.exists(app.OVERDUE_ROW_ID)
    assert not app.system_listbox.item(app.PLAN_DAY_ROW_ID, "text").startswith(" ")
    assert not app.sidebar_listbox.exists(inbox_iid)
    assert int(app.system_listbox.cget("height")) == 5
    assert not hasattr(app, "sidebar_divider")
    # Seit 3.0 traegt jede Systemzeile ein Symbol aus app.ICONS. Der Test
    # liest es von dort, damit ein Wechsel des Zeichens nur eine Stelle trifft.
    assert app.system_listbox.item(app.LABELS_ROW_ID, "text") == "Labels"
    assert app.system_listbox.set(app.LABELS_ROW_ID, "icon") == app.ICONS["labels"]
    # Die Textanpassung bei geaenderter Breite baut die Zeilen selbst zusammen.
    # Sie muss dieselben Symbole liefern - sonst verschwaenden sie beim ersten
    # Ziehen am Fensterrand.
    app.refresh_sidebar_row_texts()
    root.update_idletasks()
    assert app.system_listbox.item(app.PLAN_DAY_ROW_ID, "text") == "Heute"
    assert app.system_listbox.set(app.PLAN_DAY_ROW_ID, "icon") == app.ICONS["today"]
    assert app.system_listbox.set(app.TRASH_ROW_ID, "icon") == app.ICONS["trash"]
    assert app.IN_PROGRESS_ROW_ID not in app.sidebar_iid_to_row
    assert app.system_listbox.item(app.PLAN_DAY_ROW_ID, "tags") == ("system",)
    inbox_tag_config = app.system_listbox.tag_configure("system")
    assert inbox_tag_config["foreground"] == app.theme["text"], inbox_tag_config
    # Die Schriftgröße/Familie ist seit 3.6 personalisierbar; der Tag muss
    # deshalb der aktuell berechneten Abschnittsschrift folgen.
    assert tuple(root.tk.splitlist(inbox_tag_config["font"])) == tuple(map(str, app.sidebar_section_font())), inbox_tag_config

    class RejectingBindingWidget:
        def bind(self, *_args, **_kwargs):
            raise mod.tk.TclError("unsupported sequence")

    assert app.bind_optional(RejectingBindingWidget(), "<ISO_Left_Tab>", lambda _event: None) is False

    # Die eingecheckten Referenzdaten werden tatsächlich durch die aktuelle
    # Normalisierung geführt: v7 als Sollstand, v6/v5/v4/v2 als Migrationseingang.
    original_folders = app.folders
    original_labels = app.labels
    original_trash = app.trash
    v7_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "current_v7" / "reference_v7.json").read_text(encoding="utf-8")
    )
    v7_referenced = app.validate_backup_schema(v7_fixture)
    assert v7_referenced == set()
    v7_lists, v7_active = app.normalize_lists_data(v7_fixture)
    assert v7_active == "fixture-list-project"
    # Die beiden festen Labels stehen immer oben und entstehen beim Laden.
    assert [entry["name"] for entry in app.labels[:2]] == ["Langtext", "Zwischenüberschrift"]
    assert [app.system_label_role(entry) for entry in app.labels[:2]] == ["long", "heading"]
    user_labels = [entry for entry in app.labels if not app.is_system_label(entry)]
    assert [entry["name"] for entry in user_labels] == ["Dringend", "Kunde"]
    # Labels nutzen dieselbe Palette wie Listen- und Aufgabenfarben.
    assert [entry["color"] for entry in user_labels] == ["delete", "clear"]
    assert all(entry["color"] in app.LIST_COLOR_KEYS for entry in app.labels)
    # Auch Ordner und Listen tragen Labels; unbekannte IDs fallen weg.
    assert app.folders[0]["labels"] == ["fixture-label-customer"]
    v7_project_list = next(entry for entry in v7_lists if entry["id"] == "fixture-list-project")
    assert v7_project_list["labels"] == ["fixture-label-urgent"]
    v7_items = {
        item["id"]: item
        for entry in v7_lists
        for item in app.walk_items(entry.get("items", []))
    }
    assert v7_items["fixture-item-project"]["labels"] == [
        "fixture-label-urgent",
        "fixture-label-customer",
    ]
    # Ein Verweis auf ein nicht mehr vorhandenes Label verschwindet beim Laden.
    assert v7_items["fixture-item-loose"]["labels"] == []
    assert len(app.trash) == 2
    v7_trash_list = next(entry for entry in app.trash if entry["kind"] == "list")
    assert v7_trash_list["origin_folder_id"] == "fixture-folder-work"
    assert v7_trash_list["list"]["items"][0]["labels"] == ["fixture-label-urgent"]
    assert v7_trash_list["list"]["system_role"] is None
    assert next(entry for entry in app.trash if entry["kind"] == "folder")["folder"]["title"] == (
        "Geloeschter Ordner"
    )

    # Format 10 ist der neue Sollstand: der Papierkorb haelt jetzt auch einzelne
    # Punkte, samt Unterpunkten und Herkunft.
    v10_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "current_v10" / "reference_v10.json").read_text(encoding="utf-8")
    )
    assert app.validate_backup_schema(v10_fixture) == set()
    v10_lists, _v10_active = app.normalize_lists_data(v10_fixture)

    # Format 11 ergaenzt die Wiederholungsregel. Der v10-Bestand oben muss
    # weiterhin gelten: eine fehlende Regel heisst "wiederholt sich nicht".
    for _v10_liste in v10_lists:
        for _v10_punkt in app.walk_items(_v10_liste.get("items", [])):
            assert _v10_punkt.get("repeat") is None
    v11_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "current_v11" / "reference_v11.json").read_text(encoding="utf-8")
    )
    assert v11_fixture["version"] == 11
    assert app.validate_backup_schema(v11_fixture) == set()
    v11_lists, _v11_active = app.normalize_lists_data(v11_fixture)
    _v11_wiederholend = [
        punkt for liste in v11_lists for punkt in app.walk_items(liste.get("items", []))
        if punkt.get("repeat")
    ]
    assert len(_v11_wiederholend) == 1
    assert _v11_wiederholend[0]["repeat"]["art"] == "monatlich"
    assert app.describe_repeat(_v11_wiederholend[0]["repeat"]) == "monatlich"
    v10_item_entry = next(entry for entry in app.trash if entry["kind"] == app.TRASH_KIND_ITEM)
    assert app.trash_entry_title(v10_item_entry) == "Versehentlich geloeschter Punkt"
    v10_payload = app.trash_entry_payload(v10_item_entry)
    assert app.collect_item_ids([v10_payload]) == {"fixture-trashed-item", "fixture-trashed-child"}
    assert v10_item_entry["origin"]["list_id"] == "fixture-list-project"
    assert v10_item_entry["origin"]["index"] == 1
    # Wiederherstellen setzt ihn an genau diese Stelle zurueck. Der Bestand der
    # Anwendung wird dafuer geliehen und danach exakt zurueckgegeben, damit die
    # folgenden Abschnitte auf demselben Stand weiterarbeiten wie vorher.
    _saved_state = (app.lists, app.trash, app.active_list_id, app.items, app.app_title)
    try:
        app.lists = v10_lists
        app.set_active_list("fixture-list-project", refresh=False)
        assert app.restore_trash_entry(v10_item_entry["id"], save=False)
        assert app.items[1]["id"] == "fixture-trashed-item"
        assert app.items[1]["children"][0]["id"] == "fixture-trashed-child"
    finally:
        app.lists, app.trash, app.active_list_id, app.items, app.app_title = _saved_state

    # Format 9 laedt unveraendert weiter: verschachtelte Ordner und ein Langtext
    # mit echten Zeilenumbrüchen.
    v9_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "current_v9" / "reference_v9.json").read_text(encoding="utf-8")
    )
    assert app.validate_backup_schema(v9_fixture) == set()
    v9_lists, _v9_active = app.normalize_lists_data(v9_fixture)
    assert app.folder_parent_id("fixture-folder-sub") == "fixture-folder-work"
    assert app.folder_parent_id("fixture-folder-subsub") == "fixture-folder-sub"
    assert app.folder_depth("fixture-folder-subsub") == 2
    assert app.folder_path_titles("fixture-folder-subsub") == [
        "Arbeit", "Unterordner", "Zweite Ebene"
    ]
    v9_nested = next(entry for entry in v9_lists if entry["id"] == "fixture-list-nested")
    assert v9_nested["folder_id"] == "fixture-folder-subsub"
    assert app.list_path_title(v9_nested) == (
        "Arbeit › Unterordner › Zweite Ebene › Tief liegende Liste"
    )
    v9_long = next(
        item for entry in v9_lists for item in app.walk_items(entry.get("items", []))
        if item["id"] == "fixture-item-long"
    )
    assert app.is_long_item(v9_long)
    assert v9_long["text"].count("\n") == 2, v9_long["text"]

    # Format 8 ist der neue Sollstand: Arten, feste Labels und ein Bestand,
    # in dem Art und Label absichtlich auseinanderlaufen.
    v8_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "current_v8" / "reference_v8.json").read_text(encoding="utf-8")
    )
    assert app.validate_backup_schema(v8_fixture) == set()
    v8_lists, v8_active = app.normalize_lists_data(v8_fixture)
    assert v8_active == "fixture-list-project"
    v8_items = {
        item["id"]: item
        for entry in v8_lists
        for item in app.walk_items(entry.get("items", []))
    }
    assert app.item_kind(v8_items["fixture-item-heading"]) == app.ITEM_KIND_HEADING
    assert app.item_kind(v8_items["fixture-item-long"]) == app.ITEM_KIND_LONG
    # Eine unbekannte Art laedt als Aufgabe, statt den Punkt zu verlieren.
    assert app.item_kind(v8_items["fixture-item-unknown-kind"]) == app.ITEM_KIND_TASK
    # Fehlt das feste Label in der Datei, ergaenzt die Normalisierung es.
    assert "fixture-label-long" in v8_items["fixture-item-long-unlabelled"]["labels"]
    assert "fixture-label-heading" in v8_items["fixture-item-heading"]["labels"]
    # Eigene Labels bleiben neben dem festen erhalten.
    assert v8_items["fixture-item-long"]["labels"] == [
        "fixture-label-urgent",
        "fixture-label-long",
    ]
    assert [entry["name"] for entry in app.labels[:2]] == ["Langtext", "Zwischenüberschrift"]

    v6_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "current_v6" / "reference_v6.json").read_text(encoding="utf-8")
    )
    app.validate_backup_schema(v6_fixture)
    v6_lists, v6_active = app.normalize_lists_data(v6_fixture)
    assert v6_active == "fixture-list-project"
    # Ein Format-6-Bestand kennt weder eigene Labels noch Papierkorb; die beiden
    # festen Labels ergänzt die Migration.
    assert [entry["name"] for entry in app.labels] == ["Langtext", "Zwischenüberschrift"]
    assert app.trash == []
    assert all(
        item.get("labels") == []
        for entry in v6_lists
        for item in app.walk_items(entry.get("items", []))
    )
    v6_groups = [
        item
        for entry in v6_lists
        for item in app.walk_items(entry.get("items", []))
        if app.is_group_item(item)
    ]
    assert len(v6_groups) == 2, len(v6_groups)
    # Gruppen tragen nie einen Status; die Normalisierung muss das erzwingen.
    assert all(
        not g["done"] and g["due"] is None and g["importance"] == 0 for g in v6_groups
    )
    assert sum(app.count_items(entry.get("items", [])) for entry in v6_lists) == 5

    v5_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "current_v5" / "reference_v5.json").read_text(encoding="utf-8")
    )
    v5_lists, v5_active = app.normalize_lists_data(v5_fixture)
    assert v5_active == "fixture-list-project"
    assert v5_lists[1]["items"][0]["color"] == "due_action"
    # Ein Format-5-Bestand kennt kein "kind" und muss vollständig als Aufgaben laden.
    assert all(
        not app.is_group_item(item)
        for entry in v5_lists
        for item in app.walk_items(entry.get("items", []))
    )

    v4_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "current_v4" / "reference_v4.json").read_text(encoding="utf-8")
    )
    v4_lists, _v4_active = app.normalize_lists_data(v4_fixture)
    assert v4_lists[1]["items"][0]["color"] is None

    v2_fixture = json.loads(
        (REPOSITORY_ROOT / "tests" / "fixtures" / "legacy_v2" / "probelisten_5_listen_v2.json").read_text(encoding="utf-8")
    )
    v2_lists, _v2_active = app.normalize_lists_data(v2_fixture)
    assert len(v2_lists) == 5
    assert sum(len(entry.get("items", [])) for entry in v2_lists) == 50
    assert sum(app.count_items(entry.get("items", [])) for entry in v2_lists) >= 50
    app.folders = original_folders
    app.labels = original_labels
    app.trash = original_trash

    # Der Windows/NumLock-Fehler darf keine Command-Bindings mehr registrieren.
    if os.name == "nt":
        # Tk 9 normalisiert Command unter Windows zu Control. Die Abfrage
        # einer Alias-Sequenz liefert daher das erlaubte Control-Binding.
        assert not any("Command" in sequence for sequence in root.bind())
        if mod.tk.TkVersion < 9:
            assert not root.bind("<Command-f>")
            assert not root.bind("<Command-a>")
        assert root.bind("<Control-f>")
        assert len(app.custom_menu_buttons) == 4
        assert isinstance(app.custom_menu_buttons[0], mod.RoundedButton)
        posted_menus = []
        real_post_menu = app._post_custom_menu
        try:
            app._post_custom_menu = lambda button, menu: posted_menus.append((button, menu))
            for menu_button in app.custom_menu_buttons:
                menu_button._on_keyboard_activate(None)
            assert len(posted_menus) == 4 and len({str(menu) for _, menu in posted_menus}) == 4
        finally:
            app._post_custom_menu = real_post_menu
        assert app.theme_name == "dark"
        assert app.custom_menubar.cget("bg") == app.theme["bg"]
        assert app.custom_menu_buttons[0].cget("bg") == app.theme["bg"]

        # Der gespeicherte Dark Mode muss bereits beim ersten Mapping die
        # native Windows-Titelleiste erreichen, nicht erst nach einem Toggle.
        root.deiconify()
        root.update()
        pump_tk(root, max(app.WINDOWS_CHROME_RETRY_DELAYS_MS) + 200)
        root_bottom = root.winfo_rooty() + root.winfo_height()
        # Seit 27.09.2026 stehen keine Knöpfe mehr unter dem Listenbaum; der
        # Baum selbst muss vollständig im Fenster enden.
        assert app.sidebar_listbox.winfo_rooty() + app.sidebar_listbox.winfo_height() <= root_bottom
        assert app.sidebar_listbox.winfo_height() > 0
        # Geprüft wird die linke Textflucht des Systembereichs gegen die
        # Überschrift „Listen und Ordner". Gemessen wird dafür die **erste
        # vorhandene** Systemzeile, nicht eine namentlich genannte.
        #
        # 3.25.0: Hier stand bis 3.24 die Eingangszeile – die 3.24 aus dem
        # Systembereich entfernt hat. Diese Zusicherung läuft nur unter
        # Windows und war deshalb in der Linux-Vorabumgebung nie zu sehen;
        # sie scheiterte beim ersten Lauf auf Zielhardware mit
        # „Item list:… not found". Eine Zusicherung, die eine Zeile beim
        # Namen nennt, veraltet mit jeder Navigationsänderung.
        erste_systemzeile = app.system_listbox.get_children("")[0]
        assert erste_systemzeile == app.HOME_ROW_ID
        system_bbox = app.system_listbox.bbox(erste_systemzeile)
        assert system_bbox
        system_mid_y = system_bbox[1] + system_bbox[3] // 2
        # Die Textkante aus der benannten Titelzelle messen.
        title_bbox = app.system_listbox.bbox(erste_systemzeile, "title")
        assert str(app.system_listbox.column("title", "anchor")) == "w"
        heading_offset = app.sidebar_title.winfo_rootx() - app.system_listbox.winfo_rootx()
        if tuple(map(int, root.tk.call("package", "provide", "Tk").split(".")[:2])) < (9, 0):
            system_text_x = next(
                x
                for x in range(title_bbox[0], title_bbox[0] + title_bbox[2])
                if app.system_listbox.identify_element(x, system_mid_y) == "text"
            )
            assert abs(system_text_x - heading_offset) <= 1
        else:
            # Tk 9 identifiziert das text-Element mit einer anderen Zellfläche.
            # Die benannte Titelzelle bleibt die belastbare Layoutgrenze:
            # linksbündig, Überschrift innerhalb ihres linken Innenabstands.
            assert 0 <= heading_offset - title_bbox[0] <= 8, (heading_offset, title_bbox)
        # Seit 2.8 trennt ausschließlich Abstand die beiden Bäume; der
        # frühere Rahmen system_box ist kein Bestandteil der Oberfläche mehr.
        assert not hasattr(app, "sidebar_separator")
        assert not hasattr(app, "system_box")
        assert app.system_listbox.winfo_rooty() < app.sidebar_title.winfo_rooty()
        assert app.sidebar_title.winfo_rooty() < app.sidebar_listbox.winfo_rooty()
        system_gap = app.sidebar_title.winfo_rooty() - (
            app.system_listbox.winfo_rooty() + app.system_listbox.winfo_height()
        )
        assert system_gap >= app.SIDEBAR_SECTION_GAP - 2, system_gap
        dark_caption = read_windows_dark_caption_value(root)
        assert dark_caption is not None
        assert dark_caption == 1

        app.toggle_theme()
        pump_tk(root, max(app.WINDOWS_CHROME_RETRY_DELAYS_MS) + 200)
        assert app.theme_name == "light"
        light_caption = read_windows_dark_caption_value(root)
        assert light_caption is not None
        assert light_caption == 0

        app.toggle_theme()
        pump_tk(root, max(app.WINDOWS_CHROME_RETRY_DELAYS_MS) + 200)
        assert app.theme_name == "dark"
        assert app.custom_menubar.cget("bg") == app.theme["bg"]
        assert app.custom_menu_buttons[0].cget("bg") == app.theme["bg"]
        root.withdraw()

    normal_list = next(entry for entry in app.lists if not app.is_inbox_list(entry))
    app.set_active_list(normal_list["id"])
    task = app.new_item("Aus dem Eingang sortieren", description="Mehrzeilige\nBeschreibung")
    app.items.append(task)
    assert app.save_items() is True
    app.refresh_tree(selected_id=task["id"])

    # Listenübergreifendes Drag-&-Drop nutzt denselben Kernhelfer und ist global rückgängig.
    assert app.move_items_to_list([task["id"]], inbox["id"])
    assert not normal_list["items"]
    assert inbox["items"][0]["id"] == task["id"]
    app.undo_last_change()
    normal_list = next(entry for entry in app.lists if entry.get("id") == normal_list["id"])
    inbox = next(entry for entry in app.lists if entry.get("system_role") == "inbox")
    assert normal_list["items"][0]["id"] == task["id"]
    assert not inbox["items"]
    task = normal_list["items"][0]

    # Das neue Kontextmenü erhält Mehrfachauswahl und setzt Metadaten direkt.
    second_task = app.new_item("Zweiter Kontextpunkt")
    normal_list["items"].append(second_task)
    app.set_active_list(normal_list["id"])
    app.refresh_tree()
    app.tree.selection_set((task["id"], second_task["id"]))
    app.tree.focus(task["id"])
    context_menu = app.build_item_context_menu()
    context_labels = [
        context_menu.entrycget(index, "label")
        for index in range(context_menu.index("end") + 1)
        if context_menu.type(index) != "separator"
    ]
    assert "Wichtigkeit" in context_labels
    assert "Fälligkeit" in context_labels
    assert "Aufgabenfarbe" in context_labels
    assert "Entfernen" in context_labels

    color_index = next(
        index
        for index in range(context_menu.index("end") + 1)
        if context_menu.type(index) == "cascade" and context_menu.entrycget(index, "label") == "Aufgabenfarbe"
    )
    color_menu = context_menu.nametowidget(context_menu.entrycget(color_index, "menu"))
    turquoise_index = next(
        index
        for index in range(color_menu.index("end") + 1)
        if color_menu.type(index) == "command"
        and color_menu.entrycget(index, "label").replace("✓", "").strip() == "Türkis"
    )
    color_menu.invoke(turquoise_index)
    root.update()  # Menübefehle laufen seit 3.32.0 im nächsten Leerlauf
    context_menu.destroy()

    # Das gepostete Aufgabenmenü darf nicht direkt nach tk_popup zerstört werden.
    class PopupProbe:
        def __init__(self):
            self.popup_at = None
            self.grab_released = False
            self.destroyed = False

        def tk_popup(self, x_root, y_root):
            self.popup_at = (x_root, y_root)

        def grab_release(self):
            self.grab_released = True

        def destroy(self):
            self.destroyed = True

    first_popup = PopupProbe()
    second_popup = PopupProbe()
    original_identify_row = app.tree.identify_row
    original_context_builder = app.build_item_context_menu
    app.tree.identify_row = lambda _y: task["id"]
    app.build_item_context_menu = lambda: first_popup
    popup_event = SimpleNamespace(y=0, x_root=120, y_root=240)
    assert app.show_item_context_menu(popup_event) == "break"
    assert first_popup.popup_at == (120, 240)
    assert first_popup.grab_released is True
    assert first_popup.destroyed is False
    app.build_item_context_menu = lambda: second_popup
    assert app.show_item_context_menu(popup_event) == "break"
    assert first_popup.destroyed is True
    assert second_popup.destroyed is False
    app._destroy_item_context_menu()
    assert second_popup.destroyed is True
    app.tree.identify_row = original_identify_row
    app.build_item_context_menu = original_context_builder

    app.set_importance_selected(3)
    app.set_due_value_selected("2026-09-01")
    for context_task in (task, second_task):
        assert context_task["importance"] == 3
        assert context_task["due"] == "2026-09-01"
        assert context_task["color"] == "due_action"
        assert app.tree.item(context_task["id"], "tags") == ("itemcolor_due_action",)
        assert "01.09.2026" not in app.tree.item(context_task["id"], "text")
        assert app.tree.set(context_task["id"], "due") == f"{app.DUE_COLUMN_ICON} 01.09.26"
    # Die Labelspalte steht ganz rechts neben der Fälligkeit und bleibt
    # unsichtbar, solange keine Labels angelegt sind.
    assert tuple(app.tree.cget("columns")) == ("due", "labels", "due_padding", "text_gap", "source")
    assert tuple(app.tree.cget("displaycolumns")) == ("text_gap", "due", "labels", "due_padding")
    assert int(app.tree.column("due", "width")) == app.active_due_column_width()
    # Die Mindestbreite ist 0, damit die Spalte in einem schmalen Fenster
    # vollständig weichen kann; die Sollbreite setzt sync_task_tree_columns.
    assert int(app.tree.column("due", "minwidth")) == 0
    assert bool(int(app.tree.column("due", "stretch"))) is False
    # Seit 3.3.0 links ausgerichtet: Kalender- und Labelsymbol stehen damit
    # in jeder Zeile an derselben Stelle, unabhaengig von der Textlaenge.
    assert str(app.tree.column("due", "anchor")) == "w"
    assert str(app.tree.column("labels", "anchor")) == "w"
    assert bool(int(app.tree.column("labels", "stretch"))) is False
    # Nur die beiden festen Labels: ohne einen Punkt, der eines von ihnen
    # trägt, bleibt die Spalte geschlossen.
    assert all(app.is_system_label(entry) for entry in app.labels)
    assert app.active_label_column_width() == 0
    assert int(app.tree.column("labels", "width")) == 0
    assert int(app.tree.column("due_padding", "width")) == app.DUE_RIGHT_PADDING_WIDTH
    assert int(app.tree.column("due_padding", "minwidth")) == app.DUE_RIGHT_PADDING_WIDTH
    assert bool(int(app.tree.column("due_padding", "stretch"))) is False
    root.deiconify()
    root.update()
    text_bbox = app.tree.bbox(task["id"], "#0")
    due_bbox = app.tree.bbox(task["id"], "due")
    due_padding_bbox = app.tree.bbox(task["id"], "due_padding")
    assert text_bbox and due_bbox and due_padding_bbox
    assert due_bbox[0] - (text_bbox[0] + text_bbox[2]) == app.TASK_METADATA_GAP
    assert due_bbox[2] == app.active_due_column_width()
    assert due_bbox[0] + due_bbox[2] == due_padding_bbox[0]
    assert due_padding_bbox[2] == app.DUE_RIGHT_PADDING_WIDTH
    assert due_padding_bbox[0] + due_padding_bbox[2] <= app.tree.winfo_width()

    # Der native Aufgabenpfeil bleibt trotz eigener Drag-Bindung klickbar,
    # sitzt innerhalb des Auswahlbalkens und der Zustand überlebt Refreshes.
    task["children"].append(app.new_item("Unterpunkt für Klapptest"))
    app.refresh_tree(selected_id=task["id"])
    root.update()
    task_bbox = app.tree.bbox(task["id"])
    assert task_bbox
    task_mid_y = task_bbox[1] + task_bbox[3] // 2
    indicator_x = next(
        x
        for x in range(app.tree.winfo_width())
        if "indicator" in app.tree.identify_element(x, task_mid_y).lower()
    )
    assert indicator_x >= app.SIDEBAR_ITEM_LEFT_PADDING
    assert bool(app.tree.item(task["id"], "open")) is True
    assert app.on_drag_start(SimpleNamespace(x=indicator_x, y=task_mid_y, state=0)) == "break"
    assert bool(app.tree.item(task["id"], "open")) is False
    app.refresh_tree(selected_id=task["id"])
    assert bool(app.tree.item(task["id"], "open")) is False
    task["children"].clear()
    app.refresh_tree(selected_id=task["id"])
    root.withdraw()
    # Den zusätzlichen Prüfpunkt danach wieder entfernen, damit die folgenden
    # Backup-Assertions ihren bisherigen eindeutigen Referenzpunkt behalten.
    normal_list["items"].remove(second_task)
    app.save_items()
    app.refresh_tree(selected_id=task["id"])

    # Ordneransicht zeigt ausschließlich enthaltene Listen und legt über das Eingabefeld dort an.
    folder = app.new_folder_object("Das Roos")
    app.folders.append(folder)
    normal_list["folder_id"] = folder["id"]
    app.set_active_folder(folder["id"])
    overview_rows = app.tree.get_children("")
    assert f"folder-list:{normal_list['id']}" in overview_rows
    assert app.get_display_title() == "Das Roos"
    previous_list_title = normal_list["title"]
    app.save_items()
    assert normal_list["title"] == previous_list_title
    app.clear_entry_placeholder()
    app.entry.insert(0, "Neue Projektliste")
    app.add_item()
    new_project_list = next(entry for entry in app.lists if entry.get("title") == "Neue Projektliste")
    assert new_project_list.get("folder_id") == folder["id"]
    assert app.resolve_task_drop_destination(("folder", folder["id"])) == new_project_list["id"]

    # Lange Namen werden nur in der Seitenleiste gekürzt; Klappzustände bleiben
    # bei Auswahl und Neuaufbau erhalten und der Pfeil hat Innenabstand.
    long_title = "PROBELISTEN FÜR DIE LOKALE LISTEN-APP"
    new_project_list["title"] = long_title
    second_folder = app.new_folder_object("Ordner")
    app.folders.append(second_folder)
    app.update_sidebar_list()
    long_iid = f"list:{new_project_list['id']}"
    # Der Zähler steht immer vollständig da und berührt die rechte Kante nicht;
    # gekürzt wird ausschließlich der Titel.
    long_row_text = app.sidebar_listbox.item(long_iid, "text")
    assert app.sidebar_listbox.set(long_iid, "count") == "(0)"
    assert long_row_text.startswith("PROBELISTEN")
    assert long_row_text.endswith("…")
    sidebar_font = app.sidebar_row_font()
    sidebar_available = app.sidebar_available_text_width(app.sidebar_listbox, depth=1)
    assert sidebar_available is not None and sidebar_available > 0
    assert sidebar_font.measure(long_row_text) <= sidebar_available
    # Ohne messbare Breite greift die zeichenbasierte Rückfallebene.
    assert app.sidebar_row_text(long_title, 0, tree=None) == (
        long_title[: app.SIDEBAR_TITLE_MAX_CHARS].rstrip() + "...  (0)"
    )
    assert new_project_list["title"] == long_title
    first_folder_iid = f"folder:{folder['id']}"
    second_folder_iid = f"folder:{second_folder['id']}"
    app.sidebar_listbox.item(first_folder_iid, open=False)
    app.set_active_folder(second_folder["id"])
    assert bool(app.sidebar_listbox.item(first_folder_iid, "open")) is False
    app.set_active_folder(folder["id"])
    assert bool(app.sidebar_listbox.item(first_folder_iid, "open")) is False

    root.deiconify()
    root.update()
    folder_bbox = app.sidebar_listbox.bbox(first_folder_iid)
    assert folder_bbox
    folder_mid_y = folder_bbox[1] + folder_bbox[3] // 2
    folder_indicator_x = next(
        x
        for x in range(app.sidebar_listbox.winfo_width())
        if "indicator" in app.sidebar_listbox.identify_element(x, folder_mid_y).lower()
    )
    assert folder_indicator_x >= app.SIDEBAR_ITEM_LEFT_PADDING

    # Listen lassen sich in der Ordnerübersicht per echtem Drag-Pfad sortieren.
    app.sidebar_listbox.item(first_folder_iid, open=True)
    app.refresh_tree()
    root.update()
    source_iid = f"folder-list:{new_project_list['id']}"
    target_iid = f"folder-list:{normal_list['id']}"
    # Einmal (27.09.2026, unter Last) fehlte die Zeile hier: Ein verzögerter
    # Neuaufbau lief noch. Auf den stabilen Endzustand warten und im Fehlerfall
    # sagen, welche Ansicht offen war.
    for _versuch in range(40):
        if app.tree.exists(source_iid) and app.tree.exists(target_iid) \
                and app.tree.bbox(source_iid) and app.tree.bbox(target_iid):
            break
        root.update()
    assert app.tree.exists(source_iid), (app.view_mode, app.active_folder_id == folder["id"],
                                         app.tree.get_children())
    source_bbox = app.tree.bbox(source_iid)
    target_bbox = app.tree.bbox(target_iid)
    assert source_bbox and target_bbox
    start_event = SimpleNamespace(
        x=source_bbox[0] + 8,
        y=source_bbox[1] + source_bbox[3] // 2,
        x_root=app.tree.winfo_rootx() + source_bbox[0] + 8,
        y_root=app.tree.winfo_rooty() + source_bbox[1] + source_bbox[3] // 2,
        state=0,
    )
    drop_before_event = SimpleNamespace(
        x=target_bbox[0] + 8,
        y=target_bbox[1] + 1,
        x_root=app.tree.winfo_rootx() + target_bbox[0] + 8,
        y_root=app.tree.winfo_rooty() + target_bbox[1] + 1,
        state=0,
    )
    assert app.on_drag_start(start_event) == "break"
    assert app.on_drag_motion(drop_before_event) == "break"
    assert "drop_target" in app.tree.item(target_iid, "tags")
    assert app.on_drag_end(drop_before_event) == "break"
    assert [entry["id"] for entry in app.get_folder_lists(folder["id"])][:2] == [
        new_project_list["id"],
        normal_list["id"],
    ]

    # Derselbe Drag-Pfad verschiebt eine Übersichtsliste auf einen anderen Ordner links.
    app.refresh_tree()
    root.update()
    source_bbox = app.tree.bbox(source_iid)
    target_folder_bbox = app.sidebar_listbox.bbox(second_folder_iid)
    assert source_bbox and target_folder_bbox
    start_event = SimpleNamespace(
        x=source_bbox[0] + 8,
        y=source_bbox[1] + source_bbox[3] // 2,
        x_root=app.tree.winfo_rootx() + source_bbox[0] + 8,
        y_root=app.tree.winfo_rooty() + source_bbox[1] + source_bbox[3] // 2,
        state=0,
    )
    sidebar_drop_event = SimpleNamespace(
        x=app.sidebar_listbox.winfo_rootx() - app.tree.winfo_rootx() + target_folder_bbox[0] + 8,
        y=app.sidebar_listbox.winfo_rooty() - app.tree.winfo_rooty() + target_folder_bbox[1] + target_folder_bbox[3] // 2,
        x_root=app.sidebar_listbox.winfo_rootx() + target_folder_bbox[0] + 8,
        y_root=app.sidebar_listbox.winfo_rooty() + target_folder_bbox[1] + target_folder_bbox[3] // 2,
        state=0,
    )
    assert app.on_drag_start(start_event) == "break"
    assert app.on_drag_motion(sidebar_drop_event) == "break"
    assert "drop_target" in app.sidebar_listbox.item(second_folder_iid, "tags")
    assert app.on_drag_end(sidebar_drop_event) == "break"
    assert new_project_list["folder_id"] == second_folder["id"]
    assert not app.tree.exists(source_iid)
    root.withdraw()

    # Seit 2.7.0 bearbeitet ein gemeinsamer Dialog Titel und Beschreibungstext
    # eines Ordners – analog zu „Punktdetails“ und in genau einem Fenster.
    folder_menu = app.build_sidebar_context_menu(("folder", second_folder["id"]))
    folder_menu_labels = [
        folder_menu.entrycget(index, "label")
        for index in range(folder_menu.index("end") + 1)
        if folder_menu.type(index) != "separator"
    ]
    assert "Bearbeiten (Titel, Beschreibungstext) …" in folder_menu_labels
    assert "Umbenennen …" not in folder_menu_labels
    assert "Beschreibungstext bearbeiten …" not in folder_menu_labels
    assert "Ordner mit Listen in den Papierkorb" in folder_menu_labels
    original_page_dialog = app.themed_page_details_dialog
    app.themed_page_details_dialog = lambda *_args, **_kwargs: {
        "title": "Ordner B",
        "note": "Beschreibung von Ordner B",
    }
    description_index = folder_menu_labels.index("Bearbeiten (Titel, Beschreibungstext) …")
    command_indices = [
        index
        for index in range(folder_menu.index("end") + 1)
        if folder_menu.type(index) != "separator"
    ]
    folder_menu.invoke(command_indices[description_index])
    folder_menu.destroy()
    root.update()  # Einträge mit „…“ laufen seit 29.09.2026 im nächsten Leerlauf
    assert second_folder["note"] == "Beschreibung von Ordner B"
    assert second_folder["title"] == "Ordner B"

    # Derselbe Dialog gilt für Listen; der Eingang behält dabei seinen Namen.
    list_menu = app.build_sidebar_context_menu(("list", new_project_list["id"]))
    list_menu_labels = [
        list_menu.entrycget(index, "label")
        for index in range(list_menu.index("end") + 1)
        if list_menu.type(index) != "separator"
    ]
    assert "Bearbeiten (Titel, Beschreibungstext) …" in list_menu_labels
    assert "Umbenennen …" not in list_menu_labels
    assert "In den Papierkorb" in list_menu_labels
    list_menu.destroy()
    app.themed_page_details_dialog = lambda *_args, **_kwargs: {
        "title": "Projektliste B",
        "note": "Listenbeschreibung",
    }
    app.edit_list_details(new_project_list["id"])
    assert new_project_list["title"] == "Projektliste B"
    assert new_project_list["note"] == "Listenbeschreibung"

    captured_page_dialog = {}

    def capture_page_dialog(heading, title_value, note_value, title_label="Titel", title_editable=True, page=None):
        captured_page_dialog.update(
            {"heading": heading, "title": title_value, "editable": title_editable}
        )
        return None

    app.themed_page_details_dialog = capture_page_dialog
    app.edit_list_details(inbox["id"])
    assert captured_page_dialog["editable"] is False
    assert inbox["title"] == "Eingang"
    app.themed_page_details_dialog = original_page_dialog

    # Beschreibungstexte sind eigene Seitendaten und zählen nicht als Aufgaben.
    folder["note"] = "Ein längerer freier Beschreibungstext"
    app.update_page_note_preview()
    assert "Beschreibungstext" in folder["note"]

    # „In Bearbeitung“ ist eine abgeleitete, chronologisch sortierte Ansicht.
    inbox_due_task = app.new_item("Fälliger Eingangspunkt", due="2026-08-30")
    inbox["items"].append(inbox_due_task)
    nested_due_task = app.new_item("Fälliger Unterpunkt", due="2026-08-31")
    nested_parent = app.new_item("Undatierter Elternpunkt", children=[nested_due_task])
    new_project_list["items"].extend([nested_parent, app.new_item("Undatierter Punkt")])
    app.save_items()
    previous_active_list_id = app.active_list_id
    previous_items_reference = app.items
    app.set_in_progress_view()
    assert app.view_mode == "in_progress"
    assert app.active_list_id == previous_active_list_id
    assert app.items is previous_items_reference
    saved_smart_view_settings = json.loads(pathlib.Path(mod.SETTINGS_FILE).read_text(encoding="utf-8"))
    assert saved_smart_view_settings["view_mode"] == "in_progress"
    assert saved_smart_view_settings["active_list_id"] == previous_active_list_id
    due_entries = app.get_in_progress_items(apply_filters=False)
    assert [entry[4]["id"] for entry in due_entries] == [
        inbox_due_task["id"],
        nested_due_task["id"],
        task["id"],
    ]
    # Punkt 2 (3.24.0): „In Bearbeitung“ zeigt das Überfällige unter eigener
    # Überschrift. Die Überschrift ist kein Punkt: Sie steht in keiner
    # Quellzuordnung und wird hier deshalb von den Punktzeilen getrennt.
    # Punkte 5 und 6 (3.25.0): Die Überschriften sind seit 3.25 Elternzeilen
    # und lassen sich zuklappen; die Punktzeilen hängen darunter. Und ganz
    # oben steht die eine Aufgabe, die als Nächstes dran ist.
    def uebersichtszeilen(eltern=""):
        gesammelt = []
        for row_id in app.tree.get_children(eltern):
            if row_id in app.OVERVIEW_SECTION_ROW_IDS:
                gesammelt.extend(uebersichtszeilen(row_id))
            else:
                gesammelt.append(row_id)
        return gesammelt

    abschnittszeilen = [row_id for row_id in app.tree.get_children("")
                        if row_id in app.OVERVIEW_SECTION_ROW_IDS]
    # Seit 3.33.6 (D14) steht die nächste Aufgabe oben in „Heute“; „Demnächst“
    # (bis 3.33.5 „In Bearbeitung“) zeigt alle Fälligkeiten chronologisch.
    assert app.NEXT_TASK_SECTION_ROW_ID not in abschnittszeilen
    progress_rows = uebersichtszeilen()
    assert all(row_id not in app.in_progress_item_sources for row_id in abschnittszeilen)
    assert len(progress_rows) == 3
    assert [app.tree.set(row_id, "due") for row_id in progress_rows] == [
        f"{app.DUE_COLUMN_ICON} 30.08.26",
        f"{app.DUE_COLUMN_ICON} 31.08.26",
        f"{app.DUE_COLUMN_ICON} 01.09.26",
    ]
    # Punkt 5 (3.25.0): Die nächste Aufgabe folgt `task_urgency_rank` –
    # innerhalb derselben Dringlichkeitsstufe entscheidet die Wichtigkeit, und
    # der Punkt vom 01.09. trägt die höchste. Startseite und „Heute“ nennen
    # dieselbe Aufgabe.
    fokus_item, _fokus_liste = app.home_focus_candidate()
    assert fokus_item["id"] == app.in_progress_item_sources[progress_rows[2]][1]
    assert app.plan_day_sections(apply_filters=False, day=datetime_date.today().isoformat()).naechste[4] is fokus_item
    nested_progress_row = next(
        row_id
        for row_id, source in app.in_progress_item_sources.items()
        if source == (new_project_list["id"], nested_due_task["id"])
    )
    app.tree.focus(nested_progress_row)
    assert app.open_in_progress_source_item() == "break"
    assert app.view_mode == "list"
    assert app.active_list_id == new_project_list["id"]
    assert app.tree.selection() == (nested_due_task["id"],)
    assert bool(app.tree.item(nested_parent["id"], "open")) is True
    app.set_in_progress_view()
    before_add_counts = [app.count_items(entry.get("items", [])) for entry in app.lists]
    app.add_item()
    assert [app.count_items(entry.get("items", [])) for entry in app.lists] == before_add_counts
    assert app.resolve_task_drop_destination(("view", "in_progress")) is None
    assert all(entry.get("system_role") != "in_progress" for entry in app.lists)

    # Anhänge werden kopiert, relativ gespeichert und bei der Normalisierung erhalten.
    source_attachment = pathlib.Path(temp_root) / "beispiel bild.txt"
    source_attachment.write_text("Anhangstest", encoding="utf-8")
    attachment = app.store_attachment(str(source_attachment))
    assert not os.path.isabs(attachment["storage"])
    managed_attachment_path = pathlib.Path(app.resolve_attachment_path(attachment))
    assert managed_attachment_path.read_text(encoding="utf-8") == "Anhangstest"
    source_attachment.write_text("Original nachträglich geändert", encoding="utf-8")
    assert managed_attachment_path.read_text(encoding="utf-8") == "Anhangstest"
    source_attachment.unlink()
    assert managed_attachment_path.exists()

    # Fehlerhafte Kopien hinterlassen keine Teildatei; zu große Dateien werden
    # bereits beim Anhängen statt erst beim Komplettbackup abgewiesen.
    failure_source = pathlib.Path(temp_root) / "kopierfehler.txt"
    failure_source.write_text("Test", encoding="utf-8")
    attachments_before = set(pathlib.Path(mod.ATTACHMENTS_DIR).iterdir())
    original_copy2 = mod.shutil.copy2
    def failing_copy2(_source, destination):
        pathlib.Path(destination).write_bytes(b"teilweise")
        raise OSError("simulierter Kopierfehler")
    mod.shutil.copy2 = failing_copy2
    try:
        app.store_attachment(str(failure_source))
        raise AssertionError("Ein Kopierfehler hätte weitergereicht werden müssen.")
    except OSError:
        pass
    finally:
        mod.shutil.copy2 = original_copy2
    assert set(pathlib.Path(mod.ATTACHMENTS_DIR).iterdir()) == attachments_before
    oversized_source = pathlib.Path(temp_root) / "zu-gross.bin"
    with oversized_source.open("wb") as oversized_file:
        oversized_file.truncate(app.MAX_BACKUP_ATTACHMENT_BYTES + 1)
    try:
        app.store_attachment(str(oversized_source))
        raise AssertionError("Eine Datei über 512 MB hätte abgewiesen werden müssen.")
    except OSError as exc:
        assert "512 MB" in str(exc)
    normalized = app.normalize_items([
        {
            "id": task["id"],
            "text": "Details",
            "description": "Langtext",
            "attachments": [attachment],
            "children": [],
        }
    ])
    assert normalized[0]["description"] == "Langtext"
    assert normalized[0]["attachments"][0]["name"] == "beispiel bild.txt"
    assert normalized[0]["color"] is None

    # Speicherschema und portables Backup enthalten die neuen Daten und Binäranhänge.
    app.set_active_list(normal_list["id"])
    normal_list = app.current_list()
    normal_list["items"][0]["attachments"] = [attachment]
    normal_list["items"][0]["description"] = "Langtext"
    normal_list["note"] = "Beschreibungstext"
    app.save_items()
    payload = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    assert payload["version"] == mod.ListApp.DATA_SCHEMA_VERSION == 23
    assert payload["lists"][0]["system_role"] == "inbox"
    # Format 7 und 8 ergänzen ausschließlich additive Felder.
    assert [entry["name"] for entry in payload["labels"]] == ["Langtext", "Zwischenüberschrift"]
    assert [entry["system"] for entry in payload["labels"]] == ["long", "heading"]
    assert payload["trash"] == []
    assert all("labels" in item for item in app.walk_items(payload["lists"][0].get("items", [])))

    # Ein Format-6-Bestand ohne labels/trash bleibt unverändert ladbar.
    v6_backup = app.complete_backup_payload()
    v6_backup["version"] = 6
    v6_backup.pop("labels", None)
    v6_backup.pop("trash", None)
    app.validate_backup_schema(v6_backup, portable=True)
    v6_migrated_lists, _v6_migrated_active = app.normalize_lists_data(v6_backup)
    assert [entry["name"] for entry in app.labels] == ["Langtext", "Zwischenüberschrift"]
    assert app.trash == []
    assert all(
        item.get("labels") == []
        for entry in v6_migrated_lists
        for item in app.walk_items(entry.get("items", []))
    )

    # Komplettbackups aus 2.5.1/Datenformat 4 bleiben importierbar; die neue
    # optionale Aufgabenfarbe wird bei der Migration einfach ergänzt.
    v5_backup = app.complete_backup_payload()
    v5_backup["version"] = 5
    stack = [item for entry in v5_backup["lists"] for item in entry.get("items", [])]
    while stack:
        legacy_item = stack.pop()
        legacy_item.pop("kind", None)
        stack.extend(legacy_item.get("children", []))
    app.validate_backup_schema(v5_backup, portable=True)
    v5_lists, _v5_active = app.normalize_lists_data(v5_backup)
    assert all(
        item.get("kind") == mod.ListApp.ITEM_KIND_TASK
        for entry in v5_lists
        for item in app.walk_items(entry.get("items", []))
    )

    v4_backup = app.complete_backup_payload()
    v4_backup["version"] = 4
    stack = [item for entry in v4_backup["lists"] for item in entry.get("items", [])]
    while stack:
        legacy_item = stack.pop()
        legacy_item.pop("color", None)
        stack.extend(legacy_item.get("children", []))
    app.validate_backup_schema(v4_backup, portable=True)

    backup_path = pathlib.Path(temp_root) / "test.glidebackup"
    original_save_dialog = mod.filedialog.asksaveasfilename
    mod.filedialog.asksaveasfilename = lambda **kwargs: str(backup_path)
    app.export_full_backup()
    mod.filedialog.asksaveasfilename = original_save_dialog
    assert zipfile.is_zipfile(backup_path), dialog_errors
    with zipfile.ZipFile(backup_path) as archive:
        names = archive.namelist()
        assert "data.json" in names
        assert attachment["storage"] in names

    # Export und Speicherung melden Fehler verlässlich und lassen bestehende
    # Zieldateien unberührt.
    protected_backup = pathlib.Path(temp_root) / "bestehend.glidebackup"
    protected_backup.write_bytes(b"vorheriger-inhalt")
    broken_payload = app.complete_backup_payload()
    broken_payload["lists"][0].setdefault("items", []).append(
        app.new_item(
            "Fehlender Anhang",
            attachments=[
                {
                    "id": "missing",
                    "name": "fehlt.txt",
                    "storage": "attachments/fehlt.txt",
                    "size": 1,
                }
            ],
        )
    )
    try:
        app.write_complete_backup(str(protected_backup), broken_payload)
        raise AssertionError("Ein unvollständiges Backup hätte abgelehnt werden müssen.")
    except FileNotFoundError:
        pass
    assert protected_backup.read_bytes() == b"vorheriger-inhalt"

    original_writer = app.write_json_atomic
    app.write_json_atomic = lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("Testfehler"))
    assert app.save_items(show_error=False) is False
    assert app.dirty is True
    app.write_json_atomic = original_writer
    assert app.save_items() is True
    assert app.dirty is False

    normal_list["note"] = "Nach Backup verändert"
    app.save_items()
    original_open_dialog = mod.filedialog.askopenfilename
    mod.filedialog.askopenfilename = lambda **kwargs: str(backup_path)
    app.import_full_backup()
    mod.filedialog.askopenfilename = original_open_dialog
    restored = next(entry for entry in app.lists if entry.get("id") == normal_list["id"])
    assert restored["note"] == "Beschreibungstext"
    assert restored["items"][0]["description"] == "Langtext"
    restored_attachment = restored["items"][0]["attachments"][0]
    assert restored_attachment["storage"] != attachment["storage"]
    assert pathlib.Path(app.resolve_attachment_path(restored_attachment)).read_text(encoding="utf-8") == "Anhangstest"
    assert list(pathlib.Path(mod.BACKUP_DIR).glob("vor_import_*.glidebackup"))

    # Alte v3-Daten und doppelte Systemrollen werden verlustfrei normalisiert.
    legacy_lists, legacy_active = app.normalize_lists_data(
        {
            "version": 3,
            "active_list_id": "legacy-list",
            "folders": [{"id": "legacy-folder", "title": "Alt"}],
            "lists": [
                {
                    "id": "legacy-list",
                    "title": "Altbestand",
                    "folder_id": "legacy-folder",
                    "items": ["Ein alter Punkt"],
                }
            ],
        }
    )
    assert legacy_active == "legacy-list"
    assert legacy_lists[0]["items"][0]["text"] == "Ein alter Punkt"
    app.lists = legacy_lists + [
        app.new_list_object("E1", [], system_role="inbox"),
        app.new_list_object("E2", [app.new_item("bleibt erhalten")], system_role="inbox"),
    ]
    app.ensure_inbox_list()
    assert len([entry for entry in app.lists if app.is_inbox_list(entry)]) == 1
    assert any(item.get("text") == "bleibt erhalten" for entry in app.lists for item in entry.get("items", []))

    # --- 2.6.0: Gruppen, Kontextmenues, Typografie -------------------------

    def menu_labels(menu):
        collected = []
        last = menu.index("end")
        for position in range(0 if last is None else last + 1):
            if menu.type(position) == "separator":
                continue
            try:
                collected.append(menu.entrycget(position, "label"))
            except mod.tk.TclError:
                continue
        return collected

    # Eine Gruppe ist ein Behaelter ohne eigenen Status.
    group_probe = app.new_item("G", done=True, due="2026-05-05", importance=3, kind=app.ITEM_KIND_GROUP)
    assert app.is_group_item(group_probe)
    assert group_probe["done"] is False and group_probe["due"] is None and group_probe["importance"] == 0
    convert_probe = app.new_item("T", done=True, due="2026-05-05", importance=2)
    assert app.set_item_kind(convert_probe, app.ITEM_KIND_GROUP)
    assert not convert_probe["done"] and convert_probe["due"] is None and convert_probe["importance"] == 0
    assert not app.set_item_kind(convert_probe, app.ITEM_KIND_GROUP)
    assert app.set_item_kind(convert_probe, app.ITEM_KIND_TASK)

    app.set_active_list(normal_list["id"])
    app.items.clear()
    stats_group = app.new_item("Phase", kind=app.ITEM_KIND_GROUP)
    stats_group["children"] = [
        app.new_item("erledigt", done=True),
        app.new_item("offen"),
        app.new_item("ueberfaellig", due="2020-01-01"),
    ]
    app.items.append(stats_group)
    app.items.append(app.new_item("frei"))
    assert app.count_items(app.items) == 4
    assert app.count_items(app.items, True) == 5
    assert app.compute_stats(app.items) == (4, 1, 1)

    # Darstellung: Marker, Anzahl, eigener Tag, keine Faelligkeitsspalte.
    app.refresh_tree()
    group_row = app.tree.item(stats_group["id"], "text")
    assert app.GROUP_MARKER.strip() in group_row, group_row
    assert "(3)" in group_row, group_row
    assert "group_item" in app.tree.item(stats_group["id"], "tags")
    assert app.tree.set(stats_group["id"], "due") == ""

    # Gruppen erscheinen nie in der abgeleiteten Faelligkeitsansicht.
    stats_group["due"] = "2026-01-01"
    assert all(
        not app.is_group_item(entry[4]) for entry in app.get_in_progress_items(apply_filters=False)
    )
    stats_group["due"] = None

    # Gruppieren, Aufloesen und Duplizieren arbeiten auf echten Daten.
    original_dialog = app.themed_input_dialog
    original_new_item_dialog = app.new_item_dialog
    app.themed_input_dialog = lambda *args, **kwargs: "Sammlung"
    app.new_item_dialog = lambda *args, **kwargs: {
        "text": "Sammlung",
        "kind": kwargs.get("kind") or app.ITEM_KIND_TASK,
        "importance": 0,
        "color": None,
        "due": None,
        "labels": [],
        "list_id": app.active_list_id,
    }
    try:
        app.items.clear()
        first = app.new_item("A")
        second = app.new_item("B")
        third = app.new_item("C")
        app.items.extend([first, second, third])
        app.refresh_tree()
        app.tree.selection_set([first["id"], second["id"]])
        app.tree.focus(first["id"])
        app.group_selected_items()
        assert len(app.items) == 2 and app.is_group_item(app.items[0])
        assert [child["text"] for child in app.items[0]["children"]] == ["A", "B"]
        assert app.items[1]["text"] == "C"

        app.refresh_tree()
        app.tree.selection_set(app.items[0]["id"])
        app.tree.focus(app.items[0]["id"])
        app.dissolve_selected_group()
        assert [item["text"] for item in app.items] == ["A", "B", "C"]

        app.refresh_tree()
        app.tree.selection_set(app.items[0]["id"])
        app.tree.focus(app.items[0]["id"])
        app.add_child_item()
        assert len(app.items[0]["children"]) == 1

        app.refresh_tree()
        app.tree.selection_set(app.items[0]["id"])
        app.tree.focus(app.items[0]["id"])
        app.duplicate_selected_items()
        assert len(app.items) == 4
        # Ohne frische IDs waeren die Zeilen im Baum nicht mehr eindeutig.
        duplicated_ids = [item["id"] for item in app.walk_items(app.items)]
        assert len(duplicated_ids) == len(set(duplicated_ids)), duplicated_ids
    finally:
        app.themed_input_dialog = original_dialog
        app.new_item_dialog = original_new_item_dialog

    # Seit 3.27 ist auch der letzte Statusfilter aus der Oberfläche entfernt.
    # Der alte Einstellungswert bleibt lesbar, beeinflusst die Ansicht aber nicht.
    filter_group = app.new_item("Filter", kind=app.ITEM_KIND_GROUP)
    filter_group["children"] = [app.new_item("offen"), app.new_item("fertig", done=True)]
    app.hide_done_var.set(True)
    assert app.get_filter_mode() == "all"
    assert app.item_visible_by_filter(filter_group)
    filter_group["children"] = [app.new_item("nur fertig", done=True)]
    assert app.item_visible_by_filter(filter_group)
    filter_group["children"] = [app.new_item("offen"), app.new_item("fertig", done=True)]
    app.hide_done_var.set(False)
    assert app.get_filter_mode() == "all"
    assert app.item_visible_by_filter(filter_group)
    assert not hasattr(app, "show_done_only_var"), "Der Erledigt-Filter muss restlos entfernt sein."

    # Export und Import halten die Punktart.
    app.items.clear()
    export_group = app.new_item("Phase 1", kind=app.ITEM_KIND_GROUP, description="Gruppennotiz")
    export_group["children"] = [
        app.new_item("Task A", done=True, importance=2),
        app.new_item("Task B", due="2026-03-03"),
    ]
    app.items.append(export_group)
    app.items.append(app.new_item("Solo"))
    txt_buffer = io.StringIO()
    app.write_items_to_txt(txt_buffer, app.items, [])
    reimported = app.parse_txt_items(txt_buffer.getvalue().splitlines(keepends=True))
    assert reimported and app.is_group_item(reimported[0])
    assert len(reimported[0]["children"]) == 2
    assert reimported[0]["description"] == "Gruppennotiz"
    assert len(reimported) == 2 and not app.is_group_item(reimported[1])
    markdown_buffer = io.StringIO()
    app.write_items_to_markdown(markdown_buffer, app.items, 0)
    assert "- **Phase 1**" in markdown_buffer.getvalue()
    csv_buffer = io.StringIO()
    app.write_items_to_csv(csv.writer(csv_buffer, delimiter=";"), app.items, [])
    csv_rows = list(csv.reader(io.StringIO(csv_buffer.getvalue()), delimiter=";"))
    # Neue Spalten haengen hinten an; alle bisherigen Positionen bleiben gleich.
    assert csv_rows[0][8] == "Gruppe" and csv_rows[0][5] == "-", csv_rows[0]
    assert csv_rows[1][8] == "Aufgabe", csv_rows[1]

    # Backups lehnen eine unbekannte Punktart ab.
    kind_backup = app.complete_backup_payload()
    app.validate_backup_schema(kind_backup, portable=True)
    broken_kind = json.loads(json.dumps(kind_backup))
    for broken_list in broken_kind["lists"]:
        for broken_item in broken_list.get("items", []):
            broken_item["kind"] = "unbekannt"
    try:
        app.validate_backup_schema(broken_kind, portable=True)
        raise AssertionError("Unbekannte Punktart wurde akzeptiert.")
    except ValueError:
        pass

    # Kontextmenues: jede Oberflaeche bietet ihre Aktionen an.
    app.items.clear()
    menu_task = app.new_item("Aufgabe")
    menu_group = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP)
    app.items.extend([menu_task, menu_group])
    app.refresh_tree()
    app.tree.selection_set(menu_task["id"])
    app.tree.focus(menu_task["id"])
    task_labels = menu_labels(app.build_item_context_menu())
    for expected in (
        "Erledigt umschalten",
        "Neu anlegen",
        "Art",
        "Wichtigkeit",
        "Fälligkeit",
        "Aufgabenfarbe",
        "Labels",
        "Struktur",
        "Zwischenablage",
        "Entfernen",
    ):
        assert expected in task_labels, (expected, task_labels)
    app.tree.selection_set(menu_group["id"])
    app.tree.focus(menu_group["id"])
    assert menu_labels(app.build_item_context_menu())[0] == "Gruppenaktionen"
    background_labels = menu_labels(app.build_tree_background_menu())
    for expected in ("Neuer Punkt …", "Neue Gruppe …", "Sortieren", "Liste exportieren"):
        assert expected in background_labels, (expected, background_labels)

    menu_folder = app.new_folder_object("Menueordner")
    app.folders.append(menu_folder)
    menu_list = app.new_list_object("Menueliste", [], folder_id=menu_folder["id"])
    app.lists.append(menu_list)
    app.update_sidebar_list()
    list_labels = menu_labels(app.build_sidebar_context_menu(("list", menu_list["id"])))
    for expected in (
        "Öffnen",
        "Bearbeiten (Titel, Beschreibungstext) …",
        "Listenfarbe",
        "Verschieben",
        "Duplizieren",
        "Exportieren",
        "In den Papierkorb",
    ):
        assert expected in list_labels, (expected, list_labels)
    folder_labels = menu_labels(app.build_sidebar_context_menu(("folder", menu_folder["id"])))
    for expected in (
        "Öffnen",
        "Bearbeiten (Titel, Beschreibungstext) …",
        "Ordnerfarbe",
        "Neu anlegen",
        "Ordner auflösen (Listen bleiben)",
        "Ordner mit Listen in den Papierkorb",
    ):
        assert expected in folder_labels, (expected, folder_labels)
    folder_menu = app.build_sidebar_context_menu(("folder", menu_folder["id"]))
    creation_index = next(i for i in range(folder_menu.index("end") + 1)
                          if folder_menu.type(i) == "cascade" and folder_menu.entrycget(i, "label") == "Neu anlegen")
    creation_menu = root.nametowidget(folder_menu.entrycget(creation_index, "menu"))
    assert "Neue Liste …" in menu_labels(creation_menu)
    # Der geschuetzte Eingang bleibt loeschgeschuetzt.
    protected_inbox = next(entry for entry in app.lists if app.is_inbox_list(entry))
    inbox_menu = app.build_sidebar_context_menu(("list", protected_inbox["id"]))
    inbox_labels = menu_labels(inbox_menu)
    trash_index = inbox_labels.index("In den Papierkorb")
    trash_positions = [
        position
        for position in range(inbox_menu.index("end") + 1)
        if inbox_menu.type(position) != "separator"
    ]
    assert inbox_menu.entrycget(trash_positions[trash_index], "state") == "disabled"
    assert app.build_sidebar_context_menu(("view", "in_progress")) is not None
    assert app.build_sidebar_context_menu(("view", "trash")) is not None

    # Titeltypografie: schwerster verfuegbarer Schnitt der Oberflaechenschrift.
    assert isinstance(app.header_title_font(), tuple) and len(app.header_title_font()) == 3
    app._font_families = {"Segoe UI", "Segoe UI Black", "Segoe UI Semibold"}
    app._heaviest_font_cache = {}
    assert app.heaviest_font(24, "Segoe UI") == ("Segoe UI Black", 24, "normal")
    # Semibold ist leichter als Bold und darf den Titel nicht duenner machen.
    app._font_families = {"Segoe UI", "Segoe UI Semibold"}
    app._heaviest_font_cache = {}
    assert app.heaviest_font(24, "Segoe UI") == ("Segoe UI", 24, "bold")
    app._font_families = None
    app._heaviest_font_cache = {}

    # --- 2.5.5: Regressionen ------------------------------------------------

    # Anhangsnamen, die nach der Bereinigung ungueltig wuerden, hatten zur Folge,
    # dass die Datei zwar geschrieben, aber nie wieder aufgeloest werden konnte.
    tricky_names = [
        "report.",
        "a.b.",
        "  x  .",
        "datei.\u2603",
        "daten..",
        "CON.txt",
        "\u2026",
        "x" * 300 + ".txt",
        "normal.png",
    ]
    for tricky in tricky_names:
        candidate = app.safe_attachment_filename(tricky)
        # Wirft ValueError, sobald der Name nicht speicherbar waere.
        app.validate_attachment_storage("attachments/" + candidate)

    tricky_source = pathlib.Path(temp_root) / "report."
    tricky_source.write_bytes(b"inhalt")
    tricky_stored = app.store_attachment(str(tricky_source))
    assert tricky_stored["name"] == "report."
    tricky_path = app.resolve_attachment_path(tricky_stored)
    assert tricky_path and os.path.isfile(tricky_path), tricky_stored
    assert tricky_stored["storage"].split("/")[1].startswith(tricky_stored["id"])

    # Der Backup-Import darf bei einem nicht normierbaren Anzeigenamen nicht
    # in einer Endlosschleife haengen bleiben.
    remap_lists = [
        {
            "id": "regression-list",
            "title": "R",
            "items": [
                {
                    "id": "regression-item",
                    "text": "x",
                    "children": [],
                    "attachments": [
                        {
                            "id": "regression-attachment",
                            "name": "report.",
                            "storage": tricky_stored["storage"],
                            "size": 6,
                        }
                    ],
                }
            ],
        }
    ]
    remapped = app.remap_import_attachments(remap_lists)
    assert len(remapped) == 1
    for mapped_storage in remapped.values():
        assert app.resolve_attachment_path({"storage": mapped_storage})

    # Eine gespeicherte Fensterposition darf nie ausserhalb des Bildschirms liegen.
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    clamped = app.clamp_geometry(f"980x740+{screen_width + 4000}+{screen_height + 3000}")
    clamped_match = re.match(r"^(\d+)x(\d+)\+(-?\d+)\+(-?\d+)$", clamped)
    assert clamped_match, clamped
    assert int(clamped_match.group(3)) <= screen_width - 120
    assert int(clamped_match.group(4)) <= screen_height - 120
    assert app.clamp_geometry("980x740") == "980x740"
    assert app.clamp_geometry("unsinn") is None

    # Wiederholte Listenaufbauten duerfen keine toten after-IDs ansammeln.
    app.cancel_pending_callbacks()
    for _ in range(60):
        app.refresh_tree()
    assert len(app._after_ids) <= 2, len(app._after_ids)

    root.deiconify()
    root.geometry("1000x800")
    root.update_idletasks()

    # Ein sehr langer Listentitel darf Einstellungen und Fortschrittszeile
    # nicht aus dem Fenster schieben. Bei minimaler Kopfbreite sind die
    # Einstellungen seit 3.30 über den sichtbaren Überlauf erreichbar.
    previous_title = app.app_title
    app.app_title = "Sehr langer Listentitel " * 8
    app.update_header_title()
    root.update_idletasks()
    root.update()
    app.sync_header_density()
    root.update_idletasks()
    minimal_header = app.header_frame.winfo_width() < app.HEADER_DENSITY_COMPACT
    assert bool(app.settings_button.winfo_ismapped()) == (not minimal_header)
    assert bool(app.header_overflow_button.winfo_ismapped()) == minimal_header
    settings_access = app.header_overflow_button if minimal_header else app.settings_button
    assert app.stats_label.winfo_ismapped()
    header_right = app.header_frame.winfo_rootx() + app.header_frame.winfo_width()
    theme_right = settings_access.winfo_rootx() + settings_access.winfo_width()
    assert theme_right <= header_right, (theme_right, header_right)
    assert app.title_label.cget("text").endswith("\u2026")

    # Das echte Überlaufmenü muss die Einstellungen auch auslösen können.
    # Nur das native Popup wird unterdrückt, damit der Test nicht blockiert.
    overflow_menu = app._new_themed_popup_menu()
    saved_menu_factory = app._new_themed_popup_menu
    saved_settings_dialog = app.show_settings_dialog
    settings_opened = []
    overflow_menu.tk_popup = lambda *args: None
    app._new_themed_popup_menu = lambda: overflow_menu
    app.show_settings_dialog = lambda: settings_opened.append(True)
    try:
        app.show_header_overflow_menu()
        settings_index = next(index for index in range(overflow_menu.index("end") + 1)
                              if overflow_menu.type(index) == "command"
                              and overflow_menu.entrycget(index, "label") == "Einstellungen …")
        overflow_menu.invoke(settings_index)
        root.update()  # Menübefehle laufen seit 3.32.0 im nächsten Leerlauf.
        assert settings_opened == [True]
    finally:
        app._new_themed_popup_menu = saved_menu_factory
        app.show_settings_dialog = saved_settings_dialog
        overflow_menu.destroy()
    app.app_title = previous_title
    app.update_header_title()

    # Alle Dialogfelder beginnen an derselben senkrechten Linie.
    measured_offsets = []

    def measure_dialog_fields():
        dialog = [
            child for child in root.winfo_children() if isinstance(child, mod.tk.Toplevel)
        ][-1]
        dialog.update_idletasks()
        origin = dialog.winfo_rootx()

        def walk(widget):
            for child in widget.winfo_children():
                widget_class = child.winfo_class()
                # Nur sichtbare Felder haben eine Kante. Seit die Eingabemaske
                # Felder je nach Auswahl ein- und ausblendet (Wiederholung),
                # laegen nicht gepackte Widgets sonst auf der Position ihres
                # naechsten sichtbaren Vorfahren und meldeten einen Abstand,
                # den niemand sieht.
                if not child.winfo_ismapped():
                    walk(child)
                    continue
                if widget_class == "Entry":
                    box = child.bbox(0)
                    measured_offsets.append(child.winfo_rootx() - origin + (box[0] if box else 0))
                elif widget_class == "Text":
                    box = child.bbox("1.0")
                    measured_offsets.append(child.winfo_rootx() - origin + (box[0] if box else 0))
                elif widget_class == "Listbox" and child.size():
                    box = child.bbox(0)
                    measured_offsets.append(child.winfo_rootx() - origin + (box[0] if box else 0))
                walk(child)

        walk(dialog)
        dialog.destroy()

    details_item = app.new_item("Feldabstand", description="Beschreibung")
    for open_dialog in (
        lambda: app.themed_item_details_dialog(details_item),
        lambda: app.themed_input_dialog("Titel", "Prompt", initial="Wert"),
        lambda: app.themed_choice_dialog("Ziel", "Prompt", [("a", "Alpha"), ("b", "Beta")]),
    ):
        root.after(120, measure_dialog_fields)
        open_dialog()
    assert measured_offsets, "keine Dialogfelder gemessen"
    expected_offset = app.DIALOG_PAD_X + app.FIELD_BORDER_WIDTH + app.FIELD_PAD_X
    # Felder der linken Spalte muessen exakt auf der Kante sitzen. Ein Feld, das
    # bewusst daneben steht, liegt deutlich weiter rechts. Eine Abweichung von
    # wenigen Pixeln waere dagegen genau der Fehler, den diese Pruefung finden
    # soll.
    #
    # Punkt 20 (3.23.0): Seit die Maske zweispaltig ist, gibt es mehr solcher
    # bewussten Fluchten – etwa den Aufwand neben dem Bearbeitungstag in der
    # linken Spalte, der rund 180 Pixel neben der Kante beginnt. Die Schwelle
    # trennt weiterhin „bewusst daneben" von „um ein paar Pixel verrutscht".
    SECOND_COLUMN_MIN_GAP = 120
    assert expected_offset in measured_offsets, sorted(set(measured_offsets))
    stray = [
        offset for offset in set(measured_offsets)
        if offset != expected_offset and offset < expected_offset + SECOND_COLUMN_MIN_GAP
    ]
    assert not stray, sorted(stray)

    root.withdraw()

    # --- 2.7.x: Systemblock, Papierkorb, Labels, Kalender, Autosave ---------

    # 2.8.0: Systembereich und Listenbereich trennt ausschliesslich Abstand –
    # kein Band, kein Rahmen, keine Linie.
    root.deiconify()
    root.update()
    assert not hasattr(app, "sidebar_separator")
    assert not hasattr(app, "system_box")
    assert not hasattr(app, "sidebar_divider")
    assert not hasattr(mod.ListApp, "SIDEBAR_DIVIDER_HEIGHT")
    assert app.system_listbox.master is app.sidebar_frame
    assert app.system_listbox.winfo_rooty() < app.sidebar_title.winfo_rooty()
    assert app.sidebar_title.winfo_rooty() < app.sidebar_listbox.winfo_rooty()
    section_gap = app.sidebar_title.winfo_rooty() - (
        app.system_listbox.winfo_rooty() + app.system_listbox.winfo_height()
    )
    assert section_gap >= app.SIDEBAR_SECTION_GAP - 2, section_gap
    # Der Aufgabenbaum muss den Tastaturfokus annehmen, sonst bewegen die
    # Pfeiltasten die Auswahl nicht.
    assert bool(int(app.tree.cget("takefocus")))
    root.withdraw()
    assert app.sidebar_iid_to_row[app.TRASH_ROW_ID] == ("view", "trash")

    # Ein sauberer Ausgangszustand fuer die folgenden Pruefungen.
    app.trash = []
    app.labels = []
    app.folders = []
    app.lists = [entry for entry in app.lists if app.is_inbox_list(entry)]
    trash_folder = app.new_folder_object("Papierkorbordner")
    app.folders.append(trash_folder)
    trash_target = app.new_list_object(
        "Zu loeschende Liste", [app.new_item("Bleibt erhalten")], folder_id=trash_folder["id"]
    )
    keep_list = app.new_list_object("Bleibende Liste", [app.new_item("Unberuehrt")])
    app.lists.extend([trash_target, keep_list])
    app.active_list_id = None
    app.set_active_list(keep_list["id"])
    app.save_items()

    # Loeschen verschiebt in den Papierkorb statt zu vernichten.
    app.delete_list_by_id(trash_target["id"])
    assert len(app.trash) == 1
    trashed_entry = app.trash[0]
    assert trashed_entry["kind"] == app.TRASH_KIND_LIST
    assert trashed_entry["origin_folder_id"] == trash_folder["id"]
    assert app.trash_entry_title(trashed_entry) == "Zu loeschende Liste"
    assert trashed_entry["list"]["items"][0]["text"] == "Bleibt erhalten"
    assert all(entry.get("id") != trash_target["id"] for entry in app.lists)
    assert app.system_listbox.item(app.TRASH_ROW_ID, "text") == "Papierkorb"
    assert app.system_listbox.set(app.TRASH_ROW_ID, "icon") == app.ICONS["trash"]

    # Der Papierkorb ueberlebt Speichern und erneutes Laden vollstaendig.
    reloaded_payload = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    assert len(reloaded_payload["trash"]) == 1
    assert reloaded_payload["trash"][0]["list"]["items"][0]["text"] == "Bleibt erhalten"

    # Die Papierkorbansicht ist eine eigene Systemansicht mit eigenem Menue.
    app.set_trash_view()
    assert app.view_mode == "trash"
    assert app.get_display_title() == "Papierkorb"
    assert app.active_label_column_width() == 0
    trash_rows = app.tree.get_children("")
    assert len(trash_rows) == 1 and trash_rows[0] == f"trash:{trashed_entry['id']}"
    app.tree.selection_set(trash_rows[0])
    assert app.get_selected_trash_ids() == [trashed_entry["id"]]
    trash_menu_labels = menu_labels(app.build_trash_context_menu(trash_rows[0]))
    for expected in ("Wiederherstellen", "In Ordner wiederherstellen …", "Endgültig entfernen", "Papierkorb leeren"):
        assert expected in trash_menu_labels, (expected, trash_menu_labels)
    # Im Papierkorb entstehen keine neuen Punkte.
    before_trash_add = len(app.trash)
    app.add_item()
    assert len(app.trash) == before_trash_add

    # Wiederherstellen setzt die Liste in ihren Herkunftsordner zurueck.
    app.tree.selection_set(trash_rows[0])
    app.restore_selected_trash_entries(False)
    assert not app.trash
    restored_list = next(entry for entry in app.lists if entry.get("title") == "Zu loeschende Liste")
    assert restored_list["folder_id"] == trash_folder["id"]
    assert restored_list["items"][0]["text"] == "Bleibt erhalten"

    # Ein geloeschter Ordner nimmt seine Listen mit und bringt sie zurueck.
    app.trash_folder(trash_folder["id"])
    assert len(app.trash) == 2
    assert not app.folders
    assert all(entry.get("title") != "Zu loeschende Liste" for entry in app.lists)
    folder_trash_entry = next(entry for entry in app.trash if entry["kind"] == app.TRASH_KIND_FOLDER)
    app.restore_trash_entry(folder_trash_entry["id"])
    assert len(app.folders) == 1
    assert not app.trash
    recovered = next(entry for entry in app.lists if entry.get("title") == "Zu loeschende Liste")
    assert recovered["folder_id"] == app.folders[0]["id"]

    # „Ordner aufloesen“ behaelt die Listen und legt nur die Huelle in den Papierkorb.
    dissolve_folder_id = app.folders[0]["id"]
    app.delete_folder(dissolve_folder_id)
    assert not app.folders
    assert any(entry.get("title") == "Zu loeschende Liste" for entry in app.lists)
    assert len(app.trash) == 1 and app.trash[0]["kind"] == app.TRASH_KIND_FOLDER

    # Papierkorb leeren entfernt endgueltig.
    app.empty_trash()
    assert not app.trash
    assert app.system_listbox.item(app.TRASH_ROW_ID, "text") == "Papierkorb"
    assert app.system_listbox.set(app.TRASH_ROW_ID, "icon") == app.ICONS["trash"]

    # Der Eingang bleibt geschuetzt.
    guarded_inbox = next(entry for entry in app.lists if app.is_inbox_list(entry))
    app.delete_list_by_id(guarded_inbox["id"])
    assert not app.trash
    assert any(app.is_inbox_list(entry) for entry in app.lists)

    # Mehrfachauswahl in der Seitenleiste.
    assert str(app.sidebar_listbox.cget("selectmode")) == "extended"
    multi_folder = app.new_folder_object("Sammelordner")
    app.folders.append(multi_folder)
    multi_a = app.new_list_object("Sammel A", [])
    multi_b = app.new_list_object("Sammel B", [])
    app.lists.extend([multi_a, multi_b])
    app.set_active_list(multi_a["id"])
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set((f"list:{multi_a['id']}", f"list:{multi_b['id']}"))
    selected_rows = app.get_selected_sidebar_rows()
    assert len(selected_rows) == 2, selected_rows
    assert sorted(app.get_selected_sidebar_list_ids()) == sorted([multi_a["id"], multi_b["id"]])
    multi_menu_labels = menu_labels(app.build_sidebar_context_menu(("list", multi_a["id"]), rows=selected_rows))
    for expected in ("Listen in Ordner verschieben", "Listen aus Ordner herauslösen", "Ordner verschieben", "Farbe der Auswahl", "In den Papierkorb"):
        assert expected in multi_menu_labels, (expected, multi_menu_labels)
    app.sidebar_listbox.selection_set((f"list:{multi_a['id']}", f"list:{multi_b['id']}"))
    app.move_selected_lists_to_folder(multi_folder["id"])
    assert multi_a["folder_id"] == multi_folder["id"]
    assert multi_b["folder_id"] == multi_folder["id"]
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set((f"list:{multi_a['id']}", f"list:{multi_b['id']}"))
    app.set_selected_sidebar_color("export")
    assert multi_a["color"] == "export" and multi_b["color"] == "export"
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set((f"list:{multi_a['id']}", f"list:{multi_b['id']}"))
    app.move_selected_lists_to_folder(None)
    assert multi_a["folder_id"] is None and multi_b["folder_id"] is None
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set((f"list:{multi_a['id']}", f"list:{multi_b['id']}"))
    app.trash_selected_sidebar_entries()
    assert len(app.trash) == 2
    assert all(entry.get("id") not in (multi_a["id"], multi_b["id"]) for entry in app.lists)
    app.empty_trash()
    app.folders = [entry for entry in app.folders if entry.get("id") != multi_folder["id"]]

    # Die Entf-Taste der Seitenleiste loescht die dortige Auswahl, nicht die
    # des Aufgabenbaums, und meldet das mit "break" zurueck.
    assert app.sidebar_listbox.bind("<Delete>")
    assert app.system_listbox.bind("<Delete>")
    delete_key_folder = app.new_folder_object("Per Entf geloescht")
    app.folders.append(delete_key_folder)
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set(f"folder:{delete_key_folder['id']}")
    assert app.delete_selected_sidebar_entry() == "break"
    assert all(entry.get("id") != delete_key_folder["id"] for entry in app.folders)
    assert any(app.trash_entry_title(entry) == "Per Entf geloescht" for entry in app.trash)
    app.empty_trash()
    delete_key_list = app.new_list_object("Liste per Entf", [])
    app.lists.append(delete_key_list)
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set(f"list:{delete_key_list['id']}")
    assert app.delete_selected_sidebar_entry() == "break"
    assert all(entry.get("id") != delete_key_list["id"] for entry in app.lists)
    app.empty_trash()
    # Systemzeilen bleiben geschuetzt.
    app.update_sidebar_list()
    app.system_listbox.selection_set(app.TRASH_ROW_ID)
    assert app.delete_selected_sidebar_entry() == "break"
    assert not app.trash
    app.system_listbox.selection_remove(app.TRASH_ROW_ID)

    # Verschieben per Tastatur ist in beiden Baeumen belegt.
    for sequence in ("<Alt-Up>", "<Alt-Down>", "<Alt-Left>", "<Alt-Right>"):
        assert app.tree.bind(sequence), sequence
        assert app.sidebar_listbox.bind(sequence), sequence

    # Alt+Auf/Ab verschiebt die Auswahl ohne Maus.
    order_a = app.new_list_object("Reihenfolge A", [])
    order_b = app.new_list_object("Reihenfolge B", [])
    app.lists.extend([order_a, order_b])
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set(f"list:{order_b['id']}")
    app.move_sidebar_selection(-1)
    ids_after_move = [entry["id"] for entry in app.lists]
    assert ids_after_move.index(order_b["id"]) < ids_after_move.index(order_a["id"])

    # --- Labels -------------------------------------------------------------
    label_red = app.new_label_object("Dringend", None, "delete")
    label_blue = app.new_label_object("Kunde", None, "clear")
    app.labels = [label_red, label_blue]
    # Labels nutzen exakt dieselbe Palette wie Listen- und Aufgabenfarben.
    assert app.LABEL_COLOR_CHOICES == app.LIST_COLOR_CHOICES
    assert app.LABEL_COLOR_KEYS == app.LIST_COLOR_KEYS
    assert app.label_color_key(label_red) == "delete"
    assert app.label_color(label_red) == app.theme["delete"]
    assert all(key in app.THEMES["light"] and key in app.THEMES["dark"] for key in app.LABEL_COLOR_KEYS)
    # Seit 3.2.0 gibt es keine Abbildung alter Farbschluessel mehr: Was nicht in
    # der Palette steht, faellt auf die Vorgabefarbe zurueck - alter Schluessel
    # oder Unsinn macht keinen Unterschied.
    assert app.new_label_object("Alt", None, "label_green")["color"] == app.DEFAULT_LABEL_COLOR
    assert app.resolve_label_color("gibt-es-nicht") == app.DEFAULT_LABEL_COLOR
    assert not hasattr(app, "LEGACY_LABEL_COLOR_MAP")
    # Der Farbauswahldialog faerbt jede Zeile in ihrer eigenen Farbe.
    captured_choice = {}

    def capture_choice(title, prompt, choices, item_colors=None):
        captured_choice.update({"choices": choices, "item_colors": item_colors})
        return None

    original_choice_dialog = app.themed_choice_dialog
    app.themed_choice_dialog = capture_choice
    app.choose_label_color("delete")
    app.themed_choice_dialog = original_choice_dialog
    assert captured_choice["item_colors"] == app.LIST_COLOR_KEYS
    assert [value for value, _text in captured_choice["choices"]] == app.LIST_COLOR_KEYS
    assert any(text.startswith("\u2713") for _value, text in captured_choice["choices"])

    label_list = app.new_list_object("Labelliste", [])
    app.lists.append(label_list)
    app.set_active_list(label_list["id"])
    labelled = app.new_item("Angebot", due="2026-09-04")
    plain_item = app.new_item("Ohne Label")
    app.items.extend([labelled, plain_item])
    app.refresh_tree()
    app.tree.selection_set(labelled["id"])
    app.toggle_label_on_selected_items(label_red["id"])
    assert labelled["labels"] == [label_red["id"]]
    app.tree.selection_set(labelled["id"])
    app.toggle_label_on_selected_items(label_blue["id"])
    assert labelled["labels"] == [label_red["id"], label_blue["id"]]
    app.refresh_tree()
    label_cell = app.tree.set(labelled["id"], "labels")
    # Seit 2.12.0 steht in der Zeile ein Label; jedes weitere wird gezaehlt.
    # Zwei Namen nebeneinander verdraengten den Aufgabentext. Seit 3.0 steht
    # ein Symbol davor, wie das Kalendersymbol vor dem Datum.
    assert label_cell.startswith(f"{app.LABEL_COLUMN_ICON} Dringend"), label_cell
    assert "Kunde" not in label_cell, label_cell
    assert label_cell.endswith("+1"), label_cell
    assert app.LABEL_COLUMN_MAX_VISIBLE == 1
    assert not hasattr(app, "label_chip")
    assert app.tree.set(plain_item["id"], "labels") == ""
    # Seit 3.3.0 folgt die Spaltenbreite dem tatsaechlichen Inhalt; der
    # Musterwert bleibt die Obergrenze.
    assert 0 < app.active_label_column_width() <= app.label_column_width()
    # 2.8.0: In einem schmalen Fenster weichen erst die Labels, dann die
    # Faelligkeit. Die tatsaechlich gesetzte Breite folgt derselben Regel.
    _live_text, live_due, live_labels = app.task_tree_column_widths(app.tree.winfo_width())
    assert int(app.tree.column("labels", "width")) == live_labels
    assert int(app.tree.column("due", "width")) == live_due
    wide_text, wide_due, wide_labels = app.task_tree_column_widths(1200)
    assert wide_labels == app.active_label_column_width()
    assert wide_due == app.active_due_column_width()
    assert wide_text == 1200 - app.active_due_column_width() - app.active_label_column_width() - (
        app.DUE_RIGHT_PADDING_WIDTH + app.TASK_TREE_EDGE_PADDING + app.TASK_METADATA_GAP
    )
    # Seit 3.0 weichen Labelspalte und Hinweiszeile bei derselben Breite – rund
    # 960 Pixel Fensterbreite, also der halben Breite eines 1920er Bildschirms.
    above_text, above_due, above_labels = app.task_tree_column_widths(
        app.LABEL_COLUMN_MIN_TREE_WIDTH
    )
    assert above_labels == app.active_label_column_width(), above_labels
    assert above_due == app.active_due_column_width()
    assert above_text >= 180
    _below_text, _below_due, below_labels = app.task_tree_column_widths(
        app.LABEL_COLUMN_MIN_TREE_WIDTH - 1
    )
    assert below_labels == 0, below_labels
    # Seit 3.33.20 (U04): „+“ statt „Hinzufuegen“, „Erweitert“ nur noch ueber
    # Umschalt+Enter, Menue und Palette – kein Dauerknopf, bei keiner Breite.
    class _W:
        def __init__(self, width):
            self.width = width
    for breite in (1, app.ADVANCED_BUTTON_MIN_WIDTH, 2000):
        app.update_advanced_button_visibility(_W(breite))
        assert app._advanced_button_visible is False
        assert app.advanced_add_button.winfo_manager() == ""
    assert app.add_button.text == "+" and str(app.add_button) in [str(c) for c in app.input_frame.pack_slaves()]

    # Die Hinweiszeile folgt derselben Schwelle.
    app.update_hint_visibility(app.LABEL_COLUMN_MIN_TREE_WIDTH)
    assert app._hint_visible is True
    app.update_hint_visibility(app.LABEL_COLUMN_MIN_TREE_WIDTH - 1)
    assert app._hint_visible is False
    app.update_hint_visibility(app.LABEL_COLUMN_MIN_TREE_WIDTH)
    narrow_width = app.DUE_COLUMN_MIN_TREE_WIDTH
    narrow_text, narrow_due, narrow_labels = app.task_tree_column_widths(narrow_width)
    assert narrow_labels == 0 and narrow_due == app.active_due_column_width()
    # Die frei gewordene Labelbreite gehoert vollstaendig dem Aufgabentext.
    assert narrow_text == narrow_width - app.active_due_column_width() - (
        app.DUE_RIGHT_PADDING_WIDTH + app.TASK_TREE_EDGE_PADDING + app.TASK_METADATA_GAP
    )
    tiny_text, tiny_due, tiny_labels = app.task_tree_column_widths(
        app.DUE_COLUMN_MIN_TREE_WIDTH - 1
    )
    assert tiny_labels == 0 and tiny_due == 0
    # Eine unbekannte Breite (Tk meldet vor dem Layout 1) darf nichts ausblenden.
    _unknown_text, unknown_due, unknown_labels = app.task_tree_column_widths(1)
    assert unknown_due == app.active_due_column_width()
    assert unknown_labels == app.active_label_column_width()
    # 3.3.0: Beide rechten Spalten folgen dem tatsaechlichen Inhalt. Sie
    # fassen den laengsten Zellinhalt und bleiben unter dem Musterwert,
    # damit zwischen Faelligkeit und Label keine leere Flaeche steht.
    gemessen = app.content_column_widths()
    assert gemessen is not None
    gemessen_due, gemessen_labels = gemessen
    assert 0 < gemessen_due <= app.due_column_width()
    assert 0 < gemessen_labels <= app.label_column_width()
    assert app.active_due_column_width() == gemessen_due
    assert app.active_label_column_width() == gemessen_labels
    baumschrift = mod.tkfont.Font(root=root, font=app.TREE_FONT)
    for pruef_row in app.get_visible_tree_iids():
        for spalte, spaltenbreite in (("due", gemessen_due), ("labels", gemessen_labels)):
            zellentext = app.tree.set(pruef_row, spalte)
            if zellentext:
                assert baumschrift.measure(zellentext) <= spaltenbreite, (spalte, zellentext)
    # Ein zweites Umschalten entfernt das Label wieder.
    app.tree.selection_set(labelled["id"])
    app.toggle_label_on_selected_items(label_blue["id"])
    assert labelled["labels"] == [label_red["id"]]
    app.tree.selection_set(labelled["id"])
    app.toggle_label_on_selected_items(label_blue["id"])
    assert labelled["labels"] == [label_red["id"], label_blue["id"]]

    # Das Punktmenue bietet die Labelzuweisung an.
    app.tree.selection_set(labelled["id"])
    assert "Labels" in menu_labels(app.build_item_context_menu())

    # Labels ueberleben Speichern und Normalisieren; unbekannte IDs fallen weg.
    app.save_items()
    label_payload = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    assert [entry["name"] for entry in label_payload["labels"]] == ["Dringend", "Kunde"]
    saved_labels = app.labels
    normalized_lists, _normalized_active = app.normalize_lists_data(label_payload)
    # Beim Laden ergaenzt Glide die beiden festen Labels vor den eigenen.
    assert [entry["name"] for entry in app.labels] == [
        "Langtext",
        "Zwischenüberschrift",
        "Dringend",
        "Kunde",
    ]
    normalized_labelled = next(
        item
        for entry in normalized_lists
        for item in app.walk_items(entry.get("items", []))
        if item.get("text") == "Angebot"
    )
    assert normalized_labelled["labels"] == [label_red["id"], label_blue["id"]]
    dropped = json.loads(json.dumps(label_payload))
    dropped["labels"] = []
    dropped_lists, _dropped_active = app.normalize_lists_data(dropped)
    assert all(
        item.get("labels") == []
        for entry in dropped_lists
        for item in app.walk_items(entry.get("items", []))
    )
    app.labels = saved_labels
    app.lists, _reload_active = app.normalize_lists_data(label_payload)
    app.labels = saved_labels
    app.ensure_inbox_list()
    app.active_list_id = None
    app.set_active_list(
        next(entry["id"] for entry in app.lists if entry.get("title") == "Labelliste"), refresh=False
    )
    app.update_sidebar_list()
    app.refresh_tree()
    labelled = next(item for item in app.items if item.get("text") == "Angebot")

    # Ein geloeschtes Label loest seine Zuweisungen.
    app.labels = [label_red]
    assert app.prune_unknown_item_labels()
    assert labelled["labels"] == [label_red["id"]]
    app.labels = [label_red, label_blue]
    labelled["labels"] = [label_red["id"], label_blue["id"]]
    assert app.count_label_usage(label_red["id"]) == 1

    # Doppelte Namen und ungueltige Farben werden bereinigt.
    cleaned = app.normalize_labels_data(
        [
            {"id": "l1", "name": "Alpha", "color": "label_green"},
            {"id": "l1", "name": "Beta", "color": "unbekannt"},
            {"id": "", "name": "alpha"},
            {"name": "   "},
            "kein Objekt",
        ]
    )
    assert [entry["name"] for entry in cleaned] == ["Alpha", "Beta"]
    assert cleaned[0]["id"] != cleaned[1]["id"]
    assert cleaned[1]["color"] == app.DEFAULT_LABEL_COLOR

    # Export und Import transportieren Labels ueber TXT, CSV und Markdown.
    label_txt = io.StringIO()
    app.write_items_to_txt(label_txt, app.items, [])
    txt_content = label_txt.getvalue()
    assert "Labels: Dringend, Kunde" in txt_content
    app.labels = []
    reimported_labels = app.parse_txt_items(txt_content.splitlines(keepends=True))
    assert [entry["name"] for entry in app.labels] == ["Dringend", "Kunde"]
    assert len(reimported_labels[0]["labels"]) == 2
    app.labels = [label_red, label_blue]

    label_csv = io.StringIO()
    app.write_items_to_csv(csv.writer(label_csv, delimiter=";"), app.items, [])
    label_csv_rows = list(csv.reader(io.StringIO(label_csv.getvalue()), delimiter=";"))
    assert label_csv_rows[0][9] == "Dringend, Kunde", label_csv_rows[0]

    label_markdown = io.StringIO()
    app.write_items_to_markdown(label_markdown, app.items, 0)
    assert "`Dringend, Kunde`" in label_markdown.getvalue()

    # --- Labels an Ordnern und Listen ---------------------------------------
    page_folder = app.new_folder_object("Labelordner")
    app.folders.append(page_folder)
    page_list = app.new_list_object("Labelseite", [app.new_item("Inhalt")], folder_id=page_folder["id"])
    app.lists.append(page_list)
    assert page_folder["labels"] == [] and page_list["labels"] == []
    app.toggle_page_label("folder", page_folder["id"], label_red["id"])
    app.toggle_page_label("list", page_list["id"], label_blue["id"])
    assert page_folder["labels"] == [label_red["id"]]
    assert page_list["labels"] == [label_blue["id"]]
    assert app.count_label_usage(label_blue["id"]) >= 2
    # Das Kontextmenue bietet die Zuweisung an beiden Stellen an.
    assert "Labels" in menu_labels(app.build_sidebar_context_menu(("list", page_list["id"])))
    assert "Labels" in menu_labels(app.build_sidebar_context_menu(("folder", page_folder["id"])))
    # In der grossen Darstellung erscheinen sie, in der Seitenleiste nicht.
    app.set_active_folder(page_folder["id"])
    overview_row = f"folder-list:{page_list['id']}"
    assert app.tree.set(overview_row, "labels") == f"{app.LABEL_COLUMN_ICON} Kunde"
    assert 0 < app.active_label_column_width() <= app.label_column_width()
    assert "Kunde" not in app.sidebar_listbox.item(f"list:{page_list['id']}", "text")
    # Die Kopfzeile zeigt die Labels der geoeffneten Seite farbig.
    app.update_page_labels()
    # Seit 2.10.0 sind das Chips: dunkler Text auf aufgehellter Labelfarbe.
    assert [widget.chip_text for widget in app.page_label_widgets] == ["Dringend"]
    red_chip = app.page_label_widgets[0]
    assert isinstance(red_chip, mod.LabelChip)
    # 3.3.0: Der Chip zeichnet vollstaendig innerhalb seiner Flaeche. Zuvor
    # lag die geglaettete Kontur genau auf der Kante und wurde an allen vier
    # Seiten angeschnitten; die Rundung war nicht zu sehen.
    chip_x, chip_y = [], []
    for chip_teil in red_chip.find_all():
        if red_chip.type(chip_teil) == "text":
            continue
        chip_werte = red_chip.coords(chip_teil)
        chip_x.extend(chip_werte[0::2])
        chip_y.extend(chip_werte[1::2])
    assert chip_x and chip_y
    assert min(chip_x) >= 0 and min(chip_y) >= 0
    assert max(chip_x) <= red_chip.chip_width - 1, max(chip_x)
    assert max(chip_y) <= red_chip.chip_height - 1, max(chip_y)

    chip_typen = [red_chip.type(teil) for teil in red_chip.find_all()]
    assert chip_typen.count("arc") == 4, chip_typen
    assert chip_typen.count("rectangle") == 2, chip_typen
    expected_fill, expected_text = app.label_chip_colors(label_red)
    assert red_chip.fill == expected_fill
    assert red_chip.text_color == expected_text
    assert red_chip.fill != app.theme["delete"]
    assert red_chip.RADIUS == mod.LabelChip.RADIUS
    assert red_chip.PAD_TOP == red_chip.PAD_BOTTOM - 2
    assert red_chip.PAD_X == mod.LabelChip.PAD_X
    app.set_active_list(page_list["id"])
    app.update_page_labels()
    assert [widget.chip_text for widget in app.page_label_widgets] == ["Kunde"]
    # Ein zweites Umschalten loest das Label wieder.
    app.toggle_page_label("list", page_list["id"], label_blue["id"])
    assert page_list["labels"] == []
    app.update_page_labels()
    assert app.page_label_widgets == []
    app.toggle_page_label("list", page_list["id"], label_blue["id"])
    # Ordner- und Listenlabels ueberstehen Speichern und Laden.
    app.save_items()
    page_payload = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    saved_folder = next(f for f in page_payload["folders"] if f["id"] == page_folder["id"])
    saved_list = next(l for l in page_payload["lists"] if l["id"] == page_list["id"])
    assert saved_folder["labels"] == [label_red["id"]]
    assert saved_list["labels"] == [label_blue["id"]]
    # Ein geloeschtes Label loest sich auch von Ordnern und Listen.
    kept_labels = app.labels
    app.labels = [label_blue]
    assert app.prune_unknown_item_labels()
    assert page_folder["labels"] == []
    app.labels = kept_labels
    page_folder["labels"] = [label_red["id"]]
    # Ungueltige Labelfelder werden im Komplettbackup abgewiesen.
    for broken_target in ("folders", "lists"):
        broken_page_payload = app.complete_backup_payload()
        broken_page_payload[broken_target][0]["labels"] = "kein Feld"
        try:
            app.validate_backup_schema(broken_page_payload, portable=True)
            raise AssertionError(f"Ungueltige Labels in {broken_target} akzeptiert.")
        except ValueError:
            pass
    app.set_active_list(label_list["id"])

    # --- 3.3.0: Ansicht „Labels“ ------------------------------------------
    # Der gesamte Bestand nach Labels gruppiert; ein Zug in eine andere Gruppe
    # tauscht genau ein Label und laesst die uebrigen stehen.
    label_gruen = app.new_label_object("Zugziel", None, "export")
    app.labels.append(label_gruen)
    labelled = app.find_item_in_lists(labelled["id"])[0]
    labelled["labels"] = [label_red["id"], label_blue["id"]]
    app.save_items()
    vorherige_liste = app.active_list_id
    app.set_labels_view()
    root.update()
    assert app.view_mode == app.LABELS_VIEW
    assert app.get_display_title() == "Labels"
    assert app.system_listbox.item(app.LABELS_ROW_ID, "text") == "Labels"
    assert app.system_listbox.set(app.LABELS_ROW_ID, "icon") == app.ICONS["labels"]
    label_gruppen = list(app.tree.get_children(""))
    label_keys = [app.label_group_key_from_iid(iid) for iid in label_gruppen]
    # „Ohne Label“ steht am Ende; die beiden festen Labels bilden keine Gruppe,
    # weil ein Zug dorthin die Art des Punkts aendern wuerde.
    assert label_keys[-1] == app.UNLABELLED_GROUP_KEY
    assert all(
        not app.is_system_label(app.get_label(key))
        for key in label_keys
        if key != app.UNLABELLED_GROUP_KEY and app.get_label(key)
    )
    # Der Punkt mit zwei Labels steht in beiden Gruppen, jeweils in Labelfarbe.
    doppelte_zeilen = [
        row for row in app.label_view_row_groups if row.endswith(f":{labelled['id']}")
    ]
    assert len(doppelte_zeilen) == 2, doppelte_zeilen
    for zeile in doppelte_zeilen:
        gruppe = app.label_view_row_groups[zeile]
        farbe = app.resolve_label_color(app.get_label(gruppe).get("color"))
        assert app.tree.item(zeile, "tags") == (f"itemcolor_{farbe}",)
    # Zug aus der roten in die gruene Gruppe: rot weicht, blau bleibt stehen.
    rote_zeile = next(
        zeile for zeile in doppelte_zeilen
        if app.label_view_row_groups[zeile] == label_red["id"]
    )
    assert app.move_item_to_label_group(rote_zeile, label_gruen["id"]) is True
    assert labelled["labels"] == [label_gruen["id"], label_blue["id"]]
    # Der Zug ist eine Aenderung wie jede andere und laesst sich zuruecknehmen.
    # Das Zuruecknehmen ersetzt die Listenobjekte, deshalb wird der Punkt
    # danach ueber seine Kennung neu gesucht.
    labelled_id = labelled["id"]
    app.undo_last_change()
    labelled = app.find_item_in_lists(labelled_id)[0]
    assert labelled["labels"] == [label_red["id"], label_blue["id"]]
    app.refresh_tree()
    # Zug nach „Ohne Label“ nimmt nur das Label der Herkunftsgruppe.
    rote_zeile = next(
        zeile for zeile in app.label_view_row_groups
        if zeile.endswith(f":{labelled['id']}")
        and app.label_view_row_groups[zeile] == label_red["id"]
    )
    assert app.move_item_to_label_group(rote_zeile, app.UNLABELLED_GROUP_KEY) is True
    assert labelled["labels"] == [label_blue["id"]]
    app.undo_last_change()
    labelled = app.find_item_in_lists(labelled_id)[0]
    assert labelled["labels"] == [label_red["id"], label_blue["id"]]
    # Zurueck in die Liste; die folgenden Pruefungen arbeiten dort weiter.
    app.labels.remove(label_gruen)
    app.set_active_list(vorherige_liste)
    root.update()

    # Seit dem 27.09.2026 gibt es statt zwölf fester Knöpfe eine Auswahlleiste:
    # Sie erscheint nur mit markierten Punkten. Farbe trägt allein „Löschen“.
    assert app.labels_button.text == f"{app.ICONS['labels']}  Labels"
    assert app.plan_button.text == f"{app.ICONS['calendar']}  Einplanen"
    assert [button.color_key for button in app.selection_buttons] == ["muted", "muted", "muted", "muted", "delete"]
    assert app.add_button.color_key == "add"  # festes Lila seit 29.09.2026 (R8)
    for veraltet in ("clear_button", "calendar_button", "edit_item_button", "undo_button", "copy_button",
                     "paste_button", "expand_button", "collapse_button", "utility_frame"):
        assert not hasattr(app, veraltet), veraltet
    assert not hasattr(app, "export_button")
    assert not hasattr(app, "import_button")
    assert root.bind("<Control-e>") and root.bind("<Control-i>")
    assert root.bind("<Control-l>") and root.bind("<Control-k>")

    # --- Kalender -----------------------------------------------------------
    reference_day = datetime_date(2026, 9, 2)  # Mittwoch
    assert app.calendar_week_start(reference_day) == datetime_date(2026, 8, 31)
    assert app.calendar_week_start().weekday() == 0
    assert app.CALENDAR_MODES == (app.CALENDAR_MODE_WEEK, app.CALENDAR_MODE_MONTH)
    # Monatsraster: montagsausgerichtet, vom Montag der ersten bis zum Sonntag
    # der letzten Woche des Monats. September 2026 ergibt genau fuenf Wochen.
    calendar_start, calendar_end = app.calendar_month_grid(2026, 9)
    assert calendar_start == datetime_date(2026, 8, 31)
    assert calendar_end == datetime_date(2026, 10, 4)
    assert (calendar_end - calendar_start).days == 34
    assert calendar_start.weekday() == 0 and calendar_end.weekday() == 6
    # Februar 2026 beginnt an einem Sonntag und braucht sechs Wochen.
    feb_start, feb_end = app.calendar_month_grid(2026, 2)
    assert feb_start == datetime_date(2026, 1, 26) and feb_end == datetime_date(2026, 3, 1)
    assert ((feb_end - feb_start).days + 1) % 7 == 0
    # Monatsnavigation ueber Jahresgrenzen hinweg.
    assert app.shift_month(2026, 12, 1) == (2027, 1)
    assert app.shift_month(2026, 1, -1) == (2025, 12)
    assert app.shift_month(2026, 9, 3) == (2026, 12)
    calendar_list = app.new_list_object(
        "Kalenderliste",
        [
            app.new_item("Im Zeitraum", due="2026-09-04"),
            app.new_item("Ausserhalb", due="2026-12-24"),
            app.new_item("Gruppe faellt weg", kind=app.ITEM_KIND_GROUP),
        ],
    )
    app.lists.append(calendar_list)
    buckets = app.collect_due_tasks_by_date(calendar_start, calendar_end)
    assert datetime_date(2026, 9, 4) in buckets
    assert datetime_date(2026, 12, 24) not in buckets
    assert all(not app.is_group_item(item) for tasks in buckets.values() for item, _source in tasks)
    assert app.open_task_in_source_list(calendar_list["id"], calendar_list["items"][0]["id"]) is True
    assert app.active_list_id == calendar_list["id"]
    assert app.open_task_in_source_list("gibt-es-nicht", "x") is False

    # Der Kalender legt per Tag eine Aufgabe mit genau dieser Faelligkeit an.
    app.set_active_list(calendar_list["id"])
    assert app.calendar_target_list()["id"] == calendar_list["id"]
    original_new_item_dialog = app.new_item_dialog

    def calendar_dialog(*_a, **kwargs):
        # Der Kalender reicht Fälligkeit und Zielliste als Vorgabe hinein.
        assert kwargs.get("default_due") is not None
        assert kwargs.get("allow_list_choice") is True
        return {
            "text": "Im Kalender angelegt",
            "kind": app.ITEM_KIND_TASK,
            "importance": 3,
            "color": "flag",
            "due": kwargs.get("default_due"),
            "labels": [],
            "list_id": kwargs.get("default_list_id"),
        }

    app.new_item_dialog = calendar_dialog
    assert app.add_task_with_due(datetime_date(2026, 9, 17)) is True
    app.new_item_dialog = original_new_item_dialog
    calendar_created = next(
        item for item in app.walk_items(calendar_list["items"]) if item["text"] == "Im Kalender angelegt"
    )
    assert calendar_created["due"] == "2026-09-17"
    # Der erweiterte Anlage-Dialog gibt Wichtigkeit und Farbe direkt mit.
    assert calendar_created["importance"] == 3
    assert calendar_created["color"] == "flag"
    # Abbruch legt nichts an.
    count_before = app.count_items(calendar_list["items"])
    app.new_item_dialog = lambda *_a, **_k: None
    assert app.add_task_with_due(datetime_date(2026, 9, 18)) is False
    app.new_item_dialog = original_new_item_dialog
    assert app.count_items(calendar_list["items"]) == count_before
    # Ausserhalb einer Liste faengt der Eingang die neue Aufgabe auf.
    app.set_trash_view()
    assert app.calendar_target_list().get("system_role") == "inbox"
    app.set_active_list(calendar_list["id"])
    # Die Hover-Umrandung besitzt in beiden Themes einen eigenen Farbwert.
    assert app.THEMES["light"]["calendar_hover"] != app.THEMES["dark"]["calendar_hover"]

    # --- Automatisches Speichern und Backup-Rotation ------------------------
    assert app.AUTOSAVE_INTERVAL_MINUTES == 5
    # Ein frueherer Pruefschritt hat alle offenen Callbacks abgeraeumt; der
    # Autosave-Zyklus wird deshalb wie beim Programmstart neu eingeplant.
    if app._autosave_id is None:
        app.schedule_autosave()
    assert app._autosave_id is not None

    def clear_backups():
        for name in os.listdir(mod.BACKUP_DIR):
            if name.startswith("liste_backup_") and name.endswith(".json"):
                os.remove(os.path.join(mod.BACKUP_DIR, name))

    def backup_names():
        return [
            name
            for name in os.listdir(mod.BACKUP_DIR)
            if name.startswith("liste_backup_") and name.endswith(".json")
        ]

    # Die Zeitsperre verhindert eine Sicherung pro Tastendruck.
    clear_backups()
    app._last_backup_monotonic = None
    app.save_items()
    app.save_items()
    app.save_items()
    assert len(backup_names()) == 1, backup_names()
    # Seit 29.09.2026 nur bei geändertem Inhalt: Auch eine erzwungene
    # Sicherung legt keinen zweiten gleichen Stand an.
    app.save_items(force_backup=True)
    assert len(backup_names()) == 1, backup_names()
    app.lists[0]["title"] = "Geaendert fuer die Sicherung"
    app.save_items(force_backup=True)
    app.autosave_tick()
    assert len(backup_names()) == 2, backup_names()

    # Autosave speichert einen offenen Stand und plant sich neu ein.
    app.dirty = True
    previous_autosave_id = app._autosave_id
    app.autosave_tick()
    assert app.dirty is False
    assert app._autosave_id is not None and app._autosave_id != previous_autosave_id
    assert len(backup_names()) == 2, "unveraenderter Stand: keine weitere Sicherung"

    # Rotation: Mindestbestand bleibt, Aeltere fallen weg, Obergrenze greift.
    # Die Tagesstaende (14 Tage) prueft test_speicherlast330; hier bleiben sie
    # aus, damit ein Lauf kurz nach Mitternacht dasselbe Ergebnis liefert.
    tagesstaende = app.BACKUP_DAILY_DAYS
    app.BACKUP_DAILY_DAYS = 0
    clear_backups()
    now_stamp = time.time()
    for index in range(30):
        candidate = pathlib.Path(mod.BACKUP_DIR) / f"liste_backup_rot{index:03d}.json"
        candidate.write_text("{}", encoding="utf-8")
        age = 0 if index >= 15 else (app.BACKUP_MAX_AGE_MINUTES + 5) * 60
        os.utime(candidate, (now_stamp - age, now_stamp - age))
    app.prune_backups()
    assert len(backup_names()) == 15, backup_names()

    clear_backups()
    for index in range(12):
        candidate = pathlib.Path(mod.BACKUP_DIR) / f"liste_backup_old{index:03d}.json"
        candidate.write_text("{}", encoding="utf-8")
        stale = (app.BACKUP_MAX_AGE_MINUTES + 60) * 60
        os.utime(candidate, (now_stamp - stale, now_stamp - stale))
    app.prune_backups()
    assert len(backup_names()) == app.MIN_BACKUPS, backup_names()

    clear_backups()
    for index in range(app.MAX_BACKUPS + 25):
        candidate = pathlib.Path(mod.BACKUP_DIR) / f"liste_backup_many{index:03d}.json"
        candidate.write_text("{}", encoding="utf-8")
        os.utime(candidate, (now_stamp - index, now_stamp - index))
    app.prune_backups()
    assert len(backup_names()) == app.MAX_BACKUPS, len(backup_names())
    app.BACKUP_DAILY_DAYS = tagesstaende

    # Portable Vorab-Sicherungen eines Imports duerfen nie rotiert werden.
    guarded_backup = pathlib.Path(mod.BACKUP_DIR) / "vor_import_geschuetzt.glidebackup"
    guarded_backup.write_bytes(b"geschuetzt")
    app.prune_backups()
    assert guarded_backup.exists()

    # --- Datenintegritaet: Anhaenge im Papierkorb ---------------------------
    integrity_source = pathlib.Path(temp_root) / "papierkorb anhang.txt"
    integrity_source.write_text("Papierkorb-Anhang", encoding="utf-8")
    integrity_attachment = app.store_attachment(str(integrity_source))
    integrity_list = app.new_list_object("Anhangsliste", [app.new_item("Mit Datei")])
    integrity_list["items"][0]["attachments"] = [integrity_attachment]
    integrity_list["items"][0]["labels"] = [label_red["id"]]
    app.lists.append(integrity_list)
    app.save_items()
    app.delete_list_by_id(integrity_list["id"])
    assert len(app.trash) == 1

    integrity_backup = pathlib.Path(temp_root) / "integritaet.glidebackup"
    integrity_payload = app.complete_backup_payload()
    referenced_storages = app.validate_backup_schema(integrity_payload, portable=True)
    assert integrity_attachment["storage"] in referenced_storages
    app.write_complete_backup(str(integrity_backup), integrity_payload)
    with zipfile.ZipFile(integrity_backup) as archive:
        assert integrity_attachment["storage"] in archive.namelist()

    trash_before_import = len(app.trash)
    labels_before_import = [
        entry["name"] for entry in app.labels if not app.is_system_label(entry)
    ]
    mod.filedialog.askopenfilename = lambda **kwargs: str(integrity_backup)
    app.import_full_backup()
    mod.filedialog.askopenfilename = original_open_dialog
    assert not dialog_errors, dialog_errors
    assert len(app.trash) == trash_before_import
    assert [
        entry["name"] for entry in app.labels if not app.is_system_label(entry)
    ] == labels_before_import
    # Ein Import ohne feste Labels ergaenzt sie, ohne eigene zu verlieren.
    assert [entry["name"] for entry in app.labels[:2]] == ["Langtext", "Zwischenüberschrift"]
    restored_trash_list = app.trash[0]["list"]
    restored_trash_attachment = restored_trash_list["items"][0]["attachments"][0]
    assert restored_trash_attachment["storage"] != integrity_attachment["storage"]
    restored_trash_path = app.resolve_attachment_path(restored_trash_attachment)
    assert restored_trash_path and os.path.isfile(restored_trash_path)
    assert pathlib.Path(restored_trash_path).read_text(encoding="utf-8") == "Papierkorb-Anhang"
    assert restored_trash_list["items"][0]["labels"] == [label_red["id"]]

    # Wiederherstellen aus dem Backup-Papierkorb liefert eine echte Liste zurueck.
    app.restore_trash_entry(app.trash[0]["id"])
    recovered_attachment_list = next(entry for entry in app.lists if entry.get("title") == "Anhangsliste")
    recovered_attachment = recovered_attachment_list["items"][0]["attachments"][0]
    assert pathlib.Path(app.resolve_attachment_path(recovered_attachment)).read_text(
        encoding="utf-8"
    ) == "Papierkorb-Anhang"
    assert recovered_attachment_list["items"][0]["labels"] == [label_red["id"]]
    assert recovered_attachment_list.get("system_role") is None

    # Ein fehlerhaftes Speichern laesst den Bestand unveraendert und meldet sich.
    guard_snapshot = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    intact_writer = app.write_json_atomic
    app.write_json_atomic = lambda *_a, **_k: (_ for _ in ()).throw(OSError("Schreibfehler"))
    assert app.save_items(show_error=False) is False
    assert app.dirty is True
    app.write_json_atomic = intact_writer
    assert json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8")) == guard_snapshot
    assert app.save_items() is True
    assert app.dirty is False

    # Ungueltige Label- und Papierkorbfelder werden abgewiesen.
    for broken_field in ("labels", "trash"):
        broken_payload = app.complete_backup_payload()
        broken_payload[broken_field] = "kein Feld"
        try:
            app.validate_backup_schema(broken_payload, portable=True)
            raise AssertionError(f"Ungueltiges Feld {broken_field} wurde akzeptiert.")
        except ValueError:
            pass
    duplicate_labels = app.complete_backup_payload()
    duplicate_labels["labels"] = [
        {"id": "same", "name": "A", "color": "label_red"},
        {"id": "same", "name": "B", "color": "label_blue"},
    ]
    try:
        app.validate_backup_schema(duplicate_labels, portable=True)
        raise AssertionError("Doppelte Label-IDs wurden akzeptiert.")
    except ValueError:
        pass
    unknown_trash_kind = app.complete_backup_payload()
    unknown_trash_kind["trash"] = [{"id": "t1", "kind": "unbekannt"}]
    try:
        app.validate_backup_schema(unknown_trash_kind, portable=True)
        raise AssertionError("Unbekannte Papierkorbart wurde akzeptiert.")
    except ValueError:
        pass


    # ------------------------------------------------------------------
    # 2.8.0: Verspaetet, Langtext, Zwischenueberschrift, Hover, Anlegen
    # ------------------------------------------------------------------
    app.labels = []
    app.ensure_system_labels()
    long_label = app.get_system_label(app.SYSTEM_LABEL_LONG)
    heading_label = app.get_system_label(app.SYSTEM_LABEL_HEADING)
    assert long_label["name"] == "Langtext" and heading_label["name"] == "Zwischenüberschrift"
    assert app.SYSTEM_LABEL_KIND[app.SYSTEM_LABEL_LONG] == app.ITEM_KIND_LONG
    assert app.SYSTEM_LABEL_KIND[app.SYSTEM_LABEL_HEADING] == app.ITEM_KIND_HEADING
    # Ein zweiter Aufruf erzeugt keine Dubletten und stellt die Reihenfolge her.
    app.labels.append(app.new_label_object("Frei", None, "export"))
    assert app.ensure_system_labels() is False
    assert [entry["name"] for entry in app.labels] == ["Langtext", "Zwischenüberschrift", "Frei"]
    free_label = app.get_label_by_name("Frei")

    # Ein von Hand angelegtes Label desselben Namens wird uebernommen statt verdoppelt.
    app.labels = [app.new_label_object("Langtext", None, "delete")]
    app.ensure_system_labels()
    assert len([entry for entry in app.labels if entry["name"] == "Langtext"]) == 1
    assert app.get_system_label(app.SYSTEM_LABEL_LONG)["color"] == "delete"

    app.labels = []
    app.ensure_system_labels()
    app.labels.append(app.new_label_object("Frei", None, "export"))
    free_label = app.get_label_by_name("Frei")
    long_label = app.get_system_label(app.SYSTEM_LABEL_LONG)
    heading_label = app.get_system_label(app.SYSTEM_LABEL_HEADING)

    kind_list = app.new_list_object("Artenliste", [])
    app.lists.append(kind_list)
    app.set_active_list(kind_list["id"])
    app.items.clear()
    plain = app.new_item("Erster Punkt")
    long_task = app.new_item("Zweiter Punkt mit sehr langem Text", kind=app.ITEM_KIND_LONG)
    heading = app.new_item("Abschnitt", kind=app.ITEM_KIND_HEADING)
    after_heading = app.new_item("Nach der Ueberschrift")
    tail = app.new_item("Letzter Punkt")
    app.items.extend([plain, long_task, heading, after_heading, tail])

    # Art und festes Label sind zwei Sichten auf dieselbe Eigenschaft.
    assert long_task["labels"] == [long_label["id"]]
    assert heading["labels"] == [heading_label["id"]]
    assert plain["labels"] == []
    assert app.is_long_item(long_task) and app.is_schedulable_item(long_task)
    assert app.is_heading_item(heading) and app.is_structural_item(heading)
    assert not app.is_schedulable_item(heading)
    # Eine Ueberschrift traegt nie Status, Faelligkeit oder Wichtigkeit.
    assert heading["done"] is False and heading["due"] is None and heading["importance"] == 0
    # Ueberschriften und Gruppen zaehlen nicht als Aufgabe.
    assert app.count_items(app.items) == 4

    app.refresh_tree()
    # Die Nummerierung beginnt unter einer Ueberschrift wieder bei 1.
    assert app.tree.item(plain["id"], "text").startswith("1. ")
    assert app.tree.item(long_task["id"], "text").startswith("2. ")
    assert app.tree.item(heading["id"], "text") == "Abschnitt"
    assert app.tree.item(after_heading["id"], "text").startswith("1. ")
    assert app.tree.item(tail["id"], "text").startswith("2. ")
    assert app.tree.item(heading["id"], "tags") == ("heading_item",)
    heading_tag = app.tree.tag_configure("heading_item")
    assert tuple(root.tk.splitlist(heading_tag["font"]))[1:] == tuple(
        map(str, app.heading_row_font()[1:])
    )
    # Ueber der Ueberschrift steht eine leere Abstandszeile.
    gap_iid = f"{heading['id']}{app.SPACER_IID_MARKER}0"
    assert app.tree.exists(gap_iid)
    assert app.tree.item(gap_iid, "text") == ""
    assert app.tree.item(gap_iid, "tags") == ("spacer",)
    assert app.is_synthetic_row(gap_iid) and app.owner_row_id(gap_iid) == heading["id"]
    # Die erste sichtbare Zeile bekommt keinen Abstand nach oben.
    app.items.insert(0, app.new_item("Kopfabschnitt", kind=app.ITEM_KIND_HEADING))
    first_heading = app.items[0]
    app.refresh_tree()
    assert not app.tree.exists(f"{first_heading['id']}{app.SPACER_IID_MARKER}0")
    app.items.pop(0)
    app.refresh_tree()

    # Ein Langtext zeigt seinen vollstaendigen Text ueber mehrere Zeilen.
    long_task["text"] = (
        "Kernbotschaft in einem einzigen Satz formulieren, der ohne weitere Erklaerung "
        "funktioniert und sowohl im Vertrieb als auch auf der Startseite traegt"
    )
    app.refresh_tree()
    continuation_ids = [
        iid
        for iid in app.tree.get_children("")
        if iid.startswith(f"{long_task['id']}{app.CONTINUATION_IID_MARKER}")
    ]
    assert continuation_ids, app.tree.get_children("")
    assert len(continuation_ids) + 1 <= app.LONG_TASK_MAX_LINES
    assert all(app.is_synthetic_row(iid) for iid in continuation_ids)
    assert all(app.owner_row_id(iid) == long_task["id"] for iid in continuation_ids)
    # Synthetische Zeilen sind Darstellung, keine Daten.
    assert long_task["id"] in app.iter_tree_ids()
    assert not any(iid in app.iter_tree_ids() for iid in continuation_ids)
    assert not any(iid in app.iter_tree_ids() for iid in (gap_iid,))
    # Zahl und Symbole stehen ausschliesslich in der ersten Zeile.
    assert app.tree.item(long_task["id"], "text").startswith("2. ")
    for iid in continuation_ids:
        assert not app.tree.item(iid, "text").lstrip().startswith("2.")
        assert app.tree.set(iid, "due") == ""

    # Die Pfeiltasten ueberspringen Fortsetzungs- und Abstandszeilen.
    visible_rows = app.get_visible_tree_iids()
    assert not any(app.is_synthetic_row(iid) for iid in visible_rows)
    assert app.get_visible_tree_iids(include_synthetic=True) != visible_rows
    app.tree.selection_set(long_task["id"])
    app.tree.focus(long_task["id"])
    app.move_tree_focus(1)
    assert app.tree.focus() == visible_rows[visible_rows.index(long_task["id"]) + 1]
    assert not app.is_synthetic_row(app.tree.focus())
    app.move_tree_focus(-1)
    assert app.tree.focus() == long_task["id"]
    # Aus einer Fortsetzungszeile heraus geht es beim naechsten Punkt weiter.
    app.tree.focus(continuation_ids[0])
    app.move_tree_focus(1)
    assert app.tree.focus() == visible_rows[visible_rows.index(long_task["id"]) + 1]

    # Reine Umbruchlogik – ohne Fenster pruefbar.
    wrapped = app.wrap_long_task_text("A B C D E F G H I J", "1. ", 10000)
    assert wrapped == ["1. A B C D E F G H I J"]
    narrow = app.wrap_long_task_text(" ".join(["Wort"] * 60), "1. ", 200)
    assert len(narrow) == app.LONG_TASK_MAX_LINES
    assert narrow[-1].endswith("…")
    assert narrow[0].startswith("1. ")
    assert all(line.startswith(" ") for line in narrow[1:])
    # Ohne messbare Breite greift die zeichenbasierte Rueckfallebene.
    fallback = app.wrap_long_task_text("Ein zwei drei", "1. ", 0)
    assert fallback and fallback[0].startswith("1. ")

    # Das feste Label wirkt wie die Umwandlung im Kontextmenue – und umgekehrt.
    app.refresh_tree()
    app.tree.selection_set(plain["id"])
    app.tree.focus(plain["id"])
    app.toggle_label_on_selected_items(long_label["id"])
    assert app.is_long_item(plain) and plain["labels"] == [long_label["id"]]
    app.tree.selection_set(plain["id"])
    app.toggle_label_on_selected_items(long_label["id"])
    assert app.item_kind(plain) == app.ITEM_KIND_TASK and plain["labels"] == []
    app.tree.selection_set(plain["id"])
    app.tree.focus(plain["id"])
    app.convert_selected_kind(app.ITEM_KIND_HEADING)
    assert app.is_heading_item(plain) and plain["labels"] == [heading_label["id"]]
    app.tree.selection_set(plain["id"])
    app.convert_selected_kind(app.ITEM_KIND_TASK)
    assert app.item_kind(plain) == app.ITEM_KIND_TASK and plain["labels"] == []

    # Eigene Labels bleiben beim Wechsel der Art erhalten.
    plain["labels"] = [free_label["id"]]
    app.set_item_kind(plain, app.ITEM_KIND_LONG)
    assert plain["labels"] == [free_label["id"], long_label["id"]]
    app.set_item_kind(plain, app.ITEM_KIND_TASK)
    assert plain["labels"] == [free_label["id"]]
    # "Alle Labels entfernen" nimmt auch die Art zurueck.
    app.set_item_kind(plain, app.ITEM_KIND_LONG)
    app.refresh_tree()
    app.tree.selection_set(plain["id"])
    app.tree.focus(plain["id"])
    app.clear_labels_on_selected_items()
    assert plain["labels"] == [] and app.item_kind(plain) == app.ITEM_KIND_TASK

    # Die festen Labels gelten nur fuer Punkte, nicht fuer Listen und Ordner.
    page_menu = app._new_themed_popup_menu()
    page_label_menu = app._add_page_label_menu(page_menu, kind_list, "list")
    page_label_names = [entry.strip() for entry in menu_labels(page_label_menu)]
    assert "Langtext" not in page_label_names
    assert "Zwischenüberschrift" not in page_label_names
    assert "Frei" in page_label_names
    app.toggle_page_label("list", kind_list["id"], long_label["id"])
    assert kind_list.get("labels") in (None, [])

    # Die Art ueberlebt Speichern, Laden und ein vollstaendiges Backup.
    app.save_items()
    kind_payload = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    kind_saved = next(
        entry for entry in kind_payload["lists"] if entry["title"] == "Artenliste"
    )
    assert [item["kind"] for item in kind_saved["items"]] == [
        "task",
        "long",
        "heading",
        "task",
        "task",
    ]
    reloaded_lists, _reloaded_active = app.normalize_lists_data(kind_payload)
    reloaded_kinds = {
        item["text"]: app.item_kind(item)
        for entry in reloaded_lists
        for item in app.walk_items(entry.get("items", []))
    }
    assert reloaded_kinds["Abschnitt"] == app.ITEM_KIND_HEADING
    assert reloaded_kinds[long_task["text"]] == app.ITEM_KIND_LONG
    # Eine unbekannte Art faellt auf "Aufgabe" zurueck, statt Daten zu verlieren.
    stray = app.normalize_items([{"text": "Fremd", "kind": "phantasie"}])
    assert app.item_kind(stray[0]) == app.ITEM_KIND_TASK
    # Ein mehrzeiliger Text wird zu einer Zeile normalisiert.
    multiline = app.normalize_items([{"text": "Erste\nZweite   Dritte"}])
    assert multiline[0]["text"] == "Erste Zweite Dritte"

    # TXT-Export und -Import erhalten die Zwischenueberschrift.
    heading_export = pathlib.Path(temp_root) / "ueberschrift.txt"
    with open(heading_export, "w", encoding="utf-8") as handle:
        app.write_items_to_txt(handle, app.items, [])
    heading_txt = heading_export.read_text(encoding="utf-8")
    assert app.HEADING_MARKER.strip() in heading_txt
    reimported = app.parse_txt_items(heading_txt.splitlines(keepends=True))
    assert any(app.is_heading_item(item) for item in reimported)

    # --- Verspaetet ----------------------------------------------------
    baseline_overdue_ids = {entry[4]["id"] for entry in app.get_overdue_items(apply_filters=False)}
    overdue_list = app.new_list_object("Fristen", [])
    app.lists.append(overdue_list)
    past = (datetime_date.today() - datetime_timedelta(days=3)).isoformat()
    future = (datetime_date.today() + datetime_timedelta(days=3)).isoformat()
    overdue_open = app.new_item("Laengst faellig", due=past)
    overdue_done = app.new_item("Faellig, aber erledigt", due=past, done=True)
    upcoming = app.new_item("Kommt noch", due=future)
    overdue_group = app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP)
    overdue_group["due"] = past
    overdue_list["items"].extend([overdue_open, overdue_done, upcoming, overdue_group])
    app.update_sidebar_list()
    overdue_texts = [entry[4]["text"] for entry in app.get_overdue_items(apply_filters=False)]
    assert {entry[4]["id"] for entry in app.get_overdue_items(apply_filters=False)} == baseline_overdue_ids | {overdue_open["id"]}
    # Punkt 2 (3.24.0): „Verspätet“ hat keine Seitenleistenzeile mehr. Die
    # Ansicht selbst bleibt vollständig – erreichbar über das Ansichtsmenü,
    # die App-Aktionen, die Startseite und den Abschnitt in „In Bearbeitung“.
    assert app.OVERDUE_ROW_ID not in app.system_listbox.get_children("")
    assert "Verspätet" in mod.ListApp.ACTION_GROUPS["Ansichten"]

    app.set_overdue_view()
    assert app.view_mode == "overdue"
    assert app.get_display_title() == "Verspätet"
    assert app.view_mode in app.TASK_OVERVIEW_VIEWS
    overdue_rows = [iid for iid in app.tree.get_children("") if iid != app.EMPTY_ROW_ID]
    assert len(overdue_rows) == len(baseline_overdue_ids) + 1
    assert any("Laengst faellig" in app.tree.item(iid, "text") for iid in overdue_rows)
    assert app.build_smart_view_menu("overdue") is not None
    assert "Öffnen" in menu_labels(app.build_smart_view_menu("overdue"))
    # Wird der Punkt erledigt, verlaesst er die Ansicht von selbst.
    overdue_open["done"] = True
    assert {entry[4]["id"] for entry in app.get_overdue_items(apply_filters=False)} == baseline_overdue_ids
    overdue_open["done"] = False
    # Die Ansicht laesst sich speichern und wieder herstellen.
    app.save_settings()
    assert json.loads(
        pathlib.Path(mod.SETTINGS_FILE).read_text(encoding="utf-8")
    )["view_mode"] == "overdue"
    app.set_in_progress_view()
    assert app.view_mode == "in_progress"
    # Punkt 2 (3.24.0): Der überfällige Punkt steht jetzt im ersten Abschnitt
    # von „In Bearbeitung“, und die Abschnittsüberschrift führt per Doppelklick
    # in die eigene Ansicht.
    # Punkt 5 (3.25.0) stellte die nächste Aufgabe davor; seit 3.33.6 (D14)
    # steht sie in „Heute“, und „Verspätet“ ist wieder der erste Abschnitt.
    zeilen = app.tree.get_children("")
    assert app.OVERDUE_SECTION_ROW_ID in zeilen
    assert app.NEXT_TASK_SECTION_ROW_ID not in zeilen
    assert zeilen.index(app.OVERDUE_SECTION_ROW_ID) == 0
    assert "Verspätet" in app.tree.item(app.OVERDUE_SECTION_ROW_ID, "text")
    app.tree.focus(app.OVERDUE_SECTION_ROW_ID)
    assert app.open_in_progress_source_item() == "break"
    assert app.view_mode == "overdue"
    app.set_in_progress_view()
    # Punkt 1 (3.24.0): Der Eingang ist als Liste weiterhin erreichbar.
    assert app.open_inbox_list() == "break"
    assert app.view_mode == "list"
    assert app.is_inbox_list(app.current_list())
    app.set_in_progress_view()

    # --- Hellblauer Hover ----------------------------------------------
    assert app.theme["hover"] != app.theme["selection"]
    for theme_values in mod.ListApp.THEMES.values():
        assert theme_values["hover"] != theme_values["selection"]
    hover_config = app.tree.tag_configure("hover")
    assert hover_config["background"] == app.theme["hover"]
    # Der Hover setzt ausschliesslich den Hintergrund; Textfarben bleiben.
    assert not str(hover_config["foreground"])
    app.set_active_list(kind_list["id"])
    app.refresh_tree()
    hover_target = app.hover_row_ids(app.tree, long_task["id"])
    assert hover_target[0] == long_task["id"] and len(hover_target) > 1
    app.set_hover_rows(app.tree, hover_target)
    assert "hover" in app.tree.item(long_task["id"], "tags")
    assert all("hover" in app.tree.item(iid, "tags") for iid in hover_target)
    # Eine Fortsetzungszeile fuehrt auf ihren Punkt zurueck.
    assert app.hover_row_ids(app.tree, hover_target[1])[0] == long_task["id"]
    # Der Abstand ueber einer Ueberschrift ist nichts zum Anfassen.
    assert app.hover_row_ids(app.tree, f"{heading['id']}{app.SPACER_IID_MARKER}0") == ()
    app.set_hover_rows(app.tree, ())
    assert "hover" not in app.tree.item(long_task["id"], "tags")
    sidebar_hover_config = app.sidebar_listbox.tag_configure("hover")
    assert sidebar_hover_config["background"] == app.theme["hover"]
    assert app.system_listbox.tag_configure("hover")["background"] == app.theme["hover"]
    app.set_hover_rows(app.sidebar_listbox, (f"list:{kind_list['id']}",))
    assert "hover" in app.sidebar_listbox.item(f"list:{kind_list['id']}", "tags")
    app.set_hover_rows(app.sidebar_listbox, ())

    # --- Erweiterter Anlage-Dialog -------------------------------------
    dialog_result = {
        "text": "Aus dem Dialog",
        "kind": app.ITEM_KIND_LONG,
        "importance": 2,
        "color": "export",
        "due": "2026-12-24",
        "labels": [free_label["id"]],
        "list_id": overdue_list["id"],
    }
    built = app.build_item_from_dialog(dialog_result)
    assert built["text"] == "Aus dem Dialog"
    assert app.item_kind(built) == app.ITEM_KIND_LONG
    assert built["importance"] == 2 and built["color"] == "export"
    assert built["due"] == "2026-12-24"
    assert built["labels"] == [free_label["id"], long_label["id"]]
    assert app.build_item_from_dialog(None) is None

    original_new_item_dialog = app.new_item_dialog
    app.new_item_dialog = lambda *_a, **_k: dict(dialog_result)
    app.set_active_list(kind_list["id"])
    before_target = app.count_items(overdue_list["items"])
    app.add_sibling_item(app.ITEM_KIND_TASK)
    app.new_item_dialog = original_new_item_dialog
    # Eine abweichende Zielliste bekommt den Punkt, nicht die geoeffnete Liste.
    assert app.count_items(overdue_list["items"]) == before_target + 1
    moved_item = overdue_list["items"][-1]
    assert moved_item["text"] == "Aus dem Dialog"
    assert app.is_long_item(moved_item)


    # ------------------------------------------------------------------
    # 2.9.0: verschachtelte Ordner, Langtext-Details, Bildlaufleisten
    # ------------------------------------------------------------------
    app.folders = []
    app.lists = [entry for entry in app.lists if app.is_inbox_list(entry)]
    app.ensure_inbox_list()
    app.trash = []
    nest_top = app.new_folder_object("Oben", None, "accent")
    nest_mid = app.new_folder_object("Mitte", None, "clear", parent_id=nest_top["id"])
    nest_deep = app.new_folder_object("Tief", None, "export", parent_id=nest_mid["id"])
    nest_side = app.new_folder_object("Daneben")
    app.folders.extend([nest_top, nest_mid, nest_deep, nest_side])
    nest_list_top = app.new_list_object("Liste oben", [app.new_item("A")], folder_id=nest_top["id"])
    nest_list_deep = app.new_list_object("Liste tief", [app.new_item("B")], folder_id=nest_deep["id"])
    app.lists.extend([nest_list_top, nest_list_deep])
    app.set_active_list(nest_list_deep["id"], refresh=False)
    app.update_sidebar_list()

    # Ein Ordner kennt seine Ebene, seine Vorfahren und seinen gesamten Inhalt.
    assert app.folder_depth(nest_top["id"]) == 0
    assert app.folder_depth(nest_deep["id"]) == 2
    assert app.folder_ancestor_ids(nest_deep["id"]) == [nest_mid["id"], nest_top["id"]]
    assert app.folder_is_descendant(nest_deep["id"], nest_top["id"])
    assert not app.folder_is_descendant(nest_top["id"], nest_deep["id"])
    assert len(app.get_folder_lists(nest_top["id"])) == 1
    assert len(app.get_folder_lists_recursive(nest_top["id"])) == 2
    assert app.folder_subtree_height(nest_top["id"]) == 2
    assert app.folder_path_titles(nest_deep["id"]) == ["Oben", "Mitte", "Tief"]
    assert app.list_path_title(nest_list_deep) == "Oben › Mitte › Tief › Liste tief"

    # Die Seitenleiste zeichnet den Baum verschachtelt, mit rekursivem Zähler.
    assert app.sidebar_listbox.parent(f"folder:{nest_mid['id']}") == f"folder:{nest_top['id']}"
    assert app.sidebar_listbox.parent(f"folder:{nest_deep['id']}") == f"folder:{nest_mid['id']}"
    assert app.sidebar_listbox.parent(f"list:{nest_list_deep['id']}") == f"folder:{nest_deep['id']}"
    assert app.sidebar_listbox.set(f"folder:{nest_top['id']}", "count") == "(2)"
    assert app.sidebar_listbox.set(f"folder:{nest_deep['id']}", "count") == "(1)"

    # Ein Ordner kommt weder in sich selbst noch in einen eigenen Nachfahren.
    assert app.can_move_folder_into(nest_side["id"], nest_deep["id"])
    assert not app.can_move_folder_into(nest_top["id"], nest_deep["id"])
    assert not app.can_move_folder_into(nest_top["id"], nest_top["id"])
    folders_snapshot = json.dumps(app.folders, sort_keys=True)
    assert app.move_sidebar_folder_into_folder(nest_top["id"], nest_deep["id"]) is False
    assert json.dumps(app.folders, sort_keys=True) == folders_snapshot

    # Die Tiefe ist begrenzt; darüber hinaus wird nichts verschoben.
    level4 = app.new_folder_object("Ebene4", None, None, parent_id=nest_deep["id"])
    level5 = app.new_folder_object("Ebene5", None, None, parent_id=level4["id"])
    app.folders.extend([level4, level5])
    assert app.folder_depth(level5["id"]) == mod.ListApp.MAX_FOLDER_DEPTH - 1
    assert not app.can_move_folder_into(nest_side["id"], level5["id"])
    app.folders = [f for f in app.folders if f["id"] not in (level4["id"], level5["id"])]

    # Verschieben, herauslösen und daneben sortieren.
    assert app.move_sidebar_folder_into_folder(nest_side["id"], nest_mid["id"])
    assert app.folder_parent_id(nest_side["id"]) == nest_mid["id"]
    assert app.move_sidebar_folder_to_end(nest_side["id"])
    assert app.folder_parent_id(nest_side["id"]) is None
    assert app.move_sidebar_folder_relative(nest_side["id"], nest_deep["id"], place="before")
    assert app.folder_parent_id(nest_side["id"]) == nest_mid["id"]
    app.move_sidebar_folder_to_end(nest_side["id"])

    # Ablegezonen: oben davor, Mitte hinein, unten danach.
    root.deiconify()
    root.update()
    app.update_sidebar_list()
    app.sidebar_listbox.see(f"folder:{nest_top['id']}")
    root.update()
    root.update_idletasks()
    zone_bbox = app.sidebar_listbox.bbox(f"folder:{nest_top['id']}")
    assert zone_bbox, "Ordnerzeile ist nicht sichtbar"
    _zx, zone_top, _zw, zone_height = zone_bbox
    assert app.sidebar_drop_zone(f"folder:{nest_top['id']}", zone_top + 1) == "before"
    assert app.sidebar_drop_zone(f"folder:{nest_top['id']}", zone_top + zone_height // 2) == "into"
    assert app.sidebar_drop_zone(f"folder:{nest_top['id']}", zone_top + zone_height - 1) == "after"
    root.withdraw()

    # Tastatur: einrücken legt in den Ordner darüber, ausrücken hebt eine Ebene.
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set(f"folder:{nest_side['id']}")
    app.toggle_sidebar_indent()
    indent_parent = app.folder_parent_id(nest_side["id"])
    assert indent_parent is not None
    # Ausrücken hebt genau eine Ebene an – nicht bis ganz nach oben.
    expected_parent = app.folder_parent_id(indent_parent)
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set(f"folder:{nest_side['id']}")
    app.outdent_selected_sidebar_list()
    assert app.folder_parent_id(nest_side["id"]) == expected_parent
    while app.folder_parent_id(nest_side["id"]) is not None:
        app.move_sidebar_folder_to_end(nest_side["id"])
    assert app.folder_parent_id(nest_side["id"]) is None

    # Alt+Auf/Ab sortiert nur unter Geschwistern und ändert die Ebene nicht.
    inner_before = app.folder_parent_id(nest_mid["id"])
    app.update_sidebar_list()
    app.sidebar_listbox.selection_set(f"folder:{nest_mid['id']}")
    app.move_sidebar_selection(1)
    assert app.folder_parent_id(nest_mid["id"]) == inner_before

    # Auflösen hebt Listen und Unterordner eine Ebene an.
    dissolve = app.new_folder_object("Auflösen", None, None, parent_id=nest_top["id"])
    inside = app.new_folder_object("Innen", None, None, parent_id=dissolve["id"])
    app.folders.extend([dissolve, inside])
    inside_list = app.new_list_object("Innenliste", [], folder_id=dissolve["id"])
    app.lists.append(inside_list)
    app.delete_folder(dissolve["id"])
    assert app.get_folder(dissolve["id"]) is None
    assert app.folder_parent_id(inside["id"]) == nest_top["id"]
    assert inside_list["folder_id"] == nest_top["id"]
    app.folders = [f for f in app.folders if f["id"] != inside["id"]]
    app.lists = [e for e in app.lists if e["id"] != inside_list["id"]]
    app.trash = []

    # Papierkorb: der ganze Zweig geht gemeinsam und kehrt gemeinsam zurück.
    lists_before_trash = len(app.lists)
    folders_before_trash = len(app.folders)
    app._move_folder_to_trash(nest_top["id"])
    assert app.get_folder(nest_top["id"]) is None
    assert app.get_folder(nest_mid["id"]) is None
    assert app.get_folder(nest_deep["id"]) is None
    assert len(app.lists) == lists_before_trash - 2
    assert len([e for e in app.trash if e["kind"] == "folder"]) == 3
    root_trash = next(
        e for e in app.trash if e["kind"] == "folder" and e["folder"]["id"] == nest_top["id"]
    )
    app.restore_trash_entry(root_trash["id"], save=False)
    assert app.folder_parent_id(nest_mid["id"]) == nest_top["id"]
    assert app.folder_parent_id(nest_deep["id"]) == nest_mid["id"]
    assert len(app.lists) == lists_before_trash
    assert len(app.folders) == folders_before_trash
    assert not app.trash

    # Format 9: parent_id wird gespeichert, geprüft und beim Laden bereinigt.
    app.save_items()
    nested_payload = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    assert nested_payload["version"] == 23
    assert all("parent_id" in folder for folder in nested_payload["folders"])
    assert app.validate_backup_schema(nested_payload) == set()
    broken_parent = json.loads(json.dumps(nested_payload))
    for folder in broken_parent["folders"]:
        folder["parent_id"] = "gibt-es-nicht"
    app.normalize_lists_data(broken_parent)
    assert all(folder.get("parent_id") is None for folder in app.folders)
    cyclic = json.loads(json.dumps(nested_payload))
    cyclic_ids = [folder["id"] for folder in cyclic["folders"]]
    cyclic["folders"][0]["parent_id"] = cyclic_ids[1]
    cyclic["folders"][1]["parent_id"] = cyclic_ids[0]
    app.normalize_lists_data(cyclic)
    for folder in app.folders:
        seen_parents = {folder["id"]}
        cursor = folder.get("parent_id")
        while cursor:
            assert cursor not in seen_parents, "Kreis überlebt das Laden"
            seen_parents.add(cursor)
            cursor = app.folder_parent_id(cursor)
    try:
        app.validate_backup_schema(cyclic, portable=True)
        raise AssertionError("Ordnerkreis im Komplettbackup wurde akzeptiert.")
    except ValueError:
        pass
    unknown_parent = json.loads(json.dumps(nested_payload))
    unknown_parent["folders"][0]["parent_id"] = "fehlt"
    try:
        app.validate_backup_schema(unknown_parent, portable=True)
        raise AssertionError("Unbekannter Elternordner wurde akzeptiert.")
    except ValueError:
        pass
    app.lists, _nested_active = app.normalize_lists_data(nested_payload)
    app.ensure_inbox_list()
    app.active_list_id = None
    app.set_active_list(
        next(entry["id"] for entry in app.lists if entry["title"] == "Liste tief"), refresh=False
    )
    app.update_sidebar_list()
    app.refresh_tree()

    # Das Ordnermenü bietet das Verschieben an; die Ordnerübersicht zeigt Unterordner.
    folder_menu_labels = menu_labels(app.build_sidebar_context_menu(("folder", nest_top["id"])))
    assert "Ordner verschieben" in folder_menu_labels, folder_menu_labels
    nested_menu = app.build_sidebar_context_menu(("folder", nest_top["id"]))
    nested_index = next(i for i in range(nested_menu.index("end") + 1)
                        if nested_menu.type(i) == "cascade" and nested_menu.entrycget(i, "label") == "Neu anlegen")
    assert "Neuer Unterordner …" in menu_labels(root.nametowidget(nested_menu.entrycget(nested_index, "menu")))
    app.set_active_folder(nest_top["id"])
    overview_rows = app.tree.get_children("")
    assert any(str(iid).startswith("folder-folder:") for iid in overview_rows), overview_rows
    assert app.folder_folder_id_from_iid(f"folder-folder:{nest_mid['id']}") == nest_mid["id"]
    assert app.folder_folder_id_from_iid(f"folder-list:{nest_list_top['id']}") is None
    app.set_active_list(
        next(entry["id"] for entry in app.lists if entry["title"] == "Liste tief")
    )

    # --- Langtext: eigene Zeilenumbrüche -------------------------------
    assert app.normalize_item_text("Eins\nZwei", app.ITEM_KIND_LONG) == "Eins\nZwei"
    assert app.normalize_item_text("Eins\nZwei", app.ITEM_KIND_TASK) == "Eins Zwei"
    assert app.normalize_item_text("Eins\r\n\n\nZwei  ", app.ITEM_KIND_LONG) == "Eins\nZwei"
    multi = app.new_item("Erste Zeile\nZweite Zeile", kind=app.ITEM_KIND_LONG)
    assert multi["text"] == "Erste Zeile\nZweite Zeile"
    assert app.item_display_text(multi) == "Erste Zeile Zweite Zeile"
    plain_multi = app.new_item("Erste\nZweite")
    assert plain_multi["text"] == "Erste Zweite"
    # Beim Zurückwandeln verschwinden die Umbrüche, statt still zu bleiben.
    app.set_item_kind(multi, app.ITEM_KIND_TASK)
    assert "\n" not in multi["text"]
    app.set_item_kind(multi, app.ITEM_KIND_LONG)
    multi["text"] = "Erste Zeile\nZweite Zeile\nDritte Zeile"

    # Der Umbruch beginnt an jedem eigenen Zeilenumbruch neu.
    broken_lines = app.wrap_long_task_text("Eins.\nZwei.\nDrei.", "1. ", 4000)
    assert broken_lines == ["1. Eins.", broken_lines[1], broken_lines[2]], broken_lines
    assert broken_lines[1].strip() == "Zwei." and broken_lines[2].strip() == "Drei."
    assert len(app.wrap_long_task_text("A\nB\nC\nD\nE\nF\nG", "1. ", 4000)) == app.LONG_TASK_MAX_LINES

    app.items.clear()
    app.items.append(multi)
    app.refresh_tree()
    multi_rows = [app.tree.item(multi["id"], "text")] + [
        app.tree.item(iid, "text")
        for iid in app.tree.get_children("")
        if iid.startswith(f"{multi['id']}{app.CONTINUATION_IID_MARKER}")
    ]
    assert multi_rows[0].startswith("1. Erste Zeile"), multi_rows
    assert any(row.strip().startswith("Zweite Zeile") for row in multi_rows[1:]), multi_rows

    # TXT-Rundlauf erhält den mehrzeiligen Text und die Art.
    multi_export = pathlib.Path(temp_root) / "longtask.txt"
    with open(multi_export, "w", encoding="utf-8") as handle:
        app.write_items_to_txt(handle, app.items, [])
    exported_text = multi_export.read_text(encoding="utf-8")
    assert f"   {app.TXT_TEXT_CONTINUATION} Zweite Zeile" in exported_text, exported_text
    multi_parsed = app.parse_txt_items(exported_text.splitlines(keepends=True))
    assert len(multi_parsed) == 1
    assert app.is_long_item(multi_parsed[0])
    assert multi_parsed[0]["text"] == multi["text"], multi_parsed[0]["text"]

    # --- Bildlaufleisten in den Dialogen --------------------------------
    scrollbar_counts = {}

    def count_dialog_scrollbars(opener, key):
        def close():
            for child in list(root.winfo_children()):
                if isinstance(child, mod.tk.Toplevel):
                    found = []

                    def walk(widget):
                        for kid in widget.winfo_children():
                            if isinstance(kid, mod.ThemedAutoScrollbar):
                                found.append(kid)
                            walk(kid)

                    walk(child)
                    scrollbar_counts[key] = len(found)
                    child.destroy()

        root.after(200, close)
        opener()

    count_dialog_scrollbars(lambda: app.themed_item_details_dialog(multi), "long")
    count_dialog_scrollbars(lambda: app.themed_item_details_dialog(app.new_item("Kurz")), "task")
    count_dialog_scrollbars(lambda: app.edit_folder_details(nest_top["id"]), "folder")
    count_dialog_scrollbars(app.open_label_manager, "labels")
    # Seit 2.11.0 ist die Maske vollstaendig: Das Fenster selbst traegt eine
    # Leiste, dazu Titel, Beschreibung und Anhaenge. Seit 2.12.0 ist die
    # Labelauswahl ein Aufklappfeld und braucht in der Maske keine Leiste mehr.
    # Seit 3.22 kommt die Checkliste dazu und bringt ihre eigene Leiste mit.
    assert scrollbar_counts.get("long") == 5, scrollbar_counts
    # Ein gewöhnlicher Punkt hat ein einzeiliges Titelfeld – eine Leiste weniger.
    assert scrollbar_counts.get("task") == 5, scrollbar_counts
    # Seit 3.7: Beschreibung und die neue Anhangsliste besitzen jeweils eine Leiste.
    assert scrollbar_counts.get("folder") == 2, scrollbar_counts
    assert scrollbar_counts.get("labels") == 1, scrollbar_counts


    # ------------------------------------------------------------------
    # 2.10.0: Label-Chips und verlustfreier TXT-Rundlauf aller Arten
    # ------------------------------------------------------------------
    # Maße nach Vorgabe: 6 Pixel Radius, gleiche Seitenabstände, oben zwei
    # Pixel weniger als unten.
    assert mod.LabelChip.RADIUS == 9  # 3.0.1: runder, naeher am Vorbild des Nutzers
    assert mod.LabelChip.PAD_TOP == mod.LabelChip.PAD_BOTTOM - 2
    assert mod.LabelChip.PAD_X > 0
    chip_width, chip_height = mod.LabelChip.measure("Label", app.LABEL_CHIP_FONT)
    assert chip_width > 2 * mod.LabelChip.PAD_X
    assert chip_height == mod.LabelChip.PAD_TOP + mod.LabelChip.PAD_BOTTOM + (
        chip_height - mod.LabelChip.PAD_TOP - mod.LabelChip.PAD_BOTTOM
    )

    # Farbmischung und Helligkeitssuche.
    assert mod.mix_hex_colors("#102030", "#FFFFFF", 0) == "#102030"
    assert mod.mix_hex_colors("#102030", "#FFFFFF", 1) == "#FFFFFF"
    assert mod.mix_hex_colors("#000000", "#FFFFFF", 0.5) == "#808080"
    assert mod.mix_hex_colors("kein-hex", "#FFFFFF", 0.5) == "#808080"
    assert abs(mod.relative_luminance("#FFFFFF") - 1.0) < 0.001
    assert abs(mod.relative_luminance("#000000")) < 0.001
    tuned = mod.mix_to_luminance("#FF3B30", "#FFFFFF", 0.62)
    assert abs(mod.relative_luminance(tuned) - 0.62) < 0.02, mod.relative_luminance(tuned)

    def chip_contrast(first, second):
        first_luminance = mod.relative_luminance(first)
        second_luminance = mod.relative_luminance(second)
        lighter = max(first_luminance, second_luminance)
        darker = min(first_luminance, second_luminance)
        return (lighter + 0.05) / (darker + 0.05)

    # Jede Palettenfarbe bleibt in beiden Themes lesbar und hebt sich ab.
    chip_theme_before = app.theme_name
    for chip_theme in ("light", "dark"):
        if app.theme_name != chip_theme:
            app.toggle_theme()
        for chip_color in app.LABEL_COLOR_KEYS:
            probe_label = app.new_label_object("Probe", None, chip_color)
            chip_fill, chip_text_color = app.label_chip_colors(probe_label)
            assert chip_contrast(chip_fill, chip_text_color) >= 4.5, (chip_theme, chip_color)
            assert chip_contrast(chip_fill, app.theme["bg"]) >= 1.08, (chip_theme, chip_color)
            # Die Fläche ist nicht die rohe Palettenfarbe.
            assert chip_fill != app.theme[chip_color]
    if app.theme_name != chip_theme_before:
        app.toggle_theme()

    # Viele Labels brechen um, statt seitlich auszulaufen.
    chip_probe = mod.tk.Frame(root, bg=app.theme["bg"])
    many_labels = [app.new_label_object(f"Label {index}", None, "accent") for index in range(12)]
    packed_chips = app.pack_label_chips(chip_probe, many_labels, bg_key="bg", max_width=300)
    assert len(packed_chips) == len(many_labels)
    chip_rows = [child for child in chip_probe.winfo_children() if isinstance(child, mod.tk.Frame)]
    assert len(chip_rows) > 1, len(chip_rows)
    chip_probe.destroy()

    # Alle vier Arten überstehen den TXT-Rundlauf – auch ein einzeiliger
    # Langtext, der keine Fortsetzungszeilen mitbringt.
    kind_roundtrip = [
        app.new_item("Gewöhnliche Aufgabe"),
        app.new_item("Einzeiliger Langtext", kind=app.ITEM_KIND_LONG),
        app.new_item("Mehrzeiliger\nLangtext", kind=app.ITEM_KIND_LONG),
        app.new_item("Zwischenüberschrift", kind=app.ITEM_KIND_HEADING),
        app.new_item("Gruppe", kind=app.ITEM_KIND_GROUP, children=[app.new_item("Kind")]),
        app.new_item("Wichtig und erledigt", importance=3, done=True),
    ]
    kind_file = pathlib.Path(temp_root) / "arten.txt"
    with open(kind_file, "w", encoding="utf-8") as handle:
        app.write_items_to_txt(handle, kind_roundtrip, [])
    kind_text = kind_file.read_text(encoding="utf-8")
    assert app.LONG_MARKER.strip() in kind_text, kind_text
    kind_back = app.parse_txt_items(kind_text.splitlines(keepends=True))
    assert [(entry["text"].splitlines()[0], app.item_kind(entry)) for entry in kind_back] == [
        ("Gewöhnliche Aufgabe", app.ITEM_KIND_TASK),
        ("Einzeiliger Langtext", app.ITEM_KIND_LONG),
        ("Mehrzeiliger", app.ITEM_KIND_LONG),
        ("Zwischenüberschrift", app.ITEM_KIND_HEADING),
        ("Gruppe", app.ITEM_KIND_GROUP),
        ("Wichtig und erledigt", app.ITEM_KIND_TASK),
    ]
    kind_flagged = next(entry for entry in kind_back if entry["text"].startswith("Wichtig"))
    assert kind_flagged["importance"] == 3 and kind_flagged["done"] is True

    # ------------------------------------------------------------------
    # 2.12.0: Labelauswahl als Aufklappfeld, Kalenderknopf, Kopfbereich
    # ------------------------------------------------------------------
    for extra_name, extra_color in (("Kunde", "accent"), ("Intern", "flag")):
        app.labels.append(app.new_label_object(extra_name, None, extra_color))
    picker_labels = [label for label in app.labels if not app.is_system_label(label)]
    assert len(picker_labels) >= 2, picker_labels

    # Die Labelauswahl belegt geschlossen eine Zeile statt einer Chipflaeche.
    dropdown_host = mod.tk.Frame(root)
    dropdown = mod.LabelDropdown(
        dropdown_host, app, picker_labels, selected_ids=[picker_labels[1]["id"]]
    )
    root.update_idletasks()
    assert dropdown.read() == [picker_labels[1]["id"]], dropdown.read()
    assert picker_labels[1]["name"] in dropdown.summary_label.cget("text")
    # Die Rueckgabe folgt der Reihenfolge der Labelverwaltung, nicht der
    # Klickreihenfolge – sonst haengt die gespeicherte Reihenfolge davon ab,
    # in welcher Folge jemand angeklickt hat.
    dropdown.selected_ids = [picker_labels[1]["id"], picker_labels[0]["id"]]
    assert dropdown.read() == [picker_labels[0]["id"], picker_labels[1]["id"]], dropdown.read()
    # Eine Zuordnung auf ein geloeschtes Label faellt beim Aufbau heraus.
    stale_dropdown = mod.LabelDropdown(
        dropdown_host, app, picker_labels, selected_ids=["dieses-label-gibt-es-nicht"]
    )
    assert stale_dropdown.read() == []
    assert stale_dropdown.summary_label.cget("text") == stale_dropdown.empty_text
    dropdown_host.destroy()

    # Faelligkeit: in der Maske Felder plus Kalenderknopf, im Kalenderfenster
    # der vollstaendige Monatskalender.
    due_host = mod.tk.Frame(root)
    compact_due = mod.DueField(due_host, app, due="2026-05-04", due_time="09:30", compact=True)
    root.update_idletasks()
    assert compact_due.month_label is None and compact_due.grid_frame is None
    assert compact_due.calendar_button is not None
    assert compact_due.read() == (("2026-05-04", "09:30"), None), compact_due.read()
    # set_due laeuft ohne eingebetteten Kalender fehlerfrei durch.
    compact_due.set_due(None)
    assert compact_due.read() == ((None, None), None), compact_due.read()
    full_due = mod.DueField(due_host, app, due="2026-05-04")
    root.update_idletasks()
    assert full_due.month_label is not None and full_due.grid_frame is not None
    assert full_due.calendar_button is None
    due_host.destroy()

    # U10: Labels und Fortschritt stehen in der Unterzeile und halten
    # ihre Hoehe, damit der Kopf beim Listenwechsel nicht springt.
    assert app.stats_label.master is app.header_meta
    assert app.page_labels_frame.master is app.header_meta
    header_list = app.current_list()
    saved_header_labels = list(header_list.get("labels") or [])
    header_list["labels"] = [picker_labels[0]["id"]]
    app.update_page_labels()
    root.update_idletasks()
    height_with_labels = app.page_labels_frame.winfo_reqheight()
    header_list["labels"] = []
    app.update_page_labels()
    root.update_idletasks()
    height_without_labels = app.page_labels_frame.winfo_reqheight()
    assert height_with_labels == height_without_labels, (height_with_labels, height_without_labels)
    # Die Unterzeile liegt unter dem Titel; die Kennzahlen konkurrieren nicht
    # mehr mit dessen Breite. Der Labelwechsel behält oben exakt seine Höhe.
    header_list["labels"] = [picker_labels[0]["id"]]
    app.update_page_labels()
    root.update_idletasks()
    assert app.header_meta.master is app.subtitle_row
    assert app.header_meta.winfo_height() <= app.subtitle_row.winfo_height()
    assert app.header_meta.winfo_rooty() >= app.title_row.winfo_rooty() + app.title_row.winfo_height()
    header_list["labels"] = saved_header_labels
    app.update_page_labels()

    # Eine Zeile bleibt eine Zeile: Was nicht mehr hineinpasst, wird gezaehlt.
    chip_host = mod.tk.Frame(root)
    many_labels = (picker_labels * 6)[:12]
    packed_chips = app.pack_label_chips(
        chip_host, many_labels, bg_key="bg", max_width=120, max_rows=1, anchor="e"
    )
    root.update_idletasks()
    assert len(packed_chips) < len(many_labels), len(packed_chips)
    assert len(chip_host.winfo_children()) == 1, chip_host.winfo_children()
    chip_host.destroy()

    # Suchzeile und Filter stehen ueber der Liste, nicht ueber der vollen
    # Fensterbreite – dadurch beginnt die Seitenleiste eine Zeile weiter oben.
    assert app.search_frame.master is app.content_frame
    assert app.sidebar_shell.master is app.main_area
    assert app.content_frame.master is app.main_area
    assert app.hide_done_box_border.master is app.search_frame
    assert app.clear_search_button.master is app.search_frame

    # 3.0.2: Ein Drop mitten auf eine Gruppe legt den Punkt hinein, ein Drop an
    # den Rand sortiert daneben ein. Vorher ging Hineinlegen nur mit Shift.
    drop_group = app.new_item("Zielgruppe", kind=app.ITEM_KIND_GROUP)
    drop_task = app.new_item("Wanderpunkt")
    app.items.extend([drop_group, drop_task])
    app.refresh_tree()
    root.deiconify()
    root.update()

    class DropEvent:
        """Zeigerposition wie bei einem echten Zug - auch in Bildschirmkoordinaten,
        weil die Zielerkennung damit prueft, ueber welchem Widget der Zeiger steht."""

        def __init__(self, tree, x, y, state=0):
            self.x, self.y, self.state = x, y, state
            self.x_root = tree.winfo_rootx() + x
            self.y_root = tree.winfo_rooty() + y
            self.num = 1

    def drop_on_group(fraction):
        """Simuliert einen Zug des Punkts auf die Gruppe, relativ zur Zeilenhoehe."""
        app.refresh_tree()
        root.update_idletasks()
        bbox = app.tree.bbox(drop_group["id"])
        assert bbox, "Gruppenzeile nicht sichtbar"
        _x, y, _w, h = bbox
        app.drag_start_id = drop_task["id"]
        app.drag_item_ids = [drop_task["id"]]
        app.drag_has_moved = True
        app.tree.selection_set(drop_task["id"])
        app.on_drag_end(DropEvent(app.tree, 60, int(y + h * fraction)))

    before_total = app.count_items(app.items)
    drop_on_group(0.5)
    inside = [child["id"] for child in drop_group.get("children", [])]
    assert drop_task["id"] in inside, "Ein Drop auf die Mitte muss hineinlegen."
    # Der Bestandswaechter zaehlt mit: Kein Punkt darf dabei verschwinden.
    assert app.count_items(app.items) == before_total, app.count_items(app.items)
    # Ein zweiter Punkt, diesmal an den oberen Rand der Gruppenzeile: Er soll
    # daneben einsortiert werden, nicht hinein.
    edge_task = app.new_item("Randpunkt")
    app.items.append(edge_task)
    drop_task = edge_task
    drop_on_group(0.05)
    assert edge_task["id"] not in [child["id"] for child in drop_group.get("children", [])], (
        "Ein Drop an den Rand darf nicht hineinlegen."
    )
    assert any(entry["id"] == edge_task["id"] for entry in app.items), (
        "Der Punkt muss auf der obersten Ebene geblieben sein."
    )
    root.withdraw()

    # 3.0.1: Gruppieren steht auf der obersten Menueebene, nicht mehr unter „Art“.
    group_item = app.new_item("Gruppierbar")
    app.items.append(group_item)
    app.refresh_tree()
    app.tree.selection_set(group_item["id"])
    item_menu_labels = menu_labels(app.build_item_context_menu())
    assert any(label.startswith("Auswahl gruppieren") for label in item_menu_labels), item_menu_labels
    # „In Gruppe umwandeln“ hiess fast gleich und tat das Gegenteil - jeder
    # markierte Punkt wurde zu einer eigenen leeren Gruppe.
    assert not any("In Gruppe umwandeln" in label for label in item_menu_labels)

    # 3.0: Umbenennen an Ort und Stelle, aber nicht ueber dem Klappdreieck.
    rename_folder = app.new_folder_object("Umbenennen-Test")
    app.folders.append(rename_folder)
    app.update_sidebar_list()
    root.update_idletasks()
    folder_iid = app.find_sidebar_iid(("folder", rename_folder["id"]))
    assert folder_iid, app.sidebar_iid_to_row

    class FakeRelease:
        def __init__(self, widget, x=40, y=10, state=0):
            self.widget, self.x, self.y, self.state = widget, x, y, state

    def try_rename_click(element_name):
        """Simuliert das Loslassen der Maus ueber dem genannten Element."""
        original = app.sidebar_listbox.identify_element
        original_row = app.sidebar_listbox.identify_row
        app.sidebar_listbox.identify_element = lambda x, y: element_name
        app.sidebar_listbox.identify_row = lambda y: folder_iid
        app.sidebar_listbox.selection_set(folder_iid)
        app._sidebar_preselected = (folder_iid,)
        app._sidebar_release_moved = False
        app._cancel_sidebar_rename_timer()
        try:
            app.on_sidebar_release_for_rename(FakeRelease(app.sidebar_listbox))
            return getattr(app, "_sidebar_rename_timer", None) is not None
        finally:
            app.sidebar_listbox.identify_element = original
            app.sidebar_listbox.identify_row = original_row
            app._cancel_sidebar_rename_timer()

    assert try_rename_click("Treeitem.text") is True, "Klick auf den Namen muss umbenennen koennen."
    assert try_rename_click("Treeitem.indicator") is False, (
        "Klick auf das Klappdreieck darf nicht umbenennen."
    )

    # Das Eingabefeld erscheint an Ort und Stelle und uebernimmt den Namen.
    app.sidebar_listbox.selection_set(folder_iid)
    app.begin_sidebar_rename(folder_iid)
    root.update_idletasks()
    rename_state = app._sidebar_rename
    assert rename_state is not None and rename_state["row"] == ("folder", rename_folder["id"])
    rename_state["entry"].delete(0, mod.tk.END)
    rename_state["entry"].insert(0, "Neuer Ordnername")
    app.finish_sidebar_rename(commit=True)
    assert app.get_folder(rename_folder["id"])["title"] == "Neuer Ordnername"
    # Ein leerer Name wird verworfen - eine Liste ohne Titel waere nicht mehr auffindbar.
    app.begin_sidebar_rename(app.find_sidebar_iid(("folder", rename_folder["id"])))
    app._sidebar_rename["entry"].delete(0, mod.tk.END)
    app.finish_sidebar_rename(commit=True)
    assert app.get_folder(rename_folder["id"])["title"] == "Neuer Ordnername"
    # Der Eingang traegt einen Systemnamen und laesst sich nicht umbenennen.
    assert app.sidebar_rename_row(inbox_iid) is None

    # ------------------------------------------------------------------
    # 3.1.0: gemeinsamer Rahmen fuer Aenderungen, gemeinsamer modaler Weg
    # ------------------------------------------------------------------
    # Der Rahmen muss beides koennen: einen wirkungslosen Rueckgaengig-Schritt
    # verwerfen und einen wirksamen behalten. Genau diese Unterscheidung stand
    # bis 3.0.2 an 36 Stellen einzeln im Quelltext.
    app.view_mode = "list"
    app.items.clear()
    app.items.append(app.new_item("Rahmen A"))
    app.items.append(app.new_item("Rahmen B"))
    app.save_items()
    app.refresh_tree()
    frame_ids = [entry["id"] for entry in app.items[-2:]]

    undo_depth = len(app.undo_stack)
    with app.item_change(frame_ids) as change:
        del change  # nichts gemeldet: die Aktion blieb wirkungslos
    assert len(app.undo_stack) == undo_depth, (
        "Eine wirkungslose Aktion darf keinen Rueckgaengig-Schritt hinterlassen."
    )

    with app.item_change(frame_ids) as change:
        app.find_item(frame_ids[0])[0]["text"] = "Rahmen A geaendert"
        change.mark()
    assert len(app.undo_stack) == min(undo_depth + 1, app.MAX_UNDO_STEPS)
    app.undo_last_change()
    assert app.find_item(frame_ids[0])[0]["text"] == "Rahmen A"

    # Ist der Stapel voll, darf eine wirkungslose Aktion den aeltesten Schritt
    # nicht verdraengen. Bis 3.0.2 kuerzte schon das Anlegen des Schnappschusses.
    app.undo_stack.clear()
    for index in range(app.MAX_UNDO_STEPS):
        app.find_item(frame_ids[0])[0]["text"] = f"Stufe {index}"
        app.snapshot_undo()
    assert len(app.undo_stack) == app.MAX_UNDO_STEPS
    oldest = app.undo_stack[0]
    with app.item_change(frame_ids) as change:
        del change
    assert app.undo_stack[0] is oldest, (
        "Eine wirkungslose Aktion darf den aeltesten Rueckgaengig-Schritt nicht kosten."
    )
    assert len(app.undo_stack) == app.MAX_UNDO_STEPS
    app.undo_stack.clear()
    app.find_item(frame_ids[0])[0]["text"] = "Rahmen A"

    # focus="first" richtet den Blick auf den ersten statt den letzten Punkt.
    with app.item_change(frame_ids, focus="first") as change:
        change.mark()
    assert app.tree.focus() == frame_ids[0]
    app.undo_last_change()

    # Der Seitenleisten-Rahmen verhaelt sich gleich.
    sidebar_depth = len(app.undo_stack)
    with app.sidebar_change() as change:
        del change
    assert len(app.undo_stack) == sidebar_depth

    # Ohne Auswahl liefert der gemeinsame Vorfilter None statt einer leeren Liste.
    app.clear_tree_selection()
    assert app.selected_items_for_change(warn=False) is None
    app.tree.selection_set(frame_ids[0])
    assert app.selected_items_for_change(warn=False) == [frame_ids[0]]

    # Ein Unterpunkt kehrt hinter sein Elternteil zurueck - der gemeinsame Kern
    # von "Ausruecken" und der Tab-Umschaltung.
    app.clear_tree_selection()
    app.tree.selection_set(frame_ids[1])
    app.tree.focus(frame_ids[1])
    app.indent_selected()
    assert app.find_item(frame_ids[1])[3] is not None, "Einruecken muss ein Elternteil setzen."
    app.tree.selection_set(frame_ids[1])
    app.tree.focus(frame_ids[1])
    app.outdent_selected()
    assert app.find_item(frame_ids[1])[3] is None, "Ausruecken muss das Elternteil loesen."

    # Der modale Weg gibt den Griff an das aufrufende Fenster zurueck. Ohne das
    # blieb eine geoeffnete Maske sichtbar, nahm aber keine Eingabe mehr an -
    # das ist der gemeldete "haengt sich auf"-Fall.
    outer = mod.tk.Toplevel(root)
    outer.withdraw()
    outer.grab_set()
    inner = mod.tk.Toplevel(root)
    inner.withdraw()
    inner.after(30, inner.destroy)
    app.run_modal(inner)
    assert outer.grab_status(), (
        "Nach einem Unterdialog muss das aufrufende Fenster seinen Griff zurueckbekommen."
    )
    outer.grab_release()
    outer.destroy()

    app.items.clear()
    app.save_items()
    app.refresh_tree()

    # ------------------------------------------------------------------
    # 3.2.0: mitgelieferte Beispieldaten und Symbole aus einer Tabelle
    # ------------------------------------------------------------------
    # Die Beispieldatei liegt im Repository und muss jederzeit einlesbar sein.
    # Sie durchlaeuft hier denselben Weg wie ein echter Import: Archivpruefung,
    # Schemapruefung, Normalisierung.
    # 3.25.0: Der Dateiname wird ohne Rücksicht auf Groß- und Kleinschreibung
    # gesucht. Unter macOS und Windows sind „Glide_Beispieldaten" und
    # „glide_beispieldaten" dieselbe Datei, unter Linux nicht – die Suite war
    # auf einer Vorabumgebung deshalb nie grün zu bekommen, ohne eine zweite
    # Kopie anzulegen, die auf den Zielplattformen die erste überschreibt.
    beispiel_ordner = REPOSITORY_ROOT / "tests" / "fixtures" / "beispiele"
    beispiel_pfad = next(
        (pfad for pfad in sorted(beispiel_ordner.glob("*.glidebackup"))
         if pfad.name.lower() == "glide_beispieldaten.glidebackup"),
        beispiel_ordner / "glide_beispieldaten.glidebackup",
    )
    assert beispiel_pfad.is_file(), "Die Beispieldatei fehlt im Repository."
    with zipfile.ZipFile(beispiel_pfad, "r") as beispiel_archiv:
        app.inspect_backup_archive(beispiel_archiv)
        beispiel_daten = json.loads(beispiel_archiv.read("data.json").decode("utf-8"))
    app.validate_backup_schema(beispiel_daten)
    assert beispiel_daten["version"] == app.DATA_SCHEMA_VERSION

    beispiel_previous = (app.folders, app.labels, app.trash)
    try:
        beispiel_listen, _beispiel_aktiv = app.normalize_lists_data(beispiel_daten)
        beispiel_labels = list(app.labels)
        beispiel_papierkorb = app.normalize_trash_data(beispiel_daten.get("trash"))
    finally:
        app.folders, app.labels, app.trash = beispiel_previous

    # Umfang: Die Datei soll die Anwendung zeigen, nicht nur laden.
    assert len(beispiel_listen) >= 10, len(beispiel_listen)
    assert len(beispiel_daten["folders"]) >= 5
    assert len(beispiel_papierkorb) >= 3
    # Verschachtelte Ordner sind Teil des Nachweises.
    assert any(folder.get("parent_id") for folder in beispiel_daten["folders"])

    beispiel_arten = {}
    for beispiel_liste in beispiel_listen:
        for beispiel_punkt in app.walk_items(beispiel_liste.get("items", [])):
            art = app.item_kind(beispiel_punkt)
            beispiel_arten[art] = beispiel_arten.get(art, 0) + 1
    # Jede Art kommt vor - sonst zeigt die Datei nicht, was die App kann.
    for art in (app.ITEM_KIND_TASK, app.ITEM_KIND_GROUP,
                app.ITEM_KIND_LONG, app.ITEM_KIND_HEADING):
        assert beispiel_arten.get(art, 0) > 0, art
    assert beispiel_arten[app.ITEM_KIND_LONG] >= 10, beispiel_arten
    assert sum(beispiel_arten.values()) >= 120, beispiel_arten

    # Kein Punkt zeigt auf ein Label, das es nicht gibt.
    beispiel_label_ids = {eintrag["id"] for eintrag in beispiel_labels}
    for beispiel_liste in beispiel_listen:
        for beispiel_punkt in app.walk_items(beispiel_liste.get("items", [])):
            for label_id in beispiel_punkt.get("labels", []):
                assert label_id in beispiel_label_ids, label_id
    # Alle sieben Palettenfarben sind vertreten.
    assert {eintrag["color"] for eintrag in beispiel_labels} >= set(app.LABEL_COLOR_KEYS)
    # Mindestens eine Notiz ist wirklich mehrzeilig.
    assert any(
        "\n" in beispiel_punkt["text"]
        for beispiel_liste in beispiel_listen
        for beispiel_punkt in app.walk_items(beispiel_liste.get("items", []))
        if app.item_kind(beispiel_punkt) == app.ITEM_KIND_LONG
    )

    # Die Vorschau enthält jetzt auch echte Anhänge auf allen drei Ebenen.
    beispiel_bestand = {entry["id"] for entry in app.lists}
    assert app.import_full_backup(additive=True, path=str(beispiel_pfad))
    beispiel_neu = [entry for entry in app.lists if entry["id"] not in beispiel_bestand]
    assert len(beispiel_neu) >= 10
    anhangseigner = list(app.attachment_owners(beispiel_neu, folders=app.folders))
    assert sum(len(owner.get("attachments", [])) for owner in anhangseigner) >= 3
    for owner in anhangseigner:
        for attachment in owner.get("attachments", []):
            assert pathlib.Path(app.resolve_attachment_path(attachment)).is_file()
    app.undo_last_change()
    assert {entry["id"] for entry in app.lists} == beispiel_bestand

    # Releaseplanung: drei Arbeitslisten reisen gemeinsam durch einen echten
    # Komplettimport. Getrennte Backups würden einander beim Laden ersetzen.
    release_path = REPOSITORY_ROOT / f"tests/fixtures/beispiele/glide_releaseplanung_{mod.APP_VERSION}.glidebackup"
    assert release_path.is_file(), "Die Releaseplanung fehlt."
    with zipfile.ZipFile(release_path) as release_archive:
        app.inspect_backup_archive(release_archive)
        release_data = json.loads(release_archive.read("data.json"))
    app.validate_backup_schema(release_data, portable=True)
    assert release_data["version"] == 23
    assert release_data["app_version"] == mod.APP_VERSION
    release_previous = (app.folders, app.labels, app.trash)
    try:
        release_lists, release_active = app.normalize_lists_data(release_data)
        release_trash = app.normalize_trash_data(release_data.get("trash"))
        release_labels = {label["id"]: label for label in app.labels}
        assert not release_trash
        assert len(app.folders) == 1
        assert app.folders[0]["title"] == f"Releaseplanung {mod.APP_VERSION}"
        work_lists = [entry for entry in release_lists if not app.is_inbox_list(entry)]
        assert [entry["title"] for entry in work_lists] == [
            "Unterlagen & Assets", "Vermarktungsstrategie", "Feature-Übersicht",
        ]
        assert len(release_lists) == 4
        assert release_active == work_lists[0]["id"]
        release_items = [item for entry in release_lists for item in app.walk_items(entry["items"])]
        assert len(release_items) >= 100
        assert {app.item_kind(item) for item in release_items} == {
            app.ITEM_KIND_TASK, app.ITEM_KIND_GROUP, app.ITEM_KIND_LONG, app.ITEM_KIND_HEADING,
        }
        for entry in release_lists + app.folders + release_items:
            assert set(entry.get("labels", [])).issubset(release_labels)
        for item in release_items:
            assert len(item.get("labels", [])) <= app.MAX_LABELS_PER_ITEM
            if item.get("due"):
                assert "Planungsvorschlag:" in item["description"]
                assert "Annahme" in [release_labels[key]["name"] for key in item["labels"]]
            if "https://" in item.get("description", ""):
                assert "Abrufdatum: 2026-09-04" in item["description"]
        # Keine abgehakten Freigaben oder erfundene erledigte Releasearbeiten.
        assert not any(item["done"] for item in release_items)
        expected_release_ids = {item["id"] for item in release_items}
    finally:
        app.folders, app.labels, app.trash = release_previous

    release_messages = []
    release_dialogs = (mod.filedialog.askopenfilename, mod.ListApp.ask_yes_no,
                       mod.ListApp.show_info, mod.ListApp.show_error)
    try:
        mod.filedialog.askopenfilename = lambda **kwargs: str(release_path)
        mod.ListApp.ask_yes_no = staticmethod(lambda *args, **kwargs: True)
        mod.ListApp.show_info = staticmethod(lambda *args, **kwargs: release_messages.append(("ok", args)))
        mod.ListApp.show_error = staticmethod(lambda *args, **kwargs: release_messages.append(("error", args)))
        app.import_full_backup()
    finally:
        (mod.filedialog.askopenfilename, mod.ListApp.ask_yes_no,
         mod.ListApp.show_info, mod.ListApp.show_error) = release_dialogs
    assert [kind for kind, _ in release_messages] == ["ok"], release_messages
    assert app.app_title == "Unterlagen & Assets"
    assert app.current_list()["title"] == "Unterlagen & Assets"
    assert {item["id"] for entry in app.lists for item in app.walk_items(entry["items"])} == expected_release_ids
    # Auch der geschriebene Speicherstand muss die Titel und IDs erhalten.
    release_saved = json.loads(pathlib.Path(mod.SAVE_FILE).read_text(encoding="utf-8"))
    assert [entry["title"] for entry in release_saved["lists"]] == [entry["title"] for entry in app.lists]
    assert {item["id"] for entry in release_saved["lists"] for item in app.walk_items(entry["items"])} == expected_release_ids

    # Symbole: ausschliesslich Textzeichen, keine Emoji mehr. Ein Emoji faellt
    # ueber seinen Codepunkt auf - alles ab U+1F000 ist Bildzeichen.
    for symbol_name, symbol in app.ICONS.items():
        assert symbol, symbol_name
        assert "\uFE0F" not in symbol
        assert all(ord(char) < 0x1F000 for char in symbol) or (symbol_name == "trash" and symbol == "\U0001F5D1")
    assert app.ICONS["attachment"] and app.ICONS["attachment"] != app.ICONS["remove"]
    assert app.DUE_COLUMN_ICON == app.ICONS["calendar"]
    assert app.LABEL_COLUMN_ICON == app.ICONS["labels"]

    app.cancel_pending_callbacks()
    assert app._autosave_id is None
    close_test_app(app)
    # Strikte Backupprüfung weist fremde oder unsichere Dokumente ab.
    for invalid in ({}, {"version": 4, "folders": [], "lists": "falsch"}):
        try:
            app.validate_backup_schema(invalid)
            raise AssertionError("Ungültiges Schema wurde akzeptiert.")
        except ValueError:
            pass
    for unsafe_storage in (
        "attachments/../settings.json",
        "attachments\\evil.txt",
        "attachments/a.txt:stream",
        "C:/evil.txt",
    ):
        try:
            app.validate_attachment_storage(unsafe_storage)
            raise AssertionError(f"Unsicherer Pfad wurde akzeptiert: {unsafe_storage}")
        except ValueError:
            pass

    malicious_archive = pathlib.Path(temp_root) / "unsicher.glidebackup"
    with zipfile.ZipFile(malicious_archive, "w") as archive:
        archive.writestr("data.json", "{}")
        archive.writestr("attachments/../settings.json", "nicht erlaubt")
    with zipfile.ZipFile(malicious_archive, "r") as archive:
        try:
            app.inspect_backup_archive(archive)
            raise AssertionError("Pfad-Traversal im ZIP wurde akzeptiert.")
        except ValueError:
            pass

    txt_lines = [
        "Testliste\n",
        "==============================\n",
        "[Seitennotiz]\n",
        "Eine freie Notiz\n",
        "[/Seitennotiz]\n",
        "1. Aufgabe mit Details\n",
        "   Beschreibung: erste Zeile\n",
        "   Beschreibung: zweite Zeile\n",
        "   Fällig: 31.08.2026\n",
    ]
    parsed_txt = app.parse_txt_items(txt_lines)
    assert parsed_txt[0]["description"] == "erste Zeile\nzweite Zeile"
    assert parsed_txt[0]["due"] == "2026-08-31"
    assert app.extract_txt_note(txt_lines) == "Eine freie Notiz"
    assert app.safe_csv_cell("=1+1").startswith("'")
    assert app.safe_csv_cell("normal") == "normal"

    # Eine in 2.11.0 gespeicherte Einstellung "Nur erledigte Punkte" faellt auf
    # "alle" zurueck. Sonst bliebe ein Filterzustand stehen, den kein Schalter
    # mehr abstellen kann.
    pathlib.Path(mod.SETTINGS_FILE).write_text(
        json.dumps({"theme": "dark", "filter_mode": "done"}, ensure_ascii=False),
        encoding="utf-8",
    )
    legacy_root = mod.tk.Tk()
    legacy_root.withdraw()
    legacy_app = mod.ListApp(legacy_root)
    legacy_root.update_idletasks()
    assert legacy_app.get_filter_mode() == "all", legacy_app.get_filter_mode()
    assert legacy_app.hide_done_var.get() is False
    assert not hasattr(legacy_app, "show_done_only_var")
    close_test_app(legacy_app)

    print(
        f"Glide v{mod.APP_VERSION} Kern-, Backup-, UI-, Ordner-, Label-, Chip-, Art-, Papierkorb- "
        "und Migrationstests: OK"
    )
