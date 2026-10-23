# GitHub-Prüfung #138–#142 – Ursachen und Korrekturen

23.10.2026 · Glide 3.44.0 mit D55-Kandidat · beide Runden auf Auftrag gepusht

Aufträge des Inhabers: „Kannst du prüfen warum die Github Prüfung rot ist und das korrigieren?“; danach „du kannst jetzt auch alles pushen als Zwischenstand“.

## Erste Runde: #138–#140

Die Läufe #138 (`3ca7f09`), #139 (PR #38) und #140 (Merge `2ac339e` in `main`) der „Glide-Prüfung“ sind jeweils nur im Job „Vollprüfung (Windows x64, eigene Tk 9.1)“, Schritt „Vollprüfstand Windows“, rot. Grundstufe und Linux-Vollprüfung (eigene Tk 9.1) sind grün; #137 (`1042727`) war vollständig grün. Die Einzelbefunde stehen nur in den angemeldet lesbaren Rohprotokollen (im Browser gelesen, nicht versioniert):

| Lauf | Rot | Meldung |
|---|---|---|
| #138 | `test_uiux_paket`, `test_schutzrunde` | b04 grün, danach `PermissionError: [WinError 32]` beim Löschen des Temp-Datenordners (Galeriebild `…haus-auf-statistik….jpeg`); `ROT sitzung: AssertionError()` |
| #139 | `test_uiux_paket`, `test_schutzrunde` | dieselben zwei Meldungen (Galeriebild `…haus-in-gelb….jpeg`) |
| #140 | `test_schutzrunde` | `ROT sitzung: AssertionError()` |

Der gelbe Hinweis der Grundstufe („25 Abweichungen zwischen src/glide und 07_Python-Versionen“) ist kein Fehler: Die Lieferung lag nur im lokalen Commit `71854ec`.

**`test_schutzrunde`, Fall `sitzung` (3/3 rot):** Der Fall wechselt den Datenordner und vergleicht den Pfad der Sperrdatei als Zeichenkette mit `Path(lauf.data).parent / 'ordnerwechsel' / 'glide.lock'`. `change_data_folder` legt den neuen Ordner aber über `os.path.realpath` ab. Der Windows-Runner liefert den Temp-Ordner unter dem 8.3-Kurznamen seines Benutzerordners (`RUNNER~1` statt `runneradmin`), `realpath` löst ihn zum langen Namen auf – derselbe Ordner, eine andere Zeichenkette. Bei Benutzernamen bis acht Zeichen ohne Leerzeichen entsteht kein Kurzname; deshalb waren die lokalen Windows-Läufe grün. Die App vergleicht Pfade selbst durchgehend normalisiert; kein Produktfehler. Korrektur: Vergleich über `gleicher_ort` (`os.path.normcase(os.path.realpath(…))`); die Rot-Meldung nennt jetzt die Zeile im Test (vorher nur `AssertionError()` ohne Ort).

**`test_uiux_paket`, Abbau nach b04 (2/3 rot):** Unter Windows wandelt ein PowerShell-Unterprozess JPEG-Vorschauen (WIC) und hält die Quelldatei offen. Auf dem Runner dauert das mehrere Sekunden („6 Vorschauen, 1 geladen“). `previews.close()` im Testabbau setzt nur das Abbruchsignal; der Worker bemerkt es binnen 0,1 s, beendet den Prozess und sammelt ihn ein. Der Test löschte den Datenordner vorher. Ein offenes Handle verhindert unter Windows das Löschen (WinError 32), unter Linux nicht. Korrektur: `Lauf.vorschauen_beenden` schließt die Vorschauen und wartet bis zu 30 s auf den Konversions-Worker.

Nachgestellt unter Linux/Xvfb (Python 3.12, Tk 8.6.14, künstliche Daten) mit demselben Mechanismus: `sitzung` mit Temp-Ordner hinter einem symbolischen Link (alte Suite `ROT sitzung (Zeile 770)`, also genau der Pfadvergleich; korrigiert grün); b04 mit erzwungenem Windows-Weg, langsamem Konverter und Windows-Löschverhalten ([nachstellung_b04.py](nachstellung_b04.py); alt „6 Vorschauen, 1 geladen“ und `PermissionError` wie im CI, korrigiert grün). Volle Suiten an D55-Kandidat und an der Lieferung 3.44.0 (`d0bf4142…`): `test_schutzrunde` 16/16, `test_uiux_paket` 15/17 (rot nur b12_b13 und b16, die Tk 9 voraussetzen), `test_bildkonversion` 10/10, `test_auftraege` grün.

Gepusht auf Auftrag als `f52b024` (`claude/windows-pruefung-3.44.0`, nur diese Korrektur auf `main`) und `079ba4b` in `claude/arbeitsstand-d55` (Zwischenstand mit D55, `abacead`).

## Zweite Runde: #141 und #142

| Lauf | Job | Rot | Ursache |
|---|---|---|---|
| #141 (`f52b024`) | Windows | `test_schutzrunde` `struktur_ergebnis (Zeile 951)` | Sekundenwettlauf im Test, siehe unten |
| #141 | Linux | `test_markdownbaum` `showcase`: „Quelldateien durch Ausgabe verändert: liste_speicher.json“ | Erinnerung aus dem Showcase während des Exports zugestellt |
| #142 (`abacead`) | Linux und Windows | `test_bilder330`: `'types.SimpleNamespace' object has no attribute 'desktop_bounds'` | **Produktfehler im D55-Kandidaten**, siehe unten |
| #142 | Linux und Windows | `test_seitenkarten` `altleser_backup`, `test_ansichten` `altleser`/`altfilter`: `FileNotFoundError …v3.43.1.pyw`; `test_wiederholungsregeln` `altleser`/`altregeln`: `No module named 'drawing'` | Vorversion 3.43.1 seit der Lieferung `71854ec` im `Archiv` |
| #142 | Linux | `test_markdownbaum` `showcase` | wie #141 |
| #142 | Linux, Schritt „Kalibrierte Erwartungen gegen Defekte“ | `Mutation inspektor-mindestgroesse ist nicht mehr eindeutig` | D55: die Nebenansicht prüft dieselbe Mindestbreite |

In beiden Läufen sind die Befunde der ersten Runde behoben: `sitzung` und `test_uiux_paket` sind unter Windows grün. `test_arbeitsmodi` (D55) ist unter Linux und Windows mit Tk 9.1 grün.

**Startfenster (D55, Produktfehler):** `show_start_window` klemmt die gespeicherte Fensterlage vor dem Aufbau von `ListApp` über `ListApp.clamp_geometry(types.SimpleNamespace(root=root), …)`. D55 ließ `clamp_geometry` die neue Methode `desktop_bounds` aufrufen, die dieses Ersatzobjekt nicht hat. Jeder Start des D55-Quellstands mit vorhandener `window.conf` wäre mit `AttributeError` abgebrochen. Die gelieferte 3.44.0 in `07_Python-Versionen` ist nicht betroffen. Lokal unentdeckt, weil an der Abschluss-App nur `test_arbeitsmodi`, `test_glide` und `test_fenster330` liefen. Korrektur: `desktop_bounds(root)` als Modulfunktion, die Methode delegiert; `test_glide` prüft jetzt den Aufruf mit einem Ersatzobjekt, das nur `root` trägt.

**Altleser nach der Archivierung:** Zwei Suiten erwarteten 3.43.1 fest im Hauptordner von `07_Python-Versionen`, eine fand sie im `Archiv`, lud sie aber ohne die Begleitmodule eine Ebene höher. Korrektur nach dem Ladeweg aus dem Archiv-README (wie `test_animation3400`/`test_import3410`): `vorversion.finden` statt festem Pfad, `Lauf` und die Kindprozesse ergänzen bei einer archivierten Hauptdatei den übergeordneten Modulordner.

**Showcase-Erinnerung:** Der Showcase (Stichtag 22.10.2026) enthält „Projektstatus besprechen“, fällig 23.10., 09:00, Erinnerung 30 Minuten vorher, noch nicht zugestellt. Seit 23.10., 08:30 Uhr ist sie fällig; die Erinnerungsprüfung (alle 15 s) stellt sie zu und speichert. Fiel der erste Takt nach dem Laden in den Export, änderte sich `liste_speicher.json`. Ab dem 24.10. folgen täglich weitere solche Termine. Korrektur: Der Bytevergleich pausiert die Zustellung (`process_reminders`) wie bereits die Vorschauwandlung.

**`struktur_ergebnis`:** Der Test ließ jedes Schreiben scheitern, auch das der Sperrdatei. `restore_trash_entry` erneuert vor jeder Änderung die Sperrdatei, höchstens einmal je Sekunde. Sprang die Uhr zwischen Papierkorb und Wiederherstellung in die nächste Sekunde, brach die Wiederherstellung schon an der Sperrdatei ab, und `app.dirty` blieb falsch. Korrektur: Nur die Hauptdatei sperren, wie in `fall_speicherergebnis`.

**Gegenprobe:** Die Mutation trifft jetzt mit der Vorzeile nur noch den Aufgabeninspektor (in D55 und 3.44.0 je einmal vorhanden).

### Nachstellung und Prüfung der zweiten Runde

Linux/Xvfb, Python 3.12, Tk 8.6.14, künstliche Daten:

| Prüfung | Ergebnis |
|---|---|
| `struktur_ergebnis` mit erzwungener Sperrdatei-Erneuerung vor der Wiederherstellung | alte Suite `ROT struktur_ergebnis (Zeile 952)` (CI-Zeile 951 plus eine eingefügte Zeile), korrigiert grün |
| `test_markdownbaum` `showcase`, erster Zustelltakt erst während des Exports | alte Suite „Quelldateien durch Ausgabe verändert: liste_speicher.json“ wie im CI, korrigiert grün |
| `test_bilder330`, `test_glide` | grün |
| `test_seitenkarten`, `test_ansichten`, `test_wiederholungsregeln` | grün einschließlich aller Altleser-Fälle |
| `linux_gegenproben.py --fall inspektor-mindestgroesse` | „passend rot“ |
| Vollständiger Prüflauf (`pruefen.py --modus voll`) an App `bd21317e…` mit allen Korrekturen ([Zusammenfassung](vollpruefung_linux_bd21317e.json)) | 121 Schritte: 114 ausgeführt, 6 rot, Sichtprüfung übersprungen. Rot nur unter Linux/Tk 8.6 bzw. im Container bekannte Fälle, auf 3.44.0 ebenso rot und in der GitHub-Linux-Vollprüfung mit Tk 9.1 grün: `test_uiux_paket` b12_b13/b16 (Tk 9), `test_aufgaben3380` (121 statt ≤ 120 px mit DejaVu), `test_erwaehnungen` `oeffnen_fallen`, `test_speicherlast330`, `test_features330` (Zeitgrenze 8 s, hier 14,5 s). Dazu einmal `test_hintergrund330` („sofort aus dem Zwischenspeicher“), einzeln danach 2/2 grün; der Hintergrundcode ist seit 3.44.0 unverändert. Mechanismus aus dem Code, nicht belegt: `wait_for_backdrop` wartet höchstens 30 s, ist der Verlauf unter Last bis dahin nicht gerechnet, fehlt die Cache-Datei für die spätere Sofortprüfung (Befundklasse WA-42). Alle in #141/#142 roten Suiten grün |

## Grenzen

Die zweite Runde ist am 24.10.2026 auf Auftrag („pushen“) nachgepusht: `c40d431` in `claude/windows-pruefung-3.44.0`, `be849a1` (dieselben Testkorrekturen) und `d461f89` (Startfenster, Dokumente) in `claude/arbeitsstand-d55`. Vor dem Push auf dem `main`-Stand gezielt geprüft (`struktur_ergebnis`, `showcase`, drei Altleser-Fälle mit 3.43.1 noch im Hauptordner, Gegenprobe): grün. Windows-Ausführung und Tk 9.1 zeigen erst die neuen GitHub-Läufe.

Nebenbefund ohne Änderung (aus dem Code abgeleitet, nicht beobachtet): Auch beim Beenden der App setzt `close()` nur das Abbruchsignal. Endet der Python-Prozess, bevor der Worker es bemerkt (bis 0,1 s), läuft ein PowerShell-Prozess bis zum Ende seiner Wandlung weiter und kann eine verwaiste `glide-vorschau-*.png` im Vorschaucache hinterlassen. Ohne Risiko für Nutzerdaten; eine Produktänderung gehört in eine Produktionsrunde.
