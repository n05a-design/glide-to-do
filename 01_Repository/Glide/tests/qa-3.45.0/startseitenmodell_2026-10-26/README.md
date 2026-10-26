# Startseitenmodell und gemeinsame Bestandsauswertung

Fortsetzungsauftrag 26.10.2026: „Weiterarbeiten an Glide. Feature Umsetzung“.

## Bestand vor Produktionsänderungen

- Quelle: `codex/glide-3.45.0`, HEAD `4f101cd`; Version 3.45.0, Aufgabenformat 26. Verweisvorschau und Tagesvorschlag bereits enthalten.
- Verbindliche Quellen gelesen: Übergabe, Entwicklungsplan §21, Arbeitsrichtung D55/D56 und Roadmapauftrag 21.10., Markt/Vorbilder §10–12, Funktionen §7 und Design Richtlinien.
- Nächster bereits vorgesehener Schnitt: WA-39/WA-32 Startseitenpilot mit gemessener WA-36-Bestandsauswertung. Gleiche Kacheln, IDs und Aktionen; keine neue Produktoption.
- Unversionierte Windows-Screenshots und `13_TK-Test-Umgebung` bleiben unangetastet. Kein Commit/Push, Versionswechsel oder Lieferabgleich in dieser Runde. `07_Python-Versionen` bleibt der gesondert dokumentierte Lieferstand.
- Sämtliche App-Prüfungen setzen vor Import `GLIDE_DATA_DIR` auf einen temporären Ordner. Echte Nutzerdaten werden nicht gelesen oder geschrieben.

## Zuschnitt und Abnahme

Tk-freies Startseitenmodell: Zählung, nächster Schritt, nächster Termin, Wochenzahlen und Labels gemeinsam in einem Bestandsdurchlauf. Kompatible ListApp-Einstiege liefern außerhalb des synchronen Renderns frische Werte. Ein Renderkontext endet auch bei Fehlern; kein dauerhafter Objektcache über Undo oder Import.

Betroffene Designkontexte: bestehende Startseitenkarten mit Kontextkopf, Aktionszeilen, Meldungen und Vorschauen; B01/B02/B04/B15, D12 und vorhandene Kartenrollen bleiben verbindlich. Keine Änderung an Typografie, Raster oder sichtbaren Texten vorgesehen.

Gezielte Fach-, Startseiten-/Retention- und Lebensdauerprüfungen sowie Vorher-/Nachhermessung mit identischen künstlichen Beständen. [Maschinenlesbarer Abschluss](ergebnis.json); keine neue Voll-/Native-/Releasefreigabe aus diesem Paket.

## Ergebnis und geprüfter Stand

Implementiert im lokalen Quellkandidaten 3.45.0 / Format 26: App `4244e610…`, neues Modell `ced120a5…`. [Vollständige Hashes](quellstand.json). 86 eigene Laufzeitdateien plus separater Zeichenprototyp; `ListApp` 49.884 Zeilen und 1.742 direkte Methoden. Neue Fachlogik hat keine Tk-Abhängigkeit; das Modell umfasst 217 Zeilen. Kopier-/Mac-Bauwerkzeuge kennen das neue Modul, wurden aber nicht zum Liefern ausgeführt.

- **25 Fachtests grün:** zwölf neue Modelltests plus 13 vorhandene Kacheltests. Alle 31 nichtleeren Projektionskombinationen werden gegen das Gesamtmodell geprüft; weitere Grenzen: Strukturkinder, erledigt/offen, stabile Gleichstände, Schaltjahr/Datumsparameter, Labelreihenfolge, unbekannte Labels, Originalreferenzen und Callbackfehler.
- **Erweiterte Startseitensuite grün:** gleiche Standardkacheln und Aktionen, Einstellungen/Neustart, Designwechsel, genau ein Modellaufbau für die fünf Bestandsprojektionen, Archivvorfahren, echte Erledigen-/Undo-Aktion, ersetzte Objekte mit gleicher ID und Bereinigung nach Renderabbruch.
- **B01/B02/B04 grün:** [Scrolllage und Gelesen](b01.json), [Rasterkante bei drei Größen](b02.json), [sechs Galerie-Vorschauen und Detailöffnung](b04.json). Keine neue sichtbare Gestaltung.
- **Syntax und Diff grün.** Die [Paketprüfung](pruefung.json) enthält außerdem den ersten roten Standabgleich: Das neue Modul fehlte in zwei Dokumentaufzählungen. Beide sind ergänzt; [abschließender Standabgleich](stand_abschluss.json) ist grün, 89 aktive Dokumente geprüft. Dieser Dokumentnachlauf verändert keinen ausführbaren Pfad.

Der erste lokale Integrationsvorlauf verwendete nach Undo fälschlich `lists[0]` als Quellliste; Undo fügt den Eingang ein. Der Test wählt nun die stabile Quell-ID. Der grüne Lauf prüft den echten Undo-Weg. Keine Appkorrektur aus diesem Fixturefehler.

## Leistung und Grenzen

Windows, Python 3.14.7, Tk 9.0.4; gleiche künstliche Bestände mit zehn Listen, sechs sichtbaren Kacheln, Datum/Fälligkeit/Planung und Erledigtanteil. Gemessen: erzwungener warmer Kachelrefresh einschließlich Tk-Ereignisnachlauf. Ein erster Aufbau getrennt, danach sieben Wiederholungen; p95 als Rangquantil bei dieser kleinen Stichprobe. Rohwerte: [vorher](leistung_vorher.json), [nachher](leistung_nachher.json).

| Aufgaben | Median vorher | Median nachher | p95 vorher | p95 nachher |
|---|---:|---:|---:|---:|
| 100 | 5,03 ms | 5,05 ms | 5,58 ms | 5,62 ms |
| 1.000 | 8,31 ms | 8,01 ms | 8,91 ms | 8,70 ms |
| 5.000 | 23,30 ms | 19,48 ms | 24,53 ms | 20,99 ms |
| 10.000 | 43,30 ms | 33,92 ms | 45,21 ms | 37,35 ms |

Die erste Modellfassung verschlechterte frische Einzelabfragen ([Zwischenstand](leistung_zwischenstand.json)). Spezialisierte Einzelkollektoren vermeiden diese zusätzliche Mehrfachprojektion. Die [gepaarte Gegenprobe](leistung_gepaart.json) bindet die sechs unveränderten Methoden aus Git `4f101cd` abwechselnd an dieselbe echte App mit denselben Objekten; ein Aufwärmpaar und acht Messpaare, Reihenfolge wechselnd, Patchen außerhalb der Messzeit. Bei 10.000 Aufgaben: fünf frische Einzelabfragen zusammen 33,98 → 32,23 ms; ganzer Refresh Median 61,29 → 54,61 ms. Die langsamere/gepaart stärker streuende Reihe bleibt erhalten: Refresh-p95 176,72 → 350,11 ms. Das bestätigt einen Medianvorteil unter diesen Bedingungen, keinen verlässlichen p95-Gewinn. Fensterverwaltung, Tk-Ereignisse und andere Systemlast sind nicht vollständig isoliert. Keine allgemeine Plattform-/Tempoabnahme.

## Lieferung und Fortsetzung

`07_Python-Versionen` bleibt unverändert bei App `2e69d875…`; vier Laufzeitunterschiede einschließlich des neuen Moduls, dazu die bereits enthaltenen WA-12-/Verweisvorschauänderungen. Gemeinsamer Voll-/Lieferabschluss nach D51, kein neuer Commit/Push/Merge. Native Mac-/Reader-/DPI-/Mehrmonitor- und Menschenabnahme bleiben offen. Appweite Presenter-/Designübertragung sowie weitere gemessene Refreshkosten sind weitere Schnitte; das Startseitenmodell schließt WA-39/WA-32 nicht insgesamt ab.
