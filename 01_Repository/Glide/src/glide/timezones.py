"""Lokale Zeitzonen und mitgelieferte IANA-Daten ohne Zusatzbibliothek.

ZoneInfo.from_file liest unveränderte TZif-Daten; CLDR ordnet Windows-Namen
zu. Keine Netzwerkzugriffe und keine Änderung an Pythons globalem TZPATH.
"""
from datetime import datetime
from functools import lru_cache
from io import BytesIO
import os
from pathlib import Path, PurePosixPath
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

RESOURCES = Path(__file__).resolve().parent / "resources" / "timezones"


def valid_key(key):
    if not isinstance(key, str) or not key or len(key) > 200:
        return False
    path = PurePosixPath(key)
    return (not path.is_absolute() and path.as_posix() == key
            and all(part not in (".", "..") for part in key.split("/"))
            and "\\" not in key and ":" not in key
            and not any(ord(c) < 33 or ord(c) == 127 for c in key))


class Resolver:
    def __init__(self, resources=RESOURCES, system=ZoneInfo):
        self.resources = Path(resources)
        self.system = system

    @lru_cache(maxsize=64)
    def __call__(self, key):
        if not valid_key(key):
            raise ValueError("Ungültige Zeitzonenkennung.")
        try:
            with ZipFile(self.resources / "iana-2026e.zip") as archive:
                try:
                    content = archive.read(key)
                except KeyError:
                    content = None
            if content is not None:
                return ZoneInfo.from_file(BytesIO(content), key=key)
        except FileNotFoundError:
            pass
        try:
            return self.system(key)
        except ZoneInfoNotFoundError:
            raise ZoneInfoNotFoundError("Zeitzone nicht verfügbar: " + key) from None

    @lru_cache(maxsize=256)
    def windows_key(self, name, territory="001"):
        root = ET.parse(self.resources / "windowsZones.xml").getroot()
        mappings = [entry for entry in root.iter("mapZone") if entry.get("other") == name]
        preferred = next((entry for entry in mappings if entry.get("territory") == territory), None)
        fallback = next((entry for entry in mappings if entry.get("territory") == "001"), None)
        found = preferred if preferred is not None else fallback
        if found is None:
            raise ZoneInfoNotFoundError("Windows-Zeitzone nicht zugeordnet: " + str(name))
        return found.attrib["type"].split()[0]


def windows_configuration():
    import winreg
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                       r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation") as key:
        name = winreg.QueryValueEx(key, "TimeZoneKeyName")[0].rstrip("\x00")
        try:
            disabled = bool(winreg.QueryValueEx(key, "DynamicDaylightTimeDisabled")[0])
        except FileNotFoundError:
            disabled = False
    return name, disabled


def local_zone(resolver=None, *, environment=None, platform=None,
               localtime="/etc/localtime", timezone_file="/etc/timezone",
               windows_reader=windows_configuration, fixed_local=None):
    resolver = resolver or Resolver()
    environment = os.environ if environment is None else environment
    platform = sys.platform if platform is None else platform
    chosen = environment.get("TZ", "").removeprefix(":")
    if chosen:
        if Path(chosen).is_absolute():
            with Path(chosen).open("rb") as source:
                return ZoneInfo.from_file(source, key="lokale Zeitzone")
        return resolver(chosen)
    if platform == "win32":
        name, disabled = windows_reader()
        if disabled:
            # Windows hat Sommerzeit ausdrücklich abgeschaltet; kein IANA-DST.
            zone = fixed_local if fixed_local is not None else datetime.now().astimezone().tzinfo
            if zone is None:
                raise ValueError("Lokale Windows-Zeitzone nicht verfügbar.")
            return zone
        return resolver(resolver.windows_key(name))
    try:
        with Path(localtime).open("rb") as source:
            return ZoneInfo.from_file(source, key="lokale Zeitzone")
    except FileNotFoundError:
        pass
    try:
        chosen = Path(timezone_file).read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        chosen = ""
    if chosen:
        return resolver(chosen)
    raise ZoneInfoNotFoundError("Lokale Zeitzone nicht bestimmbar; bitte eine Zeitzone wählen.")
