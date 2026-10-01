# Externe und manuelle Testdaten

Stand 14.09.2026 · Glide 3.21.2 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

Hier liegen manuelle Importbeispiele und größere externe Testsätze.

## Abgrenzung

- Kleine, versionierte Fixtures für den Integrationstest liegen unter
  `01_Repository/Glide/tests/fixtures/` – für die Datenformate 4 bis 15 sowie Legacy 2.
- Der aktuelle Prüfbestand für manuelle Tests mit realistischem Umfang liegt
  unter `05_Probelisten_Testdaten/` als `Glide-Funktionsvorschau_3.21.2.glidebackup`.
- Dieser Ordner enthält die historischen Legacy-Beispiele.

## Stand 14.09.2026 · aktueller App-Stand 3.21.2

Der Inhalt stammt aus der Zeit vor 2.5.0 und kennt weder Gruppen noch
Fälligkeiten, Beschreibungen, Farben oder Anhänge. Er bleibt bewusst erhalten:
gerade weil er alt ist, taugt er als Eingang für Migrationsprüfungen.

## Wichtig

Tests dürfen den echten Datenordner nicht berühren. Dafür `GLIDE_DATA_DIR` auf
ein leeres Verzeichnis setzen und die Anwendung damit starten.
