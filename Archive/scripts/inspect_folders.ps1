$base = "C:\Users\erpri\OneDrive\Desktop\worksheet wonder"
$dirs = @("data", "fonts", "includes", "notes", "pdf")

foreach ($d in $dirs) {
    $p = Join-Path $base $d
    if (Test-Path $p) {
        Write-Host "=== Folder: $d ===" -ForegroundColor Cyan
        Get-ChildItem -Path $p -Recurse | Select-Object FullName, Length | Format-Table -AutoSize
    } else {
        Write-Host "Folder $d does not exist" -ForegroundColor Yellow
    }
}
