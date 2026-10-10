# Veröffentlichung – Glide

Stand 10.10.2026 · Glide 3.37.0 · interner Entwicklungsstand, keine Veröffentlichung · Aufgabenformat 23

Alles für eine spätere Auslieferung an einem Ort: Releasecheckliste, Signierung, Vertrieb und Marke, GitHub-Auftritt, Lizenzentwurf, Inhaberangaben und Store-Material. Zusammengeführt am 03.10.2026 aus der Releasecheckliste, drei Entscheidungsdokumenten vom 21.09.2026 und dem Ordner `40_Store_Material` (aufgelöst); die Vorfassungen trägt Git. Kennungen und technisch belegte Werte stehen weiter im [Produktregister](decisions/PRODUCT_IDENTITY.md).

## Releasecheckliste

**Je Version (erfüllt bis 3.33.6 und wieder seit 3.33.18; 3.33.7–3.33.17 nur unter Windows ohne Bundle):**

- [x] VERSION, `APP_VERSION`, Hauptsuite und CHANGELOG gleich; Datenformat geprüft.
- [x] Vollprüfung Exitcode 0 auf dem Referenz-Mac; Ergebnis im [QA-Bericht](07_QA_BERICHT.md).
- [x] `07_Python-Versionen` und macOS-Entwicklungsbundle per SHA-256 gleich `src/glide`, Bundle `de.shaye.glide`, Ad-hoc-Signatur gültig; Showcase ausgeliefert.
- [x] macOS-Paket enthält alle Module neben `app.pyw`, `resources` (Schriften mit Lizenztexten und `provenance.json`, Vorlagen, Logo) und `vendor/tkinterdnd2` mit Lizenz und nur den Bibliotheken der Zielplattform.
- [x] Kennungen `de.shaye.glide` und `Shaye.Glide` festgelegt (26.09.2026); echtes Programmsymbol aus dem Logo-Master (`assets/icons`).
- [x] Rückfallschutz: neuere Bestände schreibgeschützt, unlesbare gesichert, `data_format_written` warnt.

**Vor der ersten Veröffentlichung (offen):**

- [ ] Manuelle Prüfung auf macOS und Windows nach der [Prüfliste](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md), einschließlich Windows-Vollprüfung mit `tests/tools/windows_vollpruefung.cmd`.
- [ ] Release-Build mit eingebettetem Python 3.14 und Tk 9 je Plattform (D15, G26); Bauwerkzeug als eigene Abhängigkeitsentscheidung (Vorschlag: PyInstaller ab 6.22, gepinnt, Spezifikationsdatei).
- [ ] Developer-ID-Signatur und Notarisierung (macOS), Code-Signing und Installer (Windows, Inno Setup); tkDnD-Bibliothek mit signieren ([Entscheidung](decisions/ABHAENGIGKEIT_TKDND.md)).
- [ ] Windows-Verknüpfung mit AppUserModelID prüfen (`packaging/windows/verknuepfung_anlegen.ps1`); Hintergrundverläufe unter Windows ohne Bildreste.
- [ ] Clean-Machine-Test, Gatekeeper/SmartScreen, Update über eine vorhandene Installation, Datenordner in einem Cloudordner.
- [ ] DPI/Mehrmonitor, Hochkontrast/RDP, Screenreader, nur Tastatur, Ruhezustand, Dauerlauf.
- [ ] Inhaberangaben bestätigt (unten), Lizenz veröffentlicht, Markenprüfung abgeschlossen.
- [ ] Store-Texte und Screenshots vom realen Build; Hinweis „nach dem Update keine ältere Version starten“ in Neuerungen und Hilfe.

Automatisch grüne Tests ersetzen keine Plattformabnahme. Erinnerungen werden nur bei laufender App verarbeitet.

## Signierung und Notarisierung

Zertifikate, Zugangsdaten und Kennungen werden nicht erfunden und **nie im Repository gespeichert**.

**Windows:** Build und Installer reproduzierbar erzeugen → mit SignTool (Windows SDK) erst Binärdateien, dann Installer mit SHA-256 signieren, RFC-3161-Zeitstempel des Zertifikatanbieters → `signtool verify /pa /v <Datei>` für jedes Artefakt → Signatur, Herausgeber, Zeitstempel und SHA-256 im Release-Protokoll → Installation und Start auf sauberem System. Eine Signatur garantiert keine SmartScreen-Einstufung. Quellen: [SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool), [Authenticode-Zeitstempel](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures).

**macOS:** natives Bundle auf einem unterstützten Mac bauen und testen → mit Developer ID Application signieren, enthaltene ausführbare Komponenten einbeziehen → `xcrun notarytool submit <Archiv> --keychain-profile <Profil> --wait` (Zugangsdaten im lokalen Schlüsselbund) → nur bei `Accepted` `xcrun stapler staple` und `xcrun stapler validate` → Gatekeeper, Installation, Start, Datenablage und Update auf separatem System. Quellen: [Notarisierung](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), [Ablauf](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow).

Bisher wurde nichts signiert oder notarisiert außer der Ad-hoc-Signatur des Entwicklungsbundles.

## Vertrieb und Marke

- **Entschieden 27.09.2026 (E-10):** zuerst Direktvertrieb über die eigene Website; Stores später. macOS: Developer-ID-Signatur, Notarisierung, `.app` als Ordnerbundle, DMG, arm64 (Universal 2 nur, wenn Intel-Macs gebraucht werden). Windows: Installer mit Code-Signing, x64. Laufzeit Python 3.14 mit Tk 9.
- **Kanäle laut Auftrag:** GitHub, eigene Website, Social Media, Product Hunt, itch.io, Heise Software-Verzeichnis, winget; Microsoft Store gesondert prüfen. Keine Konten angelegt, nichts hochgeladen.
- Jeder Kanal braucht dasselbe geprüfte Artefakt, SHA-256-Prüfsumme, Versionshinweise, Systemvoraussetzungen, Kontakt und die freigegebene Lizenz.
- **Marke:** „Glide“ wird von mehreren Softwareanbietern genutzt. Vor einer Veröffentlichung professionelle Marken- und Namensrecherche durch einen Fachanwalt (I4). Ausgangspunkte: [DPMA-Recherche](https://www.dpma.de/marken/markenrecherche/index.html) (nur übereinstimmende Wortelemente, keine Ähnlichkeitsprüfung), [EUIPO/TMview](https://www.euipo.europa.eu/en/trade-marks/before-applying/availability). Eine Rechercheakte nennt Datum, Suchausdruck mit Varianten, Register, Waren-/Dienstleistungsklassen, Treffer, Inhaber, Status und Links.
- **Gismo** wird selbst produziert; die gezeichnete Tk-Figur bleibt, bis freigegebene Dateien vorliegen ([Arbeitsbegleiter](decisions/ARBEITSBEGLEITER.md)). Aus Inspirationsbildern wird keine Marken- oder Lizenzfreigabe abgeleitet.

## GitHub-Auftritt

Stand am 06.10.2026, über die GitHub-Schnittstelle abgerufen:

| Merkmal | Stand |
|---|---|
| Repository | [`n05a-design/glide-to-do`](https://github.com/n05a-design/glide-to-do), angelegt am 24.09.2026, öffentlich, Standardzweig `main`, maßgebliche Ablage (D09) |
| Beschreibung | englisch: „Glide is an offline desktop app for tasks, lists, notes, and journals, featuring daily planning, a calendar, pinboards, and local backups. No account or cloud service required. Built with Python and Tkinter.“ Sie nennt weder Seiten noch Pixel-Werkstatt; „journals“ heißen seit 3.30 Notizbücher. Keine Homepage |
| Tags, Releases | keine; D09 sieht Tags für Zwischenstände vor |
| Lizenz | keine; `LICENSE.md` räumt keine Nutzungs-, Änderungs- oder Weiterverteilungsrechte ein |
| Prüfungen | „Glide-Prüfung“ (CI-Grundstufe), Dependabot; CodeQL-Workflow deaktiviert; die KI-Codeprüfung „github-advanced-security“ scheiterte am 03.10.2026 am aufgebrauchten Monatskontingent |
| Funktionen | Issues (keine offen), Wiki und Projects eingeschaltet; Discussions und Pages aus |
| Größe | rund 510 MB laut GitHub, überwiegend Git-Historie |

**Empfehlungen** (nicht entschieden, I11):

1. Beschreibung aktualisieren, etwa: „Calm, local desktop workspace for your day – tasks, pages, notebooks, pinboards and a pixel workshop. No account, no cloud, German UI. Python 3.14 + Tk 9.“
2. Tags je ausgelieferter Version, wie D09 es vorsieht; eine GitHub-Release erst mit signiertem Paket und Lizenz.
3. Wiki ausschalten: Die Dokumentation liegt im Repository, ein Wiki wäre ein zweiter Ort (P3).
4. Issues bis zur Lizenz ausschalten oder nur für Fehlermeldungen öffnen; Sicherheitsmeldungen laufen vertraulich über *Security → Report a vulnerability* (`SECURITY.md`).
5. KI-Codeprüfung abschalten oder ihr Kontingent anpassen, damit kein dauerhaft roter Haken am PR steht.
6. Den Lizenzentwurf (I2) rechtlich prüfen und veröffentlichen, bevor das Repository beworben wird.

**Git-Historie (I10, eigener Auftrag):** Sie enthält gelöschte Protokolldateien mit Benutzerpfaden und frühere Archivkopien. Umschreiben verkleinert das Repository deutlich, ändert aber alle Commit-Kennungen und verlangt neue Klone auf allen Geräten. Empfehlung: bereinigen, solange es keine fremden Kopien gibt, und dabei die Entscheidung zu den Bildrechten (I9) mit umsetzen.

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

Entwurf auf Stand 3.33.6, keine Freigabe. Store-Grenzen stammen aus der Recherche vom 04.09.2026 und sind bei der Einreichung neu zu prüfen; Screenshots nur vom realen Build.

**Kurzprofil:** Deutschsprachige Desktop-App für Aufgaben, Listen, Notizen, Seiten, Notizbücher, Pinnwände, Galerien und Pixelzeichnungen. Alles lokal – ohne Konto, Server, Abo oder Telemetrie. Python 3.14 mit Tk 9 und Standardbibliothek; mitgeliefert nur tkinterdnd2 (MIT). **Alleinstellung:** Aufgabenorganisation mit echter Pixel-Werkstatt – Zeichnungen werden Symbole, Pinnwandkarten und Galeriebilder.

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
7. Startseite „Ruhig“ mit sieben Kacheln, frei anpassbar.
8. Verknüpfte Punkte, „wartet auf“ mit Kreisprüfung und Zeiterfassung je Punkt.
9. Wiederholungen, Erinnerungen, Systemmitteilungen und Kalenderaustausch per ICS.
10. Vorlagen mit selbstfüllenden Platzhaltern wie {{Datum}} und Eingabefeldern wie {{Projektname}}.
11. Zehn Designs, darunter „Pixel“ mit eigener Pixelschrift, sowie Kontrastdesigns.
12. Vollständig lokal: kein Konto, kein Abo, keine Telemetrie; Backups und Wiederherstellung mit Vorschau.

**Daten und Grenzen für Store-Texte:** Datenordner frei wählbar, auch synchronisiert; Glide synchronisiert nicht selbst, Fremdbelegung führt zum Schreibschutz. Ein Bestand aus einer neueren Version öffnet schreibgeschützt; **Glide 3.29 und älter nach der Umstellung nicht mehr starten**. Erinnerungen und Systemmitteilungen nur bei laufender App. Schriften DejaVu Sans und Pixelify Sans (SIL OFL 1.1) mit Lizenztexten.
