# Dokumentationsabgleich vom 13.11.2026

## Auftrag und Umfang

Dokumentation so verknüpfen, dass Änderungen ihre betroffenen Folgeaspekte erreichen; doppelte Pflege vermeiden, ähnliche Inhalte konsolidieren und Lücken schließen. Ausgangspunkt ist die lokale, bereits veränderte Arbeitskopie auf Git-HEAD `766978d1`; die neuen Texte sind kein Nachweis für den unveränderten Git-Commit.

- Zuständigkeiten und Änderungsbezüge in der [Pflegematrix](../../../docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) zusammengeführt.
- Roadmap, Glide-System, Architektur, Shell-Konzept, Funktions-/Daten-/Prüfverträge und Einstiege auf diese Quelle ausgerichtet.
- Doppelte Modulaufzählungen im Shell-Konzept durch Registerverweise ersetzt. Die Dokumente behalten ihre unterschiedlichen Aufgaben: Istarchitektur, Systembestand und Entkopplungsziel.
- Die tatsächliche `RedoHistory`-Grundlage und verbleibende App-Kopplungen gegenüber hypothetischen Shell-Schnittstellen präzisiert.
- Historische Bestandsaufnahmen, Originalaufträge und frühere QA-Nachweise erhalten; keine Fachdatei gelöscht. Die Konsolidierung betrifft überlappende Inhalte innerhalb bestehender Dokumente.
- Katalogkorrektur mit eigener Systemversion; keine neue App-/Datenformatversion und keine Änderung am ausführbaren Produktcode.

## Prüfung und Nachvollziehbarkeit

Die maschinenlesbaren Ergebnisse stehen in [ergebnis.json](ergebnis.json). Sie unterscheiden Baseline, finalen Dokumentationsabgleich, vorhandene Systeminventarprüfung, CI-Grundstufe und Hashvergleich. Rohprotokolle und temporäre Dokumentvergleiche bleiben außerhalb des Repositorys.

Die ergänzende lokale Linkprüfung erfasst Markdown-Verweise und HTML-Navigation einschließlich Abschnittsankern. Die bestehende Standprüfung erfasst im Git-Checkout nur bereits versionierte Dateien; der neue Contributing-Einstieg und dieser Nachweis werden deshalb zusätzlich geprüft. Externe URLs werden in dieser Runde nicht auf Erreichbarkeit oder Aktualität geprüft.

**Ergebnis:** 76 einbezogene Dokumente, 1.811 lokale Verweise und 438 Abschnittsverweise ohne Befund; Systeminventarprüfung 5/5. Der dritte, eingefrorene CI-Grundstufenlauf unter Python 3.14.7 auf Windows besteht mit 19/19 Schritten einschließlich strengen Lieferabgleichs. Die Werkzeugtests umfassen 286 Fälle mit einem Skip; beide Fachlogikdurchläufe führen jeweils 1.174 Fälle erfolgreich aus. Der Hashvergleich über 201 Code-/Versionsdateien zeigt als einzige Änderung die beabsichtigte Systemkatalogversion; die übrigen 200 Dateien einschließlich App und aktiver Python-Lieferung sind unverändert.

**Frühere Versuche bleiben rot:** Versuch 1 stoppte nach den Werkzeugtests am Integritätswächter, weil während des Laufs Zeilenenden in zwölf Dokumenten vereinheitlicht wurden. Der Werkzeugprozess selbst meldete Exitcode 0. Versuch 2 scheiterte im Durchlauf ohne Systemzeitzonen mit 16 Fehlern an Ausgabeorten oberhalb der bestehenden 130-Zeichen-Grenze; die Folgeprüfungen wurden übersprungen. Versuch 3 verwendet bei unverändertem Produktcode eine kürzere Prüfablage. Eine zwischenzeitlich falsch gesetzte neue Abschnittsverknüpfung wurde vor dem finalen Linkabgleich berichtigt.

Der Abschlussnachweis selbst wurde nach dem eingefrorenen CI-Lauf um dessen Ergebnisse ergänzt; die produktiven Quellen blieben dabei unverändert. Die ergänzende Dokumentationskontrolle ist im maschinenlesbaren Ergebnis separat ausgewiesen.

## Grenzen

Keine neue vollständige UI-/Plattformmatrix, kein nativer Paketbau und keine menschliche Abnahme. Die Strukturprüfung beweist weder, dass jede fachliche Aussage mit allen Codepfaden übereinstimmt, noch erzwingt sie die redaktionelle Pflege bei künftigen Änderungen automatisch. Die Pflegematrix ist der verbindliche Arbeitsablauf; automatisierte Inventar-/Linkprüfungen ergänzen ihn.

Dieser Auftrag umfasst keine Git-Veröffentlichung. Bestehende lokale Änderungen bleiben erhalten; frühere rote Ergebnisse, Skips und offene Freigaben werden nicht umgedeutet. Maßgeblich bleibt der [QA-Bericht](../../../docs/07_QA_BERICHT.md).

## Git-Folgeauftrag (13.11.2026)

Der Inhaber hat anschließend Commit und Push der Dokumentationsänderungen beauftragt. Die Veröffentlichung wird auf dem neueren `origin/main` `97dd55cf` vorbereitet; andere lokale Änderungen bleiben erhalten. Die erste Grundstufe mit nun vorgemerkter `CONTRIBUTING.md` scheiterte an deren fehlender Standzeile (R1). Die Standzeile ist ergänzt; der gezielte Nachlauf besteht für 76 Dokumente. Dieser zusätzliche Rotlauf ist im maschinenlesbaren Nachweis erhalten. Die früheren Ergebnisse oben bleiben ihrem damaligen Arbeitsstand zugeordnet.

**Finale Veröffentlichungsprüfung:** Die wiederholte strenge CI-Grundstufe auf Basis `97dd55cf` besteht mit 19/19 Schritten. 76 Dokumente sowie 1.812 lokale Verweise und 439 Abschnittsverweise sind ohne Befund. Die zusätzliche Standzeile ist nun auch durch die reguläre Git-basierte Standprüfung erfasst. Die Berichtsergänzung enthält nur diese Prüfergebnisse; ausführbarer Code und App-Version bleiben gegenüber der Veröffentlichungsbasis unverändert.
