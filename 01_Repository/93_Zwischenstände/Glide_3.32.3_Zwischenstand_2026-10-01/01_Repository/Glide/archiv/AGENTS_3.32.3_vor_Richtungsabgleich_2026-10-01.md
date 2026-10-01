# Glide – Arbeitsregeln

## Produktgrenzen

Glide ist eine lokale Desktop-Anwendung. Kernfunktionen müssen ohne Internet, Benutzerkonto oder Cloudservice funktionieren. Nutzerdaten bleiben außerhalb des Programm- und Installationsordners.

## Verbindliche Quellen

- Einstieg für jede neue Sitzung: `../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md` (Stand, Regeln, nächste Schritte)
- Pflegewerkzeuge für Versionswechsel und Abgleich nach `07_Python-Versionen`: `scripts/pflege/`
- Produkt und Grenzen: `docs/01_PRODUCT_CONSTRAINTS.md`
- Architektur: `docs/02_ARCHITECTURE.md`
- QA: `docs/05_QA_TESTPLAN.md`
- Daten und Backups: `docs/06_DATA_BACKUP_MIGRATION.md`
- Release: `docs/10_RELEASE_CHECKLIST.md`
- Aktuelle Version: `VERSION` und die dazu passende Konstante in `src/glide/app.pyw`
- Produkt- und Plattformidentitäten: `docs/decisions/PRODUCT_IDENTITY.md`
- Prüfstand und was ungeprüft blieb: `docs/07_QA_BERICHT.md`
- Übergabe an einen neuen Bearbeiter: `docs/09_PROJECT_HANDOFF.md`
- Wann Gruppe, wann Ordner, wann Zwischenüberschrift: `docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md`
- Betriebszustände und Grenzen der Erinnerungszustellung: `docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md`

## Entwicklungsregeln

1. Vor Änderungen den aktuellen Test ausführen und Nutzerdatenpfade prüfen.
2. Bestehende Funktionen, Nutzerdaten und Migrationen bewahren.
3. Datenformatänderungen nur mit eigener Migration, Sicherung und Tests vornehmen. Eine neue Listen- oder Ordnerart ist eine Datenformatänderung und hebt `DATA_SCHEMA_VERSION` – nur so öffnet eine ältere Fassung den Bestand schreibgeschützt, statt ihn zu überschreiben (29.09.2026).
4. Keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung einführen.
5. Tests dürfen niemals den echten Nutzerdatenordner verwenden. Die Isolierung läuft über die Umgebungsvariable `GLIDE_DATA_DIR`; `%APPDATA%` allein wirkt nur unter Windows und würde unter macOS und Linux die echten Daten treffen.
6. Änderungen in `CHANGELOG.md` und der relevanten Dokumentation festhalten.
7. Signing-Secrets, Zertifikate, Schlüssel, Tokens und Recovery-Codes niemals einchecken.
8. Änderungen an Punkten laufen durch `item_change`, an Listen und Ordnern durch `sidebar_change`; Umbauaktionen zusätzlich unter `guarded_structural_change`. Modale Dialoge ausschließlich über `run_modal`.
9. Oberflächensymbole ausschließlich als Textzeichen aus der Tabelle `ICONS`. Der Integrationstest erzwingt das. Einzige Ausnahme ist das Logo als Bild aus `resources/logo` (`logo.py`, seit 29.09.2026).
10. Überholte Dokumente werden nicht überschrieben, sondern zuerst in den `archiv/`-Unterordner desselben Ordners kopiert – benannt nach der Version, die sie beschreiben.

## Abschlusskriterium

Eine Änderung ist erst fertig, wenn Syntaxprüfung und passende automatisierte Tests grün sind, die Versionsangaben konsistent sind und verbleibende manuelle Prüfungen ausdrücklich genannt werden. Für den Inhaber ist sie erst angekommen, wenn `07_Python-Versionen` und `build/macos/Glide.app` den geprüften Stand tragen (`scripts/pflege/abgleich_07.py`, `packaging/macos/baue_app.py`, SHA-256; seit 30.09.2026).
