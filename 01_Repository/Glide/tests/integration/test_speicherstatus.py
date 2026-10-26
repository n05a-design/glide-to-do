"""WA-40/47: Speicherstatus, Retry und geschützte Größenüberschreitung."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import traceback
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests/integration"))
from test_uiux_paket import Lauf, knoepfe, knopf_befunde


def fall_fehler_retry(lauf):
    app, mod = lauf.app, lauf.mod
    item = app.new_item("Nicht verlieren")
    app.items.append(item)
    assert app.save_items()
    vorher = Path(mod.SAVE_FILE).read_bytes()
    item["text"] = "Noch nicht auf der Platte"
    writer = app.write_json_atomic

    def gesperrt(path, payload):
        if str(path) == str(mod.SAVE_FILE):
            raise OSError("Schreibprobe Hauptdatei")
        return writer(path, payload)

    with patch.object(app, "write_json_atomic", side_effect=gesperrt), patch.object(app, "log_error") as log:
        app.autosave_tick()
        app.autosave_tick()
        lauf.idle()
        assert Path(mod.SAVE_FILE).read_bytes() == vorher and app.dirty
        assert app.storage_health().failures["data"][1] == 2
        assert log.call_count == 1, "Identische Fehler fluten das Protokoll"
        assert app.storage_notice.winfo_ismapped()
    assert not lauf.errors, lauf.errors

    visited = []

    def bedienen():
        dialog = next(w for w in lauf.root.winfo_children()
                      if isinstance(w, mod.tk.Toplevel) and w.title() == "Speicherstatus")
        try:
            dialog.geometry("480x360")
            lauf.idle()
            text = next(iter(knoepfe(dialog, mod.tk.Text)))
            assert "Schreibprobe Hauptdatei" in text.get("1.0", "end")
            buttons = knoepfe(dialog, mod.RoundedButton)
            next(b for b in buttons if b.text == "Erneut speichern").command()
            lauf.idle()
            assert not app.storage_health().failures and not app.dirty
            assert "Keine offenen Speicherfehler" in text.get("1.0", "end")
            _count, findings = knopf_befunde(dialog, mod, "Speicherstatus 480x360")
            assert not findings, findings
            visited.append(True)
        finally:
            dialog.destroy()

    lauf.root.after(80, bedienen)
    app.show_storage_status()
    lauf.idle()
    assert visited and not app.storage_notice.winfo_ismapped()
    assert b"Noch nicht auf der Platte" in Path(mod.SAVE_FILE).read_bytes()
    return "Autosave-Fehler sichtbar und dedupliziert; echter Dialog/Retry, Originalbytes bis Erfolg erhalten, Fußknöpfe frei"


def fall_nebenwege(lauf):
    app, mod = lauf.app, lauf.mod
    assert app.save_items() and app.save_settings() and app.save_templates()
    writer = app.write_json_atomic
    originals = {p: Path(p).read_bytes() for p in (mod.SETTINGS_FILE, mod.TEMPLATES_FILE)}

    def gesperrt(path, payload):
        if str(path) in originals:
            raise OSError("Schreibprobe Nebendatei")
        return writer(path, payload)

    app.settings["profile_name"] = "Offene Einstellung"
    with patch.object(app, "write_json_atomic", side_effect=gesperrt):
        for _ in range(2):
            assert app.save_settings() is False
            assert app.save_templates() is False
    assert all(Path(p).read_bytes() == raw for p, raw in originals.items())
    with patch.object(app, "write_backup_copy", return_value="Sicherungsprobe"):
        assert app.save_items(show_error=False) is True
    assert "backup" in app.storage_health().failures
    assert "templates" in app.storage_health().failures
    # Ein erfolgreicher Datenweg hebt keinen Fehler einer anderen Datei auf.
    assert app.storage_notice.winfo_ismapped() or app.storage_health().notice()
    assert app.retry_storage()
    assert not app.storage_health().failures
    assert json.loads(Path(mod.SETTINGS_FILE).read_text(encoding="utf-8"))["profile_name"] == "Offene Einstellung"
    return "Einstellungen, Vorlagen und Sicherung getrennt; kein falscher Datenfehler; Retry aller offenen Speicherwege"


def fall_groessen(lauf):
    mod = lauf.mod
    assert lauf.app.save_items() and lauf.app.save_settings() and lauf.app.save_templates()
    limit = 1024 * 1024
    for kind, path in (("settings", mod.SETTINGS_FILE), ("templates", mod.TEMPLATES_FILE), ("data", mod.SAVE_FILE)):
        original = Path(path).read_bytes()
        lauf.ende()
        Path(path).write_bytes(b" " * (limit + 1))
        with patch.object(mod.ListApp, "MAX_BACKUP_DATA_BYTES", limit):
            lauf.start()
            app = lauf.app
            assert kind in app._storage_blocked_files
            assert app.storage_notice.winfo_ismapped()
            if kind == "data":
                assert app._data_read_only and app.save_items(show_error=False) is False
            elif kind == "settings":
                assert app.save_settings() is False
            else:
                assert app.save_templates() is False
            assert Path(path).stat().st_size == limit + 1
            assert Path(path).read_bytes() == b" " * (limit + 1)
        lauf.ende()
        Path(path).write_bytes(original)
        lauf.start()
    # UTF-8-Bytegrenze des atomaren Schreibers, nicht Zeichenzahl.
    path = Path(lauf.data) / "grenze.json"
    payload = {"text": "Größe"}
    raw = mod.ListApp.settings_json_text(payload).replace("\n", mod.os.linesep).encode("utf-8")
    with patch.object(mod.ListApp, "MAX_BACKUP_DATA_BYTES", len(raw)):
        mod.ListApp.write_json_atomic(path, payload)
        try:
            mod.ListApp.write_json_atomic(path, {"text": "Größer"})
        except mod.glide_storage.SizeLimitError:
            pass
        else:
            raise AssertionError("Schreibgrenze fehlt")
        assert path.read_bytes() == raw
    return "Zu große Aufgaben/Einstellungen/Vorlagen beim Start geschützt; atomare UTF-8-Schreibgrenze erhält Original"


def fall_reserve_import(lauf):
    app, mod = lauf.app, lauf.mod
    assert app.save_items()
    health = app.storage_health()
    health.sizes = {"data": app.MAX_BACKUP_DATA_BYTES * 4 // 5 + 1}
    app.sync_storage_notice()
    lauf.idle()
    assert app.storage_notice.winfo_ismapped()
    assert "Frühwarnung" in health.report()
    app.enter_compact_mode()
    lauf.root.geometry("480x560")
    lauf.idle(5)
    assert app.storage_notice.winfo_ismapped()
    _count, findings = knopf_befunde(lauf.root, mod, "Kompakt mit Sicherungsreserve 480x560")
    assert not findings, findings
    app.leave_compact_mode()
    # Eine fehlgeschlagene Vorab-Sicherung stoppt den echten Import vor der Mutation.
    before = Path(mod.SAVE_FILE).read_bytes()
    ids = [e["id"] for e in app.lists]
    incoming = Path(lauf.data) / "import.json"
    incoming.write_bytes(before)
    with patch.object(app, "write_complete_backup", side_effect=mod.glide_storage.SizeLimitError("Budgetprobe")):
        app.import_full_backup(path=str(incoming), confirm=False, show_success=False)
    assert [e["id"] for e in app.lists] == ids and Path(mod.SAVE_FILE).read_bytes() == before
    # Der Import zeigt seinen vorhandenen Fehlerdialog; kein Tk-Rückruffehler.
    assert len(lauf.errors) == 1 and "Budgetprobe" in lauf.errors[0], lauf.errors
    lauf.errors.clear()
    app.refresh_storage_sizes()
    lauf.idle()
    assert not app.storage_notice.winfo_ismapped()
    return "Reserve ab 80 % sichtbar; fehlgeschlagene Vorab-Sicherung stoppt Import ohne Datenänderung"


FAELLE = ("fehler_retry", "nebenwege", "groessen", "reserve_import")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--fall", choices=FAELLE + ("alle",), default="alle")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = {"app_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(),
              "modules_sha256": {name: hashlib.sha256((args.app.parent / name).read_bytes()).hexdigest()
                                 for name in ("storage_health.py", "schema_backups.py", "action_catalog.py")
                                 if (args.app.parent / name).is_file()},
              "test_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "faelle": {}, "fehler": []}
    for name in (FAELLE if args.fall == "alle" else (args.fall,)):
        with tempfile.TemporaryDirectory(prefix="glide-speicherstatus-") as data:
            lauf = None
            try:
                lauf = Lauf(args.app, data)
                detail = globals()["fall_" + name](lauf)
                assert not lauf.errors, lauf.errors
                result["faelle"][name] = {"ok": True, "befund": detail}
                print("OK", name, detail, flush=True)
            except Exception:
                detail = traceback.format_exc().replace(str(Path.home()), "~")[-1800:]
                result["faelle"][name] = {"ok": False, "befund": detail}
                result["fehler"].append(name)
                print("ROT", name, detail, flush=True)
            finally:
                if lauf is not None:
                    lauf.ende()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(bool(result["fehler"]))


if __name__ == "__main__":
    sys.exit(main())
