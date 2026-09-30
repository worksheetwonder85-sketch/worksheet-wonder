$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

$base = "C:\Users\erpri\OneDrive\Desktop\worksheet wonder"
$letterFile = Join-Path $base "Workbook\Letters\Letter_A.html"
$previewDir = Join-Path $base "Workbook\Preview"

Write-Host "Rendering High-Resolution 2480x3508 PNG Previews..." -ForegroundColor Cyan

# Create single-page HTML files for exact rendering
$fullHtml = Get-Content $letterFile -Raw

# Page 1 Single HTML
$p1Html = $fullHtml -replace '<div class="page" id="page-2">[\s\S]*$', '</body></html>'
$p1File = Join-Path $previewDir "temp_page1.html"
Set-Content -Path $p1File -Value $p1Html -Encoding UTF8

# Page 2 Single HTML
$p2Match = [regex]::Match($fullHtml, '(<div class="page" id="page-2">[\s\S]*?)(<div class="page" id="page-3">)')
if ($p2Match.Success) {
    $p2Content = $p2Match.Groups[1].Value
    $p2Html = $fullHtml.Split('<div class="page" id="page-1">')[0] + $p2Content + "</body></html>"
    $p2File = Join-Path $previewDir "temp_page2.html"
    Set-Content -Path $p2File -Value $p2Html -Encoding UTF8
}

# Page 3 Single HTML
$p3Match = [regex]::Match($fullHtml, '(<div class="page" id="page-3">[\s\S]*?)(</body>)')
if ($p3Match.Success) {
    $p3Content = $p3Match.Groups[1].Value
    $p3Html = $fullHtml.Split('<div class="page" id="page-1">')[0] + $p3Content + "</body></html>"
    $p3File = Join-Path $previewDir "temp_page3.html"
    Set-Content -Path $p3File -Value $p3Html -Encoding UTF8
}

# Render PNGs using Edge Headless
$p1Png = Join-Path $previewDir "Letter_A_Page1.png"
$p2Png = Join-Path $previewDir "Letter_A_Page2.png"
$p3Png = Join-Path $previewDir "Letter_A_Page3.png"

Write-Host "Rendering Page 1..." -ForegroundColor Yellow
Start-Process -FilePath $edgePath -ArgumentList "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=2480,3508", "--screenshot=`"$p1Png`"", "`"file:///$($p1File.Replace('\','/'))`"" -Wait

Write-Host "Rendering Page 2..." -ForegroundColor Yellow
Start-Process -FilePath $edgePath -ArgumentList "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=2480,3508", "--screenshot=`"$p2Png`"", "`"file:///$($p2File.Replace('\','/'))`"" -Wait

Write-Host "Rendering Page 3..." -ForegroundColor Yellow
Start-Process -FilePath $edgePath -ArgumentList "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=2480,3508", "--screenshot=`"$p3Png`"", "`"file:///$($p3File.Replace('\','/'))`"" -Wait

# Clean up temp HTMLs
Remove-Item -Path $p1File, $p2File, $p3File -ErrorAction SilentlyContinue

Write-Host "Rendering Complete!" -ForegroundColor Green
Get-ChildItem $previewDir -Filter "*.png" | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
