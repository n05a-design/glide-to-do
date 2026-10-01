# Microsoft Store Angaben für Glide – Arbeitsstand

Arbeitsstand: 21.09.2026 · Glide 3.26.0 · Quellenabruf: 04.09.2026. Die Store-Vorgaben unten sind auf Grundlage von Glide 3.14.0 / Aufgabenformat 14 erhoben.

**Historische Store-Recherche.** Der aktuelle Entwicklungsstand ist Glide 3.26.0 / Aufgabenformat 17. Die Store-Vorgaben unten sind seit dem 04.09.2026 nicht erneut abgerufen worden und vor einer Einreichung vollständig neu zu prüfen – Version, Datenformat, Textlängen und Bildanforderungen ändern sich unabhängig von Glide.

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
| Texte/Features | [Produktdatenblatt](../Produktdatenblatt_3.21.4.md) |
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
`%APPDATA%\Glide\` nicht unbeabsichtigt verändern. Signiermaterial bleibt außerhalb des Repositorys.

## Offene Entscheidungen und Reihenfolge

Publisher, Copyright, Support-/Website-/Datenschutz-URL, Lizenz, Preis,
Architektur, AppUserModelID und Installer-AppId durch den Inhaber festlegen.
Dann Build und Clean-Machine-Test, Signaturprüfung, Screenshots, redaktionelle
Freigabe und Einreichung vorbereiten. Store-Texte, Klassifizierungen und URLs
müssen im tatsächlichen Konto erneut geprüft werden; eine E-Mail ersetzt nicht
automatisch ein gefordertes URL-Feld.
