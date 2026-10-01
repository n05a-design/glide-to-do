# Produktgrenzen – Glide 3.18.0

Stand 13.09.2026 · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Glide ist eine deutschsprachige lokale Desktop-Anwendung für Aufgaben, Listen und Ordner. Kernfunktionen benötigen weder Internet noch Benutzerkonto oder Cloudservice. Laufzeit: Python, Tk und Standardbibliothek, mitgelieferte privat registrierte Schriften. Nutzerdaten liegen außerhalb des Programmordners.

Aufgaben, Gruppen, Long-Tasks, Überschriften, verschachtelte Ordner, Labels, Wichtigkeit, Fälligkeit, Wiederholungen, Benachrichtigungen, Papierkorb, Undo, Suche, Kalender, Startseite, Vorlagen und Backup/Import gehören zum Produkt. Die UI-Änderungen einschließlich einheitlicher Dropdowns und interner App-Aktionen beschreibt der [3.9-Vertrag](32_UI_UND_BEDIENUNG_3.9.0.md).

Benachrichtigungen werden bei laufender App verarbeitet. Verpasste Hinweise erscheinen gesammelt; Dock oder Taskleiste können hervorgehoben werden. Keine Systemzustellung bei beendetem Programm. Die Umbenennung ändert diese Betriebsgrenze nicht. [Systemintegration](decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Nutzerdaten dürfen in einem extern synchronisierten Ordner liegen. Glide synchronisiert selbst nicht. Die Belegungsdatei verhindert erkannte Fremdnutzung, kann aber nicht zwei noch unsynchronisierte Cloudkopien verriegeln. Nacheinander arbeiten: schließen, vollständig synchronisieren, am anderen Gerät öffnen. [Datenvertrag](06_DATA_BACKUP_MIGRATION.md).

Materialdarstellung verwendet getönte opake Tk-Flächen und Kanten, optional Windows-DWM. Keine echten transparenten oder unscharfen Flächen pro Widget. Symbole stammen aus `ICONS`. Schriftressourcen: DejaVu Sans 2.37 einschließlich Lizenz.

Außerhalb des Produkts bleiben Mehrbenutzerbetrieb, Konfliktzusammenführung, eigener Cloudservice, Telemetrie, Push bei geschlossener App, externe Kalender-/Mailintegration, Mehrsprachigkeit und ein Rich-Text-Editor. Betriebssystem-Schreibtools werden nicht nachgebildet. Installer, Signatur, Storeveröffentlichung und Markenfreigabe sind gesonderte, offene Schritte.

Historische Funktions- und Detailverträge bleiben im [Dokumentationsindex](00_INDEX.md) erhalten. Aktueller Prüfstand: [QA](07_QA_BERICHT.md).

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt „Mein Tag“ als bewusste Tagesauswahl über vorhandene Punktobjekte; 3.13 ergänzt die Tabellenansicht mit listenspezifischer Spaltenauswahl. `SavedFilters`, `today_plan` und `table_columns` werden additiv in den Einstellungen normalisiert. Aufgabenformat 13 blieb dabei unverändert; Filter, Tagesauswahl, Tabellenlayout, Reiter und Pinnwände sind keine Aufgabenbackups. Bearbeitungen laufen durch `item_change`, modale Auswahl durch `run_modal`. [Bedienung 3.13](36_TABELLENANSICHT_3.13.0.md) · [Bedienung 3.12](35_MEIN_TAG_3.12.0.md).

Bearbeitungstag und geschätzter Aufwand sind seit 3.14 freiwillige Aufgabenfelder in Datenformat 14. Sie erzeugen weder Fälligkeiten noch Tagesauswahlen. Gruppen und Überschriften tragen keine Planung. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md).

3.18 ergänzt den CSV-Import mit Spaltenzuordnung: Trennzeichen und Kodierung werden erkannt und sind umstellbar, jede Spalte wird einem Glide-Feld zugeordnet, eine Vorschau zeigt das Ergebnis vor der Übernahme. Kein XLSX, keine Anhänge, keine Wiederholungen oder Erinnerungen aus einer Spalte, kein Abgleich mit vorhandenen Punkten, kein gespeichertes Zuordnungsprofil; Grenzen sind 5000 Zeilen, 64 Spalten und 12 MB je Datei. [Bedienung 3.18](42_CSV_IMPORT_3.18.0.md).

3.17 ergänzt die Druck- und PDF-Ausgabe: vier Formate als eigenständige HTML-Druckansicht, geöffnet im Standardprogramm des Systems. Kein eigener PDF-Schreiber, kein Seriendruck, keine Druckerauswahl in Glide, kein DOCX-/XLSX-Export; ab 2000 Punkten wird abgeschnitten. [Bedienung 3.17](41_DRUCK_UND_PDF_3.17.0.md).

3.16 ergänzt ein vollständiges App-Backup: Aufgaben, Anhänge, Einstellungen, Vorlagenkatalog und Aktivitätsdaten in einem Archiv, wiederherstellbar mit Inhaltsvorschau und einzeln zuschaltbaren Bereichen. Kein Cloudspeicher, kein Zeitplan, kein Zusammenführen zweier Bestände, kein Passwortschutz. [Bedienung 3.16](40_APP_BACKUP_3.16.0.md).

3.15 fasst diese Angaben je Tag zusammen und vergleicht sie mit einer selbst gesetzten Tageskapazität. Die Anzeige nennt immer Grund und Bezugsgröße. Keine Zeiterfassung, keine gemessene Dauer, keine automatische Terminverteilung, keine Auslastungsquote über mehrere Tage und keine Bewertung der arbeitenden Person. Kein Wochentagsprofil und keine Kapazität je Liste. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).
