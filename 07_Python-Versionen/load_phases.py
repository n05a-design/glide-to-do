"""Ladeweg in zwei Phasen ohne Tk (WA-28, Befund A34).

Bis 18.10.2026 lagen in `ListApp.load_items` Lesen, Normalisieren und der
Aufbau der Ansicht im selben `try`. Ein reiner Darstellungsfehler nach einer
einwandfrei gelesenen Datei landete deshalb in `handle_unreadable_save_file`:
„Speicherdatei beschädigt“, eine Kopie `liste_unlesbar_*` und ein leerer,
schreibfähiger Bestand, den das nächste Speichern über die Datei schreiben
konnte.

Jetzt gilt:

1. **Lesen:** Datei öffnen, JSON lesen, normalisieren. Nur Fehler dieser
   Phase bedeuten eine unlesbare, beschädigte oder neuere Datei.
2. **Übernehmen und darstellen:** Ein Fehler hier ist ein Darstellungsfehler.
   Der gelesene Bestand bleibt erhalten, die Meldung nennt die richtige
   Ursache, und der Leerstartpfad wird nicht erreicht.

Die App bleibt Adapter (D17); dieses Modul ordnet Fehler ein, wählt die
aktive Liste und formuliert die Meldungen.
"""

# Fehlerarten der Lesephase. `json.JSONDecodeError`, `UnicodeDecodeError` und
# Glides `NewerDataError` sind Unterarten von `ValueError`.
READ_ERRORS = (ValueError, RecursionError, OSError)

# Fehlerarten der Darstellungsphase, die bisher fälschlich als beschädigte
# Datei galten; die App ergänzt `tkinter.TclError`. Andere Ausnahmen gehen
# weiter wie bisher.
DISPLAY_ERRORS = (ValueError, RecursionError, OSError)

DISPLAY_TITLE = "Ansicht nicht vollständig aufgebaut"


def read_failure(exc, newer_type=None):
    """Meldung und Art eines Lesefehlers: (Text, neueres Format?).

    Der Wortlaut entspricht dem bisherigen; nur seine Herkunft ist jetzt auf
    die Lesephase begrenzt.
    """
    if newer_type is not None and isinstance(exc, newer_type):
        return str(exc), True
    if isinstance(exc, OSError):
        return f"Die Speicherdatei konnte nicht gelesen werden:\n{exc}", False
    return f"Die Speicherdatei ist beschädigt oder ungültig:\n{exc}", False


def display_failure(exc):
    """Titel und Text, wenn die Ansicht nach erfolgreichem Lesen scheitert."""
    return (DISPLAY_TITLE,
            "Die Speicherdatei ist lesbar und vollständig geladen; der Bestand bleibt erhalten.\n\n"
            f"Beim Aufbau der Ansicht trat ein Fehler auf:\n{exc}\n\n"
            "Der Fehlerbericht steht im Fehlerprotokoll (Hilfe › Fehlerprotokoll öffnen). "
            "Tritt der Fehler erneut auf, Glide neu starten.")


def choose_active_list(list_ids, inbox_ids, current=None, from_file=None):
    """Aktive Liste nach dem Laden: die gemerkte, sonst die aus der Datei.

    Fehlen beide im Bestand, gilt die erste Liste außer dem Eingang, sonst die
    erste überhaupt. Leere Bestände gibt es hier nicht; `load_items` legt
    vorher eine Liste an.
    """
    ids = list(list_ids)
    preferred = current or from_file
    if preferred in ids:
        return preferred
    if from_file in ids:
        return from_file
    inbox = set(inbox_ids)
    return next((identity for identity in ids if identity not in inbox), ids[0] if ids else None)
