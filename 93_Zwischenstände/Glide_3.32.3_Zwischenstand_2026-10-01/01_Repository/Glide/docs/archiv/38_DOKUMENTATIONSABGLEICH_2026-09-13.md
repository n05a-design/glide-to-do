# Dokumentationsabgleich – 13.09.2026

Stand 13.09.2026 · Glide 3.14.0 · Aufgabenformat 14 · Einstellungen 2 · Vorlagenformat 2

Anlass war ein Abgleich aller aktiven Dokumente gegen den tatsächlichen Quell- und
Prüfstand. Programmcode, Nutzdaten, Beispielbackups, Ressourcen und die startbare
Arbeitskopie wurden nicht verändert. Es wurde keine Datei gelöscht.

## Prüfstand richtiggestellt

Ein erster Vollmodus-Lauf vom 13.09.2026 endete mit Exitcode 1. Ursache war die
Erwartungsliste des Tests, nicht die Anwendung: `FORM_KEYS` führte noch den
3.13-Feldsatz, während die Punktmaske bereits `planned_date` und `estimated_minutes`
zurückgibt. Nach Ergänzung der Liste bestand der Wiederholungslauf mit Exitcode 0
([Abschlusslauf](../../../50_Ablage/QA/qa-3.14.0/abschluss/ergebnis.json)): achtzehn Suiten, zwei
statische Analysen sowie Beispiel- und Releaseabgleich; Screenshots und Sichtprüfung
blieben plattformbedingt übersprungen. Automatisiert ist 3.14.0 damit abgenommen.

Das Faktenblatt `00_Arbeitsvorbereitung/Notizen/Technische_Fakten_3.14.0.md` hatte den
grünen Achtzehn-Suiten-Nachweis vorweggenommen, bevor er vorlag; die Angabe ist jetzt
durch den tatsächlichen Lauf gedeckt. Der aktuelle Stand steht im
[QA-Bericht](07_QA_BERICHT.md).

## Berichtigte Angaben

| Dokument | Vorher | Jetzt |
|---|---|---|
| [00_INDEX.md](00_INDEX.md) | Kopfzeile „Glide 3.13.0 · Aufgabenformat 13“, Einstiege als 3.13.0 bezeichnet | 3.14.0 / Format 14; Bearbeitungstag und Aufwand als erster Einstieg |
| [01_PRODUCT_CONSTRAINTS.md](01_PRODUCT_CONSTRAINTS.md) | „Aufgabenformat 14 bleibt unverändert“ im Absatz zu 3.11–3.13 | Format 13 blieb dort unverändert; Format 14 kam mit 3.14 |
| [07_QA_BERICHT.md](07_QA_BERICHT.md) | Gesamtlauf als noch auszuführen angekündigt | tatsächliches Ergebnis, Ursache, Abnahmestand und Reproduktionsbefehl |
| [12_ABSCHLUSSBERICHT.md](12_ABSCHLUSSBERICHT.md) | „aktueller Arbeitsstand ist Glide 3.13.0“; Verweis auf Arbeitskopie v3.11.0 | Arbeitsstand 3.14.0; Verweis auf v3.14.0 |
| [25_FEATURE_ABGLEICH_3.7.0.md](archiv/25_FEATURE_ABGLEICH_3.7.0.md) | Abschnitt „Aktueller Stand 3.13.0“; 3.7-Prüflauf als „aktuell“ geführt | „Ausbau bis 3.14.0“; der Elf-Suiten-Lauf ist als 3.7-Prüfstand gekennzeichnet |
| `00_Arbeitsvorbereitung/README.md` | Linktexte und Linkziele wiesen auf verschiedene Versionen | Linktext und Ziel stimmen überein |
| `00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_3.14.0.md` | Bearbeitungstermin und Aufwand als offene Stufe ohne Zusage für 3.14.0 | in 3.14.0 umgesetzt; nächste offene Stufe ist das vollständige App-Backup |
| `00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md` | ohne Prüfstandsangabe | nennt den offenen Gesamtlauf und die offene Plattformabnahme |

## Ablage

Neun Vorfassungen wurden vor der Bearbeitung unverändert in den `archiv/`-Unterordner
desselben Ordners kopiert, benannt nach der Version, die sie beschreiben. Fünf
3.13-Dokumente lagen zusätzlich zu ihrer bereits vorhandenen, bytegleichen
Archivfassung noch in aktiven Ebenen; sie wurden in einen Unterordner
`Archiv/Dubletten_2026-09-13/` des jeweiligen Ordners verschoben. Betroffen waren
Technische Fakten, Manuelle Prüfung, Offene Entscheidungen, Vorlagen-Praxisanleitung
und Produktdatenblatt der Version 3.13.0. Kein aktives Dokument verweist auf diese
Pfade.

[Archivmanifest mit Quelle, Ziel und SHA-256](../../../50_Ablage/QA/qa-3.14.0/dokumentationsabgleich-2026-09-13/archiv_manifest.json).

## Offen

Die native Sichtabnahme auf macOS und Windows, DPI- und Mehrmonitorprofile,
Screenreader, Langzeitbetrieb sowie Installer und Signierung bleiben offen. [Release-Checkliste](10_RELEASE_CHECKLIST.md) ·
[Vorheriger Abgleich](30_DOKUMENTATIONSABGLEICH_2026-09-12.md).
