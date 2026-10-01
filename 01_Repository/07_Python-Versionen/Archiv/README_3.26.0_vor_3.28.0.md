# Aktuelle startbare Python-Fassung

Neu in 3.26: Notizlisten mit Rich Text, Verlauf in der Seitenleiste, korrigierte Pinnwandvorschau, Lasso, Zoom und Navigator sowie responsive Punktmasken. [Umsetzung und bewusste Grenzen](../01_Repository/Glide/docs/decisions/Entscheidungen_3.26.0.md).

Glide 3.26.0 · Entwicklungsstand 21.09.2026 · Aufgabenformat 17 · Vorlagenformat 2

[Glide-Aufgaben-und-Listen_v3.26.0.pyw](Glide-Aufgaben-und-Listen_v3.26.0.pyw) ist die Arbeitskopie des kanonischen Codes. Der vollständige Nachbarordner `resources` gehört dazu. Mit einem Tk-fähigen Python 3 starten – am Mac `python3`, unter Windows `python` beziehungsweise per Doppelklick; eine laufende ältere Instanz vorher schließen. Der [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) nennt den jeweiligen Freigabestand.

Der Vorlagenkatalog unter `resources/templates` ist mit diesem Stand nachgezogen: Er stand seit 3.21.4 auf einer älteren Fassung, obwohl die startbare Datei mitging.

Seit 3.13: Die Tabellenansicht zeigt Aufgaben kompakt in wählbaren Spalten je Liste. „Mein Tag“, Schnellerfassung und gespeicherte Filter ergänzen die Reiter- und Pinnwandansichten. Alle Ansichten bearbeiten dieselben Objekte.

Aufgabenformat 14 ergänzte Bearbeitungstag und geschätzten Aufwand; 3.19 brachte Aufgabenformat 15 mit dem Änderungsverlauf; seit 3.22 gilt Aufgabenformat 16 mit der Checkliste je Aufgabe; die Tageskapazität ist eine persönliche Einstellung. Seit 3.24 trägt ein Komplettbackup zusätzlich die Anordnung der Pinnwände – neben den Aufgabenfeldern, ohne Formatsprung. Benachrichtigungen funktionieren innerhalb der laufenden App. Keine Systemzustellung bei beendetem Programm. Vorherige startbare Fassungen liegen im Unterordner `Archiv`; nur die aktuelle Fassung liegt aktiv im Ordner.

[Jüngste Bedienergänzung](../01_Repository/Glide/docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md) · [Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md) · [Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md)

