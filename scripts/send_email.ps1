# Sends reports\email_summary.html (+ the deck attached) through the Outlook already signed in on this PC.
$root = Split-Path -Parent $PSScriptRoot
$cfg = Get-Content (Join-Path $root 'config.local.json') -Raw | ConvertFrom-Json
$reports = if ($cfg.CUL_REPORTS_DIR) { $cfg.CUL_REPORTS_DIR } else { Join-Path $root 'reports' }
$to = $cfg.CUL_EMAIL_TO
if (-not $to) { throw 'Set CUL_EMAIL_TO in config.local.json' }
$ol = New-Object -ComObject Outlook.Application
$m = $ol.CreateItem(0)
$m.To = $to
$m.Subject = (Get-Content (Join-Path $reports 'email_subject.txt') -Raw -Encoding UTF8).Trim()
$m.HTMLBody = Get-Content (Join-Path $reports 'email_summary.html') -Raw -Encoding UTF8
$m.Attachments.Add((Join-Path $reports 'daily_cost_review.pptx')) | Out-Null
$m.Send()
