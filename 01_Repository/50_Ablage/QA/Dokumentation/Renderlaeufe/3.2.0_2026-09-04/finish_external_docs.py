"""Source-backed Store notes and final factual corrections, preserving baselines."""
from pathlib import Path
namespace = {'__file__': __file__}
exec(Path(__file__).with_name('update_workspace_docs.py').read_text(encoding='utf-8').split('# Historical version-labelled')[0], namespace)
write, edit, ROOT, QA = (namespace[k] for k in ('write','edit','ROOT','QA'))

write('40_Store_Material/Microsoft/Store_Angaben_Microsoft.md', '''# Microsoft Store Angaben für Glide 3.2.0

Stand und Quellenabruf: 04.09.2026 · Datenformat 10

Arbeitsgrundlage für die Win32-Einreichung als **MSI/EXE**. Ein späterer
MSIX-Vertriebsweg braucht eine eigene Prüfung. Produkttexte sind Entwürfe;
ein Installer oder freigegebener Build existiert noch nicht.

## Angaben aus dem Produkt

| Feld | Vorbereiteter Wert oder Status |
|---|---|
| Produktname | Glide; Reservierung und Markenfreigabe offen |
| Sprache | Deutsch |
| Kategorie | Produktivität als Vorschlag |
| Internet/Konto | für Glide nicht erforderlich |
| In-App-Käufe/Werbung/Telemetrie | nicht im Code vorhanden |
| Texte/Features | [Produktdatenblatt](../Produktdatenblatt_3.2.0.md) |
| Systemanforderungen | Mindestversion und Architektur nach Buildtest festlegen |
| Barrierefreiheit | Tastenkürzel implementiert; vollständiger Tastaturweg und Screenreader ungeprüft |
| Altersfreigabe | aktuellen Fragebogen ausfüllen; Ergebnis offen |

## Texte und Bildmaterial

Beschreibung: maximal **10.000 Zeichen**. Kurzbeschreibung: maximal **1.000**,
Microsoft empfiehlt unter 270. Neuerungen: maximal **1.500**, bei der ersten
Einreichung leer lassen. Bis zu 20 Features, jeweils höchstens 200 Zeichen.
[Microsoft MSI/EXE Store listing](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/add-and-edit-store-listing-info)

**1–10 Screenshots**, mindestens vier empfohlen; quadratische Box Art ist
Pflicht. Die aktuelle MSI/EXE-Seite nennt keine verbindlichen Pixelmaße:
**UNGEKLÄRT**, im tatsächlichen Einreichungsformular prüfen. 1366×768 aus
MSIX-Unterlagen wird nicht als MSI/EXE-Pflicht übernommen. Aufnahmen mit
realem Windows-Build erstellen; Linux-QA-Bilder belegen keine Windows-Darstellung.
[Microsoft MSI/EXE Screenshots](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/screenshots-and-images)

Das Win32-App-Icon wird als Multi-Resolution-ICO mit mindestens
**16, 24, 32, 48 und 256 px** vorbereitet. Store-Logo und ICO sind getrennte
Ableitungen desselben freigegebenen Masters.
[Microsoft App icon construction](https://learn.microsoft.com/en-ie/windows/apps/design/style/iconography/app-icon-construction)

## Installer und Signing

Installer und enthaltene PE-Dateien benötigen vertrauenswürdige digitale
Signaturen. Der Installer muss offline und ohne Nutzerinteraktion funktionieren;
er darf die App-Bestandteile nicht erst herunterladen. Einreichung über eine
versionierte, unveränderliche HTTPS-URL. Returncodes und Silent-Uninstall im
konkreten Build prüfen.
[Microsoft MSI/EXE package requirements](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-package-requirements)

Für einen späteren Inno-Setup-Installer ist
`/VERYSILENT /SUPPRESSMSGBOXES /NORESTART` ein zu prüfender Aufruf, noch kein
erfolgreicher Test. Upgrade und Deinstallation dürfen den Datenordner
`%APPDATA%\\Glide\\` nicht unbeabsichtigt verändern. Signiermaterial bleibt außerhalb des Repositorys.

## Offene Entscheidungen und Reihenfolge

Publisher, Copyright, Support-/Website-/Datenschutz-URL, Lizenz, Preis,
Architektur, AppUserModelID und Installer-AppId durch den Inhaber festlegen.
Dann Build und Clean-Machine-Test, Signaturprüfung, Screenshots, redaktionelle
Freigabe und Einreichung vorbereiten. Store-Texte, Klassifizierungen und URLs
müssen im tatsächlichen Konto erneut geprüft werden; eine E-Mail ersetzt nicht
automatisch ein gefordertes URL-Feld.
''')

write('40_Store_Material/Apple/Store_Angaben_Apple.md', '''# Apple Angaben für Glide 3.2.0

Stand und Quellenabruf: 04.09.2026 · Datenformat 10

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
Ausformulierbare Texte: [Produktdatenblatt](../Produktdatenblatt_3.2.0.md).

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
''')

edit('00_Arbeitsvorbereitung/Notizen/Technische_Fakten_3.2.0.md', [
('**Ausnahme:** `IMPORTANCE_MARKERS[3]` (🚩) und `GROUP_MARKER` (📁) sind noch\nEmoji und liegen außerhalb von `ICONS`. Die Umstellung ist offen', '**Ausnahmen:** `IMPORTANCE_MARKERS[3]` (🚩), `GROUP_MARKER` (📁) und\ndie Beschreibungsmarkierung (📝) sind noch Emoji außerhalb von `ICONS`. Die Umstellung ist offen'),
('die Ursache ist gefunden und beseitigt, der\n  Fehler ließ sich aber nie reproduzieren.', 'die Griffrückgabe wurde überarbeitet, der\n  gemeldete Fehler ließ sich aber nie reproduzieren.'),
('zwei Emoji außerhalb von `ICONS` sind\n  geblieben', 'Emoji-Ausnahmen außerhalb von `ICONS` sind\n  geblieben'),
])
for rel in ['00_Arbeitsvorbereitung/Notizen/Technische_Fakten_3.2.0.md', '00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.2.0.md']:
    p=ROOT/rel;s=p.read_text(encoding='utf-8')
    s += '''

## Belegte Grenzbefunde vom 04.09.2026

Die deklarierten Grenzen sind nicht auf jedem Änderungspfad durchgesetzt:
`sync_item_kind_label` kann ein Systemlabel an 20 Nutzerlabels anhängen und
damit 21 erzeugen. `make_subitem` kann Tiefe 101 erzeugen; die spätere
Normalisierung lehnt diesen Bestand ab. Beide Fälle wurden isoliert reproduziert.
App-Code unverändert; gezielte Behebung und Regression vor Release offen.
Nachweise: `../../01_Repository/Glide/docs/11_BESTANDSANALYSE.md`.
'''
    write(rel,s)

for rel in ['00_Arbeitsvorbereitung/Archiv/README.md','10_Dokumentation/Archiv/README.md','40_Store_Material/Archiv/README.md']:
    p=ROOT/rel
    write(rel, '''# Archiv

Stand: 04.09.2026 · aktive Dokumentation für Glide 3.2.0 / Datenformat 10

Hier liegen unveränderte Vorgänger und Sicherungskopien vor ihrer Fortschreibung.
Historische Versionen, Datenformate und Befunde bleiben im jeweiligen Dokument
erhalten; sie beschreiben keinen aktuellen Freigabestand. Die aktuelle Fassung
liegt im Ausgangsordner. Es wurde keine Datei gelöscht.

Archivierungsgründe und SHA-256-Nachweise der Konsolidierung stehen in
`50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/external_archive_manifest.json`
(Pfad ab Workspace-Wurzel). Die Word-Vorlage und Paketprüfung sind dort zusätzlich
in `docx_revision_manifest.json` dokumentiert.
''')

import json
ledger=namespace['ledger']
(QA/'external_archive_manifest.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
print('Store-Dokumente und Grenzbefunde nachgeführt.')
