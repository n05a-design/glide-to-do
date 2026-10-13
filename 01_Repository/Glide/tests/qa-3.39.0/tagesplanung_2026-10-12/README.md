# Tagesplanung – Nachweisrahmen

Stand 13.10.2026 · Glide 3.39.0 · Aufgabenformat 23

Paket 4 setzt S26-05/06/18 nach D20/D30/D38 vollständig im gewählten Rahmen um.
Kandidat c38d960 mit Apphash 7995ecbc ist auf dem Mac vollständig geprüft.
Gezielte Prüfungen, Vorversion, Lieferhashes, Bundle und Signaturen sind unten belegt.
Die serielle native Matrix [38309209555](https://github.com/n05a-design/glide-to-do/actions/runs/38309209555) endete rot: Grundstufe und Linux-Vollprüfung grün (18 Defektgegenproben passend rot), Windows mit zwei Prüfstandsbefunden ([Auswertung](native_38309209555.json)). Korrigiert wurde nur der Prüfstand; App, Lieferdateien und Bundle bleiben am Apphash 7995ecbc. Neuer nativer Lauf und Liefercommit stehen aus.
Tatsächliche menschliche Bedienung bleibt ein gesondertes Abnahmetor.

Gezielte Proben vor dem Einfrieren:

- [Zusammenhängende Pflichtsuite](gezielt-gesamt.json): 22 Prüfgruppen am endgültigen 3.39-Kandidaten grün, keine Callbackfehler; tatsächlicher Neustart und atomare Schreibfehler enthalten.
- [Vier getrennte Gegenproben](gezielt-ergebnis.json): gegen tatsächlich gelieferte 3.38.0/Commit 4bf8a78 passend rot; frühere positive Gruppen gehören zum dort ausdrücklich genannten Entwurfhash.
- [Echter Altleser-Rundlauf](altleser3380.json), [auslaufende QA-Nachweise](aufbewahrung33320.json).
- [Acht eigene Dialogbilder tatsächlich betrachtet](fenster.json), [Quellabgleich nach Sichtkorrektur](quellabgleich_nach_sichtkorrektur.json). PNGs ausschließlich lokal, keine Bildschirmaufnahmen oder Nutzerdaten.

Die Mac-Vollprüfung lief nach erfolgreicher Standprüfung auf eingefrorener Kopie außerhalb OneDrive. Native Linux-/Windows-Ergebnisse und Lieferabschluss werden erst nach dem vollständigen grünen Lauf übernommen.

Laufender [inhaltlicher Dokumentabgleich](dokumentabgleich_paket3.json): zehn verbliebene Paket-3-Statusstellen in Plan, Analyse, Markt, Veröffentlichung, Produktidentität und Übergabe nach dem tatsächlichen Liefercommit/native Matrix korrigiert. Historische Prüfbelege unverändert; endgültiger Sprintabgleich nach Paket 8 offen.


Der [erste Mac-Volllauf](mac_vorlauf.json) endete rot, weil der bisherige
Erinnerungstest weiterhin fünf Knöpfe erwartete. Die fünf Bestandsaktionen
sind erhalten; Tageshinweise und ihre Einstellungen ergänzen die Übersicht.
Der korrigierte Test fordert alle sieben Beschriftungen, vollständige
Sichtbarkeit bei 720 × 520 und beide neuen Weiterleitungen. Die
[gezielte Nachprüfung](erinnerungen.json) ist diesem Werkzeugstand zugeordnet.
Appcode und sein SHA-256 blieben unverändert. Die danach durchgeführte frische
eingefrorene vollständige Prüfung ist unten belegt; der rote Lauf bleibt als eigener Beleg erhalten.

[Weiterer Abgleich der Entscheidungsübersicht](dokumentabgleich_paket3_entscheidungsuebersicht.json): I6/I7, E-S2/E-S8 und das Bedienflächen-Abschlusskriterium gegen den gelieferten 3.38-Stand nachgeführt; aktuelle Übersicht datiert, historische Antworten unverändert.


Tempoabschluss am unveränderten Apphash 7995ecbc: fünf direkte frische Prozesse mit je 40 Wiederholungen, keine parallele Oberflächenprüfung. [Aggregation](tempo.json), Rohreihen [1](tempo-1.json), [2](tempo-2.json), [3](tempo-3.json), [4](tempo-4.json), [5](tempo-5.json). Startseite kalt p95 293,564 ms, warm Median/p95 72,059/78,483 ms; Einstellungen erste Anzeige p95 203,071 ms, warm 136,052/170,043 ms. D46/D48 erfüllt; höchster warmer Einstellungen-Einzelwert 202,054 ms ausdrücklich enthalten.


Mac-Abnahme und lokaler Lieferweg abgeschlossen:

- [Frischer vollständiger Mac-Lauf](mac_voll.json): Exit 0, 103 ausgeführt/zwei übersprungen, 950 eingefrorene Dateien nach Vollprüfung unverändert.
- [Produktionsübernahme](produktionsuebernahme.json), [203 Lieferdateien](lieferung.json), [111 Bundle-Dateien und beide Signaturen](bundle.json).
- 86 Suiten/432 Unit-Tests; 22 neue Prüfgruppen, vier passende rote Vorversionskontrollen, tatsächlicher 3.38-Settings-Rundlauf und acht betrachtete eigene Dialogbilder.
- Strenge Kandidat-CI grün; erste native Matrix unter Windows rot (Prüfstand, siehe oben), Wiederholung und Liefercommit offen. Menschliche Bedien-/DPI-/Readerprüfung getrennt.


[Strenge lokale Kandidat-CI](grundstufe_kandidat.json) grün (bekannter lokaler SSL-Hinweis beim unveränderten Fremdcodeabruf). Nutzer-Skilldateien waren vom isolierten Projektprüfstand ausgeschlossen. Nativer Originalvergleich folgt verpflichtend in der Matrix.

Prüfstandskorrektur nach der roten Windows-Matrix (13.10.2026): sieben Unit-Testdateien nutzen die mitgelieferten IANA-Daten über `timezones.Resolver`, `test_features329` wartet bis zum Ruhezustand der Zeichenfläche (Frist 3 s, Defektgegenprobe rot), die CI-Grundstufe prüft die Fachlogik zusätzlich ohne Systemzeitzonen. [Strenge isolierte Kandidat-CI](grundstufe_kandidat2.json) grün mit 19 Schritten (bekannter lokaler SSL-Hinweis beim Fremdcodeabruf). App/07/Bundle unverändert am Apphash 7995ecbc.

Zweite native Matrix [38322509008](https://github.com/n05a-design/glide-to-do/actions/runs/38322509008) am Kandidaten c2e792b ([Auswertung](native_38322509008.json)): Grundstufe und Linux grün, unter Windows die Unit-Tests und die erste Zeichenflächenstelle grün; `test_features329` scheiterte an einer zweiten festen 150-ms-Wartezeit nach dem Ansichtswechsel. Beide Stellen nutzen jetzt dieselbe Wartefunktion (mindestens 150 ms, dann bis zur Bedingung, Frist 3 s); zwei Defektgegenproben rot. Mac-Vollprüfung am Kandidaten c2e792b auf eingefrorener Kopie: 103 ausgeführt/zwei übersprungen, 988 Dateien unverändert.
