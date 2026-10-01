# Arbeitsvorbereitung – aktueller Einstieg

Stand: 05.09.2026 · Glide 3.5.0 · Datenformat 11

Windows-Vollprüfung und Bereinigung abgeschlossen. Aktuelle Quellen:
[Prüfstand](../10_Dokumentation/Windows_Pruefstand_3.5.0.md),
[QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md),
[Produktdatenblatt 3.5.0](../40_Store_Material/Produktdatenblatt_3.5.0.md).
Die nachfolgenden Unterlagen mit Versionsnummer 3.3.0 bleiben historische
Arbeitsgrundlagen; deren Aussagen zum Prüfstand sind keine aktuellen Ergebnisse.

## Historischer Überblick 3.3.0


Stand: 04.09.2026 · Glide 3.3.0 · Datenformat 10

Vorbereitung für Entscheidungen, Recherche, Checklisten und Notizen. Der
kanonische Source liegt unter `../01_Repository/Glide/`; diese Unterlagen
ersetzen weder Code noch den aktuellen QA-Bericht.

| Inhalt | Aktuelle Datei |
|---|---|
| Inhaberentscheidungen | [Offene Entscheidungen](Entscheidungen/Offene_Entscheidungen_3.3.0.md) |
| Manuelle Tests | [Prüfliste](Checklisten/Manuelle_Pruefung_3.3.0.md) |
| Importierbare Zusatzliste | [Veröffentlichungscheckliste](Checklisten/Glide_Veroeffentlichung_Checkliste.txt) |
| Codefakten und Grenzen | [Technische Fakten](Notizen/Technische_Fakten_3.3.0.md) |
| Arbeitsgrundlage als Word | [Dokumentation](../10_Dokumentation/README.md) |

Die früheren Fassungen 2.6.0 und 2.11.0 liegen unverändert im `Archiv/` ihres
jeweiligen direkten Ordners. Jede Fortschreibung erhält vorab eine Archivkopie.

Glide 3.3.0 enthält vier Punktarten, verschachtelte Ordner, Labels, Papierkorb,
Kalender, optionale Uhrzeiten und den Bestandswächter. Seit 3.1.0 bündeln
`item_change`, `sidebar_change` und `run_modal` Änderungen und Dialoge. Seit
3.2.0 entfällt die automatische Übernahme aus früheren Programmnamen. Neu in
3.3.0 ist die Ansicht „Labels“: der gesamte Bestand nach Labels gruppiert,
Punkte in der Labelfarbe, Labelvergabe per Ziehen zwischen den Gruppen.
Dieser Stand ist **nur unter Linux/Xvfb** geprüft; die manuelle Prüfliste ist
entsprechend erweitert.

Release-Hürden bleiben Branding, Build/Installer, Signaturen, Identitäten,
Lizenz und reale Plattformtests. Die Griffrückgabe modaler Dialoge wurde
überarbeitet; das gemeldete Einfrieren ist mangels Reproduktion weiterhin
NICHT VERIFIZIERT. Emoji-Ausnahmen für Gruppe, höchste Wichtigkeit und Beschreibungsmarker bleiben
für Windows-/macOS-Schriftprüfung relevant.

Aktuelle Nachweise: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md),
[Release-Checkliste](../01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md),
[Produktidentität](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md),
[Bestandsanalyse](../01_Repository/Glide/docs/11_BESTANDSANALYSE.md).
