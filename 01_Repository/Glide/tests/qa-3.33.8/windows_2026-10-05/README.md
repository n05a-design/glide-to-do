# Windows-Layout und Editorlebensdauer – Prüfnachweis

Glide 3.33.8 · 05.10.2026 · Datenformat 20 · Windows x64

**Vollständige Nachprüfung bestanden: Exitcode 0, 84 automatische Schritte, 66 Integrationssuiten und 75 Unit-Tests.** Eine Sichtprüfung bleibt ausdrücklich offen. [Grünes Originalergebnis](voll_2/ergebnis.json). Separate Python-3.14.8-/Tk-9.0.4-Laufzeit. [Herkunft und Herstellerhash](prueflaufzeit.json), [eingefrorene Code-/Prüfdateien](quellstand.json). PATH und Standardinstallation bleiben unverändert. Der Prüflauf verwendet ausschließlich temporäre `GLIDE_DATA_DIR`-Ordner.

## Korrekturen

- Titelkürzung folgt der zugeteilten Titelzeilenbreite, auch nach geänderter Kennzahl.
- Vier Bereichsüberschriften verwenden bei minimaler Höhe kompakte Abstände; bei Vergrößerung kehren die bisherigen Abstände zurück.
- Ein geschlossener Zeicheneditor beendet Kontext-, Größen-, Vorschau- und Speichertimer. Der vorhandene Seitenwechsel speichert vorher offene Pixel.
- Windows-Formatcache prüft den vollständigen SHA-256-Inhalt: gleich große schnelle Überschreibungen können identische Metadaten und native ChangeTime liefern. Ein Headervergleich wäre unzureichend. JSON wird bei unverändertem Inhalt weiter nur einmal geparst. Drei zusätzliche Unit-Tests bilden diese Fälle auch außerhalb Windows nach. [Kollisionsprobe](dateimetadaten_probe.json), [warme Dateiprüfung](messung_dateipruefung.json).
- Windows-Testannahmen: tatsächlich gelieferte Schriften statt fixer Dateianzahl, Einstellungen im Überlauf, Tk-9-Alias der Control-Bindung, benannte Treeview-Titelzelle statt der veränderten `identify_element`-Geometrie, interne Menüleiste, native JSON-Zeilenenden und stabiler Window-Manager-/Kontextlayoutzustand. Die strengen Mindestgrößen-/Canvasvergleiche bleiben erhalten. Der Sechs-Chip-Vergleich mit vollständigem Hinweistext hat jetzt genügend Fensterbreite.

Die Hauptsuite besteht gezielt vollständig. Mindestgrößen: 75 Ansichten in fünf Designs und 43 Dialogaufrufe ohne Befund oder Callback-Fehler. Acht schnelle Editorwechsel beenden alle alten Timer und erhalten die Pixel bis zur Datei. Speicherlast besteht gezielt mit 40 Speicherrunden, sechs Prozessabbrüchen und parallelen Lesern. Der erste [Gesamtbericht](voll/ergebnis.json) enthält 66 grüne Integrationssuiten und genau einen fehlgeschlagenen Unit-Test zur In-place-Änderung. Die neue deterministische Gegenprobe scheiterte an der vorherigen Sicherungslogik; nach Korrektur sind alle 75 Unit-Tests grün. Die vollständige Nachprüfung ist grün; maßgeblich ist das oben verlinkte `voll_2/ergebnis.json`. Alle 75 Unit-Tests bestehen zusätzlich unter Python 3.12.10. Der Windows-Starter weist diese Tk-8.6-Laufzeit mit Exitcode 3 vor der Vollprüfung zurück. 24 Werkzeugtests und die CI-Grundstufe mit strengem Liefervergleich grün. [CI-Ergebnis](ci/ergebnis.json): einschließlich Startprobe, Fremdcodeherkunft, Datenschutz und Ablagegröße. [Editor-Gegenprobe](gegenprobe_editor.json) gegen die Hauptdatei 3.33.6: erwarteter Fehler wegen verbliebener Timer.

## Grenzen

Keine menschliche Freigabe. Referenz-Mac-Abnahme und nativer macOS-Bundlebau sind auf diesem Windows-Gerät nicht ausführbar; Linux, DPI/Mehrmonitor, Screenreader, Signierung und öffentliche Verteilung bleiben offen. Python-Lieferung und Showcase nach grünem Windows-Ergebnis abgeglichen: 16 Code-Dateien, 131 Ressourcen und sechs Showcase-Dateien. [SHA-256-Nachweis](lieferabgleich.json). Inhaltssuche und Editorwechsel zusätzlich direkt gegen die ausgelieferte Hauptdatei grün. [Windows-Startanleitung](../../../../../07_Python-Versionen/README.md). Folgeschnitte stehen im Entwicklungsplan; Inhaltssuche seit 3.33.7 bleibt enthalten, Format 20 unverändert.

Ablage nach der bestehenden Sieben-Versionen-/Drei-Bildstände-Regel gekürzt; 95 weitere überholte Dateien entfernt, historische Nachweislinks auf den unveränderlichen Git-Stand umgestellt. [Nachweis](ablagekuerzung.json).
