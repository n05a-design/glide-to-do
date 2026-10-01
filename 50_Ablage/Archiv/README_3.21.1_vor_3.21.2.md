# 50_Ablage

Dieser Bereich nimmt projektbegleitende Arbeits- und Prüfarbeitsstände auf, die
weder produktiver Source noch dauerhaft eingefrorenes Archivmaterial sind.

## Abgrenzung

- `01_Repository/Glide` bleibt die einzige technische Source of Truth für
  Sourcecode, Tests und code-nahe Dokumentation.
- `07_Python-Versionen` bleibt die nachvollziehbare Historie freigegebener
  Einzeldateien.
- `10_Dokumentation` enthält die aktuelle Word-Arbeitsgrundlage und ihre historischen Fassungen.
- Archiviert wird dezentral: Jeder Ordner hat einen eigenen Unterordner
  `Archiv/` für überholte Stände genau dieses Ordners. Ein zentrales
  `100_Archiv` gab es bis 3.1.0; es wurde aufgelöst.
- `50_Ablage` enthält QA-Renderläufe, historische Screenshots und sonstige
  projektbegleitende Zwischenstände.

Produktive Dateien, Nutzerdaten, Signing-Secrets und Zertifikate gehören nicht
in diesen Ordner.

Der aktuelle App- und QA-Stand ist Glide 3.14.0. Die hier abgelegten Renderläufe,
Screenshots und Bestandsanalysen bleiben datierte historische Nachweise; die
laufende Prüfung liegt unter `01_Repository/Glide/tests/qa-3.14.0/`.

## Historischer QA-Bestand und Stand 04.09.2026

Unter `QA/Dokumentation/Renderlaeufe/` liegen neun Läufe zu den
Dokumentversionen 2.5.1 und 2.5.2 mit rund 70 MB. Fünf davon sind praktisch
identische Zwischenstände desselben Dokuments. Für den Nachweis genügt der
letzte Lauf je Dokumentversion; die übrigen gehören in den dort angelegten
Ordner `Archiv/`.

Das SHA-256-Manifest `QA/Dokumentation/MANIFEST_SHA256.csv` beschreibt den
Gesamtbestand. Nach einer Verschiebung muss es neu erzeugt werden, sonst
verweist es auf Pfade, die es nicht mehr gibt. Der neue Dokumentlauf liegt unter
`QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/`; alte Renderläufe bleiben
unverändert als historische Nachweise erhalten.
