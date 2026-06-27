# resume-context.ps1
# Quick helper to dump essential project context for a new Grok session (after reboot, etc.)

Write-Host "=== azure-ai-pantheon Context ===" -ForegroundColor Cyan
Write-Host "Project root: $(Get-Location)`n"

Write-Host "--- README.md ---" -ForegroundColor Yellow
Get-Content README.md

Write-Host "`n--- AGENTS.md (first 80 lines) ---" -ForegroundColor Yellow
Get-Content AGENTS.md -TotalCount 80

Write-Host "`n--- docs/STATUS.md ---" -ForegroundColor Yellow
if (Test-Path docs/STATUS.md) { Get-Content docs/STATUS.md -TotalCount 50 } else { "No STATUS.md yet" }

Write-Host "`n--- Key related directories ---" -ForegroundColor Yellow
$related = @(
    "..\claude-code\azure-hermes-factory",
    "..\..\Downloads\oc-agent-main\oc-agent-main"
)
foreach ($r in $related) {
    $full = Resolve-Path $r -ErrorAction SilentlyContinue
    if ($full) {
        Write-Host "Found: $full"
    } else {
        Write-Host "Not found at expected location: $r"
    }
}

Write-Host "`n--- Git status ---" -ForegroundColor Yellow
git status --short

Write-Host "`n--- Recent commits ---" -ForegroundColor Yellow
git log --oneline -5

Write-Host "`n=== End of context dump. Now read full AGENTS.md and explore. ===" -ForegroundColor Green
