# Drei Robustheitspakete für Glide 3.49.0

Stand 28.10.2026 · Quellkandidat 3.49.0 · Aufgabenformat 26

Umgesetzt: gemeinsamer abgesicherter Prüfablauf (WA-42), lokaler Wiederanlauf mit bewusster Freigabe/Originalvorsicherung (WA-40/WA-41B), begrenzte lokale Metadatendiagnose mit Prozessbegleitung (WA-41A/WA-40).

Der [Ausgangsstand](ausgangsstand.json) erfasst vorhandene lokale Änderungen und die grüne Baseline (29 Tests). Originale 3.48.0-Befunde und repeat_rules.py bleiben erhalten. Der [neue Gesamtbericht](bericht_abgleich.json) ist konsolidierte Hintergrundbewertung, kein neuer Audit/Testlauf; Einordnung in Analyse §13.19 und Plan §21.27.

## Prüfungen und Rückwege

Die finale maschinelle Bilanz steht in ergebnis.json; echte Bedien-, Restore- und Geometrieergebnisse in [wiederanlauf_final.json](wiederanlauf_final.json), vorhandene Speicherstatusregressionen in [speicherstatus.json](speicherstatus.json). Kernfälle umfassen harte eigene Prozessabbrüche, Originalschutz, neuere Formate, lebende Besitzer, Markerwechsel, Kopierfehler und Abwesenheitsbelege. Reviewkorrekturen betreffen die Sperrübernahme, den Ersatzimport aus geschütztem Fehlerstart, Altleserschutz und fehlgeschlagene Nachläufe. Kein Undo zum leeren Fehlerbild.

24 Konfigurationen prüfen Hell/Dunkel/Verlauf, mittlere/große Schrift, Hinweise an/aus und 860×700/1280×800. Speicherstatus tatsächlich bei 480×360 erreichbar; 72 Knopfprüfungen. Vier eigene künstliche PrintWindow-Aufnahmen lokal gesichtet: Statusdialoge lesbar, Fußaktionen frei. Die Hauptfensteraufnahme bildet native ttk-Flächen nur unvollständig ab und beweist deren visuelle Abnahme nicht. Bilder bleiben lokal.

## Grenzen

WA-41A/B weiterhin ungeklärt. Keine neue Intel-Stressserie, Hardwareänderung, Vollcodeaudit, breite eingefrorene Integrationsmatrix oder native Paketabnahme. Kein Commit/Push. Python/Showcase bleiben 3.47.0, native Pakete 3.45.0; keine öffentliche Releasefreigabe.

Die Versionspflege wurde ohne Ablagelöschung ausgeführt. Neun ältere Aufbewahrungskandidaten bleiben erhalten: Vorprüfung fand mindestens einen vom Git-Blob abweichenden Nachweis, deshalb keine Löschung. Ablageprüfung bleibt gegebenenfalls rot. Frühere rote Vorläufe bleiben historische Ergebnisse; finale Wiederholungen werden getrennt bewertet.

Gezielter Abschluss: 12/12 Wiederanlauf-/Restore-/Bedienfälle, 24 Layoutkonfigurationen und 72 Knopfprüfungen grün. Kern-/Diagnoseprüfungen sind zusätzlich Bestandteil der Fachtests der CI-Grundstufe. Die frühere Speicherstatusprüfung (4/4) lief vor dem abschließenden Restore-Nachlauf; sie wird nicht als neue Vollmatrix ausgegeben.

Normale Speicherprobe: 100 künstliche Aufgaben, ein Aufwärmlauf und neun Messungen mit aktiver Diagnose. Median ca.15,42 ms, Maximum ca.16,31 ms; kein Aufruf der vollständigen Wiederanlaufanalyse und keine erneute Diagnosedateischreibung für dieselbe Speicherphase. Kein Vorher-/Nachher-Vergleich und keine allgemeine Performancefreigabe. [Rohwerte](speicherweg.json).

## Abschließende CI-Bilanz

220 Werkzeugtests (ein Skip), zweimal1048 Fachtests, fünf Analysen, Syntax/Version/Fixtures/Fremdcode, Startprobe, Ablagegröße und Synchronisation bestanden. Der ursprüngliche CI-Lauf bleibt rot ausschließlich wegen absoluter Benutzerpfade in der bestehenden Übergabe. Diese wurden durch `%USERPROFILE%` ersetzt; gezielter [Datenschutznachlauf](dokumentnachlauf.json) grün, kein erneuter Gesamt-CI-Lauf. Der [Originalbefund](grundstufe/ergebnis.json) bleibt erhalten. Standprüfung nach Dokumentpflege grün. Keine globale Releasefreigabe.
