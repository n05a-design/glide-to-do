# Probelisten 3.3.0

Zwei Komplettbackups zum Ausprobieren, beide erzeugt mit Glide 3.3.0,
Datenformat 10. Die Vorgänger liegen unverändert im `Archiv/`.

| Datei | Zweck |
|---|---|
| `Glide-Funktionsvorschau_3.3.0.glidebackup` | Ausführlicher Beispielbestand: zeigt jede Funktion an realistischen Inhalten. |
| `Glide-Releaseplanung_3.3.0.glidebackup` | Drei Arbeitslisten zur Veröffentlichung: Unterlagen & Assets, Vermarktungsstrategie, belegte Feature-Übersicht. |

## Laden

In Glide über **„Datei → Komplettbackup laden …"**.

**Achtung:** Ein Komplettbackup **ersetzt den gesamten vorhandenen Bestand** –
auch die jeweils andere Datei. Die beiden Dateien lassen sich also nicht
nacheinander laden, ohne einander zu überschreiben. Glide legt vorher
automatisch eine Sicherung an und nennt den Pfad; wer bereits eigene Listen
führt, macht vorher besser selbst ein Backup über
„Datei → Komplettbackup speichern …" oder arbeitet mit einem separaten
Datenordner über die Umgebungsvariable `GLIDE_DATA_DIR`.

## Inhalt der Funktionsvorschau

| | |
|---|---|
| Ordner | 5, davon 2 verschachtelt |
| Listen | 10 |
| Punkte | 140 |
| davon Gruppen | 10 |
| davon Long-Tasks (Notizen) | 13 |
| davon Zwischenüberschriften | 25 |
| Labels | 9, über alle sieben Palettenfarben |
| Papierkorb | 3 Einträge (Liste, Ordner, einzelner Punkt) |

Inhaltlich ein Grafik- und Marketingarbeitsplatz im Wohn- und Städtebau:
Exposé-Produktion von der Datenübernahme bis zur Druckfreigabe, Website und
Redaktionsplan, eine Frühjahrskampagne mit Print, Außenwerbung und Digital,
Vermarktungsstart und Baustellenkommunikation eines Neubauvorhabens sowie ein
Ordner mit Gestaltungsregelwerk, Druckdaten-Checkliste und Textbausteinen.

Die Notizen sind echte Notizen: Farbwerte mit Begründung, Logo-Schutzraum,
Bildsprache, Tonalität, Vorbereitung eines Fototermins.

## Inhalt der Releaseplanung

| | |
|---|---|
| Ordner | 1 („Releaseplanung 3.3.0") |
| Listen | 3 plus Eingang |
| Punkte | 115 |
| Labels | 9, darunter Blocker, Windows, macOS, Text, Grafik, Recht, Annahme |

Recherchierte Angaben tragen Quelle und Abrufdatum im Beschreibungstext.
Punkte, die auf einer Annahme beruhen, tragen das Label „Annahme".

## Neu in 3.3.0 – gut an beiden Dateien zu sehen

Die Ansicht **„Labels"** in der Seitenleiste zeigt beide Bestände nach Labels
gruppiert, jeden Punkt in der Farbe seines Labels. Ein Punkt mit mehreren
Labels steht in jeder zugehörigen Gruppe; „Ohne Label" sammelt den Rest.
Ein Punkt lässt sich per Ziehen in eine andere Gruppe legen – dabei wird genau
das Label der Herkunftsgruppe getauscht, alle übrigen bleiben stehen.

## Fristen

Alle Fälligkeiten entstehen **relativ zum Erzeugungstag** (04.09.2026).
Überfällige, heutige und künftige Punkte sind also immer vertreten. Wer die
Datei viel später lädt, sieht eine plausible, aber verschobene Lage.

## Erzeugung

Reproduzierbar über `01_Repository/Glide/tests/tools/beispieldaten.py`
beziehungsweise `releasedaten.py`. Der Inhalt steht dort im Quelltext. Beide
Dateien werden vom Integrationstest auf demselben Weg eingelesen wie bei einem
echten Import und auf Umfang, Artenverteilung, Labelverweise und
Palettenabdeckung geprüft – sie können also nicht unbemerkt veralten.
