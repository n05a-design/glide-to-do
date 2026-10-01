# Checkliste je Aufgabe – Glide 3.22.0

Stand 17.09.2026 · Glide 3.22.0 · Aufgabenformat 16

Eine Aufgabe besteht oft aus wenigen Handgriffen, die keine eigenen Termine,
Labels oder Anhänge brauchen. Dafür gab es bisher nur Unterpunkte – sie tragen
den vollen Funktionsumfang mit und machen aus drei Handgriffen drei Aufgaben.
3.22 ergänzt die **Checkliste**: eine Folge kurzer Schritte mit Text und
Zustand, wie die Checkliste einer Aufgabe in Microsoft Planner.

## Bedienung

Die Punktmaske zeigt zwischen Beschreibung und Anhängen den Abschnitt
„Checkliste“. Eine Eingabezeile legt mit Enter oder „+ Schritt“ den nächsten
Schritt an, „Abhaken“ und die Leertaste schalten den Zustand um, „▲“ und „▼“
ordnen, „Entfernen“ löscht. Rechts über der Liste steht der Stand.

Wo die Checkliste erscheint:

- In der Listenansicht als Zusatz hinter dem Aufgabentext: `☑ 2/5`.
- In der Tabellenansicht als eigene Spalte „Checkliste“; sie ist über
  „Spalten …“ ein- und ausblendbar und über die Überschrift sortierbar.
- Auf einer Pinnwandkarte als Fortschrittsbalken mit Beschriftung.
- In der Reiteransicht als Liste der Schritte mit ihrem Zustand.
- Im Markdown-Export als eingerückte Kästchenliste, im Druck als Zeile
  „Checkliste: 2 von 5“.

Gruppen und Zwischenüberschriften tragen keine Checkliste – sie haben nichts
abzuhaken. Wechselt die Art eines Punkts auf Gliederung, verschwindet der
Abschnitt aus der Maske.

## Abgrenzung zum Unterpunkt

Ein Schritt der Checkliste trägt **nur** Text und Zustand. Wer Termin,
Wichtigkeit, Labels, Anhänge, Wiederholung oder eine eigene Checkliste
braucht, legt einen Unterpunkt an. Die Grenze liegt bei fünfzig Schritten je
Punkt und zweihundert Zeichen je Schritt; wer mehr braucht, arbeitet mit
Unterpunkten oder einer eigenen Liste. Ein abgehakter Schritt erledigt die
Aufgabe nicht und zählt nicht in Bestand, Tagesziel oder Aufwand.

## Daten und Migration

Aufgabenformat **16** ergänzt am Punkt das additive Feld `checklist`: eine
Liste aus `{"id", "text", "done"}`. Fehlt das Feld, trägt der Punkt keine
Checkliste. Format-15-Dateien bleiben unverändert gültig und werden beim
Laden ergänzt.

Vor dem ersten Speichern in Format 16 legt Glide die unveränderte
Originaldatei als `backups/liste_vor_format16_<Zeitstempel>.json` ab. Ältere
Glide-Fassungen bis 3.21 können Format 16 nicht lesen; für einen Rückwechsel
ist diese Kopie da.

Ein beschädigtes Feld führt auf eine leere Checkliste zurück, statt die Datei
unlesbar zu machen. Leere Schritte fallen weg, doppelte Kennungen werden neu
vergeben. Die strenge Backupprüfung weist eine Checkliste ab, die keine Liste
ist. Der Änderungsverlauf protokolliert Änderungen an der Checkliste als
eigenes Feld.

Die Regression steht in `tests/integration/test_features322.py`, das
Referenzformat in `tests/fixtures/current_v16/reference_v16.json`.

[Datenvertrag](06_DATA_BACKUP_MIGRATION.md) ·
[Gruppe, Ordner oder Zwischenüberschrift?](decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md)
