# Glide-Funktionsvorschau

Beispiel-Sicherung für Glide 2.11.0. Sie zeigt jede Funktion an Inhalten, die
so auch in einem echten Betrieb stehen könnten, und enthält gleichzeitig eine
wiederverwendbare Projektvorlage.

## Öffnen

Datei → **Komplettes Backup laden** → `Glide-Funktionsvorschau.glidebackup`

> **Achtung:** Ein Backup-Import ersetzt den gesamten aktuellen Bestand.
> Vor dem Import legt Glide automatisch eine Sicherung `vor_import_*.glidebackup`
> an; diese wird nie wegrotiert. Zum gefahrlosen Ausprobieren lässt sich Glide
> auch mit einem eigenen Datenordner starten:
>
> ```powershell
> $env:GLIDE_DATA_DIR = "$env:USERPROFILE\Glide-Probe"
> pythonw "Glide-Aufgaben-und-Listen_v2.11.0.pyw"
> ```

## Was drin ist

| | |
|---|---|
| Listen | 19 |
| Ordner | 7, über drei Ebenen verschachtelt |
| Labels | 8 (zwei feste, sechs eigene) |
| Aufgaben | 188 |
| Zwischenüberschriften | 57 |
| Long-Tasks | 13 |
| Gruppen | 5 |
| Mit Fälligkeit | 124 – von überfällig bis in drei Monaten, davon 11 mit Uhrzeit |
| Anhänge | 2 echte Dateien |
| Papierkorb | 3 Einträge: eine Liste, ein Ordner und **ein einzelner Punkt** |

## Die Projektvorlage

Der Ordner **Projekte** enthält zwei Vorhaben nebeneinander. **Redesign &
Branding** bildet ein vollständiges Marken-Redesign in zehn Phasen ab, von der Auftragsklärung bis zur Übergabe an das Tagesgeschäft:

1. Briefing & Zielbild
2. Analyse & Recherche
3. Strategie & Positionierung
4. Naming & verbale Identität
5. Visuelle Identität
6. Design-System & Anwendungen
7. Website & digitale Kanäle
8. Produktion & Rollout
9. Kommunikation & Launch
10. Erfolgsmessung & Markenpflege

Jede Liste ist mit Zwischenüberschriften gegliedert; die Long-Tasks halten
jeweils die eine Entscheidung fest, die exakt so stehen bleiben soll, wie sie
beschlossen wurde. Fälligkeiten sind auf den Erstellungstag bezogen und ergeben
eine realistische Staffelung über rund drei Monate.

**Für ein eigenes Projekt:** Ordner in der Seitenleiste auswählen, über das
Rechtsklickmenü duplizieren, Termine und Namen anpassen, Unpassendes löschen.

## Was sich damit ausprobieren lässt

- **Verspätet** – vier überfällige Aufgaben liegen bereit
- **In Bearbeitung** und **Kalender** – über 100 Fälligkeiten, Wochen- und Monatsansicht
- **Long-Task** – Rechtsklick → Art → *In Aufgabe zurückwandeln* und wieder zurück,
  oder dasselbe über das Label „Long-Task“
- **Zwischenüberschrift** – die Nummerierung darunter beginnt jeweils wieder bei 1
- **Schmales Fenster** – Label- und Fälligkeitsspalte weichen, der Text bekommt die Breite
- **Verschachtelte Ordner** – `Projekte` enthält zwei Projektordner; ein Ordner lässt
  sich per Drag & Drop in einen anderen ziehen (obere/untere Kante sortiert, die Mitte
  legt hinein)
- **Punktdetails (Long-Task)** – F2 auf einem Long-Task öffnet das Fenster mit
  mehrzeiligem Titelfeld
- **Papierkorb** – eine abgesagte Kampagne, ein Archivordner **und ein versehentlich gelöschter Punkt** warten auf Wiederherstellung. Der Punkt kehrt an genau die Stelle zurück, an der er stand.
- **Uhrzeit** – elf Termine tragen eine feste Uhrzeit; alles andere ist ganztägig
- **Erweiterte Eingabe** – „Erweitert“ neben „Hinzufügen“ öffnet die vollständige Maske mit Kalender, Uhrzeit, Labels, Beschreibung und Anhängen
