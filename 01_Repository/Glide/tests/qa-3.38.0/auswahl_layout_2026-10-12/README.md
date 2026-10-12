# Auswahl und Windows-Kopfzeile – Kandidat 3.38.0

Stand 12.10.2026 · Glide 3.38.0 · Aufgabenformat 23 · neue Produktionskorrektur in Abnahme

Aktueller Root-App-SHA-256: `bcdbc4da2197aadaffbe65cd57054c68b93db4d1aedcb9cbeb16c2204bd8ef41`. Dieser Stand ist noch keine Lieferung. Die folgenden abgeschlossenen Mac-/Linux-Belege gelten für den Vorgänger `8cda250c`.
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
Mehrfachauswahl und separate Windows-Menüzeile. Die neue Mac-Vollprüfung
und die gezielte native Windows-Wiederholung sind inzwischen grün (unten).
Vollständige Windows-Abnahme, Tempoabschluss und neuer
07-/Showcase-/Bundleabgleich bleiben offen. Menschenabnahme bleibt getrennt.
Rohprotokolle und eigene Fensterbilder bleiben außerhalb OneDrive und Git.

Die isolierte [Kandidat-Grundstufe](kandidat_grundstufe.json) ist grün.
Der noch abweichende 07-Hauptstand wird ausdrücklich als Kandidathinweis
gemeldet; dies ist keine strenge Lieferstandabnahme. Der lokale
Originalpaketabruf meldet den bekannten SSL-Zertifikathinweis.

Nach Übernahme des Remote-Merges b34cbd7/main 42e6c35 ist die
[erneute Grundstufe](grundstufe_nach_main.json) ebenfalls grün; App unverändert.
Die Main-Ergänzung enthält Projekt-Skill/Standprüfwerkzeug, keine App-Funktion.

Die [native Windows-Wiederholung](windows_layout.json) am Kandidatcommit
034662d besteht alle 36 Layoutkombinationen einschließlich der Menüknöpfe.
Lauf 38213138878 ist vollständig beendet, Ergebnis grün. Dies ist eine
gezielte Layoutprüfung; die vollständige native Matrix bleibt erforderlich.

Neue [Mac-Vollprüfung](mac-voll.json) grün: 102 ausgeführt/zwei übersprungen,
85 Suiten/294 Unit-Tests; alle 885 eingefrorenen Dateien unverändert.
[Vier aktuelle Vorversionsgegenproben](vorversionsgegenproben.json) gegen
den gelieferten 3.37.0-Commit passend rot. [Bewegung](bewegung.json) und
[sechs tatsächlich betrachtete eigene Fenster](fensterbeurteilung.json)
am selben Hash neu belegt; menschliche Bedienung bleibt getrennt.

Main-Merge PR #19 (029b821) ist bytegleich zum Kandidatcommit 034662d.
Seine native Matrix 38213392543 bestätigt bereits [Linux](linux-voll.json)
und [alle 18 Defektgegenproben](linux-defektgegenproben.json). [Windows](windows-vollbefunde.json) ist mit drei Kopftextanschnitten beendet: Mindestgröße, Titel und Planungsrückmeldung; übrige 82 Suiten einschließlich neuer Aufgabensuite grün.
Die [Tempo-Diagnose](tempo.json) enthält beide Grenzbefunde und den
Vergleich mit dem unveränderten bisherigen Kandidaten. Nach Ende der Matrix
ist eine serielle Abschlussmessung nötig; D47 wird nicht still gelockert.
Lieferabgleich/Bundle und strenge Liefer-CI bleiben offen.

Die anschließende technische Korrektur ordnet die vier Windows-Menüs innerhalb der Titelzeile an; die Statuszeile darunter behält ihre Breite. Titelmessung berücksichtigt die Menübreite. [36 lokale Menüpfadkombinationen](menues_titelzeile_mac.json) und [alle drei betroffenen Suiten](titelzeilen_mac.json) sind grün; die unveränderte Titelprüfung ist am Vorgänger passend rot. Eine solche Prüfung auf dem Mac ersetzt keine native Windows-Abnahme. Die vollständigen Prüfstände werden erneut ausgeführt.

[Serielle Abschlussmessung](tempo_abschluss.json) nach Ende der Matrix: fünf direkte Prozesse × 40 Wiederholungen, Einstellungen warm 146,85 ms Median/179,59 ms p95. Erstöffnung und Startseite innerhalb ihrer Grenzen; Einstellungs-p95 überschreitet D47. Frage 30 zur vorgeschlagenen Grenze 190 ms bleibt offen; keine Ausnahme vorweggenommen. [Kandidat-Grundstufe](kopfzeilen_grundstufe.json) grün, Lieferstand weiterhin ausdrücklich abweichend.
