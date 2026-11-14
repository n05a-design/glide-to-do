# Veröffentlichung – Glide

Stand 13.11.2026 · Glide 3.60.0 · Aufgabenformat 26

Alles für eine spätere Auslieferung an einem Ort: Releasecheckliste, Signierung, Vertrieb und Marke, GitHub-Auftritt, MPL-2.0, Inhaberangaben und Store-Material. Zusammengeführt am 03.10.2026 aus der Releasecheckliste, drei Entscheidungsdokumenten vom 21.09.2026 und dem Ordner `40_Store_Material` (aufgelöst); die Vorfassungen trägt Git. Kennungen und technisch belegte Werte stehen weiter im [Produktregister](decisions/PRODUCT_IDENTITY.md).

## Releasecheckliste

3.50.0 trägt die historische Bezeichnung **Erster öffentlicher Stand** (intern **öffentliche erste Beta**). Quell- und Paketnachweise für die Entwicklungsbauten von Glide 3.55.1 auf `45ab307` stehen im [QA-Bericht](07_QA_BERICHT.md#plattformprüfung-und-pakete-für-3551-13112026). Für einen öffentlichen Download gelten die nachfolgenden Freigabebedingungen.

- Nutzerstand und betroffene Fach-/Lieferquellen anhand der [Pflegematrix](DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) abgleichen; App-, System- und Formatversion nach ihren jeweiligen Regeln führen.
- Fach-/Werkzeugtests sowie vollständige eingefrorene Integrationsmatrix auf Mac, Linux und Windows ausführen. Nur unveränderte App-/Test-/Fixture-/Ressourcenbytes einem Ergebnis zuordnen.
- Python-Fassung bytegleich abgleichen, Showcase reproduzieren und getrennt prüfen; native Pakete mit Original-Lizenzbelegen bauen, kompilierten Quell-/Ressourcenabgleich und echte isolierte Startprobe durchführen.
- Actions auf Commit-SHA und Bauabhängigkeiten auf Version/Originalhash festlegen (WA-43/45). Herkunft von Runtime, tkDnD, Schriften und Zeitzonen beilegen; Paketprüfsummen dokumentieren.
- Die menschliche Prüfung erfolgt anschließend durch den Inhaber: Bedienung, Tastatur, Mindestgröße/große Schrift, DPI, mehrere Monitore und konkrete Plattformabläufe. **Screenreader ist bis Bedarf zurückgestellt und kein aktiver offener 3.50-Punkt.**
- Für einen allgemeinen signierten Vertrieb bleiben öffentliche Signatur/Notarisierung, MPL-Weitergabehinweise, Kanalunterlagen und Markenprüfung gesonderte Voraussetzungen. MPL-2.0 ist beschlossen; eine Versionsbezeichnung ersetzt keine Zertifikate oder Abnahmen.

Der Commit-/Pushauftrag vom 10.11.2026 wurde erfüllt; der Inhaber mergte PR #75 nach den Kandidatenprüfungen in `main`. Die erfolgreichen Main-Läufe sind im [QA-Bericht](07_QA_BERICHT.md) festgehalten. Der Auftrag umfasste weder Tag noch Releaseartefakt, Signierung oder Veröffentlichung in weiteren Vertriebskanälen; diese Schritte bleiben gesonderte Freigaben. Erinnerungen werden nur bei laufender App verarbeitet.

**Noch offene technische Releasevorbereitung (WA-46):** Ein CycloneDX-1.6-Inventar mit geprüftem Pre-build-/Incomplete-Umfang sowie Lizenz-/Bauinventare und SHA-256-Dateilisten sind vorhanden. Ein dokumentierter Mac-Baustand enthielt 24 BOM-Komponenten und 37 Lizenzdateien ohne Schemafehler; der vollständige Abhängigkeitsgraph und der abschließende Abgleich eines freigegebenen Releaseartefakts fehlen weiterhin. WA-46 ist daher offen und darf nicht als vollständiger SBOM-/Releaseabschluss ausgewiesen werden. Neuere Fassungen von Bauwerkzeugen sind im [Abhängigkeitsabgleich](https://github.com/n05a-design/glide-to-do/blob/13bcb66a7ba2007c3d8828ba1e0e082cb8918c91/01_Repository/Glide/tests/qa-3.50.0/abschlussabgleich_2026-11-02/README.md) dokumentiert; ein Upgrade verlangt neue native Bau-/Startbelege.

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

**Projektseite 13.11.2026:** README-Kopf und Galerie nutzen Glides 3.60.0-Branding. Die Windows-Aufnahmen zeigen unterschiedliche Arbeitssituationen im Showcase „Werkhaus West“. Der [Showcase](../../../05_Probelisten_Testdaten/Showcase/README.md) enthält auch den JSON-Canvas-Export derselben Pinnwand. Die [Logo-Checkliste](../../../20_Grafik_Master/README.md) führt Repository-Vorschau, Dokumentation, Betriebssystem- und Lieferressourcen.

**Projektseite 06.11.2026 (Auftrag des Inhabers, Plan §21.71):** Die README ist nach dem Vorbild erfolgreicher Repositorys neu gegliedert: zentriertes App-Symbol, Leitsatz und Ein-Satz-Nutzen, fünf Badges, Linkzeile mit „Herunterladen“ zuerst, großes Bild hell/dunkel per `<picture>`, „Warum Glide?“, Bildraster mit sechs echten Aufnahmen (künstlicher Showcase, Windows, 1440 × 900, Bedienhinweise aus), Funktionsliste, „Was Glide bewusst nicht ist“ mit passenden Alternativen, Download-Tabelle je System mit ehrlichem Hinweis zu Artefakten und unsignierten Paketen, „Deine Daten“, Häufige Fragen, Rückmeldung, Entwicklung, Lizenz und eine englische Kurzfassung. Issue-Formulare für Fehler und Wünsche liegen unter `.github/ISSUE_TEMPLATE/`; leere Issues sind abgeschaltet, Sicherheitsmeldungen verweisen auf die Richtlinie. Beschreibung und Topics der GitHub-Seite wurden auf Nutzen und Suchbegriffe ausgerichtet (höchstens 20 Topics, keine Varianten desselben Worts, damals ohne „open-source“ wegen fehlender Lizenz; dieser historische Ausschluss ist seit MPL-2.0 überholt). Aufnahmen entstehen reproduzierbar mit `tests/tools/projektseite_aufnahmen.py` aus dem Showcase in einem eigenen Prüfordner; sie liegen unter `assets/marketing/` und werden bei sichtbaren Oberflächenänderungen ersetzt, nicht gesammelt.

### Recherche erfolgreicher Repositorys (06.11.2026)

Untersucht wurden rund 20 Aufgaben-, Notiz- und Produktivitäts-Apps auf GitHub (u. a. [Super Productivity](https://github.com/super-productivity/super-productivity), [donetick](https://github.com/donetick/donetick), [Memos](https://github.com/usememos/memos), [Logseq](https://github.com/logseq/logseq), [Trilium](https://github.com/TriliumNext/Trilium), [AppFlowy](https://github.com/AppFlowy-IO/AppFlowy), [SiYuan](https://github.com/siyuan-note/siyuan), [LocalSend](https://github.com/localsend/localsend), [Mindwtr](https://github.com/dongdongbh/Mindwtr)), die meistgesternten Repos laut [EvanLi/Github-Ranking](https://github.com/EvanLi/Github-Ranking) (Spitze am 06.11.2026: build-your-own-x 560.177, awesome 531.865, public-apis 496.453, freeCodeCamp 458.615 Sterne) und GitHubs offizielle Doku. **[H]** = am Abrufdatum auf der Quelle beobachtet, **[A]** = Ableitung. Kein Repo wurde installiert; Sternzahlen schnell wachsender Neueinsteiger (openclaw, morluto/rea) taugen nicht als Gestaltungsbeleg, weil gekaufte Sterne verbreitet sind ([arXiv 2412.13459](https://arxiv.org/html/2412.13459v1)).

- **Die Sternspitze sammelt Lesezeichen [H/A]:** Sieben der zehn meistgesternten Repos sind Listen oder Lernpfade; Vorbild für eine App sind App-Repos. Übertragbar sind dennoch eine persönliche, offene Tonlage, ein Abschnitt „was nicht abgedeckt ist“ (coding-interview-university) und offene Angaben, was nach außen geht (openclaw).
- **Erster Bildschirm [H]:** Symbol oder Wortmarke, ein Satz Nutzen, Linkzeile mit Download zuerst, zwei bis sechs Badges, großes Bild/GIF; danach kurze Funktionen in zwei bis vier Gruppen, Download je Plattform, Doku, Mitwirken, Lizenz. Hell/Dunkel per `<picture>` (Memos, Excalidraw), „Warum X?“ (Logseq, Trilium, AppFlowy), ehrliche Grenzen (immich, paperless-ngx), Vergleichstabelle mit Quellen und Korrekturbitte (Mindwtr).
- **Verteilung [H]:** Keine untersuchte Desktop-App schickt Endnutzer zu Actions-Artefakten. Alle nutzen [Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) (öffentlich, dauerhaft, ohne Anmeldung, stabiler Link `releases/latest/download/<datei>`) oder Stores/Flathub. Asset-Namen `Name-Version-OS-Arch.ext`, oft mit `SHA256SUMS.txt`. Artefakte verfallen in öffentlichen Repos nach höchstens 90 Tagen und verlangen eine Anmeldung. Seit Oktober 2025 gibt es unveränderliche Releases mit signierten Attestierungen.
- **Unsignierte Pakete [H]:** Übliches Muster ist ein klarer Hinweis mit den Schritten je System und Prüfsummen. macOS: Systemeinstellungen › Datenschutz & Sicherheit › „Dennoch öffnen“, laut [Apple](https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unknown-developer-mh40616/mac) etwa eine Stunde nach dem Startversuch verfügbar; Windows SmartScreen: „Weitere Informationen“ › „Trotzdem ausführen“ (Sekundärquelle). LocalSend liefert zusätzlich eine ausdrücklich unsignierte EXE; Mindwtr signiert kostenlos über die SignPath Foundation, was nach allgemeiner Kenntnis eine Open-Source-Lizenz voraussetzt [A].
- **Auffindbarkeit [H]:** Die GitHub-Suche liest ohne Zusatz nur [Name, Beschreibung und Topics](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories); höchstens [20 Topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) zu je 50 Zeichen. `task-management-app` (55 Repos, Spitze 95 Sterne) und `productivity-app` (567 Repos) sind dünn besetzt und damit ein sofortiger Hebel; `task-manager` und `task-scheduler` führen überwiegend zu Job-Queues. Ein Längenlimit der Beschreibung ist nicht dokumentiert; 120–160 Zeichen gelten als Faustwert [A]. Social-Preview: PNG/JPG/GIF unter 1 MB, ideal 1280 × 640.
- **Sprache [H/A]:** Kein untersuchtes Repo über 500 Sterne hat ein nicht-englisches Haupt-README; Übersetzungen erscheinen als `README.xx.md`. Weil Glides Oberfläche nur deutsch ist (Produktgrenze), ist ein deutsches Haupt-README mit englischer Kurzfassung und englischen Topics der ehrliche Mittelweg; die Entscheidung liegt beim Inhaber.
- **Community [H]:** Das [Community-Profil](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories) prüft README, CODE_OF_CONDUCT, LICENSE, CONTRIBUTING, SECURITY und Issue-Vorlagen; Sterne bringen diese Dateien nicht (build-your-own-x hat nur ein Issue-Template), wohl aber klare Kanäle (paperless-ngx). Discussions sind bei 15 von 21 Vergleichsrepos aktiv; ein leerer Bereich, Star-History oder Contributor-Raster wirken bei einem Ein-Personen-Projekt eher verlassen [A]. Ein Wiki wird erst ab 500 Sternen indexiert und widerspräche „ein Thema, ein Dokument“.
- **Reichweite [H/A]:** Frühe Sterne entstehen selten im Repo selbst. LocalSend erreichte auf Hacker News bis 923 Punkte mit dem Anker „alternative to AirDrop“; Super Productivity und Mindwtr wuchsen über Stores, ladbare Releases und hohen Release-Takt. Bei allen erfolgreichen Indies steht ein ladbares Release vor jeder Reichweitenmaßnahme; für Glide passen deutschsprachige Communitys, Heise-Softwareverzeichnis und winget aus der eigenen Kanalliste besser als Trending oder Show HN.

| Maßnahme | Stand 06.11.2026 |
|---|---|
| README-Kopf mit Symbol, Nutzen, Badges, Linkzeile „Herunterladen“, Bild hell/dunkel | erledigt |
| „Warum Glide?“, Bildraster, „Was Glide bewusst nicht ist“, „Deine Daten“, Häufige Fragen, englische Kurzfassung | erledigt |
| Download-Tabelle mit ehrlichem Hinweis zu Anmeldung und unsignierten Paketen | erledigt; zeigt seit D64 auf Releases, Prüfsummen als `.sha256` je Anhang und im QA-Bericht |
| Issue-Formulare „Fehler melden“ und „Wunsch oder Idee“, leere Issues aus | erledigt |
| Beschreibung zweisprachig, 20 Topics ohne Dubletten, mit `task-management-app` und `productivity-app` | erledigt (Kontoaktion auf ausdrücklichen Auftrag) |
| Aufnahmen reproduzierbar aus dem Showcase (`tests/tools/projektseite_aufnahmen.py`) | erledigt |
| Funktionsliste weiter kürzen, Details nur im Handbuch | offen; bewusst noch vollständig, weil die README die einzige Landingpage ist |
| Kurzes GIF Erfassen → Planen → Erledigen | offen |
| CONTRIBUTING.md und SUPPORT.md (Rückmeldungen willkommen, Code nur nach Absprache, keine echten Daten) | offen; MPL-2.0 ist beschlossen, Beitrags- und Supportprozess noch festzulegen |
| Social-Preview-Bild gegen 1280 × 640 / 1 MB prüfen, ggf. neu exportieren (nur Weboberfläche) | offen |
| Seitenleiste: Packages/Deployments ausblenden, Wiki aus | offen, Kontoaktion |
| Release-Weg technisch vorbereiten, ohne zu veröffentlichen | erledigt mit D64: `.github/workflows/release.yml` erzeugt aus Tag `v<VERSION>` einen Entwurf mit Windows-ZIP, DMG, TAR und je einer `.sha256`-Datei (statt `SHA256SUMS.txt`); siehe [GitHub-Auftritt](#github-auftritt). Eine Release-Notes-Vorlage `.github/release.yml` ist nicht nötig, die Hinweise erzeugt der Workflow |
| **Inhaberentscheidungen:** Veröffentlichen eines Release-Entwurfs (Weg mit D64 beschlossen, Freigabe von Hand), Signierung (I3), Englisch als Hauptsprache, Discussions, Homepage/GitHub Pages (Website-Direktvertrieb seit 27.09.2026 vorgesehen), Inhaberangaben/Marke (I1/I4), Reichweite | offen |

Seit 07.11.2026 ist Glide-Code MPL-2.0-lizenziert. Die frühere Begründung gegen die Bezeichnung Open Source ist entfallen. Eignung für Signierprogramme muss separat geprüft werden; daraus folgen weder ein Preisbeschluss noch Signatur, Markenfreigabe oder Releasefreigabe.

Am 02.11.2026 für den ersten öffentlichen Stand gekürzt und zusammengeführt. README beginnt mit Nutzen, Funktionsübersicht und Startwegen. Versions-/Lieferdetails, historische Prüfberichte und technische Restlisten stehen im QA-Bericht bzw. Entwicklungsplan. Die Featureübersicht wird bei jeder Funktionsänderung zusammen mit Handbuch, Neuerungen und CHANGELOG gepflegt.

Das Repository ist öffentlich; `main` bleibt die maßgebliche Projektablage. GitHub Actions liefert Grundprüfung, vollständige Linux-/Windows-Matrix, eigenständige Pakete und Release-Entwürfe. Der Mac-Workflow baut auf macOS arm64 mit eigener Tcl/Tk 9.1. Action-Commits sind festgelegt; Dependabot berücksichtigt Actions und Bauabhängigkeiten. Der Aktivierungsstatus einer statischen Analyse ist separat von ihrer Workflowdatei zu prüfen; es darf nur eine passende CodeQL-Einrichtung aktiv sein. Sicherheitsmeldungen laufen vertraulich über die [Sicherheitsrichtlinie](../../../SECURITY.md).

Ein öffentlicher GitHub-Release mit allgemeinem Vertriebsversprechen ist von einem geprüften Entwicklungsartefakt zu unterscheiden; Lizenz und öffentliche Signaturen bleiben erforderlich. Weitere Kanäle und Repository-Einstellungen werden nur im konkret beauftragten Umfang verändert.

**Release-Entwurf (Auftrag 06.11.2026 „Ja, als Entwurf“):** Damit neue Testerinnen und Tester ohne Anmeldung und Suche herunterladen können, baut `.github/workflows/release.yml` aus einem Tag `v<VERSION>` einen GitHub-Release-**Entwurf** als Vorabversion. Ablauf:

1. Vollmatrix „Glide-Prüfung“ auf dem `main`-Commit grün, eigene Abnahme nach [Releasecheckliste](#releasecheckliste).
2. Tag setzen und pushen: `git tag v<VERSION> <commit>` und `git push origin v<VERSION>`. Der Workflow verweigert Tags, die nicht zu `VERSION` passen, Commits außerhalb von `main` und Versionen ohne CHANGELOG-Abschnitt.
3. Windows- und Mac-Paket werden mit denselben Workflows wie in der Prüfung neu gebaut und isoliert gestartet (`windows-paket.yml`, `macos-paket.yml`; die DMG entsteht aus dem geprüften TAR). Anhänge: `Glide-<v>-windows-x64.zip`, `Glide-<v>-macos-arm64.dmg`, `Glide-<v>-macos-arm64.tar.gz`, je mit `.sha256`.
4. Die Versionshinweise enthalten den CHANGELOG-Abschnitt, Startanleitung für SmartScreen/Gatekeeper und oben einen Prüfstandskasten (Vollmatrix für denselben Commit grün, rot oder nicht gefunden). Den Kasten vor dem Veröffentlichen entfernen.
5. **Veröffentlichen nur von Hand** in GitHub unter „Releases“. Ein erneuter Lauf auf demselben Tag ersetzt nur einen noch unveröffentlichten Entwurf, nie einen veröffentlichten Release.

Ob und wann ein Entwurf öffentlich wird, entscheidet der Inhaber (D64); das berührt I11 (öffentlicher Auftritt), I2 (MPL-2.0 beschlossen; aktuelle Paket-/Quellhinweise prüfen) und, solange unsigniert, I3. Prüfschritte vor dem Veröffentlichen: Block „Release-Entwurf prüfen“ der [manuellen Prüfung](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#e-nur-durch-den-inhaber). Für einen reibungslosen Erststart braucht es Developer-ID-Signatur mit Notarisierung (Mac) und ein Windows-Codesigning-Zertifikat; der Workflow hat dafür noch keine Schritte und keine Geheimnisse.

**Git-Historie (I10):** Frühere gelöschte Protokolle mit Benutzerpfaden und Archivkopien bleiben ein historischer Befund. Ein Umschreiben würde Commit-Kennungen und Klone ändern und ist nicht Teil des aktuellen Projektabgleichs. Neue Dateien werden vor dem Upload auf Benutzerpfade, echte Inhalte und Geheimnisse geprüft.

<a id="lizenzentwurf"></a>

## MPL-2.0

**Entschieden am 07.11.2026 (D72/I2): Mozilla Public License 2.0, SPDX `MPL-2.0`.** Der vollständige [Lizenztext in der Wurzel](../../../LICENSE) ist maßgeblich. [LICENSE.md](../LICENSE.md) erläutert den Geltungsbereich. Der frühere nichtkommerzielle Entwurf ist verworfen; seine Vorfassung bleibt in Git.

Die MPL erlaubt kommerzielle Nutzung und Weitergabe nach ihren Bedingungen. Bei externer Weitergabe sind abgedeckte Quelldateien samt Änderungen unter MPL zugänglich zu machen und vorhandene Hinweise zu bewahren. Binärempfänger brauchen einen verständlichen Bezugsweg zum entsprechenden Quellcode (Abschnitte 3.1–3.4). Ein größeres Werk kann andere Bedingungen haben, ohne die Rechte an den abgedeckten Dateien einzuschränken. Markenrechte sind ausgenommen (2.3).

Neue native Lizenzbestände führen den unveränderten Root-Text als `Glide-MPL-2.0.txt`, Geltungsbereichshinweise und `Glide-Quellcode.txt` mit Commit-URL/Quellarchiv und Verweis auf die Bauhashes mit. Der Erzeuger verlangt gesicherte Paketquellen im Git-Commit; dieser Commit muss vor Weitergabe erreichbar sein. Bei eigenem Fork den Bezugsweg anpassen. Python-Lieferung: vollständiges `LICENSE` und Hinweisdatei mitführen. Alte Pakete werden durch die neue Dokumentation nicht nachträglich korrigiert; native Neubauten bleiben eigene Tore.

Drittkomponenten und Ressourcen behalten MIT-, OFL-, Tcl/Tk-/Python-, DejaVu-, IANA-/CLDR- und weitere Originalbedingungen. Die gehashte Mac-Lizenzbasis bleibt als historischer Beleg unverändert; der Mac-Erzeuger ersetzt Glides eigenen Eintrag erst im neuen Bestand. Fremde Inspirationsbilder und Entwurfsreferenzen sind gesondert zu klären, bevor sie erneut verbreitet werden. Copyright-Inhaberschaft wird nicht erfunden. Quellen, abgerufen 07.11.2026: [Mozilla-Lizenztext](https://www.mozilla.org/en-US/MPL/2.0/), [Mozilla-FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/).

Lizenz, Preise für spätere Distribution/Services, Marke, Support und Releasefreigabe bleiben verschiedene Sachverhalte. I2 ist als Lizenzentscheidung erledigt; neue Pakete samt Hinweisen sind vor Weitergabe zu prüfen. I1/I3/I4/I11 bleiben in ihrem jeweiligen Restumfang offen.

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

## Produktkommunikation

**Verbindliche Richtung (D72/D74):** Glide ist ein Desktop-Planer für Projekte, Aufgaben, Tagesplanung, Pinnwände und Pixel-Zeichnungen. Projekte werden mit den vorhandenen Ordnern, Listen, Seiten und Verknüpfungen organisiert; ein zusätzlicher Projektdatentyp wird damit nicht behauptet. Datenhaltung bleibt eine technische Produkteigenschaft. „Privat“, „ruhig“, Sprachzugehörigkeit und Fachbegriffe zur Nutzungsdatenerfassung sind keine Leitbotschaften. Speicherung wird positiv erklärt: Inhalte werden gespeichert und mit Sicherungen/Exporten aufbewahrt. Auf Inhaberauftrag vom 08.11.2026 entfallen aktive Beta-/Erstversionswerbung und allgemeine Versionsserienbotschaften; technische Versions-/Paketzuordnung und datierte historische Nachweise bleiben erhalten.

| Fundstelle | Text / Regel |
|---|---|
| Produktname / Kategorie | **Glide – Desktop-Planer** |
| Hauptbeschreibung | **Desktop-Planer für Projekte, Aufgaben, Tagesplanung, Pinnwände und Pixel-Zeichnungen.** |
| Kurze Unterzeile | Aufgaben planen. Ideen verbinden. Selbst gestalten. |
| Ein Satz | Glide verbindet deine Aufgaben und Tagesplanung mit Seiten, Pinnwänden und eigenen Pixel-Zeichnungen. |
| GitHub-Beschreibung, freigegeben und gesetzt | Desktop-Planer für Projekte, Aufgaben, Tagesplanung, Pinnwände und Pixel-Zeichnungen. Verbinde Aufgaben mit Seiten und Notizen und gestalte deine Ideen. |
| Englische Kurzfassung | Desktop planner for tasks, day planning, pinboards and pixel drawings. Connect tasks with pages and notes and create your own visual material. |
| Ausführliche Beschreibung | Glide verbindet Aufgaben und Tagesplanung mit Seiten, Notizen und Pinnwänden. Du kannst denselben Aufgabenbestand in verschiedenen Ansichten bearbeiten, Aufwand und verfügbare Zeit gegenüberstellen und Vorschläge vor dem Übernehmen prüfen. In der Pixel-Werkstatt entstehen eigene Zeichnungen, Symbole und Bildfolgen. Deine Inhalte werden in deinem gewählten Datenordner gespeichert; automatische Sicherungen und lesbare Exporte unterstützen die Weiterarbeit. |
| Nutzen und Priorität | 1. Aufgaben im Kontext bearbeiten. 2. Den eigenen Tag planen. 3. Ideen sichtbar verbinden. 4. Eigene Zeichnungen weiterverwenden. 5. Arbeit aufbewahren und exportieren. |
| Zielgruppenhypothese | Menschen mit eigenen Desktop-Projekten, besonders Gestaltung, Schreiben, Lernen und Entwicklung; keine belegte Nutzer- oder Nachfragezahl |
| Differenzierung | Kombination aus fertiger Tagesplanung, Aufgaben in Seiten/Pinnwänden und integrierter Pixel-Werkstatt; kein weltweit belegtes Alleinstellungsmerkmal |
| GitHub-Topics, freigegeben und gesetzt | `desktop-app`, `daily-planner`, `task-management`, `productivity`, `kanban`, `note-taking`, `pinboard`, `pixel-art`, `pomodoro`, `time-management`, `python`, `tkinter`, `cross-platform`, `open-source`, `mpl-2-0` |
| Website-/Store-Suchthemen | Desktop-Planer, Aufgabenplanung, Tagesplanung, Pinnwand, Notizen, Pixel-Zeichnungen; international zusätzlich desktop planner, day planning, task management, pinboard, pixel art |

Beschreibung und die hier genannten 15 Topics wurden am 07.11.2026 nach konkreter Freigabe des Inhabers öffentlich aktualisiert und zurückgelesen. Eine erreichbare eigene Glide-Website/Store-Seite wurde in den Projektquellen nicht nachgewiesen; das Produktdatenblatt dient als Textvorlage, nicht als Nachweis einer Veröffentlichung. Die derzeitige Oberflächensprache bleibt eine technische Ist-Angabe; Internationalisierung ist vorgesehen, ohne bestätigten Termin oder implementierte Übersetzung.

**Technischer Name:** `APP_PRODUCT_NAME` („Glide – Aufgaben und Listen“) bleibt für Fenster, Druck/Export und Paketmetadaten stabil. Der öffentliche Beschreibungstext steht in `brand.DESCRIPTION` und „Über Glide“. Bundle-ID, AppUserModelID, Datenordner, Paketnamen und vorhandene Startdateinamen ändern sich nicht durch Marketing.

**Funktions- und Qualitätsgrenzen:** Der [Funktionsvertrag](20_FUNKTIONEN.md) beschreibt tatsächliche Bedienung. [QA](07_QA_BERICHT.md) trennt nachgewiesene Prüfbereiche, implementierte Korrekturen ohne vollständige Abnahme, native Pakete und menschliche Tore. Vorschläge und Teilumfänge aus dem Plan werden nicht als neue verfügbare Funktion beworben. Die existierenden Bilder sind ausdrücklich Aufnahmen von 3.50.5 und werden nicht als 3.50.6 umetikettiert.

<a id="produktdatenblatt-entwurf"></a>

## Produktdatenblatt (Entwurf)

Die aktuellen Beschreibungstexte und Suchthemen stehen im Abschnitt [Produktkommunikation](#produktkommunikation). Die frühere 3.42.0-Funktionskopie wurde durch diesen Verweis ersetzt. Store-Grenzen und Pflichtangaben sind vor einer konkreten Einreichung beim jeweiligen Anbieter neu zu prüfen. Screenshots müssen den tatsächlich eingereichten Build zeigen; keine Store-Einreichung oder allgemeine Plattformfreigabe ist belegt.

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

<a id="schriftlizenzen-und-stilklassifikationen-d60"></a>

## Schriftlizenzen und Stilklassifikationen (D60 / D77)

Geprüft am 03.11.2026 (D60) und aktualisiert am 10.11.2026 (D77): die abgelegten Original-OFL-Dateien und offiziellen Lizenztexte. Unveränderte statische Schnitte mit Prüfsummen in `resources/fonts/provenance.json`; die Anzeigenamen in Glide ändern weder Fontmetadaten noch reservierte Namen. Frühere gespeicherte Familiennamen (`Roboto Mono`, `Playfair Display`, `Fraunces`) werden ihren jeweiligen Stilklassen zugeordnet.

| Auswahl | Lizenz | GitHub mit Fontdateien | Kostenlose Glide-Weitergabe | Verkauf einer Glide-Anwendung |
|---|---|---|---|---|
| Modern: Rubik | [SIL OFL 1.1](https://github.com/googlefonts/rubik/blob/main/OFL.txt) | erlaubt | erlaubt | erlaubt |
| Technisch: DM Mono | [SIL OFL 1.1](https://github.com/google/fonts/blob/main/ofl/dmmono/OFL.txt) | erlaubt | erlaubt | erlaubt |
| Kreativ: DM Serif Display | [SIL OFL 1.1, reservierter Name „Source“](https://github.com/google/fonts/blob/main/ofl/dmserifdisplay/OFL.txt) | erlaubt | erlaubt | erlaubt |
| Klassisch: Charis SIL | [SIL OFL 1.1, reservierte Namen „Charis“, „SIL“](https://github.com/silnrsi/font-charis-sil/blob/master/OFL.txt) | erlaubt | erlaubt | erlaubt |

Bedingungen bei jedem Schritt: Copyright-Hinweise und vollständige jeweilige OFL zugänglich mitliefern; in Git liegen sie bei den Schriften, im Paket zusätzlich im Lizenzbestand. Fontdateien behalten OFL, auch wenn Glides eigener Code einer anderen Lizenz unterliegt. Der Verkauf der Fontdateien allein ist nicht erlaubt. Bei Fontänderungen bleiben die Fontderivate OFL und dürfen reservierte Schriftnamen nicht ohne Erlaubnis verwenden; hier werden keine Fontdateien verändert. Die Auswahl „Kreativ: DM Serif Display“ bzw. „Klassisch: Charis SIL“ ist eine UI-Beschriftung des unveränderten Originals. Kommerziell erzeugte Texte, Bilder und PDF-Dokumente werden durch die Fontverwendung nicht selbst OFL-pflichtig. Quellen: [offizielle OFL-Nutzungshinweise](https://openfontlicense.org/how-to-use-the-ofl/) und [FAQ, insbesondere 1.2, 1.4, 1.10 und 1.15](https://openfontlicense.org/ofl-faq/).

Diese Rechte betreffen die Fontkomponenten. Glides eigene Nutzungs-/Vertriebslizenz und sonstige Komponenten bleiben getrennte Rechte. DejaVu Sans bleibt nach Inhabernachtrag intern für Symbole mit seinem unveränderten Original-Lizenztext; Pixelify bleibt für das Pixel-Design. Beide sind keine weiteren Textstil-Angebote.
