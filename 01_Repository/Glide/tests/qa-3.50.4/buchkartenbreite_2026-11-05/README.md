# Buchbreite bis zur Karteninnenkante – 3.50.4

Stand 05.11.2026 · Aufgabenformat 26

Erneute direkte menschliche Rückmeldung zu Punkt 6: „Es ist immer noch nicht die ganze Breite?“ Drei Originalbilder bytegleich lokal gesichert; Hashes im [Ergebnis](ergebnis.json). Punkt 6 bleibt nicht bestanden, bis der korrigierte Nachtest menschlich bestätigt ist.

## Ursache der unzureichenden ersten Korrektur

Die bisherige Prüfung kontrollierte Spaltensumme und rechte Zellenkante nur gegen das Treeview-Widget. Dieses Widget hatte selbst noch 14 px Packabstand auf jeder Seite. Deshalb konnten alle bisherigen 64 Prüfungen grün sein, obwohl das Buch die Karteninnenbreite nicht ausnutzte. Der frühere Vier-Pixel-Rahmenabzug war ein separater kleiner Befund und löste diesen Packabstand nicht.

`sync_row_action_space` setzt für Bücher jetzt `padx=(0,0)`. Die gemeinsame Kartenrundung und deren eigener Innenrand bleiben erhalten; Tabellenfläche und Spalten füllen bis zu diesen Innenkanten. Labels und echte Aufgaben behalten ihre bisherigen Abstände/Aktionsflächen.

## Nachweis

- Bestehende Abnahmekorrekturprobe vor Änderung grün.
- Erweiterte Buchbreitenprobe auf unverändertem `8b3076f9…` gezielt rot: Baum beginnt bei 338, Karteninnenkante bei 324, also 14 px Versatz.
- App `85a61f0a…`: 64 erweiterte Buchbreitenprüfungen grün, nun mit linken/rechten Karteninnenkanten als äußerer Referenz. Volle/schmale/ausgeblendete Seitenleiste, 860/1280 px, Hin-/Rückwechsel, Hell/Dunkel/Glas und mittlere/große Schrift.
- Echte Sichtmessungen und Windows-Aufnahmen: 536/536 px bei schmalem Fenster mit Seitenleiste, 804/804 px ohne Seitenleiste, 1116/1116 px breit. Links jeweils identische absolute Koordinate.
- Bestehende `menschen3503`- und `werkzeugzeile`-Proben grün; die bewusst geänderte Buch-Abstandserwartung von 14 auf 0 nachgeführt, Labels-Erwartung bleibt 14. Syntax und Python-Liefergleichheit (93 Code-/171 Ressourcendateien) grün.

Rohbelege und neue Fensteraufnahmen unter `%USERPROFILE%/gq/bcard4/`. Keine neuen nativen Pakete, keine neue Plattform-Vollmatrix oder strenge Grundstufe für diesen letzten Hash behauptet; die frühere 19/19-Grundstufe gehört zu `8b3076f9…`. Menschlicher Nachtest sowie weitere Abnahmeblöcke bleiben offen. Keine Git-/Releaseaktion.

**Bereitgestellt:** Neue eingefrorene Python-Prüffassung `85a61f0a…` mit eigener synthetischer Datenkopie unter `%USERPROFILE%/gq/bcard4/Nachtest_starten.pyw` gestartet. JSON-Bytes der Quelle vor/nach Kopie identisch; Sperr-/Sitzungsdateien nicht übernommen, frühere Prüffassungen unverändert. Punkt 6 bleibt bis zur Benutzerrückmeldung offen.
