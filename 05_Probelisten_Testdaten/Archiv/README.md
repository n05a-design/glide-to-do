# Archiv – Probelisten und Testdaten

Ablage für überholte Stände **dieses Ordners**. Der jeweils aktuelle Stand
bleibt eine Ebene höher liegen; hier landet, was er ersetzt hat.

## Hierher gehört

Testbestände, die den aktuellen Funktionsumfang nicht mehr abbilden. Stand
01.09.2026 sind das die Dateien ohne Versionsangabe im Namen – sie stammen aus
der Zeit vor 2.5.0 und kennen weder Gruppen noch Fälligkeiten, Beschreibungen,
Farben oder Anhänge.

## Vorsicht bei einer Datei

`probelisten_5_listen_liste_speicher.json` ist der einzige eingecheckte Bestand
im Datenformat 2. Gegen ihn wird die Migration weiterhin geprüft – eine Kopie
liegt bereits als Fixture unter
`01_Repository/Glide/tests/fixtures/legacy_v2/`. Das Original hier darf ins
Archiv, aber nicht gelöscht werden.

## Hierher gehört nicht

Der Satz `*2.6.0*`. Er ist der aktuelle Prüfbestand für manuelle Tests.

## Abgrenzung zu 100_Archiv

`100_Archiv` ist für dauerhaft eingefrorene Gesamtstände des Projekts
reserviert – ganze Altversionen des Arbeitsbereichs. Dieser Ordner hier nimmt
dagegen nur überholte Stände seines eigenen Ordners auf. Beides nebeneinander
zu führen ist Absicht: der Rückgriff auf eine einzelne Vorgängerdatei soll
nicht bedeuten, einen ganzen Altbestand durchsuchen zu müssen.

## Pflegeregel

Nichts wird gelöscht, nur verschoben. Die Datei behält ihren Namen samt
Versionsangabe, damit die Reihenfolge ohne Zeitstempel lesbar bleibt.
