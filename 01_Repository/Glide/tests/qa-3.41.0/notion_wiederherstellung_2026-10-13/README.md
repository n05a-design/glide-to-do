# Notion-Import und Seitenwiederherstellung – Nachweisrahmen

Stand 13.10.2026 · Glide 3.41.0 · Aufgabenformat 25

Paket 6 setzt D26/D39/D37 im bestätigten Rahmen um: Notion-Export „Markdown & CSV“ mit Vorschau, ausdrücklicher Auswahl, Verlustbericht, Originalarchiv und Vorsicherung; spätere Exporte mit Wiedererkennung und Konfliktfreigabe; einzelne Seite aus einer Sicherung mit Vergleich, Anhängen, Aufgabenverweisen und Live-Listen. Datenformat 25 für Quellenzuordnungen mit Vorsicherung, Migration und schreibgeschütztem Altleser. Grundlage ist der private Codex-Entwurf; übernommen, an 3.40.0 angepasst und an den unten genannten Stellen korrigiert.

Gezielte Proben vor dem Einfrieren:

- [Pflichtsuite `test_import3410`](gezielt.json): sechs Gruppen grün (Erstimport, Wiederimport/Konflikt, selektiver Restore, Vorsicherungs- und Schreibfehler, Vorschauen bei 860 × 700 in Hell/Dunkel, Migration/Altleser), keine Callbackfehler.
- [Gegenprobe gegen 3.40.0](gegenprobe_3400.json) rot; die Vorversion kennt keinen Notion-Import.
- [Vier Defektgegenproben](defektgegenproben.json), je passend rot: lokale Änderung nicht als Konflikt erkannt, CSV-Datenbank fehlt im Verlustbericht, Seitenrestore ohne Vorsicherung, fehlende Format-25-Vorsicherung.
- 638 Unit-Tests grün, mit und ohne Systemzeitzonen; darunter 147 neue für Archivlesen, Import-, Wiederimport-, Hierarchie-, Quellen- und Restoreregeln. `test_animation3400` bleibt im neuen Format grün.
- [Eigene Fenster in Hell und Dunkel tatsächlich betrachtet](fenster.json); PNGs nur lokal, künstliche Daten.
- [Auslaufende QA-Nachweise 3.35.0](aufbewahrung3350.json): 20 Dateien bytegleich zum Commit, auf den QA-Bericht und Übergabe nun verweisen.

Korrekturen gegenüber dem Entwurf:

- Drei Abschnitte des Entwurfs trafen auf den Paket-5-Stand und wurden von Hand übertragen.
- Der Migrationsfall bildete einen Format-24-Bestand nach, behielt aber am Ordner die Format-25-Zuordnung; die App wies ihn zu Recht ab. Der Test entfernt jetzt auch diese Zuordnung.
- Die Paket-5-Probe prüfte die Ablehnung von Format 25; sie prüft jetzt das jeweils nächste Format.
- Beide Vorschauen nutzten native ttk-Tabellen und -Leisten; jetzt Glide-Dialogtabelle und -Leisten.

Der [erste eingefrorene Volllauf](mac_vorlauf.json) endete mit drei Befunden: `prepare_additive_import` arbeitet seit dem Entwurf auf unabhängigen Kopien (Quellenzuordnungen dürfen beim Hinzufügen nicht mitwandern), `test_woche33317` und `test_seiten33318` lasen aber die übergebenen Einträge; die Attributprüfung beanstandete `self.__dict__`. Die Tests nutzen jetzt den Rückgabewert wie der einzige App-Aufrufer, die Stelle verwendet `hasattr`/`del`. Vorsorglich nach dem nativen Befund von 3.40.0: `test_import3410` wartet höchstens 3 s auf die Anordnung von Knöpfen, `test_restore_assets` nutzt einen unter Windows gültigen Dateinamen. Die frische Vollprüfung ist unten belegt.

Mac-Abnahme und Lieferweg:

- [Frische eingefrorene Mac-Vollprüfung](mac_voll.json) am Kandidaten 56b9b98 außerhalb OneDrive: Exit 0, 106 ausgeführt/zwei übersprungen; alle 1042 eingefrorenen Dateien danach unverändert. Der rebasierte Kandidat trägt denselben Code, dieselben Tests und Fixtures; hinzu kamen nur Dokumente und Belege des Lieferabschlusses 3.40.0.
- [Produktionsübernahme](produktionsuebernahme.json), [215 Lieferdateien](lieferung.json), [123 Bundle-Dateien und beide Signaturen](bundle.json). 3.40.0 liegt im Archiv.

Der [erste native Lauf](https://github.com/n05a-design/glide-to-do/actions/runs/38388529406) endete rot. Drei Ursachen werden im Nachlauf vom 13.10.2026 korrigiert:

- Anhangsrollback: Gerät/Inode allein unterscheiden auf Linux eine inzwischen eingesetzte Verknüpfung bei wiederverwendeter Inode nicht. Zusätzlich den Dateityp prüfen; die bestehende Gegenprobe erzwingt die Wiederverwendung auch auf dem Mac und scheitert mit dem unveränderten Vorgänger passend.
- Altleser: Ein Kindprozess mit der Hauptdatei im Archiv muss die Begleitmodule im übergeordneten Lieferordner finden; auf Linux und Windows scheiterte zuvor der Import von `drawing`.
- ZIP-Pfade: Testarchive bewahren Backslashes unverändert. Auch der ZIP-Leser normalisiert sie unter Windows und kürzt Nullbytes; der Produktionsparser prüft deshalb `orig_filename` vor jeder Nutzung. Gegenproben mit beiden Plattformtrennzeichen und Nullbytes scheitern mit dem unveränderten Vorgänger passend.

[31 betroffene Unit-Tests und passende rote Vorgängerproben](korrektur_gegenproben.json) sowie die [gezielte Importprüfung mit sechs Gruppen](korrektur_gezielt.json) sind grün. Ein begonnener Mac-Volllauf wurde nach Ergänzung der ZIP-Originalnamenprüfung gezielt beendet (Exit 143); er gilt ausdrücklich nicht als Abnahme.

Die [frische eingefrorene Mac-Vollprüfung](mac_korrektur_voll.json) ist vollständig grün: Exit 0, 106 ausgeführt/zwei übersprungen, 89 Integrationssuiten/638 Units. [Alle 1.064 eingefrorenen Dateien sind unverändert](korrektur_quellstand.json); Code und Tests stimmen mit der Arbeitskopie überein. Die Hauptdatei bleibt am Hash 4dedf0c5; die geänderten Begleitmodule `notion_archive.py` und `restore_assets.py` sind mit eigenen Hashes belegt. [215 Lieferdateien](lieferung_korrektur.json) und [123 Bundle-Dateien](bundle_korrektur.json) bytegleich; Signaturen im Bauordner und auf frischer Rückkopie grün. Die früheren Belege oben bleiben für ihren damaligen Stand erhalten.

[Strenge lokale CI-Grundstufe](ci_korrektur.json) grün, einschließlich Werkzeugtests, 638 Units mit und ohne Systemzeitzonen, Startprobe und bytegleichem Lieferstand. Der Fremdcode-Originalabruf blieb wegen des bekannten lokalen SSL-Zertifikatsfehlers ein Hinweis; die native CI führt ihn erneut aus.

[Native Wiederholung 38441333442](https://github.com/n05a-design/glide-to-do/actions/runs/38441333442) am Kandidaten `1bc2db1` vollständig grün: [Grundstufe](grundstufe_native_korrektur.json) 19 ausgeführt, [Linux-Vollprüfung](linux_korrektur_voll.json) und [Windows-Vollprüfung](windows_korrektur_voll.json) je Exit 0, 107 ausgeführt/eine menschliche Sichtprüfung übersprungen. [18 Linux-Defektgegenproben](linux_defekt_korrektur.json) passend rot; [Job-/Laufzeitnachweise](native_final_korrektur.json). Windows Python 3.14.7/Tk 9.0.4, Referenzdesktop 1920 × 1080; Linux Python 3.14.8. Der native Originalabruf bestätigt alle 116 Vendor-Dateien bytegleich und räumt den lokalen SSL-Hinweis aus.

[Lieferabschluss](lieferabschluss.json): 215 Liefer-/123 Bundle-Dateien nach der Matrix erneut bytegleich, Ad-hoc-Signaturen im Bauordner und auf frischer Rückkopie erneut grün. Frühere rote und grüne Belege bleiben an ihren ursprünglichen Code-/Prüfständen erhalten.
[Abschließende strenge Liefer-CI](ci_lieferabschluss.json) grün; Appcode und Tests seit der nativen Matrix unverändert. Tatsächliche menschliche Bedienung bleibt ein gesondertes Abnahmetor.
