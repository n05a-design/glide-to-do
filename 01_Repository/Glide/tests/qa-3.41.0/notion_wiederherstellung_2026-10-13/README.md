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

Die Mac-Vollprüfung auf eingefrorener Kopie, Lieferabgleich, Bundle, Signaturen und native Linux-/Windows-Matrix folgen.
Tatsächliche menschliche Bedienung bleibt ein gesondertes Abnahmetor.
