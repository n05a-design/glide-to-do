# Globale Ablage- und Dokumentationsprüfung vom 18.10.2026

Glide 3.43.1 · Format 25 · Prüfkandidat auf FP-01 mit WA-27–WA-30.

## Umfang und Verfahren

Die Projektwurzel wurde rekursiv einschließlich versteckter Git-Daten und fünf lokaler Arbeitskopien inventarisiert: 17.898 Dateien, 1.325 Ordner, keine Verknüpfungen und keine Inventurfehler. Für alle Ausgangsdateien liegen vollständige SHA-256-Werte vor. Das Register erfasst 594 Markdown-/Textdokumente mit 148 unterschiedlichen Texten. Der Inhaltsabgleich unterscheidet zuständige Quellen, historische Belege, Aufträge und Fremdcodehinweise. Quellcode und Binärdateien werden nach Funktion, Provenienz, Versionsbezug und Integrität bewertet; ein Hashvergleich ist keine vollständige Funktionsabnahme jedes Binärinhalts.

Der Auftrag umfasst diese Projektablage, nicht das gesamte Benutzerkonto, andere Laufwerke oder echte Glide-Nutzerdaten. Versteckte und ignorierte Dateien gehören zur Inventur. Ihre Nichtversionierung ist keine Löschfreigabe.

## Nachweise

- [Inventar vor Bereinigung](inventar_vorher.json), [vollständige Ausgangshashes](dateihashes_vorher.json), [Dokumentregister](dokumentregister.json).
- [Bereinigungsplan und Schutzgrenzen](bereinigungsplan.json), [gesicherte Ausgangsstände](sicherungsmanifest.json), [Integrationsabgleich](schutzrunde_integration.json), [Dokumentkonflikte](integration_konflikte.json).
- [Dokumentänderungen](dokumentaenderungen.json): aktuelle Quellen fortgeschrieben, doppelte Erzählungen zusammengeführt.
- [Git-Verdichtung und Integritätsvergleich](git_verdichtung.json): ohne Ablauf von Reflogs, ohne Objekt-Pruning; vorherige Objektmenge und Verweise unverändert.
- [Sechs Git-Temporärdateien](git_temp_journal.json): wegen automatischer Freigabeablehnung erhalten; der erfolglose erste Löschversuch wurde im Journal richtiggestellt.
- [Arbeitskopien vor Bereinigung](worktree_vorpruefung.json): eigene Änderungen und ignorierte lokale Nachweise gesondert geprüft.

## Aufbewahrung und Grenzen

Erhalten bleiben alle sieben vorhandenen QA-Versionen, insbesondere die Bilder der drei neuesten Versionen, 28 originale Eingangsreferenzen, Migrationsfixtures, Grafikmaster, vorhandene Pakete, 07 und Showcase. Der historisch blockierte Affinity-Bestand wird nicht gelöscht. Wiederherstellbare Git-Zweige und Stashes bleiben erhalten; aktuelle uncommittete Ausgangsstände sind zusätzlich außerhalb der Projektwurzel gesichert. Private Sicherungsorte und Rohprotokolle bleiben lokal.

Der Quellkandidat bleibt Version 3.43.1 / Format 25, App-SHA-256 `f74af723e3fe1fc18aae5beafcef3d026a3a9c39d8eb16c90b68fb3ae7ddec26`. Die Lieferung 07 bleibt bewusst unverändert auf App-SHA-256 `ed2b7eb64cc3fc14f00a4e909c7693c34102e46e393b5937158bb7d7e25176d3`, Pakete auf 3.42.0. Native und menschliche Abnahmen sowie eingefrorener Produktionsphasenabschluss bleiben offen. Ein Commit/Pull Request ist keine Releasefreigabe.

## Primärquellen zur Bereinigung

Die Verfahren wurden gegen die offiziellen Git-Dokumentationen zu [worktree](https://git-scm.com/docs/git-worktree.html), [gc](https://git-scm.com/docs/git-gc) und [cat-file](https://git-scm.com/docs/git-cat-file) geprüft. Microsoft erläutert [OneDrive-Dateibedarf](https://support.microsoft.com/en-us/onedrive/save-disk-space-with-onedrive-files-on-demand-for-windows), [Dateiattribute](https://learn.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants) und [belegte Dateigröße](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getcompressedfilesizew). OneDrive-Löschen wird synchronisiert; das Projekt wird nicht bloß durch Auslagern offline benötigter Dateien verkleinert.

## Nicht ausführbare Bereinigung

Das Entfernen der fünf geprüften Arbeitskopien bleibt ausstehend. Der Git-Versuch an der ersten Kopie scheiterte mit Zugriffsfehler; den anschließenden geprüften Windows-Löschversuch lehnte die automatische Freigabeprüfung mit „blocked by policy“ ab. Kein Umgehungsversuch. [Tatsächliches Journal](worktree_journal.json). Der Schutzstand ist zusätzlich im Stash `fc280e880d23eef69565de3551410d48971cfabf` gesichert. Die sechs Git-Temporärdateien bleiben ebenfalls erhalten.

## Abschluss und Validierung

Die [Abschlussbilanz](ergebnis.json) verbindet die [erneute Inventur](inventar_nachher.json), [Bestandsvalidierung](bestandsvalidierung.json), [dateiweise Bewertung](dateibewertung.jsonl), [Ordnerbewertung](ordnerbewertung.json) und [Dokumentbewertung](dokumentbewertung.json). Für jede der 17.898 Ausgangsdateien und jeden der 1.325 Ausgangsordner ist eine Entscheidung erfasst. Der Inhalt großer Binärdateien wird durch Integrität, Provenienz und die zugehörigen Anwendungstests bewertet; es wird keine manuelle Prüfung jedes Bytes behauptet.

Die [Grundprüfung nach Integration](ci_integration/ergebnis.json) bleibt mit zwei damaligen Dokumentbefunden rot: Das neue Linkziel war beim frühen Prüfschritt noch nicht angelegt; der gestrafften Übergabe fehlte der explizite Kürzungsvermerk. Beide Punkte sind korrigiert. Der [erste gezielte Nachlauf](ci_nachlauf/ergebnis.json) und der [abschließende Nachlauf](ci_abschluss/ergebnis.json) prüft Syntax, Version, Dokumentation, Stand, Datenschutz, Aufbewahrung und Synchronisation am aktualisierten Stand. Die [zusammengeführte Prüfmatrix](validierung_gesamt.json) benennt für jeden der 19 Schritte seinen tatsächlichen Nachweis; sie überschreibt keinen Vorlauf und behauptet keinen neuen eingefrorenen Komplettlauf. Alle 754 Fachtests, nochmals 754 ohne Systemzeitzonen und 152 Werkzeugtests bestanden; [zehn Schutzfälle](schutzrunde_integriert.json) wurden in der Hauptarbeitskopie erneut ausgeführt. Die [abschließende Linkprüfung](links_abschluss.json) über 68 Markdown-Dateien fand bei 872 lokalen Verweisen weder fehlende Dateiziele noch ungültige Überschriftenziele.

Alle 783 geschützten Ausgangsdateien sind hashgleich, darunter die 28 Originalreferenzen. Keine ursprüngliche Hauptdatei fehlt. Alle 12.213 ursprünglichen Git-Objekte und die bisherigen Branch-/Tag-/Remoteverweise sind erhalten; die zusätzliche Schutzsicherung liegt als weiterer Stash vor. Die endgültige Speicherbilanz ist eine Projektmessung vor dem Commit; neue Git-Objekte und laufende Protokolle können sie geringfügig verändern.

Speicherbilanz vor Commit: 4.204.720.865 → 2.531.020.407 Byte Projektdateien, netto 1.673.700.458 Byte beziehungsweise 1,559 GiB weniger, einschließlich der neu angelegten Nachweise. Die fünf Arbeitskopien und sechs Git-Temporärdateien bleiben als blockierter Rest bestehen; ihre noch mögliche Einsparung ist nicht in diesem Erfolg enthalten.
