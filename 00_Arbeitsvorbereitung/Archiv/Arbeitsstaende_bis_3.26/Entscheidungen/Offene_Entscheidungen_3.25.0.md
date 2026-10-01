# Offene Entscheidungen – Glide 3.25.0

Stand: 19.09.2026 · Glide 3.25.0 · Aufgabenformat 16

Fragen, die nicht im Code beantwortet werden können, weil sie Geschäft, Recht
oder Produktausrichtung betreffen. Die Punkte aus 3.24.0 gelten unverändert
weiter, soweit sie hier nicht als beantwortet genannt sind:
[Offene Entscheidungen 3.24.0](Offene_Entscheidungen_3.24.0.md).

## Mit 3.25.0 beantwortet

| Frage aus 3.24.0 | Antwort |
|---|---|
| **Wie weit darf der Dopamin-Modus gehen** | Eine Stufe weiter, aber in die Breite statt in die Lautstärke: Jede Aktion bekommt eine Rückmeldung, keine wird lauter. Kein Ton, keine Bildschirmblitze, keine gespeicherte Punktezahl. Die Grenze zur Gamifizierung bleibt damit, wo sie war. |
| **Zählt eine Kombo als Leistungsmessung** | Unverändert nein – sie lebt nur in der Sitzung. Die neue Rückmeldung auf jede Aktion zählt ebenfalls nichts: Sie meldet, dass etwas geschehen ist, nicht wie viel. |
| **Markenfigur** (aus 3.23.0) | Teilweise. Es gibt seit 3.25 eine gezeichnete Figur auf der Startseite – Stufe 2 der Entscheidung `ARBEITSBEGLEITER.md`. Sie trägt keinen Namen, außer der Benutzer vergibt einen, und sie führt durch nichts. Markenfigur als Asset und führender Begleiter bleiben offen. |

## Neu mit 3.25.0

| Frage | Zusammenhang | Wer entscheidet |
|---|---|---|
| **Sollen Assets für den Begleiter beauftragt werden** | Die Lieferliste steht vollständig in `docs/decisions/ARBEITSBEGLEITER.md` – fünf Zustände in fünf Größen als PNG-24, Vektorquelle im Grafikmaster, Bewegung als Einzelbilder. Ergibt 25 Standbilder plus Bewegungsbilder. Erst zu beauftragen, wenn feststeht, wie die Figur aussieht und ob sie einen Namen trägt. Die gezeichnete Fassung trägt bis dahin. | Inhaber |
| **Bleibt „Rückmeldung auf jede Aktion“ auf `auto`** | Heute: im Dopamin-Design alles, sonst nur Erledigtes und Ziele. Wer die Rückmeldung mag, aber kein Dopamin-Design will, muss sie umstellen. Die Alternative wäre `all` als allgemeine Vorgabe – das ist eine Geschmacksfrage und gehört nach der Prüfung am Gerät beantwortet. | Inhaber, nach Punkt 8.8 der manuellen Prüfung |
| **Brauchen die Minimaldesigns einen Akzentton** | Sie sind bewusst vollständig farblos. Ein einzelner Akzentton für die Auswahl wäre ein Kompromiss – er würde die Lesbarkeit erhöhen und die Idee verwässern. | Inhaber, nach Punkt 7 der manuellen Prüfung |
| **Was geschieht mit dem Fehlerprotokoll** | Es liegt als Klartext neben den Daten und enthält Tracebacks, also Dateipfade und Zeilennummern – keine Aufgabeninhalte. Soll es beim Weitergeben automatisch angehängt werden, wenn es Einträge hat? Das wäre eine Datenweitergabe und braucht eine bewusste Entscheidung. | Inhaber |
| **Soll das Handbuch auch gedruckt werden können** | Es steht als Tabelle im Quelltext und ließe sich in die Druckansicht aufnehmen. Dagegen spricht, dass ein gedrucktes Handbuch altert und die App es nicht nachziehen kann. | Inhaber |

## Unverändert offen

Publisher- und Herausgebername, Markenprüfung, Vertriebsweg, Signierung und
Notarisierung, Preisfrage, der Name der Markenfigur, die Anbindung an einen
KI-Dienst, gerichtete Abhängigkeiten als echte Funktion, das Reisen von
Pinnwänden zwischen Beständen und benannte Bereiche auf der Fläche stehen
unverändert in
[Offene Entscheidungen 3.24.0](Offene_Entscheidungen_3.24.0.md) und
[Offene Entscheidungen 3.23.0](Offene_Entscheidungen_3.23.0.md).
