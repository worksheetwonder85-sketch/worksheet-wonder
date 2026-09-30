$target = "C:\Users\erpri\OneDrive\Desktop\worksheet wonder"
$outputFile = Join-Path $target "PROJECT_TREE_BEFORE.md"

Write-Host "Generating PROJECT_TREE_BEFORE.md..." -ForegroundColor Cyan

$allDirs = Get-ChildItem -Path $target -Recurse -Directory
$allFiles = Get-ChildItem -Path $target -Recurse -File

$dirCount = $allDirs.Count
$fileCount = $allFiles.Count
$totalSizeBytes = ($allFiles | Measure-Object -Property Length -Sum).Sum
$totalSizeMB = [math]::Round($totalSizeBytes / 1MB, 2)

$typeGroup = $allFiles | Group-Object Extension | Select-Object Name, Count, @{N='SizeMB';E={[math]::Round(($_.Group | Measure-Object Length -Sum).Sum / 1MB, 2)}} | Sort-Object Count -Descending
$largestFiles = $allFiles | Sort-Object Length -Descending | Select-Object -First 20
$topDirs = Get-ChildItem -Path $target -Directory | Select-Object Name, @{N='FileCount';E={(Get-ChildItem $_.FullName -Recurse -File).Count}}, @{N='SizeMB';E={[math]::Round(((Get-ChildItem $_.FullName -Recurse -File | Measure-Object Length -Sum).Sum / 1MB), 2)}}

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("# Project Inventory (BEFORE Cleanup)")
$lines.Add("")
$lines.Add("**Scan Date**: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
$lines.Add("**Root Location**: " + $target)
$lines.Add("**Total Folders**: " + $dirCount)
$lines.Add("**Total Files**: " + $fileCount)
$lines.Add("**Total Project Size**: " + $totalSizeMB + " MB")
$lines.Add("")
$lines.Add("---")
$lines.Add("")
$lines.Add("## Top-Level Directory Summary")
$lines.Add("")
$lines.Add("| Directory Name | Sub-Files | Size (MB) |")
$lines.Add("| :--- | :---: | :---: |")

foreach ($d in $topDirs) {
    $lines.Add("| " + $d.Name + " | " + $d.FileCount + " | " + $d.SizeMB + " MB |")
}

$lines.Add("")
$lines.Add("---")
$lines.Add("")
$lines.Add("## File Type Distribution")
$lines.Add("")
$lines.Add("| Extension | File Count | Aggregate Size (MB) |")
$lines.Add("| :--- | :---: | :---: |")

foreach ($t in $typeGroup) {
    $ext = if ($t.Name) { $t.Name } else { "[No Extension]" }
    $lines.Add("| " + $ext + " | " + $t.Count + " | " + $t.SizeMB + " MB |")
}

$lines.Add("")
$lines.Add("---")
$lines.Add("")
$lines.Add("## 20 Largest Files")
$lines.Add("")
$lines.Add("| File Path | Size (KB) |")
$lines.Add("| :--- | :---: |")

foreach ($f in $largestFiles) {
    $rel = $f.FullName.Replace($target, "")
    $sizeKB = [math]::Round($f.Length / 1KB, 1)
    $lines.Add("| " + $rel + " | " + $sizeKB + " KB |")
}

$lines.Add("")
$lines.Add("---")
$lines.Add("")
$lines.Add("## Complete File System Tree")
$lines.Add("")
$lines.Add('```')

foreach ($f in $allFiles) {
    $rel = $f.FullName.Replace($target, "")
    $lines.Add($rel)
}

$lines.Add('```')

[System.IO.File]::WriteAllLines($outputFile, $lines, [System.Text.Encoding]::UTF8)
Write-Host "PROJECT_TREE_BEFORE.md generated successfully!" -ForegroundColor Green
