# MacBook-M2-Gegenlauf und Pinnwandzoom mit `nsimage`

Stand 31.10.2026 · Quelle 3.49.0 (Prüfkandidat) · Aufgabenformat 26 · MacBook Air M2 (Mac14,2), 8 GiB, macOS 27.2, Python 3.14.5 / Tk 9.0.3, künstliche Daten.

Auftrag 31.10.2026 (Claude-Code-Sitzung am M2): Prüfsituation auswerten, die zwei noch nicht eingeordneten M2-Gegenläufe vom 29.10. abends dokumentieren und den dabei gefundenen macOS-Fehler beheben. Kein Versions-, Liefer- oder Gitschritt. Die Korrektur entstand im isolierten Worktree, während Codex im Hauptordner das [Abschlussaudit](../abschlussaudit_2026-10-31/README.md) abschloss. Übernommen wurde sie erst nach dessen Ende.

## Gegenläufe 29.10.2026 abends (App `39499ab3…`)

Gestartet mit `13_TK-Test-Umgebung/Macbook-M2/lauf_starten.sh`: eingefrorene Prüfkopie, `gesichert_pruefen.py --art voll --timeout 900`, Stopp beim ersten Fehler. Flache Belege lokal unter `13_TK-Test-Umgebung/Macbook-M2/m1029-*`.

| Lauf | Ergebnis |
|---|---|
| `m1029-215410`, 21:54–21:55 | 16 Schritte, 15 grün. `test_release36` rot: Nach dem Umbenennen steht der neue Titel nicht im Punkt (Zeile 166, Eingabe per `focus_force`/`<Return>`). Im Erstlauf und im Folgelauf grün. Vermutlich fokusabhängig, weil der Mac direkt nach dem Start noch bedient wurde; nicht bewiesen. |
| `m1029-221858`, 22:19–23:01 | 105 Schritte, **104 grün**: sieben Vorstufen und 97 von 98 erreichten Integrationssuiten, darunter `test_speicherlast330` und alle 18 im [Gerätevergleich](../geraetevergleich_2026-10-29/README.md) korrigierten Suiten. Kein Interpreterabbruch. Rot nur `test_seitenkarten`, Fall `titelbild_praesentation_sicherung`. |

Nicht erreicht wurden die zehn letzten Suiten (`test_ansichten` bis `test_vollpruefung325`) sowie Showcase, Analysen und Reproduktionen.

## Befund: Pinnwandzoom bricht unter macOS mit Bildkarten ab

`scale_board_view` skalierte Kartenbilder mit `zoom()`/`subsample()`. Diese Methoden gibt es nur beim Bildtyp `photo`. Unter macOS mit Tk 9 lädt `image_preview` Vorschauen jedoch als `nsimage`, und das hat keines von beiden. Deshalb brach jede Pinnwand- oder Präsentationsdarstellung mit Zoom ungleich 100 % ab, sobald eine Karte eine Bildvorschau oder ein Titelbild zeigte (`AttributeError: 'Image' object has no attribute 'zoom'`). Windows und Linux laden `photo` und sind nicht betroffen.

Die Stelle steht seit dem ersten Commit im Code. Sie ist in der gelieferten Python-Fassung 3.47.0 (und in den Archivständen) enthalten. Das Mac-Paket 3.45.0 (PyInstaller mit Tcl/Tk 9) ist nach Quellstand ebenfalls betroffen; im Paket selbst wurde das nicht ausgeführt. Frühere Mac-Läufe erreichten den Fall nicht: Im Erstlauf vom 29.10. überschritt `test_seitenkarten` das Zeitlimit.

## Korrektur

`pinboard_pages.zoomed_image(kind, width, height, factor)` entscheidet Tk-frei (D17): `photo` wie bisher in Vierteln über zoom/subsample, `nsimage` neu aus derselben Quelle in Zielgröße, andere Typen bleiben unskaliert, statt die Zeichnung abzubrechen. `scale_board_view` übernimmt bei `nsimage` `-source`/`-as` des Vorschaubilds. Kein Format-, Daten- oder Oberflächenvertragswechsel. Neuer Unit-Fall `test_zoomed_image_by_type`.

App-SHA-256 im Hauptordner (CRLF, Zählweise wie `39499ab3…`) jetzt `ce4fe362ee640c7803fc25234eb8d5bd4c4dad24022459480893449ad5404e0e`; geprüfter LF-Stand im Worktree `4f0b6b15…`, inhaltlich gleich. `pinboard_pages.py` `7c495aaa…`.

## Prüfung auf dem M2

Je Suite eigener Prozess, eigenes `GLIDE_DATA_DIR` und kurze Ablage unter `~/gq`. [Ergebnis](ergebnis.json).

- **Rot vorher:** Fall `titelbild_praesentation_sicherung` mit der alten Fassung, gleicher Stack wie im Gegenlauf. Zoomprobe gegen die alte Fassung bricht bei 50 % ab.
- **Grün nachher:** derselbe Fall; Zoomprobe mit Titelbild 24 × 16: 100/50/150/200 % ergeben `nsimage` 24 × 16, 12 × 8, 36 × 24, 48 × 32.
- **Gezielt:** 1.076 Fachtests grün (ein Skip). Grün sind auch `test_seitenkarten` mit allen sechs Fällen in 487 s sowie `test_bilder330`, `test_wissen3340`, `test_paketierung330`, `test_features326`, `test_features330` und `test_oberflaeche33321`. Nach Übernahme im Hauptordner erneut Unit-Fall, Präsentationsfall und Zoomprobe grün.
- **CI-Grundstufe im Hauptordner nach Übernahme bestanden:** 17 Schritte ausgeführt, darunter Werkzeug- und Fachtests (auch ohne Systemzeitzonen), fünf Analysen, Startprobe, Datenschutz und Ablagegröße. Zwei Hinweise: 14 Lieferabstände (bisher 13, neu `pinboard_pages.py`, erwartet bis zur Lieferung) und Fremdcodeabruf wegen lokalem TLS-Zertifikatsfehler nicht möglich.
- **Erster Fachlauf rot, umgebungsbedingt:** 14 Fälle in `test_markdown_tree`, weil der Temp-Pfad im Sitzungs-Scratchpad die Exportgrenze von 130 Zeichen überschritt (Regel in `CLAUDE.md`). Mit kurzem Pfad unter `~/gq` grün; kein Produktbefund.

## Eingefrorener M2-Volllauf 31.10.2026 (App `a6a78c41…`)

Auf Nutzerauftrag nach Ende der parallelen Codex-Arbeit gestartet: `lauf_starten.sh`, python.org-Python 3.14.5 / Tk 9.0.3, Akku, Mac unbedient, 14:17–15:06. Eingefroren wurde der aktuelle Hauptstand mit Codex' Fortsetzung §21.37 und dieser Korrektur; Quelle während des Laufs unverändert, Prüfkopie gleich (2.107 Dateien). Flache Belege lokal unter `13_TK-Test-Umgebung/Macbook-M2/m1031-141726`.

**Ergebnis: 125 von 125 Schritten grün, Exitcode 0.** Grün sind die sieben Vorstufen mit 1.081 Fachtests (ein Skip) und **alle 108 registrierten Integrationssuiten**, darunter die zehn bisher auf dem M2 nie erreichten (`test_ansichten` bis `test_vollpruefung325`), `test_speicherlast330` (98 s), `test_release36` und `test_seitenkarten` mit allen sechs Fällen. Ebenfalls grün: Showcase einschließlich Neustart, fünf Analysen, Erzeugen und Abgleich von Beispiel- und Releasedaten. Kein Interpreterabbruch, kein Python-Absturzbericht. `release_ready` bleibt `false`: keine Lieferung, kein Paketstart, keine Menschenabnahme.

Damit ist es der erste vollständig grüne eingefrorene Volllauf eines 3.49.0-Stands auf einem der drei Geräte. Er gilt für App `a6a78c41…` und nicht rückwirkend für `39499ab3…` oder `ce4fe362…`.

**Codex-Lauf zuvor, eingeordnet:** Codex' eigener Mac-Lauf `~/gq/v31/lauf-s4y_mu2b` mit selbst gebauter Tcl/Tk 9.1 endete um 13:49 in `test_speicherlast330` ohne Ergebnis. Der macOS-Absturzbericht von 13:51 zeigt `SIGSEGV` erst nach einem Signal während `time.sleep`. Der Tk-9.1-Signalhandler rief `Tcl_Exit` auf, beim Fensterabbau lief ein Python-Rückruf ohne Threadzustand. Der Prozess hing bereits an `launchd`, sein Starter war also beendet. Das spricht für einen Abbruch von außen, nicht für WA-41A; bewiesen ist es nicht. Nicht wiederholt.

## Eingrenzung Seitenkarten-Tempo 31.10.2026

Auf Nutzerauftrag gemessen, nichts geändert. App `a6a78c41…`, Python 3.14.5 / Tk 9.0.3, je Messung frischer Prozess und eigenes `GLIDE_DATA_DIR`. Messskripte lokal unter `13_TK-Test-Umgebung/Macbook-M2/g1031-seitenkarten-tempo`.

| Messung | Ergebnis |
|---|---|
| `test_seitenkarten --fall druck_tempo` allein | 62 ms je Darstellung, Fall in 5 s grün |
| Dieselbe Zeichnung achtmal in einer App | konstant rund 60 ms, Tk-Fontzahl gleichbleibend (39) |
| `druck_tempo` nach `inhalt_undo`, `archiv_loeschen`, `auswahl_ziehen` oder `altleser_backup` im selben Prozess | 59–60 ms |
| `druck_tempo` nach `titelbild_praesentation_sicherung` | 26,8 s Median |
| Nach einer früheren Instanz, die nur die Startseite zeigte (`set_home_view`) | 16,8 s je Zeichnung; nur Titelbild bzw. nur Präsentation ebenfalls langsam, beide öffnen vorher die Startseite |
| Startseite und danach Pinnwand **in derselben App** | 60–61 ms vorher, 62–71 ms nachher |

**Einordnung:** Die Verlangsamung entsteht nur, wenn im selben Prozess eine neue Tk-Instanz die Pinnwand zeichnet, nachdem eine frühere Instanz die Startseite gezeigt hat. Genau so arbeitet die Suite (je Fall `Lauf` mit neuem Interpreter). Glide selbst legt je Prozess nur eine Tk-Instanz an; `runtime_check.melden` öffnet nur im Fehlerfall ein Meldungsfenster vor dem Ende. Im normalen Betrieb ist der Fall deshalb nicht belegt, betroffen ist der Prüfablauf auf dem Mac. Die relative Grenze der Suite (+10 %) besteht trotzdem, weil beide Messreihen gleich verlangsamt sind; Windows ist mit rund 150 ms nicht betroffen.

**Mechanismus, soweit belegt:** Python-Stack `draw_card` → `Canvas.create_text`; native Stichprobe `Tk_AllocFontFromObj` → `+[NSFont fontWithName:size:]` → CoreText-Matching. Glide nutzt „DejaVu Sans“, beim Start per `CTFontManagerRegisterFontsForURL` prozessweit registriert. Jede Karte legt neue benannte Fonts an; im langsamen Fall kostet jedes Nachschlagen rund 21 ms statt 0,1 ms. Eine reine Tk-Reproduktion ohne Glide (zwei Instanzen, registrierte DejaVu Sans, benannte Fonts, `font families`, Pixelify Sans, gelöschte benannte Fonts) bleibt bei 12–14 ms. Der konkrete Auslöser in der Startseite ist deshalb nicht isoliert. Eine Tcl-Spur der Startseite zeigt nur `font create/config/delete/measure`, `tk scaling` (lesend) und `winfo`.

**Folgerung:** Kein Produktfehler belegt, keine spekulative Änderung (kein Fontcache).

**Prüfadapter umgestellt (Nutzerentscheidung 31.10.2026):** `test_seitenkarten` führt `druck_tempo` im Gesamtlauf über den vorhandenen Schalter `--fall` in einem eigenen Prozess aus (`EIGENER_PROZESS`, `fall_im_eigenen_prozess`). Fallfolge, Messung, Grenze +10 % und Bericht sind unverändert, ein Einzelaufruf mit `--fall` arbeitet wie bisher. Fehlt der Kindbericht oder läuft das Zeitlimit von 840 s ab, ist der Fall rot (Fehlerweg gezielt geprüft). Auf dem M2 dreimal grün: Suite 24–26 s statt 485 s, `druck_tempo` 60–66 ms je Darstellung, Verhältnis 0,99. Suite-SHA-256 `a8d7ce6f…`, App unverändert `a6a78c41…`.

## Tk-9.1-Volllauf und Emacs-Schutz unter macOS 31.10.2026

Fortsetzung des abgebrochenen Codex-Laufs: eingefroren mit `pruefen.py --modus voll --zugang-nativ`, Prozesswächter wie `gesichert_pruefen.py`, python.org-Python 3.14.5 mit Codex' selbst gebauter `_tkinter`-Erweiterung für Tcl/Tk 9.1.0 (`PYTHONPATH`), Akku, unbedient. Starter `voll_tk91.py` und flache Belege lokal unter `13_TK-Test-Umgebung/Macbook-M2/` (`t1031-162149`, `t1031-164116`).

**Erster Lauf `t1031-162149` (App `a6a78c41…`) rot:** 77 von 78 Schritten grün, darunter die native Zugangsbindung und Speicherlast. Stopp in `test_planen33313`: „Einplanen-Menü wurde nicht geöffnet“ nach `<Control-Shift-P>` auf der Liste. Einzeln mit Tk 9.0.3 grün, mit Tk 9.1 rot reproduziert.

**Ursache:** Auch macOS (`aqua`) legt `<<SelectPrevLine>>` auf Strg+Umschalt+P (`event info`); seit Tk 9.1 bindet die Treeview-Klasse daran (`::ttk::treeview::KeyNav %W up extend`). Reine Tk-Probe ohne Glide: Mit Tk 9.1 verschiebt Strg+Umschalt+P die Auswahl von zwei Zeilen auf eine, bevor Glides Kürzel läuft; mit Tk 9.0.3 bleibt sie. Glides Schutz aus 3.43.1 (`guard_x11_emacs_navigation`) galt nur unter X11; [Funktionen](../../../docs/20_FUNKTIONEN.md#kürzel-in-listen-unter-linux-3431) nannte macOS fälschlich unbetroffen. Nutzer mit dem gelieferten Tk 9.0 sind nicht betroffen, wohl aber die Tk-9.1-Laufzeit für P8/4.0.

**Korrektur:** Tk-freie Regel `interaction_policy.emacs_guard_applies(windowing_system)` für `x11` und `aqua` (D17), neuer Unit-Fall; `guard_x11_emacs_navigation` verwendet sie, Name und Aufrufer bleiben. Unter Tk 9.0 ändert sich nichts, weil die Treeview dort keine solche Klassenbindung hat; die Befehlstaste ist kein Emacs-Auslöser. App `1fabf883…`, `interaction_policy.py` `7181b254…`. Probe danach mit Tk 9.0 und 9.1: Auswahl bleibt bei Strg+Umschalt+P, Kürzel sieht beide Zeilen, Umschalt+↑ navigiert weiter. `test_planen33313` mit beiden Tk-Versionen grün.

**Zweiter Lauf `t1031-164116` (App `1fabf883…`): 126 von 126 Schritten grün, Exitcode 0**, 16:41–17:11. Enthalten sind 1.082 Fachtests (ein Skip), alle 108 Integrationssuiten, native Tcl-Zugangsbindungen (`native_backend: true`, Tk 9.1.0), `test_zugang400`, Speicherlast, `test_seitenkarten` in 17 s, Showcase, fünf Analysen sowie Beispiel-/Releasedaten. Quelle unverändert, Prüfkopie gleich (2.107 Dateien), kein Absturzbericht. Echte VoiceOver-Sprachausgabe und Menschenbedienung sind dadurch nicht abgenommen.

## Offen

- **Seitenkarten-Tempo:** eingegrenzt und im Prüfadapter umgangen, siehe Abschnitt oben. Offen bleibt nur der genaue Auslöser in der Startseite. Der Volllauf `m1031-141726` lief noch mit der vorherigen Suite.
- `test_release36` war im unbedienten Volllauf grün; die Fokusvermutung ist damit gestützt, nicht bewiesen.
- Python-Lieferung und Mac-Paket tragen den Fehler bis zur nächsten Lieferung; native Paketprüfung und Menschenabnahme bleiben offen.
