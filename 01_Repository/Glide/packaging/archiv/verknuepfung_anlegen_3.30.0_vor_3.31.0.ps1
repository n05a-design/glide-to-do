# Legt eine Startmenü-Verknüpfung „Glide“ mit fester AppUserModelID an.
#
# Warum: Windows ordnet Fenster, Taskleistengruppe und Benachrichtigungen
# einer Anwendung über ihre AppUserModelID zu. Glide meldet sich beim Start als
# „Shaye.Glide“ an (APP_USER_MODEL_ID in app.pyw); dieselbe Kennung steht jetzt
# in der Verknüpfung. Das ist die Windows-Hälfte der Voraussetzungen für eigene
# Systembenachrichtigungen (docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md, Stufe B).
#
# Keine Installation, keine Registry, kein Adminrecht: nur eine Datei unter
# %APPDATA%\Microsoft\Windows\Start Menu\Programs. Entfernen = Datei löschen.
#
# Aufruf (PowerShell, im Repository):
#   powershell -ExecutionPolicy Bypass -File packaging\windows\verknuepfung_anlegen.ps1
#   ... -Glide "D:\Glide\07_Python-Versionen\Glide-Aufgaben-und-Listen_v3.30.0.pyw" -Symbol "D:\glide.ico"
#
# Stand 26.09.2026: auf dem Entwicklungs-Mac geschrieben, unter Windows noch
# nicht ausgeführt (Prüfliste „Windows-Prüfung 3.30“).

param(
    [string]$Glide = "",
    [string]$Python = "",
    [string]$Symbol = ""
)

$ErrorActionPreference = "Stop"
$Hier = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Glide) { $Glide = Join-Path $Hier "..\..\src\glide\app.pyw" }
$Glide = (Resolve-Path $Glide).Path

# Kennung aus app.pyw lesen – eine Stelle für die Wahrheit.
$Treffer = Select-String -Path $Glide -Pattern '^APP_USER_MODEL_ID = "([^"]+)"' | Select-Object -First 1
if (-not $Treffer) { throw "APP_USER_MODEL_ID nicht in $Glide gefunden." }
$AppId = $Treffer.Matches[0].Groups[1].Value

if (-not $Python) {
    $Kandidat = $null
    foreach ($Befehl in @("py", "python")) {
        $Pfad = Get-Command $Befehl -ErrorAction SilentlyContinue
        if ($Pfad) {
            $Argumente = if ($Befehl -eq "py") { @("-3", "-c", "import sys; print(sys.executable)") } else { @("-c", "import sys; print(sys.executable)") }
            $Kandidat = (& $Pfad.Source @Argumente).Trim()
            if ($Kandidat) { break }
        }
    }
    if (-not $Kandidat) { throw "Kein Python 3 gefunden. Bitte -Python mit dem Pfad zu pythonw.exe angeben." }
    $Python = Join-Path (Split-Path -Parent $Kandidat) "pythonw.exe"
}
if (-not (Test-Path $Python)) { throw "pythonw.exe nicht gefunden: $Python" }

# Symbol der Verknüpfung: seit 29.09.2026 das Glide-Symbol aus assets\icons
# (erzeugt von packaging\baue_symbole.py), sofern kein eigenes angegeben ist.
if (-not $Symbol) {
    $Vorgabe = Join-Path $Hier "..\..\assets\icons\glide.ico"
    if (Test-Path $Vorgabe) { $Symbol = (Resolve-Path $Vorgabe).Path }
}

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;
using System.Text;

namespace GlideVerknuepfung {
    [ComImport, Guid("000214F9-0000-0000-C000-000000000046"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IShellLinkW {
        void GetPath([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder pszFile, int cch, IntPtr pfd, uint fFlags);
        void GetIDList(out IntPtr ppidl);
        void SetIDList(IntPtr pidl);
        void GetDescription([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder pszName, int cch);
        void SetDescription([MarshalAs(UnmanagedType.LPWStr)] string pszName);
        void GetWorkingDirectory([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder pszDir, int cch);
        void SetWorkingDirectory([MarshalAs(UnmanagedType.LPWStr)] string pszDir);
        void GetArguments([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder pszArgs, int cch);
        void SetArguments([MarshalAs(UnmanagedType.LPWStr)] string pszArgs);
        void GetHotkey(out short pwHotkey);
        void SetHotkey(short wHotkey);
        void GetShowCmd(out int piShowCmd);
        void SetShowCmd(int iShowCmd);
        void GetIconLocation([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder pszIconPath, int cch, out int piIcon);
        void SetIconLocation([MarshalAs(UnmanagedType.LPWStr)] string pszIconPath, int iIcon);
        void SetRelativePath([MarshalAs(UnmanagedType.LPWStr)] string pszPathRel, uint dwReserved);
        void Resolve(IntPtr hwnd, uint fFlags);
        void SetPath([MarshalAs(UnmanagedType.LPWStr)] string pszFile);
    }

    [ComImport, Guid("886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IPropertyStore {
        void GetCount(out uint cProps);
        void GetAt(uint iProp, out PropertyKey pkey);
        void GetValue(ref PropertyKey key, out PropVariant pv);
        void SetValue(ref PropertyKey key, ref PropVariant pv);
        void Commit();
    }

    [StructLayout(LayoutKind.Sequential, Pack = 4)]
    public struct PropertyKey { public Guid fmtid; public uint pid; }

    [StructLayout(LayoutKind.Explicit)]
    public struct PropVariant {
        [FieldOffset(0)] public ushort vt;
        [FieldOffset(8)] public IntPtr p;
        [FieldOffset(16)] public IntPtr reserviert;
    }

    [ComImport, Guid("00021401-0000-0000-C000-000000000046")]
    class CShellLink { }

    public static class Verknuepfung {
        public static void Anlegen(string datei, string ziel, string argumente, string ordner,
                                   string symbol, string appId, string beschreibung) {
            var link = (IShellLinkW)new CShellLink();
            link.SetPath(ziel);
            link.SetArguments(argumente);
            link.SetWorkingDirectory(ordner);
            link.SetDescription(beschreibung);
            if (!String.IsNullOrEmpty(symbol)) { link.SetIconLocation(symbol, 0); }
            // System.AppUserModel.ID = {9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3}, 5
            var schluessel = new PropertyKey { fmtid = new Guid("9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3"), pid = 5 };
            var wert = new PropVariant { vt = 31, p = Marshal.StringToCoTaskMemUni(appId) };  // VT_LPWSTR
            try {
                var speicher = (IPropertyStore)link;
                speicher.SetValue(ref schluessel, ref wert);
                speicher.Commit();
            } finally {
                Marshal.FreeCoTaskMem(wert.p);
            }
            ((IPersistFile)link).Save(datei, true);
        }
    }
}
"@

$Programme = [Environment]::GetFolderPath("Programs")
$Datei = Join-Path $Programme "Glide.lnk"
$Ordner = Split-Path -Parent $Glide
[GlideVerknuepfung.Verknuepfung]::Anlegen($Datei, $Python, "`"$Glide`"", $Ordner, $Symbol, $AppId,
    "Glide – Aufgaben und Listen")
Write-Host "Verknüpfung angelegt: $Datei"
Write-Host "AppUserModelID: $AppId · Ziel: $Python `"$Glide`""
