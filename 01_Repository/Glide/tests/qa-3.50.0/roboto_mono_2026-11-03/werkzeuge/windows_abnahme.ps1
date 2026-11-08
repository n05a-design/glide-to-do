# Glide · Windows-Abnahme auf PC-01: eingefrorener Volllauf mit eigener Tk 9.1 und nativer Zugangsprüfung,
# danach Windows-Paket aus genau dieser eingefrorenen Kopie und isolierte Startprobe.
#
# Aufruf (normale PowerShell):
#   powershell -NoProfile -ExecutionPolicy Bypass -File C:\gq\abnahme\windows_abnahme.ps1 -AusGitHub
#   optional -AppHash 1582c600 (erwarteter SHA-256-Anfang von src/glide/app.pyw), -NurPaket (ohne Volllauf)
#   optional -Zweig <Name> (nur mit -AusGitHub): statt main einen gepushten Zweig prüfen, z. B. vor dem Merge
#     -Zweig codex/glide-3.50-validierung-20261102 -AppHash 067e683b   (Ergänzung 03.11.2026, Vorgabe bleibt main)
#
# Voraussetzung: C:\gq\tk91\vorbereiten.ps1 erfolgreich (C:\gq\runtime91). Während des Volllaufs PC nicht bedienen.
# Laufordner C:\gq\w<MMdd-HHmm> (außerhalb OneDrive); flache Belege danach in
# 13_TK-Test-Umgebung\PC-01-AMD\w<MMdd-HHmm>. Keine Git-, Liefer- oder Versionsaktion; das Paket bleibt Entwicklungsbau.

param(
    [string]$AppHash = '',
    [switch]$NurPaket,
    [switch]$AusGitHub,
    [string]$Zweig = 'main'
)

$ErrorActionPreference = 'Stop'
$Werkzeug = $PSScriptRoot
$OneDrive = Join-Path $env:USERPROFILE 'OneDrive\Github\glide-to-do'
$Projekt  = $OneDrive
$Python   = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python314\python.exe'
$Runtime  = 'C:\gq\runtime91'
$Ext      = Join-Path $Runtime 'python-extension'
$Name     = 'w' + (Get-Date -Format 'MMdd-HHmm')
$Lauf     = Join-Path 'C:\gq' $Name
$Log      = Join-Path $Lauf 'abnahme.log'
$Belege   = Join-Path $OneDrive ('13_TK-Test-Umgebung\PC-01-AMD\' + $Name)

New-Item -ItemType Directory -Force -Path $Lauf | Out-Null
$Status = [ordered]@{ lauf = $Name; start = (Get-Date).ToString('o'); ergebnis = 'laeuft'; schritte = @() }

function Protokoll([string]$Text) {
    $zeile = (Get-Date -Format 'HH:mm:ss') + ' ' + $Text
    Write-Host $zeile
    Add-Content -LiteralPath $Log -Value $zeile -Encoding UTF8
}
function Schreibe-Status {
    $Status | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $Lauf 'status.json') -Encoding UTF8
}
function Belege-Ablegen {
    if (Test-Path -LiteralPath (Join-Path $Lauf 'status.json')) {
        $vorher = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
        & $Python -B (Join-Path $Werkzeug 'belege.py') $Lauf $Belege 2>&1 | ForEach-Object {
            $z = "$_"; Write-Host $z; Add-Content -LiteralPath $Log -Value $z -Encoding UTF8 }
        $ErrorActionPreference = $vorher
    }
}
function Ende([string]$Ergebnis, [string]$Text, [int]$Code) {
    Protokoll $Text
    $Status.ergebnis = $Ergebnis; $Status.ende = (Get-Date).ToString('o')
    if ($Code -ne 0) { $Status.fehler = $Text }
    Schreibe-Status
    Belege-Ablegen
    Protokoll ('Belege: ' + $Belege)
    exit $Code
}
function Abbruch([string]$Text) { Ende 'fehlgeschlagen' ('ABBRUCH: ' + $Text) 1 }
function Schritt([string]$Name) {
    Protokoll ('== ' + $Name)
    $Status.schritte += $Name
    Schreibe-Status
}
function Ausfuehren([string]$Datei, [string[]]$Argumente, [string]$Ort, [string]$Mitschrift) {
    Protokoll ('> ' + $Datei + ' ' + ($Argumente -join ' '))
    $vorher = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    if ($Ort) { Push-Location -LiteralPath $Ort }
    try {
        & $Datei @Argumente 2>&1 | ForEach-Object {
            $z = "$_"; Write-Host $z; Add-Content -LiteralPath $Log -Value $z -Encoding UTF8
            if ($Mitschrift) { Add-Content -LiteralPath $Mitschrift -Value $z -Encoding UTF8 }
        }
        $code = $LASTEXITCODE
    } finally {
        if ($Ort) { Pop-Location }
        $ErrorActionPreference = $vorher
    }
    return $code
}

Protokoll ("Windows-Abnahme $Name · $env:COMPUTERNAME")
# Während des Laufs weder Energiesparmodus noch Bildschirmabschaltung/-sperre (gilt nur für diesen Prozess).
Add-Type -Namespace GlideAbnahme -Name Energie -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
[void][GlideAbnahme.Energie]::SetThreadExecutionState([uint32]'0x80000003')
$env:PYTHONUTF8 = '1'; $env:PYTHONDONTWRITEBYTECODE = '1'; $env:PYTHONFAULTHANDLER = '1'; $env:GLIDE_TEST_MODE = '1'
Remove-Item -LiteralPath env:PYTHONPATH -ErrorAction SilentlyContinue

# 0. Optional: frischer, vollständiger Klon von GitHub main außerhalb OneDrive
#    (Zeilenenden unverändert wie im Repository, lange Pfade erlaubt; Tests brauchen die Git-Historie).
if ($AusGitHub) {
    Schritt 'Frischer Klon von GitHub main'
    $Projekt = Join-Path 'C:\gq' ('q' + (Get-Date -Format 'MMdd-HHmm'))
    if ((Ausfuehren 'git' @('-c', 'core.autocrlf=false', '-c', 'core.eol=lf', '-c', 'core.longpaths=true', 'clone', '--quiet', 'https://github.com/n05a-design/glide-to-do', $Projekt) $null $null) -ne 0) {
        Abbruch 'Klon von GitHub fehlgeschlagen.'
    }
    foreach ($einstellung in @(@('core.autocrlf', 'false'), @('core.eol', 'lf'), @('core.longpaths', 'true'))) {
        if ((Ausfuehren 'git' (@('-C', $Projekt, 'config') + $einstellung) $null $null) -ne 0) { Abbruch 'Git-Einstellung im Klon fehlgeschlagen.' }
    }
    if ($Zweig -ne 'main') {
        if ((Ausfuehren 'git' @('-C', $Projekt, 'checkout', '--quiet', $Zweig) $null $null) -ne 0) {
            Abbruch "Zweig $Zweig nicht auf GitHub gefunden."
        }
    }
    $Status.quelle = 'github ' + $Zweig
    $Status.zweig = $Zweig
    $Status.git_commit = (& git -C $Projekt rev-parse HEAD).Trim()
    Protokoll ("Klon $Projekt · Zweig $Zweig · Commit $($Status.git_commit)")
} else {
    if ($Zweig -ne 'main') { Abbruch '-Zweig wirkt nur zusammen mit -AusGitHub.' }
    $Status.quelle = 'OneDrive-Projektordner'
}
$Repo = Join-Path $Projekt '01_Repository\Glide'
$Status.projekt = $Projekt

# 1. Voraussetzungen und Quellstand
Schritt 'Voraussetzungen und App-Stand pruefen'
if (-not (Test-Path -LiteralPath (Join-Path $Runtime 'runtime-bau.json'))) { Abbruch 'Tk-9.1-Laufzeit fehlt; zuerst C:\gq\tk91\vorbereiten.ps1.' }
if (-not $AppHash -and $AusGitHub) {
    Protokoll "Kein -AppHash angegeben: maßgeblich ist der geklonte Stand von GitHub $Zweig."
} elseif ($AppHash.Length -lt 8) { Abbruch 'AppHash braucht mindestens 8 Zeichen (oder -AusGitHub ohne AppHash).' }
$appIst = (Get-FileHash -LiteralPath (Join-Path $Repo 'src\glide\app.pyw') -Algorithm SHA256).Hash.ToLower()
$Version = (Get-Content -LiteralPath (Join-Path $Repo 'VERSION') -Raw).Trim()
$Status.app_sha256 = $appIst; $Status.version = $Version
Protokoll ("App $($appIst.Substring(0,12))… · Version $Version")
if ($AppHash -and -not $appIst.StartsWith($AppHash.ToLower())) {
    Abbruch ("App-Stand $($appIst.Substring(0,12))… entspricht nicht dem erwarteten $AppHash. OneDrive-Synchronisierung bzw. Übernahme vom Mac abwarten.")
}
$env:PYTHONPATH = $Ext
$tk = & $Python -B -c "import tkinter as t; r=t.Tk(); r.withdraw(); print(r.tk.call('package','provide','Tk')); r.destroy()"
Remove-Item -LiteralPath env:PYTHONPATH -ErrorAction SilentlyContinue
if ("$tk".Trim() -ne '9.1.0') { Abbruch "Eigene Laufzeit liefert Tk $tk statt 9.1.0." }
$Status.tk = '9.1.0'
Protokoll 'Tk 9.1.0 aus der eigenen Laufzeit bestätigt'

Schritt 'Projektdateien aus OneDrive laden'
if ((Ausfuehren $Python @('-B', (Join-Path $Werkzeug 'dateien_laden.py'), $Projekt) $null $null) -ne 0) {
    Abbruch 'Nicht alle Projektdateien ließen sich aus OneDrive laden.'
}

# 2. Einfrieren und Volllauf (Tk 9.1, native Zugangsprüfung)
if (-not $NurPaket) {
    Schritt 'Einfrieren und Volllauf mit Tk 9.1'
    Protokoll 'Ab jetzt Maus und Tastatur nicht benutzen und den PC nicht sperren; Prüffenster öffnen sich im Vordergrund.'
    Start-Sleep -Seconds 10
    $code = Ausfuehren $Python @('-B', '-u', (Join-Path $Werkzeug 'voll_tk91.py'), $Repo, $Lauf, $Ext) $null (Join-Path $Lauf 'starter.stdout.log')
    $Status.volllauf_exitcode = $code
    Schreibe-Status
    if ($code -ne 0) { Ende 'volllauf_rot' "Volllauf rot (Exitcode $code). Kein Paketbau; Befund erhalten." 1 }
    Protokoll 'Volllauf grün'
} else {
    Schritt 'Nur Paket: Einfrieren ohne Volllauf'
    $code = Ausfuehren $Python @('-B', '-c', "import sys,json; from pathlib import Path; sys.path.insert(0, sys.argv[1]+'/tests/tools'); from pruefablauf import einfrieren; f,r=einfrieren(Path(sys.argv[1]), Path(sys.argv[2])); Path(sys.argv[2],'lauf.json').write_text(json.dumps(dict(eingefroren=str(f), nachweise=str(r)), indent=2), encoding='utf-8')", $Repo, $Lauf) $null $null
    if ($code -ne 0) { Abbruch 'Einfrieren fehlgeschlagen.' }
}
$laufDaten = Get-Content -LiteralPath (Join-Path $Lauf 'lauf.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$Frozen = $laufDaten.eingefroren
$Status.eingefroren = $Frozen
Protokoll "Eingefrorene Kopie: $Frozen"

# 3. Windows-Paket aus der eingefrorenen Kopie (eigene Tk 9.1)
Schritt 'Bauumgebung (venv, gepinnte Bauabhaengigkeiten)'
$Venv = Join-Path $Lauf 'venv'
$VPy = Join-Path $Venv 'Scripts\python.exe'
if ((Ausfuehren $Python @('-B', '-m', 'venv', $Venv) $null $null) -ne 0) { Abbruch 'venv konnte nicht angelegt werden.' }
$env:PYTHONPATH = $Ext
if ((Ausfuehren $VPy @('-B', '-m', 'pip', 'install', '--disable-pip-version-check', '-r', (Join-Path $Frozen 'requirements\build-windows.txt')) $null (Join-Path $Lauf 'pip.log')) -ne 0) {
    Abbruch 'Bauabhängigkeiten konnten nicht installiert werden (Netz/PyPI?).'
}

Schritt 'Lizenzbestand vorbereiten'
$Paket = Join-Path $Lauf 'paket'
if ((Ausfuehren $VPy @('-B', 'packaging/paket/lizenzen_vorbereiten_windows.py', '--quelle', 'src/glide', '--repo', '.', '--ziel', (Join-Path $Paket 'lizenzen'), '--runtime-bau', (Join-Path $Runtime 'runtime-bau.json')) $Frozen (Join-Path $Lauf 'lizenzen.log')) -ne 0) {
    Abbruch 'Lizenzbestand fehlgeschlagen; siehe lizenzen.log.'
}

Schritt 'Paket bauen'
if ((Ausfuehren $VPy @('-B', 'packaging/paket/baue_paket.py', '--quelle', 'src/glide', '--version', $Version, '--ziel', (Join-Path $Paket 'bau'), '--plattform', 'windows-x64', '--lizenzen', (Join-Path $Paket 'lizenzen'), '--runtime-bau', (Join-Path $Runtime 'runtime-bau.json')) $Frozen (Join-Path $Lauf 'paketbau.log')) -ne 0) {
    Abbruch 'Paketbau fehlgeschlagen; siehe paketbau.log und paket\bau.'
}
Remove-Item -LiteralPath env:PYTHONPATH -ErrorAction SilentlyContinue

Schritt 'Startprobe des gebauten Pakets'
$Exe = Join-Path $Paket 'bau\dist\Glide\Glide.exe'
if (-not (Test-Path -LiteralPath $Exe)) { Abbruch "Glide.exe fehlt: $Exe" }
$StartJson = Join-Path $Paket 'start.json'
# Startprobe ohne Prüf-/Python-Umgebungsvariablen, damit das Paket nichts von außen nachlädt.
foreach ($v in 'PYTHONPATH', 'PYTHONUTF8', 'PYTHONDONTWRITEBYTECODE', 'PYTHONFAULTHANDLER', 'GLIDE_TEST_MODE') {
    Remove-Item -LiteralPath ('env:' + $v) -ErrorAction SilentlyContinue
}
$proc = Start-Process -FilePath $Exe -ArgumentList @('--paket-pruefen', ('"' + $StartJson + '"')) -Wait -PassThru
$Status.startprobe_exitcode = $proc.ExitCode
$Status.paket = $Exe
$Status.exe_sha256 = (Get-FileHash -LiteralPath $Exe -Algorithm SHA256).Hash.ToLower()
Schreibe-Status
if ($proc.ExitCode -ne 0) { Abbruch ("Startprobe rot (Exitcode $($proc.ExitCode)); siehe paket\start.json.") }

if ($NurPaket) { $umfang = 'Paketbau und Startprobe grün (ohne Volllauf)' } else { $umfang = 'Volllauf, Paketbau und Startprobe grün' }
Ende 'gruen' "Fertig: $umfang. Paket (Entwicklungsbau, unsigniert): $Exe" 0
