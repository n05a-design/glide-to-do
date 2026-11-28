# Aktualisierung einer vorhandenen Shell-Kopie (0.6.2 → 0.10.0)

Stand 28.11.2026 · Glide Shell 0.10.0 · Glide Bento 0.3.0 · Lizenz MPL-2.0 · [English version](UPDATING.md)

Dieser Vertrag gilt für Folgeprojekte, die `glide_shell` als verwaltete Kopie mit `SHELL_MANIFEST.json` führen (Stand E01: STEPS und Chess & Chains mit 0.6.2 aus Glide-Commit `793596f1`). Er beschreibt, was sich ändert, wie aktualisiert wird und wie der vorherige Stand zurückkommt.

## 1. Kompatibilität

- `SHELL_COMPAT_SINCE` bleibt **0.6.2**. Zwischen 0.6.2 und 0.10.0 wurde keine öffentliche Funktion, Klasse oder Methode entfernt, und kein Parameter wurde umbenannt oder umgestellt. Geprüft wird das maschinell über den Schnittstellenvergleich im Framework-Checkpoint (`interface_changes`: `removed` und `changed` leer).
- Ein Host, der nur die öffentlichen Namen von 0.6.2 nutzt, läuft nach der Aktualisierung unverändert. Das belegt T376 mit einem künstlichen 0.6.2-Host. Für STEPS und Chess & Chains selbst ist das **nicht** nachgewiesen; das prüft der jeweilige E03-Auftrag mit den eigenen Regressionstests.
- Hinzugekommene Parameter haben Standardwerte (`AppHost(on_callback_error=None)`). Das Verhalten ohne diese Argumente ist unverändert.
- Datenformate der Folgeprojekte sind nicht betroffen; die Shell schreibt keine Anwendungsdaten.

## 2. Was neu ist

| Fassung | Neu | Für Folgeprojekte |
|---|---|---|
| 0.7.0 | `compat`, `conformance`, `showcase` | Versionsprüfung, Architekturprüfung, Galerie-Register |
| 0.8.0 | `spellcheck` | Rechtschreibvertrag ohne Engine |
| 0.9.0 | `ActionHandle`, `DropIndicator`, `symbol_ink_offset` | Griffe, Ablageanzeige, optische Glyphenmitte |
| 0.9.1 | Vertragsregel Griffachse (D108) | Gestaltungsregel, kein Code |
| 0.10.0 | `color_roles`, `settings_registry`, `controls`, `workspaces`; `AppHost.add_shutdown`/`shutdown`/`on_callback_error`; Konformitätsregel `host-api` | Theme-Provider, Einstellungen, Knopf/Suchfeld/Tooltip/Werkzeugleiste, Arbeitsbereiche, geordnetes Beenden |

Glide Bento 0.3.0 verlangt Shell ≥ 0.7.0. Eine Bento-Übernahme neben einer Shell 0.6.2 lehnt das Werkzeug ab; Shell und Bento werden deshalb gemeinsam aktualisiert.

## 3. Host-Anforderungen ab 0.10.0

- Farben: ein Rollenwörterbuch mit `color_roles.CORE_ROLES`. `color_roles.validate` meldet fehlende Rollen und Kontraste unter WCAG 2.2 AA. Eine eigene Markenfarbe kommt über `with_accent` oder `ThemeProvider(accent=...)`, nie über Konstanten in Komponenten.
- Schrift: wie bisher `custom_controls.set_font_provider`.
- Einstellungen: Der Host behält sein eigenes Speicherformat. `SettingsRegistry` beschreibt, prüft und gruppiert nur; unbekannte Schlüssel bleiben erhalten.
- Arbeitsbereiche: Fachansichten werden als `Workspace(id, title, factory)` registriert. Die Shell kennt kein Datenmodell.

## 4. Ablauf

1. Arbeitsstand des Folgeprojekts sichern (Git-Commit oder Kopie).
2. Prüfen, ohne zu schreiben:
   `python3 -B tools/shell_uebernehmen.py --pruefen --mit-bento <projekt>/src`
   Die Ausgabe nennt veraltete, fehlende und lokal veränderte Dateien. Unter „Host-Vertrag“ steht jeder Import eines Namens, den die neue Shell nicht hat.
3. Aktualisieren mit Sicherung:
   `python3 -B tools/shell_uebernehmen.py --mit-bento --sicherung <ordner-außerhalb> <projekt>/src`
   Das Werkzeug lehnt ab bei lokalen Änderungen an der Kopie, bei Herabstufung, bei Host-Importen fehlender Namen, bei einer inkompatiblen Shell/Bento-Kombination und bei fremden Dateien gleichen Namens. Fachdateien des Hosts werden nie überschrieben; schlägt ein Schritt fehl, wird der Ordner zurückgerollt.
4. Prüfen: `python -m glide_shell.selftest` (16/16), `python -m glide_bento.selftest` (16/16), `python -m glide_shell.conformance <src>` (conform) und die eigenen Regressionstests.
5. Rückkehr bei Bedarf: `python3 -B tools/shell_uebernehmen.py --zurueck <sicherungsordner> <projekt>/src` stellt den gesicherten Stand bytegenau wieder her. Eine veränderte Sicherung wird abgewiesen.

## 5. Grenzen

- Geprüft unter Windows 11 mit Tk 9 und künstlichen Daten. macOS und Linux nativ sowie die echten Folgeprojekte sind offen (E03, E06).
- `--commit` liest eine ältere Quelle; der Host-Vertrag wird dann nicht geprüft.
- Die Shell ist vor 1.0. Kompatible Erweiterungen sind bis zur Stabilisierung nach E03 möglich, Brüche nur mit angehobenem `SHELL_COMPAT_SINCE` und Eintrag hier.
