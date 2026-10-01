# Prüfprotokoll Abnahme – Glide 3.23.0

Stand: 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Einstellungen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner
`00_Arbeitsvorbereitung` der Arbeitsablage.

**Eine Kopie je Durchgang.** Dateiname:
`Protokoll_Abnahme_3.23.0_<Durchgang>_<JJJJ-MM-TT>.md`, abgelegt unter
`Checklisten/Protokolle/`. Die Kennungen entsprechen der
[Abnahme am Gerät](Checklisten/Abnahme_Windows_macOS_3.23.0.md); dort steht,
was jeder Schritt tut und was erwartet wird. Hier steht nur, was tatsächlich
geschah.

**Ergebniswerte:** `ok` · `abw` (Abweichung, Befund unten eintragen) ·
`n/a` (gilt für diesen Durchgang nicht) · `ns` (nicht geprüft, mit Grund).
Leere Zellen gelten als nicht geprüft und machen das Protokoll unvollständig.

---

## Umgebung

| Angabe | Wert |
| --- | --- |
| Durchgang | P… |
| Datum und Uhrzeit | |
| Prüfende Person | |
| Betriebssystem und Aufbaunummer | |
| Python-Fassung | |
| Tk-Fassung | |
| Gerät (Modell, Prozessor, Arbeitsspeicher) | |
| Bildschirm 1: Auflösung, Skalierung, Pixeldichte | |
| Bildschirm 2: Auflösung, Skalierung, Pixeldichte | |
| Eingabegeräte | |
| Systemzeitzone | |
| Systemsprache und Regionsformat | |
| Geprüfte Fassung: Datei und SHA-256 | |
| `GLIDE_DATA_DIR` dieses Durchgangs | |
| Ausgangsbestand (Datei, Punktzahl) | |

## Vorbedingungen

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| V1 Vollprüflauf, Exitcode | | Protokollpfad: |
| V2 SHA-256-Abgleich | | |
| V3 Isolierte Ablage | | |
| V4 Prüfbestände eingespielt | | |
| V5 3.22-Ausgangszustand vorbereitet | | |
| V6 Umgebungskopf ausgefüllt | | |

**V1 und V2 müssen `ok` sein, bevor ein Block beginnt.**

---

## Block A · Start, Ablage und Migration

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| A1 | | Angelegter Pfad: |
| A2 | | |
| A3 | | |
| A4 | | |
| A5 | | Ausgangszustand → ermitteltes Design: |
| A6 | | |
| A7 | | |
| A8 | | Verwendeter Dienst: |
| A9 | | |
| A10 | | |

## Block B · Erscheinung am Gerät

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| B1 | | |
| B2 | | Nativer Backdrop verfügbar: ja / nein |
| B3 | | |
| B4 | | Gemessene Glyphenfamilien: |
| B5 | | |
| B6 | | |

Zusätzlich die sieben Designs nach
[Manuelle Prüfung, Abschnitt 2](Checklisten/Manuelle_Pruefung_3.23.0.md):

| Design | Ansichten geprüft | Hover Tabellenkopf | Auswahl lesbar | Bemerkung |
| --- | --- | --- | --- | --- |
| Hell | | | | |
| Dunkel | | | | |
| Liquid Glass · hell | | | | |
| Liquid Glass · dunkel | | | | |
| Dopamin | | | | |
| Kontrast hell | | | | |
| Kontrast dunkel | | | | |

## Block C · Skalierung, Auflösung und mehrere Monitore

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| C1 100 % | | |
| C1 125 % | | |
| C1 150 % | | |
| C1 200 % | | |
| C2 | | |
| C3 | | |
| C4 | | Stufenwechsel beobachtet bei (Fensterbreite): |
| C5 | | |
| C6 | | |
| C7 | | |
| C8 | | |

## Block D · Fensterzustände und Dichte

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| D1 | | |
| D2 | | |
| D3 | | |
| D4 | | Beobachtete Schwellen: voll ab … · kompakt ab … · Aktionsreihe ab … |
| D5 | | |
| D6 | | |

## Block E · Eingabegeräte und Tastenkürzel

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| E1 | | Kollidierende Kürzel: |
| E2 | | F11 direkt / mit fn / gar nicht · „Fläche“ funktioniert: |
| E3 | | |
| E4 | | |
| E5 | | |
| E6 | | |
| E7 | | |
| E8 | | |
| E9 | | |

## Block F · Pinnwand am Gerät

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| F1 | | Verhalten an der Grenze: |
| F2 | | |
| F3 | | |
| F4 | | |
| F5 | | |

Zusätzlich [Manuelle Prüfung, Abschnitt 4](Checklisten/Manuelle_Pruefung_3.23.0.md)
vollständig: ☐

## Block G · Ausgaben an fremde Programme

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| G1 | | Tatsächlich gedruckt auf: |
| G2 | | |
| G3 | | Zweiter Browser: |
| G4 | | Verwendete Ersatzschrift: |
| G5 Apple Kalender | | |
| G5 Outlook | | |
| G5 Thunderbird | | |
| G5 zweiter Import | | Ersetzen / Überspringen / Kopie: |
| G6 | | |
| G7 | | |
| G8 | | |

## Block H · Fremde Dateien einlesen

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| H1 | | |
| H2 | | |
| H3 Apple Kalender | | |
| H3 Outlook | | |
| H3 Webkalender | | Quelle: |
| H4 | | Übersprungene Termine beim zweiten Import: |
| H5 | | Geprüfte Zonen: |
| H6 | | |
| H7 | | |
| H8 | | |
| H9 | | |

## Block I · Backup und Wiederherstellung

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| I1 | | |
| I2 | | Vorschauwerte gegen Bestand: |
| I3 | | |
| I4 | | |
| I5 | | Richtung: Windows → macOS / macOS → Windows |
| I6 | | |

## Block J · Benachrichtigungen, Ruhezustand, Dauerbetrieb

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| J1 | | |
| J2 | | |
| J3 | | Dauer des Ruhezustands: |
| J4 | | |
| J5 | | |
| J6 | | Exitcode, Protokollpfad: |
| J7 | | Laufzeit, Speicher zu Beginn und am Ende: |
| J8 | | |

## Block K · Barrierefreiheit

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| K1 | | Fassung des Hilfsmittels: |
| K2 | | Fassung des Hilfsmittels: |
| K3 | | Stellen ohne Tastaturzugang: |
| K4 | | |
| K5 | | |
| K6 | | |

## Block L · Leistung am Gerät

| Nr. | Ergebnis | Messwert |
| --- | --- | --- |
| L1 | | Protokollpfad: |
| L2 | | Bestandsgröße … Punkte · Ansichtswechsel … ms |
| L3 | | |
| L4 | | Start bis bedienbar: … s / … s / … s |
| L5 | | |

## Block M · Regression

| Nr. | Ergebnis | Bemerkung |
| --- | --- | --- |
| M1 | | |
| M2 | | |
| M3 | | |
| M4 | | |
| M5 | | |
| M6 | | |
| M7 | | |
| M8 | | |
| M9 | | |
| M10 | | |

## Screenshots

| Ansicht | Design | Datei | Angesehen |
| --- | --- | --- | --- |
| | | | |

Erzeugungsweg und Werkzeugfassung: …

---

## Befunde

Je Befund ein Block. Kennung aus der Prüfliste, Klasse nach Abschnitt 3 der
[Abnahme am Gerät](Checklisten/Abnahme_Windows_macOS_3.23.0.md).

### B-01

| Feld | Inhalt |
| --- | --- |
| Kennung | |
| Klasse | S1 / S2 / S3 / S4 |
| Durchgang | |
| Handlung (nachstellbar, Schritt für Schritt) | |
| Erwartet | |
| Tatsächlich | |
| Reproduzierbarkeit | immer / gelegentlich / einmalig |
| Bestand verändert | ja / nein |
| Screenshot | |
| Vermutete Stelle im Code | |
| Entscheidung | behoben in … / bleibt Plattformgrenze / zurückgestellt |

### B-02

| Feld | Inhalt |
| --- | --- |
| Kennung | |
| Klasse | |
| Durchgang | |
| Handlung | |
| Erwartet | |
| Tatsächlich | |
| Reproduzierbarkeit | |
| Bestand verändert | |
| Screenshot | |
| Vermutete Stelle im Code | |
| Entscheidung | |

---

## Abschluss dieses Durchgangs

| Angabe | Wert |
| --- | --- |
| Schritte insgesamt / geprüft / `ok` / `abw` / `n/a` / `ns` | |
| Befunde S1 | |
| Befunde S2 | |
| Befunde S3 | |
| Befunde S4 | |
| Durchgang abgebrochen | nein / ja, weil … |
| Dauer | |

**Aussage der prüfenden Person.** Genau eine Zeile ankreuzen:

- ☐ Dieser Durchgang ist ohne Befund der Klassen S1 und S2 bestanden.
- ☐ Bestanden mit Befunden, die vor einer Freigabe zu entscheiden sind – siehe oben.
- ☐ Nicht bestanden.

Unterschrift oder Namenszeichen, Datum: …

**Nach dem letzten Durchgang:** Ergebnis in
[QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md),
[Weitergabe](Glide_Weitergabe_neuer_Chat_2026-09-18.md) und
[Technische Fakten](Notizen/Technische_Fakten_3.23.0.md) derselben Version
eintragen; S1- und S2-Befunde nach
[Offene Entscheidungen](Entscheidungen/Offene_Entscheidungen_3.23.0.md)
überführen.
