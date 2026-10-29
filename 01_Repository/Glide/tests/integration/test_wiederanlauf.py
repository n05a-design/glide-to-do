"""Echter Start, Freigabe, Undo und Restore mit ausschließlich künstlichen Daten."""
import argparse
import copy
from contextlib import ExitStack
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import traceback
from unittest.mock import patch
import zipfile
import zlib

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests/integration"))
from test_uiux_paket import Lauf, knoepfe, knopf_befunde
from test_sicherungszentrale import visit

CAPTURE_DIR = None


def screenshot(lauf, window, name):
    """Nur das eigene Tk-Fenster per vorhandenem PrintWindow-Helfer abbilden."""
    if CAPTURE_DIR is None or os.name != "nt":
        return None
    sys.path.insert(0, str(REPO / "tests/tools"))
    from releasedaten import save_windows_screenshot
    ready = lauf.mod.tk.BooleanVar(master=window, value=False)
    window.after(200, lambda: ready.set(True))
    window.wait_variable(ready)
    window.update()
    path = CAPTURE_DIR / (name + ".png")
    save_windows_screenshot(window, path)
    data = path.read_bytes()
    width, height = struct.unpack(">II", data[16:24])
    compressed = bytearray()
    offset = 8
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        if data[offset + 4:offset + 8] == b"IDAT":
            compressed.extend(data[offset + 8:offset + 8 + length])
        offset += length + 12
    pixels = zlib.decompress(compressed)
    colors = set()
    stride = width * 3 + 1
    for row in range(height):
        line = pixels[row * stride + 1:(row + 1) * stride]
        colors.update(line[index:index + 3] for index in range(0, len(line), 3))
        if len(colors) > 256:
            break
    if width < 200 or height < 200 or len(colors) < 10:
        raise ValueError("PrintWindow-Aufnahme ist leer oder hat unzureichende Bilddaten")
    return {"file": path.name, "sha256": hashlib.sha256(data).hexdigest(),
            "width": width, "height": height, "method": "PrintWindow; ausschließlich eigenes Tk-Fenster"}


def setup_task(lauf):
    app = lauf.app
    item = app.new_item("Wiederanlaufprobe – Original erhalten")
    app.items.append(item)
    assert app.save_items()
    return item["id"]


def stopped_session(lauf):
    """Beendete Altsitzung simulieren, ohne den aktuellen Prozess zu töten."""
    marker = lauf.app._recovery_guard.marker_path
    lauf.ende()
    record = json.loads(marker.read_text(encoding="utf-8"))
    record.update(state="running", pid=2147483647)
    record.pop("finished_at", None)
    marker.write_text(json.dumps(record), encoding="utf-8")
    return marker


def button(dialog, mod, text):
    label = mod.RoundedButton.action_text(text)
    return next(b for b in knoepfe(dialog, mod.RoundedButton) if b.text == label)


def fall_sauber(lauf):
    item_id = setup_task(lauf)
    marker = lauf.app._recovery_guard.marker_path
    lauf.app.on_close()
    assert json.loads(marker.read_text(encoding="utf-8"))["state"] == "clean"
    lauf.start()
    app = lauf.app
    assert not app._data_read_only and app._recovery_assessment.writable
    assert any(item["id"] == item_id for entry in app.lists for item in entry["items"])
    return "Echtes on_close vermerkt clean; Neustart lädt dieselben IDs ohne Wiederanlaufsperre"


def fall_freigabe(lauf):
    identity = setup_task(lauf)
    marker = stopped_session(lauf)
    source = Path(lauf.mod.SAVE_FILE)
    original, old_marker = source.read_bytes(), marker.read_bytes()
    lauf.start()
    app, mod = lauf.app, lauf.mod
    assert app._data_read_only and app._read_only_reason == "recovery"
    assert app._recovery_assessment.needs_recovery
    assert app.save_items(show_error=False) is False
    assert source.read_bytes() == original and marker.read_bytes() == old_marker
    with patch.object(app, "ask_yes_no", return_value=False):
        assert app.resume_recovery_session() is False
    assert source.read_bytes() == original and marker.read_bytes() == old_marker

    with patch.object(app, "ask_yes_no", return_value=True):
        visit(lauf, "Speicherstatus", app.show_storage_status,
              lambda dialog: button(dialog, mod, "Bestand freigeben").command())
    assert not app._data_read_only
    assert source.read_bytes() == original
    assert Path(app._recovery_assessment.preserved_path).read_bytes() == original
    entry = next(entry for entry in app.lists if any(i["id"] == identity for i in entry["items"]))
    app.set_active_list(entry["id"])
    item = next(item for item in app.items if item["id"] == identity)
    original_text = item["text"]
    with app.item_change([identity]) as change:
        item["text"] = "Nach Freigabe geändert"
        change.mark(identity)
    assert b"Nach Freigabe" in source.read_bytes()
    app.undo_last_change()
    assert next(item for item in app.items if item["id"] == identity)["text"] == original_text
    assert app.save_items()
    assert not lauf.errors, lauf.errors
    return "Schreibschutz und Abbruch erhalten Original; echte Freigabe sichert bytegleich, Ändern/Undo/Sofortspeicherung funktionieren"


def fall_fehler(lauf):
    setup_task(lauf)
    marker = stopped_session(lauf)
    source = Path(lauf.mod.SAVE_FILE)
    original, old_marker = source.read_bytes(), marker.read_bytes()
    lauf.start()
    app = lauf.app
    with patch.object(app, "ask_yes_no", return_value=True), patch.object(
            app._recovery_guard, "preserve_original", side_effect=PermissionError("Vorsicherung verweigert")):
        assert app.resume_recovery_session() is False
    assert app._data_read_only and source.read_bytes() == original and marker.read_bytes() == old_marker
    assert app._recovery_assessment.needs_recovery, "Fehlgeschlagene Kopie muss erneut prüfbar bleiben"
    assert len(lauf.errors) == 1
    lauf.errors.clear()
    payload = json.loads(original)
    payload["lists"][0]["title"] = "Nach Vorschau verändert"
    source.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    changed = source.read_bytes()
    with patch.object(app, "ask_yes_no", return_value=True):
        assert app.resume_recovery_session() is False
    assert app._data_read_only and source.read_bytes() == changed and marker.read_bytes() == old_marker
    assert len(lauf.errors) == 1
    lauf.errors.clear()
    return "Kopierfehler und geänderte Eingangsbytes verhindern Freigabe; Original und Altsitzung bleiben erhalten"


def fall_ungueltig(lauf):
    setup_task(lauf)
    stopped_session(lauf)
    source = Path(lauf.mod.SAVE_FILE)
    invalid = b'{"version":'
    source.write_bytes(invalid)
    lauf.start()
    app = lauf.app
    assert app._data_read_only and app._read_only_reason == "recovery"
    assert app._recovery_assessment.kind == "invalid_data"
    assert app.save_items(show_error=False) is False
    assert app.resume_recovery_session() is False
    assert source.read_bytes() == invalid
    lauf.idle(8)
    assert source.read_bytes() == invalid
    return "Ungültiges JSON bleibt bytegleich; kein Leerspeichern, keine Freigabe, kein stiller Backupimport"


def fall_fehlend(lauf):
    setup_task(lauf)
    stopped_session(lauf)
    source = Path(lauf.mod.SAVE_FILE)
    source.unlink()
    lauf.start()
    app = lauf.app
    assert app._data_read_only and app._recovery_assessment.kind == "missing_data"
    assert app.save_items(show_error=False) is False
    lauf.idle(8)
    assert not source.exists(), "Ein fehlender unsauberer Bestand darf nicht als Leerdatei ersetzt werden"
    return "Nach ungeklärtem Ende fehlende Hauptdatei wird nicht leer neu angelegt"


def fall_layout(lauf):
    setup_task(lauf)
    stopped_session(lauf)
    source = Path(lauf.mod.SAVE_FILE)
    original = source.read_bytes()
    lauf.start()
    app, mod = lauf.app, lauf.mod
    count, matrix, captures, capture_failures, sizes = 0, [], [], [], []
    for design in ("light", "dark", "glass_dark"):
        app.set_design(design)
        for font in ("mittel", "gross"):
            app.settings["ui_font_size"] = font
            app.apply_ui_font()
            for hints in (False, True):
                app.settings["show_hints"] = hints
                for main_geometry in ("860x700", "1280x800"):
                    lauf.root.geometry(main_geometry + "+20+20")
                    lauf.idle(5)
                    assert app.storage_notice.winfo_ismapped(), "Wiederanlaufhinweis muss auch ohne Bedienhinweise sichtbar bleiben"
                    context = f"{design}/{font}/{hints}/{main_geometry}"
                    def inspect(dialog):
                        nonlocal count
                        dialog.geometry("480x360")
                        lauf.idle(5)
                        labels = {b.text for b in knoepfe(dialog, mod.RoundedButton)}
                        required = {mod.RoundedButton.action_text(value) for value in
                                    ("Bestand freigeben", "Sicherungen …", "Schließen")}
                        assert required <= labels, labels
                        n, errors = knopf_befunde(dialog, mod, context)
                        assert not errors, errors
                        count += n
                        body = next(iter(knoepfe(dialog, mod.tk.Text)))
                        assert "Abschluss" in body.get("1.0", "end")
                        matrix.append(context)
                        sizes.append({"context": context, "requested": [480, 360],
                                      "actual_client": [dialog.winfo_width(), dialog.winfo_height()]})
                        if font == "gross" and hints and main_geometry == "860x700":
                            try:
                                capture = screenshot(lauf, dialog, "wiederanlauf_" + design + "_gross_status")
                                if capture:
                                    captures.append(capture)
                                if design == "dark":
                                    capture = screenshot(lauf, lauf.root, "wiederanlauf_dark_gross_hauptfenster")
                                    if capture:
                                        captures.append(capture)
                            except Exception as error:
                                capture_failures.append(context + ": " + type(error).__name__)
                    visit(lauf, "Speicherstatus", app.show_storage_status, inspect)
    assert source.read_bytes() == original
    assert len(matrix) == 24, len(matrix)
    if captures:
        assert len({entry["sha256"] for entry in captures}) == len(captures), "Designaufnahmen dürfen nicht identisch sein"
    return {"button_checks": count, "contexts": matrix, "screenshots": captures,
            "capture_unavailable": capture_failures, "dialog_sizes": sizes,
            "result": "Freigabe/Sicherungen/Schließen bei angeforderten 480x360 und tatsächlichen Dialogmindestmaßen erreichbar; 24 Design-/Schrift-/Hinweis-/Hauptgrößenkombinationen"}


def fall_restore(lauf):
    """Der reguläre Wiederherstellungsweg bewahrt Identitäten und Anhangbytes."""
    app, mod = lauf.app, lauf.mod
    first = app.new_item("Serienaufgabe für Restore")
    target = app.new_item("Ziel eines lokalen Verweises")
    first["due"] = "2026-12-14"
    first["repeat"] = app.normalize_repeat({"art": "taeglich"}, default_start=first["due"])
    first["references"] = ["glide://item/" + target["id"]]
    storage = "attachments/restoreprobe.txt"
    attachment = Path(mod.BASE_DIR) / storage
    attachment.parent.mkdir(exist_ok=True)
    contents = b"Kuenstliche Anhangbytes fuer Restore"
    attachment.write_bytes(contents)
    first["attachments"] = [dict(id="attachment-restore", name="restoreprobe.txt", storage=storage)]
    app.items.extend((first, target))
    assert app.save_items()
    expected = {item["id"]: copy.deepcopy(item) for item in (first, target)}
    archive_path = Path(lauf.data) / "wiederherstellung.glidebackup"
    app.write_complete_backup(str(archive_path), app.complete_backup_payload())
    with zipfile.ZipFile(archive_path) as archive:
        archived = json.loads(archive.read("data.json"))
        assert archived["version"] == app.DATA_SCHEMA_VERSION
        assert archive.read(storage) == contents
    with app.item_change([first["id"]]) as change:
        first["text"] = "Zwischenzeitlich geändert"
        change.mark(first["id"])
    assert app.import_full_backup(path=str(archive_path), show_success=False, confirm=False)
    restored = {item["id"]: item for entry in app.lists for item in entry["items"]}
    for identity, before in expected.items():
        after = restored[identity]
        for key in ("text", "repeat", "references"):
            assert after.get(key) == before.get(key), (identity, key, before.get(key), after.get(key))
    restored_attachment = restored[first["id"]]["attachments"][0]
    assert Path(app.resolve_attachment_path(restored_attachment)).read_bytes() == contents
    assert list(Path(mod.BACKUP_DIR).glob("vor_import_*.glidebackup")), "Regulärer Restore braucht Vorsicherung"
    assert json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8"))["version"] == app.DATA_SCHEMA_VERSION
    return "Regulärer portabler Restore erhält IDs, Wiederholungen, Verweise, Anhangbytes und Format; Originalvorsicherung vor Import bestätigt"


def recovery_fixture(lauf, *, missing=False):
    """Gültige portable Sicherung plus ausdrücklich ungelösten Fehlerstart."""
    fall_restore(lauf)
    archive_path = Path(lauf.data) / "wiederherstellung.glidebackup"
    with zipfile.ZipFile(archive_path) as archive:
        expected = json.loads(archive.read("data.json"))
        attachments = {name: archive.read(name) for name in archive.namelist()
                       if name.startswith("attachments/") and not name.endswith("/")}
    marker = stopped_session(lauf)
    source = Path(lauf.mod.SAVE_FILE)
    if missing:
        source.unlink()
        original = None
    else:
        original = b'{"version":'
        source.write_bytes(original)
    original_marker = marker.read_bytes()
    lauf.start()
    app = lauf.app
    assert app._data_read_only and app._read_only_reason == "recovery"
    assert app._recovery_assessment.kind == ("missing_data" if missing else "invalid_data")
    return archive_path, source, original, marker, original_marker, expected, attachments


def unchanged(source, original):
    assert (not source.exists()) if original is None else (source.read_bytes() == original)


def assert_portable_restored(lauf, expected, attachment_bytes):
    app = lauf.app
    wanted = {item["id"]: item for entry in expected["lists"] for item in app.walk_items(entry["items"])}
    actual = {item["id"]: item for entry in app.lists for item in app.walk_items(entry["items"])}
    assert set(actual) == set(wanted), (set(wanted), set(actual))
    for identity, before in wanted.items():
        after = actual[identity]
        for key in ("text", "repeat", "references"):
            assert after.get(key) == before.get(key), (identity, key, before.get(key), after.get(key))
        for index, attachment in enumerate(before.get("attachments", [])):
            restored = after["attachments"][index]
            expected_bytes = attachment_bytes[attachment["storage"]]
            assert Path(app.resolve_attachment_path(restored)).read_bytes() == expected_bytes
    saved = json.loads(Path(lauf.mod.SAVE_FILE).read_text(encoding="utf-8"))
    assert saved["version"] == app.DATA_SCHEMA_VERSION
    assert not app._data_read_only
    assert not app.undo_stack and app.redo_steps().peek() is None, "Wiederanlauf darf kein Undo zum leeren Fehlerstart anbieten"
    saved_bytes = Path(lauf.mod.SAVE_FILE).read_bytes()
    app.undo_last_change()
    assert Path(lauf.mod.SAVE_FILE).read_bytes() == saved_bytes
    assert set(actual) == {item["id"] for entry in app.lists for item in app.walk_items(entry["items"])}


def restore_recovery(lauf, *, missing):
    path, source, original, marker, marker_before, expected, attachments = recovery_fixture(lauf, missing=missing)
    app = lauf.app
    with patch.object(app, "ask_yes_no", return_value=False) as question:
        assert not app.import_full_backup(path=str(path), show_success=False, confirm=False)
        assert question.call_count == 1, "Auch confirm=False ersetzt keine bewusste Wiederanlauffreigabe"
    unchanged(source, original)
    assert marker.read_bytes() == marker_before
    assert app._data_read_only
    with patch.object(app, "ask_yes_no", return_value=True) as question:
        assert app.import_full_backup(path=str(path), show_success=False, confirm=False)
        assert question.call_count == 1
    assert_portable_restored(lauf, expected, attachments)
    preserved = Path(app._recovery_assessment.preserved_path)
    if missing:
        evidence = json.loads(preserved.read_text(encoding="utf-8"))
        assert app._recovery_assessment.original_missing
        assert evidence["original_missing"] is True and evidence["evidence_version"] == 1
        assert "lists" not in evidence and evidence["data_key"] == app._recovery_guard.data_key
    else:
        assert preserved.read_bytes() == original
    assert not lauf.errors, lauf.errors
    return {"original_missing": missing, "ids": len([item for entry in expected["lists"]
            for item in app.walk_items(entry["items"])]), "attachments": len(attachments),
            "result": "Bewusste portable Wiederherstellung aus geschütztem Fehlerstart; Original-/Abwesenheitsnachweis, IDs/Serie/Verweise/Anhänge/Format erhalten, kein Undo zum Leeren"}


def fall_restore_ungueltig(lauf):
    return restore_recovery(lauf, missing=False)


def fall_restore_fehlend(lauf):
    return restore_recovery(lauf, missing=True)


def fall_restore_fehler(lauf):
    path, source, original, marker, marker_before, expected, attachments = recovery_fixture(lauf)
    app = lauf.app
    missing_attachment = Path(lauf.data) / "fehlender_anhang.glidebackup"
    with zipfile.ZipFile(path) as original_zip, zipfile.ZipFile(missing_attachment, "w") as incomplete:
        omitted = next(iter(attachments))
        for member in original_zip.infolist():
            if member.filename != omitted:
                incomplete.writestr(member, original_zip.read(member))
    corrupt = Path(lauf.data) / "kaputt.glidebackup"
    corrupt.write_bytes(b"Defekte Sicherung; kein JSON oder ZIP")
    checked = []
    for variant, chosen in (("fehlender_anhang", missing_attachment), ("kaputte_sicherung", corrupt),
                            ("vorsicherung", path), ("commit", path)):
        attachments_before = {str(p.relative_to(Path(lauf.data))): p.read_bytes()
                              for p in (Path(lauf.data) / "attachments").rglob("*") if p.is_file()}
        writer = app.write_json_atomic

        def fail_commit(target, payload):
            if str(target) == str(source):
                raise PermissionError("Kontrollierter Hauptdatei-Commitfehler")
            return writer(target, payload)

        with ExitStack() as stack:
            stack.enter_context(patch.object(app, "ask_yes_no", return_value=True))
            if variant == "vorsicherung":
                stack.enter_context(patch.object(app._recovery_guard, "preserve_original",
                                                side_effect=PermissionError("Kontrollierter Vorsicherungsfehler")))
            if variant == "commit":
                stack.enter_context(patch.object(app, "write_json_atomic", side_effect=fail_commit))
            assert not app.import_full_backup(path=str(chosen), show_success=False, confirm=False), variant
        unchanged(source, original)
        assert app._data_read_only and app._read_only_reason == "recovery", variant
        assert not app.undo_stack and app.redo_steps().peek() is None, variant
        assert lauf.errors, (variant, "Fehler muss sichtbar gemeldet werden")
        lauf.errors.clear()
        assert attachments_before == {str(p.relative_to(Path(lauf.data))): p.read_bytes()
                                       for p in (Path(lauf.data) / "attachments").rglob("*") if p.is_file()}, variant
        assert app.save_items(show_error=False) is False, variant
        checked.append(variant)
    # Ein fehlgeschlagener Commit darf weder eine stille Freigabe bewirken
    # noch den danach bewussten, unveränderten Wiederholungsweg verbauen.
    with patch.object(app, "ask_yes_no", return_value=True):
        assert app.import_full_backup(path=str(path), show_success=False, confirm=False)
    assert_portable_restored(lauf, expected, attachments)
    assert not lauf.errors, lauf.errors
    return {"checked": checked, "result": "Alle vier Fehler erhalten Originalbytes, Anhänge und Schreibschutz; bewusste Wiederholung danach erfolgreich"}


def fall_lockuebernahme(lauf):
    setup_task(lauf)
    marker = stopped_session(lauf)
    source = Path(lauf.mod.SAVE_FILE)
    original, previous_marker = source.read_bytes(), marker.read_bytes()
    lock = Path(lauf.mod.LOCK_FILE)
    lock.write_bytes(b'{"defekte_sperre":')
    with patch.object(lauf.mod.ListApp, "ask_yes_no", return_value=False):
        lauf.start()
    app = lauf.app
    assert app._data_read_only and app._read_only_reason == "lock_defective"
    assert app.take_over_data_lock(), "Bewusste Sperrübernahme muss lokal gelingen"
    assert app._data_read_only and app._read_only_reason == "recovery", "Sperrübernahme darf den ungeklärten Sitzungsabschluss nicht umgehen"
    assert app._recovery_assessment.needs_recovery
    assert app.save_items(show_error=False) is False
    assert source.read_bytes() == original and marker.read_bytes() == previous_marker
    assert not lauf.errors, lauf.errors
    return "Defekte Sperre bewusst übernommen; anschließende Sitzungsprüfung erhält Original und erzwingt Wiederanlauffreigabe"


def fall_restore_nachlauf(lauf):
    path, source, original, *_ = recovery_fixture(lauf)
    app = lauf.app
    writer = app.write_json_atomic
    writes = 0
    def fail_second(target, payload):
        nonlocal writes
        if str(target) == str(source):
            writes += 1
            if writes == 2:
                raise PermissionError('Kontrollierter Nachlauffehler')
        return writer(target, payload)
    with patch.object(app, 'ask_yes_no', return_value=True), patch.object(app, 'write_json_atomic', side_effect=fail_second):
        assert not app.import_full_backup(path=str(path), show_success=False, confirm=False)
    assert writes == 2 and source.read_bytes() != original
    assert json.loads(source.read_text(encoding='utf-8'))['version'] == app.DATA_SCHEMA_VERSION
    assert app._data_read_only and app._read_only_reason == 'recovery'
    assert lauf.errors
    lauf.errors.clear()
    return 'Nach Commit fehlgeschlagener Speichernachlauf meldet keinen Erfolg; importierter Bestand bleibt geschützt'


FAELLE = ("sauber", "freigabe", "fehler", "ungueltig", "fehlend", "layout", "restore",
          "restore_ungueltig", "restore_fehlend", "restore_fehler", "lockuebernahme", "restore_nachlauf")


def main():
    global CAPTURE_DIR
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--fall", choices=FAELLE + ("alle",), default="alle")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report:
        CAPTURE_DIR = args.report.parent / "fenster"
    report = dict(app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),
                  session_guard_sha256=hashlib.sha256((args.app.parent / "session_guard.py").read_bytes()).hexdigest(),
                  test_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  faelle={}, fehler=[], limitations=["Hardware-Stromausfall, native Mac-/Linux-/DPI-/Reader- und Menschenabnahme ungeprüft."])
    for name in FAELLE if args.fall == "alle" else (args.fall,):
        with tempfile.TemporaryDirectory(prefix="glide-wiederanlauf-") as folder:
            lauf = None
            try:
                lauf = Lauf(args.app, folder)
                result = globals()["fall_" + name](lauf)
                assert not lauf.errors, lauf.errors
                report["faelle"][name] = dict(ok=True, befund=result)
                print("OK", name, result, flush=True)
            except Exception:
                detail = traceback.format_exc().replace(str(Path.home()), "~")[-2600:]
                report["faelle"][name] = dict(ok=False, befund=detail)
                report["fehler"].append(name)
                print("ROT", name, detail, flush=True)
            finally:
                if lauf is not None:
                    lauf.ende()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(bool(report["fehler"]))


if __name__ == "__main__":
    sys.exit(main())
