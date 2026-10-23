# D55 – Arbeitsmodi und Seitenbedienung

23.10.2026 · lokaler Kandidat auf Glide 3.44.0 · Aufgabenformat 26 · keine Lieferung, kein Commit

Auftrag und Auswahl: „weiter mit den features“; E-U1 A (Kompaktmodus), E-U2 A (Nebenansicht im Inspektorbereich), E-U3 A (durchsuchbare Seiten-/Blockaktionen, Blockgriff, ruhiger Seitenkopf) als [D55](../../../docs/ARBEITSRICHTUNG.md). Zuschnitt, Ergebnis und Abweichungen: [Plan §21.11](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2111-viertes-umsetzungspaket-arbeitsmodi-und-seitenbedienung-d55); Verhalten: [Funktionen](../../../docs/20_FUNKTIONEN.md#arbeitsmodi-und-seitenbedienung-d55-lokaler-kandidat-auf-3440); Gestaltungsregeln: [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md#arbeitsmodi-und-seitenbedienung-d55-23102026).

## Quelle

Ausgangs-App `d0bf41427f85edd8ad3b5185310dc4879d175cf577677cb0050ba2dfa9490762` (Lieferung 3.44.0). Abschluss-App `ff9b9cae0fc2c0cf3daf606fc3934e2efa2464b562fd250b3ddbb7abff823e45`. Neu: `action_menu.py`, `side_view.py`, `compact_mode.py` (Tk-frei) mit Unit-Tests und die Pflichtsuite `test_arbeitsmodi.py`; geändert: `app.pyw`, `action_catalog.py`, `symbol_policy.py`, `pruefen.py`. Keine neue Abhängigkeit, keine Datenformatänderung, zwei additive Einstellungen. [Quellmanifest](quellmanifest.json). `07_Python-Versionen` ist unverändert und weicht damit bewusst vom Quellbaum ab.

## Ausgeführte Prüfungen

Linux mit Xvfb, Python 3.12, Tk 8.6.14, künstliche Daten in temporärem `GLIDE_DATA_DIR` vor jedem Appimport. Ein Tk-8.6-Lauf ist kein Nachweis der Windows-/Mac-Darstellung unter Tk 9.

| Prüfung | Ergebnis |
|---|---|
| Fachlogik | 887 Unit-Tests grün, ebenso ohne Systemzeitzonen (`PYTHONTZPATH=""`); 160 Werkzeugtests grün (1 übersprungen) |
| Neue Pflichtsuite | `test_arbeitsmodi.py` 12/12 grün an der Abschluss-App, sequenziell in einem Prozess bei Bildschirm 1600 × 1000 ([Bericht](test_arbeitsmodi.json)) und 1920 × 1200 ([Bericht](test_arbeitsmodi_1920.json)); Knopfschutz B15 ohne Befund in allen Fällen |
| Rote Gegenprobe | Dieselbe Suite gegen die unveränderte Lieferung 3.44.0: 12/12 rot ([Bericht](gegenprobe_3.44.0.json)) |
| Regression | Einmal alle 102 Suiten auf einer eingefrorenen Zwischenstandskopie, danach die betroffenen Suiten an zwei späteren Ständen und 17 Seiten-, Layout-, Handbuch- und Zugänglichkeitssuiten an einem Stand, der sich von der Abschluss-App nur in den Fensterlagen unterscheidet; an der Abschluss-App selbst `test_arbeitsmodi`, `test_glide` und `test_fenster330` grün ([Übersicht](regression.json)) |
| Sichtprüfung | Eigene Fensteraufnahmen (lokal, nicht versioniert) von Seite, Blockaktionen, Kopfverweisen, Nebenansicht und Kompaktmodus in hell, dunkel und Verlauf; Befund zur Kopfzeile siehe unten |
| Statische Prüfung | `pyflakes` ohne neue Meldung gegenüber 3.44.0; neue Module ohne Meldung |

## Befunde und Korrekturen

- **Designwechsel:** Die Kopfverweise wurden zunächst über `make_button` angelegt und landeten in der Themenliste `app.buttons`. Nach einem Neuaufbau des Editors brach der nächste Designwechsel mit `invalid command name …page_head_actions…` ab (rot in `test_seiten33318`, `test_mindestgroesse330`, `test_uiux_paket` b17_b19). Jetzt wie alle Editorknöpfe eigenständig; alle drei grün.
- **15-%-Regel:** Eine eigene Zeile für die Kopfverweise über dem Titel schob die Seiteninhaltskante bei 1280 × 800 von 121 auf 157 px (`test_aufgaben3380`). Danach reservierte Breite am Titelzeilenende; die Sichtprüfung zeigte Titel, die bei offener Nebenansicht in schmale Spalten umbrachen. Endstand: „+ Symbol“/„+ Titelbild“ nur auf ohnehin freiem Platz, sonst über „Mehr“; Inhaltskante wieder 121 px wie in 3.44.0.
- **Inspektor im schmalen Fenster:** Beim Verkleinern von 1280 auf 900 px behielt der Aufgabeninspektor die Oberkante des breiten Fensters und überdeckte Ansichtsumschalter und „☰“ (3.44.0: 11 Knopfbefunde, frisch bei 900 px geöffnet keiner). Inspektor und Nebenansicht hängen jetzt am Packplatz der Inhaltsfläche; 0 Befunde.
- **Abbau mit offenen Leerlaufaufträgen:** Prüfungen nach Fokusverlust des Editors sind am Hauptfenster vorgemerkt und werden beim Abbau abgebrochen. Gefunden, weil ein nicht vollständig abgebautes Testfenster spätere `StringVar` an den alten Interpreter band.
- **Zweiter Bildschirm:** Tk meldet unter Windows nur die Größe des Hauptbildschirms. Ein Fenster auf einem zweiten Bildschirm wäre beim Eintritt in den Kompaktmodus auf den Hauptbildschirm gesprungen; dieselbe Grenze hatte schon in 3.44.0 die Wiederherstellung der Fensterlage beim Start. Zudem schrieb der Kompaktmodus Lagen links vom Hauptbildschirm als „-x“, was Tk als Abstand vom rechten Rand liest, und der Start verwarf Tks eigene Schreibweise „+-x“ (unter Tk 8.6 nachgestellt: „300x200-100+50“ landet auf einem 1600 px breiten Bildschirm bei x = 1200). Kompaktmodus und Start rechnen unter Windows jetzt mit der virtuellen Fläche aller Bildschirme (`desktop_bounds`) und lesen Tk-Geometrie einheitlich (`compact_mode.parse`). Unit-Tests mit Bildschirm rechts und links, `test_glide` mit „+-x“, Windows-Zweig unter Linux mit nachgestellten Maßen geprüft; echte Windows-Hardware offen. Die Abschluss-App unterscheidet sich vom Stand der Regressionssuiten nur in Fensterlagen (Start, Kompaktmodus).
- **Vollprüfung in der Windows-Sandbox:** Neues Werkzeug `tests/tools/windows_sandbox.py` mit Starter `windows_sandbox.cmd` (Auftrag 23.10.2026). Neun Werkzeugtests für Einfrieren, Quellmanifest, Konfiguration, Startskript, Prüflaufzeit und Bildschirmwahl; Trockenlauf mit `--nur-dateien` am ganzen Projekt. Start der Sandbox und Fensterlage sind nur unter Windows prüfbar und noch nicht erprobt.
- **Prüfwerkzeug:** Die neue Suite bewegt den echten Mauszeiger nicht mehr (`warp`); unter Windows wäre er sonst während einer Vollprüfung über den Bildschirm gesprungen. Tastenereignisse holen vorher den Fensterfokus; ohne Fenstermanager folgt er unter Xvfb dem Mauszeiger, das Ergebnis hing sonst von der Bildschirmgröße ab.

## Rot ohne Bezug zu D55

Unter Linux/Tk 8.6 in dieser Umgebung rot und auf der unveränderten Lieferung 3.44.0 ebenso rot: `test_uiux_paket` b12_b13 (Zelltags erst ab Tk 9) und b16 (pixelweises Bildscrollen nur mit Tk 9), `test_aufgaben3380` (Seiten 121 statt ≤ 120 px mit DejaVu-Schrift), `test_speicherlast330` (WA-41-Umfeld), `test_erwaehnungen` Fall `oeffnen_fallen`, `test_seitenkarten`/`test_ansichten`/`test_wiederholungsregeln` (Altleser-Gegenproben finden die 3.43.1-Datei nicht am erwarteten Ort in `07_Python-Versionen`) und `test_features330` (Pinnwand-Zeitgrenze 8 s, im Container rund 15 s). `test_features330` mit gelockerter Zeitgrenze lief einschließlich der Inspektorfälle im schmalen Fenster vollständig grün.

## Offen

Versionswechsel und eingefrorene Vollprüfung am nächsten Phasenende (Windows/Tk 9), Mac, Sicht-/DPI-/Screenreader- und Menschenabnahme nach der [Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#arbeitsmodi-und-seitenbedienung-d55-lokaler-kandidat-auf-3440). Im Kompaktmodus bleibt dem Titel bei 480 px Breite nur wenig Platz; er wird gekürzt.
