# Apple Angaben für Glide – Arbeitsstand

Arbeitsstand: 21.09.2026 · Glide 3.26.0 · Quellenabruf: 04.09.2026. Die Store-Vorgaben unten sind auf Grundlage von Glide 3.14.0 / Aufgabenformat 14 erhoben.

**Historische Store-Recherche.** Der aktuelle Entwicklungsstand ist Glide 3.26.0 / Aufgabenformat 17. Die Store-Vorgaben unten sind seit dem 04.09.2026 nicht erneut abgerufen worden und vor einer Einreichung vollständig neu zu prüfen – Version, Datenformat, Textlängen und Bildanforderungen ändern sich unabhängig von Glide.

Vorbereitung für **Direktverteilung** und **Mac App Store**. Der Vertriebsweg
ist offen; ein macOS-Build, signiertes DMG oder getesteter Sandbox-Betrieb liegt
noch nicht vor. Beide Wege werden getrennt geprüft.

## Produktangaben und Store-Texte

| Feld | Inhalt oder Grenze |
|---|---|
| Name | Glide, maximal 30 Zeichen; Reservierung und Markenlage offen |
| Untertitel | Aufgaben und Listen, maximal 30 Zeichen |
| Sprache | Deutsch |
| Kategorie | Produktivität als Vorschlag |
| Beschreibung | maximal 4.000 Zeichen |
| Keywords | maximal 100 **Bytes**, UTF-8-Länge bei Umlauten beachten |
| Neuerungen | maximal 4.000 Zeichen; bei Erstversion nicht erforderlich |
| Altersfreigabe | anhand des aktuellen Fragebogens ermitteln; nicht pauschal 4+ zusagen |
| Systemanforderungen | Mindest-macOS und Architektur erst nach Buildtest freigeben |

Quellen: [Apple App information](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/),
[Apple Platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/).
Ausformulierbare Texte: [Produktdatenblatt](../Produktdatenblatt_3.21.4.md).

## Screenshots und Icons

Mac: **1–10 PNG/JPEG ohne Alpha**, 16:10 in **1280×800, 1440×900,
2560×1600 oder 2880×1800 px**. Auf dem Zielsystem erstellen und relevante
Funktionen im tatsächlich eingereichten Build zeigen.
[Apple Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/)

Klassisches macOS-iconset für `.icns`: 16, 32, 128, 256 und 512 Punkte
jeweils in 1x/2x, maximal 1024×1024 px. Dies ist die archivierte technische
Formatspezifikation, keine vollständige aktuelle Store-Gestaltungsrichtlinie.
Aktuelle Icon-Composer-/Layer-Anforderungen beim gewählten Buildweg zusätzlich prüfen.
[Apple IconSetType](https://developer.apple.com/library/archive/documentation/Xcode/Reference/xcode_ref-Asset_Catalog_Format/IconSetType.html),
[Apple Icon Composer](https://developer.apple.com/icon-composer/).

## App Privacy

Glide selbst überträgt keine Nutzerdaten, enthält kein Netzwerkmodul,
keine Analytics, Werbung oder Anmeldung. Nutzerinhalte werden lokal gelesen
und gespeichert, auch automatisch im eigenen Datenordner. Der vorbereitete
App-Privacy-Status ist daher **Data Not Collected**; vor Einreichung den
tatsächlichen Build einschließlich Bibliotheken und Vertriebsfunktionen prüfen.
Manuell exportierte oder in einen synchronisierten Ordner gespeicherte Daten
können außerhalb von Glide weitergegeben werden.
[Apple App privacy details](https://developer.apple.com/app-store/app-privacy-details/)

## Mac App Store und Sandbox

Mac-App-Store-Apps müssen Sandbox-Anforderungen erfüllen. Für Glide sind
Dateiauswahl, Anhänge, Export, Backup, Öffnen externer Programme und persistenter
Speicher im signierten Sandbox-Build zu testen. Die derzeitige Funktion
`get_app_data_dir()` verwendet den normalen Application-Support-Pfad;
eine korrekte Containerauflösung darf daraus nicht als bereits geprüft abgeleitet werden.
[Apple Review Guidelines 2.4.5](https://developer.apple.com/app-store/review/guidelines/)

User-selected read/write ist ein zu prüfender Entitlement-Bedarf für Exporte
und Backups. Dauerzugriff und Security-Scoped Bookmarks hängen vom tatsächlichen
Ablauf ab. Containerpfade und ein möglicher Wechsel zwischen Direkt- und
Store-Build müssen separat getestet und über Komplettbackup dokumentiert werden.

## Direktverteilung

Für den geplanten vertrauenswürdigen Direktvertrieb: Developer-ID-Signatur,
Hardened Runtime, sicherer Zeitstempel, Notarisierung mit `notarytool`, Stapling
und Gatekeeper-Prüfung. Sandbox und Store-Signierung sind ein anderer Weg.
[Apple Notarizing macOS software](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)

Offen: Developer-Mitgliedschaft/Team-ID, Bundle Identifier, Architektur,
Mindestversion, Copyright, Support-URL, Datenschutz-URL, Preis und Lizenz.
Der Inhaber entscheidet den Vertriebsweg; technische Umsetzung und Nachweise folgen.
