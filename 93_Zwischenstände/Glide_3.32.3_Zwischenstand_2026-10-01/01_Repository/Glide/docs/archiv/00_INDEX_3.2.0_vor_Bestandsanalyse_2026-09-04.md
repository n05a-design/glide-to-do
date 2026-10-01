# Dokumentationsindex

- `01_PRODUCT_CONSTRAINTS.md` – verbindliche Produktgrenzen und Nicht-Ziele
- `02_ARCHITECTURE.md` – aktueller technischer Aufbau und bewusste Übergangsstruktur
- `05_QA_TESTPLAN.md` – automatisierte und manuelle Prüfungen
- `07_QA_BERICHT.md` – was geprüft wurde, mit welchem Ergebnis, und was ungeprüft bleibt
- `06_DATA_BACKUP_MIGRATION.md` – Datenformat, Speicherorte, Backup und Restore
- `08_CODE_BEFUND.md` – Befund der Codeüberprüfung 3.0.2 und was in 3.1.0 daraus wurde
- `09_PROJECT_HANDOFF.md` – konsolidierter Projektstand zur Übergabe an einen neuen Agenten
- `09_STARTKONTEXT.md` – komprimierter Einstieg, zum Kopieren in einen neuen Chat
- `09_ARBEITSAUFTRAG_BESTANDSANALYSE.md` – ausformulierter Auftrag: Bestandsanalyse, Archivierung, Fehlerprüfung, Prozesse, drei Glide-Deliverables
- `10_RELEASE_CHECKLIST.md` – Go/No-Go vor Build und Veröffentlichung
- `archiv/` – überholte Fassungen dieser Dokumente, benannt nach der Version, die sie beschrieben
- `decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md` – wann Gruppe, wann Ordner, wann Zwischenüberschrift
- `decisions/PRODUCT_IDENTITY.md` – technisch belegte Werte und noch offene Produkt-/Plattformidentitäten
- `exec-plans/3.0.0-oberflaeche-und-symbole.md` – Dunkelblau statt Schwarz, Listenübersicht ganz oben, Umbenennen in der Ansicht, Symboltabelle, Bildlaufleiste und Menürahmen
- `exec-plans/2.12.0-oberflaeche-verdichten.md` – Labelauswahl als Aufklappfeld, Fälligkeit mit Kalenderknopf, Kopfbereich ohne Sprung, Listenübersicht weiter oben, lesbares Fälligkeitsdatum
- `exec-plans/2.11.0-datenintegritaet-und-eingabemaske.md` – Ursache des Datenverlusts, Bestandswächter, Papierkorb für Punkte, Strg+Klick, gemeinsame Eingabemaske, Kalender und Uhrzeit, Datenformat 10
- `exec-plans/2.10.0-label-chips-und-codepflege.md` – Labels als Chips, verlustfreier TXT-Rundlauf, Codepflege, QA-Bericht, Veröffentlichungs-Checkliste
- `exec-plans/2.9.0-verschachtelte-ordner.md` – Ordner in Ordner, Punktdetails (Long-Task), Bildlaufleisten, app-weiter Durchlauf, Datenformat 9
- `exec-plans/2.8.0-arten-verspaetet-und-hover.md` – Long-Task, Zwischenüberschrift, „Verspätet“, erweiterter Anlage-Dialog, Hover, responsive Spalten, Datenformat 8
- `exec-plans/2.7.2-fokus-und-kalenderinteraktion.md` – Tastaturfokus im Aufgabenbaum, graues Trennband, Hover und Doppelklick im Kalender
- `exec-plans/2.7.1-ui-feinschliff.md` – Systemfläche statt Trennlinie, Labelpalette, Labels an Ordnern und Listen, Kalendermodi, Verschiebe-Tastenkürzel
- `exec-plans/2.7.0-papierkorb-labels-kalender.md` – Systemblock, Papierkorb, gemeinsamer Bearbeiten-Dialog, Mehrfachauswahl, Labels, Kalender, Autosave, Datenformat 7
- `exec-plans/2.6.0-gruppen-und-kontextmenues.md` – Gruppen als Punktart, Kontextmenüs, Titeltypografie, Datenformat 6
- `exec-plans/2.5.5-fehlerbehebung-und-macos.md` – Anhangs- und Importfehler, Dialogabstände, macOS-Tastenkürzel
- `exec-plans/2.5.4-uebersichten-und-ui-stabilisierung.md` – Systemansicht, Ordnerübersicht, Beschreibungstexte, Layout- und Anhangshärtung
- `exec-plans/2.5.3-ui-und-struktur-stabilisierung.md` – Kontextmenü-Fix, feste Fälligkeitsspalte, Eingang-Stil und Ablagekonsolidierung
- `exec-plans/2.5.2-qol-stabilisierung.md` – separate Eingangsdarstellung, Aufgaben-Kontextmenü und Dark-Start
- `exec-plans/2.5.1-stabilisierung.md` – nachvollzogener Arbeitsstand der damaligen Überarbeitung

Die Word-Datei unter dem äußeren Ordner `10_Dokumentation/` ist die ausführliche Management- und Release-Arbeitsgrundlage. Die Markdown-Dateien hier sind die knappen, code-nahen Quellen.

## Produktdaten für Stores und Texte

Faktische Produktangaben, die sich direkt aus dem Code ergeben – Systemvoraussetzungen, Datenspeicherorte, Datenschutzaussagen, Funktionsumfang – liegen gebündelt unter dem äußeren Ordner `40_Store_Material/`. Das dort abgelegte `Produktdatenblatt_2.6.0.md` ist der letzte gepflegte Stand und damit **vier Minor-Versionen alt**; es muss vor einer Store-Einreichung auf 3.2.0 nachgeführt werden. Store-spezifische Formulare liegen darunter je Plattform.
