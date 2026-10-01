# Arbeitsvorbereitung

Persönlicher Vorbereitungsbereich für Entscheidungen, Research, Checklisten und
Notizen. Produktiver Sourcecode gehört ausschließlich nach
`01_Repository/Glide`; finale Binärartefakte ausschließlich nach
`30_Release_Exports/<Version>`. Projektbegleitende QA-Läufe und Zwischenstände
liegen unter `50_Ablage`. Archiviert wird dezentral: Jeder Ordner hat einen
eigenen Unterordner `Archiv/` für überholte Stände genau dieses Ordners.

## Aktueller Inhalt

- `Entscheidungen/Offene_Entscheidungen_2.11.0.md` – was noch entschieden werden
  muss, jeweils mit Empfehlung, plus die Liste dessen, was nicht mehr offen ist.
  **Stand 2.11.0; die Sachlage gilt weiter, die Versionsangaben darin nicht.**
- `Checklisten/Manuelle_Pruefung_3.2.0.md` – genau die Prüfungen, die die
  automatisierten Läufe **nicht** abdecken: Sicht, Eingabegeräte, Plattform,
  reale Daten. Abschnitt 3a hat Vorrang; der erste Block darin betrifft das
  gemeldete Einfrieren.
- `Checklisten/Manuelle_Pruefung_2.11.0.md` – Vorgängerfassung, gehört ins
  `Archiv`.
- `Checklisten/Glide_Veroeffentlichung_Checkliste.txt` – dieselben offenen
  Punkte als **importierbare Glide-Liste**. In Glide über „Liste importieren"
  laden; sie kommt als zusätzliche Liste dazu und ersetzt nichts.
- `Notizen/Technische_Fakten_3.2.0.md` – belegte Kennzahlen, Grenzen, Formate
  und Formulierungen für Texte und Formulare, samt der Liste dessen, was
  **nicht** belegbar ist.
- `Notizen/Technische_Fakten_2.11.0.md` – Vorgängerfassung, gehört ins `Archiv`.
- `Research/` – eigene Recherche, unverändert.
- `Archiv/` – überholte Fassungen dieser Dokumente.

## Wo der aktuelle Stand steht

Der laufend gepflegte Projektstand liegt im Repository, nicht hier:

| Frage | Datei |
|---|---|
| Was ist geprüft, was nicht? | `01_Repository/Glide/docs/07_QA_BERICHT.md` |
| Was fehlt bis zur Veröffentlichung? | `01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md` |
| Welche Werte sind belegt, welche offen? | `01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md` |
| Vollständige Übergabe an einen neuen Bearbeiter | `01_Repository/Glide/docs/09_PROJECT_HANDOFF.md` |

## Was seit 2.11.0 passiert ist

**2.12.0 bis 3.0.2** – Oberfläche: Labelauswahl als Aufklappfeld, Fälligkeit über
ein Kalendersymbol, Dunkelblau statt Schwarz im Hellmodus, Listenübersicht ganz
oben, Umbenennen direkt in der Seitenleiste, Symbole in Seitenleiste und
Schaltflächen, Punkte per Zug in eine Gruppe legen.

**3.1.0** – Aufräumversion ohne neue Bedienfunktion. Ein gemeinsamer Rahmen für
jede Änderung (`item_change`, `sidebar_change`) und ein gemeinsamer Weg für jeden
modalen Dialog (`run_modal`). Dabei behoben: Eine wirkungslose Aktion kostete bei
vollem Rückgängig-Speicher den ältesten Schritt.

**3.2.0** – Die automatische Übernahme von Nutzerdaten aus früheren
Programmnamen ist entfernt (auf ausdrücklichen Wunsch). Alle Symbole sind
Textzeichen aus einer zentralen Tabelle. Neu: ein umfangreicher Beispielbestand
unter `05_Probelisten_Testdaten`.

**Vor dem nächsten Build zuerst prüfen:** Das zu 3.0.1 gemeldete Einfrieren.
Die Ursache ist gefunden und behoben – modale Unterdialoge gaben den Tastatur-
und Mausgriff nicht zurück, wodurch die aufrufende Maske sichtbar blieb, aber
keine Eingabe mehr annahm. **Reproduzieren ließ sich der Fehler nie.** Nur
längere Benutzung auf Windows kann bestätigen, dass das die einzige Ursache war.

Ebenfalls neu zu prüfen: die Textzeichen `⊕` (Anhang) und `▦` (Fälligkeit) in
den echten Systemschriften von Windows und macOS.

## Was zwischen heute und einer Veröffentlichung liegt

Kurzfassung; die vollständige Liste steht in
`01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md`.

| Bereich | Stand |
|---|---|
| Funktion und Datenformat | fertig und automatisiert geprüft (Datenformat 10) |
| Einfrieren aus 3.0.1 | Ursache behoben, **auf Windows unbestätigt** |
| App-Icon | **fehlt** – `assets/branding` ist leer |
| Build (PyInstaller) | **fehlt** – `packaging/pyinstaller` ist leer |
| Windows-Installer | **fehlt** – `packaging/windows` ist leer |
| macOS-Bundle, DMG, Notarisierung | **fehlt** – `packaging/macos` ist leer |
| Codesignatur Windows und Apple | **fehlt**, mit Vorlauf und Kosten verbunden |
| Release-Export | **fehlt** – vorbereitet sind nur die leeren Ordner 2.5.1 und 2.5.2 |
| Lizenztext | **Platzhalter** in `LICENSE.md` |
| Markenprüfung „Glide" | **offen**, extern zu beauftragen |
| Publisher, Support, Datenschutz-URL, Preis | **offen**, Geschäftsentscheidungen |
| Produktdatenblatt | auf 3.2.0 nachgeführt (`40_Store_Material/Produktdatenblatt_3.2.0.md`) |
| Store-Texte | entworfen, redaktionell **nicht freigegeben** |
| Screenshots | Prüfaufnahmen unter `50_Ablage/Screenshots/3.2.0/`, **kein Store-Material** |
| Manuelle Prüfung Windows und macOS | **offen** |

Die ausführliche Management- und Release-Arbeitsgrundlage liegt als Word-Datei
unter `10_Dokumentation/` – dort in der Fassung **2.6.0**. Sie ist damit das
einzige größere Dokument, das noch nicht auf 3.2.0 steht; als Binärdatei wurde
sie hier nicht angefasst.
