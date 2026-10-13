"""Begrenzte Notion-Markdown-/CSV-Archive lesen, ohne Entpacken oder Tk.

ZIP-Pfade dienen ausschließlich als Archivkennungen, nie als lokale Pfade.
Der Aufrufer erhält eine Vorschau mit Verlustmeldungen und bewahrt das
Originalarchiv als Anhang des Importberichts. Noch keine Bestandsmutation.
"""
from dataclasses import dataclass
import hashlib
from pathlib import PurePosixPath
import posixpath
import re
import stat
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile
import zlib

import page_markdown
import object_references

MAX_ARCHIVE_BYTES = 200 * 1024 * 1024
MAX_EXPANDED_BYTES = 256 * 1024 * 1024
MAX_MEMBER_BYTES = 32 * 1024 * 1024
MAX_MARKDOWN_BYTES = 4 * 1024 * 1024
MAX_MEMBERS = 5000
_PAGE_ID = re.compile(r"(?:^|[ _-])([0-9a-f]{32}|[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})$", re.I)
_LINK = re.compile(r"(!?)\[([^\]\n]*)\]\(([^\s)]+)([^)]*)\)")
_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff", ".svg"}


class NotionFormatError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Loss:
    path: str
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class Page:
    key: str
    path: str
    title: str
    folders: tuple[tuple[str, str], ...]
    markdown: str
    source_hash: str
    asset_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Export:
    pages: tuple[Page, ...]
    members: dict[str, bytes]
    losses: tuple[Loss, ...]


def safe_member(name):
    if (not isinstance(name, str) or not name or len(name) > 4096 or "\\" in name
            or name.startswith("/") or re.match(r"^[A-Za-z]:", name)
            or any(ord(char) < 32 for char in name)):
        raise NotionFormatError("Das Archiv enthält einen ungültigen Dateipfad.")
    parts = name.rstrip("/").split("/")
    if any(part in ("", ".", "..") or len(part) > 255 for part in parts):
        raise NotionFormatError("Das Archiv enthält einen unzulässigen Dateipfad.")
    return unicodedata.normalize("NFC", "/".join(parts))


def source_key(name):
    path = PurePosixPath(name)
    stem = path.stem if path.suffix.lower() in (".md", ".csv") else path.name
    match = _PAGE_ID.search(stem)
    if match:
        return "notion:" + match.group(1).replace("-", "").lower()
    return "path:" + hashlib.sha256(name.encode("utf-8")).hexdigest()


def plain_title(name):
    stem = PurePosixPath(name).stem if PurePosixPath(name).suffix.lower() in (".md", ".csv") else name
    match = _PAGE_ID.search(stem)
    title = stem[:match.start()].strip(" _-") if match else stem
    return title.strip() or "Ohne Titel"


def local_target(page_path, target, members):
    """Relatives URL-Ziel im Archiv, einschließlich `../` innerhalb des Archivs."""
    if not isinstance(target, str) or len(target) > 4096 or "\\" in target:
        return None
    try:
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            return None
        path = unquote(parsed.path, errors="strict")
    except (ValueError, UnicodeError):
        return None
    if (not path or path.startswith("/") or "\\" in path or re.match(r"^[A-Za-z]:", path)
            or any(ord(char) < 32 for char in path)):
        return None
    candidate = unicodedata.normalize("NFC", posixpath.normpath(posixpath.join(posixpath.dirname(page_path), path)))
    if candidate in (".", "..") or candidate.startswith("../"):
        return None
    return candidate if candidate in members else None


def _links(text):
    """Markdown-Verweise im Text, keine Verweise in Codeblöcken/-spannen."""
    offset, fence = 0, None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            value = marker.group(1)
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
        elif fence is None:
            code = [(match.start(), match.end()) for match in
                    re.finditer(r"(?<!`)(`+)(.*?)\1(?!`)", line)]
            for match in _LINK.finditer(text, offset, offset + len(line)):
                if not any(a <= match.start() - offset < b for a, b in code):
                    yield match
        offset += len(line)


def _read_members(source):
    # ZipFile akzeptiert Path und Seek-Dateien; keine Dateien außerhalb
    # dieses Handles werden von Markdown-Verweisen geöffnet.
    source_size = None
    if hasattr(source, "seek"):
        position = source.tell()
        source.seek(0, 2); source_size = source.tell(); source.seek(position)
    else:
        from pathlib import Path
        source_size = Path(source).stat().st_size
    if source_size > MAX_ARCHIVE_BYTES:
        raise NotionFormatError("Das Notion-Archiv darf höchstens 200 MiB groß sein.")
    try:
        with zipfile.ZipFile(source) as archive:
            infos = archive.infolist()
            if not 1 <= len(infos) <= MAX_MEMBERS:
                raise NotionFormatError("Das Archiv enthält keine oder mehr als 5.000 Einträge.")
            members = {}
            paths, folded = set(), set()
            total = 0
            inspected = []
            for info in infos:
                # ZipInfo normalisiert Backslashes unter Windows und kürzt
                # Nullbytes. Den ungekürzten Archivnamen vor jeder Nutzung prüfen.
                name = safe_member(info.orig_filename)
                if name in paths or name.casefold() in folded:
                    raise NotionFormatError("Das Archiv enthält doppelte oder mehrdeutige Dateipfade.")
                paths.add(name); folded.add(name.casefold())
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode))):
                    raise NotionFormatError("Verknüpfungen und Sonderdateien sind im Import nicht erlaubt.")
                if info.flag_bits & 1:
                    raise NotionFormatError("Verschlüsselte Archive werden nicht unterstützt.")
                if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    raise NotionFormatError("Das Kompressionsverfahren wird nicht unterstützt; ZIP ohne Kompression oder mit Deflate verwenden.")
                if info.is_dir():
                    continue
                limit = MAX_MARKDOWN_BYTES if name.lower().endswith(".md") else MAX_MEMBER_BYTES
                if info.file_size > limit or info.file_size < 0:
                    raise NotionFormatError("Ein Archivbestandteil überschreitet die erlaubte Größe: " + name)
                total += info.file_size
                if total > MAX_EXPANDED_BYTES:
                    raise NotionFormatError("Die entpackten Inhalte dürfen höchstens 256 MiB belegen.")
                inspected.append((info, name, limit))
            for info, name, limit in inspected:
                with archive.open(info) as stream:
                    data = stream.read(limit + 1)
                if len(data) > limit or len(data) != info.file_size:
                    raise NotionFormatError("Die Größe eines Archivbestandteils ist ungültig: " + name)
                members[name] = data
            return members
    except (zipfile.BadZipFile, NotImplementedError, RuntimeError, OSError, EOFError, zlib.error) as exc:
        raise NotionFormatError("Das Notion-Archiv konnte nicht gelesen werden: " + str(exc)) from exc


def inspect_export(source):
    members = _read_members(source)
    losses, pages, identities = [], [], set()
    prefixes = {name.split("/", 1)[0] for name in members}
    wrapper = next(iter(prefixes)) if len(prefixes) == 1 else None
    wrapper = wrapper if wrapper and wrapper.casefold().startswith("export-") and any("/" in n for n in members) else None
    for path, raw in sorted(members.items()):
        suffix = PurePosixPath(path).suffix.lower()
        if suffix == ".csv":
            losses.append(Loss(path, "csv-database", "CSV-Datenbank bleibt im Originalarchiv; Datenbankansichten und Eigenschaften werden nicht nachgebaut."))
        elif suffix == ".html":
            losses.append(Loss(path, "html-file", "HTML-Datei bleibt im Originalarchiv und wird nicht als Seite übernommen."))
        if suffix != ".md":
            continue
        try:
            text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        except UnicodeError as exc:
            raise NotionFormatError("Markdown enthält ungültiges UTF-8: " + path) from exc
        if "\x00" in text:
            raise NotionFormatError("Markdown enthält ein Nullzeichen: " + path)
        semantic_path = path[len(wrapper) + 1:] if wrapper else path
        key = source_key(semantic_path)
        if key in identities:
            raise NotionFormatError("Eine Notion-Quellenkennung kommt mehrfach vor: " + path)
        identities.add(key)
        if key.startswith("path:"):
            losses.append(Loss(path, "path-identity", "Keine Notion-Kennung im Dateinamen; die Wiedererkennung nutzt den Archivpfad. Umbenennungen müssen gegebenenfalls zugeordnet werden."))
        if re.search(r"<(?:aside|table|div|details|iframe|script)\b", text, re.I):
            losses.append(Loss(path, "html-block", "HTML-/Hinweisblöcke bleiben als Quelltext lesbar; ihre Gestaltung und eingebettete Funktionen werden nicht übernommen."))
        if re.search(r"^#{5,6}\s", text, re.M):
            losses.append(Loss(path, "heading-depth", "Überschriften der Stufen 5/6 werden als Stufe 4 übernommen."))
        assets = set()
        for match in _links(text):
            target = match.group(3)
            found = local_target(path, target, members)
            try:
                parsed = urlsplit(target)
            except ValueError:
                parsed = None
            if found and not found.lower().endswith(".md"):
                assets.add(found)
                if not match.group(1):
                    losses.append(Loss(path, "attachment-link", "Dateiverweis wird als Seitenanhang übernommen: " + found))
                if match.group(1) and PurePosixPath(found).suffix.lower() not in _IMAGE_SUFFIXES:
                    losses.append(Loss(path, "image-format", "Bildformat bleibt als Datei erhalten: " + found))
                if match.group(1):
                    start = text.rfind("\n", 0, match.start()) + 1
                    end = text.find("\n", match.end())
                    line = text[start:len(text) if end == -1 else end]
                    if line.strip() != match.group(0).strip():
                        losses.append(Loss(path, "inline-image-block", "Ein Bild innerhalb einer Textzeile wird als eigener Bildblock übernommen."))
            elif found is None and (parsed is None or not parsed.scheme or parsed.scheme in ("file", "data")):
                losses.append(Loss(path, "missing-local-target", "Lokales Ziel nicht im Archiv gefunden: " + target))
            if parsed and parsed.fragment:
                losses.append(Loss(path, "link-anchor", "Abschnittsanker wird nicht als eigenes Sprungziel übernommen: " + target))
        title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), plain_title(PurePosixPath(path).name))
        parent = PurePosixPath(path).parent
        parts = parent.parts[1:] if wrapper and parent.parts and parent.parts[0] == wrapper else parent.parts
        folders = []
        prefix = ""
        for part in parts:
            prefix = posixpath.join(prefix, part)
            folders.append((source_key(prefix), plain_title(part)))
        # Referenzierte Dateien gehören zum Quellenzustand. Eine geänderte
        # Bilddatei muss auch bei unverändertem Markdown erkannt werden.
        digest = hashlib.sha256(semantic_path.encode("utf-8") + b"\x00" + raw)
        for asset in sorted(assets):
            asset_key = asset[len(wrapper) + 1:] if wrapper else asset
            digest.update(b"\x00" + asset_key.encode("utf-8") + b"\x00")
            digest.update(hashlib.sha256(members[asset]).digest())
        pages.append(Page(key, path, title[:200] or "Ohne Titel", tuple(folders), text,
                          digest.hexdigest(), tuple(sorted(assets))))
    if not pages:
        raise NotionFormatError("Das Archiv enthält keine Markdown-Seiten.")
    return Export(tuple(pages), members, tuple(dict.fromkeys(losses)))


def unresolved_links(export, page_ids):
    by_path = {value.path: value.key for value in export.pages}
    losses = []
    for page in export.pages:
        if page.key not in page_ids:
            continue
        for match in _links(page.markdown):
            target = local_target(page.path, match.group(3), export.members)
            if target in by_path and by_path[target] not in page_ids:
                losses.append(Loss(page.path, "unselected-page", "Seitenziel ist nicht zur Übernahme ausgewählt und noch nicht in Glide zugeordnet: " + target))
    return tuple(dict.fromkeys(losses))


def page_document(export, page, page_ids, asset_ids):
    """Interne Seitenziele und eingebettete Bilder auf gewählte Glide-IDs abbilden.

    `asset_ids` ordnet einem Archivpfad den gespeicherten Anhang zu. Andere
    Dateien bleiben Anhänge; das Originalarchiv erhält auch ihre Linksyntax.
    Nicht ausgewählte oder fehlende Seitenziele bleiben benannte Textstellen
    und erscheinen bereits in der Vorschau als offener Verweis.
    """
    by_path = {value.path: value.key for value in export.pages}
    def replace(match):
        target = local_target(page.path, match.group(3), export.members)
        identity = page_ids.get(by_path.get(target))
        if identity and not match.group(1):
            return f"[{match.group(2)}]({object_references.uri('list', identity)})"
        if match.group(1) and target in asset_ids and PurePosixPath(target).suffix.lower() in _IMAGE_SUFFIXES:
            return "\n\n" + match.group(0) + "\n\n"
        return match.group(0)
    pieces, previous = [], 0
    for match in _links(page.markdown):
        pieces.extend((page.markdown[previous:match.start()], replace(match)))
        previous = match.end()
    pieces.append(page.markdown[previous:])
    markdown = "".join(pieces)
    image_index = [0]
    def image(description, target):
        path = local_target(page.path, target, export.members)
        attachment = asset_ids.get(path)
        if attachment and PurePosixPath(path).suffix.lower() in _IMAGE_SUFFIXES:
            image_index[0] += 1
            identity = hashlib.sha256((page.key + ":" + str(image_index[0]) + ":" + path).encode("utf-8")).hexdigest()[:16]
            return "img:" + identity, {"attachment": attachment["id"], "mode": "left", "width": 360}
        return None
    return page_markdown.markdown_to_page(markdown, image_resolver=image)


def bind_page_tasks(document, item_factory):
    """Markdown-Kästchen an echte Seitenaufgaben binden, Quelle unverändert lassen.

    Die Kennungen kommen aus dem bestehenden Glide-Aufgabenwerkzeug. Ein
    unvollständiger oder mehrdeutiger Bezug wird vor der Mutation abgewiesen.
    """
    import copy
    if not isinstance(document, dict) or not isinstance(document.get("spans"), list):
        raise NotionFormatError("Das Seitendokument enthält keine gültigen Formatspannen.")
    tasks = document.get("tasks", [])
    if not isinstance(tasks, list):
        raise NotionFormatError("Die Seitenaufgaben sind keine Liste.")
    mapped, items, used_ids = {}, [], set()
    for task in tasks:
        if (not isinstance(task, dict) or set(task) != {"ref", "text", "done"}
                or type(task["ref"]) is not int or task["ref"] < 0
                or not isinstance(task["text"], str) or type(task["done"]) is not bool):
            raise NotionFormatError("Eine Seitenaufgabe enthält ungültige Angaben.")
        tag = "taskref:" + str(task["ref"])
        if tag in mapped:
            raise NotionFormatError("Eine Quellenaufgabe ist mehrfach definiert.")
        item = item_factory(task["text"], done=task["done"])
        identity = item.get("id") if isinstance(item, dict) else None
        if not isinstance(identity, str) or not identity or identity in used_ids:
            raise NotionFormatError("Die Aufgabenwerkzeuge lieferten keine eindeutige Kennung.")
        used_ids.add(identity)
        mapped[tag] = "item:" + identity
        items.append(copy.deepcopy(item))
    result = copy.deepcopy(document)
    result.pop("tasks", None)
    seen = set()
    for span in result["spans"]:
        if not isinstance(span, dict) or not isinstance(span.get("tag"), str):
            raise NotionFormatError("Eine Formatspanne ist ungültig.")
        tag = span["tag"]
        if tag.startswith("taskref:"):
            if tag not in mapped:
                raise NotionFormatError("Ein Kästchen verweist auf eine fehlende Quellenaufgabe.")
            span["tag"] = mapped[tag]
            seen.add(tag)
    if seen != set(mapped):
        raise NotionFormatError("Eine Quellenaufgabe hat keine sichtbare Textstelle.")
    return result, tuple(items)
