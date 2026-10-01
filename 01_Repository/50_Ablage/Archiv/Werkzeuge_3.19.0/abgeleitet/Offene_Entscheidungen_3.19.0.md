# Offene Entscheidungen Glide 3.19.0

Stand: 13.09.2026. Umgesetzt und automatisiert geprüft sind Tabellenansicht,
Bearbeitungstag und Aufwand, Tagesplanung mit Tageskapazität, das vollständige
App-Backup mit Inhaltsvorschau, die Druck- und PDF-Ausgabe, der CSV-Import mit
Spaltenzuordnung sowie der dauerhafte Änderungsverlauf. Offen für eine Veröffentlichung
bleiben Anbieter- und Markenangaben, Support-/Datenschutzadressen, Preis und
Lizenzmodell, Installer und Signierung, Mindestbetriebssystem, Storeweg sowie eine echte
macOS-, DPI-, Accessibility- und Langzeitabnahme.

Beim Änderungsverlauf bewusst nicht entschieden: das Wiederherstellen einzelner alter
Werte aus dem Protokoll (das wäre eine Versionsverwaltung und ein eigenes Ausbauthema),
das Mitschreiben alter Feldinhalte, eine Verlaufsansicht am einzelnen Punkt, ein
Benutzer- oder Gerätebezug, die Aufnahme von Einstellungs-, Vorlagen- und
Ansichtsänderungen sowie ein Export nach CSV oder JSON. Ebenfalls offen: ob der Verlauf
eine eigene Datei neben dem Bestand bekommen sollte, falls die Speicherdatei durch lange
Nutzung merklich wächst – heute begrenzt die Obergrenze von 4000 Einträgen das Wachstum.

Beim CSV-Import bleiben ein gespeichertes Zuordnungsprofil, XLSX-Lesen ohne
Fremdbibliothek, ein Abgleich mit vorhandenen Punkten, Ordnerstruktur aus einer Spalte
sowie das Übernehmen von Wiederholungen, Erinnerungen und Anhängen offen. Bei der
Druckausgabe bleiben eigenes Layout mit Logo, Seriendruck, Druckerauswahl in Glide,
DOCX-/XLSX-Export und ein eigener PDF-Schreiber offen. Beim App-Backup bleiben Cloud- oder
Netzwerkziel, zeitgesteuerte Sicherung, Zusammenführen zweier Bestände, Teilrestore
einzelner Listen, Versionsgeschichte im Archiv sowie Passwortschutz offen.

Die nächsten offenen Ausbaustufen sind benutzerdefinierte Felder und – darauf aufbauend –
eigene Ansichten je Feld. Keine davon ist zugesagt. Ein echter Desktop-Blur wäre weiterhin
ein eigener WinUI-/WebView- oder AppKit-Kompositionszweig. Die Sperrdatei warnt, löst aber
keine konkurrierenden Offline-Änderungen zusammen.

Details und Nachweise stehen im [Dokumentationsindex](../../01_Repository/Glide/docs/00_INDEX.md), im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md) und in der [Funktionsübersicht](../Glide_Funktionsvorschlaege_2026-09-11.md).
