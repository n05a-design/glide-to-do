# Grafik-Master

Arbeitsbereich für Illustrator-/Photoshop-Quellen und freigegebene
Branding-Master. Generierte App-Assets werden erst nach Freigabe in den
Repository-Bereich `assets/` übernommen.

## Struktur

- `Illustrator/`, `Photoshop/`, `Arbeitsdateien/` – Quellen
- `Branding/` – freigegebene Master
- `Archiv/` – überholte Master und deren Arbeitsdateien

## Stand 01.09.2026

Es liegt noch kein freigegebenes Masterpaket vor. Deshalb enthält der
Repository-Bereich `assets/` bewusst keine Platzhaltergrafiken.

Die benötigten Prüfgrößen und die Trennung zwischen Win32-ICO und späteren
Store-Assets stehen im Arbeitsvorbereitungsplan unter `10_Dokumentation/`,
Kapitel 5.

## Hinweis zur Typografie

Seit 2.6.0 nutzt die Hauptüberschrift der Anwendung den schwersten verfügbaren
Schnitt der Systemschrift. Wird später eine eigene Hausschrift eingeführt, muss
deren schwerer Schnitt als eigene Schriftfamilie installiert sein – nur dann
erkennt die Anwendung ihn. Der Familienname wird in der Konstante
`HEADER_FONT_FAMILY` eingetragen.
