# Sicherheitsrichtlinie

Glide ist eine lokale Desktop-Anwendung für Aufgaben, Notizen und Pinnwände. Sie überträgt keine Nutzerdaten und öffnet keine Netzwerkverbindungen. Technische Sicherheitsregeln (Import, Anhänge, Datenordner, mitgelieferter Fremdcode) stehen in [`01_Repository/Glide/SECURITY.md`](01_Repository/Glide/SECURITY.md).

## Unterstützte Fassungen

Es gibt noch keine veröffentlichte Releasefassung. Korrekturen gehen in den laufenden Entwicklungsstand auf `main` (Version in [`01_Repository/Glide/VERSION`](01_Repository/Glide/VERSION)) und von dort in den Lieferordner `07_Python-Versionen`.

## Schwachstelle melden

- **Vertraulich über GitHub:** Reiter **Security** → **Report a vulnerability**. Die Meldung ist nur für die Verantwortlichen sichtbar.
- **Keine öffentlichen Issues** für Sicherheitsfunde.
- **Keine echten Daten:** Keine echten Nutzerdaten, Sicherungen (`.glidebackup`) oder Anhänge mitschicken; ein künstliches Beispiel genügt.
- **Hilfreich sind:**
  - betroffene Version,
  - Betriebssystem mit Python- und Tk-Version,
  - Schritte zum Nachstellen,
  - erwartetes und tatsächliches Verhalten.

**Ablauf nach einer Meldung:**
1. Eingangsbestätigung.
2. Bewertung und Nachstellen mit künstlichen Daten.
3. Korrektur mit Prüfung.
4. Bei Bedarf ein Security Advisory im Repository.

## Im Umfang

- **Anwendung:** Code unter `01_Repository/Glide/src/glide` und dessen Lieferkopie in `07_Python-Versionen`.
- **Dateneingang:** Import von Sicherungen, Vorlagen, CSV- und Kalenderdateien sowie Anhängen.
- **Fremdcode:** mitgelieferte Erweiterung unter `src/glide/vendor` (tkDnD).
- **Werkzeuge:** Prüf- und Pflegewerkzeuge sowie die GitHub-Workflows.

Nicht im Umfang: Schwachstellen in Python, Tk oder im Betriebssystem selbst; diese bitte beim jeweiligen Hersteller melden.

## Schutzmaßnahmen im Repository

| Maßnahme | Wo |
|---|---|
| CI-Grundstufe bei jedem Push und Pull Request: Prüfungen, Startprobe, Lieferstand, **Herkunft des Fremdcodes** gegen das Originalpaket, **keine Benutzerpfade** in versionierten Dateien | `.github/workflows/python-app.yml`, `01_Repository/Glide/tests/tools/ci_grundstufe.py` |
| Wöchentliche Aktualisierung der verwendeten GitHub Actions | `.github/dependabot.yml` |
| Keine Schlüssel, Zertifikate, Zugangsdaten oder Signing-Secrets im Repository; Secret Scanning ist aktiv | `.gitignore` (Abschnitt Sicherheit) |
| Keine echten Nutzerbestände, Sicherungen oder Archivkopien; Archive und Nachweise nur der sieben neuesten Versionen | `.gitignore`, CI-Schritt „Ablagegröße“ |
| Rohprotokolle (`*.log`) bleiben lokal; veröffentlichte Prüfergebnisse enthalten keine Benutzerpfade (vor dem Hochladen `python3 -B scripts/pflege/pfade_bereinigen.py <Ordner>`) | `.gitignore`, CI-Schritt „Datenschutz“ |

`.gitignore` verhindert nur das versehentliche Hinzufügen neuer Dateien; bereits versionierte Dateien, `git add -f` und Uploads über die Weboberfläche umgehen es. Deshalb setzen CI und Secret Scanning die Regeln zusätzlich durch.
