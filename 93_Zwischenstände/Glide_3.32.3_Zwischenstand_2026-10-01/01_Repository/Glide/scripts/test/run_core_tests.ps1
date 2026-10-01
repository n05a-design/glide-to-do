param(
    [ValidateSet('schnell', 'voll')]
    [string]$Modus = 'schnell',
    [string]$Python = 'python',
    [string]$Protokoll = ''
)

$ErrorActionPreference = 'Stop'
$repositoryRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$testFile = Join-Path $repositoryRoot 'tests\tools\pruefen.py'
$testArguments = @($testFile, '--modus', $Modus)
if ($Protokoll) {
    $testArguments += @('--protokoll', $Protokoll)
}
& $Python @testArguments
exit $LASTEXITCODE
