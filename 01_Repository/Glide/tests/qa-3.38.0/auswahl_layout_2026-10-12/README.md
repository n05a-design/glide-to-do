# Auswahl und Windows-Kopfzeile – Kandidat 3.38.0

Stand 12.10.2026 · Glide 3.38.0 · Aufgabenformat 23 · neue Produktionskorrektur in Abnahme

App-SHA-256: `8cda250ca0e6219f9d9cab165e6a05b8e161b4bad148175d916e3143d993dccc`. Dieser Stand ist noch keine Lieferung.
Die bisherigen Mac-Vollprüfung, 07- und Bundlebelege am Hash `49ca48aa`
bleiben [historisch getrennt](../aufgaben_2026-10-11/README.md).

Der echte Größenwechsel am unveränderten Vorgängerhash 49ca48aa verlor
zwei ausgewählte Zeilen bis auf eine; der Stack führt in den verzögerten
Langtextumbruch. Der reine Layoutweg bewahrt nun Auswahl, Zeilenfokus und
Bildlauf; ein inzwischen erfolgter Bereichswechsel beendet den alten Auftrag.
Die bestehende Aufräumsuite enthält zwei tatsächliche Größenwechsel und
einen eigenen gezielten Defekteinstieg.

Der native [Windows-Diagnoselauf 38181035403](https://github.com/n05a-design/glide-to-do/actions/runs/38181035403)
weist [147 px Inhaltskante](windows_ursache.json) nach: Die zusätzliche eigene
Menüzeile beansprucht 30 px, Kopf und Werkzeugzeile sind schon 61/40 px hoch.
Die vorhandenen vier Menüknöpfe teilen jetzt die Kopfzeile neben den
Symbolaktionen. Menübaum, Beschriftungen, Fokusweg und Alt-Kürzel bleiben
erhalten. Die Menürahmenbreite folgt den tatsächlichen Knopfbreiten.

Die [lokale Kontrolle mit aktiviertem Windows-Menüpfad](menues_mac.json)
besteht 36 Ansichts-/Größen-/Schriftkombinationen auf dem Mac, einschließlich
860 × 700 und großer Schrift. Sie ersetzt keinen nativen Windows-Lauf.
Die Pflichtsuite prüft jeden Menüknopf vollständig sichtbar und die
vorhandenen Alt-Bindungen. Die 15-Prozent-Grenze bleibt unverändert.

[Gezielte Kontrollen](gezielte_proben.json) am oben genannten Hash grün:
Hauptsuite, vollständige Aufräumsuite sowie passende rote Defektkopien für
Mehrfachauswahl und separate Windows-Menüzeile. Native Windows-Wiederholung,
neue eingefrorene Mac-Vollprüfung und abschließender
07-/Showcase-/Bundleabgleich bleiben Pflicht und werden am tatsächlichen Hash nachgetragen. Menschenabnahme bleibt getrennt.
Rohprotokolle und eigene Fensterbilder bleiben außerhalb OneDrive und Git.

Die isolierte [Kandidat-Grundstufe](kandidat_grundstufe.json) ist grün.
Der noch abweichende 07-Hauptstand wird ausdrücklich als Kandidathinweis
gemeldet; dies ist keine strenge Lieferstandabnahme. Der lokale
Originalpaketabruf meldet den bekannten SSL-Zertifikathinweis.
