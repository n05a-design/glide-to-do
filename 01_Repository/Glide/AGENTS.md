# Glide – Arbeitsregeln

## Produktgrenzen

Glide ist eine lokale Desktop-Anwendung. Kernfunktionen müssen ohne Internet, Benutzerkonto oder Cloudservice funktionieren. Nutzerdaten bleiben außerhalb des Programm- und Installationsordners.

## Verbindliche Quellen

- Einstieg für jede neue Sitzung: `../../00_Arbeitsvorbereitung/Glide_Uebergabe.md` (Stand, Regeln, nächste Schritte)
- Aufgaben mit Status: `../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`
- Entscheidungen D01–D83 (D81–D83: Überlastungsgründe im Entlastungsdialog, Meldung bei nicht erreichbarem Datenordner, verbindliche Gestaltungslehren aus der Marktanalyse; D78: Dreierpaket 3.54.0 mit Fundortübersicht WA-21, JSON Canvas 1.0 WA-07 und Sperrklinke 0/0; D77: Schriftwechsel auf DM Mono, DM Serif Display und Charis SIL; D74: Steps-Übernahmegrundlage, technische Systemfeatures und neutrale aktive Produkttexte; D75: Seitenleiste und Fensterkopf; D76: unabhängiges Schriftgewicht, Kopflogo und Themenfarben; D66–D69 und D71 Abnahme 07.11.: keine Systemelemente im Altstil, Neuerungen höchstens drei Versionen, Unterzeile neben dem Logo, Maximallängen mit Restzähler, Anhangsnamen höchstens 40 Zeichen, Ansichtstitel in Themenfarbe, Leistenauswahl als Knopf und Auswahlpfeil neben dem Text, Seitentitel nur im Kopf; D70 Bündelung als 3.50.6 nach unabhängigen Prüfungen und weiterer menschlicher Abnahme; D62 neue Logo-Master und Darkmode-Gelb, D49 als Auslegung mit Korrekturvorbehalt, D50 UI-/UX-Vorrang, D51 phasenweise Prüfung, D52–D54 zentrale Roadmap/Designgeltung/Integrationsbewertung/Pflege, D55 Auswahl E-U1 A/E-U2 A/E-U3 A), Auftrag und Arbeitsablauf: `docs/ARBEITSRICHTUNG.md`; neue Produktentscheidungen ab D84
- Appweiter Gestaltungsvertrag für jede neue oder angefasste Oberfläche: `docs/DESIGN_RICHTLINIEN.md` einschließlich Kontext-/Komponentenmatrix und Paketnachweis; Originalauftrag: `../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md`
- Produkt, Grenzen und Prinzipien: `docs/01_PRODUCT_CONSTRAINTS.md`
- Architektur, Performance-Regeln, Tk-Fallstricke: `docs/02_ARCHITECTURE.md`
- **System-und-Modulpflege (eigenständige Version):** `src/glide/README.md` (Glide-System) ist das einzige aktuelle vollständige Inventar von Modulen, Funktionen, Wiederverwendung, Testdateien und datierten QA-Risiken. Bei Modul-/Feature-/Teständerungen im selben Commit pflegen; `tests/tools/test_glide_system.py` läuft über die CI-Grundstufe.  Architektur-/Paketierungsdokumente dürfen keine zweite vollständige Modulbestandsliste führen. Die **Systemversion** steht allein in `GLIDE_SYSTEM_VERSION` (Start: V1.0, unabhängig von `VERSION`); jede inhaltliche Katalogänderung hebt sie nach den Regeln und dem Versionsverlauf in `src/glide/README.md` an und pflegt den Versionsverlauf im selben Commit.
- Verhalten der Funktionen: `docs/20_FUNKTIONEN.md`
- QA: `docs/05_QA_TESTPLAN.md`, geprüfter Stand und was ungeprüft blieb: `docs/07_QA_BERICHT.md`
- Übergreifender Dokumentabgleich: [Pflegematrix](docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge). Für jede Änderung führende Quelle und betroffene Folgeaspekte prüfen; Architektur-Istzustand, Systembestand und [Shell-Zielbild](docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) getrennt pflegen.
- Daten und Backups: `docs/06_DATA_BACKUP_MIGRATION.md`
- Release, Lizenz, Signierung, Store: `docs/10_VEROEFFENTLICHUNG.md`
- Aktuelle Version: `VERSION` und die dazu passende Konstante in `src/glide/app.pyw`
- Produkt- und Plattformidentitäten: `docs/decisions/PRODUCT_IDENTITY.md`
- Wann Gruppe, wann Ordner, wann Zwischenüberschrift: `docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md`
- Betriebszustände und Grenzen der Erinnerungszustellung: `docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md`
- Pflegewerkzeuge für Versionswechsel, Abgleich nach `07_Python-Versionen` und Kürzen der Ablage: `scripts/pflege/`

D58 (02.11.2026): 3.50.0 heißt „Erster öffentlicher Stand“ (intern „öffentliche erste Beta“); Commit und Push für den Abschluss sind autorisiert. Screenreader-Abnahme bis Bedarf zurückgestellt, menschliche Prüfung nach dem technischen Abschluss. Aktuelle Statusachsen in Plan §21.43 und im Betanachweis.

D74 (08.11.2026) ersetzt diese Bezeichnungen für aktive Produkttexte. Die historische D58-Entscheidung und ihre Prüfnachweise bleiben erhalten. Für neue Projekte das Glide-System samt Übernahmevertrag verwenden; Steps wurde noch nicht angelegt. Historische QA im laufenden Audit nicht kürzen; konkret geschützten Bestand und Bewahrungsnachtrag beachten.

## Entwicklungsregeln

1. Vor Produktionsänderungen eine passende bestehende Baselineprüfung ausführen und Nutzerdatenpfade prüfen. Dokumentations-/Prüfwerkzeugnachläufe nach `docs/ARBEITSRICHTUNG.md` behandeln; unveränderte App-Version erhalten.
2. Bestehende Funktionen, Nutzerdaten und Migrationen bewahren.
3. Datenformatänderungen nur mit eigener Migration, Sicherung und Tests vornehmen. Eine neue Listen- oder Ordnerart ist eine Datenformatänderung und hebt `DATA_SCHEMA_VERSION` – nur so öffnet eine ältere Fassung den Bestand schreibgeschützt, statt ihn zu überschreiben (29.09.2026).
4. Keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung einführen.
5. Tests dürfen niemals den echten Nutzerdatenordner verwenden. Die Isolierung läuft über die Umgebungsvariable `GLIDE_DATA_DIR`; `%APPDATA%` allein wirkt nur unter Windows und würde unter macOS und Linux die echten Daten treffen.
6. Änderungen in `CHANGELOG.md` und den nach der [Pflegematrix](docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) betroffenen Fachquellen festhalten. Einstiege verlinken die Quelle; vollständige Bestands-/Statuslisten nicht duplizieren.
7. Signing-Secrets, Zertifikate, Schlüssel, Tokens und Recovery-Codes niemals einchecken.
8. Änderungen an Punkten laufen durch `item_change`, an Listen und Ordnern durch `sidebar_change`; Umbauaktionen zusätzlich unter `guarded_structural_change`. Modale Dialoge ausschließlich über `run_modal`.
9. Oberflächensymbole ausschließlich als Textzeichen aus der Tabelle `ICONS`. Der Integrationstest erzwingt das. Einzige Ausnahme ist das Logo als Bild aus `resources/logo` (`logo.py`, seit 29.09.2026).
10. Aktuelle Dokumente an ihrer verbindlichen Quelle fortschreiben: ein Thema, ein Dokument. Seit dem Auftrag vom 03.10.2026 werden doppelte und überholte Dokumente zusammengeführt und gelöscht statt archiviert oder mit `_Z` markiert; Git trägt die Historie. Neue Funktionen bekommen einen Abschnitt in `docs/20_FUNKTIONEN.md`, keine eigene Vertragsdatei. Archive und Nachweise nur der sieben neuesten Versionen (`scripts/pflege/ablage_kuerzen.py`). Siehe `docs/DOKUMENTENPFLEGE.md`.

11. Aufgabenstatus, nächste Schritte, Entscheidungen und Prüfgrenzen nach der zentralen [Abgleichregel](docs/DOKUMENTENPFLEGE.md#abgleich-ohne-doppelte-pflege) verfolgen. Der Entwicklungsplan führt Aufgaben, die Arbeitsrichtung Entscheidungen, der QA-Bericht Prüfstände; die Übergabe verweist darauf. Aktuelle Versionszeilen allein reichen nicht.
12. Caches nach stabilen IDs und Host-Lebensdauer führen, vollständig invalidieren; Undo kann Objekte ersetzen. Ersetzte Bindungen/after-Aufträge freigeben. Keine verschachtelten `update()`/`update_idletasks()` in selbstauslösenden Rückrufen. Details und Abnahme in `docs/ARBEITSRICHTUNG.md`.

13. Nach D17 entsteht neue oder angefasste Fachlogik als Tk-freies Modul mit eigenen Unit-Tests; bestehende UI- und Mutationseinstiege bleiben erhalten. Seit D09 ist die Git-Arbeitskopie des gesamten Projektordners maßgeblich.

14. Jede Entwicklungsrunde führt den vorhandenen `Glide_Entwicklungsplan.md` fort (aktueller Roadmap-Abgleich §21): Entscheidung/Auftrag und Implementierung/Prüfung/Lieferung/Menschenabnahme trennen, Restumfang und passende Belege nennen. Vor UI-Arbeit betroffene Designkontexte/Rollen festlegen, nachher echte Bedien-/Geometrie-/Sichtbelege bzw. offene native Grenzen dokumentieren. Neue Integrationsoptionen bleiben bis zur konkreten Auswahl Vorschläge; kein Hintergrundjob entscheidet Features oder pusht eigenständig.

## Prüfphasen

D51 bündelt mehrere zusammenhängende Pakete in einer Phase: gezielte Unit-/Bereichsprüfungen während der Arbeit, Versionswechsel, eingefrorene Vollprüfung, native Matrix und Lieferung am Phasenende. Die vorgeschlagenen Phasen und E-P1–E-P5 sind noch nicht als Gesamtumfang bestätigt; D17/D42/D43 und Datenformat-Tore gelten weiter.

## Abschlusskriterium

Eine Änderung ist erst fertig, wenn Syntaxprüfung und passende automatisierte Tests grün sind, die Versionsangaben konsistent sind und verbleibende manuelle Prüfungen ausdrücklich genannt werden. Für den Inhaber ist sie erst angekommen, wenn `07_Python-Versionen` und die eigenständigen Windows-/Mac-Pakete einschließlich `build/macos/Glide.app` den geprüften Stand tragen (SHA-256 und native Bau-/Start-/Signaturnachweise). Python-Abgleich: `scripts/pflege/abgleich_07.py`; eigenständige Pakete: `packaging/paket/baue_paket.py`, für Mac auch `packaging/paket/baue_und_pruefe_macos.sh` bzw. der native GitHub-Workflow. `packaging/macos/baue_app.py` erzeugt ausschließlich eine Vorstufe mit externem Python: eigenes Ziel wie `build/macos-vorstufe`, niemals damit ein eigenständiges Paket unter `build/macos` überschreiben. Auf Windows bleiben Mac-NT-Linkziele eine Inspektionskopie; native Weitergabe über das unveränderte geprüfte TAR.
