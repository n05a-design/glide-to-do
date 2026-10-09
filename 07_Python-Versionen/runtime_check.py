"""Mindestlaufzeit prüfen, bevor Glide geladen wird (AB08 seit 3.33.20).

Bewusst in einfacher Syntax ohne neuere Sprachmittel: Die Datei muss auch ein
zu altes Python lesen können, um es verständlich abzuweisen. Geprüft wird vor
jedem Zugriff auf Nutzerdaten. Python 3.12/3.13 und Tk 8.6 starten weiter,
sind aber eingeschränkt (Architektur, Abschnitt 1); Referenz ist Python 3.14
mit Tk 9.
"""
import sys

MIN_PYTHON = (3, 12)
REFERENZ_PYTHON = (3, 14)
MIN_TK = 8.6
REFERENZ_TK = 9.0


def python_status(version=None):
    """("ok" | "eingeschränkt" | "zu_alt", Meldung) für die Python-Version."""
    version = tuple(version or sys.version_info[:3])
    text = ".".join(str(teil) for teil in version[:3])
    if version[:2] < MIN_PYTHON:
        return ("zu_alt", "Glide braucht Python 3.12 oder neuer (empfohlen: Python 3.14 von python.org). "
                          "Gefunden: Python " + text + ". Deine Daten wurden nicht geöffnet.")
    if version[:2] < REFERENZ_PYTHON:
        return ("eingeschränkt", "Python " + text + " startet Glide mit Einschränkungen; empfohlen ist Python 3.14.")
    return ("ok", "")


def tk_status(tk_version):
    """("ok" | "eingeschränkt" | "zu_alt", Meldung) für die Tk-Version (Zahl wie 8.6 oder 9.0)."""
    try:
        wert = float(tk_version)
    except (TypeError, ValueError):
        return ("zu_alt", "Die Tk-Version ließ sich nicht bestimmen. Glide braucht Tk 8.6 oder neuer.")
    if wert < MIN_TK:
        return ("zu_alt", "Glide braucht Tk 8.6 oder neuer (empfohlen: Tk 9 mit Python 3.14 von python.org). "
                          "Gefunden: Tk " + str(tk_version) + ". Deine Daten wurden nicht geöffnet.")
    if wert < REFERENZ_TK:
        return ("eingeschränkt", "Tk " + str(tk_version) + " startet Glide mit Einschränkungen "
                                 "(Vorschauen, Systemmitteilungen, Logo); empfohlen ist Tk 9.")
    return ("ok", "")


def melden(text):
    """Meldung zeigen: als Fenster, wenn Tk geht, sonst auf der Konsole."""
    try:
        import tkinter
        from tkinter import messagebox
        fenster = tkinter.Tk()
        fenster.withdraw()
        messagebox.showerror("Glide kann nicht starten", text, parent=fenster)
        fenster.destroy()
    except Exception:
        sys.stderr.write(text + "\n")


def pruefen_oder_beenden():
    """Beendet den Prozess mit einer Meldung, wenn Python zu alt ist."""
    stufe, text = python_status()
    if stufe == "zu_alt":
        melden(text)
        raise SystemExit(1)
    return stufe
