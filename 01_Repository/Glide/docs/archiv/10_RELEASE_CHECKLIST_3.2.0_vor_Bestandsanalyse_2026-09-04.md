# Release-Checkliste

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

## Source und Qualität

- [x] `VERSION`, `APP_VERSION`, Changelog und Dokumentversion stimmen überein (3.2.0).
- [x] Syntaxprüfung, Integrationstest, Datenintegritätstest und app-weiter Durchlauf (`audit_app.py`) sind grün.
- [x] Referenzbestände der Formate 10, 9, 8, 7, 6, 5, 4 und 2 laufen durch die aktuelle Normalisierung.
- [x] Keine Umbauaktion verliert einen Punkt (Bestandswächter plus 130 geprüfte Gruppen-Kombinationen).
- [x] Statische Analyse und Erreichbarkeitsanalyse ohne offene Befunde: 0 nie genannte Namen, 0 strukturgleiche Methodenpaare.
- [x] Sichtprüfung hell und dunkel erzeugt und angesehen (`50_Ablage/Screenshots/3.2.0/`).
- [ ] `pyflakes` erneut ausgeführt – in der Prüfumgebung von 3.2.0 nicht verfügbar, zuletzt zu 2.11.0 ohne Meldung.
- [ ] Zufallsläufe wiederholt – die Werkzeuge von 2.11.0 sind nicht im Repository erhalten (siehe QA-Bericht, Abschnitt 2.5).
- [ ] Strg+Klick als Mehrfachauswahl unter Windows und Cmd+Klick unter macOS am echten Gerät bestätigt.
- [ ] Das zu 3.0.1 gemeldete Einfrieren auf Windows bestätigt oder ausgeschlossen. **Ursache gefunden und behoben, aber nie reproduziert** – siehe QA-Bericht, Abschnitt 3.1.
- [ ] Darstellung der Textzeichen `⊕` (Anhang) und `▦` (Fälligkeit) in den echten Systemschriften geprüft.
- [ ] Manuelle Windows-/macOS-Matrix ist dokumentiert.
- [ ] Migration, Backup und Restore wurden mit Kopien echter Testdaten geprüft.

## Produktidentität

- [ ] Publisher, Copyright, Supportkontakt, Website und Datenschutz-URL festgelegt.
- [ ] Lizenzmodell rechtlich freigegeben. `LICENSE.md` ist bis heute ein **Platzhalter**.
- [ ] Windows AppUserModelID und stabile Inno-Setup-AppId festgelegt.
- [ ] macOS Bundle Identifier, Mindestversion und Architektur festgelegt.
- [ ] Namens-/Markenrisiko „Glide" professionell geprüft.

Der technisch belegte Teil dieser Angaben steht in
`decisions/PRODUCT_IDENTITY.md` und ist auf 3.2.0 nachgeführt; offen sind
ausschließlich Geschäfts- und Rechtsentscheidungen.

## Build und Distribution

Nichts davon existiert bisher. `packaging/` ist leer.

- [ ] Build-Abhängigkeiten gepinnt.
- [ ] PyInstaller-OneDir-Konfiguration reproduzierbar.
- [ ] App-Icon vorhanden – `assets/branding` ist leer.
- [ ] Windows-Installer und macOS-App/DMG auf Clean Machines geprüft.
- [ ] Windows signiert und Zeitstempel verifiziert.
- [ ] macOS signiert, notarisiert, gestapelt und per Gatekeeper geprüft.
- [ ] macOS-Sandbox-Entitlements geprüft, falls Mac App Store angestrebt wird.
- [ ] SHA-256-Manifest und Release Notes erstellt.
- [ ] Finale Binärartefakte ausschließlich unter äußerem `30_Release_Exports/<Version>/` abgelegt.

## Store-Vorbereitung

- [x] Datenschutzfragebogen beider Stores ist beantwortbar: keine Datenerhebung, kein Netzwerkzugriff, kein Konto, keine Telemetrie.
- [ ] Produktdatenblatt auf 3.2.0 nachgeführt – vorhanden ist `40_Store_Material/Produktdatenblatt_2.6.0.md`, also **vier Minor-Versionen alt**.
- [ ] Screenshots in den geforderten Auflösungen erstellt. Die vorhandenen Aufnahmen stammen aus der Linux-Prüfumgebung und taugen nicht als Store-Material.
- [ ] Store-Texte redaktionell freigegeben.
- [ ] Altersfreigabe-Fragebogen ausgefüllt.

## Status 3.2.0

Syntaxprüfung, die drei Testsuiten, beide Analysewerkzeuge und die Sichtprüfung
sind grün. Funktional und im Datenformat ist der Stand fertig; die letzten
beiden Versionen waren reine Aufräum- und Konsolidierungsrunden ohne neue
Bedienfunktion.

Neu automatisiert geprüft gegenüber 2.11.0:

- gemeinsamer Änderungsrahmen (`item_change`, `sidebar_change`) einschließlich
  der Zusage, dass eine wirkungslose Aktion keinen Rückgängig-Schritt hinterlässt;
- Kürzung des Rückgängig-Speichers ohne Verlust des ältesten Schritts;
- Griff-Rückgabe nach einem modalen Unterdialog;
- Symboltabelle ohne Emoji;
- der mitgelieferte Beispielbestand über den echten Importweg.

**Kein öffentliches Stable-Release.** Es fehlen: die vollständige manuelle
Prüfung auf Windows und macOS, jede Form von Packaging und Signing, die
Produktidentität und die Store-Materialien. Der kritischste offene Punkt für die
Qualität ist die Bestätigung, dass das gemeldete Einfrieren behoben ist – das
kann nur die Benutzung auf einem Windows-Gerät zeigen.
