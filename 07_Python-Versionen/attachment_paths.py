"""Portable flache Anhangspfade, ohne Tk und ohne Dateizugriff.

Seit D67 (menschliche Abnahme 07.11.2026) gilt für Anhangsnamen dieselbe Grenze
wie für Titel: höchstens 40 Zeichen einschließlich Endung. Der Speichername
(32 Zeichen Kennung, Unterstrich, Name) bleibt damit höchstens 73 Zeichen lang;
zu lange Pfade ließen sich unter Windows/OneDrive nicht mehr öffnen und ändern.
"""
import os
import unicodedata

NAME_MAX_CHARS = 40
ID_PREFIX_CHARS = 32
STORED_NAME_MAX_CHARS = ID_PREFIX_CHARS + 1 + NAME_MAX_CHARS
EXTENSION_MAX_CHARS = 12
FORBIDDEN_CHARS = '<>:"/\\|?*'


def validate_storage(storage):
    if not isinstance(storage, str):
        raise ValueError("Ungültiger Anhangspfad.")
    storage = storage.strip()
    if not storage or "\\" in storage or "\x00" in storage:
        raise ValueError("Ungültiger Anhangspfad.")
    parts = storage.split("/")
    if len(parts) != 2 or parts[0] != "attachments":
        raise ValueError("Anhänge müssen direkt im Ordner attachments liegen.")
    filename = parts[1]
    if filename in ("", ".", "..") or filename.rstrip(" .") != filename:
        raise ValueError("Ungültiger Anhangsname.")
    if any(ord(char) < 32 or char in '<>:"/\\|?*' for char in filename):
        raise ValueError("Der Anhangsname enthält unzulässige Zeichen.")
    reserved = {"CON", "PRN", "AUX", "NUL"}
    reserved.update({f"COM{number}" for number in range(1, 10)})
    reserved.update({f"LPT{number}" for number in range(1, 10)})
    if filename.split(".", 1)[0].upper() in reserved:
        raise ValueError("Der Anhangsname ist unter Windows reserviert.")
    return storage


def storage_key(storage):
    """Auch auf Windows und üblichen Mac-Dateisystemen kollisionsfrei bleiben."""
    return unicodedata.normalize("NFC", validate_storage(storage)).casefold()


def _clean(name):
    text = " ".join(str(name or "").replace("\\", "/").split("/")[-1].split())
    return "".join("_" if ord(char) < 32 or char in FORBIDDEN_CHARS else char for char in text)


def split_extension(name):
    """Name und Endung; ungewöhnlich lange oder leere Endungen zählen zum Namen."""
    stem, extension = os.path.splitext(str(name or ""))
    if not stem or len(extension) < 2 or len(extension) > EXTENSION_MAX_CHARS or " " in extension:
        return str(name or ""), ""
    return stem, extension


def too_long(name, limit=NAME_MAX_CHARS):
    """Nur die Länge: Diese Regel setzt Glide überall durch (D67).

    Zeichenregeln betreffen den Speichernamen, den `safe_attachment_filename`
    ohnehin bereinigt; sie gelten zusätzlich für selbst eingetippte Namen.
    """
    return len(" ".join(str(name or "").split())) > limit


def name_problem(name, limit=NAME_MAX_CHARS):
    """Klare Meldung, warum ein Anhangsname nicht zulässig ist – sonst None."""
    text = " ".join(str(name or "").split())
    if not text:
        return "Bitte einen Dateinamen eingeben."
    if len(text) > limit:
        return f"Der Anhangsname hat {len(text)} Zeichen; erlaubt sind höchstens {limit}."
    if any(ord(char) < 32 or char in FORBIDDEN_CHARS for char in text):
        return "Der Anhangsname enthält unzulässige Zeichen (< > : \" / \\ | ? *)."
    if text.rstrip(" .") != text:
        return "Der Anhangsname darf nicht auf Punkt oder Leerzeichen enden."
    return None


def shortened_name(name, limit=NAME_MAX_CHARS):
    """Zulässiger Vorschlag: Endung bleibt, der Name davor wird gekürzt."""
    text = _clean(name).rstrip(" .")
    if text and name_problem(text, limit) is None:
        return text
    stem, extension = split_extension(text)
    if len(extension) >= limit:
        extension = ""
    stem = stem[:max(1, limit - len(extension))].rstrip(" ._-") or "Anhang"[:max(1, limit - len(extension))]
    return (stem + extension)[:limit].rstrip(" .") or "Anhang"


def keep_extension(name, original):
    """Fehlt im neuen Namen die ursprüngliche Endung, wird sie angehängt."""
    text = " ".join(str(name or "").split())
    _stem, extension = split_extension(_clean(original))
    if extension and not text.lower().endswith(extension.lower()):
        text = text.rstrip(" .") + extension
    return text


def stored_name_too_long(storage):
    """Ob der Speichername eines vorhandenen Anhangs die Grenze überschreitet."""
    return len(str(storage or "").rsplit("/", 1)[-1]) > STORED_NAME_MAX_CHARS


def group_long_storages(attachments):
    """Anhänge mit zu langem Speichernamen, gruppiert nach Speichername (gemeinsame Dateien einmal)."""
    gruppen = {}
    for anhang in attachments or ():
        if isinstance(anhang, dict) and stored_name_too_long(anhang.get("storage")):
            gruppen.setdefault(anhang["storage"], []).append(anhang)
    return gruppen


def restore_names(attachments, records):
    """Gekürzte Anzeigenamen über die Anhangskennung zurücksetzen; liefert die Anzahl.

    `records` sind (Kennung, Original, Kurzname). Zugeordnet wird über die
    Kennung, nicht über den Kurznamen – zwei Anhänge können denselben Kurznamen
    tragen (Prüfbefund H1 vom 07.11.2026).
    """
    offen = {kennung: (original, kurz) for kennung, original, kurz in records or () if kennung}
    zurueck = 0
    for anhang in attachments or ():
        eintrag = offen.get(anhang.get("id")) if isinstance(anhang, dict) else None
        if eintrag and anhang.get("name") == eintrag[1]:
            anhang["name"] = eintrag[0]
            zurueck += 1
    return zurueck
