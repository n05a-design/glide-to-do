# Regeln für die Dokumentenpflege

Stand 23.09.2026 · Glide 3.28.0 · Datenformat 18

Der aktuelle Nutzerauftrag ergänzt die Arbeitsregeln des Repositorys:

- Vor Änderungen an bestehenden Dokumenten eine Kopie im benachbarten `archiv/` anlegen, mit der beschriebenen vorherigen Version im Namen.
- Historische Versionsdokumente älter als aktuelle Version minus fünf nach `docs/archiv/` verschieben. Für 3.28 betrifft dies Versionen vor 3.23. Eine ausdrücklich im aktuellen Index als fortgeltender Funktionsvertrag geführte Datei bleibt aktiv, bis ein neuer kumulativer Vertrag sie ersetzt. Aktive Verweise werden auf den neuen Ort nachgeführt.
- Mehr als zehn Versionen alte historische Dokumente dürfen nur entfallen, wenn weder aktive Verweise noch weiterhin gültige Grundsatzinhalte vorhanden sind. Löschen ist optional; in dieser Nachbesserung bleiben Belege erhalten.
- Mindestens drei Versionen alte Prüfprotokolle gehören nach `50_Ablage/`. Originalergebnis, Datum und Exitcode bleiben unverändert.
- Für normale Änderungen zunächst die letzten drei Versionen lesen. Ältere Unterlagen bei konkretem Bedarf gezielt hinzunehmen.
- `PRODUCT_IDENTITY.md`, `ARBEITSBEGLEITER.md`, `09_PROJECT_HANDOFF.md`, `07_QA_BERICHT.md` und weiterhin gültige Entscheidungen werden nicht automatisch archiviert.
- Nutzeraufträge, historische Screenshots und abgeschlossene QA-Ergebnisse sind Belege. Sie werden nicht auf eine neue Versionsnummer umetikettiert.
- Neue Dokumente und Archive im Index aufnehmen. Stand- und Linkprüfung vor einer Freigabe ausführen.

Produktionskommentare erklären Invarianten, technische Gründe und Plattformbesonderheiten. Arbeitsauftragsnummern und Entwicklungserzählungen gehören in Changelog beziehungsweise Archiv. Eine reine Kommentarbereinigung muss den ausführbaren Syntaxbaum unverändert lassen.
