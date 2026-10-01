# 50_Ablage

Stand 25.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Dieser Bereich nimmt projektbegleitende Arbeits- und Prüfarbeitsstände auf, die
weder produktiver Source noch dauerhaft eingefrorenes Archivmaterial sind.

## Abgrenzung

- `01_Repository/Glide` bleibt die einzige technische Source of Truth für
  Sourcecode, Tests und code-nahe Dokumentation.
- `07_Python-Versionen` bleibt die nachvollziehbare Historie freigegebener
  Einzeldateien.
- `10_Dokumentation` enthält die aktuelle Markdown-Dokumentation; die früheren Word-Berichte liegen dort im `Archiv/`.
- Archiviert wird dezentral: Jeder Ordner hat einen eigenen Unterordner
  `Archiv/` für überholte Stände genau dieses Ordners. Ein zentrales
  `100_Archiv` gab es bis 3.1.0; es wurde aufgelöst.
- `50_Ablage` enthält QA-Renderläufe, historische Screenshots und sonstige
  projektbegleitende Zwischenstände.

Produktive Dateien, Nutzerdaten, Signing-Secrets und Zertifikate gehören nicht
in diesen Ordner.

Der aktuelle App-Stand ist Glide 3.30.0. Die hier abgelegten Renderläufe,
Screenshots und Bestandsanalysen bleiben datierte historische Nachweise. Der
maßgebliche Prüfstatus steht im aktuellen `01_Repository/Glide/docs/07_QA_BERICHT.md`;
alte QA-Ordner belegen ausschließlich ihren jeweiligen Stand.

## Historischer QA-Bestand und Stand 04.09.2026

Unter `QA/Dokumentation/Renderlaeufe/` liegen neun Läufe zu den
Dokumentversionen 2.5.1 und 2.5.2 mit rund 70 MB. Fünf davon sind praktisch
identische Zwischenstände desselben Dokuments. Die Renderläufe bleiben
vollständig erhalten. Zur Sichtung genügt jeweils der letzte Lauf einer
Dokumentversion; vorhandene historische Archivzuordnungen bleiben bestehen.

Das SHA-256-Manifest `QA/Dokumentation/MANIFEST_SHA256.csv` beschreibt den
Gesamtbestand. Nach einer Verschiebung muss es neu erzeugt werden, sonst
verweist es auf Pfade, die es nicht mehr gibt. Der neue Dokumentlauf liegt unter
`QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/`; alte Renderläufe bleiben
unverändert als historische Nachweise erhalten.

## Übernahme 3.21.4

[Ablage- und Prüfnachweis](Archiv/Werkzeuge_3.21.4/Ablageprotokoll_2026-09-15.md) · [Originalpaket](Archiv/Uebertragungspakete/glide-3.21.4-ablagepaket.zip). Die Originalwerkzeuge, Nacharbeiten und Prüfsummen liegen zusammen im Werkzeugarchiv. Das QA-Dateimanifest wurde nach der Archivierung aktualisiert.
