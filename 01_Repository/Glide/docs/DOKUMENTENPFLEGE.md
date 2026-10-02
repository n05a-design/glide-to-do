# Regeln für die Dokumentenpflege

Stand 02.10.2026 · Glide 3.33.6 · Datenformat 20

Der aktuelle Nutzerauftrag ergänzt die Arbeitsregeln des Repositorys:

- Aktuelle Dokumente an ihrer verbindlichen Quelle fortschreiben; Git trägt die Historie. Keine zusätzliche Markdown-Versionskopie bei jeder Änderung.
- Historische Versionsdokumente älter als aktuelle Version minus fünf nach `docs/archiv/` verschieben. Für 3.28 betrifft dies Versionen vor 3.23, für 3.30 Versionen vor 3.25; die im Index unter „Aktueller Einstieg“ geführten Verträge 45 bis 58 bleiben als fortgeltende Funktionsverträge aktiv. Eine ausdrücklich im aktuellen Index als fortgeltender Funktionsvertrag geführte Datei bleibt aktiv, bis ein neuer kumulativer Vertrag sie ersetzt. Aktive Verweise werden auf den neuen Ort nachgeführt.
- Seit dem ausdrücklichen Nutzerauftrag vom 01.10.2026 überholte und doppelte Dokumentationsdateien nach Wissensabgleich löschen. Diese Anweisung ersetzt „nichts selbst löschen“ und `_Z`-Vormerkungen. Alter allein genügt weiterhin nicht: gültige Verträge und einzigartige relevante Informationen erhalten bzw. an einer gepflegten Quelle zusammenfassen; Verweise nachführen, Pfad/Hash/Löschgrund/erhaltene Quelle dokumentieren. [Bereinigung und gemeinsamer Wissenseinstieg](75_DOKUMENTATIONSREDUKTION_UND_LOGOS_3.33.1.md).
- Mindestens drei Versionen alte Prüfprotokolle gehören nach `50_Ablage/`. Originalergebnis, Datum und Exitcode bleiben unverändert.
- Für normale Änderungen zunächst die letzten drei Versionen lesen. Ältere Unterlagen bei konkretem Bedarf gezielt hinzunehmen.
- `PRODUCT_IDENTITY.md`, `ARBEITSBEGLEITER.md`, `09_PROJECT_HANDOFF.md`, `07_QA_BERICHT.md` und weiterhin gültige Entscheidungen werden nicht automatisch archiviert.
- Nutzeraufträge, historische Screenshots und abgeschlossene QA-Ergebnisse sind Belege. Sie werden nicht auf eine neue Versionsnummer umetikettiert.
- Seit 02.10.2026 (Entscheidung des Inhabers) keine Archivkopien von Fixtures, Showcase und Beispieldaten: Vorfassungen trägt Git wie bei Dokumenten. Fensterbilder (`fenster/`) der Vollprüfung bleiben lokal; versioniert werden Ergebnis und README. Von älteren Läufen bleibt je Version nur die letzte Vollprüfung mit Bildern, Ergebnisse aller Läufe bleiben erhalten.
- Neue Dokumente und Archive im Index aufnehmen. Stand- und Linkprüfung vor einer Freigabe ausführen.

Produktionskommentare erklären Invarianten, technische Gründe und Plattformbesonderheiten. Arbeitsauftragsnummern und Entwicklungserzählungen gehören in Changelog beziehungsweise Archiv. Eine reine Kommentarbereinigung muss den ausführbaren Syntaxbaum unverändert lassen.

## Fortgeschriebene Einstiege trotz Datum im Namen

Sitzungsübergabe, Arbeits-/Featureplanung, Richtungsauswahl und beide aktiven Checklisten werden weiter gepflegt. Ihre Dateinamen bleiben für bestehende Verweise stabil; sie sind in `GEPFLEGT` der Standprüfung registriert und müssen die laufende Version nennen. Fortgeschriebene Titel dürfen keinen älteren Stand behaupten; der erste ausführbare Vollprüfungsaufruf verwendet die laufende Version oder `<Version>`. Historische Befehle und versionsbenannte Detailverträge bleiben als Belege erlaubt.

Versionstool und Standprüfung kontrollieren formale Angaben. Zusätzlich Aufgabenstatus, beantwortete Entscheidungen, nächste Schritte und tatsächliche Prüfgrenzen inhaltlich gegen Code und Ergebnisse abgleichen. Erledigte Teilpakete nicht als neue Aufgaben empfehlen. Erhaltene Archive im Index verlinken; entfernte Kopien nicht erneut anlegen. Reine Dokumentations-/Werkzeugnachläufe erhalten einen eigenen Nachweis; siehe [Arbeitsrichtung](ARBEITSRICHTUNG.md).

Datierte vollständige Ablageabbilder `Glide_<Version>_Zwischenstand_<Datum>` bleiben unveränderte Belege und werden von der aktiven Standprüfung getrennt. Ein während der Arbeit kopierter Zwischenstand ist keine abgeschlossene Lieferung; fehlende Abschlussnachweise werden dort nicht nachträglich erfunden. Kanonischer Einstieg bleibt die ursprüngliche Ablage mit `01_Repository/Glide`.

Die Suitezahl einer laufenden Standzeile wird direkt gegen `SUITEN` in `pruefen.py` geprüft (R14). Zahlen historischer Läufe bleiben unverändert; neue tatsächliche Prüfergebnisse und aktive Umfangsangaben sind davon zu unterscheiden.
