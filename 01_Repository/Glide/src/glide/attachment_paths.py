"""Portable flache Anhangspfade, ohne Tk und ohne Dateizugriff."""
import unicodedata


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
