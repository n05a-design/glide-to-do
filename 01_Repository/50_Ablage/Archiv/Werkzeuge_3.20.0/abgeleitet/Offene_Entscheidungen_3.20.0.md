# Offene Entscheidungen Glide 3.20.0

Stand: 14.09.2026. Umgesetzt und automatisiert geprüft sind Tabellenansicht,
Bearbeitungstag und Aufwand, Tagesplanung mit Tageskapazität, das vollständige App-Backup
mit Inhaltsvorschau, die Druck- und PDF-Ausgabe, der CSV-Import mit Spaltenzuordnung, der
dauerhafte Änderungsverlauf sowie die Kalenderausgabe als ICS. Offen für eine
Veröffentlichung bleiben Anbieter- und Markenangaben, Support-/Datenschutzadressen, Preis
und Lizenzmodell, Installer und Signierung, Mindestbetriebssystem, Storeweg sowie eine
echte macOS-, DPI-, Accessibility- und Langzeitabnahme.

Bei der Kalenderausgabe bewusst nicht entschieden: ein **Kalenderimport** (ICS lesen) und
damit die Frage, ob Glide fremde Termine als Aufgaben übernimmt; eine echte
Synchronisierung über CalDAV, die Konto, Netzwerkschicht und Hintergrundprozess bräuchte;
eine `VTODO`-Ausgabe für Apple Erinnerungen; Teilnehmer, Orte und Einladungen;
Ausnahmetermine einer Serie; eine automatische Neuausgabe bei jeder Änderung, damit ein
Abonnement aktuell bleibt; und `VTIMEZONE`-Definitionen anstelle der schwebenden Ortszeit.
Jeder dieser Punkte verschiebt die Ausgabe zu einer Anbindung und braucht eine eigene
dokumentierte Entscheidung.

Beim Änderungsverlauf bleiben das Wiederherstellen einzelner alter Werte, alte
Feldinhalte, eine Verlaufsansicht am einzelnen Punkt, Benutzer- oder Gerätebezug sowie ein
Export nach CSV oder JSON offen. Beim CSV-Import bleiben Zuordnungsprofil, XLSX, Abgleich
mit vorhandenen Punkten und Ordnerstruktur aus einer Spalte offen. Bei der Druckausgabe
bleiben eigenes Layout mit Logo, Seriendruck, Druckerauswahl und ein eigener PDF-Schreiber
offen. Beim App-Backup bleiben Cloud- oder Netzwerkziel, zeitgesteuerte Sicherung,
Zusammenführen zweier Bestände, Teilrestore und Passwortschutz offen.

Die nächsten offenen Ausbaustufen sind benutzerdefinierte Felder, darauf aufbauende eigene
Ansichten je Feld und der Kalenderimport. Keine davon ist zugesagt. Ein echter
Desktop-Blur wäre weiterhin ein eigener WinUI-/WebView- oder AppKit-Kompositionszweig. Die
Sperrdatei warnt, löst aber keine konkurrierenden Offline-Änderungen zusammen.

Details und Nachweise stehen im [Dokumentationsindex](../../01_Repository/Glide/docs/00_INDEX.md), im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md) und in der [Funktionsübersicht](../Glide_Funktionsvorschlaege_2026-09-11.md).
