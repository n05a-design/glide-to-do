# Offene Entscheidungen – Glide 3.23.0

Stand: 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16

Fragen, die nicht im Code beantwortet werden können, weil sie Geschäft, Recht
oder Produktausrichtung betreffen. Unverändert übernommene Punkte aus 3.21.4
sind als solche gekennzeichnet.

## Neu mit 3.23.0

| Frage | Zusammenhang | Wer entscheidet |
|---|---|---|
| **Freies Zeichnen auf der Pinnwand** | Ein Strich ist kein Aufgabenpunkt. Er bräuchte eine zweite Datenhaltung auf der Fläche – mit eigenen Regeln für Export, Backup und Formatwechsel. Bisher gilt: eine Aufgabe, viele Ansichten. | Inhaber |
| **Notizzettel ohne zugehörigen Punkt** | Dieselbe Frage. In 3.23 ist eine Notiz ein Long-Task und damit ein echter Punkt. | Inhaber |
| **Gerichtete Abhängigkeiten** | Die Verbindungen aus 3.23 sind ungerichtet. „A muss vor B fertig sein“ verlangt Richtung, eine Prüfung auf Kreise und eine Darstellung in Listen- und Tabellenansicht. | Inhaber |
| **Anbindung an einen KI-Dienst** | 3.23 tauscht Dateien aus. Eine direkte Anbindung hieße: Netzzugriff, Schlüsselverwaltung, Datenschutzfolgeabschätzung und die Frage, welche Inhalte das Gerät verlassen. Das widerspricht nicht der Produktgrenze, ist aber eine ausdrückliche Entscheidung. | Inhaber |
| **Name der Markenfigur** | Ein Name macht sie zur Marke und bindet sie an die offene Markenprüfung. | Inhaber |
| **Soll der Begleiter sprechen oder nur zeigen** | Eine Figur ohne Text braucht keine Tonalität und altert langsamer. | Inhaber |
| **Zeiterfassung je Punkt** | Geplante gegen tatsächliche Dauer. Technisch klein, aber sie verändert, was Glide über die eigene Arbeit aussagt. Die Regel „keine Produktivitätsbewertung“ müsste ausdrücklich bestätigt werden. | Inhaber |

## Unverändert offen aus 3.21.4

| Feld | Stand |
|---|---|
| Publisher / Herausgebername | offen |
| Copyright-Zeile | offen |
| Datenschutz-URL | offen, für beide Stores Pflicht |
| Lizenzmodell | offen, rechtlich prüfen lassen |
| Preis und Monetarisierung | offen |
| Windows-Zielarchitektur | offen, Empfehlung x64 |
| Windows AppUserModelID | folgt aus Publisher und Produktname |
| Inno-Setup-AppId | einmalige GUID, danach nie ändern |
| macOS Bundle Identifier | Form `de.<domain>.glide` |
| macOS Mindestversion und Architektur | offen |
| Sicherheitskontakt | offen |
| Markenprüfung „Glide“ | offen, Fachanwalt |

## Nicht mehr offen

| War offen | Entschieden in 3.23.0 |
|---|---|
| Wie Design, Farbmodus und Materialoptik zusammenpassen | Eine Designauswahl mit sieben Einträgen; Registry erweiterbar |
| Ob das Austauschformat menschen- oder maschinenlesbar sein soll | Beides mit Rangfolge: JSON verbindlich, Markdown als Zweitweg |
| Ob Pinnwandverbindungen Linien oder Beziehungen sind | Beziehungen zwischen Punktkennungen, ungerichtet |
| Welches Assetformat der Arbeitsbegleiter braucht | PNG in festen Größen, Vektorquelle als Master, keine Animation als GIF |
