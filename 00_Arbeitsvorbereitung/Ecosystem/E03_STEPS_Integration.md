# E03 – STEPS: Shared Framework Integration (Arbeitsauftrag)

Stand 28.11.2026 · Glide 1.0.3 · Aufgabenformat 27 · Framework-Checkpoint Shell 0.9.1 / Bento 0.3.0

Separat einsetzbarer Auftrag für den Entwicklungsagenten von STEPS (https://github.com/n05a-design/steps). Er wird erst nach Freigabe durch den Inhaber übergeben. Dieser Glide-Auftrag hat STEPS nicht verändert.

## 1. Ziel

Die vorhandene musikalische Fachlogik von STEPS läuft innerhalb einer konsistenten Glide-Shell-Architektur. Geeignete Bento-Komponenten werden produktiv verwendet. Die Fachlogik wird nicht neu entwickelt.

## 2. Bekannter Ausgangsstand (öffentlich gelesen am 28.11.2026, ungeprüft)

- STEPS `VERSION` 0.8.0-dev, letzter Commit `8fe71630` auf `main`, Python ≥ 3.11.
- `glide_shell` 0.6.2 aus Glide-System V1.86 mit unverändertem `SHELL_MANIFEST.json`; kein `glide_bento`.
- Der tatsächliche Funktionsbestand (Keyboard, Tonleitern, Akkorde, Progressionen, Theorie, Lernbereiche, Wissensbibliothek, Analyse, Komposition) ist **vom STEPS-Agenten zu prüfen**, bevor etwas geändert wird.

## 3. Framework-Checkpoint

Übernahme ausschließlich aus einem eindeutig identifizierten Checkpoint (`CHECKPOINT.json` mit `snapshot_id`, Dateimanifest, SHA-256, öffentlichen Schnittstellen, Kompatibilität). Erzeugung in Glide: `python3 -B scripts/pflege/framework_checkpoint.py <Ziel>`, Prüfung mit `--pruefen`. Übernahme in STEPS mit `shell_uebernehmen.py --mit-bento`. Verwaltete Framework-Kopien werden in STEPS nicht dauerhaft verändert.

## 4. Verbindliche Arbeitsweise

1. Bestandsprüfung vor jeder Änderung; Arbeitsstand sichern.
2. Shell 0.6.2 → Checkpoint-Stand anheben, Manifest prüfen, Konformität (`python -m glide_shell.conformance`) grün.
3. Shell als Anwendungsfundament: `AppHost`, `modal_session`, `window_lifetime`, `desktop_adapter`, `runtime_paths`, Theme über Provider. Konkurrierende allgemeine UI-Mechanismen kontrolliert ablösen.
4. Bento dort, wo Kennzahlen, Karten und Raster passen (z. B. Lernfortschritt, Übungsübersicht, Wissenskarten); Musiktheorie bleibt in STEPS.
5. Datensicherheit: vorhandene STEPS-Daten nie still migrieren; Sicherung vor Formatänderungen.
6. Regressionstests der Fachfunktionen vor und nach der Integration.
7. Versionsfortschreibung von STEPS nach eigenem Vertrag; Framework-Version wird übernommen, nicht verändert.
8. Fehlende allgemeine Komponenten **nicht** lokal bauen, sondern über den Rückmeldevertrag an Glide melden.

## 5. Rückmeldevertrag (je fehlender Framework-Funktion)

Anforderndes Projekt · tatsächlicher Anwendungsfall · Framework-Version (Snapshot) · bereits genutzte Komponenten · fehlende Funktion · gewünschter Datenvertrag · gewünschte Interaktion · Wiederverwendbarkeit · Plattformen · Designanforderungen · Abnahmekriterien · Risiken. Vorlage: [Entwicklungsplan §4.8](../Glide_Entwicklungsplan.md#48-glide-ecosystem-e01e08-ab-28112026).

## 6. Abnahme

Start und Bedienung auf Windows (macOS/Linux, soweit verfügbar), Konformität grün, Selbsttests aus der Kopie grün, Fachregressionen grün, Liste gemeldeter Framework-Anforderungen, Kompatibilitätszeile für die Matrix in Glide.
