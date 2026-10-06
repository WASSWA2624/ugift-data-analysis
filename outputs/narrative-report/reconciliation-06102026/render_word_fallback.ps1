param(
    [Parameter(Mandatory=$true)][string]$InputDocx,
    [Parameter(Mandatory=$true)][string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $InputDocx).Path
$destinationPath = [System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $destinationPath -Force | Out-Null
$pdfPath = Join-Path $destinationPath ([System.IO.Path]::GetFileNameWithoutExtension($sourcePath) + '.pdf')
$beforeHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
$renderWord = $null
$renderDocument = $null
try {
    $renderWord = New-Object -ComObject Word.Application
    $renderWord.Visible = $false
    $renderWord.DisplayAlerts = 0
    $renderWord.AutomationSecurity = 3
    $renderDocument = $renderWord.Documents.Open($sourcePath, $false, $true, $false)
    $renderDocument.Repaginate()
    $pageCount = $renderDocument.ComputeStatistics(2)
    $renderDocument.ExportAsFixedFormat($pdfPath, 17, $false, 0)
    Write-Output ('PDF: ' + $pdfPath)
    Write-Output ('PAGES: ' + $pageCount)
} finally {
    if ($null -ne $renderDocument) {
        $renderDocument.Close(0)
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($renderDocument) | Out-Null
    }
    if ($null -ne $renderWord) {
        $renderWord.Quit(0)
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($renderWord) | Out-Null
    }
}
$afterHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
if ($beforeHash -ne $afterHash) { throw 'Read-only render unexpectedly changed the source document.' }
Write-Output ('SOURCE_SHA256_UNCHANGED: ' + $afterHash)
