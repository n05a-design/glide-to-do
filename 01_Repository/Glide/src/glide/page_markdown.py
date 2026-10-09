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

Bilder (B4 seit 3.34.0): Steht ein Bild allein auf seiner Zeile und findet der
Aufrufer die Datei (`image_resolver`), wird es wieder ein Seitenbild – so
übersteht eine Seite den Weg über Markdown samt Bildern. Sonst bleibt es ein
benannter Verweis im Text.
"""

import os
import re
import urllib.parse
import task_references as task_refs
import object_references as object_refs

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
_IMAGE_LINE = re.compile(r"^\s*!\[([^\]]*)\]\(([^)\s]+)[^)]*\)\s*$")
_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)[^)]*\)")
_AUTOLINK = re.compile(r"<(https?://[^>\s]+)>")
_BARE_URL = re.compile(r"(?<![\w(\[\"'])(https?://[^\s<>()]+[^\s<>().,;:!?\"'])")
_SAFE_URL = re.compile(r"^(https?://|mailto:)[^\s]+$")


def insert_blocks(document, addition, position, link_map):
    """Blöcke einfügen, vorhandene Bilder und geteilte Formatbereiche bewahren."""
    if type(position) is not int or not 0 <= position <= len(document['text']):
        raise ValueError('Ungültige Einfügeposition.')
    delta = len(addition['text']) + 2
    spans = []
    for span in document['spans']:
        start, end = span['start'], span['end']
        if start >= position:
            spans.append(dict(span, start=start + delta, end=end + delta))
        elif end <= position:
            spans.append(dict(span))
        else:
            spans.append(dict(span, end=position))
            spans.append(dict(span, start=position + delta, end=end + delta))
    spans.extend(dict(span, start=span['start'] + position + 1, end=span['end'] + position + 1,
                      tag=link_map.get(span['tag'], span['tag'])) for span in addition['spans'])
    links = dict(document.get('links', {}))
    links.update({link_map.get(tag, tag): url for tag, url in addition.get('links', {}).items()})
    ergebnis = dict(document, text=document['text'][:position] + '\n' + addition['text'] + '\n'
                    + document['text'][position:], spans=spans, links=links)
    if addition.get('images'):
        ergebnis['images'] = dict(document.get('images') or {}, **addition['images'])
    return ergebnis


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
        self.images = {}
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
                if _SAFE_URL.match(url) or object_refs.parse(url):
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
        dokument = {"text": "".join(self.parts),
                    "spans": sorted(self.spans, key=lambda s: (s["start"], s["end"], s["tag"])),
                    "links": self.links, "tasks": self.tasks}
        if self.images:
            dokument["images"] = dict(self.images)
        return dokument


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


def local_image_path(source, base_dir=None):
    """Lokaler Dateipfad eines Markdown-Bildverweises oder None – ohne Dateizugriff.

    `file:`-Adressen und absolute Pfade gelten immer, relative Pfade nur mit
    `base_dir` (Ordner der Markdown-Datei). Andere Adressen (http, data …)
    werden nie geladen.
    """
    quelle = str(source or "").strip()
    if not quelle or len(quelle) > 4096:
        return None
    if quelle.lower().startswith("file:"):
        teile = urllib.parse.urlsplit(quelle)
        if teile.netloc not in ("", "localhost"):
            return None
        from urllib.request import url2pathname
        return url2pathname(teile.path) or None
    if _SCHEME.match(quelle) and not re.match(r"^[A-Za-z]:[\\/]", quelle):
        return None
    pfad = urllib.parse.unquote(quelle)
    if os.path.isabs(pfad):
        return os.path.normpath(pfad)
    return os.path.normpath(os.path.join(base_dir, pfad)) if base_dir else None


def markdown_to_page(markdown, image_resolver=None):
    """Markdown → {'text', 'spans', 'links', 'tasks'} (mit Bildern auch 'images').

    `tasks` ist eine Liste {'ref', 'text', 'done'}; die Aufgabenzeile trägt die
    Bereiche `task` und `taskref:<ref>`. `image_resolver(beschreibung, quelle)`
    liefert für ein Bild allein auf seiner Zeile (Kennung `img:…`, Angaben)
    oder None; dann bleibt es ein Verweis im Text.
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
        treffer = _IMAGE_LINE.match(zeile) if image_resolver else None
        bild = image_resolver(treffer.group(1), treffer.group(2)) if treffer else None
        if bild:
            absatz_schliessen()
            kennung, angaben = bild
            builder.line(IMAGE_ANCHOR, (kennung,), inline=False)
            builder.images[kennung] = angaben
            index += 1
            continue
        treffer = _HEADING.match(zeile)
        if treffer:
            absatz_schliessen()
            # Seit 29.09.2026 auch Überschrift 4 (Blockarten nach Notion).
            stufe = min(4, len(treffer.group(1)))
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


IMAGE_ANCHOR = "\ufffc"


def page_to_markdown(document, task_state=None, image_source=None):
    """Seitendokument → Markdown.

    `task_state(item_id)` liefert (Titel, erledigt) für eine Aufgabenzeile oder
    None; ohne Angabe gilt die Aufgabe als offen. `image_source(info)` liefert
    (Beschreibung, Pfad) für ein Seitenbild (27.09.2026); ohne Angabe steht
    dort „Bild“.
    """
    text = str((document or {}).get("text") or "")
    spans = list((document or {}).get("spans") or [])
    links = dict((document or {}).get("links") or {})
    images = dict((document or {}).get("images") or {})
    bloecke = []  # (Art, Zeile) – Art bestimmt die Leerzeilen dazwischen

    position = 0
    for zeile in text.split("\n"):
        start, ende = position, position + len(zeile)
        position = ende + 1
        auf_zeile = {span["tag"] for span in spans if span["start"] < max(ende, start + 1) and span["end"] > start}
        if IMAGE_ANCHOR in zeile:
            for tag in sorted(tag for tag in auf_zeile if tag in images):
                beschreibung, pfad = image_source(images[tag]) if image_source else ("Bild", "")
                bloecke.append(("image", f"![{beschreibung}]({pfad})" if pfad else f"*[{beschreibung}]*"))
            zeile = zeile.replace(IMAGE_ANCHOR, "")
            if not zeile.strip():
                continue
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
            item = next((task_refs.task_id(tag) for tag in auf_zeile if task_refs.task_id(tag)), None)
            zustand = task_state(item) if item and task_state else None
            erledigt = bool(zustand[1]) if zustand else False
            if zustand and " ".join(zeile.split()) != " ".join(str(zustand[0]).split()):
                inhalt = str(zustand[0])
            bloecke.append(("list", f"{praefix}- [{'x' if erledigt else ' '}] {inhalt}"))
        elif any(f"h{stufe}" in auf_zeile for stufe in (1, 2, 3, 4)):
            stufe = next(stufe for stufe in (1, 2, 3, 4) if f"h{stufe}" in auf_zeile)
            bloecke.append(("heading", "#" * stufe + " " + _ohne_aufklapppfeil(inhalt)))
        elif "toggle" in auf_zeile:
            # Aufklappliste: in Markdown eine Aufzählung, ihr Inhalt eingerückt.
            bloecke.append(("list", f"{praefix}- {_ohne_aufklapppfeil(inhalt)}"))
        elif "callout" in auf_zeile:
            bloecke.append(("quote", f"> {inhalt}"))
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


TOGGLE_PREFIXES = ("▾ ", "▸ ")


def _ohne_aufklapppfeil(text):
    for praefix in TOGGLE_PREFIXES:
        if text.startswith(praefix):
            return text[len(praefix):]
    return text


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


# --- Druckseite (B4 seit 3.34.0) -------------------------------------------
# Eine Seite wird wie für Markdown in Blöcke zerlegt und daraus als HTML
# gesetzt. Bilder kommen als Daten-URL ins HTML, damit die Druckseite keine
# Verweise auf Dateien braucht; zu große Bilder bleiben ein benannter Platzhalter.
IMAGE_PLACEHOLDER = "glide-bild:"
_HTML_IMAGE = re.compile(r"!\[([^\]]*)\]\((" + re.escape(IMAGE_PLACEHOLDER) + r"\d+)\)")
_HTML_LINK = re.compile(r"\[([^\]]+)\]\(((?:https?://|mailto:)[^)\s]+)\)")


def _html(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def _inline_html(zeile, bilder):
    """Inline-Markdown einer Zeile als HTML; Bilder über ihre Platzhalter."""
    teile = []
    pos = 0
    for treffer in _HTML_IMAGE.finditer(zeile):
        teile.append(_inline_text_html(zeile[pos:treffer.start()]))
        beschreibung, quelle = treffer.group(1), bilder.get(treffer.group(2))
        if quelle:
            teile.append(f'<img src="{quelle}" alt="{_html(beschreibung)}">')
        else:
            teile.append(f'<span class="image-missing">[Bild: {_html(beschreibung)}]</span>')
        pos = treffer.end()
    teile.append(_inline_text_html(zeile[pos:]))
    return "".join(teile)


def _inline_text_html(text):
    links = []

    def link(treffer):
        links.append((treffer.group(1), treffer.group(2)))
        return f"\x00{len(links) - 1}\x00"
    text = _HTML_LINK.sub(link, text)
    text = _html(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"~~([^~]+)~~", r"<s>\1</s>", text)
    for index, (titel, ziel) in enumerate(links):
        text = text.replace(f"\x00{index}\x00", f'<a href="{_html(ziel)}">{_html(titel)}</a>')
    return text


def markdown_to_print_html(markdown, bilder=None):
    """HTML-Körper aus dem Markdown, das `page_to_markdown` schreibt.

    Kennt genau dessen Formen: Überschriften, Absätze, Listen mit Einzug,
    Aufgaben, Zitate, Codeblöcke, Tabellen und Trennlinien. `bilder` ordnet
    Platzhalter (`glide-bild:N`) einer Daten-URL zu.
    """
    bilder = bilder or {}
    zeilen = str(markdown or "").split("\n")
    html = []
    i = 0
    while i < len(zeilen):
        zeile = zeilen[i]
        if not zeile.strip():
            i += 1
            continue
        if zeile.startswith("```"):
            block = []
            i += 1
            while i < len(zeilen) and not zeilen[i].startswith("```"):
                block.append(zeilen[i])
                i += 1
            html.append("<pre>" + _html("\n".join(block)) + "</pre>")
            i += 1
            continue
        kopf = _HEADING.match(zeile)
        if kopf:
            stufe = min(4, len(kopf.group(1)) + 1)  # h1 ist der Seitentitel
            html.append(f"<h{stufe}>{_inline_html(kopf.group(2), bilder)}</h{stufe}>")
            i += 1
            continue
        if _RULE.match(zeile):
            html.append("<hr>")
            i += 1
            continue
        if _TABLE_ROW.match(zeile):
            reihen = []
            while i < len(zeilen) and _TABLE_ROW.match(zeilen[i]):
                if not _TABLE_SEPARATOR.match(zeilen[i]):
                    zellen = [zelle.strip() for zelle in zeilen[i].strip().strip("|").split("|")]
                    reihen.append("<tr>" + "".join(f"<td>{_inline_html(z, bilder)}</td>" for z in zellen) + "</tr>")
                i += 1
            html.append("<table>" + "".join(reihen) + "</table>")
            continue
        if _QUOTE.match(zeile):
            block = []
            while i < len(zeilen) and _QUOTE.match(zeilen[i]):
                block.append(_inline_html(_QUOTE.match(zeilen[i]).group(1), bilder))
                i += 1
            html.append("<blockquote>" + "<br>".join(block) + "</blockquote>")
            continue
        if _TASK.match(zeile) or _BULLET.match(zeile) or _NUMBER.match(zeile):
            punkte = []
            while i < len(zeilen) and (_TASK.match(zeilen[i]) or _BULLET.match(zeilen[i]) or _NUMBER.match(zeilen[i])):
                aufgabe, punkt, nummer = _TASK.match(zeilen[i]), _BULLET.match(zeilen[i]), _NUMBER.match(zeilen[i])
                if aufgabe:
                    einzug, inhalt = len(aufgabe.group(1)), aufgabe.group(3)
                    erledigt = aufgabe.group(2) in "xX"
                    inhalt = ('<span class="box done">✓</span>' if erledigt else '<span class="box"></span>') + \
                        (f'<s>{_inline_html(inhalt, bilder)}</s>' if erledigt else _inline_html(inhalt, bilder))
                elif nummer:
                    einzug, inhalt = len(nummer.group(1)), f"{nummer.group(2)}. " + _inline_html(nummer.group(3), bilder)
                else:
                    einzug, inhalt = len(punkt.group(1)), "• " + _inline_html(punkt.group(2), bilder)
                punkte.append(f'<li style="margin-left: {einzug * 6}pt">{inhalt}</li>')
                i += 1
            html.append('<ul class="page">' + "".join(punkte) + "</ul>")
            continue
        absatz = []
        while i < len(zeilen) and zeilen[i].strip() and not (
                zeilen[i].startswith("```") or _HEADING.match(zeilen[i]) or _RULE.match(zeilen[i])
                or _TABLE_ROW.match(zeilen[i]) or _QUOTE.match(zeilen[i]) or _TASK.match(zeilen[i])
                or _BULLET.match(zeilen[i]) or _NUMBER.match(zeilen[i])):
            absatz.append(_inline_html(zeilen[i], bilder))
            i += 1
        html.append("<p>" + "<br>".join(absatz) + "</p>")
    return "\n".join(html)


def page_to_print_html(document, task_state=None, image_data=None, max_image_bytes=6_000_000,
                       max_total_bytes=30_000_000):
    """Seitendokument → HTML-Körper der Druckseite (B4).

    `image_data(info)` liefert (Beschreibung, MIME-Typ, Bytes) eines
    Seitenbilds oder None. Bilder über `max_image_bytes` oder über die
    Gesamtgrenze bleiben ein benannter Platzhalter.
    """
    import base64
    bilder, quellen = {}, []
    gesamt = [0]

    def quelle(info):
        nummer = len(quellen)
        quellen.append(info)
        platzhalter = f"{IMAGE_PLACEHOLDER}{nummer}"
        daten = image_data(info) if image_data else None
        if daten:
            beschreibung, mime, roh = daten
            if roh and len(roh) <= max_image_bytes and gesamt[0] + len(roh) <= max_total_bytes:
                gesamt[0] += len(roh)
                bilder[platzhalter] = f"data:{mime};base64," + base64.b64encode(roh).decode("ascii")
            return str(beschreibung or "Bild").replace("]", ")"), platzhalter
        return "Bild", platzhalter
    markdown = page_to_markdown(document, task_state, quelle)
    return markdown_to_print_html(markdown, bilder)
