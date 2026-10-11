# Beginn der gemeinsamen Sprintplanung (09.10.2026)

Stand 09.10.2026 · Glide 3.35.0 · Nachlauf ohne neue App-Version · Referenz-Mac, Python 3.14.5, Tk 9.0.3

Auftrag: neues umfangreiches Feature-Sprint-Paket gemeinsam auswählen, jede Funktion durch den Inhaber entscheiden lassen und erst nach Bestätigung des fertigen Paketplans umsetzen. Vollständig gelesene Grundlagen und vorläufige Aufgabenkarten stehen im [Entwicklungsplan §15](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#15-neuer-feature-sprint-ab-09102026-gemeinsame-planung), das Entscheidungsverfahren in der [Arbeitsrichtung](../../../docs/ARBEITSRICHTUNG.md). Noch keine neue Auswahlantwort; D18 ff. bleiben frei.

Geändert wurden ausschließlich Planungs-/Übergabedokumente und dieser Nachweis. Gezielte Primärquellen im Marktvergleich ergänzt, außerdem dessen falsche Glide-Markierung für „Erscheinungsbild wie System“ berichtigt (bereits seit 3.33.21 vorhanden). App, Version, Format, Prüfsuiten und Auslieferung unverändert gegenüber dem Merge-Stand `b5f5c226ccdb06b02537c8b091086bd5defd6fcd`.

## Prüfung

- [CI-Grundstufe](ci/ergebnis.json) mit strengem Lieferabgleich: Exitcode 0; Syntax, Versionen, Dokumentation, Fixtures, Werkzeug- und Fachlogiktests, fünf Analysen, isolierte Tk-Startprobe, Lieferstand, Datenschutz, Ablagegröße und Synchronisation grün.
- Fremdcodeabgleich mit PyPI blieb wegen `CERTIFICATE_VERIFY_FAILED` ein ausdrücklich ausgewiesener Hinweis; kein neuer Fremdcode und keine neue Abhängigkeit.
- [Unveränderter Lieferstand](ergebnis.json): Git-Abgleich von App, 07 und Showcase mit dem Merge-Stand ohne Differenz; 168 Code-/Ressourcendateien aus dem Quellbaum SHA-256-gleich zu 07, zusätzlich die für das macOS-Bundle vorgesehenen Dateien abgeglichen. Plattformfremde tkdnd-Bibliotheken werden nach dem bestehenden Bauwerkzeug nicht ins Mac-Bundle übernommen.
- Keine neue Vollprüfung oder Signaturprüfung: keine ausführbare Änderung und kein Bundlebau. Die früheren eingefrorenen Vollprüfungen bleiben Belege ihres jeweiligen Stands. Windows-/Linux- und menschliche Abnahme bleiben offen.

Rohprotokolle liegen außerhalb von OneDrive und werden nicht versioniert. Die Nachweisdateien enthalten keine Benutzerpfade.
