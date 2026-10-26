"""Lesende Nebenansicht im Inspektorbereich ohne Tk (E-U2 A, D55, 23.10.2026).

Die Nebenansicht zeigt einen zweiten Inhalt – Liste, Seite oder Notiz – neben
der eigentlichen Arbeit. Bearbeitet wird weiter im Hauptbereich; nebenan gibt
es nur gezielte Originalaktionen (Aufgabe abhaken über den bestehenden Weg,
„Öffnen“). Dieses Modul bestimmt, ob ein Ziel lesbar ist, und bereitet seinen
Inhalt als Zeilen auf. Es kennt keine Widgets und ändert keine Daten.

Ziel ist immer eine stabile Listen-ID. Undo kann Objekte ersetzen; die
Oberfläche löst die ID deshalb bei jedem Abgleich neu auf.
"""

import bisect
import hashlib
import re

IMAGE_ANCHOR = "￼"
LINE_STYLES = ("h1", "h2", "h3", "h4", "codeblock", "quote", "callout", "table", "divider",
               "bullet", "number", "task", "toggle", "toggle_closed")
INLINE_STYLES = ("bold", "italic", "underline", "strike", "code", "highlight")
INDENT_TAGS = {"indent1": 1, "indent2": 2, "indent3": 3}
TASK_TAG = re.compile(r"^(item|taskref):(.+)$")
MAX_ROWS = 2000
MAX_LINES = 5000

UNSUPPORTED_KINDS = {"drawing": "Zeichnungen", "gallery": "Galerien"}

STATE_TEXT = {
    "missing": "Dieser Inhalt ist nicht mehr vorhanden.",
    "trash": "Dieser Inhalt liegt im Papierkorb. Über den Papierkorb lässt er sich wiederherstellen.",
}


def target_for(entry):
    """Normalisiertes Ziel einer Liste/Seite/Notiz oder None."""
    if isinstance(entry, dict) and isinstance(entry.get("id"), str) and entry.get("id"):
        return {"kind": "list", "id": entry["id"]}
    return None


def normalize_target(value):
    if (isinstance(value, dict) and value.get("kind") == "list" and isinstance(value.get("id"), str)
            and 0 < len(value["id"]) <= 200):
        return {"kind": "list", "id": value["id"]}
    return None


def _trash_contains(trash, identity):
    """Liegt die Liste (einzeln oder mit ihrem Ordner) im Papierkorb?"""
    for value in trash or ():
        if not isinstance(value, dict):
            continue
        holder = value.get("list")
        if isinstance(holder, dict) and holder.get("id") == identity:
            return True
        folder = value.get("folder")
        if isinstance(folder, dict) and any(isinstance(entry, dict) and entry.get("id") == identity
                                            for entry in folder.get("lists", ()) or ()):
            return True
    return False


def availability(entry, identity=None, trash=()):
    """(Zustand, Hinweis) eines Ziels.

    ``ok`` – lesbar; ``archived`` – lesbar, im Archiv; ``unsupported`` –
    Zeichnung/Galerie, nur über „Öffnen“; ``trash``/``missing`` – nicht mehr da.
    """
    if not isinstance(entry, dict):
        return ("trash", STATE_TEXT["trash"]) if identity and _trash_contains(trash, identity) else (
            "missing", STATE_TEXT["missing"])
    kind = entry.get("list_kind") or "tasks"
    if kind in UNSUPPORTED_KINDS:
        return ("unsupported", f"{UNSUPPORTED_KINDS[kind]} zeigt die Nebenansicht nicht. "
                               "„Öffnen“ zeigt den Inhalt im Hauptbereich.")
    if entry.get("archived"):
        return "archived", "Im Archiv · nur lesen"
    return "ok", ""


def content_kind(entry):
    """'page', 'note' oder 'tasks' für die Darstellung."""
    kind = entry.get("list_kind") if isinstance(entry, dict) else None
    return kind if kind in ("page", "note") else "tasks"


def reference_target(key, index):
    """Aktuelles, lesbares Verweisziel samt Heimatcontainer; keine gespeicherte Kopie."""
    if not isinstance(key, tuple) or len(key) != 2 or key[0] not in ("list", "item"):
        return None
    found = index.get(key)
    if found is None:
        return None
    state, _holder, entry = found
    if state not in ("active", "archived") or not isinstance(entry, dict):
        return None
    if availability(entry)[0] == "unsupported":
        return None
    return {"list_id": entry["id"], "item_id": key[1] if key[0] == "item" else None}


def list_rows(items, limit=MAX_ROWS):
    """Punkte einer Liste als flache Zeilen in Anzeigereihenfolge.

    Jede Zeile: ``{"id", "text", "done", "depth", "kind", "due", "toggle"}``.
    ``toggle`` ist True für echte Aufgaben (Aufgabe, Langtext); Gruppen und
    Zwischenüberschriften lassen sich nicht abhaken.
    """
    rows = []

    def visit(values, depth):
        for item in values or ():
            if len(rows) >= limit:
                return
            if not isinstance(item, dict):
                continue
            kind = item.get("kind") if item.get("kind") in ("task", "group", "long", "heading") else "task"
            text = " ".join(str(item.get("text") or "").split())
            rows.append({"id": item.get("id"), "text": text, "done": bool(item.get("done")), "depth": depth,
                         "kind": kind, "due": item.get("due") or "", "toggle": kind in ("task", "long")})
            visit(item.get("children"), depth + 1)

    visit(items, 0)
    return rows


def list_summary(rows):
    """Kurze Zeile „3 offen · 2 erledigt“ für den Kopf."""
    tasks = [row for row in rows if row["toggle"]]
    if not tasks:
        return "Keine Aufgaben"
    done = sum(1 for row in tasks if row["done"])
    open_count = len(tasks) - done
    parts = [f"{open_count} offen"] if open_count else []
    if done:
        parts.append(f"{done} erledigt")
    return " · ".join(parts)


def page_projection(document, limit=MAX_LINES):
    """Lesbare Projektion eines Seiten-/Notizdokuments.

    Liefert ``{"text", "lines", "inline", "images", "truncated"}``:

    - ``text``: Dokumenttext bis zur Zeilengrenze, unverändert (Versätze bleiben gültig),
    - ``lines``: je Zeile ``{"line", "style", "indent", "task", "reference"}``,
    - ``inline``: ``(start, ende, format)`` für Fett, Kursiv usw. innerhalb des Texts,
    - ``images``: Versätze der unsichtbaren Bildanker.
    """
    text = document.get("text", "") if isinstance(document, dict) else ""
    spans = document.get("spans", []) if isinstance(document, dict) else []
    text = text if isinstance(text, str) else ""
    raw_lines = text.split("\n")
    truncated = len(raw_lines) > limit
    if truncated:
        raw_lines = raw_lines[:limit]
        text = "\n".join(raw_lines)
    starts = []
    offset = 0
    for line in raw_lines:
        starts.append(offset)
        offset += len(line) + 1
    tags = [set() for _ in raw_lines]
    inline = []
    for span in spans if isinstance(spans, list) else ():
        if not isinstance(span, dict):
            continue
        tag, start, end = span.get("tag"), span.get("start"), span.get("end")
        if not isinstance(tag, str) or type(start) is not int or type(end) is not int or not 0 <= start < end:
            continue
        if tag in INLINE_STYLES:
            if start < len(text):
                inline.append((start, min(end, len(text)), tag))
            continue
        if tag not in LINE_STYLES and tag not in INDENT_TAGS and not TASK_TAG.match(tag):
            continue
        if TASK_TAG.match(tag):
            # Eine Aufgabe gehört zu jeder Zeile, die ihr Bereich berührt.
            index = max(0, bisect.bisect_right(starts, start) - 1)
        else:
            # Zeilenformate beginnen am Zeilenanfang und reichen über den Umbruch.
            index = bisect.bisect_left(starts, start)
        while index < len(starts) and starts[index] < end:
            tags[index].add(tag)
            index += 1
    lines = []
    for number, values in enumerate(tags, start=1):
        style = next((name for name in LINE_STYLES if name in values), "body")
        if style == "toggle_closed":
            style = "toggle"
        indent = max((INDENT_TAGS[name] for name in values if name in INDENT_TAGS), default=0)
        task = reference = None
        for name in sorted(values):
            match = TASK_TAG.match(name)
            if match:
                task, reference = match.group(2), match.group(1) == "taskref"
                break
        if task:
            style = "task" if style in ("body", "task", "bullet", "number") else style
        line_text = raw_lines[number - 1]
        if IMAGE_ANCHOR in line_text:
            style = "image"
        lines.append({"line": number, "style": style, "indent": indent, "task": task, "reference": bool(reference)})
    images = [position for position, char in enumerate(text) if char == IMAGE_ANCHOR]
    return {"text": text, "lines": lines, "inline": sorted(inline), "images": images, "truncated": truncated}


def page_tasks(projection):
    """IDs der Aufgabenzeilen einer Projektion in Reihenfolge, ohne Doppelte."""
    return list(dict.fromkeys(line["task"] for line in projection["lines"] if line["task"]))


def signature(entry, done_states=(), extra=()):
    """Vergleichswert für den Abgleich: ändert sich, sobald sich Sichtbares ändert.

    Bewusst ohne vollständige JSON-Kopie großer Dokumente; der Text geht als
    Prüfsumme ein.
    """
    if not isinstance(entry, dict):
        return ("none",) + tuple(extra)
    document = entry.get("rich_note") if isinstance(entry.get("rich_note"), dict) else {}
    text = document.get("text", "") if isinstance(document.get("text", ""), str) else ""
    digest = hashlib.sha1(text.encode("utf-8", "replace")).hexdigest()
    span_digest = hashlib.sha1(repr(document.get("spans", [])).encode("utf-8", "replace")).hexdigest()
    rows = tuple((row["id"], row["text"], row["done"], row["depth"], row["kind"], row["due"])
                 for row in list_rows(entry.get("items", [])))
    return (entry.get("id"), str(entry.get("title") or ""), entry.get("list_kind"), bool(entry.get("archived")),
            entry.get("folder_id"), digest, span_digest, rows, tuple(done_states)) + tuple(extra)
