# Oberfläche und Schreibschutzmeldung – Glide 3.50.0, 02.11.2026

Nutzerauftrag: große Überschriften verkleinern; verschobene Block-Einfügemarke korrigieren; Listen-/Tabellen-/Pinnwandbuttons als Symbole; brauchbare Zeilenaktionen; Hintergrund-Speicherproblem untersuchen. [Plan §21.47](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2147-oberflächenkorrekturen-und-schreibschutzmeldung).

## Umsetzung

- Gemeinsame große Titelstufe 24 → 22, einschließlich Notiz-H1, unabhängig von Fensterbreite. Fließtext und nachgeordnete Stufen bleiben erhalten.
- Block-Einfügemarke nutzt `PageEditor.place_at` wie Bilder und Blockgriff: Tk 9 zählt Text-Innenabstände bei `place` mit, Tk 8.6 nicht. Beide Achsen werden korrigiert.
- Ansichten: ☷ Liste, ⊞ Tabelle, ▨ Pinnwand. Zentraler Symbolvertrag mit lesbaren Rückfällen, Klartextnamen/Tooltips, aktiver neutraler Hervorhebung und bestehenden Tastaturwegen.
- Explizite Symbolknöpfe erhalten ihren Symboltext auch beim ASCII-Rückfall; `...` wird dort nicht zu „Mehr“. Zeilenaktionen 32 × 32 px, passender reservierter Rand, keine Metadatenüberdeckung; übrige Textknöpfe behalten ihre Breiten- und Beschriftungsregeln.
- Bewusst angeforderter Einstellungs-Speichervorgang meldet Schreibschutz. Hintergrundfarbe/-verlauf werden bei Misserfolg im Modell zurückgesetzt; kein verfrühtes Erfolgssignal.

## Prüfbelege

[Baseline Beta350](baseline_beta350.json) und [Wiederanlauf](baseline_wiederanlauf.json) vor Produktionsänderung grün. Ergänzte Geometrie-/Rückmeldungsprüfungen gegen die Vorfassung gezielt rot: [Einfügemarke](rot_einfuegemarke.json), [Zeilenaktion](rot_zeilenaktionen.json), [gesperrter Hintergrundwechsel](rot_speichermeldung.json). [Geometrie vorher](geometrie_vorher.json): 81 px nach rechts und 18 px nach unten versetzte Einfügemarke; Rückfall „Mehr“ überläuft 28-px-Zeilenknopf. [Geometrie nachher](geometrie_nachher.json): beide Achsen 0 px Abweichung, native Symbole innerhalb von 32-px-Flächen.

[Beta350](beta350.json), [Ansichtssymbole und Tastatur](ansichtssymbole.json), [Wiederanlauf/Restore](wiederanlauf.json), [Gestaltung](gestaltung.json) und [appweiter Knopfschutz](b15_appweit.json). Alle Bedienfälle verwenden synthetische Daten mit temporärem `GLIDE_DATA_DIR` vor dem Import. [Native Geometrie/Symbole](native_geometrie.json): 16 Kombinationen Hell/Dunkel × mittel/groß × 860/1280 px × Lesebreite/volle Breite, jeweils 0 px X-/Y-Versatz; große Titel mit 22–23 gemessen, zentrale Grundstufe 22 statt zuvor 24. Alle sechs geprüften Symbole tatsächlich aus DejaVu Sans. [Sichtprobe](sichtprobe.py), eigene Fensterbilder lokal unter `fensterbilder/`. [Kopf/Titelkante](kopfverweise.json) und [Kompaktmodus](kompakt.json) grün; [Aufgaben-/Tabellenregressionen](bereichsregression.json) ebenfalls. Gestaltung 211 und appweiter Knopfschutz 1.120 Knopfprüfungen grün; zwölf Wiederanlauf-/Restorefälle grün. [CI-Grundstufe](grundstufe.json): 19 Schritte grün, 1.113 Fachtests zweimal (je ein Skip), 238 Werkzeugtests (drei Skips), 444 aktive lokale Dokumentlinks, strenger Lieferabgleich und 116 Vendor-Originaldateien. [Abschluss](ergebnis.json).

## Speicherdiagnose

Nur technische Metadaten aus Sitzungs- und Abschlussprotokollen gelesen, keine echten Aufgaben/Einstellungen geändert. Der Start am 02.11. um 16:04 Uhr hat keinen Abschluss; sein Prozess existiert nicht mehr. Spätere Starts endeten sauber, gaben den geschützten Bestand aber nicht automatisch frei. Die Abbruchursache ist weiterhin unbewiesen (WA-41). Die Größenanzeige begründet diesen Schutz nicht. [Datensparsame Diagnose](speicherdiagnose.json).

Paketprobe und verwendete UI-Prüfhelfer setzen den temporären Datenpfad bereits vor dem App-Import; Marker und Diagnosen liegen dann ebenfalls dort. Aus den vorliegenden Metadaten lässt sich keine Ursache durch die Prüfungen belegen oder ausschließen. Reale Wiederanlaufsperre unverändert: Speicherstatus → Bestand freigeben, nach bewusster Bestätigung und bytegleicher Originalvorsicherung. Die automatische Freigabe wurde weder eingeführt noch ausgeführt.

## Lieferstand und Grenzen

Quelle 3.50.0, Aufgabenformat 26 und Einstellungen 2 unverändert; begrenzter UI-Nachlauf ohne neue Laufzeitabhängigkeit. Python-Fassung bytegleich abgeglichen (91 Code-/147 Ressourcen-/Vendordateien). Native Mac-App mit eigener Tk 9.1 gebaut, 463 installierte Paketdateien gegen Bauinventar und Ad-hoc-Signatur geprüft; beide isolierten Paketstarts ohne externes Python grün. Aktive App `~/Applications/Glide.app`, über den bestehenden Link auch `build/macos/Glide.app`; Vorfassung unter `~/Applications/Glide-vor-Oberflaeche-20261102.app` erhalten. Kandidaten-TAR separat unter `build/macos/Kandidaten`, ursprüngliche öffentliche Archive unverändert. [Bau](mac_bau.json), [Start des Baus](mac_start_bau.json), [Lieferabgleich](mac_lieferung.json), [Start der installierten App](mac_start_lieferung.json); Hashes im [Abschluss](ergebnis.json). Windows-EXE bleibt beim ursprünglichen öffentlichen 3.50-Stand. Kein neuer vollständiger Matrixlauf, keine menschliche DPI-/Mehrmonitorabnahme; Reader nach D58 bis Bedarf zurückgestellt. Frühere Nachweise behalten ihre ursprünglichen Eingangsbytes.
