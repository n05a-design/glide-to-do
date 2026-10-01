# Abschlussbericht – Bestandsanalyse 3.2.0

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

## 1. Was ich geändert habe

- Aktive technische Dokumentation, Übergabe, Startkontext, Release-Checkliste
  und Produktunterlagen auf den tatsächlichen Stand abgeglichen; Einstieg:
  [Dokumentationsindex](00_INDEX.md).
- Die Word-Arbeitsgrundlage auf 3.2.0 fortgeschrieben, ursprüngliche Struktur
  erhalten und Vorgänger archiviert; Datei im äußeren `10_Dokumentation/`.
- Zwei Windows-Testannahmen und eine eng begrenzte Schriftmetrik-Prüfung
  korrigiert; alle drei Suiten und der abschließende Vollmodus erfolgreich.
- [Gemeinsames Prüfwerkzeug](../tests/tools/pruefen.py) und
  [Erzeuger der Arbeitslisten](../tests/tools/releasedaten.py) bereitgestellt.
- Eine [Glide-Backupdatei](../tests/fixtures/archiv/glide_releaseplanung_3.2.0.glidebackup)
  mit drei Arbeitslisten, 114 Punkten, Quellen und offenen Entscheidungen
  erzeugt, testabgedeckt und in Hell/Dunkel auf Windows visuell geprüft.
- [Bestandsanalyse](11_BESTANDSANALYSE.md), vollständigen Index und
  nachvollziehbare dezentrale Archive angelegt beziehungsweise vervollständigt.

## 2. Was ich gefunden, aber nicht geändert habe

Die Labelgrenze kann durch ein Systemlabel überschritten werden; ein
Einrückweg kann die zulässige Punkttiefe überschreiten. Beide Fehler sind
reproduziert. Die Behebung muss alle betroffenen Änderungswege konsistent
abdecken. Drei Emoji-Symbolarten bestehen außerhalb von `ICONS`; beim
Gruppenmarker betrifft ein Austausch außerdem TXT-Kompatibilität.
Außerdem werden gemeinsame Änderungsrahmen und Bestandswächter noch nicht
von allen vorgesehenen Wegen verwendet; diese Architekturreststellen sind
als offen dokumentiert. Der App-Quelltext blieb unverändert und bytegleich zur externen 3.2.0-Datei.

## 3. Was ich nicht feststellen konnte

Die Behebung der ursprünglichen Einfriermeldung ist nicht verifiziert.
Ohne Git-Historie sind eine verlorene „Phase 11“, ehemalige Zufallslaufwerkzeuge
und die frühere Bedeutung der Dokumentnummern 03/04 nicht belegbar.

## 4. Was nur du entscheiden kannst

Publisher, Copyright, Kontakte/URLs, Lizenz und Preis, Plattformkennungen,
Architekturen, Mindestversionen, Vertriebswege und Markenfreigabe bleiben offen.

## 5. Was noch manuell zu prüfen ist

Windows-/macOS-Matrix, längere Dialogbenutzung, mehrere Monitore und DPI-Stufen,
reale Eingabegeräte, große Bestände und Restore mit echten Datenkopien.
Build, Signing, Notarisierung und Store-Abnahme stehen aus.

## 6. Empfohlener nächster Schritt

Zuerst die beiden belegten Grenzwertfehler gezielt absichern. Parallel die
Release-Arbeitslisten in einer isolierten Ablage ansehen und die Windows-
Prüfmatrix abarbeiten.

**Ein Komplettbackup ersetzt den gesamten vorhandenen Bestand.** Vor dem
Einlesen eigene Daten vollständig sichern; zum Ausprobieren bevorzugt einen
separaten Datenordner über `GLIDE_DATA_DIR` verwenden.
