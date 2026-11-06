# Fortgesetzte menschliche Abnahme – 3.50.4

Stand 05.11.2026 · Glide 3.50.4 · Aufgabenformat 26

Auftrag: neuen Stand 3.50.4 beginnen und die menschliche Abnahme fortsetzen. Neue Logo-Master/G-Kontur, Darkmode-Gelb und Buchbreitenkorrektur bleiben enthalten. Gegenüber dem vorherigen Apphash `ce60fd8c…` ändert sich in der Appdatei ausschließlich die Versionskonstante; die neue Neuerungenkarte liegt separat in `release_notes.py`.

Versionen, Testverträge, Beispieldaten/Rundgang/Showcase/Vorlagen und aktive Dokumentstände nachgeführt. Aktuelle Hashes und Prüfungen in [ergebnis.json](ergebnis.json). Strenge Grundstufe und Buchbreitenprobe werden separat auf dem neuen Stand erfasst; alte grüne Ergebnisse werden nicht umetikettiert.

Nach bestehender Aufbewahrungsregel 19 überalterte 3.47.0-Dateien vorab bytegleich lokal gesichert und aus der Arbeitsablage entfernt; [Pfad-/Hashmanifest](aufbewahrung.json). Acht historische Links auf die bytegleich bestätigte Fassung im Ausgangscommit umgestellt. Kein Git-Index geändert. Alte 3.50.2-/3.50.3-Prüffassungen und ihre synthetischen Daten bleiben erhalten.

## Menschliche Fortsetzung

Punkte 1–5 sind auf dem bisherigen nativen Windows-Kandidaten bestanden. Punkt 6 (Buchbreite bei schmalem/breitem Fenster und voller/schmaler/ausgeblendeter Seitenleiste samt Rückwechsel) bleibt bis zur direkten Rückmeldung offen. Danach Seiten-/Zeichenwerkzeuge und übrige Blöcke. Kriterien an der [manuellen Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md).

3.50.4 wird als eingefrorene Python-Prüffassung mit bestehender eigener Tcl/Tk 9.1 und eigener Kopie des bisherigen synthetischen Nachtestbestands bereitgestellt. Keine echten Nutzerdaten. Lokaler Starter unter `%USERPROFILE%/gq/v3504/Nachtest_starten.pyw`.

Native Windows-/Mac-Neubauten und Paket-/Shell-/DPI-Abnahme übernimmt der Benutzer heute Abend am vorhandenen Bauplatz; diese Lieferung nun auf 3.50.4 ausrichten. Hier keine entsprechende Runtime-Bauablage/MSVC-Toolchain. Keine neue native Vollmatrix oder menschliche Gesamtfreigabe, kein Commit/Push/Release.

## Lokaler technischer Abschluss

Auf App `8b3076f9…` strenge Grundstufe **19/19 grün**, einschließlich 244 Werkzeugtests (ein Skip), zweimal 1.129 Fachtests und strenger Liefergleichheit. Bestehende Buchbreitenprobe **64/64 grün**; Showcase über echten Import/Undo/Export/Neustart geprüft und geliefert. Quelle/Python 93 Code-Dateien/171 Ressourcen bytegleich. Kein neuer nativer Plattform-Vollnachweis.

3.50.4-Python-Prüffassung gestartet, Datenbasis eine unabhängige Kopie des synthetischen bisherigen Nachtestbestands. JSON-Bytes vor/nach der Kopie identisch; Sperr-/Sitzungsdateien nicht übernommen. Nach erkannter Benutzerbedienung wurde die ältere Prüffassung geöffnet belassen. Menschlicher Punkt 6 weiterhin offen.
