"""Belastungstest Speichern und Laden (Auftrag vom 29.09.2026, Punkt 5 der Prüfung vom 28.09.2026).

Geprüft wird, was im Alltag selten, aber folgenreich ist:

1. **Großer Bestand:** rund 20.000 Punkte in 150 Listen mit Unterpunkten,
   Beschreibungen, Labels, Fälligkeiten und Sonderzeichen – Speichern und
   Laden verlustfrei und in vertretbarer Zeit.
2. **Viele Runden:** 40 Runden aus zufälligen Änderungen, Speichern und Laden;
   nach jeder Runde steht genau das in der Datei, was geladen wird.
3. **Abbruch mitten im Schreiben:** Ein zweiter Prozess schreibt große
   Bestände in Dauerschleife und wird hart beendet. Die Datei ist danach nie
   halb geschrieben, sondern immer einer der beiden vollständigen Stände.
   Liegengebliebene Zwischendateien räumt der nächste Start auf.
4. **Paralleles Schreiben:** Zwei Prozesse schreiben gleichzeitig; wer liest,
   bekommt immer eine vollständige Datei.
5. **Sperre:** Übernimmt eine zweite Instanz den Datenordner, speichert diese
   nicht mehr.
6. **Sicherungen:** nur bei geändertem Inhalt, dazu je Tag der letzte Stand
   für 14 Tage (Entscheidung 1).
7. **Startprüfung:** Ein älteres Format wird beim Start umgestellt (mit
   bytegenauer Vorsicherung); ein neueres Format und eine unbekannte
   Listenart öffnen schreibgeschützt; eine kaputte Datei wird gesichert
   (Entscheidungen 2 b und 3).
8. **Schreibrechte:** Fehlt das Schreibrecht, bleibt die Datei unverändert.
"""
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import random
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
APP = REPO / "src/glide/app.pyw"
sys.dont_write_bytecode = True

# Schreibprozess für Teil 3 und 4: lädt die App als Modul (ohne Oberfläche)
# und schreibt mit derselben Funktion wie Glide selbst.
SCHREIBER = r'''
import importlib.machinery, importlib.util, json, os, sys
sys.dont_write_bytecode = True
os.environ["GLIDE_DATA_DIR"] = sys.argv[1]
loader = importlib.machinery.SourceFileLoader("glide_schreiber", sys.argv[2])
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)
ziel = sys.argv[3]
namen = sys.argv[4].split(",")
payloads = [json.loads(open(os.path.join(sys.argv[1], name + ".json"), encoding="utf-8").read()) for name in namen]
print("bereit", flush=True)
while True:
    for payload in payloads:
        mod.ListApp.write_json_atomic(ziel, payload)
'''


def grosser_payload(marke, punkte=6000):
    """Deterministischer Bestand in Speicherform, rund 3 MB."""
    zufall = random.Random(marke)
    listen = []
    for index in range(60):
        items = []
        for nummer in range(punkte // 60):
            items.append({"id": f"{marke}-{index}-{nummer}", "text": f"Punkt {nummer} {'x' * zufall.randint(5, 80)}",
                          "done": zufall.random() < 0.3, "children": [], "description": "ä ö ü ß € 😀 " * 3})
        listen.append({"id": f"{marke}-liste-{index}", "title": f"Liste {index}", "items": items})
    return {"version": 20, "marker": marke, "lists": listen}


def dateibytes(payload):
    return json.dumps(payload, ensure_ascii=False, indent=4).encode("utf-8")


with tempfile.TemporaryDirectory(prefix="glide-last-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_speicherlast", str(APP))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1280x860+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    meldungen = []
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: meldungen.append(args[:1])
    # Die Beispieldaten tragen fällige Erinnerungen. Ihre Zustellung ändert den
    # Bestand zu Recht – aber mitten im Vergleich von Gespeichertem und
    # Geladenem. Zustellung prüfen andere Suiten.
    app.process_reminders = lambda *args, **kwargs: False
    SPEICHER = Path(mod.SAVE_FILE)
    SICHERUNGEN = Path(mod.BACKUP_DIR)
    ergebnis = {}

    def ruhe(runden=4):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    def bestand():
        """Gespeicherter Teil des Bestands, vergleichbar (ohne Ansichtszustand)."""
        daten = app.data_payload()
        return json.dumps({schluessel: daten[schluessel] for schluessel in
                           ("folders", "labels", "lists", "trash", "history")},
                          ensure_ascii=False, sort_keys=True)

    def aus_datei():
        daten = json.loads(SPEICHER.read_text(encoding="utf-8"))
        return json.dumps({schluessel: daten.get(schluessel) for schluessel in
                           ("folders", "labels", "lists", "trash", "history")},
                          ensure_ascii=False, sort_keys=True)

    def alle_punkte():
        return [item for eintrag in app.lists for item in app.walk_items(eintrag.get("items", []))]

    try:
        ruhe()
        # --- 1. Großer Bestand ------------------------------------------------
        zufall = random.Random(20260929)
        label_ids = [label["id"] for label in app.labels][:6]
        sonder = ["😀 Emoji", "שלום RTL", "é kombiniert", "Zero‍Width", "Tab\tim Text",
                  "Anführung „“ und ‚‘", "Mathe ∑∫√", "Astral 𝄞𝕏"]
        neue_listen = []
        for index in range(150):
            items = []
            for nummer in range(130):
                kinder = []
                if nummer % 10 == 0:
                    for kind in range(3):
                        enkel = [app.new_item(f"Enkel {index}.{nummer}.{kind}.{e}") for e in range(2)] \
                            if kind == 0 and nummer % 50 == 0 else []
                        kinder.append(app.new_item(f"Unterpunkt {index}.{nummer}.{kind}", children=enkel))
                items.append(app.new_item(
                    f"{sonder[nummer % len(sonder)]} · Punkt {index}.{nummer}",
                    done=zufall.random() < 0.25, children=kinder,
                    importance=zufall.randint(0, 3),
                    due=(datetime(2026, 10, 1) + timedelta(days=zufall.randint(0, 400))).date().isoformat()
                    if nummer % 3 == 0 else None,
                    description=("Beschreibung " + "lang " * zufall.randint(0, 200)) if nummer % 7 == 0 else "",
                    labels=[zufall.choice(label_ids)] if label_ids and nummer % 4 == 0 else None))
            neue_listen.append(app.new_list_object(f"Last {index:03d}", items))
        app.lists.extend(neue_listen)
        anzahl = len(alle_punkte())
        assert anzahl >= 20000, anzahl
        start = time.perf_counter()
        assert app.save_items()
        ergebnis["speichern_s"] = round(time.perf_counter() - start, 2)
        groesse_mb = SPEICHER.stat().st_size / 1e6
        vorher = bestand()
        start = time.perf_counter()
        app.load_items()
        ergebnis["laden_s"] = round(time.perf_counter() - start, 2)
        ruhe()
        assert len(alle_punkte()) == anzahl, (len(alle_punkte()), anzahl)
        assert bestand() == vorher, "großer Bestand verlustfrei"
        assert ergebnis["speichern_s"] < 20 and ergebnis["laden_s"] < 30, ergebnis
        # Titel sind einzeilig: Aus dem Tabulator wird schon bei der Eingabe ein
        # Leerzeichen. Alles andere muss den Rundlauf unverändert überstehen.
        texte = {item["text"] for item in alle_punkte()}
        eingegeben = [app.new_item(zeichen)["text"] for zeichen in sonder]
        assert all(any(zeichen in text for text in texte) for zeichen in eingegeben), "Sonderzeichen erhalten"
        assert "e\u0301" in "".join(texte) and "\u200d" in "".join(texte) and "𝄞" in "".join(texte)

        # --- 2. Viele Runden aus Ändern, Speichern, Laden -----------------------
        papierkorb_voll = False
        for runde in range(40):
            listen = [eintrag for eintrag in app.lists if eintrag.get("list_kind", "tasks") == "tasks"
                      and eintrag.get("items")]
            for _ in range(25):
                eintrag = zufall.choice(listen)
                aktion = zufall.randrange(5)
                if aktion == 0:
                    eintrag["items"].append(app.new_item(f"Neu {runde} {zufall.random():.6f} ✓"))
                elif aktion == 1 and eintrag["items"]:
                    item = zufall.choice(eintrag["items"])
                    if not app.is_structural_item(item):
                        item["done"] = not item.get("done")
                elif aktion == 2 and eintrag["items"]:
                    zufall.choice(eintrag["items"])["text"] = f"Umbenannt {runde} · 𝄞 {zufall.randint(0, 9999)}"
                elif aktion == 3 and len(eintrag["items"]) > 1:
                    # Löschen wie in der App: in den Papierkorb. Nach 200
                    # Einträgen fallen die ältesten endgültig heraus – samt
                    # der Verweise darauf (`drop_dangling_references`).
                    app.move_item_to_trash(zufall.choice(eintrag["items"])["id"])
                elif aktion == 4 and eintrag["items"]:
                    ziel = zufall.choice(listen)
                    ziel["items"].append(eintrag["items"].pop(zufall.randrange(len(eintrag["items"]))))
            erwartet = len(alle_punkte())
            papierkorb_voll = papierkorb_voll or len(app.trash) >= app.MAX_TRASH_ENTRIES
            assert app.save_items(), runde
            auf_platte = aus_datei()
            app.load_items()
            assert bestand() == auf_platte, f"Runde {runde}: geladen ≠ gespeichert"
            assert len(alle_punkte()) == erwartet, (runde, len(alle_punkte()), erwartet)
        ruhe()
        # Endgültiges Entfernen (Papierkorb voll oder geleert) lässt keine
        # Verweise auf fehlende Punkte zurück.
        # Gezielt: Ein verknüpfter Punkt fällt durch das Überlaufen des
        # Papierkorbs endgültig heraus; die Verknüpfung geht mit.
        ziel_liste = next(eintrag for eintrag in app.lists if eintrag.get("list_kind", "tasks") == "tasks"
                          and not app.is_inbox_list(eintrag))
        quelle, ziel_punkt = app.new_item("Verweist"), app.new_item("Ziel")
        ziel_liste["items"] += [quelle, ziel_punkt]
        quelle["links"] = [ziel_punkt["id"]]
        quelle["blocked_by"] = [ziel_punkt["id"]]
        assert app.move_item_to_trash(ziel_punkt["id"])
        assert quelle["links"] == [ziel_punkt["id"]], "im Papierkorb bleibt der Verweis"
        for nummer in range(app.MAX_TRASH_ENTRIES):
            fuellung = app.new_item(f"Füllung {nummer}")
            ziel_liste["items"].append(fuellung)
            app.move_item_to_trash(fuellung["id"])
        papierkorb_voll = True
        assert quelle["links"] == [] and quelle["blocked_by"] == [], "endgültig entfernt: Verweis weg"
        ergebnis["papierkorb_voll"] = "ja" if papierkorb_voll else "nein"
        app.ask_yes_no = lambda *args, **kwargs: True
        app.empty_trash()
        bekannt = {item["id"] for item in alle_punkte()}
        for item in alle_punkte():
            for feld in ("links", "blocked_by"):
                assert set(item.get(feld) or ()) <= bekannt, (feld, item["id"])
        assert app.save_items()
        auf_platte = aus_datei()
        app.load_items()
        assert bestand() == auf_platte, "nach dem Leeren des Papierkorbs"

        # --- 3. Abbruch mitten im Schreiben ------------------------------------
        schreibordner = Path(ordner, "schreiber")
        schreibordner.mkdir()
        a, b = grosser_payload("A"), grosser_payload("B")
        Path(schreibordner, "A.json").write_text(json.dumps(a), encoding="utf-8")
        Path(schreibordner, "B.json").write_text(json.dumps(b), encoding="utf-8")
        erlaubt = {hashlib.sha256(dateibytes(a)).hexdigest(), hashlib.sha256(dateibytes(b)).hexdigest()}
        ziel = schreibordner / "liste_speicher.json"
        skript = schreibordner / "schreiber.py"
        skript.write_text(SCHREIBER, encoding="utf-8")

        def starten(namen, ziel_datei):
            prozess = subprocess.Popen([sys.executable, str(skript), str(schreibordner), str(APP), str(ziel_datei),
                                        namen], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            assert prozess.stdout.readline().strip() == "bereit", prozess.stderr.read()
            return prozess

        def lesen_pruefen(ziel_datei, fund):
            try:
                with open(ziel_datei, "rb") as datei:
                    inhalt = datei.read()
            except FileNotFoundError:
                return
            except PermissionError:
                fund["gesperrt"] = fund.get("gesperrt", 0) + 1
                return
            pruefsumme = hashlib.sha256(inhalt).hexdigest()
            assert pruefsumme in erlaubt, f"halbe Datei gelesen ({len(inhalt)} Bytes)"
            fund["gelesen"] = fund.get("gelesen", 0) + 1

        fund = {}
        abbrueche = 0
        for durchgang in range(6):
            prozess = starten("A,B", ziel)
            try:
                for _ in range(40):
                    time.sleep(zufall.uniform(0.005, 0.06))
                    lesen_pruefen(ziel, fund)
            finally:
                time.sleep(zufall.uniform(0.0, 0.2))
                prozess.kill()
                prozess.wait(timeout=20)
                abbrueche += 1
            lesen_pruefen(ziel, fund)
            json.loads(ziel.read_text(encoding="utf-8"))
        reste = [name for name in os.listdir(schreibordner) if name.startswith(".glide-json-")]
        ergebnis["abbrueche"] = abbrueche
        ergebnis["gelesen"] = fund.get("gelesen", 0)
        ergebnis["reste_nach_abbruch"] = len(reste)

        # Zwischendateien: Alte räumt der Start auf, frische bleiben.
        alt = Path(ordner, ".glide-json-alt.tmp")
        neu = Path(ordner, ".glide-json-neu.tmp")
        fremd = Path(ordner, "notiz.tmp")
        for pfad in (alt, neu, fremd):
            pfad.write_text("{", encoding="utf-8")
        vergangen = time.time() - (app.STALE_TEMP_MINUTES + 5) * 60
        os.utime(alt, (vergangen, vergangen))
        os.utime(fremd, (vergangen, vergangen))
        assert app.remove_stale_temp_files() == 1
        assert not alt.exists() and neu.exists() and fremd.exists(), "nur alte eigene Zwischendateien"
        neu.unlink()
        fremd.unlink()

        # --- 4. Paralleles Schreiben --------------------------------------------
        fund_parallel = {}
        erster, zweiter = starten("A", ziel), starten("B", ziel)
        try:
            ende = time.monotonic() + 4
            while time.monotonic() < ende:
                lesen_pruefen(ziel, fund_parallel)
                time.sleep(0.01)
        finally:
            for prozess in (erster, zweiter):
                prozess.kill()
                prozess.wait(timeout=20)
        lesen_pruefen(ziel, fund_parallel)
        assert fund_parallel.get("gelesen", 0) > 50, fund_parallel
        ergebnis["parallel_gelesen"] = fund_parallel.get("gelesen", 0)

        # Unter Windows wartet das Ersetzen kurz, wenn jemand die Datei offen hält.
        versuche = []
        echt_replace = mod.os.replace

        def gesperrt(quelle, ziel_datei):
            versuche.append(1)
            if len(versuche) < 3:
                raise PermissionError(13, "gesperrt")
            return echt_replace(quelle, ziel_datei)

        mod.os.replace = gesperrt
        echt_windows = mod.IS_WINDOWS
        mod.IS_WINDOWS = True
        try:
            mod.ListApp.write_json_atomic(str(schreibordner / "probe.json"), {"a": 1})
        finally:
            mod.os.replace = echt_replace
            mod.IS_WINDOWS = echt_windows
        assert len(versuche) == 3 and json.loads((schreibordner / "probe.json").read_text()) == {"a": 1}

        # --- 5. Sperre: eine zweite Instanz übernimmt ---------------------------
        wartend = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        try:
            host = os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "unbekannt"
            jetzt = datetime.now().astimezone().isoformat(timespec="seconds")
            mod.ListApp.write_json_atomic(mod.LOCK_FILE, {"host": host, "pid": wartend.pid, "token": "fremd",
                                                          "started_at": jetzt, "refreshed_at": jetzt})
            app.refresh_data_lock()
            assert app._data_read_only and app._read_only_reason == "lock"
            vorher_bytes = SPEICHER.read_bytes()
            assert app.save_items(show_error=False) is False
            assert SPEICHER.read_bytes() == vorher_bytes, "gesperrt: Datei unverändert"
        finally:
            wartend.kill()
            wartend.wait(timeout=10)
        assert app.read_foreign_lock() is None, "beendeter Prozess hält keine Sperre"
        app._data_read_only = False
        assert app.acquire_data_lock() is None and not app._data_read_only
        assert app.save_items(show_error=False)

        # --- 6. Sicherungen nur bei Änderung, Tagesstände 14 Tage ---------------
        for name in os.listdir(SICHERUNGEN):
            if name.startswith("liste_backup_"):
                os.remove(SICHERUNGEN / name)
        app._latest_backup = None
        app._last_backup_monotonic = None

        def sicherungen():
            return sorted(name for name in os.listdir(SICHERUNGEN) if name.startswith("liste_backup_"))

        assert app.write_backup_copy(force=True) is None and len(sicherungen()) == 1
        for _ in range(5):
            app.autosave_tick()
            app.write_backup_copy(force=True)
        assert len(sicherungen()) == 1, "ohne Änderung keine weitere Sicherung"
        app.lists[0]["title"] = "Geändert für die Sicherung"
        assert app.save_items(force_backup=True)
        app.write_backup_copy(force=True)
        assert len(sicherungen()) == 2, sicherungen()
        inhalte = {hashlib.sha256((SICHERUNGEN / name).read_bytes()).hexdigest() for name in sicherungen()}
        assert len(inhalte) == 2, "zwei verschiedene Stände"

        # Rotation mit künstlichem Alter: 30 Tage, je Tag drei Stände, dazu
        # zwölf frische der letzten Minuten.
        for name in sicherungen():
            os.remove(SICHERUNGEN / name)
        jetzt = time.time()
        erzeugt = {}
        for tag in range(30):
            for stunde in (8, 12, 18):
                zeitpunkt = datetime.now().replace(hour=stunde, minute=0, second=0, microsecond=0) - timedelta(days=tag)
                if zeitpunkt.timestamp() > jetzt - 3600:
                    continue
                pfad = SICHERUNGEN / f"liste_backup_{zeitpunkt:%Y%m%d_%H%M%S}_000000.json"
                pfad.write_text(json.dumps({"t": zeitpunkt.isoformat()}), encoding="utf-8")
                os.utime(pfad, (zeitpunkt.timestamp(), zeitpunkt.timestamp()))
                erzeugt[pfad.name] = zeitpunkt
        for minute in range(12):
            zeitpunkt = datetime.fromtimestamp(jetzt - 60 * (minute + 1))
            pfad = SICHERUNGEN / f"liste_backup_{zeitpunkt:%Y%m%d_%H%M%S}_{minute:06d}.json"
            pfad.write_text(json.dumps({"frisch": minute}), encoding="utf-8")
            os.utime(pfad, (zeitpunkt.timestamp(), zeitpunkt.timestamp()))
            erzeugt[pfad.name] = zeitpunkt
        app.prune_backups()
        bleibt = set(sicherungen())
        nach_alter = sorted(erzeugt, key=lambda name: erzeugt[name], reverse=True)
        neueste = set(nach_alter[:app.MIN_BACKUPS])
        frisch = {name for name in erzeugt if jetzt - erzeugt[name].timestamp() <= app.BACKUP_MAX_AGE_MINUTES * 60}
        heute = datetime.now().date()
        je_tag = {}
        for name in nach_alter:
            tag = erzeugt[name].date()
            if (heute - tag).days < app.BACKUP_DAILY_DAYS and tag not in je_tag:
                je_tag[tag] = name
        soll = neueste | frisch | set(je_tag.values())
        assert bleibt == soll, (sorted(bleibt ^ soll))
        # Kurz nach Mitternacht hat „heute“ unter Umständen noch keinen Stand.
        assert len(je_tag) >= app.BACKUP_DAILY_DAYS - 1, len(je_tag)
        assert not any((heute - erzeugt[name].date()).days >= app.BACKUP_DAILY_DAYS for name in bleibt
                       if name not in neueste), "nichts älter als 14 Tage außer den neuesten zehn"
        ergebnis["sicherungen_nach_rotation"] = len(bleibt)

        # --- 7. Startprüfung -----------------------------------------------------
        def neu_laden(inhalt):
            for name in os.listdir(SICHERUNGEN):
                if name.startswith(("liste_vor_format", "liste_unlesbar_")):
                    os.remove(SICHERUNGEN / name)
            SPEICHER.write_bytes(inhalt)
            app._data_read_only = False
            app._read_only_reason = "lock"
            meldungen.clear()
            app.load_items()
            ruhe()

        # a) Älteres Format: beim Start umgestellt, Vorsicherung bytegenau.
        alt_bytes = (REPO / "tests/fixtures/current_v17/reference_v17.json").read_bytes()
        neu_laden(alt_bytes)
        assert json.loads(SPEICHER.read_text(encoding="utf-8"))["version"] == app.DATA_SCHEMA_VERSION, \
            "Format beim Start umgestellt"
        vorsicherungen = [name for name in os.listdir(SICHERUNGEN) if name.startswith("liste_vor_format20_")]
        assert len(vorsicherungen) == 1 and (SICHERUNGEN / vorsicherungen[0]).read_bytes() == alt_bytes
        assert getattr(app, "_format_migration_notice", None), "Hinweis vorgemerkt"
        app.show_format_migration_notice()
        assert meldungen and meldungen[-1][0] == "Bestand umgestellt"
        # Ein zweiter Start findet nichts mehr umzustellen.
        stand = SPEICHER.read_bytes()
        app.load_items()
        ruhe()
        assert SPEICHER.read_bytes() == stand and not getattr(app, "_format_migration_notice", None)

        # b) Unbekannte Listenart: schreibgeschützt, Datei unverändert, keine Kopie.
        referenz = json.loads((REPO / "tests/fixtures/current_v20/reference_v20.json").read_text(encoding="utf-8"))
        referenz["lists"][0]["list_kind"] = "zukunft"
        zukunft = json.dumps(referenz, ensure_ascii=False, indent=4).encode("utf-8")
        neu_laden(zukunft)
        assert app._data_read_only and app._read_only_reason == "newer_format"
        assert meldungen and meldungen[-1][0] == "Bestand aus neuerer Glide-Version"
        assert app.save_items(show_error=False) is False and SPEICHER.read_bytes() == zukunft
        assert not [name for name in os.listdir(SICHERUNGEN) if name.startswith("liste_unlesbar_")]

        # c) Neueres Format: ebenso.
        referenz["lists"][0]["list_kind"] = "tasks"
        referenz["version"] = app.DATA_SCHEMA_VERSION + 1
        neuer = json.dumps(referenz, ensure_ascii=False, indent=4).encode("utf-8")
        neu_laden(neuer)
        assert app._data_read_only and app._read_only_reason == "newer_format"
        assert app.save_items(show_error=False) is False and SPEICHER.read_bytes() == neuer

        # d) Kaputte Dateien: gesichert, leer begonnen, danach speicherbar.
        for name, kaputt in (("abgeschnitten", alt_bytes[: len(alt_bytes) // 2]), ("leer", b""),
                             ("binaer", bytes(range(256)) * 40), ("tief", b"[" * 200000)):
            neu_laden(kaputt)
            kopien = [datei for datei in os.listdir(SICHERUNGEN) if datei.startswith("liste_unlesbar_")]
            assert len(kopien) == 1 and (SICHERUNGEN / kopien[0]).read_bytes() == kaputt, name
            assert not app._data_read_only, name
            assert app.save_items(show_error=False), name
            assert json.loads(SPEICHER.read_text(encoding="utf-8"))["version"] == app.DATA_SCHEMA_VERSION
            assert (SICHERUNGEN / kopien[0]).read_bytes() == kaputt, "die Kopie bleibt"

        # --- 8. Fehlendes Schreibrecht --------------------------------------------
        neu_laden(stand)
        if os.name != "nt":
            vorher_bytes = SPEICHER.read_bytes()
            os.chmod(ordner, 0o500)
            try:
                app.lists[0]["title"] = "Ohne Schreibrecht"
                assert app.save_items(show_error=False) is False
                assert SPEICHER.read_bytes() == vorher_bytes
            finally:
                os.chmod(ordner, 0o700)
            assert app.save_items(show_error=False)
        assert not fehler, fehler[:1]
    finally:
        try:
            os.chmod(ordner, 0o700)
        except OSError:
            pass
        try:
            root.destroy()
        except Exception:
            pass

print(f"test_speicherlast330: OK; {anzahl} Punkte ({groesse_mb:.1f} MB) gespeichert in {ergebnis['speichern_s']} s "
      f"und geladen in {ergebnis['laden_s']} s, 40 Änderungsrunden verlustfrei (Papierkorb übergelaufen: "
      f"{ergebnis['papierkorb_voll']}), {ergebnis['abbrueche']} harte "
      f"Abbrüche und {ergebnis['gelesen']} Lesezugriffe ohne halbe Datei, {ergebnis['parallel_gelesen']} Lesezugriffe "
      f"bei zwei Schreibern, Sperre, Sicherungen nur bei Änderung mit Tagesständen "
      f"({ergebnis['sicherungen_nach_rotation']} nach Rotation), Startprüfung, Schreibrechte.")
