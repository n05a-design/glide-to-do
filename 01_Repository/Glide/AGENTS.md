# Glide – Arbeitsregeln

## Produktgrenzen

Glide ist eine lokale Desktop-Anwendung. Kernfunktionen müssen ohne Internet, Benutzerkonto oder Cloudservice funktionieren. Nutzerdaten bleiben außerhalb des Programm- und Installationsordners.

## Verbindliche Quellen

- Einstieg für jede neue Sitzung: `../../00_Arbeitsvorbereitung/Glide_Uebergabe.md` (Stand, Regeln, nächste Schritte)
- Aufgaben mit Status: `../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`
- Entscheidungen D01–D44, Auftrag und Arbeitsablauf: `docs/ARBEITSRICHTUNG.md`
- Produkt, Grenzen und Prinzipien: `docs/01_PRODUCT_CONSTRAINTS.md`
- Architektur, Performance-Regeln, Tk-Fallstricke: `docs/02_ARCHITECTURE.md`
- Verhalten der Funktionen: `docs/20_FUNKTIONEN.md`
- QA: `docs/05_QA_TESTPLAN.md`, geprüfter Stand und was ungeprüft blieb: `docs/07_QA_BERICHT.md`
- Daten und Backups: `docs/06_DATA_BACKUP_MIGRATION.md`
- Release, Lizenz, Signierung, Store: `docs/10_VEROEFFENTLICHUNG.md`
- Aktuelle Version: `VERSION` und die dazu passende Konstante in `src/glide/app.pyw`
- Produkt- und Plattformidentitäten: `docs/decisions/PRODUCT_IDENTITY.md`
- Wann Gruppe, wann Ordner, wann Zwischenüberschrift: `docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md`
- Betriebszustände und Grenzen der Erinnerungszustellung: `docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md`
- Pflegewerkzeuge für Versionswechsel, Abgleich nach `07_Python-Versionen` und Kürzen der Ablage: `scripts/pflege/`

## Entwicklungsregeln

1. Vor Produktionsänderungen eine passende bestehende Baselineprüfung ausführen und Nutzerdatenpfade prüfen. Dokumentations-/Prüfwerkzeugnachläufe nach `docs/ARBEITSRICHTUNG.md` behandeln; unveränderte App-Version erhalten.
2. Bestehende Funktionen, Nutzerdaten und Migrationen bewahren.
3. Datenformatänderungen nur mit eigener Migration, Sicherung und Tests vornehmen. Eine neue Listen- oder Ordnerart ist eine Datenformatänderung und hebt `DATA_SCHEMA_VERSION` – nur so öffnet eine ältere Fassung den Bestand schreibgeschützt, statt ihn zu überschreiben (29.09.2026).
4. Keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung einführen.
5. Tests dürfen niemals den echten Nutzerdatenordner verwenden. Die Isolierung läuft über die Umgebungsvariable `GLIDE_DATA_DIR`; `%APPDATA%` allein wirkt nur unter Windows und würde unter macOS und Linux die echten Daten treffen.
6. Änderungen in `CHANGELOG.md` und der relevanten Dokumentation festhalten.
7. Signing-Secrets, Zertifikate, Schlüssel, Tokens und Recovery-Codes niemals einchecken.
8. Änderungen an Punkten laufen durch `item_change`, an Listen und Ordnern durch `sidebar_change`; Umbauaktionen zusätzlich unter `guarded_structural_change`. Modale Dialoge ausschließlich über `run_modal`.
9. Oberflächensymbole ausschließlich als Textzeichen aus der Tabelle `ICONS`. Der Integrationstest erzwingt das. Einzige Ausnahme ist das Logo als Bild aus `resources/logo` (`logo.py`, seit 29.09.2026).
10. Aktuelle Dokumente an ihrer verbindlichen Quelle fortschreiben: ein Thema, ein Dokument. Seit dem Auftrag vom 03.10.2026 werden doppelte und überholte Dokumente zusammengeführt und gelöscht statt archiviert oder mit `_Z` markiert; Git trägt die Historie. Neue Funktionen bekommen einen Abschnitt in `docs/20_FUNKTIONEN.md`, keine eigene Vertragsdatei. Archive und Nachweise nur der sieben neuesten Versionen (`scripts/pflege/ablage_kuerzen.py`). Siehe `docs/DOKUMENTENPFLEGE.md`.

11. Aufgabenstatus, nächste Schritte, Entscheidungen und Prüfgrenzen in Entwicklungsplan, Arbeitsrichtung und Übergabe inhaltlich abgleichen. Aktuelle Versionszeilen allein reichen nicht.
12. Caches nach stabilen IDs und Host-Lebensdauer führen, vollständig invalidieren; Undo kann Objekte ersetzen. Ersetzte Bindungen/after-Aufträge freigeben. Keine verschachtelten `update()`/`update_idletasks()` in selbstauslösenden Rückrufen. Details und Abnahme in `docs/ARBEITSRICHTUNG.md`.

13. Nach D17 entsteht neue oder angefasste Fachlogik als Tk-freies Modul mit eigenen Unit-Tests; bestehende UI- und Mutationseinstiege bleiben erhalten. Seit D09 ist die Git-Arbeitskopie des gesamten Projektordners maßgeblich.

## Abschlusskriterium

Eine Änderung ist erst fertig, wenn Syntaxprüfung und passende automatisierte Tests grün sind, die Versionsangaben konsistent sind und verbleibende manuelle Prüfungen ausdrücklich genannt werden. Für den Inhaber ist sie erst angekommen, wenn `07_Python-Versionen` und `build/macos/Glide.app` den geprüften Stand tragen (`scripts/pflege/abgleich_07.py`, `packaging/macos/baue_app.py`, SHA-256; seit 30.09.2026).
