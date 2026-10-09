# Gemeinsame Sprintplanung: erste Auswahl und Referenzen (10.10.2026)

Stand 10.10.2026 · Glide 3.35.0 · Nachlauf ohne neue App-Version · Referenz-Mac, Python 3.14.5, Tk 9.0.3

Die Auswahlantwort des Inhabers ist wörtlich als D18–D29 in der [Arbeitsrichtung](../../../docs/ARBEITSRICHTUNG.md) festgehalten: Animation A/V, gemeinsame Referenzentwürfe B/V und Tageshinweise A/V. Übrige Funktionen werden weiterhin gemeinsam ausgewählt. [Entwicklungsplan §15](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#15-neuer-feature-sprint-ab-09102026-gemeinsame-planung) enthält den ausgewählten Umfang, Abhängigkeiten, Akzeptanzkriterien, Prüfungen und den weiteren Gesprächsstand. Bild 1 und OB02/OB03/N05/KO04 vollständig gewählt; außerdem Notion A/V, PyInstaller für Mac/Windows A/V, Logo B+C+D+F und gesamte ICONS-Tabelle mit Systemzeichen. Weitere Auswahlrunden laufen. Die Umsetzung beginnt nach Bestätigung des vollständigen Paketplans.

Vier neue Aufnahmen des eigenen Glide-Fensters mit künstlichen Aufgaben und isoliertem temporärem `GLIDE_DATA_DIR` bilden die Grundlage für drei unabhängig erzeugte Bildtafeln (je Heute, Liste, Seite und Inspektor). Quellaufnahmen und verworfene Varianten liegen lokal außerhalb von OneDrive; Bild 1 ist nach D21 im Grafik-Master gesichert. Sichtbare Reihenfolge, Dateinamen, SHA-256 und bekannte Bildabweichungen sind im [Ergebnis](ergebnis.json) festgehalten; Bindung an die tatsächlichen Tk-Mittel und Produktregeln in §15.4. Bilder sind Entwürfe, kein Nachweis einer implementierten oder nativ abgenommenen Oberfläche.

## Prüfung

[Erneute strenge CI mit D18–D29 und ausgewählter Referenz](ci/ergebnis.json): Exitcode 0. Alle Pflichtschritte bestanden; Fremdcodeabruf wie im Vorlauf mit SSL-Hinweis. Quellen-/Nachweisergänzungen danach mit Stand-, Verweis- und Datenschutzprüfung nachgeführt.

- [Vorlauf in der Arbeitskopie](ci_vorlauf/ergebnis.json): Exitcode 1, einziger Befund der Standprüfung war die externe unversionierte Datei `Apple Design Skill.md` ohne Glide-Standangabe. Alle anderen Schritte bestanden; die Datei bleibt unverändert und unversioniert.
- [Erste strenge CI auf isolierter Projektkopie, Stand D18–D20](ci_runde_1/ergebnis.json): Exitcode 0. Git-Stand `f9c07c1` mit allen eigenen Dokumentänderungen und neuen Nachweisen außerhalb von OneDrive geprüft; die externe Datei gehört nicht zu diesem Prüfstand. Syntax, Versionen, Dokumentation, Fixtures, Werkzeug-/Fachlogiktests, fünf Analysen, isolierte Tk-Startprobe, Lieferstand, Datenschutz, Ablagegröße und Synchronisation bestanden. Der Fremdcodeabruf von PyPI blieb wegen `CERTIFICATE_VERIFY_FAILED` ein Hinweis; keine neue Abhängigkeit.
- [Lieferabgleich](ergebnis.json): App, 07 und Showcase ohne Git-Differenz zu `b5f5c22`; 168 Code-/Ressourcendateien SHA-256-gleich zu 07, 82 für macOS vorgesehene Dateien SHA-256-gleich zum bestehenden Bundle. Keine ausführbare Änderung.
- Keine neue Vollprüfung oder Signaturprüfung: kein Bundlebau. Die eingefrorenen Vollprüfungen bleiben Belege ihres jeweiligen Stands. Windows-/Linux- und menschliche Abnahme bleiben offen. Neue Verweise und Datenschutz nach dem Nachführen dieses Nachweises erneut geprüft.

Rohprotokolle bleiben außerhalb von OneDrive; Ergebnisdateien enthalten keine Benutzerpfade. Der gesamte Arbeitsordner bleibt wegen der externen Datei in der Standprüfung rot; die grüne CI gilt ausdrücklich für den dokumentierten Projektprüfstand.
