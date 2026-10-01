# Glide 3.4.0 – Persönliche Startseite und Oberfläche

Stand: 05.09.2026 · Aufgabendatenformat 10

Die startbare Einzeldatei liegt im äußeren Projektordner unter
`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.4.0.pyw`.
Der Quellstand ist weiterhin `src/glide/app.pyw`. Die Version 3.3.0 bleibt erhalten.

## Was sich in der Bedienung ändert

**Startseite:** Oben in der linken Leiste ist ein neuer Einstieg. Unter
**Bearbeiten → Einstellungen** lassen sich Begrüßungsname, persönliches
Textlogo aus 1–3 Buchstaben oder Ziffern, die Startansicht und die Anzeige
der Bestandszahlen einstellen. Das Logo ist ein Monogramm und bleibt damit
bei der Vorgabe, in der Oberfläche Textzeichen zu verwenden.

Die Startseite zeigt offene und erledigte Aufgaben, heute fällige und
überfällige Aufgaben, die dazugehörigen heute fälligen Listen und die sechs
zuletzt tatsächlich bearbeiteten Listen. Ein unveränderter Speichervorgang
oder der bloße Aufruf einer Liste zählt nicht als Bearbeitung. Die Historie
beginnt mit dieser Version. Ein Tageswechsel aktualisiert die Anzeige.
Das sind Zahlen aus dem vorhandenen Bestand, keine Nutzungsdauer oder Telemetrie.

**Vorlagen:** Tagesplanung, Projektstart und Einkauf legen jeweils eine neue,
frei bearbeitbare Liste mit neuen Punkt-IDs an. Mehrfaches Anlegen erzeugt
unabhängige Listen mit unterscheidbaren Namen. Rückgängig nimmt die Neuanlage zurück.

**Seitenleiste:** Titel stehen links, Zahlen in einer eigenen rechten Spalte.
Ordner summieren die Aufgaben aller enthaltenen Listen und Unterordner;
Überschriften und Gruppen zählen nicht als Aufgaben. Der Einzug ist pro Ebene
12 statt 20 Pixel. Lange Titel nutzen die tatsächlich verfügbare Breite.

**Aufgabenliste:** Zwischen der Titelzelle und sichtbaren Metadaten liegen
mindestens 24 Pixel. Der Zusatzraum in Fälligkeits- und Labelzellen sinkt von
30 auf 12 Pixel; die rechte Abstandsspalte von 16 auf 4 Pixel. Beim Verkleinern
weichen weiterhin zuerst die Labels, danach die Fälligkeit.

**Eingaben:** Farbnamen erscheinen sowohl in der Auswahl als auch im gewählten
Feld in ihrer Farbe. Dasselbe gilt für die Fähnchen der Wichtigkeit. Hinter
Labelchips beginnt die Auswahl-/Hoverfläche; der Chip selbst bleibt unverändert.

**Artlabels:** Long-Task und Überschrift stehen auch in der erweiterten Eingabe
zur Verfügung. Ein Klick wechselt die Punktart direkt in derselben Maske.
Long-Task macht den Titel mehrzeilig; Überschrift blendet Wichtigkeit und
Fälligkeit aus. Beim Hin- und Herwechsel bleibt der Entwurf erhalten; beim
Speichern einer Überschrift entfallen Status, Fälligkeit und Wichtigkeit gemäß
dem bestehenden Datenmodell. Die beiden Artlabels schließen sich gegenseitig aus.
Speichern/Anlegen und Abbrechen bleiben fest am unteren Fensterrand.

**Hilfe und Meldungen:** Tastenkürzel, Über Glide, Warnungen und Rückfragen
übernehmen das App-Theme. Tastenkombinationen stehen links fett, die Erklärung
rechts. Lange Inhalte sind scrollbar. Über Glide enthält eine persönliche
Danksagung, drei Sätze zur Motivation und Shaye.de / mailme@shaye.de.

## Symbolvergleich

Die Spalte „3.4.0“ bezeichnet die eingebaute Auswahl. Alternativen sind Vorschläge.
Alle Einträge sind Schriftzeichen; kein Iconpaket oder Bild ist erforderlich.

| Verwendung | Vorher (3.3.0) | 3.4.0 | Weitere Möglichkeit |
|---|---|---|---|
| Eingang | ↓ | ▼ | ⇩, ▾ |
| Papierkorb | × | 🗑 | ⌧, × als neutraler Ersatz |
| In Bearbeitung | ◐ | ◐ | ◉, ≋ |
| Labels | ◈ | ◈ | ◆, ◇ |
| Verspätet | ‼ | ‼ | !, !! |
| Fälligkeit/Kalender | ▦ | ▦ | ▣, □ |
| Wichtigkeit niedrig | ⚐ | ⚐ | ! |
| Wichtigkeit mittel | ⚑ | ⚑ | !! |
| Wichtigkeit hoch | 🚩 | ⚑⚑ | !!! |
| Gruppe | 📁 | ▸ | ▹, ▰ |
| Beschreibung | 📝 | ≡ | ¶, § |
| Anhang | ⊕ | ⊕ | + |
| Startseite | – | ⌂ | ◆ |
| Theme dunkel/hell | ☾ / ☀ | ☾ / ☀ | ◐ / ◑ |

Das Papierkorbzeichen U+1F5D1 hat standardmäßig Textdarstellung. Unicode führt
es auch mit expliziter Textvariante; Windows/Tk 8.6 reserviert für den dazu
gehörigen Variationsselektor zusätzlichen Leerraum. Glide verwendet deshalb
das Grundzeichen. Die genaue Form und verfügbare Schrift unterscheiden sich
zwischen Betriebssystemen. Eine pixelgleiche Darstellung wird nicht zugesagt.
Quelle: [Unicode-Zeichenliste und Darstellungsvarianten](https://unicode.org/emoji/charts/emoji-variants.html).

## Pflege und Speicherung

Die Symbolauswahl steht zentral in `ICONS`. `PALETTE` definiert feste Farben;
`THEMES` ordnet sie Verwendungen wie Bestätigen, Warnen oder hoher Wichtigkeit zu.
Layoutabstände besitzen ebenfalls benannte Konstanten.

Aufgaben, Listen und Komplettbackups bleiben im Datenformat 10. Persönliche
Angaben bleiben gerätespezifisch in `settings.json`. Vor der ersten Umstellung
wird die alte Einstellung als `settings.before-v1.json` gesichert. Persönliche
Angaben sind nicht Bestandteil des Aufgaben-Komplettbackups.

Neue TXT-Dateien verwenden die neuen Gruppen-/Wichtigkeitszeichen. Die Parser
lesen alte TXT-Dateien weiterhin. Für den Austausch mit älteren Glide-Versionen
ist das Format-10-Komplettbackup geeignet; deren TXT-Parser kennen neue Zeichen
möglicherweise noch nicht.

## Prüfung und Grenzen

Fünf automatisierte Suiten prüfen den Bestand, Datenintegrität, die neuen
Eingaben, die Startseite sowie Dialoge in beiden Themes. Windows-Sichtnachweise
entstehen aus eigenen Testfenstern. Details und Ergebnisse stehen im
[QA-Bericht](07_QA_BERICHT.md).

Native Dateiauswahlfenster gehören zum Betriebssystem und können dessen
Darstellung statt des Glide-Themes verwenden. macOS/Linux, weitere
Anzeigeskalierungen, mehrere Monitore und längere reale Mausbedienung benötigen
weiterhin eine eigene Prüfung. Es gibt keine neue Laufzeitabhängigkeit.
