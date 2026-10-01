# Produktgrenzen – Glide 3.13.0

Stand 13.09.2026 · Aufgabenformat 13 · Einstellungen 2 · Vorlagen 2

Glide ist eine deutschsprachige lokale Desktop-Anwendung für Aufgaben, Listen und Ordner. Kernfunktionen benötigen weder Internet noch Benutzerkonto oder Cloudservice. Laufzeit: Python, Tk und Standardbibliothek, mitgelieferte privat registrierte Schriften. Nutzerdaten liegen außerhalb des Programmordners.

Aufgaben, Gruppen, Long-Tasks, Überschriften, verschachtelte Ordner, Labels, Wichtigkeit, Fälligkeit, Wiederholungen, Benachrichtigungen, Papierkorb, Undo, Suche, Kalender, Startseite, Vorlagen und Backup/Import gehören zum Produkt. Die UI-Änderungen einschließlich einheitlicher Dropdowns und interner App-Aktionen beschreibt der [3.9-Vertrag](32_UI_UND_BEDIENUNG_3.9.0.md).

Benachrichtigungen werden bei laufender App verarbeitet. Verpasste Hinweise erscheinen gesammelt; Dock oder Taskleiste können hervorgehoben werden. Keine Systemzustellung bei beendetem Programm. Die Umbenennung ändert diese Betriebsgrenze nicht. [Systemintegration](decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Nutzerdaten dürfen in einem extern synchronisierten Ordner liegen. Glide synchronisiert selbst nicht. Die Belegungsdatei verhindert erkannte Fremdnutzung, kann aber nicht zwei noch unsynchronisierte Cloudkopien verriegeln. Nacheinander arbeiten: schließen, vollständig synchronisieren, am anderen Gerät öffnen. [Datenvertrag](06_DATA_BACKUP_MIGRATION.md).

Materialdarstellung verwendet getönte opake Tk-Flächen und Kanten, optional Windows-DWM. Keine echten transparenten oder unscharfen Flächen pro Widget. Symbole stammen aus `ICONS`. Schriftressourcen: DejaVu Sans 2.37 einschließlich Lizenz.

Außerhalb des Produkts bleiben Mehrbenutzerbetrieb, Konfliktzusammenführung, eigener Cloudservice, Telemetrie, Push bei geschlossener App, externe Kalender-/Mailintegration, Mehrsprachigkeit und ein Rich-Text-Editor. Betriebssystem-Schreibtools werden nicht nachgebildet. Installer, Signatur, Storeveröffentlichung und Markenfreigabe sind gesonderte, offene Schritte.

Historische Funktions- und Detailverträge bleiben im [Dokumentationsindex](00_INDEX.md) erhalten. Aktueller Prüfstand: [QA](07_QA_BERICHT.md).

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt „Mein Tag“ als bewusste Tagesauswahl über vorhandene Punktobjekte; 3.13 ergänzt die Tabellenansicht mit listenspezifischer Spaltenauswahl. `SavedFilters`, `today_plan` und `table_columns` werden additiv in den Einstellungen normalisiert. Aufgabenformat 13 bleibt unverändert; Filter, Tagesauswahl, Tabellenlayout, Reiter und Pinnwände sind keine Aufgabenbackups. Bearbeitungen laufen durch `item_change`, modale Auswahl durch `run_modal`. [Bedienung 3.13](36_TABELLENANSICHT_3.13.0.md) · [Bedienung 3.12](35_MEIN_TAG_3.12.0.md).
