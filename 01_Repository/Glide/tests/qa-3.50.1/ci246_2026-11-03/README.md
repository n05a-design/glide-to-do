# CI #246: Feste Kopfzeile und Inhaltskante

Datum 03.11.2026 · Reparaturkandidat 3.50.1 auf Basis `6fa00813` · lokale Laufzeit Windows x64, Python 3.14.7, Tk 9.1.0.

## Remote-Befund

Geprüft wurde [Lauf #246](https://github.com/n05a-design/glide-to-do/actions/runs/41641237040) auf `893625c687a553f463a972b5af9b88f5c8c626b4` (3.50.0). Die folgenden lokalen 3.50.1-Commits waren nicht gepusht und sind kein Gegenstand dieses roten Fernlaufs.

- [Windows-Job](https://github.com/n05a-design/glide-to-do/actions/runs/41641237040/job/125945733858): `test_festlayout330`, „Mein Tag“ bei 1280 × 860: Kopf `(290, 12, 968, 56)` → `(290, 12, 968, 59)`. 53 ausgeführte, ein fehlgeschlagener, 71 übersprungene Schritte innerhalb der Vollprüfung.
- [Linux-Job](https://github.com/n05a-design/glide-to-do/actions/runs/41641237040/job/125935897716): `test_aufgaben3380`, Liste bei 1280 × 800: tatsächlicher Inhalt 131 statt höchstens 130 px. Kopf 57 px; Tk-Skalierung 1,3873283395755305. 91 ausgeführte, ein fehlgeschlagener, 33 übersprungene Schritte.
- Die nachfolgende Kalibrierung erkennt 13 absichtliche Defekte korrekt. Fünf Aufgaben3380-Gegenproben sind mangels grüner positiver Basissuite nicht belegbar. Exitcode 1 ist dafür richtig. Die dbus-/AT-SPI-Aktivierung ist kein Fehler. Der frühere Kartenhöhenfehler in `test_features322` wird passiert. Die spätere Seitenflächenprüfung ist in Windows übersprungen und unter Linux wegen des Listenabbruchs noch nicht erreicht.

## Reproduktion und Reparatur

Der Windows-Kopfversatz wurde vor der Änderung im aktuellen lokalen 3.50.1 exakt reproduziert. Die kursiven Pfeilzeichen im Tageshinweis stammen unter Windows aus Segoe UI Symbol statt Rubik und erzwingen einen 19-px-Zeilenrahmen statt der 16-px-Kennzahlenzeile. Der Kopf behält die einmal gewachsene Höhe. Der Hinweis nennt die Pfeile jetzt als Klartext. Ein zusätzlicher Pixel Kopfabschlussreserve entfällt; Glyphen-Schutzränder, Schriftgrößen, Werkzeugabstand und die 130-px-Grenze bleiben unverändert.

Die bestehende Festlayoutprüfung ist danach grün: neun Ansichten, beide Fenstergrößen, Auswahl ohne Verschiebung und Werkzeuge über der Karte. Eine zusätzliche echte Windows-Tk-Probe setzt ausschließlich im lokalen Prüftreiber die aus Linux bekannte Skalierung; alle bestehenden Assertions bleiben aktiv. 36 Messungen einschließlich großer Schrift grün. Bei 1280 × 800/mittel: Liste und Heute 130 px, Seite 129 px. Das belegt den Skalierungspfad unter Windows, keine native Linux-Abnahme.

## Abschlussbilanz

Gesamte Aufgaben3380-Suite grün: Inspektor 22, Klicks 30, Bewegung sieben, Flächen je 18 in mittel/groß. Feste Kopfzeile, Logo und Werkzeugzeile grün. Echte Defektprobe „bedienflaeche“ unter Windows passend rot. Strenge Grundstufe 19/19 grün: 242 Werkzeugtests (ein Skip), zweimal 1.124 Fachtests, Appstart und strenger Liefervergleich. Python: 92 Code-Dateien und 171 Ressourcen bytegleich. [Maschinenlesbare Bilanz](ergebnis.json). Rohprotokolle bleiben lokal. Python-Abgleich erfolgt nach der Quellkorrektur; neue Remote-Vollmatrix, native Pakete und menschliche DPI-/Sichtabnahme bleiben offen. Historische rote Ergebnisse werden nicht umetikettiert.

Zuordnung: Die Prozessnummer 23684 aus der vom Inhaber kopierten Kalibrierung stimmt mit dem Linux-Job von #246 überein. Zuerst wurde Vorgängerlauf #244 betrachtet; beide haben dieselben ersten Fehler. `main` `893625c6` (Merge PR #59) und `1ba516a8` besitzen nach lokalem/live Git-Abgleich denselben Dateibaum `8ceb781f699661d96fe470cc0bd58c85a5fe9137`. Die identische Ursache ist damit auf beiden Ständen belegt; maßgeblicher letzter main-Lauf ist #246.
