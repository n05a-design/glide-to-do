# Glide – Vollprüfung unter Windows
#
# Startet dieselbe Vollprüfung wie auf dem Entwicklungs-Mac (tests/tools/pruefen.py
# im Vollmodus) und legt das Protokoll unter tests/qa-<Version>/windows_<Zeitstempel>
# ab. Die Suiten isolieren ihre Daten selbst über GLIDE_DATA_DIR; der echte
# Datenordner unter %APPDATA%\Glide wird nicht berührt.
#
# Aufruf: Doppelklick auf windows_vollpruefung.cmd oder
#   powershell -NoProfile -ExecutionPolicy Bypass -File tests\tools\windows_vollpruefung.ps1

param(
    [int]$Timeout = 900
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repo

# Python finden: bevorzugt den Starter "py -3", sonst "python".
if (Get-Command py -ErrorAction SilentlyContinue) {
    $python = "py"; $pyArgs = @("-3")
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $python = "python"; $pyArgs = @()
} else {
    Write-Host "Kein Python gefunden. Bitte Python 3.12 oder neuer von python.org installieren (mit Tcl/Tk)." -ForegroundColor Red
    exit 3
}

Write-Host "== Glide-Vollprüfung unter Windows"
& $python @pyArgs --version
& $python @pyArgs -c "import tkinter; print('Tk', tkinter.Tcl().eval('info patchlevel'))"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tk fehlt in diesem Python. Bitte die python.org-Installation mit Tcl/Tk verwenden." -ForegroundColor Red
    exit 3
}

# OneDrive-Platzhalter (nur online verfügbare Dateien) ließen den Lauf 3.28 scheitern.
$offline = Get-ChildItem -Path $repo -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Attributes -band [IO.FileAttributes]::Offline }
if ($offline) {
    Write-Host "$($offline.Count) Dateien sind nur online verfügbar (OneDrive-Platzhalter)." -ForegroundColor Yellow
    Write-Host "Bitte den Ordner 'Glide ToDo' im Explorer per Rechtsklick auf 'Immer auf diesem Gerät behalten' stellen und neu starten." -ForegroundColor Yellow
    exit 4
}

$version = (Get-Content -Raw -Path (Join-Path $repo "VERSION")).Trim()
$stempel = Get-Date -Format "yyyy-MM-dd_HHmm"
$ziel = "tests/qa-$version/windows_$stempel"

& $python @pyArgs tests/tools/pruefen.py --modus voll --protokoll $ziel --timeout $Timeout
$code = $LASTEXITCODE
Write-Host ""
Write-Host "Exitcode: $code"
Write-Host "Protokoll: $ziel (ergebnis.json, Logs und release_hell.png zur Sichtprüfung)"
exit $code
