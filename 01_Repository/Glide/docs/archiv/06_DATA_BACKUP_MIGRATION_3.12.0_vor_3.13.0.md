# Daten, Backups und Migration – Glide 3.12.0

Stand 13.09.2026 · additive Einstellungserweiterung in 3.12

Aufgabenformat **13**, Einstellungen **2**, Vorlagenformat **2**. Die UI nennt Erinnerungen jetzt Benachrichtigungen; gespeicherte Felder und APIs wie `reminder`, `reminder_attention`, Zustellbelege und Aufschub bleiben unverändert. Neuer additiver boolescher Einstellungswert: `sidebar_visible`, Standard `true`. Design bleibt im bisherigen Feld `theme`.

Vor dem ersten Speichern von Aufgaben vor Format 13 entsteht die unrotierte unveränderte Originalkopie `backups/liste_vor_format13_<Zeitstempel>.json`. Bei Fehler wird nicht gespeichert. Formate 4–13 und Legacy 2 bleiben lesbar. Version 3.7 kann Format 13 nicht lesen.

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

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt die additive Einstellung `today_plan` für „Mein Tag“. Die Tagesauswahl enthält nur geordnete Aufgaben-IDs, wird am Tageswechsel geleert und ist kein Bestandteil eines Aufgabenbackups. Aufgabenformat 13, Backups und Vorlagen bleiben unverändert. [Bedienung 3.12](35_MEIN_TAG_3.12.0.md) · [Bedienung 3.11](34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md).
