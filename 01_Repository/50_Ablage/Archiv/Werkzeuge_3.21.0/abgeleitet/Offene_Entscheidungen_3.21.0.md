# Offene Entscheidungen Glide 3.21.0

Stand: 14.09.2026. Umgesetzt und automatisiert geprüft sind Tabellenansicht,
Bearbeitungstag und Aufwand, Tagesplanung mit Tageskapazität, das vollständige App-Backup
mit Inhaltsvorschau, die Druck- und PDF-Ausgabe, der CSV-Import mit Spaltenzuordnung, der
dauerhafte Änderungsverlauf sowie Kalenderausgabe und Kalenderimport als ICS. Offen für
eine Veröffentlichung bleiben Anbieter- und Markenangaben, Support-/Datenschutzadressen,
Preis und Lizenzmodell, Installer und Signierung, Mindestbetriebssystem, Storeweg sowie
eine echte macOS-, DPI-, Accessibility- und Langzeitabnahme.

Beim Kalenderimport bewusst nicht entschieden: ein **Abgleich**, der vorhandene Punkte
anhand fremder UIDs aktualisiert statt neue anzulegen – das wäre der erste Schritt zu einer
Synchronisierung und braucht eine Antwort auf die Frage, wer im Konflikt gewinnt. Ebenfalls
offen: CalDAV oder ein Abonnement mit automatischer Neuausgabe, Teilnehmer und
Einladungsantworten, Ausnahmetermine einer Serie, `VTODO`-Einträge als Aufgaben ohne
Fälligkeit, das Übernehmen von Anhängen aus Terminen sowie eine Zuordnungsmaske, mit der
man ICS-Felder wie beim CSV-Import frei auf Glide-Felder legt.

Bei der Kalenderausgabe bleiben `VTODO`, Teilnehmer, Orte, Ausnahmetermine und
`VTIMEZONE`-Definitionen offen. Beim Änderungsverlauf bleiben das Wiederherstellen
einzelner alter Werte, alte Feldinhalte, eine Verlaufsansicht am einzelnen Punkt sowie ein
Export offen. Beim CSV-Import bleiben Zuordnungsprofil, XLSX und der Abgleich mit
vorhandenen Punkten offen. Beim App-Backup bleiben Cloud- oder Netzwerkziel,
zeitgesteuerte Sicherung, Zusammenführen zweier Bestände, Teilrestore und Passwortschutz
offen.

Die nächsten offenen Ausbaustufen sind benutzerdefinierte Felder und darauf aufbauende
eigene Ansichten je Feld. Keine davon ist zugesagt. Ein echter Desktop-Blur wäre weiterhin
ein eigener WinUI-/WebView- oder AppKit-Kompositionszweig. Die Sperrdatei warnt, löst aber
keine konkurrierenden Offline-Änderungen zusammen.

Details und Nachweise stehen im [Dokumentationsindex](../../01_Repository/Glide/docs/00_INDEX.md), im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md) und in der [Funktionsübersicht](../Glide_Funktionsvorschlaege_2026-09-11.md).
