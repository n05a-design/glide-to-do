# Glide 3.50.0 – Abschlussabgleich vom 02.11.2026

Prüfauftrag: begonnene Features, Optimierungen und Erweiterungen auf Umsetzung, Dokumentation und Aktualität prüfen. Eingangsstand `e251453`; während der Prüfung traf aus einer anderen Sitzung `55d2caf` ein. App-SHA-256 unverändert `2fb07ca2f6d8d119639df56511e3313e0ac94564af66ad81a2c8284899a0403b`. Keine neue App-Version, kein neuer Paketbau und keine Nutzerdatenänderung durch diesen Audit.

## Ergebnis und verbindliche Statusquelle

Die gewählten Nutzerfunktionen bis 3.50.0 sind implementiert und geliefert. **Nicht alle begonnenen appweiten technischen Vorhaben sind abgeschlossen.** Vollständige Restliste und Folge ausschließlich im [Entwicklungsplan §21.44](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2144-abschlussabgleich-von-features-optimierungen-und-dokumentation); Befunde in [Analyse §13.23](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1323-abschlussabgleich-vom-02112026). Ungewählte Zukunftsoptionen und nach D58 zurückgestellte Readerabnahme sind keine fehlenden 3.50-Erstimplementierungen. Menschliche Sicht-/Bedien-, DPI-/Mehrmonitorprüfung bleibt offen.

Berichtigt wurden aktive Quell-/Lieferstände in Roadmap, Index und Quell-README, WA-09-/FP-Lieferstatus, D55-Auswahl, D58-Blockziehen/Readerstatus und nächste freie Entscheidung D59. Dokumentenpflege und Prüfwerkzeugbeschreibung nennen korrekt R1–R15. Historische Messungen und QA-Belege wurden nicht umetikettiert. README-Featureübersicht, Handbuch, Neuerungskatalog und CHANGELOG bilden die gewählten 3.50-Funktionen ab.

## Tatsächliche Prüfungen

| Beleg | Ergebnis / Grenze |
|---|---|
| [CI-Grundstufe vor der Dokumentpflege](grundstufe_vorlauf.json) | 19 Schritte, Exit 0; 238 Werkzeugtests (drei Skips), zweimal 1.112 Fachtests (je ein Skip), Syntax/Versionen/Links/Analysen/Startprobe und strenger Python-Lieferabgleich grün. Fremdcodeabruf wegen lokalem Python-CA-Pfad nur Hinweis; abschließender Lauf nutzt die vorhandene System-CA-Datei |
| [Abschließende CI-Grundstufe](grundstufe.json) | 19 Schritte, Exit 0; 238 Werkzeugtests (drei Skips), zweimal 1.112 Fachtests (je ein Skip), 460 Syntaxeingaben, 432 aktive Dokumentlinks und 116 Vendor-Dateien gleich dem Original. Anschließende reine Textpräzisierungen separat mit Stand-/Linkprüfung und `git diff --check` geprüft |
| [Bereichsprüfung](bereichspruefung.json) | Korrigierte `test_fortsetzung33311.py` auf macOS/Python 3.14.5 grün; suiteeigener temporärer `GLIDE_DATA_DIR`, null Differenzfälle. Kein neuer nativer Windows-Gegenlauf |
| [Quell-/Lieferabgleich](quell_lieferabgleich.json) | 238 Python-Dateien bytegleich; 463 Mac- und 104 Windows-Dateien gleich den Bauinventaren, beide Archivhashes gleich der Lieferung; Mac-Ad-hoc-Signatur erneut grün |
| [Remote-CI-Abruf](github.json) | Historischer grüner Lauf 41438822957, späterer roter `main`-Lauf 41454826947 und neue Matrix 41465033321 getrennt mit tatsächlichem Abrufstatus; laufende Jobs sind keine Erfolge |
| [Abhängigkeitsabgleich](abhaengigkeiten.json) | Neun Paketnamen mit Version/Datum/Primärquelle live gegen PyPI geprüft. Neuere Fassungen erkannt; keine ungeprüfte Übernahme in fertige Pakete |

Der [reproduzierbare Hashabgleich](pruefabgleich.py) liest die tatsächlichen Quell-/Lieferdateien, die bestehenden Bauinventare und Git-Blobs von `b2b54e7`. Alle 941 Eingaben des früheren Mac-Laufs werden gegen den heutigen Bestand geprüft. Inhaltlich abweichend sind die unabhängig eingetroffene Testkorrektur `test_fortsetzung33311.py` und die hier berichtigte reine Regelanzahl im Moduldocstring von `standpruefung.py`; weitere Unterschiede betreffen ausschließlich LF/CRLF. Der frühere 108-Suiten-Volllauf bleibt ein Beleg seines ursprünglichen Teststands. Es wurde kein neuer vollständiger Integrationslauf behauptet.

```bash
# Aus 01_Repository/Glide; der Hashabgleich importiert die App nicht.
python3 -B tests/qa-3.50.0/abschlussabgleich_2026-11-02/pruefabgleich.py

# macOS-System-CA nur für diesen Prozess, ohne Zertifikatsprüfung abzuschalten.
SSL_CERT_FILE=/etc/ssl/cert.pem python3 -B tests/tools/ci_grundstufe.py \
  --lieferstand-streng --protokoll /tmp/glide-abschlussaudit-20261102-final
```

## Aktuelle Abhängigkeiten

| Paket | Geprüfter Pin | PyPI am 02.11.2026 | Folgerung |
|---|---|---|---|
| PyInstaller | 6.22.3 | [6.22.3](https://pypi.org/project/pyinstaller/6.22.3/) | Aktuell |
| pyinstaller-hooks-contrib | 2026.8 | [2026.9](https://pypi.org/project/pyinstaller-hooks-contrib/2026.9/) | Upgrade mit neuen nativen Bau-/Startbelegen |
| setuptools | 84.1.0 | [84.2.1](https://pypi.org/project/setuptools/84.2.1/) | Upgrade mit neuen nativen Bau-/Startbelegen |
| tkinterdnd2 | 0.6.3 | [0.7.0](https://pypi.org/project/tkinterdnd2/0.7.0/) | Wheel-/Bibliotheks-/Hookvergleich, Herkunft/Hashes und native DnD-/Paketprüfung vor Übernahme |

altgraph, macholib, packaging, pefile und pywin32-ctypes entsprechen zum Abrufzeitpunkt den neuesten PyPI-Fassungen. Gepinnte Laufzeitquellen und das installierte System-Python wurden nicht aktualisiert; deren bewusste Reproduzierbarkeit und native Prüfbelege bleiben erhalten. Diese Prüfung ist keine vollständige Recherche sämtlicher Betriebssystem-/Toolchain-Releases und kein neuer Sicherheitsscan.

## Grenzen

WA-32/36/37/38/39/40 bleiben appweite Teilvorhaben. WA-46-SBOM sowie WA-49-Initialisierung und WA-50-Prüfbudget sind noch nicht umgesetzt. WA-41A/B-Ursachen bleiben unbewiesen; keine zusätzliche Intel-Stressserie. Vorhandene Lizenz-/Bau-/Dateilisten ersetzen keine CycloneDX-/SPDX-SBOM. Die frühere QA-Ablage `qa-3.43.1` war beim Einstieg bereits unversioniert vorhanden und wurde nicht verändert oder entfernt. Automatisierte Checks erfassen nicht pauschal den Inhalt sämtlicher lokaler ignorierter Altbelege oder separater Worktrees.

Rohlogs bleiben lokal; veröffentlichte JSON-Nachweise sind über das vorhandene Pflegewerkzeug von Benutzerpfaden bereinigt. [Maschinenlesbarer Abschluss](ergebnis.json).
