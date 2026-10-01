# Startkontext – Glide 3.7.0

Stand: 07.09.2026 · Aufgabenformat 12 · Einstellungen 2 · Vorlagenformat 2

Arbeitsordner: `C:/Users/Timvo/OneDrive/Glide ToDo/01_Repository/Glide`.
Kanonischer Code: `src/glide/app.pyw`. Die startbare Kopie im äußeren
`07_Python-Versionen/` muss mitsamt `resources/fonts/` weitergegeben werden.

Zuerst `AGENTS.md`, [Produktgrenzen](01_PRODUCT_CONSTRAINTS.md),
[Architektur](02_ARCHITECTURE.md), [Feature-Abgleich](25_FEATURE_ABGLEICH_3.7.0.md)
und [aktuellen QA-Bericht](24_VERSION_3.7.0.md) lesen. Aktueller Quellstand und
nachgewiesene Tests haben Vorrang vor Claudes zitierten Linux-Protokollen.
Die nicht vorliegende Linux-Datei wurde nicht als fertig vorhanden angenommen.

Der 3.7-Ausbau umfasst Navigation, Eingabefarben, reichere Anlage, Vorlagen
mit Bearbeitung/Speicherung, verlustfreie Teilbackups, Datenordnerwechsel,
Belegungsprüfung, private Schriften, Personalisierung, Mondphase,
Bearbeitungskalender und Materialdarstellung. Die genaue Zuordnung der
ursprünglichen Wünsche steht in der Feature-Matrix.

Prüfen unter Windows:

```powershell
$env:GLIDE_DATA_DIR = Join-Path $env:TEMP 'glide-qa-isoliert'
& C:\Python312\python.exe tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.7.0/erneute-pruefung
```

Tests setzen zusätzlich eigene temporäre Datenpfade vor dem App-Import.
Niemals echte Nutzdaten für Experimente laden. Bestehende Formate und historische
Fixtures erhalten. Normale Änderungen über die Änderungsrahmen; Dialoge über
`run_modal`. Vor dem Ersetzen eines aktuellen Dokuments dessen Vorfassung
archivieren.

Offen bleiben die ausdrücklich ausgewiesenen Plattform- und Veröffentlichungsschritte:
macOS, reale Synchronisation zwischen zwei Geräten, weitere DPI/Monitore,
Langzeitbedienung, Installer, Signatur und Storefreigabe. Echtes per Panel
Blur und ein Ersatz des Treeview sind nicht Teil der vorhandenen Tk-Oberfläche.
Die früheren 3.2-/3.5-Arbeitsaufträge im Archiv sind keine neuen Aufgaben.

## Stand 3.7.0

Aktuelle Ergänzungen und Prüfnachweise: [Version 3.7.0](24_VERSION_3.7.0.md). Versionsgebundene 3.6-Berichte beschreiben den vorherigen Stand.

Startbare Kopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.7.0.pyw` im übergeordneten Arbeitsbereich. Erster Schritt für Folgearbeiten: AGENTS.md lesen, aktuellen Nachweis prüfen und Tests mit isolierter Ablage ausführen. Fertige 3.6-/3.7-Funktionen nicht erneut als offen behandeln.

Aktueller Einstieg für die Nachbesserung 11.09.2026: [Mac, Vorlagen und Ablage](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md).
