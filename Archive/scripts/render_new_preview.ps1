$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$base = "C:\Users\erpri\OneDrive\Desktop\worksheet wonder"
$mockupHtml = Join-Path $base "NEW_LAYOUT_MOCKUP.html"
$outputPng = Join-Path $base "NEW_LAYOUT_PREVIEW.png"

Write-Host "Rendering High-Res A4 300 DPI NEW_LAYOUT_PREVIEW.png..." -ForegroundColor Cyan

# Create temp single page 1 HTML for clean single-page preview
$fullHtml = Get-Content $mockupHtml -Raw
$p1Html = $fullHtml -replace '<div class="page" id="page-2">[\s\S]*$', '</body></html>'
$tempFile = Join-Path $base "temp_new_p1.html"
Set-Content -Path $tempFile -Value $p1Html -Encoding UTF8

Start-Process -FilePath $edgePath -ArgumentList "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=2480,3508", "--screenshot=`"$outputPng`"", "`"file:///$($tempFile.Replace('\','/'))`"" -Wait

Remove-Item -Path $tempFile -ErrorAction SilentlyContinue

Write-Host "NEW_LAYOUT_PREVIEW.png Successfully Rendered!" -ForegroundColor Green
Get-Item $outputPng | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
