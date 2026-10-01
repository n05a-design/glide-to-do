# Release-Checkliste

## Source und Qualität

- [x] `VERSION`, `APP_VERSION`, Changelog und Dokumentversion stimmen überein (2.11.0).
- [x] Syntaxprüfung, `pyflakes`, Integrationstest, Datenintegritätstest und app-weiter Durchlauf (`audit_app.py`) sind grün.
- [x] Referenzbestände der Formate 10, 9, 8, 7, 6, 5, 4 und 2 laufen durch die aktuelle Normalisierung.
- [x] Keine Umbauaktion verliert einen Punkt (Bestandswächter plus 130 geprüfte Gruppen-Kombinationen).
- [ ] Strg+Klick als Mehrfachauswahl unter Windows und Cmd+Klick unter macOS am echten Gerät bestätigt.
- [ ] Manuelle Windows-/macOS-Matrix ist dokumentiert.
- [ ] Migration, Backup und Restore wurden mit Kopien echter Testdaten geprüft.

## Produktidentität

- [ ] Publisher, Copyright, Supportkontakt, Website und Datenschutz-URL festgelegt.
- [ ] Lizenzmodell rechtlich freigegeben.
- [ ] Windows AppUserModelID und stabile Inno-Setup-AppId festgelegt.
- [ ] macOS Bundle Identifier, Mindestversion und Architektur festgelegt.
- [ ] Namens-/Markenrisiko „Glide“ professionell geprüft.

Der technisch belegte Teil dieser Angaben steht bereits in
`decisions/PRODUCT_IDENTITY.md`; offen sind ausschließlich Geschäfts- und
Rechtsentscheidungen.

## Build und Distribution

- [ ] Build-Abhängigkeiten gepinnt.
- [ ] PyInstaller-OneDir-Konfiguration reproduzierbar.
- [ ] Windows-Installer und macOS-App/DMG auf Clean Machines geprüft.
- [ ] Windows signiert und Zeitstempel verifiziert.
- [ ] macOS signiert, notarisiert, gestapelt und per Gatekeeper geprüft.
- [ ] macOS-Sandbox-Entitlements geprüft, falls Mac App Store angestrebt wird.
- [ ] SHA-256-Manifest und Release Notes erstellt.
- [ ] Finale Binärartefakte ausschließlich unter äußerem `30_Release_Exports/<Version>/` abgelegt.

## Store-Vorbereitung

- [x] Faktische Produktangaben liegen als Datenblatt vor (`40_Store_Material/Produktdatenblatt_2.11.0.md`).
- [x] Datenschutzfragebogen beider Stores ist beantwortbar: keine Datenerhebung.
- [ ] Screenshots in den geforderten Auflösungen erstellt.
- [ ] Store-Texte redaktionell freigegeben.
- [ ] Altersfreigabe-Fragebogen ausgefüllt.

Status 2.11.0: Syntaxprüfung, `pyflakes`, der erweiterte Integrationstest, der neue
Datenintegritätstest und der
app-weite Durchlauf `audit_app.py` mit
einer Python-3.12/Tk-8.6-Laufzeit sind grün. Neu automatisiert geprüft sind verschachtelte Ordner mit Kreis- und
Tiefenschutz, Ablegezonen, Papierkorb-Rundlauf über ganze Zweige, der
mehrzeilige Long-Task-Text samt TXT-Rundlauf, die Bildlaufleisten der Dialoge
sowie – aus 2.8.0 – die
vier Aufgabenarten samt Gleichlauf von Art und festem Label, die Systemzeile
„Verspätet“, der Nummerierungsneustart unter einer Zwischenüberschrift, die
Umbruchlogik des Long-Tasks, die responsiven Spaltenbreiten, der Hover in beiden
Themes, der Sicherheitsbereich des Seitenleistenzählers und der erweiterte
Anlage-Dialog. Automatisiert geprüft sind zusätzlich der Papierkorb über seinen gesamten Lebenszyklus einschließlich der
Anhänge gelöschter Listen im Komplettbackup, das Label-Datenmodell mit Anzeige
und Austauschformaten, der gemeinsame Bearbeiten-Dialog, die Mehrfachauswahl in
der Seitenleiste, die Kalenderberechnung, der Autosave-Zyklus und die gesamte
Sicherungsrotation. Aus 2.6.0 bleiben Gruppen als Punktart, die Vollständigkeit
aller Kontextmenüs, eindeutige IDs beim Duplizieren, die Auswahl des schwersten
Schriftschnitts, kritische Anhangsdateinamen, der vollständige Backup-Rundlauf,
die Kopfzeilenbreite bei langen Titeln, die Fensterposition nach Monitorwechsel
und die plattformunabhängige Testisolierung abgedeckt. Vollständige manuelle Plattform- und
Sichtprüfung, Packaging, Signing, Store und Clean-Machine-Prüfungen bleiben
offen. Daher kein öffentliches Stable-Release.
