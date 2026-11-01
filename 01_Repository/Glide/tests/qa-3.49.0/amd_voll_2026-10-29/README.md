# Neuer vollständiger AMD-Prüflauf auf PC-01

Stand 29.10.2026 · Quelle 3.49.0 · Aufgabenformat 26 · PC-01 AMD Ryzen 7 5800X3D · Python 3.14.7 / Tcl/Tk 9.0.4.

Auftrag: vollständige Windows-Prüfung als späterer Vergleich mit PC-02/Intel. Anschließende Fortsetzung „weiter“ autorisiert die begrenzte Korrektur des bestätigten Neustart-Testablaufs und einen neuen eingefrorenen Vollversuch. Kein Produktions-, Format-, Versions-, Liefer- oder Gittransport aus dieser Prüfkorrektur.

## Erhaltene rote Ausgangsläufe

- `%USERPROFILE%\GlidePruefung\pc1-amd-voll-2026-10-29_090909`: 09:09–09:11, 1.064 Fachtests mit 14 Fehlern an der 130-Zeichen-Exportzielgrenze. Gewählter Prüf-/Temppfad zu lang; Folge korrekt gestoppt. Keine Produktions-/Testkriterienänderung als Pfadkorrektur.
- `%USERPROFILE%\gq\a1029-092252`: 09:22–09:26, alle 1.064 Fachtests grün. 13 erfolgreiche Schritte, ein Fehler in `test_ui_updates`, 108 übersprungene Berichtseinträge einschließlich manueller Restprüfung. Direkte Rootzerstörung vor neuer ListApp umgeht Sitzungsabschluss. Kein unerwarteter Interpreterabbruch, kein Integritätsstopp.
- Lesende Originaldiagnose unter `%USERPROFILE%\gq\diag-ui-1029`: Anzeige 3 → 0 bei erkanntem aktivem Vorgänger; gespeicherter Bestand und Datei-SHA-256 identisch. Null-Zähler in dieser Probe durch geschützten Start erklärt, keine allgemeine Datenintegritätsfreigabe.

## Begrenzte Prüfkorrektur

`tests/integration/test_ui_updates.py` verwendet beim normalen Neustart den echten `on_close`-Weg und prüft den sauberen Sitzungsmarker sowie schreibfähigen Neustart zusätzlich zu den unveränderten vorhandenen Fachassertions. Widgeteigene Tcl-Zeitaufträge werden vor dem Interpreterwechsel nur aus dem Scheduler entfernt; ihre Befehle bleiben bis zur Freigabe durch das Eigentümerwidget erhalten. Abschließender Testabbau beendet Sitzung und Datensperre.

Erster Korrekturvorlauf rot: Python-`root.after_cancel` löschte auch fremde Tcl-Befehle und verursachte doppelte Freigabe beim Widgetabbau. Korrigiert auf Tcl-`after cancel`; unveränderte Assertions. Zweiter gezielter UI-Lauf grün, ohne Tcl-Restmeldung. Nachweis `%USERPROFILE%\gq\fix-ui-1029\test_ui_updates_v2.log`; roter Vorlauf daneben erhalten. Originalsuite-Wiederanlaufprüfung und neuer Vollversuch folgen separat.

## Vergleich und Ablage

Der Appstand von PC-02 ist inzwischen eingetroffen: App-SHA-256 `9e7e4e2c8fc94817959be05dec46a8883ee867fae9d73e290a677e7c28f54364`. Die zwei roten neuen AMD-Läufe prüften den vorherigen Stand `8025a20c…`. Ein neuer Vollversuch muss deshalb mit neuer eingefrorener Quelle, Suite-/Fixturehashes und Hardwareprofil dokumentiert werden; kein Einzelfaktor-CPU-Vergleich allein anhand unterschiedlicher Entwicklungsstände.

Die vom Benutzer eingerichtete Vergleichsablage `13_TK-Test-Umgebung/PC-01-AMD` bleibt lokal und Git-ausgeschlossen. Dort stehen `VERGLEICH_2026-10-29.md` sowie die einzelnen Lauf-/Diagnosebelege. Laufende künstliche Daten, Temp und Prüfkopien bleiben außerhalb OneDrive unter `%USERPROFILE%\gq`. Protokollkopien sind keine neuen Laufbelege anderer Hardware. WA-41A/B, native/Menschenabnahme und Lieferung bleiben gesondert.

## Dritter Vollversuch, 29.10.2026 abends (App `39499ab3…`)

19:47–21:09 Uhr, eingefroren mit den Korrekturen aus dem [Gerätevergleich](../geraetevergleich_2026-10-29/README.md). Unveränderter Starter `windows_vollpruefung.ps1`, Vollmodus, 900 s je Suite, Python 3.14.7 / Tk 9.0.4, Standardablage `%USERPROFILE%\GlidePruefung` (28 Zeichen; der 09:09-Pfadfehler trat nicht auf). Systemkontext: Ryzen 7 5800X3D, 16 logische Prozessoren, MSI B550M PRO-VDH WIFI, BIOS 2.L0.

**Ergebnis: 115 von 115 ausgeführten Schritten grün, danach Stopp im Schritt „Showcase“ (Exitcode 1).** Grün sind Syntax, Versionen, Dokumentation, Fixtures, 1.075 Fachtests, Tk-/Zeitzonenprüfung und alle 108 registrierten Integrationssuiten. Darunter sind die 18 im Gerätevergleich korrigierten Suiten, `test_ui_updates`, `test_wiederanlauf` und `test_speicherlast330` (26.420 Punkte, 40 Änderungsrunden verlustfrei, sechs harte Abbrüche ohne halbe Datei). Kein Interpreterabbruch, keine Integritätsbefunde, Quelle und Prüfkopie unverändert. Nicht ausgeführt: fünf Analysen, Beispieldaten-/Release-Reproduktion und Windows-Aufnahme. Der Gegenlauf der korrigierten Suiten auf PC-01 ist damit erbracht, ein vollständig grüner Volllauf noch nicht.

**Showcase-Befund:** `tests/tools/pruefe_showcase.py` beendete die erste App per `root.destroy()` ohne regulären Sitzungsabschluss und startete sofort den Neustart-Kindprozess. Der Elternprozess lebt währenddessen weiter. Deshalb bewertet der Kindprozess dessen Sitzungsnachweis korrekt als aktiv und startet schreibgeschützt (`recovery`) mit leerem Grundbestand; `integrity(app, 11)` scheitert. Das ist dasselbe Prüfadaptermuster wie bei den 15 im Gerätevergleich korrigierten Suiten (Regel im [Prüfplan](../../../docs/05_QA_TESTPLAN.md#regeln)), kein Appfehler und kein Datenverlust. Die Suiten liefen bisher nie bis zu diesem Schritt.

**Korrektur:** Vor `root.destroy()` ruft die Prüfung `getattr(app, "finish_recovery_session", lambda: None)()` und `app.release_data_lock()` auf; Fachassertions unverändert. SHA-256 vorher `b5ed47ed…`, nachher `faea67f3…`. `beispieldaten.py` und `releasedaten.py` öffnen je Prozess nur eine Instanz und sind nach Codelesung nicht betroffen.

**Gegenprobe Linux/Tk 9.0.3, künstliche Daten:** 132 Eingangsdateien bytegleich zum Quellmanifest der Prüfkopie, optionales tkdnd ausgenommen. Originalfassung zweimal rot an derselben Stelle; Diagnose im Kindprozess `kind=active`, `reason=recovery`, `lists=2`. Korrigierte Fassung dreimal grün einschließlich „Neustart: ok“. Das ersetzt keinen Windows-Nachweis.

**Offen:** neuer eingefrorener Volllauf auf PC-01 mit dieser Korrektur bis zum Ende (Showcase, Analysen, Reproduktionen, Windows-Aufnahme), danach M2-Gegenlauf. Rohlogs bleiben lokal; flache Belege unter `13_TK-Test-Umgebung/PC-01-AMD/v1029-1947`.
