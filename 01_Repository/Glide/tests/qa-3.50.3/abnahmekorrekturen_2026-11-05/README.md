# Abnahmekorrekturen 3.50.3

Stand 05.11.2026 · Glide 3.50.3 · Aufgabenformat 26

Auftrag: menschliche Rückmeldungen aus der eingefrorenen 3.50.2-Prüfung in 3.50.3 umsetzen; angehängten Skill Design-Richtlinien anwenden. Originale und menschlicher Teilstatus im [Abnahmeprotokoll](../../qa-3.50.2/menschenabnahme_2026-11-04/README.md). Keine pauschale Menschenfreigabe aus diesen Korrekturen.

## Geänderter Umfang

| Rückmeldung | Korrektur |
|---|---|
| 3.1 | Eine dauerhaft sichtbare Mehr-Aktion pro sichtbarer Aufgabe. Tabellenbudget und Fristenbreite gemeinsam berechnet, ganze Metadatenspalten weichen vor dem Titel. |
| 3.2 | 8 px Abstand zwischen gestapelter Eingabe und Suche. |
| 3.3 | Einzeilige Seitenwerkzeuge, Überschrift/Code direkt am Text; vorhandenes Mehr-Menü erhält die weiteren Aktionen. |
| 3.4 | Werkzeugwahl und Optionen der Zeichnung gebündelt, Raster/Referenz/Bildfolgenexport unter Mehr; doppelte Farbwahl und separate Undo-/Redo-Knöpfe entfallen, bestehende Kürzel bleiben. |
| 3.5 | Zellcursor erst bei Tastaturnavigation/-aktion; Mausbewegung und Fokusverlust entfernen ihn. Echte Auswahl und Fokusrahmen bleiben erhalten. |
| 4 | Gemeinsame Buttonrundung und 38 px äußere Werkzeughöhe; Theme-Registrierung beim Editorabbau entfernen. |
| 5 | Ungenutzte rechte Aktionsreserve in Labels/Büchern entfernt, Buchtitel priorisiert und leere Beschreibung ausgeblendet. |
| Seitenfuß | Textgemessene Knopfbreite, 10 px Karteninnenrand. |
| Ergänzung Kopf | Bei knapper Breite dieselbe globale Symbolgruppe neben die Eingabe beziehungsweise in die vorhandene Werkzeugzeile verschieben; Titel und Windows-Menüs bleiben oben. Beim Verbreitern zurück. |

## Prüfstand und Status

Windows 11 / Python 3.14.7 / eigene Tcl/Tk 9.1.0; ausschließlich isolierte künstliche Daten. Betroffene Designkontexte und D61 an der zentralen Gestaltungsquelle dokumentiert.

- Bestehende Baseline Werkzeugzeile: grün nach UTF-8-Konsolenaufruf; der erste Konsolenlauf scheiterte beim Drucken von ≥, nicht an der Geometrie. Originalrot erhalten.
- Gegenprobe mit neuem Befundtest auf unverändertem 3.50.2: passend rot an 108 px ungenutzter Labels-Reserve.
- Entwurfsprüfung: vier Kombinationen von Light/Dark/Glas, 860 × 700/1280 × 800 und mittlerer/großer Schrift grün. Originalrotstände aus der Entwicklung lokal erhalten.
- Lokaler technischer Nachteststand abgeschlossen: strenge Grundstufe 19/19 grün, Quelle/Python/Showcase abgeglichen, nativer Windows-Kandidat gebaut und isoliert gestartet. Genaue Bereichs-/Vollmatrixgrenzen unten; menschlicher Nachtest und neue native Mac-/Linux-Matrix offen.

Lokale Laufablage enthält Originalbilder/Skill, Hashmanifeste, Rohlogs, JSON-Berichte und eigene Fensteraufnahmen. Öffentliches Protokoll enthält keine personenbezogenen Pfade oder Bilder. Quelle, Python-Lieferung, eigenständige Pakete und Menschenabnahme bleiben getrennte Statusachsen.


## Gesicherte Vorläufe und Betriebsgrenze

- Erste vollständige Arbeitsmodi-Serie am Entwurf: 44 grün, zwei rote Fälle. Kopfverweise benötigte einen ausdrücklich hergestellten Ruhe-/Fokuszustand statt Abhängigkeit vom echten Benutzerzeiger. Kompakt-Heute zeigte überlappende Zeilenaktionen; Randgrenze und tatsächliche native Zeilenhöhe werden nun berücksichtigt. Die ergänzte Probe prüft auch künstlich 26 px hohe Zeilen, Scrollen und einen veralteten Knopfbefehl.
- Nach dem ersten Randfix zeigte Kompakt-Heute weiterhin 6 px Überlappung benachbarter Knöpfe. Erst die Begrenzung auf die tatsächlich gemessene Zeilenhöhe löste diesen Befund. Separate unveränderte Kompaktprobe danach grün (138 Knopfprüfungen). Nicht als bereits durch den ersten Fix behoben ausgeben.
- Während Endprüfung/Paketbau wurde Laufwerk C voll. Die unterbrochenen Läufe gelten als Betriebsabbrüche. Ausschließlich die Prüfablage dieser Runde auf Laufwerk E verschoben, keine Nutzerdaten oder alte Abnahmefassung entfernt; folgende Läufe einschließlich TEMP/TMP und PyInstaller-Cache auf E. Originale/Rohlogs bleiben erhalten.
- Windows-Paket ist lokal gebaut, nativer Quell-/PE-/Lizenzvergleich grün; nach der Kopf-Ergänzung erneut gebaut. Echte isolierte Startprobe und abschließende UI-/CI-Ergebnisse noch ausstehend. 244 Werkzeugtests grün (ein Skip); erste 1.128 Fachtests grün, endgültige Grundstufe folgt.
- Die dritte Inhaberrückmeldung ist im selben Versionsschnitt enthalten. Neue konkrete Probe und Gestaltungsprobe des Kopfes: vier Konfigurationen sowie 192 Knopfprüfungen in fünf Konfigurationen grün. Vollständige neue Arbeitsmodi-/Bereichsserie auf dem Kopfstand läuft.
- Nach der bestehenden Aufbewahrungsregel 60 überalterte Dateien vorab bytegleich lokal gesichert und aus der Arbeitsablage entfernt; sieben historische Links auf die im Ausgangscommit belegte Git-Fassung umgestellt. Keine Änderung am Git-Index durch die Kürzung.


## Technischer Abschlussstand und genaue Grenzen

Quelle, Python-Fassung und Showcase tragen 3.50.3 / Format 26. Python-Abgleich: 92 Code-Dateien und 171 Ressourcen bytegleich. Showcase über echten Import, ID-Verweise, Bilder, Undo, Export und Neustart geprüft und geliefert. Vollständige allgemeine UI-/UX-Suite 17/17 grün. Nach dem letzten Eingriff (Packreihenfolge der globalen Symbole vor den Pinnwand-Ansichtsumschaltern) sind Werkzeugzeile, konkrete Abnahmeprobe und Kompaktprobe sowie gesamte Aufgaben3380-, Planungs-, Pixel-, Bildfolgen-, Editorabbau-, Drag- und Rückmeldungssuiten grün. Der ältere Rückmeldungstest prüft die Auswahlaufhebung nun über das echte neue Optionsmenü statt den beauftragt entfernten Dauerschalter.

Die vollständige Arbeitsmodi-Runde auf App `52b47d77…` hatte 45/46 grün; die eine verbleibende Pinnwand-Reihenfolge wurde anschließend gezielt korrigiert und mit unveränderter Werkzeugleistenprobe nachgeprüft. **Kein neuer vollständig eingefrorener Gesamt-/Remote-Matrixlauf auf App `ed3fd6dd…` behauptet.** Einzelne grüne Bereiche sind weder eine neue Plattformmatrix noch eine menschliche Freigabe. [Maschinenlesbare Statusachsen](ergebnis.json).

Windows-Kandidat unter `build/windows/Kandidaten/Glide-3.50.3-abnahme-20261105`: 132 Dateien vom nativen Bau bytegleich kopiert; Quellcode-/PE-/Lizenznachprüfung und echte isolierte Startprobe mit eigener Python-3.14.7-/Tcl/Tk-9.1.0-Laufzeit grün. Der erste Paketstart erbte zwei ICU-Bibliotheken aus dem Poppler-Werkzeugpfad der Ausführungsumgebung und wurde korrekt abgelehnt. Herkunft über den gestarteten Prozess nachgewiesen; Wiederholung mit ausschließlich Windows-Systemverzeichnissen im lokalen Prozess-PATH grün. Keine fremden DLLs zusätzlich gebündelt, keine Laufzeitgrenze gelockert. Der Nachteststarter verwendet dieselbe bereinigte Umgebung.

Grundstufe: der erste Lauf scheiterte im No-TZ-Unterlauf an einem über 130 Zeichen langen temporären Exportpfad; kurze Prüfablage korrigiert. Der folgende Lauf bestand alle übrigen Schritte und meldete nur den aus der vorbestehenden Dokumentpflege stammenden Kürzungsvermerk mit altem Datum. Historische Kürzung vom 04.11. bewahrt und Vermerk zum fortgeschriebenen Stand 05.11. ergänzt; Synchronisationsnachprüfung grün. Abschließender vollständiger Grundstufenlauf **19/19 grün**: Syntax/Version/Dokumente/Fixtures, 244 Werkzeugtests (ein Skip), zweimal 1.128 Fachtests, Analysen, Start, strenger Lieferabgleich, Fremdcode/Datenschutz/Aufbewahrung und Synchronisation. [Abschlussmetadaten](ci-abschluss.json).

Der neue Nachtest nutzt eine eigene, bei der Kopie auf stabile JSON-Bytes geprüfte Kopie des bisherigen künstlichen Abnahmebestands, einschließlich der vom Inhaber angelegten Zeichnung. Sperr-/Sitzungsdateien wurden nicht übernommen. Originaldaten und Quellbytes der 3.50.2-Prüffassung bleiben erhalten. Nachtest der Korrekturen, weitere menschliche Blöcke, physische DPI-/Mehrmonitorprobe und neue Mac-/Linux-Pakete bleiben offen. Keine Veröffentlichung, kein Commit oder Push.


**Bereit für den menschlichen Nachtest:** 3.50.3 ist ein lokal geprüfter Windows-Abnahmekandidat. Die eigenständige Lieferung enthält dieselben geprüften Quellbytes wie die Python-Fassung. Nachteststarter und eigene Datenkopie liegen in der lokalen Prüfablage; Originalbestand 3.50.2 bleibt erhalten. Die tatsächliche menschliche Rückmeldung wird erst nach Eingang eingetragen. Kein neuer Release-/Plattform-Gesamtabschluss.

## Fortsetzung der menschlichen Abnahme am 05.11.2026

Auf erneuten Benutzerauftrag den nativen Windows-Kandidaten geöffnet; EXE-SHA-256 erneut identisch mit `e05aaa4f…`. Die bisherige lokale Prüfablage auf Laufwerk E ist auf diesem Rechner nicht erreichbar. Deshalb eine neue isolierte Ablage mit frischem synthetischem Showcase verwendet: Teilbackup über den echten Bedienweg „Datei → Sicherung → Listen/Ordner hinzufügen“ importiert, zehn Dokumente hinzugefügt; „Vermarktung · Umsetzung“ sichtbar. Dies ist keine Fortsetzung derselben Datenkopie; die frühere eigene Zeichnung wurde nicht übernommen. Originalbestand unverändert.

Lokaler Startkontext und Wiederanlaufstarter liegen unter `%USERPROFILE%/GlidePruefung/abnahme3503-20261105/`; `GLIDE_DATA_DIR` zeigt ausschließlich auf dessen Unterordner `daten`. Start mit bereinigtem Prozess-PATH. Zuerst Kopf/Umbruch und Erreichbarkeit bei schmaler/breiter Darstellung menschlich nachtesten, danach Tabellen-/Buchbreiten, Seiten-/Zeichenwerkzeuge und restliche Blöcke. **Status: geöffnet und vorbereitet, menschliche Rückmeldung ausstehend.** Kein Freigabehaken aus der eigenen Start-/Importsichtung.

### Erste menschliche Nachtestrückmeldung – bestanden

05.11.2026, direkte Benutzerrückmeldung im Chat: „1. passt / 2. passt / 3. passt“. Zuordnung zum unmittelbar vorher angeleiteten Nachtest auf dem nativen Windows-Kandidaten `e05aaa4f…`:

| Nachtestpunkt | Menschliches Ergebnis |
|---|---|
| 1 – Fenster schmal/breit: globale Symbole wechseln neben die Eingabe und zurück; Titel und Windows-Menüs bleiben lesbar | bestanden |
| 2 – Eingabe/Suche und Plus bleiben erreichbar, Abstand bei schmalem Fenster passend | bestanden |
| 3 – dauerhafter Mehr-Knopf je sichtbarer Aufgabe; Scrollen und Unterpunkte auf-/zuklappen ohne störende Überdeckung | bestanden |

Nur diese drei Teilpunkte sind menschlich bestätigt. Große Schrift, alle Seitenleisten-/Themevarianten, Tabellen-/Label-/Buchbreiten, Seiten-/Zeichenwerkzeuge und weitere Sitzungsblöcke bleiben offen. Für die nächste Rückmeldung die Tabellenansicht von „Vermarktung · Umsetzung“ geöffnet. Keine Gesamtabnahme.

## Weitere Rückmeldung und Buchbreiten-Nachlauf

05.11.: Punkte 4 (Tabelle) und 5 (Labels) vom Benutzer jeweils mit „ist sehr gut“ bestätigt. Punkt 6 (Buch) mit ungenutzter Innenbreite; ausdrücklich auch schmale/ausgeblendete Seitenleiste einbeziehen. Quelle/Python `449f8aec…` korrigiert und als neuer Python-Nachtest geöffnet. Die bisherigen nativen Hashes und breiten Prüfbelege oben gelten weiterhin nur für ihre ursprünglichen Bytes. [Korrektur, 64 Breitenprüfungen und offene Liefer-/Abnahmegrenzen](../buchbreite_2026-11-05/README.md).
