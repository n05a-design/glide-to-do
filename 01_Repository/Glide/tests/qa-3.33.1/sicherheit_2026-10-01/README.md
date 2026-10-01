# Sicherheit und öffentliches Repository 3.33.1 – Nachweis

Datiert 01.10.2026 · App unverändert 3.33.1 · Konfigurations-, Werkzeug- und Dokumentationsnachlauf, keine Produktionsversion

## Anlass

- **Auftrag des Inhabers:** Die READMEs auf GitHub aktualisieren und Sicherheitskonzepte einbauen, die auf den GitHub-Funktionen aufbauen.
- **Ausgangslage im Reiter *Security and quality*:** Sicherheitsrichtlinie, vertrauliche Meldungen, Dependabot-Warnungen und Code-Scanning waren aus oder nicht eingerichtet; Secret Scanning und Advisories waren aktiv.
- **Das Repository ist öffentlich.** Bei der Prüfung fielen auf:
  - 263 versionierte Rohprotokolle (`*.log`), die seit D09 freigegeben waren;
  - 57 Dateien mit Benutzerpfaden aus macOS- und Windows-Konten, überwiegend in diesen Protokollen.
- **Entscheidung des Inhabers:** Rohprotokolle nicht mehr veröffentlichen.

## Umsetzung

| Bereich | Änderung |
|---|---|
| Sicherheitsrichtlinie | [`.github/SECURITY.md`](../../../../../.github/SECURITY.md): vertraulicher Meldeweg, Umfang, Ablauf, Schutzmaßnahmen. `SECURITY.md` der Anwendung verweist darauf |
| Code-Scanning | [`.github/workflows/codeql.yml`](../../../../../.github/workflows/codeql.yml): CodeQL für Python und Workflows bei Push, Pull Request und wöchentlich. Weil CodeQL nur `.py` liest, werden die `.pyw`-Dateien vor der Analyse gespiegelt; Archive und Lieferkopie sind ausgenommen |
| Abhängigkeiten | [`.github/dependabot.yml`](../../../../../.github/dependabot.yml): wöchentliche, gebündelte Aktualisierung der GitHub Actions. Laufzeitpakete gibt es nicht |
| Workflow-Härtung | Checkout ohne gespeichertes Token (`persist-credentials: false`), nur Leserechte |
| Fremdcode | CI-Schritt „Fremdcode“: lädt das in `vendor/provenance.json` genannte Paket von PyPI, prüft dessen SHA-256 gegen `provenance.json` und PyPI und vergleicht jede Datei unter `vendor/tkinterdnd2` |
| Datenschutz | CI-Schritt „Datenschutz“: keine versionierte Textdatei mit Benutzerpfad. Neues Werkzeug [`scripts/pflege/pfade_bereinigen.py`](../../../scripts/pflege/pfade_bereinigen.py) |
| Rohprotokolle | `Glide/.gitignore` schließt `*.log` wieder aus; 263 Protokolle aus dem aktuellen Stand genommen (in der Git-Historie erhalten) |
| Benutzerpfade | 110 Fundstellen in 27 Dateien ersetzt (`/Users/<Name>/` → `~/`, `C:\Users\<Name>` → `%USERPROFILE%`), byteweise, JSON gültig |
| READMEs | Wurzel-README als GitHub-Einstieg neu gegliedert (Abzeichen, Stand, Schnellstart, Ablage, Arbeitsweise, Qualität und Sicherheit, Lizenz); README des Quellbaums um CI, CodeQL, Datenschutz und Meldeweg ergänzt |
| Regeln | D09 in Arbeitsrichtung und Entscheidungsvorlage, `CLAUDE.md`, Übergabe, Planung, Test- und Werkzeug-READMEs, CHANGELOG |

## Prüfung (Linux-Container, Python 3.14.0rc2, Tk 8.6.14)

- **CI-Grundstufe mit `--lieferstand-streng`:** alle Schritte bestanden ([Ergebnis](grundstufe_streng_py3.14rc2/ergebnis.json)).
- **Fremdcode:** `tkinterdnd2` 0.6.3, 116 Dateien bytegleich zum Originalpaket. SHA-256 des Pakets `50c73863…` stimmt mit `provenance.json` und PyPI überein; `LICENSE` stammt aus `dist-info/licenses/`.
- **Gegenproben:**
  - Eine an `TkinterDnD.py` angehängte Zeile wird als Abweichung gemeldet.
  - Eine neue Datei mit `/Users/<Name>/` wird vom Datenschutz-Wächter gefunden.
  - `pfade_bereinigen.py` erhält CRLF-Zeilenenden, hält JSON gültig und lässt `/Users/Shared/` unverändert.
- **Ohne die entfernten Protokolle:** Standprüfung und Dokumentationsindex bestehen; kein aktives Dokument verlinkt auf eine `.log`-Datei.
- **YAML:** alle drei Dateien unter `.github` syntaktisch gültig. Der erste CodeQL-Lauf erfolgt mit dem Pull Request.

## Beim Inhaber (Einstellungen auf GitHub)

Diese Schalter lassen sich nicht über Dateien setzen; die Liste mit Begründung steht in der Antwort zum Pull Request:
- **Vertrauliche Meldungen:** Private vulnerability reporting einschalten.
- **Dependabot:** Alerts und Security updates einschalten.
- **Secret Scanning:** Push protection einschalten.
- **CodeQL:** **nicht** zusätzlich die Standardeinrichtung aktivieren.
- **Ruleset für `main`:** Statusprüfung „Grundstufe“ vor dem Merge verlangen, Force-Push und Löschen blockieren.

## Grenzen

- **Git-Historie:** Entfernte Protokolle und die ersetzten Pfade bleiben in der Historie öffentlich einsehbar. Ein Umschreiben der Historie war nicht beauftragt.
- **Archive ungeprüft:** Komprimierte Archive (`.glidebackup`, `.zip`) prüft der Datenschutz-Wächter nicht.
- **Fremdcode ohne Netz:** Ohne Netzzugang meldet der Schritt „Fremdcode“ nur einen Hinweis.
