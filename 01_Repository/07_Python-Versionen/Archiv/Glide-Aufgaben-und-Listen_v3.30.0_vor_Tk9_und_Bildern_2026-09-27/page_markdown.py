"""Markdown ↔ Seitendokument für die Seitenart „Seite“ (26.09.2026).

Seiten sind für KI-erzeugte Berichte gedacht; die kommen als Markdown. Dieses
Modul übersetzt Markdown in das Dokumentmodell des Seiteneditors – Text plus
Formatbereiche (`spans`) und Links, dasselbe Modell wie die Notiz – und zurück.
Nur Standardbibliothek, ohne Tk.

Unterstützt: Überschriften, Absätze, Aufzählung und Nummerierung (auch
verschachtelt), Aufgaben (`- [ ]`, `- [x]`), Zitate, Codeblöcke, Trennlinien,
Tabellen sowie fett, kursiv, durchgestrichen, Code und Links im Text.

Aufgaben entstehen hier nur als Platzhalter (`taskref:N`); aus ihnen macht der
Aufrufer echte Glide-Punkte und ersetzt den Platzhalter durch `item:<id>`.
"""

import re

BULLET = "•"
DIVIDER = "―" * 24
INDENT_TAGS = ("indent1", "indent2", "indent3")

_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_TASK = re.compile(r"^(\s*)[-*+]\s+\[([ xX])\]\s+(.*)$")
_BULLET = re.compile(r"^(\s*)[-*+]\s+(.*)$")
_NUMBER = re.compile(r"^(\s*)(\d{1,4})[.)]\s+(.*)$")
_QUOTE = re.compile(r"^\s*>\s?(.*)$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_RULE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_SEPARATOR = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)[^)]*\)")
_AUTOLINK = re.compile(r"<(https?://[^>\s]+)>")
_BARE_URL = re.compile(r"(?<![\w(\[\"'])(https?://[^\s<>()]+[^\s<>().,;:!?\"'])")
_SAFE_URL = re.compile(r"^(https?://|mailto:)[^\s]+$")


def looks_like_markdown(text):
    """Grobe Erkennung, ob eingefügter Text Markdown ist (für das Einfügen)."""
    if not isinstance(text, str) or "\n" not in text.strip():
        return bool(re.search(r"\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\)", text or ""))
    treffer = 0
    for zeile in text.splitlines()[:200]:
        if (_HEADING.match(zeile) or _TASK.match(zeile) or _BULLET.match(zeile) or _NUMBER.match(zeile)
                or _QUOTE.match(zeile) or _FENCE.match(zeile) or _TABLE_ROW.match(zeile)):
            treffer += 1
    return treffer >= 2 or bool(re.search(r"^#{1,6}\s", text, re.MULTILINE))


class _Builder:
    """Sammelt Text und Formatbereiche Zeile für Zeile."""

    def __init__(self):
        self.parts = []
        self.length = 0
        self.spans = []
        self.links = {}
        self.tasks = []
        self._link_index = 0

    def line(self, text, tags=(), inline=True):
        """Hängt eine Zeile an; `tags` gelten für die ganze Zeile."""
        if self.parts:
            self.parts.append("\n")
            self.length += 1
        start = self.length
        if inline:
            text, inline_spans = self.inline(text)
        else:
            inline_spans = []
        self.parts.append(text)
        self.length += len(text)
        end = self.length
        if end > start:
            for tag in tags:
                self.spans.append({"tag": tag, "start": start, "end": end})
            for tag, a, b in inline_spans:
                if a < b:
                    self.spans.append({"tag": tag, "start": start + a, "end": start + b})
        return start, end

    def inline(self, text):
        """Inline-Markdown in reinen Text plus Bereiche (relativ zur Zeile)."""
        text = _IMAGE.sub(lambda m: f"[Bild: {m.group(1) or 'ohne Titel'}]({m.group(2)})", text)
        text = _AUTOLINK.sub(lambda m: f"[{m.group(1)}]({m.group(1)})", text)
        ausgabe, spans, index = [], [], 0
        offen = {}
        muster = re.compile(r"(\*\*|__|~~|`|\*|_)|\[([^\]]+)\]\(([^)\s]+)[^)]*\)")
        while index < len(text):
            treffer = muster.search(text, index)
            if not treffer:
                ausgabe.append(text[index:])
                break
            ausgabe.append(text[index:treffer.start()])
            position = sum(len(teil) for teil in ausgabe)
            if treffer.group(2) is not None:
                inhalt, url = treffer.group(2), treffer.group(3)
                ausgabe.append(inhalt)
                if _SAFE_URL.match(url):
                    self._link_index += 1
                    tag = f"link:md{self._link_index}"
                    self.links[tag] = url
                    spans.append((tag, position, position + len(inhalt)))
                index = treffer.end()
                continue
            zeichen = treffer.group(1)
            if zeichen == "`":
                ende = text.find("`", treffer.end())
                if ende == -1:
                    ausgabe.append(zeichen)
                    index = treffer.end()
                    continue
                inhalt = text[treffer.end():ende]
                ausgabe.append(inhalt)
                spans.append(("code", position, position + len(inhalt)))
                index = ende + 1
                continue
            tag = {"**": "bold", "__": "bold", "~~": "strike", "*": "italic", "_": "italic"}[zeichen]
            # Ein einzelner Unterstrich mitten im Wort (datei_name) ist kein Kursiv.
            if zeichen == "_" and treffer.start() > 0 and text[treffer.start() - 1].isalnum():
                ausgabe.append(zeichen)
                index = treffer.end()
                continue
            if zeichen in offen:
                start = offen.pop(zeichen)
                spans.append((tag, start, position))
            elif text.find(zeichen, treffer.end()) == -1:
                # Ohne schließendes Gegenstück ist es kein Format („5 * 3“).
                ausgabe.append(zeichen)
            else:
                offen[zeichen] = position
            index = treffer.end()
        klartext = "".join(ausgabe)
        for treffer in _BARE_URL.finditer(klartext):
            if any(tag.startswith("link:") and a <= treffer.start() < b for tag, a, b in spans):
                continue
            self._link_index += 1
            tag = f"link:md{self._link_index}"
            self.links[tag] = treffer.group(1)
            spans.append((tag, treffer.start(), treffer.end()))
        return klartext, spans

    def document(self):
        return {"text": "".join(self.parts), "spans": sorted(self.spans, key=lambda s: (s["start"], s["end"], s["tag"])),
                "links": self.links, "tasks": self.tasks}


def _indent_level(prefix):
    breite = len(prefix.replace("\t", "    "))
    return min(len(INDENT_TAGS), breite // 2)


def _table_lines(rows):
    """Tabelle als ausgerichtete Zeilen im Markdown-Format (bleibt exportierbar)."""
    zellen = [[zelle.strip() for zelle in row.strip().strip("|").split("|")] for row in rows]
    spalten = max(len(zeile) for zeile in zellen)
    for zeile in zellen:
        zeile.extend([""] * (spalten - len(zeile)))
    breiten = [max(3, max(len(zeile[i]) for zeile in zellen)) for i in range(spalten)]
    ausgabe = []
    for index, zeile in enumerate(zellen):
        ausgabe.append("| " + " | ".join(zelle.ljust(breiten[i]) for i, zelle in enumerate(zeile)) + " |")
        if index == 0:
            ausgabe.append("|" + "|".join("-" * (breite + 2) for breite in breiten) + "|")
    return ausgabe


def markdown_to_page(markdown):
    """Markdown → {'text', 'spans', 'links', 'tasks'}.

    `tasks` ist eine Liste {'ref', 'text', 'done'}; die Aufgabenzeile trägt die
    Bereiche `task` und `taskref:<ref>`.
    """
    builder = _Builder()
    zeilen = str(markdown or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    absatz = []
    index = 0

    def absatz_schliessen():
        if absatz:
            builder.line(" ".join(teil.strip() for teil in absatz))
            absatz.clear()

    while index < len(zeilen):
        zeile = zeilen[index]
        if not zeile.strip():
            absatz_schliessen()
            index += 1
            continue
        if _FENCE.match(zeile):
            absatz_schliessen()
            zaun = _FENCE.match(zeile).group(1)
            index += 1
            while index < len(zeilen) and not zeilen[index].strip().startswith(zaun):
                builder.line(zeilen[index], ("codeblock",), inline=False)
                index += 1
            index += 1
            continue
        if _TABLE_ROW.match(zeile) and index + 1 < len(zeilen) and _TABLE_SEPARATOR.match(zeilen[index + 1]):
            absatz_schliessen()
            reihen = [zeile]
            index += 2
            while index < len(zeilen) and _TABLE_ROW.match(zeilen[index]):
                reihen.append(zeilen[index])
                index += 1
            for position, text in enumerate(_table_lines(reihen)):
                tags = ("table", "bold") if position == 0 else ("table",)
                builder.line(text, tags, inline=False)
            continue
        if _RULE.match(zeile):
            absatz_schliessen()
            builder.line(DIVIDER, ("divider",), inline=False)
            index += 1
            continue
        treffer = _HEADING.match(zeile)
        if treffer:
            absatz_schliessen()
            stufe = min(3, len(treffer.group(1)))
            builder.line(treffer.group(2), (f"h{stufe}",))
            index += 1
            continue
        treffer = _TASK.match(zeile)
        if treffer:
            absatz_schliessen()
            ref = len(builder.tasks)
            einzug = _indent_level(treffer.group(1))
            tags = ["task", f"taskref:{ref}"] + ([INDENT_TAGS[einzug - 1]] if einzug else [])
            start, end = builder.line(treffer.group(3), tags)
            builder.tasks.append({"ref": ref, "text": "".join(builder.parts)[start:end],
                                  "done": treffer.group(2).lower() == "x"})
            index += 1
            continue
        treffer = _BULLET.match(zeile)
        if treffer:
            absatz_schliessen()
            einzug = _indent_level(treffer.group(1))
            tags = ["bullet"] + ([INDENT_TAGS[einzug - 1]] if einzug else [])
            builder.line(f"{BULLET} {treffer.group(2)}", tags)
            index += 1
            continue
        treffer = _NUMBER.match(zeile)
        if treffer:
            absatz_schliessen()
            einzug = _indent_level(treffer.group(1))
            tags = ["number"] + ([INDENT_TAGS[einzug - 1]] if einzug else [])
            builder.line(f"{treffer.group(2)}. {treffer.group(3)}", tags)
            index += 1
            continue
        treffer = _QUOTE.match(zeile)
        if treffer:
            absatz_schliessen()
            builder.line(treffer.group(1), ("quote",))
            index += 1
            continue
        absatz.append(zeile)
        index += 1
    absatz_schliessen()
    return builder.document()


def page_to_markdown(document, task_state=None):
    """Seitendokument → Markdown.

    `task_state(item_id)` liefert (Titel, erledigt) für eine Aufgabenzeile oder
    None; ohne Angabe gilt die Aufgabe als offen.
    """
    text = str((document or {}).get("text") or "")
    spans = list((document or {}).get("spans") or [])
    links = dict((document or {}).get("links") or {})
    bloecke = []  # (Art, Zeile) – Art bestimmt die Leerzeilen dazwischen

    position = 0
    for zeile in text.split("\n"):
        start, ende = position, position + len(zeile)
        position = ende + 1
        auf_zeile = {span["tag"] for span in spans if span["start"] < max(ende, start + 1) and span["end"] > start}
        if "codeblock" in auf_zeile:
            bloecke.append(("code", zeile))
            continue
        if "table" in auf_zeile:
            bloecke.append(("table", zeile.rstrip()))
            continue
        if "divider" in auf_zeile:
            bloecke.append(("rule", "---"))
            continue
        inhalt = _inline_markdown(zeile, start, spans, links)
        einzug = next((2 * (INDENT_TAGS.index(tag) + 1) for tag in INDENT_TAGS if tag in auf_zeile), 0)
        praefix = " " * einzug
        if "task" in auf_zeile:
            item = next((tag[5:] for tag in auf_zeile if tag.startswith("item:")), None)
            zustand = task_state(item) if item and task_state else None
            erledigt = bool(zustand[1]) if zustand else False
            bloecke.append(("list", f"{praefix}- [{'x' if erledigt else ' '}] {inhalt}"))
        elif "h1" in auf_zeile or "h2" in auf_zeile or "h3" in auf_zeile:
            stufe = 1 if "h1" in auf_zeile else 2 if "h2" in auf_zeile else 3
            bloecke.append(("heading", "#" * stufe + " " + inhalt))
        elif "bullet" in auf_zeile:
            bloecke.append(("list", f"{praefix}- {re.sub('^' + re.escape(BULLET) + r' ?', '', inhalt)}"))
        elif "number" in auf_zeile:
            bloecke.append(("list", f"{praefix}{inhalt}"))
        elif "quote" in auf_zeile:
            bloecke.append(("quote", f"> {inhalt}"))
        elif zeile.strip():
            bloecke.append(("paragraph", inhalt))
        else:
            bloecke.append(("blank", ""))

    ausgabe = []
    vorher = None
    for art, zeile in bloecke:
        if art == "blank":
            vorher = None
            continue
        zusammen = art == vorher and art in ("code", "table", "list", "quote")
        if ausgabe and not zusammen:
            if vorher == "code":
                ausgabe.append("```")
            ausgabe.append("")
        if art == "code" and not zusammen:
            ausgabe.append("```")
        ausgabe.append(zeile)
        vorher = art
    if vorher == "code":
        ausgabe.append("```")
    return "\n".join(ausgabe).strip() + "\n"


def _inline_markdown(zeile, start, spans, links):
    """Inline-Formatierung einer Zeile zurück in Markdown-Zeichen."""
    marken = {"bold": "**", "italic": "*", "strike": "~~", "code": "`"}
    einfuegen = {}
    for span in spans:
        a, b = span["start"] - start, span["end"] - start
        if b <= 0 or a >= len(zeile):
            continue
        a, b = max(0, a), min(len(zeile), b)
        tag = span["tag"]
        if tag in marken:
            einfuegen.setdefault(a, []).append(marken[tag])
            einfuegen.setdefault(b, []).insert(0, marken[tag])
        elif tag in links:
            if zeile[a:b] == links[tag]:
                continue  # nackter Link bleibt nackt
            einfuegen.setdefault(a, []).append("[")
            einfuegen.setdefault(b, []).insert(0, f"]({links[tag]})")
    teile = []
    for index, zeichen in enumerate(zeile):
        teile.extend(einfuegen.get(index, []))
        teile.append(zeichen)
    teile.extend(einfuegen.get(len(zeile), []))
    return "".join(teile)
