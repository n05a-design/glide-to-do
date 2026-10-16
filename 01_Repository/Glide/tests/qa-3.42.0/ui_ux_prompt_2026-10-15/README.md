# UI-/UX-Promptpaket – Dokumentationsnachlauf

Stand 15.10.2026 · Glide 3.42.0 · App- und Datenformat unverändert

Auftrag: wiederverwendbaren Prompt zu drei Fragen und 22 Änderungs-/Pflegepunkten formulieren, alle 28 Nutzerbilder lokal sichern und die UI-/UX-Vorgaben agentenunabhängig auffindbar machen. Keine App-Umsetzung, kein Versionswechsel, kein Commit/Push und keine Skillmigration.

Ergebnisquellen: [Ausführungsprompt](../../../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md), [Originalauftrag](../../../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/AUFTRAG.md), [Bildreferenzen](../../../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/BILDREFERENZEN.md), [Manifest](../../../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/screenshots.json) und [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md). Status im Entwicklungsplan §17; Einstieg über Arbeitsvorbereitungsindex, Übergabe und Dokumentationsindex.

## Prüfung

Ergebnis in [ergebnis.json](ergebnis.json). Alle 25 Anforderungs-IDs, die vollständige Originalnummerierung, 28 Bildzuordnungen, SHA-256 gegen die Originale, Git-Ausschluss der Bilder und die lokalen Dokumentationslinks sind geprüft. Die neuen, noch nicht versionierten Dokumente wurden unmittelbar mit der vorhandenen Stand-/Linkprüfung geprüft; die Git-basierte Grundstufe allein erfasst sie nicht vollständig. Eine unabhängige Inhaltsprüfung fand keine wesentlichen Auslassungen oder Widersprüche.

Die [CI-Grundstufe mit strengem Lieferabgleich](grundstufe/ergebnis.json) meldet **18 erfolgreiche Schritte und einen bestehenden Werkzeugtestfehler** (Gesamtexitcode 1). Syntax, Versionskonsistenz, Dokumentation, fünf Analysen, 638 Fachlogiktests und dieselben 638 Tests ohne Systemzeitzonen, Startprobe unter Windows/Python 3.14.7/Tk 9.0.4, Lieferstand, Fremdcode, Datenschutz, Ablage und Synchronisation bestanden. Die Startprobe wechselte durch sechs Ansichten ohne Callbackfehler.

**Bestehender Befund:** `test_git_inventory_respects_requested_subdirectory_and_staged_new_document` erwartet `README.md` vor `packaging/README.md`; unter Windows liefert die vorhandene Sortierung die umgekehrte Reihenfolge. Derselbe Fehler wurde separat mit unveränderten `standpruefung.py` und `test_standpruefung.py` aus Git HEAD reproduziert. 104 der 105 Werkzeugtests bestanden. Keine Reparatur des Prüfwerkzeugs im Auftrag zum Formulieren dieses Pakets; die Grundstufe wird ausdrücklich nicht als grün ausgegeben. Rohprotokoll der Gegenprobe lokal: `head_werkzeuggegenprobe.log`.

**Unveränderter Appstand:** 420 Laufzeit-/Ressourcen-/Lieferdateien einschließlich VERSION vor und nach der Runde per SHA-256 verglichen; keine Änderung. Apphash `d6709820b223293d6480e2fa15616cbf4257293d4cfb87422bc9782d409afa05`; Hauptdatei in `07_Python-Versionen` weiter bytegleich.

28 Originalbilder wurden bytegleich kopiert, mit stabilen IDs und relativen Pfaden erfasst. Keine Bildbearbeitung. Originale bleiben wegen sichtbarer Kontoangaben lokal und über `.gitignore` ausgeschlossen. Rohprotokolle der Prüfung bleiben lokal.

App-Sichtprüfung, Feature-Regressionen und Plattformabnahme des künftigen Pakets sind nicht Gegenstand dieser Vorbereitungsrunde. Die vorherige Release-QA bleibt ein Beleg für ihren damaligen Quellstand.
