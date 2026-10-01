# Dokumentationsabgleich – 12.09.2026 (historischer Prüfstand)

Dieses Dokument ist ein abgeschlossener Nachweis und wird nicht nachgezogen. Der aktuelle Stand steht im [Dokumentationsindex](00_INDEX.md) und im [QA-Bericht](07_QA_BERICHT.md).

> **Historischer Nachtrag:** Dieses Protokoll beschreibt den Stand vor dem
> Erinnerungsausbau. Die unten als Zukunftsideen genannten Erinnerungen sind
> inzwischen in 3.8.0 umgesetzt, samt Hervorhebung in Taskleiste bzw. Dock.
> Maßgeblich sind [Erinnerungsvertrag](31_ERINNERUNGEN_3.8.0.md),
> [Reiter und Pinnwand](33_REITER_UND_PINNWAND_3.10.0.md),
> [Tabellenansicht](36_TABELLENANSICHT_3.13.0.md) und [QA-Bericht](07_QA_BERICHT.md).

## Ergebnis

Die aktuellen Funktions-, Versions-, Architektur-, Start- und Übergabedokumente
beschreiben jetzt den vollständigen Vorlageneditor, Mac-Auswahlfelder und die
dynamischen Kacheln. Überholte Mengen-/Formatangaben (12 statt 16 Vorlagen,
Vorlagenformat 1 statt 2), feste Windows-Benutzerpfade und alte globale
Prüffreigaben wurden korrigiert. Historische Windows-Bilder und Messungen gelten
weiterhin nur für ihren damaligen Quellstand. Der frühere Word-Bericht wird
nicht mehr als aktuelle Fassung geführt.

26 Vorgänger wurden vor der Bearbeitung unverändert lokal gesichert.
4 überholte Dokumente wurden aus aktiven Ebenen in lokale Archive verschoben:
drei technische Faktenblätter älterer Versionen und der Windows-Prüfstand vom
07.09.2026. Es wurde keine Datei endgültig gelöscht.

[Archivmanifest mit Quelle, Ziel und SHA-256](../tests/qa-3.7.0/dokumentationsabgleich-2026-09-12/archiv_manifest.json).

## Einordnung der Ablage

Aktuelle Einstiege stehen im [Index](00_INDEX.md). Archivdateien sind historische
Nachweise, keine parallel zu pflegenden Fassungen. Alte QA-Protokolle und
Migrations-Fixtures bleiben für Regressionen erhalten. Ressourcen, Beispieldaten,
Programmcode und reale Nutzerbackups wurden durch diesen Dokumentationsabgleich
nicht verändert. Die [frühere Ablageprüfung](28_ABLAGEPRUEFUNG_2026-09-11.md)
bleibt als datierter Prüfstand erhalten.

Die Chatweitergabe und das Produktdatenblatt verwiesen damals auf
den 3.13-macOS-Gesamtlauf. Erinnerungen, Reiter, Pinnwand und Tabellenansicht
sind umgesetzt; native Sichtprüfung und ein Windows-Lauf des jüngsten UI-Stands
bleiben offen.

## Prüfung

Der erfolgreiche App-Gesamtlauf wurde als Ausgangsnachweis übernommen;
Programmcode wurde nicht geändert. Dokumentationsindex, lokale Links,
Archiv-Prüfsummen und die Unverändertheit des geprüften Quellstands werden
im [Prüfprotokoll dieses Abgleichs](../tests/qa-3.7.0/dokumentationsabgleich-2026-09-12/pruefung.json) festgehalten.
