# Glide – lokale Aufgaben, Notizen und Pinnwände

Glide ist eine deutschsprachige Desktop-Anwendung für persönliche Aufgaben,
Listen, Notizen, Tagebücher und visuelle Pinnwände. Die Anwendung läuft lokal
mit Python und Tk, benötigt weder Konto noch Cloudservice und hält Nutzerdaten
außerhalb des Programmordners.

> **Projektstatus:** interner Entwicklungsstand **3.30.0** · Datenformat 20 ·
> keine veröffentlichte oder signierte Releasefassung. Der aktuelle
> [QA-Bericht](docs/07_QA_BERICHT.md) nennt bestandene Prüfungen und offene
> Plattformtests.

## Was Glide bereits kann

- verschachtelte Listen und normale oder datumsorientierte Tagebuchordner; das
  Tagebuch nimmt Notizen, Listen, Zeichnungen und Pinnwände auf und filtert
  nach Tag oder Zeitraum;
- eine Pixel-Werkstatt direkt in der Seitenansicht:
  - Flächen mit 16, 32, 64 oder 128 Zellen;
  - Pinsel, Füllen, Pipette, Linie, Rechteck, Ellipse und Auswahl;
  - zwei Farben, Symmetrie, Muster, Paletten und Rückgängig je Aktion;
  - PNG-Export, PNG-Referenz und Nachzeichnung;
  - JSON- und Glide-SVG-Austausch;
  - Pixelsymbole für Listen und Ordner;
- Aufgaben, Long-Tasks, Gruppen, Überschriften, Unterpunkte und Notizseiten;
- Fälligkeiten, Wiederholungen, Erinnerungen, Prioritäten, Labels, Farben,
  Beschreibungen und lokale Anhänge;
- „Mein Tag“, Tagesplanung, Kapazität, Bearbeitungstag und Aufwandsschätzung;
- Listen-, Tabellen-, Kalender-, Karten- und Pinnwandansichten auf demselben
  Datenbestand – Gruppieren nach Feld, Spaltenboard mit Ziehen, Bereiche,
  beschriftete Verbindungen und Präsentation;
- verknüpfte Punkte, Abhängigkeiten, Zeiterfassung, Tagesbeginn und
  Wochenrückblick, Archiv statt Löschen;
- eine Startseite zum direkten Anpassen, angeheftete Seiten und Filter sowie
  eine Seiten- und Befehlssuche mit Strg/Cmd+O;
- Suche, gespeicherte Filter, Schnellerfassung, Mehrfachauswahl, Rückgängig und
  Papierkorb;
- Vorlagen, CSV-, TXT-, Markdown-, ICS- und Glide-Austausch sowie lokale
  Voll- und Teilbackups;
- zehn Designs (darunter „Pixel“), Hell-/Dunkelmodus, Akzentfarben und drei
  Schriftgrößen, alle mit lesbarem Kontrast nach WCAG AA;
- ein Stundenraster in „Mein Tag“ und ein Detailbereich neben der Liste;
- eine saubere Darstellung bis zur Mindestgröße 860 × 700;
- je Design fünf moderne Hintergrundverläufe (Mesh, Nordlicht, Körnung,
  Pixel), im Glasdesign mit Liquid-Glass-Tönung.

Die Einführung einzelner Funktionen ist in den
[fortgeltenden Funktionsverträgen](docs/00_INDEX.md) dokumentiert.

## Schnellstart aus dem Quellstand

Voraussetzung ist eine Python-Installation mit Tk/Tcl. Zusätzliche
Laufzeitpakete werden derzeit nicht benötigt.

```bash
python3 src/glide/app.pyw
```

Unter Windows lautet der Aufruf üblicherweise:

```powershell
python src\glide\app.pyw
```

Die mitgelieferten Schriften und Vorlagen unter `src/glide/resources` müssen
neben der Anwendung erhalten bleiben. Ein Installer ist noch nicht Bestandteil
dieses Repository-Stands.

Unter macOS lässt sich ein Entwicklungsbundle „Glide.app“ bauen. Es nutzt das
installierte Python und ist nicht zur Weitergabe gedacht:

```bash
python3 packaging/macos/baue_app.py --ziel build/macos
```

## Daten, Datenschutz und Sicherungen

Glide arbeitet ohne eigenen Netzwerkzugriff. Nutzerdaten und Anhänge werden in
einem lokalen Datenordner gespeichert. Der genaue Pfad hängt vom Betriebssystem
oder einer bewusst gewählten Ablage ab. Vollständige Backups verwenden das
Format `.glidebackup`; ein Komplettimport erzeugt vor dem Ersetzen des Bestands
ein Rückfallbackup.

Vor Tests muss `GLIDE_DATA_DIR` auf ein temporäres Verzeichnis zeigen. So
bleiben persönliche Daten vom Prüfbestand getrennt. Details stehen im
[Daten-, Backup- und Migrationsvertrag](docs/06_DATA_BACKUP_MIGRATION.md) und
in den [Sicherheitshinweisen](SECURITY.md).

## Zeichnungsseiten

Seit 3.29.0 ist die Zeichnung eine eigene Listenart im Glide-Bestand
(Datenformat 19); 3.30 erweitert sie zur Pixel-Werkstatt
([Vertrag 3.30](docs/66_MODERNISIERUNG_3.30.0.md)). Die Fläche liegt eingebettet in der Seitenanzeige, speichert
automatisch und reist mit Duplizieren, Papierkorb, Backups, Vorlagen und
Austausch. Bedienung, Datenvertrag und offene Punkte:
[Zeichnungsseite 3.29](docs/65_ZEICHNUNGSSEITE_3.29.0.md). Die isolierte
Bedienprobe bleibt für Experimente erhalten:

```bash
python3 src/glide/drawing_prototype.pyw
```

## Entwicklung und Prüfung

Der Anwendungskern liegt in `src/glide/app.pyw`; der Zeichenkern in
`src/glide/drawing.py` und `src/glide/drawing_image.py`. Tests arbeiten mit isolierten
Datenordnern. Der vollständige Prüflauf wird aus dem Repository-Stamm gestartet:

```bash
python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.30.0/lokaler_lauf --timeout 900
```

Eine schnelle Prüfung von Versions- und Dokumentationsständen:

```bash
python3 tests/tools/standpruefung.py
```

Ein nicht vollständig grüner Lauf darf nicht als Releasefreigabe ausgelegt
werden. Umfang, Plattformgrenzen und bekannte Blockaden stehen im
[Testplan](docs/05_QA_TESTPLAN.md) und im [QA-Bericht](docs/07_QA_BERICHT.md).

## Repository-Struktur

| Pfad | Inhalt |
|---|---|
| `src/glide/` | Anwendung, Zeichenflächenprobe und Laufzeitressourcen |
| `tests/` | Integrationsprüfungen, Fixtures, Werkzeuge und QA-Nachweise |
| `docs/` | Architektur, Produktverträge, Entscheidungen und Übergaben |
| `packaging/` | Bauskripte: macOS-Entwicklungsbundle, Windows-Startmenü-Verknüpfung; Voraussetzungen für Release-Pakete |
| `assets/` | reservierter Ort für freigegebene Branding-Master (noch leer; Logo-Quelle siehe `20_Grafik_Master`) |
| `requirements/` | Laufzeit-, Entwicklungs- und Build-Abhängigkeiten |

## Dokumentation

- [Dokumentationsindex](docs/00_INDEX.md)
- [Produktgrenzen](docs/01_PRODUCT_CONSTRAINTS.md)
- [Architektur](docs/02_ARCHITECTURE.md)
- [Projektübergabe](docs/09_PROJECT_HANDOFF.md)
- [Releasecheckliste](docs/10_RELEASE_CHECKLIST.md)
- [Modernisierung 3.30](docs/66_MODERNISIERUNG_3.30.0.md)
- [QA-Bericht](docs/07_QA_BERICHT.md)
- [Sitzungsprotokoll 24.–26.09.2026](docs/67_SITZUNGSPROTOKOLL_2026-09-24_BIS_2026-09-26.md)
- [Änderungsverlauf](CHANGELOG.md)

Historische Unterlagen liegen in `archiv/`-Ordnern. Sie belegen frühere
Entscheidungen und Prüfläufe, bilden aber keinen aktuellen Funktionsstand ab.

## Mitwirken und Weitergabe

Vor Änderungen gelten die Regeln in [AGENTS.md](AGENTS.md). Änderungen müssen
zum bestehenden Datenmodell passen, Nutzerdaten schützen und mit den jeweils
betroffenen Tests sowie der Dokumentation abgeschlossen werden.

Für Glide ist noch keine öffentliche Softwarelizenz festgelegt. Der vorhandene
Quelltext räumt deshalb derzeit keine allgemeinen Nutzungs-, Änderungs- oder
Weiterverteilungsrechte ein. Maßgeblich ist der [Lizenzstatus](LICENSE.md).
