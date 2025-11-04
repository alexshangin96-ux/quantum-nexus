# Quantum Nexus v6.7.58 - Full Rollback Script (PowerShell)
# Rollback to stable version before recent issues
# Commit: 8d8ebf3 (fix: Complete daily tasks fixes v6.7.58)
# Date: 2025-11-05

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Quantum Nexus v6.7.58 - FULL ROLLBACK" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  WARNING: This will revert to commit 8d8ebf3" -ForegroundColor Yellow
Write-Host "   All changes after v6.7.58 will be lost!" -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Press Enter to continue or Ctrl+C to cancel"

# Step 1: Navigate to project directory
Write-Host ""
Write-Host "Step 1: Navigating to project directory..." -ForegroundColor Green
$projectPath = "c:\Users\SmartFix\Desktop\qwantum 2.0\quantum-nexus"
if (Test-Path $projectPath) {
    Set-Location $projectPath
    Write-Host "✅ In project directory" -ForegroundColor Green
} else {
    Write-Host "❌ Project directory not found: $projectPath" -ForegroundColor Red
    exit 1
}

# Step 2: Backup current version (before rollback)
Write-Host ""
Write-Host "Step 2: Creating backup of current state..." -ForegroundColor Green
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = "quantum-nexus-backup-before-rollback-$timestamp"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

$filesToBackup = @("web_app.html", "web_server.py", "handlers.py", "bot.py", "models.py")
foreach ($file in $filesToBackup) {
    if (Test-Path $file) {
        Copy-Item $file -Destination "$backupDir\$file" -Force
        Write-Host "  ✅ Backed up $file" -ForegroundColor Green
    }
}
Write-Host "✅ Backup created: $backupDir" -ForegroundColor Green

# Step 3: Fetch latest from GitHub
Write-Host ""
Write-Host "Step 3: Fetching latest from GitHub..." -ForegroundColor Green
try {
    git fetch origin
    Write-Host "✅ Fetched successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Git fetch failed!" -ForegroundColor Red
    exit 1
}

# Step 4: Reset to v6.7.58 commit
Write-Host ""
Write-Host "Step 4: Resetting to commit 8d8ebf3 (v6.7.58)..." -ForegroundColor Green
try {
    git reset --hard 8d8ebf3
    Write-Host "✅ Reset to v6.7.58 successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Git reset failed!" -ForegroundColor Red
    exit 1
}

# Step 5: Force push to remote (optional)
Write-Host ""
Write-Host "Step 5: Force pushing to remote..." -ForegroundColor Green
$push = Read-Host "Force push to origin/main? (y/N)"
if ($push -eq "y" -or $push -eq "Y") {
    try {
        git push origin main --force
        Write-Host "✅ Force pushed to remote" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Force push failed (may need manual push)" -ForegroundColor Yellow
    }
} else {
    Write-Host "⏭️  Skipped force push" -ForegroundColor Yellow
}

# Step 6: Verify rollback
Write-Host ""
Write-Host "Step 6: Verifying rollback..." -ForegroundColor Green
$currentCommit = git rev-parse HEAD
if ($currentCommit -eq "8d8ebf3") {
    Write-Host "✅ Confirmed: Rolled back to commit 8d8ebf3" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: Current commit is $currentCommit (expected 8d8ebf3)" -ForegroundColor Yellow
}

# Step 7: Summary
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "✅ v6.7.58 ROLLBACK COMPLETED!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Reverted to:" -ForegroundColor White
Write-Host "  Commit: 8d8ebf3" -ForegroundColor White
Write-Host "  Version: v6.7.58" -ForegroundColor White
Write-Host "  Message: fix: Complete daily tasks fixes v6.7.58" -ForegroundColor White
Write-Host ""
Write-Host "What was rolled back:" -ForegroundColor White
Write-Host "  ❌ Recent JSON parsing error handling (was causing issues)" -ForegroundColor Red
Write-Host "  ❌ Recent mining machine display fixes (was causing issues)" -ForegroundColor Red
Write-Host "  ✅ Back to stable daily tasks system" -ForegroundColor Green
Write-Host "  ✅ Working mining system" -ForegroundColor Green
Write-Host ""
Write-Host "Backup Location: $backupDir" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor White
Write-Host "  1. Run server rollback script: ROLLBACK_v6.7.58.sh" -ForegroundColor White
Write-Host "  2. Test daily tasks loading on server" -ForegroundColor White
Write-Host "  3. Test mining machine purchase" -ForegroundColor White
Write-Host "  4. Test user profile loading" -ForegroundColor White
Write-Host ""
Write-Host "To restore from backup:" -ForegroundColor White
Write-Host "  Copy files from $backupDir back to quantum-nexus/" -ForegroundColor White
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
