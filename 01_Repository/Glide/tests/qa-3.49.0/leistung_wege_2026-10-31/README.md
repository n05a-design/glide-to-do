# WA-36: weitere Änderungswege und macOS-Nachlauf

Stand 31.10.2026 · Glide 3.49.0 · Aufgabenformat 26 · App `1fabf883…` (geliefert) · MacBook Air M2, macOS 27.2, Retina · künstliche Daten

Auftrag: Fortsetzung „weiter“ nach der unabhängigen Schlusskontrolle, zunächst reine Messung am gelieferten Stand; danach auf Nutzerentscheidung Befund 1 umgesetzt (Abschnitt „Umsetzung“). Codex maß in [§21.37](../gesamtabschluss_2026-10-31/README.md) nur den Wichtigkeitswechsel (10.000 Aufgaben: 230 → 128 ms); WA-36 verlangt den übrigen echten Mutationsweg.

## Messung

[`messung_wege.py`](messung_wege.py) nach dem Muster von `messung_mutationen.py`: 12 Listen mit festen IDs, je Größe eigener Prozess und eigenes `GLIDE_DATA_DIR`, je Weg 2 Aufwärm- und 9 Messläufe. Verbrauchende Wege werden nach jeder Runde ungemessen per Undo zurückgenommen, damit der Bestand gleich bleibt. Gemessen sind Aufruf gesamt, die Phasen Snapshot/Speichern/Rendern und der Tk-Nachlauf (`update_idletasks`/`update`) getrennt; nach jedem Schritt gespeichert und ohne Callbackfehler. Python 3.14.5 mit **Tk 9.0.3** (python.org). [Rohwerte](ergebnis.json).

| Aufgaben | Weg | gesamt Median / p95 ms | Speichern ms | Snapshot ms | Rendern ms | Tk-Nachlauf ms |
|---:|---|---:|---:|---:|---:|---:|
| 100 | Abhaken | 8 / 13 | 4 | 0,4 | 2 | 895 |
| 100 | Anlegen | 8 / 9 | 5 | 0,4 | 2 | 310 |
| 100 | Löschen / Verschieben 1 / Verschieben mehrfach | 8–10 / 12–16 | 5 | 0,4 | 2 | 93 |
| 1.000 | Abhaken | 21 / 24 | 11 | 3 | 4 | 915 |
| 1.000 | Anlegen / Löschen / Verschieben | 30–32 / 31–42 | 21 | 3 | 4 | 96–320 |
| 5.000 | Abhaken | 74 / 78 | 46 | 14 | 11 | 936 |
| 5.000 | Anlegen / Löschen / Verschieben | 125–131 / 132–139 | 95 | 15 | 12–13 | 96–283 |
| 10.000 | Abhaken | 141 / 153 | 84 | 29 | 21 | 914 |
| 10.000 | Anlegen / Löschen / Verschieben | 238–255 / 245–263 | 184 | 29 | 21–24 | 96–318 |

## Befund 1: Speichern dominiert, Vollvergleich bei Anlegen/Löschen/Verschieben

Der Aufwand wächst linear; bei 10.000 Aufgaben entfallen rund drei Viertel auf das Speichern. Abhaken läuft über `item_change(..., local=True)`: Die betroffenen Listen gehen als `changed_list_ids` an `list_comparison`, unveränderte Listen nutzen ihre zwischengespeicherten Prüfsummen (84 ms). Anlegen, Löschen und Verschieben öffnen `item_change` mit leerer Auswahl; dann gilt vertragsgemäß der Vollvergleich über alle Listen (184 ms). Eine ausdrückliche Angabe der Quell-/Zielliste würde dort voraussichtlich rund 100 ms bei 10.000 Aufgaben sparen. Das berührt die Verlaufs-/Aktivitätskorrektheit und braucht Gleichheitstests gegen den Vollvergleich; inzwischen umgesetzt, siehe unten.

## Befund 2: fester Nachlauf ist Tk 9.0 unter macOS, mit Tk 9.1 behoben

Der Nachlauf hängt nicht von der Bestandsgröße ab. Nach dem Abhaken läuft die „Erledigt“-Fahne (`_draw_celebration`, 14 Bilder à 38 ms). Python-Profil: fast die ganze Zeit nativ in Tk. Native Stichprobe: Jede CoreAnimation-Übergabe rechnet das Fensterbild per Farbraumumwandlung um (`CA::Render::copy_image` → `CGColorTransformConvertUsingCMSConverter` → `vImageConvert_AnyToAny`).

Reine Tk-Probe ohne Glide ([`frame_probe.py`](frame_probe.py), ein Label 14-mal verschoben): Tk 9.0.3 kostet je Bild bei 1280 × 800 im Median 37 ms (bis 70 ms), bei 640 × 400 10,5 ms; **Tk 9.1.0 kostet 5,3 bzw. 1,9 ms**. Glide selbst mit Tk 9.1: Nachlauf nach Abhaken 109–170 ms statt 898–962 ms, nach Anlegen 90–157 statt 194–232 ms.

**Einordnung:** Das gelieferte Mac-Paket 3.49.0 bringt Tk 9.1.0 mit und ist damit schnell. Wer die Python-Fassung mit dem python.org-Python (Tk 9.0.3) startet, hat den langsamen Darstellungsweg. Kein Glide-Fehler; ein Aufschlag in jeder größeren Bildänderung unter Tk 9.0 auf Retina-Mac.

## Umsetzung Befund 1 (Nutzerentscheidung 31.10.2026)

`item_change` erhält den Parameter `lists`: alle Listen, die eine Änderung vorher und nachher berührt. Der Speichervergleich liest dann nur diese (und wie bisher die aktive Liste) neu; ohne Angabe bleibt der Vollvergleich. Die nachträgliche Vereinigung der Punktlisten gilt nur noch für `local=True`. Ausdrückliche Listen setzen neun Einstiege: Anlegen (`add_item`, Zielliste), Löschen (`delete_item`, Quelllisten; der Papierkorb gehört nicht zum Listenvergleich), Verschieben (`move_items_to_list`, Quelle und Ziel), Sortieren, Gruppe auflösen, Zeitplan (listenübergreifend), Erinnerung, Label-Gruppe und Ziehen in der Ordnerübersicht (gezogene Liste). App `f6cd2dd6…`, kein Format- oder Oberflächenwechsel.

**Test:** `test_fortsetzung33311` (P08b) prüft am Suitenende für Anlegen, Verschieben, Löschen, Sortieren, Gruppe auflösen, Zeitplan und Erinnerung die Zahl der gelesenen Listen, die Wiederverwendung einer unberührten Liste und die Gleichheit von `history_snapshot` mit dem Vollvergleich. Gegen die gelieferte App rot (Anlegen liest 8 statt 1 Liste), neu 8 von 8 grün, mit `--baseline-app` gegen die gelieferte Klasse dreimal grün mit je 120 Differenzfällen. **Rote Vorläufe erhalten:** Mitten in der Suite platziert war der Block in 2 von 6 Läufen in der unveränderten Retry-Prüfung (Zeile 122) rot und einmal ohne gesicherten Traceback; die Originalsuite war gegen die neue App 6 von 6 grün. Ursache waren nachlaufende Tk-Aufträge des Testblocks, deshalb steht er jetzt am Ende. Eine zunächst überfällige Testerinnerung wurde in die Zukunft gelegt, damit die Hintergrundzustellung nicht zeitabhängig eingreift.

**Bereich:** 1.082 Fachtests und 16 betroffene Suiten grün, darunter Mutationen, Erinnerungen, Heute/Planen, Tagespaket, Schutzrunde, Wiederanlauf und Datenintegrität.

**Messung vorher/nachher** mit gleichem Bestand (Prüfsumme ohne Zeitstempel identisch), vorher gelieferte Fassung `1fabf883…` aus `07`, nachher neue Quelle, Tk 9.0.3:

| 10.000 Aufgaben | vorher Median/p95 ms | nachher Median/p95 ms | Änderung | Speichern ms |
|---|---|---|---:|---|
| Anlegen | 247 / 265 | 144 / 148 | −42 % | 189 → 89 |
| Löschen | 252 / 259 | 152 / 153 | −40 % | 191 → 92 |
| Verschieben einzeln | 241 / 245 | 154 / 156 | −36 % | 183 → 98 |
| Verschieben mehrfach | 263 / 277 | 170 / 180 | −35 % | 186 → 96 |
| Abhaken (unverändert) | 140 / 145 | 141 / 145 | ±0 % | 85 → 85 |

Bei 1.000 Aufgaben −17 bis −36 %. [Rohwerte](ergebnis.json).

**Eingefrorener Tk-9.1-Volllauf** mit `--zugang-nativ` auf App `f6cd2dd6…`: 126 von 126 Schritten grün (21:53–22:23), alle 108 Integrationssuiten, 1.082 Fachtests, native Zugangsbindungen, Showcase, Analysen, Reproduktionen; Quelle unverändert, Prüfkopie gleich (2.140 Dateien). Belege lokal `13_TK-Test-Umgebung/Macbook-M2/t1031-215331`.

**Lieferung offen:** `07_Python-Versionen` und das Mac-Paket tragen weiter `1fabf883…`; der neue Stand ist nicht geliefert (Lieferabgleich bei Codex).

## Verlaufsabgleich ohne unveränderte Punkte

Profil des Speicherwegs bei 10.000 Aufgaben: größter Einzelposten war `history_events` mit rund 74 ms je Speicherung, eine Feldschleife über alle Punkte. Unveränderte Punkte werden jetzt übersprungen: dasselbe Objekt aus einem wiederverwendeten Vergleichsteil oder gleiche Liste, gleicher Elternpunkt und gleiche Werte. Dann kann weder „verschoben“ noch ein Feldereignis entstehen; die erzeugten Ereignisse sind unverändert. Speicherung im Profil 228 → 152 ms.

**Prüfung:** `test_fortsetzung33311` vergleicht mit `--baseline-app` jetzt auch die Verlaufsereignisse jedes WA-36-Wegs mit der gelieferten Klasse und verlangt „created“/„moved“/„trashed“; dreimal grün, dazu 120 Differenzfälle. 1.082 Fachtests und 28 Verlaufs-/Bereichssuiten grün. Eingefrorener Tk-9.1-Volllauf auf App `28f02f74…` 126 von 126 grün (lokal `t1031-224726`).

**Gesamt gegen die gelieferte Fassung** (gleicher Bestand, Tk 9.0.3), 10.000 Aufgaben: Anlegen 247 → 124 ms (−50 %), Löschen 252 → 128 ms (−49 %), Verschieben 241 → 135 ms (−44 %), mehrfach 263 → 152 ms (−42 %), Abhaken 140 → 124 ms (−11 %). Bei 1.000 Aufgaben −10 bis −39 %.

## Grenzen

Ein Gerät, eine Fenstergröße, künstliche Daten. Keine Messung unter Windows/Linux, kein Vergleich vor/nach einer Optimierung. WA-36 bleibt offen (übrige Wege und gegebenenfalls Umsetzung von Befund 1); Nachlauf- und Speicherzahlen sind kein allgemeiner Leistungsnachweis.
