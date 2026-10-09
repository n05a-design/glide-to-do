"""Unveränderte Vorversion für Altleser-Proben finden – mit Blick auf die Aufbewahrung.

Mehrere Suiten prüfen einen Formattor mit der unveränderten Vorversion aus
`07_Python-Versionen` (oder deren `Archiv`). Die Aufbewahrung hält dort nur die
sieben neuesten Hauptdateien (`scripts/pflege/ablage_kuerzen.py`). Fällt eine
Vorversion planmäßig heraus, entfällt die Probe ausdrücklich; sie war mit der
Version belegt, die den Formattor einführte. Fehlt eine Vorversion, die noch
vorgehalten werden müsste, bleibt das ein Fehler.
"""
from pathlib import Path
import re

AUFBEWAHRUNG = 7


def versionen(changelog):
    """Versionen aus den Überschriften des Änderungsverlaufs, neueste zuerst."""
    text = Path(changelog).read_text(encoding="utf-8")
    return re.findall(r"^## (\d+\.\d+\.\d+)\b", text, flags=re.M)


def vorgehalten(version, changelog):
    """Gehört `version` zu den sieben neuesten Versionen?"""
    liste = versionen(changelog)
    return version in liste[:AUFBEWAHRUNG]


def finden(ablage, version, changelog, ausdruecklich=None):
    """Pfad der Vorversion oder None, wenn sie außerhalb der Aufbewahrung liegt.

    `ausdruecklich` ist ein über die Befehlszeile gesetzter Pfad; er muss
    existieren. Sonst wird zuerst `07_Python-Versionen`, dann `Archiv` gesucht.
    """
    if ausdruecklich is not None:
        pfad = Path(ausdruecklich)
        assert pfad.exists(), pfad
        return pfad
    name = f"Glide-Aufgaben-und-Listen_v{version}.pyw"
    ordner = Path(ablage) / "07_Python-Versionen"
    for pfad in (ordner / name, ordner / "Archiv" / name):
        if pfad.exists():
            return pfad
    if vorgehalten(version, changelog):
        raise AssertionError(f"Vorversion {version} fehlt in 07_Python-Versionen, obwohl sie vorgehalten wird")
    return None


def hinweis(version):
    return (f"Altleser-Probe mit {version} entfällt: Die Hauptdatei liegt nach der Aufbewahrungsregel "
            f"(sieben neueste Versionen) nicht mehr in 07_Python-Versionen; belegt mit der Version, "
            f"die den Formattor einführte")
