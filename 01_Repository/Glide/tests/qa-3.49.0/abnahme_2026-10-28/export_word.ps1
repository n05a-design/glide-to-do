param()
$ErrorActionPreference = 'Stop'
$sourcePath = Join-Path $PSScriptRoot 'Glide_Abnahmebericht_3.49.0_2026-10-28.docx'
$targetPath = Join-Path $PSScriptRoot 'Glide_Abnahmebericht_3.49.0_2026-10-28.pdf'
$wordApp = $null
$reportDocument = $null
try {
    # Eigene unsichtbare Word-Instanz; keine bestehende Benutzersitzung übernehmen.
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $wordApp.AutomationSecurity = 3
    $reportDocument = $wordApp.Documents.Open($sourcePath, $false, $true, $false)
    $reportDocument.Fields.Update() | Out-Null
    $reportDocument.Repaginate()
    $pageCount = $reportDocument.ComputeStatistics(2)
    # PDF/A-1 mit eingebetteten Schriften; keine wiederverwendeten Strukturmarkierungen.
    $reportDocument.ExportAsFixedFormat($targetPath, 17, $false, 0, 0, 1, 1, 0, $true, $true, 0, $false, $true, $true)
    [ordered]@{renderer='Microsoft Word COM'; visible=$false; source_readonly=$true; pages=$pageCount; pdfa1=$true; structure_tags=$false;
        fallback_reason='Packaged render_docx requires LibreOffice; soffice.exe unavailable.'} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'renderverfahren.json') -Encoding utf8
    Write-Output "PDF erzeugt: $targetPath ($pageCount Seiten)"
}
finally {
    if ($null -ne $reportDocument) {
        $reportDocument.Close(0)
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($reportDocument) | Out-Null
    }
    if ($null -ne $wordApp) {
        $wordApp.Quit()
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordApp) | Out-Null
    }
}
