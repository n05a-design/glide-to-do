# Windows-Vollprüfung vorbereitet und Befunde festgehalten – Nachweis

05.10.2026 · App 3.33.8 unverändert, kein Versionswechsel · Linux/Tk 8.6, künstliche Daten · Ausgangsstand: `main` nach PR #13 plus Planungsnachlauf ([Nachweis](../planung_2026-10-05/README.md))

Auftrag des Inhabers vom 05.10.2026: Die Befunde der Logo-Diagnose und der Windows-Arbeit dauerhaft in die richtigen Dokumente übernehmen. Prüfen, wie eine vollständige Prüfung wie am Mac auch unter Windows läuft, und die Lücke in Dokumentation und Prüfliste schließen. Danach festhalten, was noch zu prüfen und nachzutragen ist.

## Befunde am vorhandenen Windows-Nachweis

Grundlage ist [`windows_2026-10-05`](../windows_2026-10-05/README.md). Dessen Originalergebnisse bleiben unverändert.

| Nr. | Befund | Beleg |
|---|---|---|
| 1 | `release_hell.png` und `release_hell_dunkel.png` sind in beiden Läufen byte-gleich (SHA-256 `fa8654d6dfec3e58…`). Für 3.33.8 gibt es also keine Dunkelaufnahme. | Hashvergleich der vier Bilder |
| 2 | Ursache: `releasedaten.screenshots` setzte `theme_name`. `_compose_theme` leitet es bei jedem `apply_theme` aus dem Design neu ab. | Nachstellung: Zuweisung `light`/`dark` lässt das Design `glass_light`; `set_design` wechselt zu `light`/`dark` |
| 3 | Dieselbe wirkungslose Zuweisung steht in `test_ui_updates` (Dunkelschleife) und `test_ui_polish36`. Deren Dunkelfälle laufen hell. | Quelltext; Aufgabe W02 |
| 4 | Das Logo ist unter Windows mit Tk 9.0.4 geglättet: 116 Farbwerte im Logobereich statt 2 unter Tk 8.6. | Pixelauswertung `voll_2/screenshots/release_hell.png` |
| 5 | Gekürzte Seitenleistentitel sind unter Windows rechts um etwa ein Zeichen angeschnitten, ohne „…“: „Unterlagen & Asset“ statt „Unterlagen & Assets“, „Releaseplanung 3.3..“, „Vermarktungsstra..“. Unter Linux/Tk 8.6 kürzt dieselbe Stelle korrekt mit „…“. | Vorbefund W01, in der Sichtprüfung zu bestätigen |
| 6 | Unter Windows entstanden keine Fensterfotos; `test_fenster330` fotografierte nur unter macOS. | `pruefen.py`, `test_fenster330.py` |
| 7 | Die Prüfliste B0 beschrieb eine Laufzeitwahl (`py -3`, Tcl-Version), die der Starter seit 05.10.2026 nicht mehr hat. Pfade standen in `cmd`-Schreibweise. Die Prüflaufzeit ließ sich nicht reproduzierbar anlegen. | Prüfliste vor diesem Nachlauf |

## Änderungen

**Prüfwerkzeuge** (kein Lieferstand, keine Fachlogik):
- `tests/tools/releasedaten.py`: Aufnahme im hellen Design und seinem dunklen Gegenstück über `set_design`. Ein gleiches Bildpaar bricht ab.
- `tests/integration/test_fenster330.py`: Fensterfotos auch unter Windows über das vorhandene `save_windows_screenshot` (PrintWindow, nur das eigene Fenster). Fotofehler bleiben wie am Mac ein Zusatzbefund.
- `tests/tools/pruefen.py`: nur der Kommentar zu den Fensterfotos.

**Dokumente** (Zuordnung nach [Dokumentenpflege](../../../docs/DOKUMENTENPFLEGE.md)):

| Befund | Dokument |
|---|---|
| Leinwand ohne Kantenglättung, `subsample`/`zoom` ohne Filter, Rückfallwege brauchen ein Qualitätskriterium, Design statt `theme_name` | [Architektur §5](../../../docs/02_ARCHITECTURE.md#5-tk-fallstricke-teuer-gelernt) |
| Logo und Programmsymbol unter Tk 8.6, Seitenleistentitel unter Windows | [Funktionen §13](../../../docs/20_FUNKTIONEN.md#13-bekannte-grenzen) |
| Befunde am Logo-Master, PNG-Verwendung berichtigt | [Grafik-Master](../../../../../20_Grafik_Master/README.md) |
| Aufgaben LG01–LG04, W01–W04; Inhaberentscheidung I8; I6 präzisiert | [Entwicklungsplan](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) |
| I8 als offene Entscheidung | [Arbeitsrichtung](../../../docs/ARBEITSRICHTUNG.md) |
| Lehren zu Rückfallwegen, OneDrive-Arbeitskopie und PowerShell-Pfaden; Windows-Prüfaufruf | [Übergabe §4, §5, §7](../../../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md) |
| B0 neu gefasst, Sichtbefunde in B1, B5 präzisiert, neuer Punkt B13 „Anhänge an Aufgaben“ | [Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) |
| Nachprüfung der Windows-Aufnahmen | [QA-Bericht](../../../docs/07_QA_BERICHT.md) |
| Übernahmestand, §6 in den Grafik-Master verschoben | [Diagnose](../../../docs/diagnosen/LOGO_KANTENGLAETTUNG.md) |

## Synchronisationskopien zusammengeführt

Mit 3.33.8 kamen aus der Windows-Arbeitskopie gekürzte Fassungen zentraler Dokumente ins Repository. Die vollständigen Fassungen lagen daneben als OneDrive-Konfliktkopien `<Name>-MacBook Pro Max Ultra.md`. Die gekürzten Fassungen hatten Abschnitte verloren, auf die andere Dokumente verweisen: Prinzipien-Check, Grenzen einzelner Funktionen, Regeln des Prüfplans, Glossar und Versionsverlauf. Je Paar bleibt jetzt ein Dokument. Grundlage ist die vollständige Fassung; aus der Windows-Fassung kam hinzu, was dort neu war.

| Dokument | Übernommen aus der Windows-Fassung |
|---|---|
| [Index](../../../docs/00_INDEX.md) | Fehlerdiagnose, Lizenzstatus und Showcase als Orte |
| [Produktgrenzen](../../../docs/01_PRODUCT_CONSTRAINTS.md) | Tk 8.6 lauffähig, tkinterdnd2 optional mit Entscheidung, `ICONS`-Regel, Verweise auf Funktionen und Datenvertrag |
| [Prüfplan](../../../docs/05_QA_TESTPLAN.md) | Belegregeln, semantischer Abgleich, Messmethodik, Windows ohne Hintergrundmodus, Kontrollmatrix, Suiten 3.33.7/3.33.8 |
| [QA-Bericht](../../../docs/07_QA_BERICHT.md) | Prüfstatus 3.33.6 (Windows-Baseline), 3.33.7, 3.33.8, Lieferung, Nachprüfung der Aufnahmen |
| [Paketierung](../../../packaging/README.md) | `content_search.py` in der Modulliste |
| [Python-Lieferung](../../../../../07_Python-Versionen/README.md) | Stand 3.33.8, Windows-Start mit der Prüflaufzeit, Archivstand |

Gelöscht sind die sechs Kopien und `docs/09_PROJECT_HANDOFF.md`. Diese Projektübergabe war am 03.10.2026 in Übergabe, Arbeitsrichtung und Entwicklungsplan aufgegangen und aus der Windows-Arbeitskopie wieder aufgetaucht. Ihr Inhalt (D01–D17, Aufgabenvorrat, Inhaberantworten vom 30.09.2026) steht vollständig in [Arbeitsrichtung](../../../docs/ARBEITSRICHTUNG.md) und [Entwicklungsplan](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md). Alle Sprungmarken im Repository führen wieder ans Ziel; vorher waren es sechs tote, etwa `#regeln` im Prüfplan. Die Regel steht jetzt in der [Dokumentenpflege](../../../docs/DOKUMENTENPFLEGE.md), der Wächter als Aufgabe W04 im Entwicklungsplan.

**Gegenprüfung:** Ein getrennter Prüfagent hat jede Zusammenführung gegen beide Ausgangsfassungen gelesen. Aus den vollständigen Fassungen fehlte nichts. Aus den Windows-Fassungen und der Projektübergabe sind kleine Punkte nachgetragen: Tastatur und Mindestfenster im Prinzipien-Check, Lizenzen in Paketierung und Lieferung, Kennungszuordnungen G01 = B-01, U01 = N03, U07 = N02, G26 = N11, N12 mit Canvas-Beschriftung und D08 mit verschachtelten Bereichen. Bewusst nicht übernommen sind die Aufwand-, Risiko- und Begründungswerte des alten Aufgabenvorrats; die Projektübergabe nannte sie selbst Herkunftskontext, Git trägt sie. Ebenso entfällt das wörtliche Zitat der Inhaberantwort vom 30.09.2026; ihr Inhalt steht in der Arbeitsrichtung (Q1–Q5).

Der Herstellerhash der Prüflaufzeit wurde am 05.10.2026 gegen den Paketindex von python.org (`index-windows.json`, `pythoncore-3.14-64`, 3.14.8) abgeglichen. Er stimmt mit [`prueflaufzeit.json`](../windows_2026-10-05/prueflaufzeit.json) überein. 3.14.8 ist dort die neueste 3.14-Fassung.

## Prüfung

- Aufnahmeweg mit X11-Aufnahme statt PrintWindow nachgestellt: zwei verschiedene Bilder in `glass_light` und `glass_dark`.
- `test_fenster330` unter Xvfb: 50 Fenster, grün. Unter Linux entstehen wie vorgesehen keine Fotos.
- CI-Grundstufe mit strengem Liefervergleich ([Ergebnis](ci/ergebnis.json)).

Der Windows-Zweig von Aufnahme und Fensterfotos ist im Lauf um 18:29 bestätigt: 50 Fotos und zwei verschiedene Aufnahmen ([Nachweis](../windows_2026-10-05_1829/README.md)). Rohprotokolle und Bilder bleiben lokal.
