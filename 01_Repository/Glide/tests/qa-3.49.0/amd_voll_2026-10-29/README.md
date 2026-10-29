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
