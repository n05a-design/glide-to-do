param([string]$Revision='final1')
$ErrorActionPreference='Stop'
$workspacePath = '%USERPROFILE%\OneDrive\Glide ToDo'
$docPath = Join-Path $workspacePath '10_Dokumentation\3.2.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.docx'
$qaPath = $PSScriptRoot
$pdfPath = Join-Path $qaPath ($Revision + '.pdf')
$wordForQa = New-Object -ComObject Word.Application
$wordForQa.Visible = $false
$wordForQa.DisplayAlerts = 0
try {
    $qaDocument = $wordForQa.Documents.Open($docPath, $false, $true)
    $qaDocument.Repaginate()
    $qaDocument.ExportAsFixedFormat($pdfPath,17)
    $pageMap = @{}
    foreach($bookmark in $qaDocument.Bookmarks) {
        if ($bookmark.Name -like 'GlideToc*') {
            $pageMap[$bookmark.Name] = $bookmark.Range.Information(3)
        }
    }
    $pageMap | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $qaPath 'bookmark_pages.json') -Encoding utf8
    $qaDocument.Close(0)
    Get-Item -LiteralPath $pdfPath | Select-Object Name,Length
} finally {
    $wordForQa.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordForQa) | Out-Null
}
