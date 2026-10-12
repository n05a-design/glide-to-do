# Tagesplanung – Nachweisrahmen

Stand 12.10.2026 · Glide 3.39.0 · Aufgabenformat 23

Paket 4 setzt S26-05/06/18 nach D20/D30/D38 vollständig im gewählten Rahmen um.
Aktuell vorbereiteter Kandidat; noch keine Vollabnahme oder Lieferung.
Gezielte Prüfungen und Vorversion werden mit ihrem jeweiligen Quellhash nachgetragen.
Mac-/Linux-/Windows-Vollprüfung, Lieferhashes, Bundle und Signaturen stehen aus.
Tatsächliche menschliche Bedienung bleibt ein gesondertes Abnahmetor.

Gezielte Proben vor dem Einfrieren:

- [Zusammenhängende Pflichtsuite](gezielt-gesamt.json): 22 Prüfgruppen am endgültigen 3.39-Kandidaten grün, keine Callbackfehler; tatsächlicher Neustart und atomare Schreibfehler enthalten.
- [Vier getrennte Gegenproben](gezielt-ergebnis.json): gegen tatsächlich gelieferte 3.38.0/Commit 4bf8a78 passend rot; frühere positive Gruppen gehören zum dort ausdrücklich genannten Entwurfhash.
- [Echter Altleser-Rundlauf](altleser3380.json), [auslaufende QA-Nachweise](aufbewahrung33320.json).
- [Acht eigene Dialogbilder tatsächlich betrachtet](fenster.json), [Quellabgleich nach Sichtkorrektur](quellabgleich_nach_sichtkorrektur.json). PNGs ausschließlich lokal, keine Bildschirmaufnahmen oder Nutzerdaten.

Mac-Vollprüfung beginnt nach erfolgreicher Standprüfung auf unveränderlicher Kopie außerhalb OneDrive. Alle nativen Vollprüfungen und der Lieferabschluss bleiben bis zum Ergebnis offen.

Laufender [inhaltlicher Dokumentabgleich](dokumentabgleich_paket3.json): zehn verbliebene Paket-3-Statusstellen in Plan, Analyse, Markt, Veröffentlichung, Produktidentität und Übergabe nach dem tatsächlichen Liefercommit/native Matrix korrigiert. Historische Prüfbelege unverändert; endgültiger Sprintabgleich nach Paket 8 offen.


Der [erste Mac-Volllauf](mac_vorlauf.json) endete rot, weil der bisherige
Erinnerungstest weiterhin fünf Knöpfe erwartete. Die fünf Bestandsaktionen
sind erhalten; Tageshinweise und ihre Einstellungen ergänzen die Übersicht.
Der korrigierte Test fordert alle sieben Beschriftungen, vollständige
Sichtbarkeit bei 720 × 520 und beide neuen Weiterleitungen. Die
[gezielte Nachprüfung](erinnerungen.json) ist diesem Werkzeugstand zugeordnet.
Appcode und sein SHA-256 blieben unverändert. Danach folgt eine frische
eingefrorene vollständige Prüfung; der rote Lauf bleibt als eigener Beleg erhalten.

[Weiterer Abgleich der Entscheidungsübersicht](dokumentabgleich_paket3_entscheidungsuebersicht.json): I6/I7, E-S2/E-S8 und das Bedienflächen-Abschlusskriterium gegen den gelieferten 3.38-Stand nachgeführt; aktuelle Übersicht datiert, historische Antworten unverändert.


Tempoabschluss am unveränderten Apphash 7995ecbc: fünf direkte frische Prozesse mit je 40 Wiederholungen, keine parallele Oberflächenprüfung. [Aggregation](tempo.json), Rohreihen [1](tempo-1.json), [2](tempo-2.json), [3](tempo-3.json), [4](tempo-4.json), [5](tempo-5.json). Startseite kalt p95 293,564 ms, warm Median/p95 72,059/78,483 ms; Einstellungen erste Anzeige p95 203,071 ms, warm 136,052/170,043 ms. D46/D48 erfüllt; höchster warmer Einstellungen-Einzelwert 202,054 ms ausdrücklich enthalten.


Mac-Abnahme und lokaler Lieferweg abgeschlossen:

- [Frischer vollständiger Mac-Lauf](mac_voll.json): Exit 0, 103 ausgeführt/zwei übersprungen, 950 eingefrorene Dateien nach Vollprüfung unverändert.
- [Produktionsübernahme](produktionsuebernahme.json), [203 Lieferdateien](lieferung.json), [111 Bundle-Dateien und beide Signaturen](bundle.json).
- 86 Suiten/432 Unit-Tests; 22 neue Prüfgruppen, vier passende rote Vorversionskontrollen, tatsächlicher 3.38-Settings-Rundlauf und acht betrachtete eigene Dialogbilder.
- Native Linux-/Windows-Vollmatrix, strenge Kandidat-CI und Liefercommit noch offen. Menschliche Bedien-/DPI-/Readerprüfung getrennt.


[Strenge lokale Kandidat-CI](grundstufe_kandidat.json) grün (bekannter lokaler SSL-Hinweis beim unveränderten Fremdcodeabruf). Nutzer-Skilldateien waren vom isolierten Projektprüfstand ausgeschlossen. Nativer Originalvergleich folgt verpflichtend in der Matrix.
