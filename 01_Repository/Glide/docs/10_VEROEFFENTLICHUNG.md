# Veröffentlichung – Glide

Stand 06.11.2026 · Glide 3.50.5 · Erster öffentlicher Stand (intern: öffentliche erste Beta) · Aufgabenformat 26

Alles für eine spätere Auslieferung an einem Ort: Releasecheckliste, Signierung, Vertrieb und Marke, GitHub-Auftritt, Lizenzentwurf, Inhaberangaben und Store-Material. Zusammengeführt am 03.10.2026 aus der Releasecheckliste, drei Entscheidungsdokumenten vom 21.09.2026 und dem Ordner `40_Store_Material` (aufgelöst); die Vorfassungen trägt Git. Kennungen und technisch belegte Werte stehen weiter im [Produktregister](decisions/PRODUCT_IDENTITY.md).

## Releasecheckliste

3.50.0 heißt öffentlich **Erster öffentlicher Stand**, intern **öffentliche erste Beta**. Dieser datierte Erstlieferstand trug in allen Ausgaben 3.50.0. Quelle und Python/Showcase werden inzwischen als 3.50.2 gepflegt; die vorhandenen nativen Pakete bleiben bei ihrem separat geprüften 3.50.0-Quellstand. Ein neuer Paketbau darf daraus nicht abgeleitet werden. Der [aktuelle QA-/Liefernachweis](07_QA_BERICHT.md) nennt die tatsächlich erzeugten Artefakte, Quellhashes und Prüfungen; eine Versionsbezeichnung ersetzt keine Abnahme.

- VERSION, `APP_VERSION`, Neuerungen, CHANGELOG, Handbuch und README auf denselben Nutzerstand bringen.
- Fach-/Werkzeugtests sowie vollständige eingefrorene Integrationsmatrix auf Mac, Linux und Windows ausführen. Nur unveränderte App-/Test-/Fixture-/Ressourcenbytes einem Ergebnis zuordnen.
- Python-Fassung bytegleich abgleichen, Showcase reproduzieren und getrennt prüfen; native Pakete mit Original-Lizenzbelegen bauen, kompilierten Quell-/Ressourcenabgleich und echte isolierte Startprobe durchführen.
- Actions auf Commit-SHA und Bauabhängigkeiten auf Version/Originalhash festlegen (WA-43/45). Herkunft von Runtime, tkDnD, Schriften und Zeitzonen beilegen; Paketprüfsummen dokumentieren.
- Die menschliche Prüfung erfolgt anschließend durch den Inhaber: Bedienung, Tastatur, Mindestgröße/große Schrift, DPI, mehrere Monitore und konkrete Plattformabläufe. **Screenreader ist bis Bedarf zurückgestellt und kein aktiver offener 3.50-Punkt.**
- Für einen allgemeinen signierten Vertrieb bleiben öffentliche Signatur/Notarisierung, freigegebene Lizenz, Kanalunterlagen und Markenprüfung gesonderte Voraussetzungen. Die neue Versionsbezeichnung erteilt keine Lizenz und ersetzt keine Zertifikate.

Der aktuelle Auftrag umfasst Commit und Push. Eine Veröffentlichung in weiteren Vertriebskanälen, rechtliche Festlegungen oder Eingriffe in die Git-Historie werden daraus nicht abgeleitet. Erinnerungen werden nur bei laufender App verarbeitet.

**Noch offene technische Releasevorbereitung (WA-46):** Lizenz-/Bauinventare und SHA-256-Dateilisten sind vorhanden; ein CycloneDX-/SPDX-Inventar samt automatisiertem Erzeugungs-/Prüfweg ist noch nicht umgesetzt. Vor einem entsprechend freigegebenen Release aus den vorhandenen Manifesten erzeugen und mit den tatsächlichen Artefakten abgleichen. Nicht als erfülltes Tor ausweisen. Neuere Fassungen von Bauwerkzeugen sind im [Abhängigkeitsabgleich](../tests/qa-3.50.0/abschlussabgleich_2026-11-02/README.md) dokumentiert; ein Upgrade verlangt neue native Bau-/Startbelege.

## Signierung und Notarisierung

Zertifikate, Zugangsdaten und Kennungen werden nicht erfunden und **nie im Repository gespeichert**.

**Windows:** Build und Installer reproduzierbar erzeugen → mit SignTool (Windows SDK) erst Binärdateien, dann Installer mit SHA-256 signieren, RFC-3161-Zeitstempel des Zertifikatanbieters → `signtool verify /pa /v <Datei>` für jedes Artefakt → Signatur, Herausgeber, Zeitstempel und SHA-256 im Release-Protokoll → Installation und Start auf sauberem System. Eine Signatur garantiert keine SmartScreen-Einstufung. Quellen: [SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool), [Authenticode-Zeitstempel](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures).

**macOS:** natives Bundle auf einem unterstützten Mac bauen und testen → mit Developer ID Application signieren, enthaltene ausführbare Komponenten einbeziehen → `xcrun notarytool submit <Archiv> --keychain-profile <Profil> --wait` (Zugangsdaten im lokalen Schlüsselbund) → nur bei `Accepted` `xcrun stapler staple` und `xcrun stapler validate` → Gatekeeper, Installation, Start, Datenablage und Update auf separatem System. Quellen: [Notarisierung](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), [Ablauf](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow).

Bisher wurde nichts signiert oder notarisiert außer der Ad-hoc-Signatur des Entwicklungsbundles.

## Vertrieb und Marke

- **Entschieden 27.09.2026 (E-10):** zuerst Direktvertrieb über die eigene Website; Stores später. macOS: Developer-ID-Signatur, Notarisierung, `.app` als Ordnerbundle, DMG, arm64 (Universal 2 nur, wenn Intel-Macs gebraucht werden). Windows: Installer mit Code-Signing, x64. Laufzeit Python 3.14 mit Tk 9.
- **Ergänzt 06.11.2026 (D64):** GitHub-Releases sind ein vorgeschalteter **Testkanal** für neue Testerinnen und Tester (Windows-ZIP und DMG, unsigniert, Vorabversion); die eigene Website bleibt erster Vertriebskanal. Der Windows-Installer aus E-10 ist noch nicht gebaut, der Testkanal liefert den Paketordner als ZIP.
- **Kanäle laut Auftrag:** GitHub, eigene Website, Social Media, Product Hunt, itch.io, Heise Software-Verzeichnis, winget; Microsoft Store gesondert prüfen. Keine Konten angelegt, nichts hochgeladen.
- Jeder Kanal braucht dasselbe geprüfte Artefakt, SHA-256-Prüfsumme, Versionshinweise, Systemvoraussetzungen, Kontakt und die freigegebene Lizenz.
- **Marke:** „Glide“ wird von mehreren Softwareanbietern genutzt. Vor einer Veröffentlichung professionelle Marken- und Namensrecherche durch einen Fachanwalt (I4). Ausgangspunkte: [DPMA-Recherche](https://www.dpma.de/marken/markenrecherche/index.html) (nur übereinstimmende Wortelemente, keine Ähnlichkeitsprüfung), [EUIPO/TMview](https://www.euipo.europa.eu/en/trade-marks/before-applying/availability). Eine Rechercheakte nennt Datum, Suchausdruck mit Varianten, Register, Waren-/Dienstleistungsklassen, Treffer, Inhaber, Status und Links.
- **Gismo** wird selbst produziert; die gezeichnete Tk-Figur bleibt, bis freigegebene Dateien vorliegen ([Arbeitsbegleiter](decisions/ARBEITSBEGLEITER.md)). Aus Inspirationsbildern wird keine Marken- oder Lizenzfreigabe abgeleitet.

## GitHub-Auftritt

**Projektseite 06.11.2026 (Auftrag des Inhabers, Plan §21.71):** Die README ist nach dem Vorbild erfolgreicher Repositorys neu gegliedert: zentriertes App-Symbol, Leitsatz und Ein-Satz-Nutzen, fünf Badges, Linkzeile mit „Herunterladen“ zuerst, großes Bild hell/dunkel per `<picture>`, „Warum Glide?“, Bildraster mit sechs echten Aufnahmen (künstlicher Showcase, Windows, 1440 × 900, Bedienhinweise aus), Funktionsliste, „Was Glide bewusst nicht ist“ mit passenden Alternativen, Download-Tabelle je System mit ehrlichem Hinweis zu Artefakten und unsignierten Paketen, „Deine Daten“, Häufige Fragen, Rückmeldung, Entwicklung, Lizenz und eine englische Kurzfassung. Issue-Formulare für Fehler und Wünsche liegen unter `.github/ISSUE_TEMPLATE/`; leere Issues sind abgeschaltet, Sicherheitsmeldungen verweisen auf die Richtlinie. Beschreibung und Topics der GitHub-Seite wurden auf Nutzen und Suchbegriffe ausgerichtet (höchstens 20 Topics, keine Varianten desselben Worts, kein „open-source“ und kein „local-first“, weil beides für Glide nicht zutrifft). Aufnahmen entstehen reproduzierbar aus dem Showcase in einem eigenen Prüfordner; sie liegen unter `assets/marketing/` und werden bei sichtbaren Oberflächenänderungen ersetzt, nicht gesammelt.

Belegter Befund der Recherche vom 06.11.2026: Keine der rund 20 untersuchten Aufgaben-, Notiz- und Produktivitäts-Apps auf GitHub verweist Endnutzer auf Actions-Artefakte; alle verteilen über Releases (`/releases/latest`) oder Stores, Artefakte verfallen nach höchstens 90 Tagen und verlangen eine Anmeldung. Alle erfolgreichen Repos haben eine klar benannte Lizenz und ein englisches Haupt-README. Daraus folgen **Inhaberentscheidungen**, die diese Pflege nicht trifft: GitHub-Release statt Artefakt (nach dieser Regel erst mit Lizenz und Signatur), Lizenzwahl, Englisch als Hauptsprache, Discussions, Homepage/GitHub Pages und Signierung. Ohne Entscheidung umsetzbar und erledigt: README, Bilder, Issue-Formulare, Beschreibung, Topics.

Am 02.11.2026 für den ersten öffentlichen Stand gekürzt und zusammengeführt. README beginnt mit Nutzen, Funktionsübersicht und Startwegen. Versions-/Lieferdetails, historische Prüfberichte und technische Restlisten stehen im QA-Bericht bzw. Entwicklungsplan. Die Featureübersicht wird bei jeder Funktionsänderung zusammen mit Handbuch, Neuerungen und CHANGELOG gepflegt.

Das Repository ist öffentlich; `main` bleibt die maßgebliche Projektablage. GitHub Actions liefert Grundprüfung, vollständige Linux-/Windows-Matrix, eigenständige Pakete und Release-Entwürfe. Der Mac-Workflow baut auf macOS arm64 mit eigener Tcl/Tk 9.1. Action-Commits sind festgelegt; Dependabot berücksichtigt Actions und Bauabhängigkeiten. Der Aktivierungsstatus einer statischen Analyse ist separat von ihrer Workflowdatei zu prüfen; es darf nur eine passende CodeQL-Einrichtung aktiv sein. Sicherheitsmeldungen laufen vertraulich über die [Sicherheitsrichtlinie](../../../SECURITY.md).

Ein öffentlicher GitHub-Release mit allgemeinem Vertriebsversprechen ist von einem geprüften Entwicklungsartefakt zu unterscheiden; Lizenz und öffentliche Signaturen bleiben erforderlich. Weitere Kanäle und Repository-Einstellungen werden nur im konkret beauftragten Umfang verändert.

**Release-Entwurf (Auftrag 06.11.2026 „Ja, als Entwurf“):** Damit neue Testerinnen und Tester ohne Anmeldung und Suche herunterladen können, baut `.github/workflows/release.yml` aus einem Tag `v<VERSION>` einen GitHub-Release-**Entwurf** als Vorabversion. Ablauf:

1. Vollmatrix „Glide-Prüfung“ auf dem `main`-Commit grün, eigene Abnahme nach [Releasecheckliste](#releasecheckliste).
2. Tag setzen und pushen: `git tag v<VERSION> <commit>` und `git push origin v<VERSION>`. Der Workflow verweigert Tags, die nicht zu `VERSION` passen, Commits außerhalb von `main` und Versionen ohne CHANGELOG-Abschnitt.
3. Windows- und Mac-Paket werden mit denselben Workflows wie in der Prüfung neu gebaut und isoliert gestartet (`windows-paket.yml`, `macos-paket.yml`; die DMG entsteht aus dem geprüften TAR). Anhänge: `Glide-<v>-windows-x64.zip`, `Glide-<v>-macos-arm64.dmg`, `Glide-<v>-macos-arm64.tar.gz`, je mit `.sha256`.
4. Die Versionshinweise enthalten den CHANGELOG-Abschnitt, Startanleitung für SmartScreen/Gatekeeper und oben einen Prüfstandskasten (Vollmatrix für denselben Commit grün, rot oder nicht gefunden). Den Kasten vor dem Veröffentlichen entfernen.
5. **Veröffentlichen nur von Hand** in GitHub unter „Releases“. Ein erneuter Lauf auf demselben Tag ersetzt nur einen noch unveröffentlichten Entwurf, nie einen veröffentlichten Release.

Ob und wann ein Entwurf öffentlich wird, entscheidet der Inhaber (D64); das berührt I11 (öffentlicher Auftritt), I2 (bis zur Lizenzentscheidung räumt [LICENSE.md](../LICENSE.md) keine Nutzungsrechte ein; die Versionshinweise verweisen darauf) und, solange unsigniert, I3. Prüfschritte vor dem Veröffentlichen: Block „Release-Entwurf prüfen“ der [manuellen Prüfung](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#e-nur-durch-den-inhaber). Für einen reibungslosen Erststart braucht es Developer-ID-Signatur mit Notarisierung (Mac) und ein Windows-Codesigning-Zertifikat; der Workflow hat dafür noch keine Schritte und keine Geheimnisse.

**Git-Historie (I10):** Frühere gelöschte Protokolle mit Benutzerpfaden und Archivkopien bleiben ein historischer Befund. Ein Umschreiben würde Commit-Kennungen und Klone ändern und ist nicht Teil des 3.50-Abschlusses. Neue Dateien werden vor dem Upload auf Benutzerpfade, echte Inhalte und Geheimnisse geprüft.

## Lizenzentwurf

Entwurf vom 21.09.2026, **noch nicht veröffentlicht** (I2):

> Glide darf für eigene private, nicht kommerzielle Zwecke kostenlos installiert und verwendet werden, einschließlich lokaler Sicherungskopien. Eigene Inhalte bleiben bei ihren Rechteinhabern. Kommerzielle Nutzung, Verkauf oder entgeltliche Weitergabe brauchen eine gesonderte Erlaubnis des Herausgebers. Eine Erlaubnis zur Weiterverbreitung veränderter Fassungen wird nicht erteilt. Gesetzlich zwingende Rechte bleiben unberührt. Komponenten Dritter (Schriften, tkinterdnd2) unterliegen ihren eigenen Lizenzen; deren Hinweise dürfen nicht entfernt werden.

Vor der Veröffentlichung festlegen: Geltungsbeginn und Lizenzdatei im Paket; Abgrenzung privat/ehrenamtlich/geschäftlich und unveränderte Weitergabe; Kontakt für kommerzielle Anfragen; rechtliche Endfassung zu Haftung, Gewährleistung und Vertragspartei. Der Entwurf macht Glide nicht zu Open-Source-Software; bis zur Freigabe sagen Store- und Vertriebsseiten keine weitergehenden Rechte zu. Bis dahin gilt `LICENSE.md` im Quellbaum: keine Lizenz festgelegt, keine Nutzungs-, Änderungs- oder Weiterverteilungsrechte eingeräumt.

## Inhaberangaben

Vorschläge vom 27.09.2026 (E-11). **Keiner gilt vor Bestätigung durch den Inhaber** (I1); bis dahin fließen sie in keine Build- oder Store-Konfiguration.

| Feld | Vorschlag | Begründung |
|---|---|---|
| Copyright-Zeile | `© 2026 Tim von Trostorff` | Herausgeber laut Register, Jahr der ersten Veröffentlichung |
| Datenschutz-URL | `https://shaye.de/glide/datenschutz` | unter der eingetragenen Website; beide Stores verlangen eine erreichbare Seite |
| Sicherheitskontakt | `mailme@shaye.de` (Betreff „Glide Sicherheit“) | wie Support, bis ein eigenes Postfach sinnvoll ist |
| Inno-Setup-AppId | `{0A756FC5-5DDB-4B0F-9EC8-B4AA85753597}` | einmal erzeugt am 27.09.2026; nach Bestätigung nie mehr ändern |
| macOS-Mindestversion | folgt aus der mitgelieferten Python-Laufzeit; beim ersten Release-Build messen | – |

Nach der Bestätigung: Produktregister mit Datum nachführen, Sicherheitskontakt in `SECURITY.md`, Copyright und Datenschutz-URL ins Produktdatenblatt, AppId ins Inno-Setup-Skript. Voraussetzungen, die nur der Inhaber schaffen kann: Apple-Developer-Konto mit Developer-ID-Zertifikat, Windows-Code-Signing-Zertifikat (I3).

**Entwurf der Datenschutzseite** (keine Rechtsberatung, vor Veröffentlichung prüfen lassen):

> Glide ist eine lokale Anwendung. Aufgaben, Notizen, Seiten, Zeichnungen, Bilder und Einstellungen bleiben auf deinem Gerät, in dem Datenordner, den du selbst wählst. Glide hat kein Benutzerkonto und keinen Server, sendet keine Nutzungsdaten, Absturzberichte oder Telemetrie und stellt von sich aus keine Verbindung ins Internet her; nur ein Link, den du anklickst, öffnet den Browser. Liegt dein Datenordner in einem Cloudordner, gelten für diese Kopie die Bedingungen des Anbieters. Systemmitteilungen, falls eingeschaltet, zeigt dein Betriebssystem an; sie enthalten den Titel der fälligen Aufgabe.

## Produktdatenblatt (Entwurf)

Technischer Entwurf zur gelieferten Basis 3.42.0, keine Veröffentlichungsfreigabe. Store-Grenzen stammen aus der Recherche vom 04.09.2026 und sind bei der Einreichung neu zu prüfen; Screenshots nur vom realen Build.

**Kurzprofil:** Deutschsprachige Desktop-App für Aufgaben, Listen, Notizen, Seiten, Notizbücher, Pinnwände, Galerien und Pixelzeichnungen. Alles lokal – ohne Konto, Server, Abo oder Telemetrie. Python 3.14 mit Tk 9 und Standardbibliothek; mitgeliefert nur tkinterdnd2 (MIT). **Positionierungshypothese:** Aufgabenorganisation mit Pixel-Werkstatt – Zeichnungen werden Symbole, Pinnwandkarten und Galeriebilder. Keine weltweit belegte Alleinstellung.

**Kurzbeschreibung** (Microsoft empfiehlt unter 270 Zeichen):

> Aufgaben, Notizen, Seiten, Notizbücher, Pinnwände und Pixelzeichnungen in einer deutschsprachigen App – vollständig lokal, ohne Konto und ohne Abo. Plane deinen Tag, ordne Projekte auf Boards und gestalte eigene Pixelsymbole.

**Beschreibung** (höchstens 10.000 Zeichen):

> Glide ordnet, was du dir vornimmst – und gibt ihm ein Gesicht.
>
> Listen, Ordner und Notizbücher halten Aufgaben, Notizen und Zeichnungen zusammen. „Heute“ zeigt, was ansteht – Verspätetes, Eingeplantes und heute Fälliges, jede Aufgabe genau einmal, mit Zeitplan und Stundenraster. Erfasse in Alltagssprache: „Angebot schicken morgen bis Freitag !hoch“. Die Pinnwand wird zum Board: Karten nach Fälligkeit, Wichtigkeit oder Dringlichkeit × Wichtigkeit in Spalten ziehen, Bereiche benennen, Verbindungen beschriften und alles als Folien präsentieren.
>
> Die Pixel-Werkstatt ist Glides Besonderheit. Zeichne auf 16 bis 128 Zellen mit Pinsel, Formen, Symmetrie und Mustern, verwende eigene Paletten und exportiere als PNG oder Symbol (ICO). Mache deine Zeichnungen zu Symbolen für Listen und Ordner.
>
> Alles bleibt auf deinem Rechner. Glide braucht weder Internet noch Konto, sendet keine Nutzungsdaten und sichert deinen Bestand mit vollständigen Backups und einer Sicherung vor jeder Formatumstellung.

**Features** (bis zu 20, je höchstens 200 Zeichen):

1. Aufgaben, Listen, Ordner, Bücher und Notizbücher – verschachtelt, mit Gruppen, Überschriften und Archiv.
2. „Heute“ und „Demnächst“: Verspätet, Liegen geblieben, Tagesplan, heute fällig; Zeitplan, Stundenraster, Kapazität.
3. Schnelleingabe in Alltagssprache mit sichtbaren, einzeln rücknehmbaren Feldern.
4. Pinnwand als Board: Spalten nach Feldern, Eisenhower-Gruppierung, Bereiche, Verbindungen, Präsentation.
5. Pixel-Werkstatt mit 16 bis 128 Zellen, Formen, Symmetrie, Mustern, Paletten, PNG- und ICO-Export.
6. Seiten für lange Texte und KI-Berichte mit Markdown, Bildern und echten Aufgaben.
7. Startseite „Ruhig“ mit sieben Kacheln in der hier beschriebenen Paketbasis 3.42.0; seit B04/3.43.0 acht Standardkacheln im Python-Stand, frei anpassbar.
8. Verknüpfte Punkte, „wartet auf“ mit Kreisprüfung und Zeiterfassung je Punkt.
9. Wiederholungen, Erinnerungen, Systemmitteilungen und Kalenderaustausch per ICS.
10. Vorlagen mit selbstfüllenden Platzhaltern wie {{Datum}} und Eingabefeldern wie {{Projektname}}.
11. Zehn Designs, darunter „Pixel“ mit eigener Pixelschrift, sowie Kontrastdesigns.
12. Vollständig lokal: kein Konto, kein Abo, keine Telemetrie; Backups und Wiederherstellung mit Vorschau.
13. Eigenständige Mac-/Windows-Entwicklungspakete mit eigenem Python/Tcl-Tk; Python-Startweg zusätzlich verfügbar.
14. Notion-Import mit Quellenvergleich und ausdrücklich gewählter Übernahme, ohne Live-Synchronisation.
15. Einzelne Seiten aus Sicherungen mit Vorschau, Bildern und Aufgabenverweisen wiederherstellen.
16. Pixel-Bildfolgen und Animationsvorschau innerhalb der Pixel-Werkstatt.

**Daten und Grenzen für Store-Texte:** Datenordner frei wählbar, auch synchronisiert; Glide synchronisiert nicht selbst, Fremdbelegung führt zum Schreibschutz. Ein Bestand aus einer neueren Formatversion öffnet schreibgeschützt. Erinnerungen und Systemmitteilungen nur bei laufender App. Textschriften Rubik, Roboto Mono, Playfair Display und Fraunces sowie Pixelify Sans unter SIL OFL 1.1; interner DejaVu-Symbolbegleiter unter eigener Bitstream-/Arev-Lizenz. Original-Lizenztexte gehen mit.

<a id="windows-entwicklungsbau-auf-eigenem-gerät-3490"></a>

## Windows-Entwicklungsbau auf eigenem Gerät (3.50.0)

Nach grüner Windows-Matrix und mit der [eigenen geprüften Tcl/Tk-9.1-Runtime](../packaging/runtime/README.md#eigene-prüfgeräte--bau-und-auswahl-der-runtime) aus `01_Repository/Glide`. Die Konsole verwendet dieselbe reguläre x64-Python-Patchversion wie beim Runtimebau. Neue Zielordner, keine vorhandene Lieferung überschreiben:

```powershell
python -B -m venv C:\gq\bau350-venv
$PythonGlideBau = 'C:\gq\bau350-venv\Scripts\python.exe'
$env:PYTHONPATH = 'C:\gq\runtime91\python-extension'
$VersionGlideBau = (Get-Content VERSION -Raw).Trim()
& $PythonGlideBau -B -m pip install -r requirements/build-windows.txt
& $PythonGlideBau -B packaging/paket/lizenzen_vorbereiten_windows.py --quelle src/glide --repo . --ziel C:/gq/p350/lizenzen --runtime-bau C:/gq/runtime91/runtime-bau.json
& $PythonGlideBau -B packaging/paket/baue_paket.py --quelle src/glide --version $VersionGlideBau --ziel C:/gq/p350/bau --plattform windows-x64 --lizenzen C:/gq/p350/lizenzen --runtime-bau C:/gq/runtime91/runtime-bau.json
& 'C:\gq\p350\bau\dist\Glide\Glide.exe' --paket-pruefen C:/gq/p350/start.json
```

Jeden Aufruf nur nach Exitcode 0 des vorherigen ausführen. Die Paketprobe isoliert ihre synthetischen Nutzdaten. `runtime-bau.json`, `bau-ergebnis.json`, PE-/Lizenzinventar, `start.json` und alle Bau-/Startlogs mitgeben. Das Artefakt bleibt bis zur Auswertung Entwicklungsbau, keine öffentliche Windows-Signatur oder Menschenfreigabe.

Dieser normale Start auf dem eigenen Gerät ersetzt die ausdrücklich an Hosted-CI gebundene externe Python-/Quellen-ACL-Isolationsprobe **nicht**. `pruefe_start_windows.py` und `windows_isolation.plan` lassen persönliche Installationen dafür nicht zu. Diese Grenze bleibt bestehen; keine fremden oder eigenen Inhaberinstallationen für eine Prüfung sperren und keine Hosted-Marker vortäuschen. Die aktuelle bereits geprüfte Mac-Lieferung und die frühere Windows-Lieferung bleiben bis zum tatsächlichen Windows-Abgleich erhalten.

## Schriftlizenzen und Stilklassifikationen (D60)

Geprüft am 03.11.2026: die vier abgelegten Original-OFL-Dateien und offiziellen Google-Fonts-Lizenztexte. Unveränderte statische Schnitte mit Prüfsummen in `resources/fonts/provenance.json`; die Anzeigenamen in Glide ändern weder Fontmetadaten noch reservierte Namen.

| Auswahl | Lizenz | GitHub mit Fontdateien | Kostenlose Glide-Weitergabe | Verkauf einer Glide-Anwendung |
|---|---|---|---|---|
| Modern: Rubik | [SIL OFL 1.1](https://github.com/google/fonts/blob/main/ofl/rubik/OFL.txt) | erlaubt | erlaubt | erlaubt |
| Technisch: Roboto Mono | [SIL OFL 1.1](https://github.com/google/fonts/blob/main/ofl/robotomono/OFL.txt) | erlaubt | erlaubt | erlaubt |
| Kreativ: Playfair Display | [SIL OFL 1.1, reservierter Name „Playfair Display“](https://github.com/google/fonts/blob/main/ofl/playfairdisplay/OFL.txt) | erlaubt | erlaubt | erlaubt |
| Klassisch: Fraunces | [SIL OFL 1.1](https://github.com/google/fonts/blob/main/ofl/fraunces/OFL.txt) | erlaubt | erlaubt | erlaubt |

Bedingungen bei jedem Schritt: Copyright-Hinweise und vollständige jeweilige OFL zugänglich mitliefern; in Git liegen sie bei den Schriften, im Paket zusätzlich im Lizenzbestand. Fontdateien behalten OFL, auch wenn Glides eigener Code einer anderen Lizenz unterliegt. Der Verkauf der Fontdateien allein ist nicht erlaubt. Bei Fontänderungen bleiben die Fontderivate OFL und dürfen reservierte Schriftnamen nicht ohne Erlaubnis verwenden; hier werden keine Fontdateien verändert. Die Auswahl „Kreativ: Playfair Display“ ist eine UI-Beschriftung des unveränderten Originals. Kommerziell erzeugte Texte, Bilder und PDF-Dokumente werden durch die Fontverwendung nicht selbst OFL-pflichtig. Quellen: [offizielle OFL-Nutzungshinweise](https://openfontlicense.org/how-to-use-the-ofl/) und [FAQ, insbesondere 1.2, 1.4, 1.10 und 1.15](https://openfontlicense.org/ofl-faq/).

Diese Rechte betreffen die Fontkomponenten. Glides eigene Nutzungs-/Vertriebslizenz und sonstige Komponenten bleiben getrennte Rechte. DejaVu Sans bleibt nach Inhabernachtrag intern für Symbole mit seinem unveränderten Original-Lizenztext; Pixelify bleibt für das Pixel-Design. Beide sind keine weiteren Textstil-Angebote.
