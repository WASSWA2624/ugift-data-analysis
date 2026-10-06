param([Parameter(Mandatory=$true)][string]$DocumentPath)
$ErrorActionPreference = 'Stop'
$reportPath = (Resolve-Path -LiteralPath $DocumentPath).Path
$navigationWord = $null
$navigationDocument = $null
try {
    $navigationWord = New-Object -ComObject Word.Application
    $navigationWord.Visible = $false
    $navigationWord.DisplayAlerts = 0
    $navigationWord.AutomationSecurity = 3
    $navigationDocument = $navigationWord.Documents.Open($reportPath, $false, $false, $false)
    $navigationDocument.Repaginate()
    foreach ($reportContents in $navigationDocument.TablesOfContents) {
        $reportContents.Update()
    }
    $navigationDocument.Repaginate()
    foreach ($reportContents in $navigationDocument.TablesOfContents) {
        $reportContents.UpdatePageNumbers()
        $reportContents.Range.HighlightColorIndex = 0
    }
    $navigationDocument.Save()
    Write-Output ('NAVIGATION_UPDATED: ' + $reportPath)
    Write-Output ('PAGES: ' + $navigationDocument.ComputeStatistics(2))
} finally {
    if ($null -ne $navigationDocument) {
        $navigationDocument.Close(0)
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($navigationDocument) | Out-Null
    }
    if ($null -ne $navigationWord) {
        $navigationWord.Quit(0)
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($navigationWord) | Out-Null
    }
}
