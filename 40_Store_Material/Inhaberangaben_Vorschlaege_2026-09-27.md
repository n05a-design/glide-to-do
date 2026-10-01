# Inhaberangaben – Vorschläge zur Bestätigung

Stand 27.09.2026 · Glide 3.30.0 · Entwurf, nicht freigegeben

Der Inhaber hat am 27.09.2026 um Vorschläge für die offenen Zeilen im
[Produktregister](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md)
gebeten. Hier stehen sie. **Keine davon gilt, bevor der Inhaber sie bestätigt.**
Erst danach übernimmt das Register sie. Bis dahin dürfen sie in keine Build-
oder Store-Konfiguration einfließen (Regel im Register).

## 1. Entschieden am 27.09.2026 (E-10)

| Feld | Entscheidung |
|---|---|
| Vertriebsweg | zuerst Direktvertrieb über die eigene Website; Stores später |
| macOS | Developer-ID-Signatur, Notarisierung, `.app` als Ordnerbundle (keine Einzeldatei), DMG |
| Windows | Installer (Inno Setup) mit Code-Signing-Zertifikat |
| Windows-Architektur | x64 |
| macOS-Architektur | Apple Silicon (arm64); Universal 2 nur, wenn Intel-Macs gebraucht werden |
| Laufzeit des Builds | Python 3.14 mit Tk 9 (E-03) |

Voraussetzungen, die nur der Inhaber schaffen kann:

- ein Apple-Developer-Konto mit Developer-ID-Zertifikat;
- ein Code-Signing-Zertifikat für Windows.

## 2. Vorschläge (E-11)

| Feld | Vorschlag | Begründung |
|---|---|---|
| Copyright-Zeile | `© 2026 Tim von Trostorff` | Herausgeber laut Register; Jahr der ersten Veröffentlichung |
| Datenschutz-URL | `https://shaye.de/glide/datenschutz` | unter der eingetragenen Website; beide Stores verlangen eine erreichbare Seite |
| Sicherheitskontakt | `mailme@shaye.de` (Betreff „Glide Sicherheit“) | dieselbe Adresse wie der Support, bis ein eigenes Postfach sinnvoll ist |
| Inno-Setup-AppId | `{0A756FC5-5DDB-4B0F-9EC8-B4AA85753597}` | einmal erzeugt am 27.09.2026; nach Bestätigung **nie mehr ändern** |
| macOS-Mindestversion | folgt aus dem Python-3.14-Installer von python.org; wird beim ersten Release-Build gemessen und hier eingetragen | Die Mindestversion bestimmt die mitgelieferte Laufzeit, nicht Glide |
| Logo | PNG 1024 × 1024, transparenter Grund, aus `Glide-Logo.af`, abgelegt in `20_Grafik_Master` | Grundlage für `.icns`, `.ico` und die Store-Symbole |
| Markenprüfung „Glide“ | Fachanwalt für Markenrecht beauftragen | lässt sich durch eigene Recherche nicht ersetzen |

## 3. Entwurf der Datenschutzseite

Ein Textvorschlag für `shaye.de/glide/datenschutz`. Er beschreibt, was Glide
technisch tut. Er ist **keine Rechtsberatung** und sollte vor der
Veröffentlichung rechtlich geprüft werden.

> **Datenschutz bei Glide**
>
> Glide ist eine lokale Anwendung. Deine Aufgaben, Notizen, Seiten,
> Zeichnungen, Bilder und Einstellungen bleiben auf deinem Gerät, in dem
> Datenordner, den du selbst wählst.
>
> - Glide hat kein Benutzerkonto und keinen Server.
> - Glide sendet keine Nutzungsdaten, keine Absturzberichte und keine
>   Telemetrie.
> - Glide stellt von sich aus keine Verbindung ins Internet her. Nur ein Link,
>   den du selbst anklickst, öffnet deinen Browser.
> - Liegt dein Datenordner in einem Cloud-Ordner (etwa OneDrive oder iCloud),
>   gelten für diese Kopie die Bedingungen des jeweiligen Anbieters.
> - Systemmitteilungen, falls eingeschaltet, zeigt dein Betriebssystem an. Sie
>   enthalten den Titel der fälligen Aufgabe.
>
> Herausgeber: Tim von Trostorff · Kontakt: mailme@shaye.de

## 4. Nach der Bestätigung

1. Produktregister: die Zeilen von „offen“ auf die bestätigten Werte setzen,
   mit Datum.
2. `SECURITY.md`: den Sicherheitskontakt eintragen.
3. Produktdatenblatt: Copyright und Datenschutz-URL übernehmen.
4. Paketierung: AppId in das Inno-Setup-Skript, sobald es entsteht.
