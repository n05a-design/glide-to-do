# Historische Python-Versionen

Dieser Ordner bewahrt nachvollziehbare Einzeldatei-Stände auf:

- `v2.4.1`: Ausgangsversion vor der aktuellen Quality-of-Life-Erweiterung.
- `v2.5.0`: begonnener, noch nicht vollständig stabilisierter Zwischenstand.
- `v2.5.1`: abgeschlossene Stabilisierung mit Ordnern, Eingang, Notizen, Anhängen und Backup-Härtung.
- `v2.5.2`: getrennter Eingang, Aufgaben-Kontextmenü, Aufgabenfarben und Windows-Dark-Start.
- `v2.5.3`: reparierte Rechtsklickaktionen, feste rechte Fälligkeitsspalte und Eingang in Überschriftenoptik.
- `v2.5.4`: stabile Einzüge und Einklappzustände, Ordnerübersicht-DnD, Beschreibungstexte, Anhangshärtung und die abgeleitete Ansicht „In Bearbeitung“.
- `v2.5.5`: einheitliche Feldabstände in allen Dialogen, reparierte Anhangsnamen und Backup-Import, robuste Kopfzeile und Fensterposition sowie macOS-Tastenkürzel inklusive Cmd+Q.
- `v2.6.0`: Gruppen innerhalb einer Liste, durchgängig ausgebaute Kontextmenüs auf allen Oberflächen, Titel im schwersten verfügbaren Schriftschnitt und Datenformat 6.
- `v2.7.0`: interner Teststand mit Papierkorb, Labels, Kalender, gemeinsamem Bearbeiten-Dialog, Mehrfachauswahl, automatischem Speichern und Datenformat 7.
- `v2.7.1`: Labels in der Listenfarbpalette und zusätzlich an Ordnern und Listen, Kalender mit Wochen- und Monatsansicht, Entf-Taste in der Seitenleiste und Verschieben per Alt+Pfeiltasten.
- `v2.7.2`: Tastaturfokus im Aufgabenbaum für die Pfeiltasten, graues Trennband in der Seitenleiste, Hover-Umrandung im Kalender und Aufgabe per Doppelklick auf einen Tag.
- `v2.8.0`: Long-Task und Zwischenüberschrift als neue Aufgabenarten, Systemzeile „Verspätet“, vollständiger Anlage-Dialog, hellblauer Hover, responsive Spalten und Datenformat 8. **Ohne Einzeldatei in diesem Ordner** – der Stand wurde nicht abgelegt, ist aber im Changelog und im Ausführungsplan vollständig dokumentiert und in `v2.9.0` enthalten.
- `v2.9.0`: verschachtelte Ordner mit Kreis- und Tiefenschutz, eigenes Detailfenster „Punktdetails (Long-Task)“ mit mehrzeiligem Titelfeld, Bildlaufleisten in allen Dialogfeldern und Datenformat 9.
- `v2.10.0`: Labels als Chips mit Zielhelligkeit statt festem Mischanteil, verlustfreier TXT-Rundlauf aller vier Arten, bereinigte Code-Basis, QA-Bericht. Datenformat bleibt 9. **Ohne Einzeldatei in diesem Ordner** – der Stand ist im Changelog und im Ausführungsplan vollständig dokumentiert und in `v2.11.0` enthalten.
- `v2.11.0`: Papierkorb auch für einzelne Punkte, Bestandswächter um jede Umbauaktion, Strg+Klick wieder als Mehrfachauswahl (macOS: Cmd), gemeinsame Eingabemaske für Anlegen und Bearbeiten mit Kalender und optionaler Uhrzeit, „Erweitert“ neben der Schnelleingabe und Datenformat 10.
- `v2.12.0`: Labelauswahl als Aufklappfeld mit Mehrfachauswahl, Fälligkeit mit Kalenderknopf statt eingebautem Monatskalender, Kopfbereich ohne Sprung beim Listenwechsel, Such- und Filterzeile über der Liste statt über die volle Breite (die Listenübersicht beginnt dadurch weiter oben), „Nur erledigte Punkte“ entfallen, vollständig lesbares Fälligkeitsdatum mit zweistelligem Jahr, ein Label je Zeile. Datenformat bleibt 10.

- `v3.0.0`: Dunkelblau statt Schwarz im Hellmodus, Listenübersicht ganz oben, Eingabe- und Suchzeile über der Liste, Umbenennen von Listen und Ordnern in der Ansicht, Symbole in Seitenleiste und Schaltflächen, eigenes Klappdreieck für Ordner, ein Label je Zeile mit Symbol, Bildlaufleiste nur bei Bedarf, Auswahlmenüs ohne Rahmen. Datenformat bleibt 10.

- `v3.0.1`: Dialoge öffnen auf dem richtigen Bildschirm, erweiterte Eingabe startet in voller Höhe, gleiche Ränder in den Fenstern, Gruppieren auf der obersten Menüebene, rundere Labelchips, Kopfzeile auf einer Flucht.

- `v3.0.2`: Punkte per Zug in eine Gruppe legen, leere Gruppe heißt „(leer)“, Labels direkt in der Eingabemaske anlegen, gemeinsame Griff-Rückgabe für alle Unterdialoge.

- `v3.1.0`: Aufräumversion ohne neue Bedienfunktion. Gemeinsamer Rahmen für jede Änderung (`item_change`, `sidebar_change`), gemeinsamer Weg für jeden modalen Dialog (`run_modal`), behobener Fehler im Rückgängig-Speicher: Eine wirkungslose Aktion kostete bei vollem Speicher den ältesten Schritt. Datenformat bleibt 10. **Ohne Einzeldatei in diesem Ordner** – der Stand ist im Changelog dokumentiert und in `v3.2.0` enthalten.

- `v3.2.0`: Automatische Übernahme von Nutzerdaten aus früheren Programmnamen entfernt, zentrale Textsymbole in ICONS (Anhang `⊕`, Fälligkeit `▦`); Emoji-Ausnahmen bleiben für Gruppenmarker, höchste Wichtigkeit und Beschreibungsmarker, umfangreicher Beispielbestand zum Einlesen unter `05_Probelisten_Testdaten`. Datenformat bleibt 10.

- `v3.3.0`: neue Ansicht „Labels“ in der Seitenleiste – der gesamte Bestand nach Labels gruppiert, Punkte in der Labelfarbe, ein Punkt mit mehreren Labels in jeder zugehörigen Gruppe, „Ohne Label“ als letzte Gruppe. Ziehen zwischen zwei Gruppen tauscht genau das Label der Herkunftsgruppe. Dazu Feinschliff in der Liste: Labelchips werden nicht mehr an den Kanten beschnitten, Fälligkeits- und Labelspalte folgen dem tatsächlichen Inhalt statt dem längstmöglichen Fall und sind links ausgerichtet, im schmalen Fenster weicht auch die Fälligkeit. Datenformat bleibt 10.

Der kanonische, getestete Source-Pfad für weitere Entwicklung ist `01_Repository/Glide/src/glide/app.pyw`. Die jeweils aktuelle Einzeldatei hier ist bytegleich und dient als leicht startbare Versionskopie; ältere Dateien werden nicht überschrieben.

- `v3.4.0`: persönliche Startseite und Einstellungen, Vorlagen, ausgerichtete Zähler, kompaktere Abstände, farbige Eingaben, feste Artlabels in der Eingabemaske sowie Hilfe und Meldungen im Theme. Die neue Einzeldatei ist bytegleich mit dem kanonischen Source. Datenformat bleibt 10.


- `v3.6.0`: Vorlagenseite, Teilbackups, wechselbarer Datenordner mit
  Sperrhinweis, Mondphase und Jahresanzeige bei Datenformat 11.
  Aktuelle startbare Datei: [Glide 3.6.0](Glide-Aufgaben-und-Listen_v3.6.0.pyw).
- `v3.5.0`: wiederkehrende Aufgaben und Datenformat 11. Die Datei bleibt als
  historischer Stand erhalten: [Glide 3.5.0](Glide-Aufgaben-und-Listen_v3.5.0.pyw).
  Windows-Vollprüfung am 05.09.2026 bestanden. Per SHA-256 bytegleich mit dem
  unveränderten kanonischen Quellcode; keine neue Version durch die Bereinigung.
  [Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).
