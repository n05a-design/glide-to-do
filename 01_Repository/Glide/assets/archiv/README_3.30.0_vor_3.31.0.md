# Assets

Stand 29.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Hier liegen Installer- und Paketierungs-Assets, die reproduzierbar aus den
freigegebenen Mastern in `20_Grafik_Master` entstehen. Laufzeitgrafiken
liegen nicht hier, sondern bei der App unter `src/glide/resources/logo/`.

| Datei | Zweck | Erzeugt von |
|---|---|---|
| `icons/glide.ico` | Windows: Programm- und Verknüpfungssymbol, 16 bis 256 px | `packaging/baue_symbole.py` |
| `icons/glide_macos_1024.png` | macOS: Grundlage für `Glide.icns`, mit Apples Rand (824 von 1024 px) | `packaging/baue_symbole.py` |
| `icons/glide_512.png` | Linux (`.desktop`) und Store-Symbole, randlos | `packaging/baue_symbole.py` |

Quelle aller drei ist `src/glide/resources/logo/glide-app-icon.svg`, eine
unveränderte Kopie von `20_Grafik_Master/02_App-Icon/App-Icon-weiß.svg`. Nach
einer Änderung am Master: kopieren, `python3 packaging/baue_symbole.py`
ausführen (Tk 9 nötig) und die Dateien hier ersetzen.

Store-Grafiken (Screenshots, Werbebilder) gibt es noch nicht; ihre
Anforderungen stehen in der [Releasecheckliste](../docs/10_RELEASE_CHECKLIST.md).
