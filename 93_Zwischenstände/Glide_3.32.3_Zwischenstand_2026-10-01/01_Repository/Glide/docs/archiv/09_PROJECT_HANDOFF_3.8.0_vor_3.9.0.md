# Projektübergabe – Glide 3.8.0

Stand 12.09.2026 · Aufgabenformat 13 · Einstellungen 2 · Vorlagen 2

Kanonischer Code: `src/glide/app.pyw`; startbare Kopie im äußeren
`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.8.0.pyw` mit vollständigen Ressourcen.
Unveröffentlichter Entwicklungsstand, kein Git-Checkout.

## Aktuelle Umsetzung

Die priorisierte erste Erinnerungsstufe ist implementiert: feste/relative
Zeitpunkte in den Punktdetails, gemeinsame Übersicht, Aufschub, Bestätigung,
Erledigen mit Serienfortschritt, gespeicherte Zustellbelege und Originalbackup
vor Format 13. [Vollständiger Vertrag](31_ERINNERUNGEN_3.8.0.md).

Die Verarbeitung läuft im Tk-Zyklus alle 15 Sekunden. Eine neu zugestellte
Erinnerung hebt zusätzlich den Eintrag in Taskleiste bzw. Dock hervor – einmal
je Prüflauf, abschaltbar, ohne Fokusdiebstahl. Es gibt weiterhin keine
Systembenachrichtigungen und keine Verarbeitung bei beendetem Programm; beides
setzt eine registrierte, installierte Anwendung voraus
([Entscheidung](decisions/SYSTEMBENACHRICHTIGUNGEN.md)).
Verpasste Hinweise erscheinen nach Rückkehr gesammelt. Hintergrundänderungen
laufen über `item_change(background=True)` ohne Undo-/Aktivitätszählung.

Der 3.7-Bestand bleibt erhalten: vollständiger isolierter Vorlageneditor,
16 Praxisvorlagen, thematisierte Mac-Auswahlfelder und dynamische Kacheln.
[Vorlagen-/Mac-Vertrag](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md) ·
[Kacheln](29_DYNAMISCHE_KACHELN_3.7.0.md).

## Prüfung und Fortsetzung

[Aktueller QA-Bericht](07_QA_BERICHT.md). Beide vollständigen 3.8-Läufe sind
grün – der für die Erinnerungen und der für die Aufmerksamkeitsstufe: je zwölf
Suiten, zwei Analysen, Versions-, Dokumentations- und Datenabgleich.
Automatisiert ist damit alles abgenommen. Native Windows-Sichtprüfung, physischer Ruhezustand,
Trackpad, Screenreader, DPI/Monitore, Langzeitbetrieb und signierte Pakete bleiben offen.

Nächste Schritte: erste Stufe nativ abnehmen, Systemintegration der Erinnerungen
entwerfen, danach Reiter/Pinnwand. Gleiche Aufgabenobjekte weiterverwenden,
keine zusätzliche Statusverwaltung oder neue Projektmappe. Vor Änderungen
`AGENTS.md` lesen; echte Nutzdaten niemals für Tests verwenden. Frühere Dokumente
liegen vor ihrer Ersetzung im lokalen Archiv.
