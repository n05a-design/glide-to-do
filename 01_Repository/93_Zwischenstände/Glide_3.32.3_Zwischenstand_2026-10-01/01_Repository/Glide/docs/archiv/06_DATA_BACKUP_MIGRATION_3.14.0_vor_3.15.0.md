# Daten, Backups und Migration – Glide 3.14.0

Stand 13.09.2026 · optionale Aufgabenplanung in 3.14

Aufgabenformat **14**, Einstellungen **2**, Vorlagenformat **2**. Die UI nennt Erinnerungen jetzt Benachrichtigungen; gespeicherte Felder und APIs wie `reminder`, `reminder_attention`, Zustellbelege und Aufschub bleiben unverändert. Neuer additiver boolescher Einstellungswert: `sidebar_visible`, Standard `true`. Design bleibt im bisherigen Feld `theme`.

Vor dem ersten Speichern von Aufgaben vor Format 14 entsteht die unrotierte unveränderte Originalkopie `backups/liste_vor_format14_<Zeitstempel>.json`. Bei Fehler wird nicht gespeichert. Formate 4–14 und Legacy 2 bleiben lesbar. Glide 3.13 und ältere Versionen können Format 14 nicht lesen. Für einen Rückwechsel die alte Sicherung in einer separaten Ablage verwenden; sie enthält keine späteren Änderungen.

| Ablage | Inhalt | Transport |
|---|---|---|
| `liste_speicher.json` | Ordner, Listen, Aufgaben, Labels, Wiederholungen, Benachrichtigungen, Papierkorb | Aufgabenbackup |
| `settings.json` | Theme, Profil, Anzeige, Historien, `reminder_attention`, `sidebar_visible` | Datenordnerkopie |
| `vorlagen.json` | System-/eigene Vorlagen | `.glidetemplates` oder Datenordnerkopie |
| `attachments/`, `backups/` | Lokale Anhänge und Sicherungen | referenzierte Anhänge in Aufgabenbackup; vollständige Datenordnerkopie |
| `glide.lock` | Temporäre Belegung | nicht kopieren |
| `datenordner.json` | Gerätebezogener Ablagezeiger | nicht im Aufgabenbackup |

Ein `.glidebackup` ist ein ZIP aus `data.json` und referenzierten Anhängen. Vollrestore ersetzt erst nach Validierung und Sicherung. Additiver Import erzeugt neue IDs und erhält den bisherigen Bestand. Teilbackups umfassen vollständige Zweige einschließlich leerer Unterordner. Archivpfade, Größen, Symlinks, doppelte Namen und Kompressionsverhältnisse werden weiter geprüft. Einstellungen und separater Vorlagenkatalog sind nicht Teil eines Aufgabenbackups.

Die frei wählbare Ablage liegt außerhalb des Programms. `GLIDE_DATA_DIR` hat für Tests Vorrang; andernfalls gelten Plattformstandard und optional `datenordner.json`. Ein Datenordnerwechsel kopiert in ein leeres Ziel oder öffnet einen vorhandenen Bestand; die Quelle bleibt erhalten. Erkannte Fremdbelegung verhindert Speichern. Die Sperre ersetzt keinen verteilten Synchronisationsdienst.

Historischer vollständiger [Zustellvertrag Format 13](31_ERINNERUNGEN_3.8.0.md) gilt technisch weiter. Aktuelle [Bedienung](32_UI_UND_BEDIENUNG_3.9.0.md) und [QA](07_QA_BERICHT.md).

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt `today_plan`; 3.13 ergänzt `table_columns` für die listenspezifische Tabellenansicht. Diese Werte sind persönliche Einstellungen, werden beim Laden bereinigt und sind kein Bestandteil eines Aufgabenbackups. Seit 3.14 führen Aufgabenformat 14, Backups und Vorlagen zusätzlich Bearbeitungstag und geschätzten Aufwand mit. [Bedienung 3.13](36_TABELLENANSICHT_3.13.0.md) · [Bedienung 3.12](35_MEIN_TAG_3.12.0.md).

3.14 ergänzt `planned_date` (ISO-Datum oder `null`) und `estimated_minutes` (ganze Minuten 1–60000 oder `null`) in jedem Punkt. Fehlende ältere Angaben werden leer ergänzt. Ungültige Werte werden vor einem Import abgewiesen. Beide Angaben sind unabhängig von Fälligkeit und Tagesauswahl. Gruppen und Überschriften tragen keine Planung. [Vollständige Regeln einschließlich Wiederholungen, Vorlagen und Export](37_PLANUNG_UND_AUFWAND_3.14.0.md).
