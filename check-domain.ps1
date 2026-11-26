# Daily check: connects uraslesson.com.tr to the GitHub Pages site once its DNS is ready.
# Prints one line starting with STATUS: and is safe to run any number of times.
#   NOT_REGISTERED  - the domain does not exist in public DNS yet (registration / propagation pending)
#   WRONG_DNS       - the domain exists but does not point to GitHub Pages yet (DNS records need setting)
#   ADDED           - DNS points to GitHub; CNAME file committed and pushed now
#   ALREADY_ADDED   - CNAME file already in place; prints whether the site answers on the domain
#   PUSH_FAILED     - DNS is ready but committing/pushing the CNAME file failed
$ErrorActionPreference = 'Continue'
$domain    = 'uraslesson.com.tr'
$pagesHost = 'ozgencilimge-prog.github.io'
$ghIps     = '185.199.108.153','185.199.109.153','185.199.110.153','185.199.111.153'
$git       = 'C:\Program Files\Git\cmd\git.exe'
$here      = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

function Get-Answers([string]$name, [string]$type) {
  $out = @()
  foreach ($server in '8.8.8.8','1.1.1.1') {
    try {
      $out += Resolve-DnsName -Name $name -Type $type -Server $server -DnsOnly -ErrorAction Stop |
        Where-Object { $_.Section -eq 'Answer' } |
        ForEach-Object { if ($_.IPAddress) { $_.IPAddress } elseif ($_.NameHost) { $_.NameHost.TrimEnd('.').ToLower() } }
    } catch {}
  }
  $out | Select-Object -Unique
}

$apexA   = @(Get-Answers $domain 'A')
$wwwHost = @(Get-Answers "www.$domain" 'CNAME')
$apexNS  = @(Get-Answers $domain 'NS')

$apexOk = ($apexA.Count -gt 0) -and (@($apexA | Where-Object { $ghIps -notcontains $_ }).Count -eq 0)
$wwwOk  = $wwwHost -contains $pagesHost

$cnamePath = Join-Path $here 'CNAME'
$current = if (Test-Path $cnamePath) { (Get-Content $cnamePath -Raw).Trim() } else { '' }

if ($current) {
  $code = try { (Invoke-WebRequest -UseBasicParsing -Uri "http://$current/" -TimeoutSec 20 -ErrorAction Stop).StatusCode } catch { "error: $($_.Exception.Message)" }
  $https = try { (Invoke-WebRequest -UseBasicParsing -Uri "https://$current/" -TimeoutSec 20 -ErrorAction Stop).StatusCode } catch { "not yet ($($_.Exception.Message))" }
  "STATUS: ALREADY_ADDED | CNAME=$current | http=$code | https=$https"
  exit 0
}

if (-not $apexOk -and -not $wwwOk) {
  if ($apexA.Count -eq 0 -and $apexNS.Count -eq 0 -and $wwwHost.Count -eq 0) {
    "STATUS: NOT_REGISTERED | $domain is not in public DNS yet"
  } else {
    "STATUS: WRONG_DNS | A=$($apexA -join ',') | www CNAME=$($wwwHost -join ',') | NS=$($apexNS -join ',')"
  }
  exit 0
}

# DNS points to GitHub Pages: publish the custom domain
$target = if ($apexOk) { $domain } else { "www.$domain" }
[IO.File]::WriteAllText($cnamePath, "$target`n", (New-Object Text.UTF8Encoding $false))
& $git add CNAME
& $git -c core.safecrlf=false commit --quiet -m "Connect custom domain $target" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
& $git push origin main
if ($LASTEXITCODE -ne 0) { "STATUS: PUSH_FAILED | CNAME=$target committed locally but push failed"; exit 1 }
"STATUS: ADDED | CNAME=$target pushed; GitHub Pages will serve https://$target after its certificate is issued (can take up to 24h)"
