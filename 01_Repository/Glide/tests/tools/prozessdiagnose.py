"""Lesende Prüfplatzdiagnose; ein Verdacht ändert niemals das Prüfergebnis."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import signal
import subprocess
import sys


def systemkontext():
    """Ohne Adminrechte, Rechnernamen, Benutzerpfade oder Appimport erfassen."""
    result = {
        "runner_python": sys.version,
        "implementierung": platform.python_implementation(),
        "plattform": sys.platform,
        "systemversion": platform.version(),
        "architektur": platform.machine(),
        "cpu": platform.processor() or "nicht ermittelt",
        "logische_prozessoren": os.cpu_count(),
    }
    if sys.platform == "win32":
        import winreg

        for key_path, fields in (
            (r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
             {"ProcessorNameString": "cpu", "VendorIdentifier": "cpu_hersteller"}),
            (r"HARDWARE\DESCRIPTION\System\BIOS",
             {"BaseBoardManufacturer": "board_hersteller", "BaseBoardProduct": "board",
              "BIOSVersion": "bios", "BIOSReleaseDate": "bios_datum"}),
        ):
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                    for field, target in fields.items():
                        try:
                            value, _ = winreg.QueryValueEx(key, field)
                            result[target] = "; ".join(value) if isinstance(value, list) else str(value).strip()
                        except OSError:
                            result[target] = "nicht ermittelt"
            except OSError:
                for target in fields.values():
                    result.setdefault(target, "nicht ermittelt")
    elif sys.platform == 'darwin':
        # Nur zwei feste, nicht personenbezogene Schlüssel. Auch ein fehlender
        # sysctl/Rosetta-Schlüssel darf weder hängen noch den Prüfstart stoppen.
        result['macos_version'] = platform.mac_ver()[0] or None
        result['rosetta'] = None
        for key in ('machdep.cpu.brand_string', 'sysctl.proc_translated'):
            try:
                read = subprocess.run(['/usr/sbin/sysctl', '-n', key], capture_output=True,
                                      text=True, timeout=2, check=False)
                value = read.stdout.strip() if read.returncode == 0 else ''
            except (OSError, subprocess.TimeoutExpired, UnicodeError):
                continue
            if key == 'machdep.cpu.brand_string' and value:
                result['cpu'] = value
            elif key == 'sysctl.proc_translated' and value in ('0', '1'):
                result['rosetta'] = value == '1'
    return result


def pruefplatz(kontext):
    """Vergleichbares Hardwareprofil, keine Rechneridentität oder Fehlerdiagnose."""
    fields = ("cpu", "cpu_hersteller", "board_hersteller", "board", "bios", "bios_datum", "architektur")
    hardware = {key: " ".join(str(kontext.get(key) or "").split()) for key in fields}
    processor = (hardware["cpu"] + " " + hardware["cpu_hersteller"]).casefold()
    families = [name for name in ("intel", "amd") if name in processor]
    if re.search(r'\bapple\s+m[1-9]\d*\b', hardware['cpu'], re.IGNORECASE):
        families.append('apple_silicon')
    family = families[0] if len(families) == 1 else "unbestimmt"
    encoded = json.dumps(hardware, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return {"cpu_familie": family, "hardwareprofil_sha256": hashlib.sha256(encoded.encode("utf-8")).hexdigest(),
            "grenze": "Hardwareprofil ohne Rechner-/Benutzerkennung; keine eindeutig bestimmte physische Maschine."}


def prozessdiagnose(schritt, exitcode, output, *, plattform=None, kontext=None):
    """Fehlersignaturen einordnen, ohne daraus eine CPU-Ursache abzuleiten.

    Exitcode 0 bleibt ohne Absturzverdacht: Die Speicherlastsuite beendet
    absichtlich eigene Schreiber hart; deren Logzeilen sind kein Suiteabsturz.
    Historische Protokolle werden nicht verändert oder neu bewertet.
    """
    if exitcode == 0:
        return None
    plattform = sys.platform if plattform is None else plattform
    kontext = kontext or {}
    signatures = []
    code = exitcode & 0xFFFFFFFF
    native = False
    if plattform == "win32" and code in (0xC0000005, 0xC0000409):
        signatures.append(f"0x{code:08X}")
        native = True
    elif plattform != "win32" and exitcode < 0:
        crash_signals = {int(getattr(signal, name)) for name in
                         ("SIGSEGV", "SIGABRT", "SIGBUS", "SIGILL") if hasattr(signal, name)}
        if -exitcode in crash_signals:
            signatures.append(signal.Signals(-exitcode).name)
            native = True
    fatal = re.search(r"(?m)^(?:Fatal Python error:|Windows fatal exception:).*$", output)
    if fatal:
        signatures.append(fatal.group(0)[:240])
    # Nur tatsächliche Ausnahmezeilen, nicht Quelltext oder zitierte Prüferwartungen.
    data_mismatch = schritt == "test_speicherlast330" and re.search(
        r"(?m)^AssertionError: (?:Runde \d+: geladen ≠ gespeichert|großer Bestand verlustfrei)\s*$",
        output,
    )
    known_type_error = schritt == "test_speicherlast330" and re.search(
        r"(?m)^(?:TypeError: 'dict_valueiterator' object is not callable|"
        r"NameError: name 'isinstance' is not defined)\s*$", output,
    )
    if data_mismatch:
        signatures.append(data_mismatch.group(0).strip())
        category, track = "datenabweichung", "WA-41B"
        hint = ("Gespeicherter und geladener Bestand weichen ab. Eigenständiger Datenintegritätsfehler; "
                "auch bei Hardwareverdacht nicht freigeben oder als Umgebungsfehler ausblenden.")
    elif native or fatal or known_type_error:
        if known_type_error:
            signatures.append(known_type_error.group(0).strip())
        category = "prozessabbruch" if native or fatal else "auffaelliger_python_fehler"
        track = "WA-41A" if schritt == "test_speicherlast330" else "Prozessdiagnose"
        hint = ("Mögliche Ursachen: Software, Python/native Bibliotheken oder instabile "
                "CPU-/Firmware-/RAM-Umgebung. Die Signatur beweist keine Hardwareursache.")
        if track == "WA-41A":
            hint += (" Vergleichsfall WA-41: auf i9-14900K sporadisch rot, zehn ausgewertete "
                     "AMD-Prozesse grün. Das stützt einen Systemunterschied; ein Intel-/CPU-Defekt "
                     "ist damit nicht isoliert bewiesen.")
        cpu = (str(kontext.get("cpu", "")) + " " + str(kontext.get("cpu_hersteller", ""))).lower()
        if "intel" in cpu:
            hint += " Intel-Prüfplatz: vorhandene WHEA-/Dumpbelege und Firmwarestand abgleichen."
    else:
        return None
    return {
        "kategorie": category,
        "spur": track,
        "exitcode": exitcode,
        "signaturen": signatures,
        "ursache_bewiesen": False,
        "hinweis": hint,
        "naechster_schritt": (
            "Rohlog und vorhandene Dumps sichern; WHEA-Ereignisse zeitlich getrennt bewerten. "
            "Bei Bedarf kontrollierte Gegenprobe mit gleichem Quell-/Datenhash und passenden "
            "Python-/Paketversionen. Keine automatische Wiederholung, Affinitäts-, BIOS- oder CPU-Änderung."
        ),
    }
