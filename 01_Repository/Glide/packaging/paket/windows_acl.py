"""Original-DACLs ohne erneute Windows-Vererbungspropagation restaurieren.

Nur der bereits auf Hosted-CI begrenzte Startprüfer verwendet diese Schnittstelle.
Unvererbte Original-ACEs brauchen SetFileSecurityW ohne Propagation.
Bereits geschützte Originale brauchen SetNamedSecurityInfoW für ihren P-Schutz;
die vollständige Restaurierung läuft deshalb Eltern vor Kindern.
"""
import ctypes
from ctypes import wintypes
from pathlib import Path, PureWindowsPath
import sys

from windows_isolation import plan, restoration_entries, restoration_security_information


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
        self.get_dacl = self.api.GetSecurityDescriptorDacl
        self.get_dacl.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.BOOL),
                                  ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.BOOL)]
        self.get_dacl.restype = wintypes.BOOL
        self.apply_protected = self.api.SetNamedSecurityInfoW
        self.apply_protected.argtypes = [wintypes.LPWSTR, ctypes.c_int, wintypes.DWORD,
                                         ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        self.apply_protected.restype = wintypes.DWORD
        self.apply_handle = self.api.SetSecurityInfo
        self.apply_handle.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.DWORD,
                                      ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        self.apply_handle.restype = wintypes.DWORD
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.free = self.kernel.LocalFree
        self.free.argtypes = [ctypes.c_void_p]
        self.free.restype = ctypes.c_void_p
        self.open = self.kernel.CreateFileW
        self.open.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                             wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        self.open.restype = wintypes.HANDLE
        self.close = self.kernel.CloseHandle
        self.close.argtypes = [wintypes.HANDLE]
        self.close.restype = wintypes.BOOL

    def restore(self, source, snapshot):
        if PureWindowsPath(str(source)) not in self.sources:
            raise ValueError('Nur die ausdrücklich gesicherten Hosted-CI-Quellen restaurieren.')
        entries = restoration_entries(str(source), snapshot)
        errors, reparse_points = [], []
        for path, dacl in entries:
            descriptor = ctypes.c_void_p()
            try:
                if not self.convert(dacl, 1, ctypes.byref(descriptor), None):
                    raise ctypes.WinError(ctypes.get_last_error())
                information = restoration_security_information(dacl)
                reparse = bool(Path(path).lstat().st_file_attributes & 0x400)
                if reparse or information & 0x80000000:
                    # SetFileSecurityW ignoriert den gesicherten P-Schutz auf
                    # dem nativen Prüfstand. Nur diese Originale explizit setzen.
                    present, defaulted, original_dacl = wintypes.BOOL(), wintypes.BOOL(), ctypes.c_void_p()
                    if not self.get_dacl(descriptor, ctypes.byref(present), ctypes.byref(original_dacl), ctypes.byref(defaulted)):
                        raise ctypes.WinError(ctypes.get_last_error())
                    if not present.value or not original_dacl.value:
                        raise ValueError('Gesicherte geschützte DACL fehlt; keine NULL-DACL setzen.')
                    if reparse:
                        # CPythons Misc/mypy-Dateien sind originale Symlinks.
                        # Deren gesicherte DACL gehört zum Link, nicht zum Ziel.
                        handle = self.open(path, 0x40000, 7, None, 3, 0x00200000 | 0x02000000, None)
                        if handle in (None, ctypes.c_void_p(-1).value):
                            raise ctypes.WinError(ctypes.get_last_error())
                        try:
                            code = self.apply_handle(handle, 1, information, None, None, original_dacl, None)
                            reparse_points.append(path)
                        finally:
                            if not self.close(handle):
                                raise ctypes.WinError(ctypes.get_last_error())
                    else:
                        code = self.apply_protected(path, 1, information, None, None, original_dacl, None)
                    if code:
                        raise ctypes.WinError(code)
                elif not self.apply(path, 0x4, descriptor):
                    raise ctypes.WinError(ctypes.get_last_error())
            except (OSError, ValueError) as error:
                errors.append({'datei': path, 'winerror': getattr(error, 'winerror', None), 'fehler': str(error)})
            finally:
                if descriptor.value:
                    self.free(descriptor)
        return {'dateien': len(entries), 'reparsepunkte': reparse_points, 'fehler': errors, 'exitcode': int(bool(errors))}
