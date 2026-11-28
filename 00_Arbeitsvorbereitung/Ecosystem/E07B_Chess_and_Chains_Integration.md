# E07-B – Chess & Chains: Shared Framework Integration (Arbeitsauftrag)

Stand 28.11.2026 (E06) · Glide 1.0.3 · Aufgabenformat 27 · Framework-Checkpoint `4e8758439cf3ffe7` · Shell 0.11.0 / Bento 0.4.0

Separat einsetzbarer Auftrag für den Entwicklungsagenten von Chess & Chains (https://github.com/n05a-design/chess-and-chains). Früher als E03 geführt (Zuordnung im [Entwicklungsplan §4.8.9](../Glide_Entwicklungsplan.md#489-fortschreibung-der-roadmap-d110-28112026)). Übergabe erst nach Freigabe des E06-Checkpoints durch den Inhaber; beide Folgeprojekte nutzen denselben Checkpoint. Dieser Glide-Auftrag hat Chess & Chains nicht verändert.

## 1. Ziel

Brett, Zugregeln, Engines, Partien, Rätsel, Varianten und Analyse bleiben in Chess & Chains; Shell und Bento übernehmen Fenster, Einstellungen, Übersichten, Statistiken und allgemeine Bedienung. Das Projekt migriert **einmal** von Shell 0.6.2 auf den gemeinsamen Stand.

## 2. Bekannter Ausgangsstand (öffentlich gelesen, vom Agenten zu prüfen)

- Chess & Chains `main` @ `13b27f65` (gelesen 28.11.2026), `__version__` 0.3.0, keine Veröffentlichung, Python ≥ 3.11; `src/glide_shell` 0.6.2 aus Glide `7dcd8dc0`, kein Bento.
- Funktionsbestand und Tests prüft der Agent vor jeder Änderung; Arbeitsstand sichern.

## 3. Verbindlicher Framework-Checkpoint (E06)

Übernommen wird ausschließlich aus dem Checkpoint **`4e8758439cf3ffe7`** (vollständig `4e8758439cf3ffe729589c54eb77e8957ad879908c000ab1f12280be5aa6092d`): Glide Shell **0.11.0** (kompatibel seit 0.6.2), Glide Bento **0.4.0** (verlangt Shell ≥ 0.11.0), Glide-System V1.98, Quellstand `9e8527c4 + lokale Änderungen (vor dem Commit; vor der Übergabe aus dem freigegebenen Commit neu erzeugen)`. Der Inhaber übergibt den Ordner (beim Inhaber unter `%USERPROFILE%\gq\e06\checkpoint`). Er enthält `CHECKPOINT.json` (Kennung, Quellstand, Manifest mit SHA-256, öffentliche Schnittstellen, Schnittstellenvergleich zu 0.6.2/`7dcd8dc0`, Kompatibilität, Prüfergebnisse, Leistungsnachweise, bekannte Einschränkungen), `src/glide_shell`, `src/glide_bento` und `tools/`.

1. Checkpoint prüfen: `python3 -B <checkpoint>/tools/framework_checkpoint.py --pruefen <checkpoint>` → „unverändert“.
2. Ausgangsstand belegen: `SHELL_MANIFEST.json` des Projekts nennt Shell 0.6.2 aus `7dcd8dc0`; Abweichungen melden, nicht überschreiben.
3. Vorab prüfen: `python3 -B <checkpoint>/tools/shell_uebernehmen.py --pruefen --mit-bento <quellordner>`; jeder Befund unter „Host-Vertrag“ wird zuerst im Projekt gelöst.
4. Übernehmen mit Sicherung außerhalb des Projekts: `python3 -B <checkpoint>/tools/shell_uebernehmen.py --mit-bento --unsauber-erlauben --sicherung <ordner> <quellordner>` (der Checkpoint vermerkt `framework_snapshot` im Manifest der Kopie). Für dieses Projekt ist es die erste Bento-Übernahme.
5. Rückkehr: `--zurueck <sicherung>` stellt Shell 0.6.2 bytegenau wieder her.
6. Vertrag und Grenzen: `src/glide_shell/AKTUALISIERUNG.md` im Checkpoint.

Nie aus einem Glide-Arbeitsbaum übernehmen; verwaltete Framework-Kopien bleiben unverändert.

## 4. Pflicht: produktive Integration (nicht nur Dateien kopieren)

| System | Verpflichtend | Erwartung |
|---|---|---|
| Shell-Fundament | ja | `AppHost` mit `add_shutdown`/`shutdown`, `workspaces` für die Fachbereiche, `modal_session`, `window_lifetime`, `desktop_adapter`, `runtime_paths` |
| Designsystem | ja | `color_roles.ThemeProvider` mit eigener Markenfarbe; eigene allgemeine Farb-/Knopf-/Suchfeldlösungen kontrolliert ablösen (`controls`) |
| Einstellungen | ja | `settings_registry` neben dem eigenen Speicherformat; kein Formatwechsel ohne Sicherung |
| Produktinformationen | ja | „Über“ mit `software_catalog.system_info`; Weitere Programme mit `glide_bento.marketing.PortfolioView` aus `ECOSYSTEM_CATALOG.json` |
| Symbole | ja | `symbols`/`symbol_picker`; fachliche Sammlungen als Anbieter des Projekts mit Lizenzangabe |
| Bento | ja, wo Kennzahlen/Übersichten bestehen | `charts`/`data` mit Daten des Projekts; Fachberechnung bleibt im Projekt |
| Caches/Hintergrund | wo Ressourcen oder lange Arbeit anfallen | `resources.BoundedCache`, `background.TaskQueue`; keine unbegrenzten Caches |
| Konformität | ja | `python -m glide_shell.conformance <quellordner>` → conform; Selbsttests Shell 16/16, Bento 16/16 |

## 5. Rückmeldevertrag

Fehlende allgemeine Funktionen nicht lokal bauen, sondern melden: anforderndes Projekt, Anwendungsfall, Checkpoint, genutzte Komponenten, fehlende Funktion, Datenvertrag, Interaktion, Wiederverwendbarkeit, Plattformen, Designanforderungen, Abnahmekriterien, Risiken ([Entwicklungsplan §4.8.2](../Glide_Entwicklungsplan.md#482-governance-und-rückmeldevertrag)).

## 6. Abnahme

Start und Bedienung (Windows; macOS/Linux soweit verfügbar), Konformität und Selbsttests aus der Kopie grün, Fachregressionen vor und nach der Integration grün, Datensicherung vor Formatänderungen, Leistungsmessung vorher/nachher mit eigenen Werkzeugen (keine Übernahme der Glide-Zahlen), Liste gemeldeter Framework-Anforderungen, Kompatibilitätszeile für die Matrix in Glide. Alle Prüfläufe unbeaufsichtigt (kein Dialog wartet auf den Inhaber).
