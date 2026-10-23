# GitHub-Prüfung #138–#140 – Ursachen und Korrektur

23.10.2026 · Prüfwerkzeugnachlauf auf Glide 3.44.0 · App unverändert · kein Commit, kein Push

Auftrag des Inhabers: „Kannst du prüfen warum die Github Prüfung rot ist und das korrigieren?“

## Befund

Die Läufe #138 (`3ca7f09`), #139 (PR #38) und #140 (Merge `2ac339e` in `main`) der „Glide-Prüfung“ sind jeweils nur im Job „Vollprüfung (Windows x64, eigene Tk 9.1)“, Schritt „Vollprüfstand Windows“, rot. Grundstufe und Linux-Vollprüfung (eigene Tk 9.1) sind grün; #137 (`1042727`) war vollständig grün. Die Einzelbefunde stehen nur in den angemeldet lesbaren Rohprotokollen (am 23.10.2026 im Browser gelesen, nicht versioniert):

| Lauf | Rot | Meldung |
|---|---|---|
| #138 | `test_uiux_paket`, `test_schutzrunde` | b04 grün, danach `PermissionError: [WinError 32]` beim Löschen des Temp-Datenordners (Galeriebild `…haus-auf-statistik….jpeg`); `ROT sitzung: AssertionError()` |
| #139 | `test_uiux_paket`, `test_schutzrunde` | dieselben zwei Meldungen (Galeriebild `…haus-in-gelb….jpeg`) |
| #140 | `test_schutzrunde` | `ROT sitzung: AssertionError()` |

Der gelbe Hinweis der Grundstufe („25 Abweichungen zwischen src/glide und 07_Python-Versionen“) ist kein Fehler: Die Lieferung liegt nur im lokalen Commit `71854ec`.

## Ursachen

**`test_schutzrunde`, Fall `sitzung` (3/3 rot):** Der Fall wechselt den Datenordner und vergleicht den Pfad der Sperrdatei als Zeichenkette mit `Path(lauf.data).parent / 'ordnerwechsel' / 'glide.lock'`. `change_data_folder` legt den neuen Ordner aber über `os.path.realpath` ab. Der Windows-Runner liefert den Temp-Ordner unter dem 8.3-Kurznamen seines Benutzerordners (`RUNNER~1` statt `runneradmin`), `realpath` löst ihn zum langen Namen auf – derselbe Ordner, eine andere Zeichenkette. Bei Benutzernamen bis acht Zeichen ohne Leerzeichen entsteht kein Kurzname; deshalb waren die lokalen Windows-Läufe grün. Die App vergleicht Pfade selbst durchgehend normalisiert; kein Produktfehler.

**`test_uiux_paket`, Abbau nach b04 (2/3 rot):** Unter Windows wandelt ein PowerShell-Unterprozess JPEG-Vorschauen (WIC) und hält die Quelldatei offen. Auf dem Runner dauert das mehrere Sekunden („6 Vorschauen, 1 geladen“). `previews.close()` im Testabbau setzt nur das Abbruchsignal; der Worker bemerkt es binnen 0,1 s, beendet den Prozess und sammelt ihn ein. Der Test löschte den Datenordner vorher. Ein offenes Handle verhindert unter Windows das Löschen (WinError 32), unter Linux nicht – daher nur dort rot, und nur wenn eine Wandlung beim Abbau noch lief.

## Korrektur

- `tests/integration/test_schutzrunde.py`: Pfadvergleich über `gleicher_ort` (`os.path.normcase(os.path.realpath(…))`); die Rot-Meldung nennt jetzt die Zeile im Test (vorher nur `AssertionError()` ohne Ort).
- `tests/integration/test_uiux_paket.py`: `Lauf.vorschauen_beenden` schließt die Vorschauen und wartet bis zu 30 s auf den Konversions-Worker, bevor der Datenordner gelöscht wird.
- Prüfplan: Regel „Pfade und Aufräumen unter Windows“.

App, `src/glide` und `07_Python-Versionen` unverändert. Suiten vorher/nachher (SHA-256): `test_schutzrunde.py` `ec8f0c60…` → `61f611b0…`, `test_uiux_paket.py` `c2728634…` → `fcc7f7ae…`. Die Volläufe unten liefen mit `test_schutzrunde.py` `e0a333f7…`; danach wurde nur ein Docstring ohne Benutzerpfad formuliert und `sitzung` erneut grün geprüft.

## Nachstellung und Prüfung

Linux/Xvfb, Python 3.12, Tk 8.6.14, künstliche Daten. Windows selbst ist hier nicht prüfbar; beide Ursachen sind mit dem gleichen Mechanismus nachgestellt:

| Prüfung | Ergebnis |
|---|---|
| `sitzung`, Temp-Ordner hinter symbolischem Link (`TMPDIR`) – `realpath` ändert die Schreibweise wie unter Windows der Kurzname | alte Suite: `ROT sitzung (Zeile 770): AssertionError()`, also genau der Pfadvergleich; korrigierte Suite grün; ohne Link vorher und nachher grün |
| b04 mit erzwungenem Windows-Weg, langsamem Konverter, der die Datei offen hält, und Windows-Löschverhalten ([nachstellung_b04.py](nachstellung_b04.py)) | alte Suite: „6 Vorschauen, 1 geladen“, dann `PermissionError` beim Aufräumen wie im CI; korrigierte Suite grün |
| Vollständige Suiten am D55-Kandidaten (App `ff9b9cae…`) | `test_schutzrunde` 16/16 grün, auch mit verlinktem Temp-Ordner; `test_uiux_paket` 15/17 grün, rot nur b12_b13 und b16, die Tk 9 voraussetzen (unter Tk 8.6 schon in 3.44.0 rot, in der GitHub-Linux-Vollprüfung mit Tk 9.1 grün); `test_bildkonversion` 10/10 und `test_auftraege` grün (beide nutzen `Lauf` aus `test_schutzrunde`) |
| Vollständige Suiten an der Lieferung 3.44.0 (App `d0bf4142…`, Quellbaum `3ca7f09`, wie auf GitHub geprüft) | `test_schutzrunde` 16/16 grün mit verlinktem Temp-Ordner; `test_uiux_paket` 15/17 mit denselben zwei Tk-9-Fällen |
| Statische Prüfung | `pyflakes` ohne neue Meldung (je sechs ältere Hinweise vorher und nachher) |

## Grenzen

Grün auf GitHub wird die Prüfung erst nach einem Commit und Push dieser beiden Suiten; beides nur auf ausdrücklichen Auftrag. Eine echte Windows-Ausführung der korrigierten Suiten steht bis dahin aus.

Nebenbefund ohne Änderung (aus dem Code abgeleitet, nicht beobachtet): Auch beim Beenden der App setzt `close()` nur das Abbruchsignal. Endet der Python-Prozess, bevor der Worker es bemerkt (bis 0,1 s), läuft ein PowerShell-Prozess bis zum Ende seiner Wandlung weiter und kann eine verwaiste `glide-vorschau-*.png` im Vorschaucache hinterlassen. Ohne Risiko für Nutzerdaten; eine Produktänderung gehört in eine Produktionsrunde.
