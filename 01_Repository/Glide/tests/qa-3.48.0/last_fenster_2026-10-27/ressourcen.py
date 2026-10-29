"""Windows-Prozesszaehler; laeuft nur im Elternprozess, nicht in Glide."""
import ctypes as c
from ctypes import wintypes as w


class Memory(c.Structure):
    _fields_=[('cb',w.DWORD),('PageFaultCount',w.DWORD)]+[(name,c.c_size_t) for name in
        'PeakWorkingSetSize WorkingSetSize QuotaPeakPagedPoolUsage QuotaPagedPoolUsage QuotaPeakNonPagedPoolUsage QuotaNonPagedPoolUsage PagefileUsage PeakPagefileUsage PrivateUsage'.split()]


class SystemMemory(c.Structure):
    _fields_=[('length',w.DWORD),('load',w.DWORD)]+[(name,c.c_ulonglong) for name in
        'total_physical available_physical total_pagefile available_pagefile total_virtual available_virtual extended_virtual'.split()]


kernel=c.WinDLL('kernel32',use_last_error=True)
user=c.WinDLL('user32',use_last_error=True)
psapi=c.WinDLL('psapi',use_last_error=True)
kernel.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD]
kernel.OpenProcess.restype=w.HANDLE
kernel.CloseHandle.argtypes=[w.HANDLE]
kernel.CloseHandle.restype=w.BOOL
kernel.GetProcessHandleCount.argtypes=[w.HANDLE,c.POINTER(w.DWORD)]
kernel.GetProcessHandleCount.restype=w.BOOL
kernel.GlobalMemoryStatusEx.argtypes=[c.POINTER(SystemMemory)]
kernel.GlobalMemoryStatusEx.restype=w.BOOL
psapi.GetProcessMemoryInfo.argtypes=[w.HANDLE,c.POINTER(Memory),w.DWORD]
psapi.GetProcessMemoryInfo.restype=w.BOOL
user.GetGuiResources.argtypes=[w.HANDLE,w.DWORD]
user.GetGuiResources.restype=w.DWORD
user.GetForegroundWindow.argtypes=[]
user.GetForegroundWindow.restype=w.HWND
user.GetWindowThreadProcessId.argtypes=[w.HWND,c.POINTER(w.DWORD)]
user.GetWindowThreadProcessId.restype=w.DWORD


class Monitor:
    def __init__(self,pid):
        self.pid=pid
        self.handle=kernel.OpenProcess(0x1000,False,pid)
        if not self.handle:
            raise c.WinError(c.get_last_error())

    def sample(self):
        memory=Memory(cb=c.sizeof(Memory))
        system=SystemMemory(length=c.sizeof(SystemMemory))
        handles=w.DWORD()
        owner=w.DWORD()
        row={}
        if psapi.GetProcessMemoryInfo(self.handle,c.byref(memory),c.sizeof(memory)):
            row.update(working_set=memory.WorkingSetSize,working_set_peak=memory.PeakWorkingSetSize,
                private_bytes=memory.PrivateUsage)
        if kernel.GlobalMemoryStatusEx(c.byref(system)):
            row.update(available_physical=system.available_physical,memory_load_percent=system.load)
        if kernel.GetProcessHandleCount(self.handle,c.byref(handles)):
            row['handles']=handles.value
        row.update(gdi=user.GetGuiResources(self.handle,0),user=user.GetGuiResources(self.handle,1),
            gdi_peak=user.GetGuiResources(self.handle,2),user_peak=user.GetGuiResources(self.handle,4))
        window=user.GetForegroundWindow()
        if window:
            user.GetWindowThreadProcessId(window,c.byref(owner))
        row['foreground']=owner.value==self.pid
        return row

    def close(self):
        kernel.CloseHandle(self.handle)
