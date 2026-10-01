# Release-Checkliste

Stand: 04.09.2026 · App-Version 3.3.0 · Datenformat 10

## Source und Qualität

- [x] `VERSION`, `APP_VERSION`, Testprüfung und Changelog nennen 3.2.0.
- [x] Syntax und drei automatisierte Suiten auf Windows geprüft; Details und
  Testkorrekturen in `07_QA_BERICHT.md`.
- [x] Referenzbestände Schema 10, 9, 8, 7, 6, 5, 4 und 2 erhalten.
- [x] Bestandswächter und 130 Gruppen-Kombinationen automatisiert geprüft.
- [x] Statische und Erreichbarkeitsanalyse ausgewertet; keine automatischen
  Löschungen aus Erreichbarkeitsvermutungen abgeleitet.
- [x] Dokumente und Produktdatenblatt auf tatsächlichen Stand 3.2.0 abgeglichen.
- [ ] Vollständige manuelle Windows-/macOS-Matrix abgeschlossen.
- [ ] Einfrieren bei längerer Windows-Benutzung reproduziert oder belastbar
  ausgeschlossen; ursprüngliche Fehlermeldung weiterhin nicht verifiziert.
- [ ] Textzeichen, mehrfache DPI/Monitore und reale Eingabegeräte geprüft.
- [ ] Drei Emoji-Ausnahmen zur Textzeichen-Vorgabe entschieden und geprüft;
  bei Gruppenmarkern TXT-Kompatibilität bewahren.
- [ ] Backup und Restore mit Kopien realer Daten und Anhänge geprüft.
- [ ] Große Bestände auf Zielgeräten vermessen.
- [ ] Tiefenschutz vor sämtlichen tiefenerhöhenden Punktänderungen absichern.
- [ ] Labelgrenze bei Wechsel der Punktart inklusive festem Artlabel einhalten.
  Beide Lücken sind in `11_BESTANDSANALYSE.md` reproduziert dokumentiert.

## Produktidentität

- [ ] Publisher, Copyright, Supportkontakt, Website und Datenschutz-URL festgelegt.
- [ ] Lizenzmodell und Preis entschieden; `LICENSE.md` ist weiterhin Platzhalter.
- [ ] Windows-Zielarchitektur, AppUserModelID und stabile Installer-ID festgelegt.
- [ ] macOS Bundle Identifier, Mindestversion und Architektur festgelegt.
- [ ] Namens-/Markenrisiko „Glide“ fachlich geprüft.

Technische Fakten und offene Entscheidungen: `decisions/PRODUCT_IDENTITY.md`.

## Build und Distribution

`packaging/` enthält eine Vorbereitungserklärung und Verzeichnisse; konkrete
Build-Konfigurationen und freigegebene Binärartefakte fehlen.

- [ ] Build-Abhängigkeiten gepinnt und reproduzierbarer PyInstaller-OneDir-Build.
- [ ] App-Icons aus freigegebenem Gestaltungsmaster abgeleitet.
- [ ] Windows-Installer und macOS-App/DMG auf Clean Machines geprüft.
- [ ] Windows-Binärdateien/Installer signiert und Zeitstempel verifiziert.
- [ ] macOS Developer-ID-Verteilung signiert, notarisiert, Ticket angeheftet
  und Gatekeeper geprüft.
- [ ] Falls Mac App Store: separater Sandbox-/Entitlement-/Zugriffsworkflow geprüft.
- [ ] SHA-256-Manifest und Release Notes für die tatsächlichen Binärartefakte.
- [ ] Finale Pakete unter äußerem `30_Release_Exports/3.2.0/` abgelegt;
  ein leerer Zielordner ist kein Buildnachweis.

## Store-Vorbereitung

- [x] Faktische Textgrundlage liegt im äußeren
  `40_Store_Material/Produktdatenblatt_3.2.0.md` vor.
- [x] Drei editierbare Arbeitslisten mit recherchierten Anforderungen und
  Quellen sind als gemeinsames Glide-Backup vorbereitet.
- [ ] Vertriebskanal je Plattform entschieden (Windows MSI/EXE oder MSIX;
  macOS direkte Verteilung oder Store).
- [ ] Datenschutzangaben gegen das endgültige Build einschließlich Installer,
  Website und optionalen Diensten geprüft und im jeweiligen Formular beantwortet.
- [ ] Zielplattform-Screenshots nach den gewählten Store-Vorgaben erstellt.
- [ ] Store-Texte, URLs und Altersfreigabe redaktionell/fachlich freigegeben.

## Status

3.2.0 bleibt ein interner Vorabstand. Automatisierte Source-Prüfungen sind kein
öffentliches Stable-Release. Vor Veröffentlichung fehlen insbesondere manuelle
Plattformabnahme, Produktidentität, reproduzierbare Builds, Signing und finale
Store-Materialien. Recherchierte Anforderungen sind mit Abrufdatum in den
Release-Arbeitslisten und Store-Unterlagen festgehalten und vor Einreichung
erneut zu prüfen.
