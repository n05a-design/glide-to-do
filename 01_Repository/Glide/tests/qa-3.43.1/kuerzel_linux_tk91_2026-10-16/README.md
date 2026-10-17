# 3.43.1 – Kürzel in Listen unter Linux/Tk 9.1

Stand 16.10.2026 · Glide 3.43.1 · Datenformat 25 · Apphash `ed2b7eb64cc3fc14f00a4e909c7693c34102e46e393b5937158bb7d7e25176d3` · Windows 11 Pro, Python 3.14.7, Tk 9.0.4, künstliche Daten

Produktionsrunde auf Wunsch des Inhabers (16.10.2026). Anlass ist die GitHub-Vollprüfung „Linux/Xvfb, eigene Tk 9.1“, die seit [PR #26](https://github.com/n05a-design/glide-to-do/pull/26) rot war, nach [PR #29](https://github.com/n05a-design/glide-to-do/pull/29) nur noch durch drei Integrationssuiten und den Folgeschritt „Kalibrierte Erwartungen“. Maschinenlesbar: [ergebnis.json](ergebnis.json). Rohprotokolle bleiben lokal.

## Fehlermeldungen aus der CI

[Lauf 38930140166](https://github.com/n05a-design/glide-to-do/actions/runs/38930140166) auf `main` `8b59a8b`, Job „Vollprüfung (Linux/Xvfb, eigene Tk 9.1)“, angemeldet im Jobprotokoll gelesen:

| Suite | Stelle | Meldung |
|---|---|---|
| `test_tempo330` | Zeile 98, `grund = bildzeit(baum, packed=False, require_scroll=True)` | `AssertionError: Scrollereignisse bewegen die lange Prüfansicht nicht` – die Vergleichsansicht aus reinem Tk, nicht Glide |
| `test_planen33313` | Zeile 191, `popup(lambda: app.tree.event_generate("<Control-Shift-P>"))` | `AssertionError: Einplanen-Menü wurde nicht geöffnet` |
| `test_oberflaeche33321` | Zeile 114, nach `neu_starten()` | `AssertionError` bei `app.design_name() == "pixel"` |
| „Kalibrierte Erwartungen“ | `linux_gegenproben.py` | 16 Muster passend rot; `scrollen` und `datum` fehlen, weil ihre Basissuiten (`test_tempo330`, `test_planen33313`) nicht grün waren |

## Ursachen und Entscheidung je Suite

**`test_tempo330` – nur der Test (Prüfwerkzeug).** Die Vergleichsansicht erzeugte unter Linux `<Button-4>`/`<Button-5>`. Tk 9 liest diese Muster als Maustaste 8/9 (`GetButtonNumber` in `tkBind.c` am Tk-Pin `3f45110c`; lokal unter Tk 9.0.4 belegt: erzeugtes `<Button-5>` kommt als Taste 9 an). Nur echte X11-Radtasten 4–7 wandelt `Tk_HandleEvent` in `<MouseWheel>` mit ±120. Die Treeview ohne Glide scrollte deshalb nicht. Glide selbst bindet `<MouseWheel>` und reagiert auf das echte Rad richtig. Korrektur: Unter Tk 9 erzeugt die Vergleichsansicht auch unter Linux `<MouseWheel>`; Tk 8 behält `<Button-4/5>`.

**`test_oberflaeche33321` – nur der Test (Prüfisolation).** Die Suite ersetzte die Systemerkennung erst nach dem Neustart. Unter Xvfb ohne Fenstermanager bekommt das neue Hauptfenster sofort `<FocusIn>`; Glide fragt dann `gsettings`, bekommt im Prüfstand „hell“ (sonst wäre Pixel stehen geblieben) und folgt richtig dem System. Die Erwartung „Pixel“ galt aber dem simulierten dunklen System. Unter Windows nachgestellt (Erkennung „hell“, `<FocusIn>` beim Start): vorher rot an Zeile 114 wie in der CI, nachher grün. Korrektur: Ersatz auf Klassenebene vor dem ersten Fenster; die echte Erkennung wird weiter einmal aufgerufen.

**`test_planen33313` – Glide reagiert falsch (App-Korrektur 3.43.1).** Unter X11 legt Tk Strg+A/B/E/F/N/P, mit Umschalt erweiternd, zusätzlich auf Emacs-Navigation, hier `<Control-P>` auf `<<SelectPrevLine>>` (`::tk::EventMotifBindings` in `tk.tcl`). Bis Tk 9.0 band die Treeview nur Pfeiltasten; seit 9.1 bindet sie `<<SelectPrevLine>>` an `ttk::treeview::KeyNav up extend`. Die Treeview-Klasse läuft vor Glides Fensterbindung, setzte die Auswahl auf den Vorgänger der Fokuszeile – in „Heute“ die Abschnittszeile `section:timeplan` – und Glides „Einplanen“ fand keine planbare Aufgabe mehr. Eine echte Strg+Umschalt+P-Taste nimmt denselben Weg; betroffen sind alle Strg-Buchstaben-Kürzel Glides in Listen (u. a. Strg+A/E/F/N/P). Strg+Umschalt+T (`test_tagpaket33314`, unter Linux grün) hat keine Emacs-Belegung, deshalb fiel es nur hier auf. Unter Windows nachgestellt (Emacs-Ereignis plus Tk-9.1-Klassenbindung): an derselben Stelle rot mit derselben Meldung.

Korrektur: Tk-freie Regel in `interaction_policy.py` (`is_emacs_trigger`, `emacs_guarded_events`, `guard_emacs_script`). `ListApp.guard_x11_emacs_navigation` wendet sie beim Start unter X11 auf die Treeview-Klasse an: Navigationsereignisse mit Strg-Buchstaben-Auslöser bekommen eine Klassenbindung, die bei einem einzelnen Buchstaben (`%K`) nichts tut und sonst unverändert wirkt, ohne `break`. Pfeiltasten, Pos1/Ende, unmittelbar erzeugte virtuelle Ereignisse, Text- und Eingabefelder bleiben wie bisher; Windows und macOS bleiben unberührt. Das stellt für die Treeview das Verhalten bis Tk 9.0 wieder her.

## Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Unit-Tests `test_interaction_policy.py` | 9 grün (3 neu: Emacs-Auslöser, Auswahl der Navigationsereignisse, idempotente Schutzbindung) |
| `test_planen33313` (3.43.1) | grün; stellt den Tk-9.1-Tastenweg nach, wo Tk ihn nicht selbst hat, und verlangt nach Strg+Umschalt+P die unveränderte Auswahl |
| Rote Gegenprobe `test_planen33313 --app` gegen den 3.43.0-Quellbaum (`git archive 5674936`) | rot an derselben Stelle wie in der CI: `Einplanen-Menü wurde nicht geöffnet` |
| `test_tempo330`, `test_oberflaeche33321` | grün; Simulation „System hell + `<FocusIn>`“ für `test_oberflaeche33321` vorher rot (Zeile 114), nachher grün |
| `linux_gegenproben.py --fall scrollen` und `--fall datum` (unter Windows, ohne Xvfb) | beide passend rot |
| Eingefrorene Vollprüfung | `pruefen.py --modus voll --timeout 900` auf einer Kopie außerhalb von OneDrive (ohne `.git`, `.claude`, `build`, `skills-main`), Apphash `ed2b7eb6`: 111 Schritte, 108 grün, Sichtprüfung wie immer übersprungen – 91 von 92 Integrationssuiten (darunter `test_planen33313`, `test_tempo330`, `test_oberflaeche33321`, `test_template_workflows`), 714 Units, Beispiel-/Releasedaten-Abgleich, Showcase, Bilder und vier Analysen. Rot: `standpruefung` nur, weil der Kopie `.claude/skills` fehlte (die Standprüfung liest die versionierte Design-Referenz) – auf der ergänzten Kopie grün; `test_tag3390` („Speichern nicht sichtbar“ im Dialog „Kalender als Belegzeiten“, im zweiten Lauf Fokusprüfung Zeile 297) – abwechselnd wiederholt unter 3.43.1 und 3.43.0 (`5674936`) je zweimal rot an denselben Stellen, also nicht durch 3.43.1; in der 3.43.0-Vollprüfung vom 16.10. war sie grün, ebenso in der GitHub-Windows-Vollprüfung nach dem Merge (Lauf 38979558948). Ein erster Lauf brach nach 43 Schritten mit einem Sitzungsende ab. |
| CI-Grundstufe | bestanden, Exit 0, 19 Schritte: Syntax (307 Quelldateien), Versionen 3.43.1/Format 25, 188 Dokumentlinks, 152 Werkzeugtests, 714 Units auch ohne Systemzeitzonen, fünf Analysen, Startprobe, Lieferstand bytegleich, Fremdcode, Datenschutz, Ablagegröße (Nachweise und Archive der sieben neuesten Versionen), Synchronisation ([Protokoll](grundstufe.json)) |
| Lieferabgleich | `abgleich_07.py`: 67 Code-/146 Ressourcendateien in `07_Python-Versionen` bytegleich (Apphash `ed2b7eb6`), 3.43.0 ins Archiv; `showcase_abgleich.py` grün, sechs Dateien nach `05_Probelisten_Testdaten/Showcase`; `packaging/macos/baue_app.py` unter Windows nicht ausführbar |

## Wackelige Suite `test_template_workflows` (vorbestehend)

Im ersten, durch ein Sitzungsende nach 43 Schritten abgebrochenen Volllauf war `test_template_workflows` rot, im zweiten grün: Das Auswahl-Popup eines Optionsfelds war beim Hervorheben schon geschlossen (`invalid command name …dropdownpopup…`). Einzeln mit `PYTHONUTF8=1` wie im Prüfstand, abwechselnd unter denselben Bedingungen: 3.43.1 viermal grün und dreimal rot, 3.43.0 (`git archive 5674936`, kurzer Pfad) fünfmal grün und einmal rot – dort schloss sich das Popup sogar direkt nach dem Öffnen (`assert field._popup is not None`). Der Fehler tritt also in beiden Fassungen auf; die Korrektur greift unter Windows nicht (`guard_x11_emacs_navigation` endet dort vor jeder Bindung). Vermutlich nimmt ein Fokuswechsel auf dem Desktop dem Popup den Fokus. Nicht behoben, als Beobachtung für die Prüfstandspflege festgehalten. Nebenbei: Ohne `PYTHONUTF8=1` scheitert die Suite schon an Zeile 49 (Vorlagen-Erzeuger liest im Gebietsschema), und unter einem Pfad über 260 Zeichen findet 3.43.0 seine Vorlagendatei nicht (lange Pfade sind auf diesem Rechner aus).

## Nebenbefund (ohne Änderung)

Glide bindet weiterhin `<Button-4>`/`<Button-5>` für das Rad unter Tk 8. Unter Tk 9 treffen diese Bindungen die Seitentasten 8/9 der Maus; sie tun dort nichts (kein Scrollschritt, `break`). Das echte Rad läuft unter Tk 9 über `<MouseWheel>`. Kein Fehlverhalten, nur toter Bindungsweg.

## Offen

- **`test_tag3390`:** lokal unter 3.43.1 und 3.43.0 gleich rot, in der GitHub-Windows-Vollprüfung grün; lokale Ursache in der Prüfstandspflege (PS-01) klären.
- **GitHub-Bestätigung – erledigt 17.10.2026:** [Lauf 38979558948](https://github.com/n05a-design/glide-to-do/actions/runs/38979558948) auf `main` (`eb5658c`, Merge von PR #32): Grundstufe, Vollprüfung Linux mit eigener Tk 9.1 einschließlich „Kalibrierte Erwartungen“, Vollprüfung Windows und Windows-Paket grün. Damit sind die X11-Wege nativ unter Linux bestätigt.
- **macOS:** Mac-Vollprüfung und `packaging/macos/baue_app.py` auf dem Referenz-Mac; Mac-Bundle und eigenständige Pakete tragen bis dahin 3.42.0.
- **Menschenabnahme:** echte Tastatur unter Linux (Strg+Umschalt+P, Strg+N/P/A/E/F in Listen) nach der [Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md).
