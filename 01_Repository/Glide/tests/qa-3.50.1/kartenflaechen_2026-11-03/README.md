# Themenfarbe in Seitenleiste und Inhaltskarte

Prüfdatum 03.11.2026 · Kandidat 3.50.1 · Windows x64, Python 3.14.7, Tk 9.1.0 · Basis `1ba516a8`.

## Reproduktion und Korrektur

Der vorhandene Fall `beta350` war vor der Änderung grün. Die neue echte UI-Gegenprobe `kartenflaechen` wurde auf dem unveränderten Appcode rot: Wechsel hell/Fensterfläche → Braun, `system_listbox`, abgeleiteter Stil `FrostEDE9E7.System.Treeview`, Hintergrund `#EDE9E7` statt Kartenweiß `#FFFFFF`. Die Farbzuordnung hatte die vorher identische Grund-/Kartenfarbe verwechselt und einen dauerhaften abgeleiteten Baumstil angelegt. Beim Themenwechsel wird nun der reguläre Baumstil wiederhergestellt; seine Kartenrolle ist maßgeblich. Tatsächliche Verlaufstönungen werden weiterhin separat abgeglichen.

## Prüfung

- `test_arbeitsmodi.py --fall kartenflaechen`: grün, 59 Farb-/Design-/Ansichtswechsel einschließlich Neustart. Standard, Minimal und Glas jeweils hell/dunkel, sechs Bäume, System-Symbolfläche, beide Karten, Liste/Tabelle/Pinnwand sowie echter Glasverlauf → feste Farbe.
- `test_arbeitsmodi.py --fall beta350`: grün; Hintergrundpalette in zehn Designs, gespeicherte Wahl/Neustart, drei Fenstergrößen, Seitenleiste und Blockziehen/Undo/Redo/Abbruch/Schreibschutz.
- `test_arbeitsmodi.py --fall werkzeugzeile`: grün; zwölf Geometriemessungen, Abstand, Umschalter, Pinnwand und Seitenfuß.
- Strenge CI-Grundstufe grün: 19/19 Schritte, 242 Werkzeugtests (ein Skip), zweimal 1.122 Fachtests, Appstart und strenger Python-Liefervergleich ohne Abweichung. Maschinenlesbare Ergebnisse in [ergebnis.json](ergebnis.json).

Native Windows-Fensterbilder mit synthetischen Daten wurden lokal aufgenommen und vom Agenten auf weiße bzw. dunkelgraue Karten vor farbigem Grund geprüft. Rohprotokolle und Bilder bleiben lokal. Automatisierte Farb-/Geometrieprüfung ersetzt keine menschliche DPI-/Mehrmonitorabnahme.

## Liefer- und Abnahmegrenze

Quelle und Python-Fassung tragen 3.50.1. Der Datenformatstand bleibt 26. Neue eigenständige Windows-/Mac-Pakete, Remote-Vollmatrix und menschliche Sichtprüfung sind hier nicht nachgewiesen. Historische Nachweise bleiben in ihren Versionsordnern. Kein automatischer main-Merge oder Release durch diese Korrektur.

Versionspflege: Nummern/aktuelle Dokumentköpfe und synthetische Fixtures auf 3.50.1 nachgeführt. Nach der bestehenden Sieben-Versionen-Regel 79 versionierte 3.44-Belege aus dem aktiven Baum genommen, vorher bytegleich lokal gesichert; unversionierte Belege unangetastet. Python-Quellabgleich: 92 Code-Dateien und 167 Ressourcen ohne Abweichung.

CI-Vorlauf war wegen relativer Verweise auf die nach Aufbewahrungsregel entfallenen 3.44-Nachweise rot; keine zusätzliche Appregression. Historische Verweise an den gepflegten Quellen auf die lokal geprüfte unveränderliche Git-Fassung `1ba516a8` umgestellt; danach komplette Grundstufe grün. Rohprotokolle bleiben lokal.
