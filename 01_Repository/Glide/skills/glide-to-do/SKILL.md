---
name: glide-to-do
description: Legt Ergebnisse direkt als Glide-Importdateien an. Recherchen, Berichte und Übersichten werden eine Glide-Seite (Markdown), Aufgabenlisten, Einkaufslisten, Projekte und Aufgabenübersichten eine .glideexchange-Datei mit Ordnern, Listen, Punkten, Fälligkeiten, Bearbeitungstagen, Aufwand, Wichtigkeit, Labels, Checklisten, Dateianhängen, Galeriebildern und Titelbildern; dazu Notizen, Pixelzeichnungen und Änderungsvorschläge zu einem Glide-Kontextpaket (.glidecontext). Verwenden, wenn der Nutzer Glide nennt, etwas „für Glide“ oder „zum Import in Glide“ haben möchte oder eine Datei mit Endung .glideexchange oder .glidecontext vorliegt. Auch für englische Anfragen wie Glide task list, shopping list, project plan oder report.
license: MPL-2.0
compatibility: Erzeugt Dateien für Glide 1.0 oder neuer (Austauschformat 2). Das optionale Hilfsskript braucht Python 3.9 oder neuer, nur Standardbibliothek.
metadata:
  version: "1.4"
  glide-version: "1.0.1"
  exchange-format: "2"
---

# Glide-Dateien anlegen

Glide ist ein lokaler Desktop-Planer für Aufgaben, Listen, Seiten, Notizen und Pixelzeichnungen. Er läuft ohne Konto und ohne Netz. Du schreibst **Importdateien**; der Nutzer öffnet sie in Glide, sieht eine Vorschau und übernimmt sie mit einem einzigen Rückgängig-Schritt. Glide legt dabei nur Neues an und überschreibt nichts.

**Niemals** in den Glide-Datenordner schreiben, `liste_speicher.json`, `settings.json` oder `vorlagen.json` anfassen oder `.glidebackup`/`.glideapp` erzeugen. Diese Dateien tragen interne Kennungen und Schutzmechanismen; Fremdeingriffe können Daten zerstören.

## 1. Weg wählen

| Der Nutzer möchte … | Datei | Import in Glide |
|---|---|---|
| Recherche, Bericht, Übersicht, Protokoll, Anleitung – formatierter Text, gern mit Tabellen und Aufgaben | **Seite** als `.md` | Datei › Importieren › „Seite aus Datei …“ oder „Seite aus Zwischenablage“ |
| Aufgabenliste, Einkaufsliste, Packliste, Projekt, Wochenplan, Aufgabenübersicht | `.glideexchange` mit Ordnern, Listen und Punkten | Datei › Datenaustausch › „KI-Ergebnis importieren …“ |
| Kurze Notiz ohne Formatierung, auch mit einzelnen Aufgaben | `.glideexchange` mit `list_kind: "note"` | wie oben |
| Pixelzeichnung, Symbol | `.glideexchange` mit `list_kind: "drawing"` über das Hilfsskript | wie oben |
| Vorhandene Glide-Aufgaben überarbeiten (Termine, Wichtigkeit, Titel, Beschreibung, Labels) | Änderungsvorschlag `mode: "patch"` als Antwort auf ein Kontextpaket | wie oben |

Ein Projekt darf aus zwei Dateien bestehen: eine `.glideexchange` mit den Aufgaben und eine `.md`-Seite mit Ziel, Hintergrund und Entscheidungen.

Details: [Austauschformat](references/austauschformat.md), [Seiten in Markdown](references/seiten-markdown.md), [Rezepte je Dokumentart](references/dokumentarten.md), [Änderungsvorschlag](references/aenderungsvorschlag.md). Wie Glide aufgebaut ist und speichert: [Glide verstehen](references/glide-aufbau.md).

## 2. Inhalt nach Glide-Regeln ordnen

1. **Titel höchstens 40 Zeichen** – für Listen, Ordner, Punkte und Seiten. Glide kürzt längere neue Titel und schiebt das Original in die Beschreibung. Details, Mengen und Begründungen gehören in `description`.
2. **Fälligkeit und Bearbeitungstag sind verschieden.** `due` sagt, *bis wann* etwas fertig sein muss; `planned_date` sagt, *wann* man daran arbeitet. Nur setzen, was der Nutzer gesagt hat oder was sich zwingend ergibt.
3. **Nicht jeder Absatz ist eine Aufgabe.** `task` für etwas, das man erledigen kann; `heading` für Abschnitte; `group` für einen Behälter mit Unterpunkten; `long` für erklärenden Text. Gruppen und Überschriften haben keine Termine, Wichtigkeit oder Checkliste.
4. **Unterpunkte oder Checkliste?** `children` sind eigenständig erledigbare Punkte (höchstens 12 Ebenen). `checklist` sind kurze Schritte innerhalb eines Punkts ohne eigene Termine (höchstens 50, je 200 Zeichen).
5. **Wenige, wiederverwendete Labels** statt eines Labels je Aufgabe. Labels können an Punkten, Listen und Ordnern vergeben werden.
6. **Datum als `JJJJ-MM-TT`, Uhrzeit als `HH:MM`.** Relative Angaben („nächsten Freitag“) vom heutigen Datum des Nutzers aus berechnen; kennst du das Datum nicht, frag nach oder lass das Feld weg. Eine Uhrzeit braucht ein Datum.
7. **Wiederholungen und Benachrichtigungen.** An Aufgaben mit Fälligkeit können Wiederholungen (`repeat`: `daily`, `weekly`, `monthly`, `yearly`, `weekdays`, `every_n_days`) und Erinnerungen (`reminder`: relativ oder fest) direkt gesetzt werden.
8. **Wichtigkeit 0–3** (0 keine, 3 hoch), sparsam vergeben. **Aufwand** `estimated_minutes` als ganze Minuten.
9. **Nichts erfinden.** Keine Felder außerhalb des Formats, keine internen Kennungen, keine Kontodaten, keine absoluten Pfade, keine Bilder aus dem Netz. Freie Schlüssel (`key`) wählst du selbst; Glide vergibt die echten Kennungen.
10. **Sprache des Nutzers**, sachlich und knapp. Die Seite beginnt mit `# Titel`; diese Zeile wird der Seitentitel.

## 3. Was Glide über diese Wege noch nicht übernimmt

Farben (an Punkten, Listen und Ordnern), Pixelsymbole, Verknüpfungen („Verknüpft mit“, „Wartet auf“), Vorlagen, Pinnwand-Anordnung und Ansichtseinstellungen. Wiederholungen (`repeat`), Erinnerungen (`reminder`), Ordnerarten (`folder_kind`: standard, library, journal), formatierte Seiten/Notizen (`markdown`), Dateianhänge (`attachments`), Galerien (`gallery`) und Titelbilder (`cover`) werden direkt übernommen. Welches Glide-Feld ankommt, geplant ist oder bewusst in Glide bleibt, steht je Feld in [abdeckung.json](abdeckung.json). Details zur Verteilung und Einbindung in [VERTEILUNG.md](VERTEILUNG.md).

## 4. Datei schreiben

- UTF-8, ohne Text vor oder nach dem JSON. Dateinamen kurz und sprechend: `einkauf-wochenende.glideexchange`, `recherche-teamausflug.md`.
- **Mit Dateizugriff** (Claude Code, Codex, Copilot, Cursor, Gemini CLI): Datei im Arbeitsordner des Nutzers oder an dem Ort ablegen, den er nennt – nie im Glide-Datenordner.
- **Ohne Dateizugriff** (Chat): die Datei zum Herunterladen anbieten oder als Codeblock ausgeben und den Dateinamen nennen. Eine Seite kann der Nutzer auch kopieren und in Glide „Seite aus Zwischenablage“ wählen.
- Höchstens 5.000 Punkte und 12 MB je Austauschdatei; große Vorhaben auf mehrere Listen verteilen.

## 5. Prüfen

Wenn Python verfügbar ist:

```
python3 scripts/glide_datei.py pruefen DATEI
python3 scripts/glide_datei.py pruefen vorschlag.glideexchange --kontext paket.glidecontext
```

Fehler beheben, Warnungen ernst nehmen. Ohne Python die Regeln aus Abschnitt 2 und die [Feldtabelle](references/austauschformat.md) von Hand abgleichen. Pixelzeichnungen immer mit dem Skript kodieren:

```
python3 scripts/glide_datei.py zeichnung eingabe.json zeichnung.glideexchange
```

Das Eingabeformat zeigt [assets/beispiele/zeichnung-eingabe.json](assets/beispiele/zeichnung-eingabe.json).

**Darstellung in Glide prüfen.** Arbeitest du im Glide-Repository, zeigt die zentrale Prüfung mit dem echten Glide-Code, wie Glide die Datei darstellt – Feld für Feld, mit `--oberflaeche` in einer echten Glide-Instanz mit künstlichem Datenordner, Neustart und Ablesen der Anzeige:

```
python3 -B tests/tools/ki_ausgabe.py DATEI [--oberflaeche]
```

ABWEICHUNG heißt: Glide zeigt etwas anderes, als die Datei beschreibt. Datei anpassen und erneut prüfen.

## 6. Dem Nutzer sagen, wie es weitergeht

Kurz nennen: welche Datei(en), wo sie liegen, welcher Menüpunkt in Glide sie öffnet und was nicht übernommen wurde. Beispiel: „Öffne in Glide Datei › Datenaustausch › „KI-Ergebnis importieren …“ und wähle `einkauf-wochenende.glideexchange`. Die Vorschau zeigt 1 Liste mit 13 Punkten; mit „Importieren“ legst du sie an, Rückgängig nimmt alles zurück.“

Glide zeigt in der Vorschau unbekannte Angaben an und setzt dann den Fokus auf „Abbrechen“. Das ist ein Zeichen, dass die Datei Felder enthält, die diese Glide-Fassung nicht kennt.

## Beispiele

In [assets/beispiele/](assets/beispiele/): `einkaufsliste.glideexchange`, `projekt.glideexchange`, `notiz.glideexchange`, `zeichnung.glideexchange` mit `zeichnung-eingabe.json`, `recherchebericht.md`, `kontextpaket.glidecontext` mit `aenderungsvorschlag.glideexchange`. Alle bestehen die Prüfung des Hilfsskripts und die zentrale Prüfung mit Glide 3.69.0, auch in der echten Oberfläche.

## Für die Arbeit an Glide selbst

Der Skill beschreibt Glides Datenmodell und ist daran gekoppelt: [Glide verstehen](references/glide-aufbau.md) erklärt Bereiche, Objekte, Felder und Speicherweg, `abdeckung.json` ordnet jedes Datenfeld ein. Wer im Glide-Repository das Datenformat, ein Feld, eine Listen-, Ordner- oder Punktart oder den Austauschweg ändert, zieht diesen Skill im selben Schnitt nach; `tests/tools/test_agenten_skill.py` schlägt sonst fehl.
