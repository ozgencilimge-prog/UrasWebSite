# Builds the GitHub Pages files from the site source.
#   uras-english-cup.html  -> index.html (adds the document head GitHub Pages needs)
#   uras-sticker.jpg       -> app icons for "Add to Home Screen"
# Run from this folder:  powershell -ExecutionPolicy Bypass -File .\build.ps1
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

# 1) index.html
$src = [IO.File]::ReadAllText((Join-Path $here 'uras-english-cup.html'), [Text.Encoding]::UTF8)
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
'Built index.html and icons.'
