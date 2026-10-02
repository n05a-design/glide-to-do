# Glide 3.33.1 – Bereiche und Fenster

Stand 01.10.2026 · Glide 3.33.1 · Aufgabenformat 20

Der Ergänzungsauftrag erweitert 3.33 um Zeichnungen, wählbare Bereichssichtbarkeit, einheitliche Inhaltsgrenzen, Logohöhe, Fensterreaktion und Ablageprüfung. Die frühere Reservierung 3.33.1 für UX1 ist damit kein gelieferter UX1-Umbau.

## Bedienvertrag

| Bereich | Inhalt | Ausblendbar |
|---|---|---|
| Seiten | Bücher (Art `library`, bisher Bibliothek), Ordner, Seiten | Ja |
| Listen | Alle bestehenden Dokument- und Ordnerarten | Nein |
| Notizen | Notizbücher, Ordner, Notizen; im Notizbuch auch datierte Zeichnungen | Ja |
| Zeichnungen | Ordner, Zeichnungen | Ja |

**Klarstellung des Inhabers vom 01.10.2026:** Ein Notizbuch nimmt im Bereich Notizen weiterhin datierte Zeichnungen auf („Zeichnung · TT.MM.JJJJ“ mit Momentdatum, [Vertrag 65](65_ZEICHNUNGSSEITE_3.29.0.md)). Die Regel hängt am direkten Elternordner der Art `journal`; ein gewöhnlicher Ordner unter Notizen nimmt keine Zeichnung auf. Aufgabenlisten und Pinnwände in einem Notizbuch bleiben ein Fall für Listen. Anlegen, Ziehen, Verschieben, Einrücken, Wiederherstellen und Vorlagen prüfen dafür den Zielordner (`sidebar_policy.CONTAINED`).

Ausblenden entfernt nur die Navigation. Ganze Zweige bleiben in Listen erreichbar. Gemischte Altbestände stehen vollständig unter Listen; keine automatische Umwandlung oder Teilung. Die neue Zeichnungsübersicht zeigt Zeichnungen auch in bestehenden gemischten Ordnern. Eine gewöhnliche Ordnerwurzel merkt ihren Bereich über `sidebar_locations` in Einstellungen; Aufgabenbackups enthalten diese gerätespezifische Anzeigeeinstellung nicht, Komplettbackups mit Einstellungen schon. Ohne Einstellung gelten die natürlichen Arten. Kein neues Datenformat oder Inhaltstyp.

Neue Inhalte und Verschiebungen müssen im Zielbereich zulässig sein. Ausrücken erhält den aktuellen Bereich, auch wenn ein früherer Root-Verweis einen anderen Bereich nannte. Die Zielauswahl beim Wiederherstellen bietet nur passende Ordner; das Zurückholen an den alten Ort erhält gemischte Altbestände. Ordner werden samt allen Unterordnern/Inhalten geprüft. Neutraler Drag erhält Arten, IDs und Termine; ein gemeinsamer Undo-Schritt stellt auch die Root-Zuordnung wieder her. Überschriften sind Ziele für leere oder eingeklappte Bereiche. Alle Bäume verwenden gemeinsame Bindungen und Klappzustände. Die Fachlogik ist Tk-frei in `sidebar_policy.py`. Bei knapper Fensterhöhe passen sich Baumhöhen an; die Überschriften und Listen bleiben erreichbar.

## Fenster und Performance

`_center_dialog` misst das fertig aufgebaute, noch verborgene Fenster und positioniert es vor dem Einblenden. Anschließend wird es sichtbar; bestehende Aufrufer behalten den bisherigen Sichtbarkeitsvertrag vor `run_modal`. `run_modal` bleibt der einzige Modalweg, mit Griffwiederherstellung und Schließen über Escape beziehungsweise Fensterschalter. Das Menükommando bleibt wegen der macOS-Menüverfolgung weiterhin verschoben. Eine bereits gemessene Dialogbreite wird ohne zweiten vollständigen Tk-Leerlauf geprüft. Breitenkonfigurationen der Seitenleiste vermessen unveränderte Spalten nicht erneut. Settings-Umbruch setzt identische Werte nicht wiederholt.

Die native Einblendung des Einstellungsfensters bleibt ein Performance-Schwerpunkt. Eine alternierende Messung eines früheren Zwischenstands brachte dort keine stabile Verbesserung (Median etwa 2,1 gegenüber 2,2 Sekunden); Aktionen und Druck reagierten in dieser Messung schneller. Der spätere Wiederholungslauf wurde ohne Ergebnis beendet. Diese Messung ist kein Latenznachweis für den endgültigen Stand und ersetzt keine physische Bedienprobe. Eine pauschale Zusage „alle Fenster sofort“ ist nicht abgenommen.

Das Logo hat einen Schriftabhängigen oberen Innenabstand und eine entsprechend verringerte Höhe. Die aktualisierten Logo-Master werden übernommen; Akzentfarben, Klickaktion und Verhalten bei schmaler Kopfzeile bleiben bestehen. Die direkten SVG-Attribute und Innenkonturen sind im [Logo-Vertrag](75_DOKUMENTATIONSREDUKTION_UND_LOGOS_3.33.1.md) beschrieben. Der Pack-Innenabstand wird nur bei einer echten Änderung gesetzt; identische Aktualisierungen dürfen keine neue Geometrieschleife auslösen.

## Prüfung und Nachweise

[Arbeitsnachweise](../tests/qa-3.33.1/bereiche_fenster_2026-10-01/README.md). Passende Baseline, vollständige Quell-/Python-/Bundle-Vorsicherung, bestehende Fenster-, Logo-, Drag- und Klappsuiten sowie neue Bereichssuite. Die Fensterprüfung erreicht 50 Fenster über Menüs und Knöpfe. Neue Bereichssuite: echte Formular-/Klick-/Tastatur-/Drag-Bindungen, Root-Undo, Speichern/Ausblenden/Wiedereinblenden, kleine Höhe, Schriftwechsel und Reload. Showcase-Pixelskizze sichtbar im Zeichnungsbereich; Fotos zeigen ausschließlich eigene Prüffenster.

**Abschluss 02.10.2026** ([Nachweis](../tests/qa-3.33.1/abschluss_2026-10-01/README.md)): Die erste Vollprüfung des Prüfkandidaten war rot (vier Suiten). Behoben: Der Dialog „Neu anlegen“ übergeht die 1 × 1-Meldung beim Einblenden, sonst blieb die breite Maske auf niedrigen Bildschirmen einspaltig; Notizbücher nehmen datierte Zeichnungen auf (Klarstellung oben); zwei Prüfungen auf diesen Vertrag gebracht. Abnahme: Vollprüfung Exitcode 0 mit 60 Integrationssuiten, Unit-Tests, Showcase und fünf Analysen; 142 Python-/56 Bundle-Dateien bytegleich, Signatur gültig. Physische OS-Maus-/Fokusbedienung, Windows/Linux, DPI/Mehrmonitor und Screenreader bleiben separat offen.

## Ablage

Zwei verbliebene echte `_Z`-Markierungen wurden gefunden: die überholten manuellen Checklisten 3.28 und 3.29. Sie wurden zunächst unverändert ins benachbarte Archiv verschoben und nach der ausdrücklichen Löschfreigabe vom 01.10.2026 entfernt; die aktuelle Prüfliste ersetzt sie. Namensbestandteile wie „Zeichnungen“ oder „Zwischenstände“ sind keine Löschmarkierung. Historische QA-Ergebnisse, Nutzerdaten und Grafikquellen bleiben Belege. Überholte Markdown-Versionskopien wurden nach Wissensabgleich entfernt; der [Bereinigungsnachweis](75_DOKUMENTATIONSREDUKTION_UND_LOGOS_3.33.1.md) dokumentiert dies. Aktive Verweise werden gegen reale Dateiexistenz geprüft; bereits entfernte Dateien werden nicht als vorhandene Originale ausgegeben.

## Anschluss

Offen bleiben der komplette UX1-Umbau mit sieben Startseitenkacheln (D12), P03/P09b, P04 Bildlayout, P06/P08 sowie Parser/Feldchips nach D10. GIF-Umfang D07 und Paketbauwerkzeug werden erst bei ihrer Etappe entschieden. Dieser Ergänzungsauftrag entscheidet keine weiteren ungewählten Richtungen.
