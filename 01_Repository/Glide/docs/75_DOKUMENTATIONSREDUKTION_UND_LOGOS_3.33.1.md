# Dokumentationsreduktion und neue Logos

Stand 01.10.2026 · Glide 3.33.1 · Datenformat 20

Der Inhaber hat am 01.10.2026 ausdrücklich erlaubt, doppelte und überholte Dokumente zu löschen. Diese Anweisung ersetzt die frühere Vorgabe, jede Änderung nochmals zu archivieren oder mit `_Z` vorzumerken. Aktuelle Informationen werden an ihrer verbindlichen Quelle fortgeschrieben. Git enthält die Änderungshistorie; eine zusätzliche vollständige Markdown-Kopie bei jeder Pflege entfällt.

## Wissen an den verbindlichen Quellen

| Thema | Verbindlicher Einstieg |
|---|---|
| Architektur, Mutationen, UI und Cache-Lebensdauer | [Architektur](02_ARCHITECTURE.md), [Arbeitsrichtung](ARBEITSRICHTUNG.md) |
| Formate, Migrationen, Anlagen und Rücksicherung | [Datenvertrag](06_DATA_BACKUP_MIGRATION.md) |
| Produktgrenzen, lokale Nutzung und Entscheidungen | [Produktgrenzen](01_PRODUCT_CONSTRAINTS.md), [Entscheidung D09–D17](../../../00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md) |
| Prüfungen und tatsächlich nachgewiesener Stand | [Testplan](05_QA_TESTPLAN.md), [QA-Bericht](07_QA_BERICHT.md) |
| Laufende Aufgaben und neue Richtungen | [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md), [Auswahl A–H](../../../00_Arbeitsvorbereitung/Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md) |
| Vier Bereiche, erlaubte Inhalte und Fenster | [Vertrag 3.33.1](74_BEREICHE_UND_FENSTER_3.33.1.md) |

Technische Lehren aus früheren Ständen bleiben gültig: vor einer Mutation vollständig prüfen; Undo und stabile Kennungen erhalten; Anlagenpfade begrenzen; Migrationen sichern; modale Fenster ausschließlich über `run_modal`; macOS-Menüaktionen weiterhin verzögert über `after_idle` starten; keine verschachtelten Layout-/Update-Schleifen in Configure-Rückrufen; Tests immer mit temporärem `GLIDE_DATA_DIR`. Die aktuellen Quellen und Prüfungen tragen diese Regeln.

Frühere Feature-Vorräte sind keine neuen Aufträge. Fokus/Pomodoro, Wochenrückblick, Wiedervorlage, Ziele und Gewohnheiten bleiben im aktuellen Plan bzw. Vorrat. Echte Aufgabenabhängigkeiten benötigen weiterhin eine eigene Entscheidung über Kreisprüfung und Blockierungswirkung. Kalenderimport/-export ist keine Synchronisierung; steigendes `SEQUENCE`, vollständige Wiederholungsregeln, Konflikte und Löschweitergabe gehören zu einem gesonderten Schnitt. Automatisches Weitergeben von Fehlerprotokollen und Zusammenführen globaler Pinnwände sind nicht stillschweigend genehmigt. Store-Angaben müssen vor einer Einreichung aktuell geprüft werden. Diese Grenzen ersetzen die verstreuten alten offenen Entscheidungslisten als Einstieg; bereits beantwortete Fragen werden nicht erneut vorgelegt.

## Bereinigung

Die Bereinigung erfolgt ordnerweise und nur für Dokumentationskopien: Arbeitsvorbereitung, Checklisten, Repository-Dokumentation/Entscheidungen, Grafikmaster, Store-Material und begleitende README-Archive. Eine Kopie wird nur entfernt, wenn eine gepflegte Quelle oder ein einzelner fachlicher Vertrag erhalten bleibt. Eine bytegleiche Austauschformat-Dublette und zwei bereits überholte `_Z`-Prüflisten werden ebenfalls entfernt.

Ältere Funktionsverträge mit fortbestehendem Inhalt bleiben trotz Versionsalter erhalten, etwa Erinnerungen, Kalenderausgabe, App-Backup, CSV und Druck. Historische Importfixtures, Nutzerdaten, Grafikquellen, Produktionscode und Prüfresultate werden durch diese Dokumentationsbereinigung nicht verändert. Alte vollständige Liefer- und QA-Bestände sind eine getrennte Ablagefrage und werden hier nicht als Markdown-Dubletten behandelt.

Entfernt wurden 1506 Dateien mit zusammen 18,593,183 Bytes. Sechs alte Entscheidungslisten sind am gemeinsamen Wissenseinstieg zusammengeführt.

Der [Lösch- und Verweisnachweis](../tests/qa-3.33.1/bereiche_fenster_2026-10-01/archiv_bereinigung.json) nennt je Datei Pfad, vorherigen SHA-256, Größe, Grund und erhaltene Quelle. Er speichert keine erneute Kopie des gelöschten Inhalts. Nach dem ersten POSIX-Löschlauf wurden die Dateien erneut sichtbar. Die finale Entfernung erfolgt über `FileManager.trashItem` mit SHA-256-Abgleich; alle 1.506 ausgewählten Dateien sind danach außerhalb der Projektordner im macOS-Papierkorb. Dieser Löschweg bewahrt die Wiederherstellbarkeit, ohne neue Austauschkopien in der Ablage anzulegen. Die genaue Ursache des Wiederauftauchens ist nicht abschließend nachgewiesen.

## Logo-Quellen und Auslieferung

Die direkt an den Formen gespeicherten Attribute der neuen Exporte vermeiden die CSS-Abhängigkeit des SVG-Lesers:

- App-Zeichen: `20_Grafik_Master/01_Logo/Glide-Logo-01.svg` → `resources/logo/glide-logo.svg`.
- Programmsymbol: `20_Grafik_Master/03_Fav-Icon/App-Icon-transparent-02.svg` → `resources/logo/glide-app-icon.svg`.
- PNG-Rückfälle stammen aus den jeweils danebenliegenden aktuellen PNG-Mastern. Der frühere weiße Icon-Master wird nicht mehr verwendet.

Die gewählten SVG-Dateien werden unverändert kopiert. `svg_geometry.py` verarbeitet relative und absolute kubische Kurven einschließlich verkürzter `S`-Kurven sowie transparente Innenkonturen für den Canvas-Rückfall. CSS-basierte Exporte bleiben ebenfalls lesbar und Akzentfarben weiterhin einstellbar. Die Programmsymbole für Windows, Linux und macOS werden aus demselben neuen SVG erzeugt. Grafikvarianten bleiben als bewusst bereitgestellte Quellen erhalten.

24 Tk-freie Unit-Tests und der Logo-Integrationstest prüfen die Geometrie, Farbersetzung, Innenaussparung, fünf Designs, acht Ansichten und den Rückfall. Der endgültige Volllauf und Lieferabgleich werden im QA-Bericht derselben Version eingetragen.
