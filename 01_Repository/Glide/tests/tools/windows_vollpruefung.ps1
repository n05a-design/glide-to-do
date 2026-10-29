# Glide – Vollprüfung unter Windows
#
# Startet dieselbe Vollprüfung wie auf dem Entwicklungs-Mac (tests/tools/pruefen.py
# im Vollmodus) in einer lokalen eingefrorenen Prüfkopie außerhalb von
# OneDrive/System-Temp. Die Suiten isolieren ihre Daten über GLIDE_DATA_DIR; der echte
# Datenordner unter %APPDATA%\Glide wird nicht berührt.
#
# Aufruf: Doppelklick auf windows_vollpruefung.cmd oder
#   powershell -NoProfile -ExecutionPolicy Bypass -File tests\tools\windows_vollpruefung.ps1

param(
    [int]$Timeout = 900,
    [string]$PythonExecutable,
    [string]$Arbeitsablage
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repo

# Eine explizite Laufzeit hat Vorrang. Der lokale QA-Cache verändert weder
# PATH noch die Standardinstallation; danach den 3.14-Starter versuchen.
$glideQaPython = Join-Path $env:USERPROFILE '.cache/glide-qa/python-3.14.8/runtime/python.exe'
if ($PythonExecutable) {
    $python = (Get-Command $PythonExecutable -ErrorAction Stop).Source; $pyArgs = @()
} elseif (Test-Path -LiteralPath $glideQaPython -PathType Leaf) {
    $python = $glideQaPython; $pyArgs = @()
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $python = "py"; $pyArgs = @("-3.14")
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $python = "python"; $pyArgs = @()
} else {
    Write-Host "Kein Python gefunden. Die Vollprüfung braucht Python 3.14 mit Tk 9 von python.org." -ForegroundColor Red
    exit 3
}

Write-Host "== Glide-Vollprüfung unter Windows"
& $python @pyArgs --version
& $python @pyArgs -B -c "import sys,tkinter as tk; r=tk.Tk(); r.withdraw(); v=r.tk.call('package','provide','Tk'); print('Tk',v); r.destroy(); sys.exit(0 if sys.version_info >= (3,14) and int(v.split('.')[0]) >= 9 else 3)"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ungeeignete Prüflaufzeit. Python 3.14 und Tk 9 sind erforderlich; -PythonExecutable kann den Pfad explizit setzen." -ForegroundColor Red
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

$pruefArgumente = @('-B', 'tests/tools/gesichert_pruefen.py', '--art', 'voll', '--timeout', "$Timeout")
if ($Arbeitsablage) { $pruefArgumente += @('--arbeitsablage', $Arbeitsablage) }
& $python @pyArgs @pruefArgumente
$code = $LASTEXITCODE
Write-Host ""
Write-Host "Exitcode: $code"
Write-Host "Prüfkopie, Hashnachweise und Protokoll: im oben ausgegebenen lokalen Prüfordner (Standard: ~/GlidePruefung)."
exit $code
