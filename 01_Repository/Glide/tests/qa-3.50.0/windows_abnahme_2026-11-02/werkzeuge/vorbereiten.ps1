# Glide · Werkzeugkette für das Windows-Paket auf PC-01
# Visual Studio Build Tools (C++), gepinnte Tcl/Tk-/CPython-Quellen und eigene Tcl/Tk-9.1-Laufzeit
# mit den Windows-Bedienungshilfe-Patches – wie das Mac-Paket 3.49.0.
#
# Aufruf in einer normalen PowerShell (nicht als Administrator; die Installation fragt selbst nach):
#   powershell -NoProfile -ExecutionPolicy Bypass -File C:\gq\tk91\vorbereiten.ps1
#
# Ergebnis: C:\gq\runtime91\runtime-bau.json, Status C:\gq\tk91\status.json, Protokoll C:\gq\tk91\vorbereiten.log.
# Unabhängig vom App-Stand; ändert nichts im Projektordner. Bereits fertige Schritte werden übersprungen.

$ErrorActionPreference = 'Stop'
$Ordner  = 'C:\gq\tk91'
$Log     = Join-Path $Ordner 'vorbereiten.log'
$Quellen = 'C:\gq\quellen91'
$Ziel    = 'C:\gq\runtime91'
$Repo    = Join-Path $env:USERPROFILE 'OneDrive\Github\glide-to-do\01_Repository\Glide'
$Python  = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python314\python.exe'
$Vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
$Repos   = [ordered]@{ tcl = 'https://github.com/tcltk/tcl.git'; tk = 'https://github.com/tcltk/tk.git'; python = 'https://github.com/python/cpython.git' }

New-Item -ItemType Directory -Force -Path $Ordner | Out-Null
$Status = [ordered]@{ start = (Get-Date).ToString('o'); ergebnis = 'laeuft'; schritte = @() }

function Protokoll([string]$Text) {
    $zeile = (Get-Date -Format 'HH:mm:ss') + ' ' + $Text
    Write-Host $zeile
    Add-Content -LiteralPath $Log -Value $zeile -Encoding UTF8
}
function Schreibe-Status {
    $Status | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $Ordner 'status.json') -Encoding UTF8
}
function Abbruch([string]$Text) {
    Protokoll ('ABBRUCH: ' + $Text)
    $Status.ergebnis = 'fehlgeschlagen'; $Status.fehler = $Text; $Status.ende = (Get-Date).ToString('o')
    Schreibe-Status
    exit 1
}
function Schritt([string]$Name) {
    Protokoll ('== ' + $Name)
    $Status.schritte += $Name
    Schreibe-Status
}
function Ausfuehren([string]$Datei, [string[]]$Argumente, [string]$Ort) {
    Protokoll ('> ' + $Datei + ' ' + ($Argumente -join ' '))
    $vorher = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    if ($Ort) { Push-Location -LiteralPath $Ort }
    try {
        & $Datei @Argumente 2>&1 | ForEach-Object {
            $z = "$_"; Write-Host $z; Add-Content -LiteralPath $Log -Value $z -Encoding UTF8
        }
        $code = $LASTEXITCODE
    } finally {
        if ($Ort) { Pop-Location }
        $ErrorActionPreference = $vorher
    }
    if ($code -ne 0) { Abbruch ("$Datei endete mit Exitcode $code") }
}
function Git-Ausgabe([string]$Ort, [string[]]$Argumente) {
    $vorher = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    try { $text = (& git -C $Ort @Argumente 2>$null) -join "`n" } finally { $ErrorActionPreference = $vorher }
    return $text.Trim()
}

Protokoll ('Start Werkzeugkette Tk 9.1 · ' + $env:COMPUTERNAME)

# 1. Python, Header und Importbibliothek
Schritt 'Python 3.14 mit Entwicklungsdateien pruefen'
if (-not (Test-Path -LiteralPath $Python)) { Abbruch "Python 3.14 nicht gefunden: $Python" }
$pyBasis = Split-Path -Parent $Python
foreach ($datei in 'Include\patchlevel.h', 'libs\python314.lib') {
    if (-not (Test-Path -LiteralPath (Join-Path $pyBasis $datei))) {
        Abbruch "Python-Entwicklungsdatei fehlt: $datei (python.org-Installer mit Entwicklungsdateien erforderlich)"
    }
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Abbruch 'Git fehlt im PATH.' }
$pinsJson = & $Python -B -c "import sys,json,platform; sys.path.insert(0, sys.argv[1]); from runtime_contract import PINS, PYTHON_PINS; v=platform.python_version(); print(json.dumps(dict(PINS, python=PYTHON_PINS.get(v), version=v)))" (Join-Path $Repo 'packaging\runtime')
if ($LASTEXITCODE -ne 0) { Abbruch 'Pins aus runtime_contract.py nicht lesbar (OneDrive synchronisiert?).' }
$Pins = $pinsJson | ConvertFrom-Json
if (-not $Pins.python) { Abbruch ("Python $($Pins.version) hat keinen geprüften Quellpin (erlaubt 3.14.5/3.14.7/3.14.8).") }
$Status.python = $Pins.version; $Status.pins = $Pins
Protokoll ("Python $($Pins.version) · tcl $($Pins.tcl.Substring(0,8)) · tk $($Pins.tk.Substring(0,8)) · cpython $($Pins.python.Substring(0,8))")

# 2. Visual Studio Build Tools mit C++-x64-Werkzeugen
Schritt 'Visual Studio Build Tools (C++) pruefen bzw. installieren'
function Finde-VS {
    if (-not (Test-Path -LiteralPath $Vswhere)) { return $null }
    $pfad = & $Vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if ($pfad) { return ($pfad | Select-Object -First 1).Trim() }
    return $null
}
$VS = Finde-VS
if (-not $VS) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { Abbruch 'winget fehlt; Build Tools bitte manuell installieren (Workload „Desktopentwicklung mit C++“).' }
    Protokoll 'Installiere Visual Studio 2022 Build Tools mit C++-Workload (mehrere GB; Windows fragt nach Administratorrechten) …'
    $vorher = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    & winget install --id Microsoft.VisualStudio.2022.BuildTools -e --source winget --accept-package-agreements --accept-source-agreements --override '--wait --passive --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended' 2>&1 | ForEach-Object { $z = "$_"; Write-Host $z; Add-Content -LiteralPath $Log -Value $z -Encoding UTF8 }
    $wingetCode = $LASTEXITCODE
    $ErrorActionPreference = $vorher
    Protokoll "winget beendet mit Code $wingetCode"
    $VS = Finde-VS
    if (-not $VS) { Abbruch 'Build Tools mit C++-x64-Werkzeugen nicht gefunden. Ggf. Neustart von Windows und Skript erneut starten.' }
}
$Status.visual_studio = $VS
Protokoll "Build Tools: $VS"
$vcvars = Join-Path $VS 'VC\Auxiliary\Build\vcvars64.bat'
if (-not (Test-Path -LiteralPath $vcvars)) { Abbruch "vcvars64.bat fehlt: $vcvars" }
$umgebung = & cmd.exe /d /c "`"$vcvars`" >nul 2>&1 && set"
foreach ($zeile in $umgebung) {
    if ($zeile -match '^([^=]+)=(.*)$') { Set-Item -LiteralPath ('env:' + $Matches[1]) -Value $Matches[2] }
}
foreach ($werkzeug in 'cl', 'nmake', 'link') {
    if (-not (Get-Command $werkzeug -ErrorAction SilentlyContinue)) { Abbruch "$werkzeug nach vcvars64 nicht verfügbar." }
}
Remove-Item -LiteralPath env:PYTHONPATH -ErrorAction SilentlyContinue

# 3. Gepinnte Originalquellen (flacher Abruf, LF-Zeilenenden nur in diesen Arbeitskopien)
Schritt 'Tcl-/Tk-/CPython-Quellen an den Pins holen'
New-Item -ItemType Directory -Force -Path $Quellen | Out-Null
foreach ($art in $Repos.Keys) {
    $ort = Join-Path $Quellen $art
    $pin = $Pins.$art
    if (Test-Path -LiteralPath (Join-Path $ort '.git')) {
        $kopf = Git-Ausgabe $ort @('rev-parse', 'HEAD')
        $offen = Git-Ausgabe $ort @('status', '--porcelain', '--untracked-files=all')
        if ($kopf -eq $pin -and -not $offen) { Protokoll "$art bereits am Pin, unverändert"; continue }
        Abbruch "$ort existiert, steht aber nicht sauber auf $pin. Ordner beiseitelegen und neu starten."
    }
    if ((Test-Path -LiteralPath $ort) -and (Get-ChildItem -LiteralPath $ort -Force | Select-Object -First 1)) {
        Abbruch "$ort ist nicht leer und kein Git-Ordner."
    }
    New-Item -ItemType Directory -Force -Path $ort | Out-Null
    Ausfuehren 'git' @('init', '-q') $ort
    Ausfuehren 'git' @('config', 'core.autocrlf', 'false') $ort
    Ausfuehren 'git' @('config', 'core.eol', 'lf') $ort
    Ausfuehren 'git' @('fetch', '--depth=1', $Repos[$art], $pin) $ort
    Ausfuehren 'git' @('checkout', '-q', '--detach', 'FETCH_HEAD') $ort
    $kopf = Git-Ausgabe $ort @('rev-parse', 'HEAD')
    if ($kopf -ne $pin) { Abbruch "$art steht auf $kopf statt $pin" }
    Protokoll "$art geholt: $pin"
}

# 3b. CPython-Header: baue_runtime.py verlangt den Export bytegleich zur installierten patchlevel.h.
#     CPython legt keine Zeilenenden fest; der Windows-Installer liefert CRLF. Nur diese Quellkopie anpassen.
Schritt 'CPython-Header mit Installation abgleichen'
$pyOrt = Join-Path $Quellen 'python'
$headerInstalliert = Join-Path $pyBasis 'Include\patchlevel.h'
$hatCrlf = [Text.Encoding]::ASCII.GetString([IO.File]::ReadAllBytes($headerInstalliert)).Contains("`r`n")
if ($hatCrlf) {
    Ausfuehren 'git' @('config', 'core.autocrlf', 'true') $pyOrt
    Ausfuehren 'git' @('config', 'core.eol', 'crlf') $pyOrt
} else {
    Ausfuehren 'git' @('config', 'core.autocrlf', 'false') $pyOrt
    Ausfuehren 'git' @('config', 'core.eol', 'lf') $pyOrt
}
$exportHeader = Join-Path $Ordner 'patchlevel_export.h'
& cmd.exe /d /c "git -C `"$pyOrt`" cat-file --filters HEAD:Include/patchlevel.h > `"$exportHeader`""
if ($LASTEXITCODE -ne 0) { Abbruch 'Export von Include/patchlevel.h fehlgeschlagen.' }
$hashInstalliert = (Get-FileHash -LiteralPath $headerInstalliert -Algorithm SHA256).Hash
$hashExport = (Get-FileHash -LiteralPath $exportHeader -Algorithm SHA256).Hash
$Status.header = [ordered]@{ installiert = $hashInstalliert; export = $hashExport; crlf = $hatCrlf }
Protokoll ("patchlevel.h installiert $($hashInstalliert.Substring(0,12)) · Export $($hashExport.Substring(0,12)) · CRLF $hatCrlf")
if ($hashInstalliert -ne $hashExport) {
    Abbruch 'Installierte patchlevel.h weicht auch nach Zeilenendenabgleich vom gepinnten Original ab (andere Python-Fassung oder veränderte Installation?).'
}

# 4. Laufzeit bauen (leeres Ziel; ein unvollständiger Altbau wird beiseitegelegt, nicht gelöscht)
Schritt 'Tcl/Tk 9.1 und _tkinter bauen'
if (Test-Path -LiteralPath (Join-Path $Ziel 'runtime-bau.json')) {
    Protokoll "Vorhandene Laufzeit mit runtime-bau.json gefunden, Bau übersprungen: $Ziel"
} else {
    if ((Test-Path -LiteralPath $Ziel) -and (Get-ChildItem -LiteralPath $Ziel -Force | Select-Object -First 1)) {
        $beiseite = $Ziel + '_unvollstaendig_' + (Get-Date -Format 'yyyyMMdd-HHmmss')
        Rename-Item -LiteralPath $Ziel -NewName (Split-Path -Leaf $beiseite)
        Protokoll "Unvollständigen Altbau beiseitegelegt: $beiseite"
    }
    Ausfuehren $Python @('-B', (Join-Path $Repo 'packaging\runtime\baue_runtime.py'),
        '--tcl-quelle', (Join-Path $Quellen 'tcl'), '--tk-quelle', (Join-Path $Quellen 'tk'),
        '--python-quelle', (Join-Path $Quellen 'python'), '--ziel', $Ziel) $Ordner
}

# 5. Probe: lädt Python tatsächlich Tk 9.1 aus der eigenen Laufzeit?
Schritt 'Probe Tk 9.1'
$env:PYTHONPATH = Join-Path $Ziel 'python-extension'
$probe = & $Python -B -c "import json,_tkinter,tkinter as t; r=t.Tk(); r.withdraw(); v=r.tk.call('package','provide','Tk'); r.destroy(); print(json.dumps(dict(tk=str(v), extension=_tkinter.__file__)))"
$probeCode = $LASTEXITCODE
Remove-Item -LiteralPath env:PYTHONPATH -ErrorAction SilentlyContinue
if ($probeCode -ne 0) { Abbruch 'Tk-Probe mit eigener Laufzeit fehlgeschlagen.' }
$probeDaten = $probe | ConvertFrom-Json
Protokoll ("Probe: Tk $($probeDaten.tk) aus $($probeDaten.extension)")
if ($probeDaten.tk -ne '9.1.0') { Abbruch "Erwartet Tk 9.1.0, geladen $($probeDaten.tk)." }

$Status.probe = $probeDaten
$Status.runtime_bau = Join-Path $Ziel 'runtime-bau.json'
$Status.ergebnis = 'fertig'
$Status.ende = (Get-Date).ToString('o')
Schreibe-Status
Protokoll 'Fertig: eigene Tcl/Tk-9.1-Laufzeit gebaut und geprüft. Weiter erst mit dem eingefrorenen App-Stand.'
exit 0
