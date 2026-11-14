# Assets

Stand 14.11.2026 · Glide 3.61.0 · Aufgabenformat 26 · Einstellungen 2 · Vorlagen 2

Hier liegen Installer- und Paketierungs-Assets, die reproduzierbar aus den
freigegebenen Mastern in `20_Grafik_Master` entstehen. Laufzeitgrafiken
liegen nicht hier, sondern bei der App unter `src/glide/resources/logo/`.

| Datei | Zweck | Erzeugt von |
|---|---|---|
| `icons/glide.ico` | Windows: Programm- und Verknüpfungssymbol, 16 bis 256 px | `packaging/baue_symbole.py` |
| `icons/glide_macos_1024.png` | macOS: Grundlage für `Glide.icns`, mit Apples Rand (824 von 1024 px) | `packaging/baue_symbole.py` |
| `icons/glide_512.png` | Linux (`.desktop`) und Store-Symbole, randlos | `packaging/baue_symbole.py` |

Quelle aller drei ist `src/glide/resources/logo/glide-app-icon.svg`, eine
unveränderte Kopie von `20_Grafik_Master/01_Logo/svg/Logo_Glide-03.svg`.
Bei einer Änderung am Master die [zentrale Logo-Checkliste](../../../20_Grafik_Master/README.md) und `scripts/pflege/logo_abgleich.py` verwenden. `marketing/` enthält die aktuelle Windows-Galerie für das GitHub-README.

Store-Grafiken (Screenshots, Werbebilder) gibt es noch nicht; ihre
Anforderungen stehen in der [Veröffentlichung](../docs/10_VEROEFFENTLICHUNG.md).
