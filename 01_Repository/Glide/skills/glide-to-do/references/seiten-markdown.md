# Seiten als Markdown

Stand 16.11.2026 · Glide 3.69.0 · Aufgabenformat 26

Eine Glide-Seite ist für lange, formatierte Texte gedacht: Recherchen, Berichte, Übersichten, Protokolle. Der Nutzer importiert die Datei über Datei › Importieren › „Seite aus Datei …“ (`.md`, `.markdown`, `.txt`, bis 5 Mio. Zeichen) oder kopiert den Text und wählt „Seite aus Zwischenablage“. Die Seite entsteht auf oberster Ebene; der Nutzer verschiebt sie bei Bedarf in einen Ordner.

## Aufbau

- **Erste Zeile `# Titel`** – sie wird der Seitentitel (höchstens 40 Zeichen) und erscheint nicht doppelt im Text. Ohne Überschrift wird die erste Zeile zum Titel.
- Danach normaler Markdown-Text.

## Was Glide umwandelt

| Markdown | In Glide |
|---|---|
| `## …` bis `#### …` | Überschrift 2–4 (tiefere Ebenen werden Ebene 4) |
| Absatz | Absatz |
| `- …`, `* …`, `1. …`, eingerückt bis drei Stufen | Aufzählung, Nummerierung, Einzug |
| `- [ ] …`, `- [x] …` | **echte Glide-Aufgaben** der Seite, offen oder erledigt; Titel höchstens 40 Zeichen |
| `> …` | Zitat |
| ```` ``` ```` … ```` ``` ```` | Codeblock |
| `---` | Trennlinie |
| Tabelle mit Kopfzeile und Trennzeile | Tabelle, Kopfzeile fett |
| `**fett**`, `*kursiv*`, `~~durchgestrichen~~`, `` `Code` `` | Zeichenformat |
| `[Text](https://…)`, `<https://…>`, `mailto:` | Link |
| Bildzeile wie im Beispiel unten, allein auf einer Zeile | Seitenbild, wenn die Datei neben der `.md` liegt; Netzadressen lädt Glide nie |

```markdown
![Grundriss zweites Obergeschoss](grundriss.png)
```

## Was nicht ankommt

Unterstreichen, Markieren, Hinweis- und Aufklappblöcke gibt es in Glide, aber nicht über Markdown; `> [!NOTE]` wird ein Zitat. HTML wird nicht als Format übernommen. Fälligkeiten, Labels und Aufwand für Aufgaben in einer Seite setzt der Nutzer in Glide; wer sie gleich mitliefern will, legt die Aufgaben zusätzlich oder stattdessen als `.glideexchange` an.

## Gute Seiten

- Oben ein kurzer Abschnitt mit dem Ergebnis, dann Begründung und Details.
- Tabellen für Vergleiche, Zitate für Empfehlungen, Aufgaben nur für echte nächste Schritte.
- Quellen mit Abrufdatum am Ende; Schätzungen als solche kennzeichnen.
