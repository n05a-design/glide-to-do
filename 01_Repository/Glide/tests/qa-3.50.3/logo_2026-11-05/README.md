# Neue Logos und Darkmode-Gelb – 3.50.3

Stand 05.11.2026 · Aufgabenformat 26 · D62

Neue Master einschließlich geänderter G-Kontur unverändert aus `20_Grafik_Master/01_Logo` übernommen. Primärfarbe `#9E4AC8`, App-Symbolgrund und farbige Darkmode-Gelbrollen `#FFDC0B`. Hellmodus-Ocker, Minimaldesigns und individuelle Oberflächenakzente erhalten. Zentrale Fundorte und zukünftiger Ablauf in der [Logo-Übersicht](../../../../../20_Grafik_Master/README.md).

## Umsetzung und Belege

- Alte Master, Affinity-Datei, Laufzeit-/Paketsymbole und frühere Marketingaufnahme auf ausdrücklichen Benutzerauftrag archiviert; 34 erhaltene Dateien mit SHA-256, Manifest im Grafikarchiv. Historische QA-/Referenzbilder und alte Pakete nicht retuschiert oder umetikettiert.
- Beide neuen SVGs in Normal-/Kleingrößen bytegleich zur Quelle. Der App-Zuschnitt erhält die vollständige originale viewBox einschließlich gelbem Rechteck; die Kontur des G allein wäre dafür falsch.
- `brand.py` führt die Farben zentral; `logo_abgleich.py` verteilt und erzeugt Raster-/Paketsymbole, Favicons und allgemeine Exporte. Der Vergleichslauf meldet null Abweichungen.
- Quelle/Python mit 93 Code-Dateien und 171 Ressourcen abgeglichen. Echte neue Windows-Aufnahme der Showcase-Seite für die Dokumentation; Vorschauen vor der Aufnahme fertig geladen.
- Bestehende Logo330-/Logo3370-Suiten und Dialog-Themes grün. Neue Markenprüfung kontrolliert SVG-Kopien, transparente Ecken, beide Farben in SVG/PNG und allen sieben tatsächlichen ICO-Einträgen sowie fünf farbige dunkle Designs. Neun SVG- und sechs Raster-Unit-Tests grün. Gegenprobe auf der Vorfassung scheitert gezielt am alten Master.
- Erster Logo330-Nachlauf traf mit dem alten Farbsampler eine geglättete Kante der neuen G-Form. Probe auf häufigste Flächenfarbe berichtigt, ohne Toleranzen oder Kontrastgrenzen zu lockern; Rohrot lokal erhalten.

Aktueller Apphash, Eingangs-/Ausgabedateihashes und Abschlussstatus in [ergebnis.json](ergebnis.json). Rohlogs und eigene Dunkelaufnahme lokal unter `%USERPROFILE%/gq/logo1105/`. Keine echten Nutzerdaten verwendet.

## Native Lieferung und menschliche Abnahme

Auf diesem Rechner fehlt die bisherige Tk-9.1-Bauablage; kein verfügbarer MSVC-/Paketbauplatz. Benutzer bestätigt, die nativen Neubauten heute Abend am vorhandenen Bauplatz durchzuführen. Windows-EXE/PE-Icon, Mac-Bundle/ICNS/Signatur und tatsächliche Taskleisten-/Dock-/Explorer-/Finder-/Menü-/Vorschauanzeigen bleiben deshalb ausdrücklich offen. Quellen und Symbolressourcen sind vorbereitet, bisherige native Pakete bleiben ihre historischen Lieferstände.

Dateitypsymbole für Glide-Datendateien hängen von einer OS-Zuordnung beziehungsweise einem noch nicht fertigen Installervertrag ab; keine neue Systemregistrierung durchgeführt. Kein Commit, Push oder Release. Die Dokumentationsaufnahme belegt die Quellfassung, kein neu gebautes Paket und keine menschliche Freigabe.

## Lokaler Abschluss

Strenge CI-Grundstufe auf App `ce60fd8c…` **19/19 grün**: Syntax/Version/Dokumente/Fixtures, 244 Werkzeugtests (ein Skip), zweimal 1.129 Fachtests, Analysen, Tk-/Startprobe, strenger Liefervergleich, Fremdcode/Datenschutz/Ablage/Synchronisation. Grundprüfung ist keine neue Plattform-Vollmatrix. Eingefrorene Python-Prüffassung mit neuer G-Kontur und Buchbreite sowie eigener Kopie des geschlossenen synthetischen Nachtestbestands bereitgestellt. Native Neubauten und menschliche Logo-/Shell-/DPI-Abnahmen bleiben wie oben offen.
