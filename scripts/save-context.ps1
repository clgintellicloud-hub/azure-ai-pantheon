<#
.SYNOPSIS
    Minimal reliable context saver for azure-ai-pantheon.

.DESCRIPTION
    Appends a session summary to SESSION_LOG.md and stages the memory files.
    For full LIVE_STATE.md updates, the AI agent edits the file directly (more reliable).

    Always run with ExecutionPolicy Bypass on this machine if needed.
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Summary,

    [string]$FocusArea = "Work session"
)

Set-Location (Split-Path -Parent $PSScriptRoot)

$ts = Get-Date -Format "yyyy-MM-dd HH:mm"

# Append to log (very safe)
$entry = @"

## $ts — $FocusArea
**Key Changes**: $Summary
**Saved**: docs/LIVE_STATE.md + this log (git staged)
"@

Add-Content -Path "docs\SESSION_LOG.md" -Value $entry
Write-Host "Appended to SESSION_LOG.md" -ForegroundColor Green

# Stage memory files
git add AGENTS.md docs/LIVE_STATE.md docs/SESSION_LOG.md docs/TODOS.md 2>$null
Write-Host "Staged context files" -ForegroundColor Green

Write-Host ""
Write-Host "Recommended commit:" -ForegroundColor Yellow
Write-Host "git commit -m 'chore(context): $FocusArea - $Summary'"
Write-Host ""
Write-Host "For best results, also ask the agent to refresh docs/LIVE_STATE.md directly."
