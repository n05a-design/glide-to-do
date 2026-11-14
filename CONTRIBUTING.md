# An Glide arbeiten

Stand 14.11.2026 · Glide 3.61.0

Du möchtest einen Fehler melden, eine Idee einbringen, die Dokumentation verbessern oder an Glide entwickeln? Hier findest du den Einstieg und die zuständigen Unterlagen.

[Projektübersicht](README.md) · [Roadmap](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) · [Funktionen](01_Repository/Glide/docs/20_FUNKTIONEN.md) · [Aufbau der App](01_Repository/Glide/docs/02_ARCHITECTURE.md) · [Entwicklungsablauf](#entwicklungsablauf) · [Qualität](01_Repository/Glide/docs/07_QA_BERICHT.md)

## Den passenden Einstieg finden

| Du möchtest … | Hier geht es weiter |
|---|---|
| wissen, woran gearbeitet wird und was geplant ist | [Roadmap und Aufgabenstatus](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) |
| verstehen, wie eine Funktion arbeitet | [Funktionen und Bedienung](01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| den technischen Aufbau kennenlernen | [Architektur](01_Repository/Glide/docs/02_ARCHITECTURE.md), [Glide-System als Bestandsregister](01_Repository/Glide/src/glide/README.md) und [Shell-Konzept als Entkopplungsziel](01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) |
| eine Entwicklungsumgebung einrichten und Glide starten | [Voraussetzungen und Schnellstart](01_Repository/Glide/README.md#schnellstart-aus-dem-quellstand) |
| eine bestehende Arbeit fortsetzen | [Übergabe und aktueller Arbeitsstand](00_Arbeitsvorbereitung/Glide_Uebergabe.md), danach [Arbeitsregeln](01_Repository/Glide/AGENTS.md) |
| Prüfungen ausführen oder Ergebnisse einordnen | [Prüfplan](01_Repository/Glide/docs/05_QA_TESTPLAN.md), [Prüfwerkzeuge](01_Repository/Glide/tests/README.md) und [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md) |
| Texte, Verweise oder Anleitungen verbessern | [Zuständigkeiten und Änderungsbezüge](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) und [Dokumentationsindex](01_Repository/Glide/docs/00_INDEX.md) |

Der Entwicklungsplan bleibt die zentrale Roadmap. Funktionsbeschreibungen, Architektur und Prüfergebnisse werden in den jeweils verlinkten Fachunterlagen gepflegt.

## Fehler melden und Ideen vorschlagen

Nutze die [Formulare für Fehler und Wünsche](https://github.com/n05a-design/glide-to-do/issues/new/choose). Beschreibe bei einem Fehler die Glide-Version, das Betriebssystem, die Schritte zur Wiederholung sowie das erwartete und das beobachtete Verhalten. Verwende für Bilder und Beispieldateien künstliche Inhalte oder den [Showcase](05_Probelisten_Testdaten/Showcase/README.md).

Bei einer Idee hilft die konkrete Arbeitssituation: Was möchtest du erreichen, und wo fehlt dir etwas? Prüfe zuvor die Roadmap und die [Produktgrenzen](01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md). Größere Änderungen und neue Abhängigkeiten werden vor der Umsetzung mit dem Inhaber abgestimmt; Vorschläge und Prioritäten werden im Entwicklungsplan festgehalten.

Sicherheitslücken bitte vertraulich nach der [Sicherheitsrichtlinie](SECURITY.md) melden.

## Entwicklungsablauf

1. **Aufgabe und Umfang klären.** Übergabe und Roadmap lesen, den betroffenen Bereich eingrenzen und vorhandene Entscheidungen in der [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) berücksichtigen. Produktentscheidungen liegen beim Inhaber.
2. **Ausgangsstand verstehen und prüfen.** Die [Arbeitsregeln](01_Repository/Glide/AGENTS.md), betroffene Funktionsbeschreibungen und Architektur lesen, im Code auch die Aufrufer ansehen und eine passende bestehende Prüfung als Ausgangspunkt ausführen. Bei Oberflächenarbeit gelten die [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md).
3. **Zusammenhängende Änderung umsetzen.** Bestehendes Verhalten, Nutzerdaten und Datenformate bewahren. Fachlogik und Oberfläche nach den Arbeitsregeln trennen; Formatänderungen benötigen Migration, Sicherung und passende Tests.
4. **Wirkung prüfen und dokumentieren.** Die passenden Prüfungen ausführen, Ergebnisse und Grenzen festhalten und die betroffenen Fachunterlagen anhand der zentralen [Pflegematrix](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) abgleichen. Dort stehen auch die Beziehungen zwischen Roadmap, Glide-System und Shell-Konzept. Der [verbindliche Arbeitsablauf](01_Repository/Glide/docs/ARBEITSRICHTUNG.md#arbeitsablauf-einer-implementierung) beschreibt die Prüfphasen; für reine Dokumentations- und Werkzeugarbeit gelten die dortigen [Nachlaufregeln](01_Repository/Glide/docs/ARBEITSRICHTUNG.md#nachläufe-ohne-neue-app-version).
5. **Änderung zur Prüfung vorlegen.** Ein Pull Request erläutert Anlass, tatsächliche Änderungen, ausgeführte Prüfungen, offene Punkte und Risiken. Die Zusammenführung benötigt eine ausdrückliche Freigabe; Lieferung und Veröffentlichung folgen ihren eigenen Prüfschritten.

## Lokal entwickeln und sicher prüfen

Der Quellcode liegt unter `01_Repository/Glide/src/glide`. Der [technische Einstieg](01_Repository/Glide/README.md) enthält Voraussetzungen, Startbefehle und die CI-Grundstufe. Die [Modulübersicht](01_Repository/Glide/src/glide/README.md) hilft, die zuständige Codestelle und vorhandene Tests zu finden.

Für Tests muss `GLIDE_DATA_DIR` auf einen eigenen temporären Datenordner zeigen. Echte Nutzerdaten dürfen dabei nicht verwendet werden. Die sichere Testumgebung, Prüfmodi und Befehle stehen im [Prüfplan](01_Repository/Glide/docs/05_QA_TESTPLAN.md) und in der [Prüfwerkzeugübersicht](01_Repository/Glide/tests/README.md).

## Qualität, Lieferung und Freigabe

Der [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md) ordnet Ergebnisse ihrem jeweiligen Quellstand und ihrer Plattform zu. Gezielte Tests, vollständige Prüfungen, native Paketbauten und menschliche Abnahme werden getrennt ausgewiesen. Fehlgeschlagene oder übersprungene Prüfungen und offene manuelle Fälle bleiben sichtbar.

Ein grüner CI-Lauf ist keine Veröffentlichungsfreigabe. Die [manuelle Prüfliste](00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) beschreibt die menschliche Abnahme; die [Veröffentlichungsanleitung](01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) führt die weiteren Schritte für Pakete und Veröffentlichung auf.

## Lizenz

Der Projektcode steht unter der [Mozilla Public License 2.0](LICENSE). Beachte auch die [Hinweise zu Geltungsbereich, Drittkomponenten und Weitergabe](01_Repository/Glide/LICENSE.md).
