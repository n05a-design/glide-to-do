"""Filesystem- und DLL-eingebettete Tcl/Tk-Skriptpfade im eigenen Paket prüfen."""
from pathlib import Path, PureWindowsPath
import re


def defender_provider(path, programdata):
    """Nur den dokumentierten Defender-AMSI-Anbieter im Systembestand erkennen."""
    if not programdata:
        return None
    root = PureWindowsPath(programdata)
    path = PureWindowsPath(path)
    base = root/'Microsoft/Windows Defender/Platform'
    if not root.is_absolute() or '..' in path.parts or not path.is_relative_to(base):
        return None
    relative = path.relative_to(base)
    if (len(relative.parts) != 2 or relative.name.casefold() != 'mpoav.dll' or
            not re.fullmatch(r'\d+\.\d+\.\d+\.\d+(?:-\d+)?', relative.parts[0])):
        return None
    return relative.as_posix()


def authenticode(path, windows):
    """Native Code-Signatur/Windows-Vertrauenskette ohne Netzwerk oder GUI."""
    import ctypes as C
    import sys
    if sys.platform != 'win32':
        raise RuntimeError('Authenticode braucht den nativen Windows-Prüfstand.')
    system = Path(windows)/'System32'
    trust = C.WinDLL(str(system/'wintrust.dll'), use_last_error=True)
    crypto = C.WinDLL(str(system/'crypt32.dll'), use_last_error=True)
    DWORD = C.c_uint32

    class Guid(C.Structure):
        _fields_ = [('a',DWORD),('b',C.c_uint16),('c',C.c_uint16),('d',C.c_ubyte*8)]

    class FileInfo(C.Structure):
        _fields_ = [('size',DWORD),('path',C.c_wchar_p),('file',C.c_void_p),('subject',C.c_void_p)]

    class TrustData(C.Structure):
        _fields_ = [('size',DWORD),('policy',C.c_void_p),('sip',C.c_void_p),('ui',DWORD),
                    ('revocation',DWORD),('choice',DWORD),('file',C.POINTER(FileInfo)),
                    ('action',DWORD),('state',C.c_void_p),('url',C.c_wchar_p),
                    ('flags',DWORD),('context',DWORD),('settings',C.c_void_p)]

    class FileTime(C.Structure):
        _fields_ = [('low',DWORD),('high',DWORD)]

    class CertificatePrefix(C.Structure):
        _fields_ = [('size',DWORD),('certificate',C.c_void_p)]

    class SignerPrefix(C.Structure):
        _fields_ = [('size',DWORD),('time',FileTime),('count',DWORD),
                    ('certificates',C.POINTER(CertificatePrefix))]

    verify = trust.WinVerifyTrust
    verify.argtypes = [C.c_void_p,C.POINTER(Guid),C.POINTER(TrustData)]
    verify.restype = C.c_int32
    provider_data = trust.WTHelperProvDataFromStateData
    provider_data.argtypes = [C.c_void_p];provider_data.restype = C.c_void_p
    provider_signer = trust.WTHelperGetProvSignerFromChain
    provider_signer.argtypes = [C.c_void_p,DWORD,C.c_int,DWORD]
    provider_signer.restype = C.POINTER(SignerPrefix)
    certificate_name = crypto.CertGetNameStringW
    certificate_name.argtypes = [C.c_void_p,DWORD,DWORD,C.c_void_p,C.c_wchar_p,DWORD]
    certificate_name.restype = DWORD
    if C.sizeof(C.c_void_p) != 8 or C.sizeof(TrustData) != 88 or C.sizeof(FileInfo) != 32:
        raise RuntimeError('Signaturprobe benötigt die geprüfte native Windows-x64-ABI.')
    action = Guid(0x00aac56b,0xcd44,0x11d0,(C.c_ubyte*8)(0x8c,0xc2,0,0xc0,0x4f,0xc2,0x95,0xee))
    file = FileInfo(C.sizeof(FileInfo),str(Path(path).resolve()),None,None)
    data = TrustData()
    data.size = C.sizeof(data)
    data.ui = 2  # WTD_UI_NONE
    data.choice = 1  # WTD_CHOICE_FILE
    data.file = C.pointer(file)
    data.action = 1  # WTD_STATEACTION_VERIFY
    data.flags = 0x1000 | 0x2000  # Nur lokaler URL-Cache, MD2/MD4 verbieten.
    try:
        status = verify(C.c_void_p(-1),C.byref(action),C.byref(data))
        if status != 0:
            return {'Status':f'WinVerifyTrust 0x{status & 0xffffffff:08x}','Subject':'',
                    'verfahren':'lokale Windows-Vertrauenskette, kein Netzwerk'}
        provider = provider_data(data.state)
        signer = provider_signer(provider,0,False,0) if provider else None
        if not signer or signer.contents.size < C.sizeof(SignerPrefix) or signer.contents.count < 1:
            raise RuntimeError('Windows bestätigt keinen auslesbaren Signierer.')
        first = signer.contents.certificates[0]
        if first.size < C.sizeof(CertificatePrefix) or not first.certificate:
            raise RuntimeError('Windows-Signiererzertifikat fehlt.')
        name_format = DWORD(3)  # CERT_X500_NAME_STR
        length = certificate_name(first.certificate,2,0,C.byref(name_format),None,0)
        if length <= 1:
            raise RuntimeError('Windows-Signierername fehlt.')
        subject = C.create_unicode_buffer(length)
        if certificate_name(first.certificate,2,0,C.byref(name_format),subject,length) != length:
            raise RuntimeError('Windows-Signierername nicht vollständig gelesen.')
        return {'Status':'Valid','Subject':subject.value,
                'verfahren':'WinVerifyTrust, lokale Windows-Vertrauenskette, kein Netzwerk'}
    finally:
        data.action = 2  # Jede Verifikation gibt ihren nativen Kontext frei.
        verify(C.c_void_p(-1),C.byref(action),C.byref(data))

def validate_loaded(package, windows, libraries, *, programdata=None, authenticate=None):
    """Tatsächlich geladene Windows-Bibliotheken zusätzlich zum Baugraph prüfen."""
    package, windows = PureWindowsPath(package), PureWindowsPath(windows)
    if not package.is_absolute() or not windows.is_absolute():
        raise ValueError('Paket und Windows-Systemordner brauchen absolute Pfade.')
    system_roots = tuple(windows/name for name in ('System32', 'SysWOW64', 'WinSxS'))
    records, errors = [], []
    for name in libraries:
        path = PureWindowsPath(name)
        if not path.is_absolute():
            errors.append('Geladener Bibliothekspfad ist nicht absolut.')
        elif path.is_relative_to(package):
            records.append({'bereich': 'paket', 'datei': path.relative_to(package).as_posix()})
        elif any(path.is_relative_to(root) for root in system_roots):
            records.append({'bereich': 'windows', 'datei': path.relative_to(windows).as_posix()})
        elif defender_provider(path, programdata) is not None and authenticate is not None:
            signature = authenticate(str(path))
            if (signature.get('Status') == 'Valid' and
                    re.search(r'(?:^|,\s*)O=Microsoft Corporation(?:,|$)', signature.get('Subject', ''))):
                records.append({'bereich': 'windows-defender', 'datei': defender_provider(path, programdata),
                                'signatur': 'Valid', 'herausgeber': 'Microsoft Corporation'})
            else:
                errors.append('Windows-Defender-Anbieter ohne gültige Microsoft-Signatur: '+path.name)
        else:
            errors.append('Geladene Bibliothek liegt außerhalb des Pakets und Windows-Systemordners: '+path.name)
    return {'bibliotheken': records, 'fehler': errors, 'exitcode': int(bool(errors))}


def script_library(value, kind, package, *, provider=None):
    if kind not in ('tcl', 'tk'):
        raise ValueError('Unbekannte Skriptbibliothek.')
    package = Path(package).resolve()
    value = str(value)
    if value.startswith('//zipfs:/'):
        if value != f'//zipfs:/lib/{kind}/{kind}_library':
            raise ValueError('Unbekannter eingebetteter Tcl/Tk-Skriptpfad.')
        if provider is None:
            raise ValueError('Eingebettete Skripte brauchen einen nachgewiesenen geladenen Paketanbieter.')
        provider = Path(provider).resolve()
        if not provider.is_file() or not provider.is_relative_to(package):
            raise ValueError('Anbieter der eingebetteten Skripte liegt außerhalb des Pakets.')
        return {'modus': 'eingebettetes-zip', 'ort': value,
                'anbieter': provider.relative_to(package).as_posix()}
    library = Path(value).resolve()
    if not library.is_dir() or not library.is_relative_to(package):
        raise ValueError('Tcl/Tk-Skriptbibliothek liegt außerhalb des Pakets oder fehlt.')
    return {'modus': 'dateien', 'ort': library.relative_to(package).as_posix()}


_TK = re.compile(r"(?:lib)?(?:tcl9)?tk9[0-9]*(?:\.[0-9]+)*\.(?:dylib|dll|so)")
_TCL = re.compile(r"(?:lib)?tcl9[0-9]*(?:\.[0-9]+)*\.(?:dylib|dll|so)")


def tk_providers(libraries):
    """Geladene Tcl/Tk-Bibliotheken erkennen.

    Exakte Namensmuster: macOS-Frameworks `Tcl`/`Tk`, Windows `tcl90.dll`/
    `tcl9tk90.dll`, Linux/macOS `libtcl9.0.dylib`/`libtcl9tk9.0.dylib`.
    Erweiterungen wie `libtcl9tkdnd2.10.2.dylib` sind keine Anbieter.
    """
    found = {'tcl': [], 'tk': []}
    for value in libraries:
        name = Path(value).name.casefold()
        if name == 'tk' or _TK.fullmatch(name):
            found['tk'].append(value)
        elif name == 'tcl' or _TCL.fullmatch(name):
            found['tcl'].append(value)
    if any(len(values) > 1 for values in found.values()):
        raise ValueError('Mehrere Tcl-/Tk-Anbieter sind gleichzeitig geladen.')
    return {kind: values[0] for kind, values in found.items() if values}
