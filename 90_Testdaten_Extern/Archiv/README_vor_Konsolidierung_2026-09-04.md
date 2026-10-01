# Externe und manuelle Testdaten

Hier liegen manuelle Importbeispiele und größere externe Testsätze.

## Abgrenzung

- Kleine, versionierte Fixtures für den Integrationstest liegen unter
  `01_Repository/Glide/tests/fixtures/` – aktuell für die Datenformate 6, 5, 4
  und 2.
- Der aktuelle Prüfbestand für manuelle Tests mit realistischem Umfang liegt
  unter `05_Probelisten_Testdaten/` und trägt `2.6.0` im Namen.
- Dieser Ordner enthält die historischen Legacy-Beispiele.

## Stand 01.09.2026

Der Inhalt stammt aus der Zeit vor 2.5.0 und kennt weder Gruppen noch
Fälligkeiten, Beschreibungen, Farben oder Anhänge. Er bleibt bewusst erhalten:
gerade weil er alt ist, taugt er als Eingang für Migrationsprüfungen.

## Wichtig

Tests dürfen den echten Datenordner nicht berühren. Dafür `GLIDE_DATA_DIR` auf
ein leeres Verzeichnis setzen und die Anwendung damit starten.
