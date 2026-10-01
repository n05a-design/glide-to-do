# Funktionsvorschau 3.2.0

`Glide-Funktionsvorschau_3.2.0.glidebackup` – ausführlicher Beispielbestand zum
Ausprobieren. Nachfolger von `Glide-Funktionsvorschau.glidebackup`; die ältere
Fassung gehört ins `Archiv`.

## Laden

In Glide über **„Datei → Komplettbackup laden …"**.

**Achtung:** Ein Komplettbackup **ersetzt den gesamten vorhandenen Bestand**.
Glide legt vorher automatisch eine Sicherung an und nennt den Pfad, aber wer
bereits eigene Listen führt, macht vorher besser selbst ein Backup über
„Datei → Komplettbackup speichern …".

## Inhalt

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

## Fristen

Alle Fälligkeiten entstehen **relativ zum Erzeugungstag** (04.09.2026).
Überfällige, heutige und künftige Punkte sind also immer vertreten. Wer die
Datei viel später lädt, sieht eine plausible, aber verschobene Lage.

## Erzeugung

Reproduzierbar über `01_Repository/Glide/tests/tools/beispieldaten.py`.
Der Inhalt steht dort im Quelltext und lässt sich an einer Stelle ändern.
Der Integrationstest liest die Datei auf demselben Weg ein wie ein echter
Import und prüft Umfang, Artenverteilung, Labelverweise und Palettenabdeckung –
sie kann also nicht unbemerkt veralten.
