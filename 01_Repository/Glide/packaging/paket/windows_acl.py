"""Original-DACLs ohne erneute Windows-Vererbungspropagation restaurieren.

Nur der bereits auf Hosted-CI begrenzte Startprüfer verwendet diese Schnittstelle.
SetFileSecurityW ist hier gezielt erforderlich: SetNamedSecurityInfo/icacls
normalisieren das Vererbungsmodell und schreiben dadurch Original-DACLs um.
"""
import ctypes
from ctypes import wintypes
from pathlib import PureWindowsPath
import sys

from windows_isolation import plan, restoration_entries


class OriginalAclRestorer:
    def __init__(self, environment, package, report, sources):
        if sys.platform != 'win32':
            raise RuntimeError('Original-DACLs brauchen den nativen Windows-Prüfstand.')
        boundary = plan(environment, str(package), str(report), [str(path) for path in sources])
        self.sources = {PureWindowsPath(path) for path in boundary['forbidden']}
        self.api = ctypes.WinDLL('advapi32', use_last_error=True)
        self.convert = self.api.ConvertStringSecurityDescriptorToSecurityDescriptorW
        self.convert.argtypes = [wintypes.LPCWSTR, wintypes.DWORD,
                                 ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.DWORD)]
        self.convert.restype = wintypes.BOOL
        self.apply = self.api.SetFileSecurityW
        self.apply.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p]
        self.apply.restype = wintypes.BOOL
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.free = self.kernel.LocalFree
        self.free.argtypes = [ctypes.c_void_p]
        self.free.restype = ctypes.c_void_p

    def restore(self, source, snapshot):
        if PureWindowsPath(str(source)) not in self.sources:
            raise ValueError('Nur die ausdrücklich gesicherten Hosted-CI-Quellen restaurieren.')
        entries = restoration_entries(str(source), snapshot)
        errors = []
        for path, dacl in entries:
            descriptor = ctypes.c_void_p()
            try:
                if not self.convert(dacl, 1, ctypes.byref(descriptor), None):
                    raise ctypes.WinError(ctypes.get_last_error())
                # Nur DACL_SECURITY_INFORMATION; Eigentümer/SACL bleiben erhalten.
                # Diese API propagiert die Ordner-ACL ausdrücklich nicht weiter.
                if not self.apply(path, 0x4, descriptor):
                    raise ctypes.WinError(ctypes.get_last_error())
            except OSError as error:
                errors.append({'datei': path, 'winerror': error.winerror})
            finally:
                if descriptor.value:
                    self.free(descriptor)
        return {'dateien': len(entries), 'fehler': errors, 'exitcode': int(bool(errors))}
