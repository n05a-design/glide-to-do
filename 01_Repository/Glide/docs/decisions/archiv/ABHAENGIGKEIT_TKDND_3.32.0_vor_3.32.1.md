# Entscheidung: tkinterdnd2 für das Ziehen aus Finder und Explorer

Stand 30.09.2026 · Glide 3.32.0 · entschieden vom Inhaber am 27.09.2026

AGENTS.md, Regel 4: keine neue Laufzeitabhängigkeit ohne dokumentierte
Entscheidung. Dies ist sie.

## Anlass

Bilder sollen sich aus Finder oder Explorer in die Galerie und in Seiten
ziehen lassen. Tk kann das selbst nicht; `tkinter.dnd` wirkt nur innerhalb
einer Anwendung. Der übliche Weg ist die Tk-Erweiterung tkDnD, in Python
über tkinterdnd2.

Die Entscheidungsvorlage empfahl, damit bis zum Release-Build zu warten. Der
Inhaber fragte, warum nicht schon jetzt zum Testen, und wählte: „Ins Projekt
legen“.

## Was im Projekt liegt

| Angabe | Wert |
|---|---|
| Paket | tkinterdnd2 0.6.3 (PyPI, 04.09.2026) |
| Datei | `tkinterdnd2-0.6.3-py3-none-any.whl`, 816.576 Bytes |
| SHA-256 | `50c7386302104bfb30d8e15b4cc53c0581bc51a28186ff4d7ad3cb2cc820c936` |
| Lizenz | MIT (`src/glide/vendor/tkinterdnd2/LICENSE`); tkDnD von Georgios Petasis, BSD-artig |
| Inhalt | Python-Hülle und tkDnD-Bibliotheken für macOS arm64/x64, Windows x64/x86/arm64 und Linux x64/arm64, je für Tk 8.6 und Tk 9 |
| Ort | `src/glide/vendor/tkinterdnd2`, Herkunft in `src/glide/vendor/provenance.json` |
| Größe | 2,6 MB |

## Wie Glide es nutzt

- Es wird erst beim ersten Gebrauch geladen (`file_drop_support`). Glide
  ändert dafür weder die Klasse des Hauptfensters noch den Start.
- Beim Laden entsteht kein `__pycache__` neben dem Paket. Der Ordner liegt im
  synchronisierten Ablageordner und im signierten Bundle.
- Fehlt der Ordner oder lädt die Bibliothek nicht, bleibt alles, wie es war:
  „Bilder hinzufügen …“ bzw. „Bild“.
- `GLIDE_NO_FILE_DROP=1` schaltet das Ziehen ab, etwa zur Fehlersuche.
- Das macOS-Bundle (`packaging/macos/baue_app.py`) nimmt nur die
  macOS-Bibliotheken mit.

## Geprüft und offen

- Unter macOS (Darwin 27) mit Python 3.14.5 und Tk 9.0.3 geladen (`tkdnd` 2.10.2),
  mit einer Galerie und einer Seite als Ziel.
- Das echte Ziehen mit der Maus aus dem Finder ist eine manuelle Prüfung.
- Windows und Linux sind ungeprüft.
- Für die Veröffentlichung müssen die nativen Bibliotheken mitsigniert und
  notarisiert werden. Die macOS-Bibliothek ist bisher nur ad hoc signiert.

## Aktualisieren

Eine neue Fassung wird wie diese geholt: Wheel von PyPI laden, Prüfsumme
notieren, den Ordner `tkinterdnd2` samt `LICENSE` ersetzen,
`provenance.json` fortschreiben, `test_bilder330` und
`test_paketierung330` laufen lassen.
