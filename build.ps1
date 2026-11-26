# Builds the GitHub Pages files from the site source.
#   uras-english-cup.html  -> index.html (adds the document head GitHub Pages needs)
#   uras-sticker.jpg       -> app icons for "Add to Home Screen"
# Run from this folder:  powershell -ExecutionPolicy Bypass -File .\build.ps1
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

# 0) Parent password -> SHA-256 hash in the page (the password file itself stays out of git)
$pwFile = Join-Path $here 'parent-password.txt'
if (-not (Test-Path $pwFile)) { throw "parent-password.txt bulunamadi. Bu klasore olusturup ilk satirina veli sifresini yazin." }
$pw = ([IO.File]::ReadAllLines($pwFile, [Text.Encoding]::UTF8) | Where-Object { $_.Trim() } | Select-Object -First 1)
if (-not $pw) { throw "parent-password.txt bos. Ilk satira veli sifresini yazin." }
$pw = $pw.Trim()
$sha = [System.Security.Cryptography.SHA256]::Create()
$hash = -join ($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes('uras-english-cup:' + $pw)) | ForEach-Object { $_.ToString('x2') })
$srcPath = Join-Path $here 'uras-english-cup.html'
$src = [IO.File]::ReadAllText($srcPath, [Text.Encoding]::UTF8)
$src = [regex]::Replace($src, "const PARENT_HASH='[^']*';", "const PARENT_HASH='$hash';")
[IO.File]::WriteAllText($srcPath, $src, (New-Object Text.UTF8Encoding $false))

# 1) index.html
$head = @'
<!doctype html>
<html lang="en">
<meta name="theme-color" content="#132029">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="Uras Cup">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
'@
[IO.File]::WriteAllText((Join-Path $here 'index.html'), $head + $src, (New-Object Text.UTF8Encoding $false))

# 2) icons: Uras's round sticker on the pitch-green background
Add-Type -AssemblyName System.Drawing
function New-Icon([int]$size, [string]$name) {
  $img = [System.Drawing.Image]::FromFile((Join-Path $here 'uras-sticker.jpg'))
  $bmp = New-Object System.Drawing.Bitmap $size, $size
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = 'AntiAlias'; $g.InterpolationMode = 'HighQualityBicubic'
  $g.Clear([System.Drawing.Color]::FromArgb(47,154,87))
  $pad = [int]($size * 0.08); $d = $size - 2*$pad
  $ring = [int]($size * 0.035)
  $g.FillEllipse((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255,201,60))), $pad - $ring, $pad - $ring, $d + 2*$ring, $d + 2*$ring)
  $path = New-Object System.Drawing.Drawing2D.GraphicsPath
  $path.AddEllipse($pad, $pad, $d, $d); $g.SetClip($path)
  $g.DrawImage($img, $pad, $pad, $d, $d)
  $g.Dispose(); $bmp.Save((Join-Path $here $name), [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose(); $img.Dispose()
}
New-Icon 192 'icon-192.png'
New-Icon 512 'icon-512.png'
New-Icon 180 'apple-touch-icon.png'

# 3) kelime-listesi.pdf from kelime-listesi.html (written by vocab.py), printed with Edge or Chrome
$listHtml = Join-Path $here 'kelime-listesi.html'
if (Test-Path $listHtml) {
  $browser = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
  if ($browser) {
    $pdf = Join-Path $here 'kelime-listesi.pdf'
    $url = 'file:///' + ($listHtml -replace '\\','/')
    $p = Start-Process -FilePath $browser -ArgumentList @('--headless=new','--disable-gpu','--no-pdf-header-footer',"--print-to-pdf=`"$pdf`"",$url) -PassThru -Wait -WindowStyle Hidden
    if (Test-Path $pdf) { "Built kelime-listesi.pdf ($([int]((Get-Item $pdf).Length/1KB)) KB)" } else { "PDF could not be created (exit $($p.ExitCode))" }
  } else { 'No Edge/Chrome found: skipped PDF.' }
}
'Built index.html and icons.'
