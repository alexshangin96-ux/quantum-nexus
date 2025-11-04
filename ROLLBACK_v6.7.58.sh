#!/bin/bash

# Quantum Nexus v6.7.58 - Full Rollback Script
# Rollback to stable version before recent issues
# Commit: 8d8ebf3 (fix: Complete daily tasks fixes v6.7.58)
# Date: 2025-11-05

echo "=================================================="
echo "Quantum Nexus v6.7.58 - FULL ROLLBACK"
echo "=================================================="
echo ""
echo "⚠️  WARNING: This will revert to commit 8d8ebf3"
echo "   All changes after v6.7.58 will be lost!"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Step 1: Navigate to project directory
echo ""
echo "Step 1: Navigating to project directory..."
cd /root/quantum-nexus || exit 1

# Step 2: Backup current version (before rollback)
echo ""
echo "Step 2: Creating backup of current state..."
BACKUP_DIR="/root/quantum-nexus-backup-before-rollback-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r web_app.html web_server.py handlers.py bot.py models.py "$BACKUP_DIR/" 2>/dev/null
echo "✅ Backup created: $BACKUP_DIR"

# Step 3: Fetch latest from GitHub
echo ""
echo "Step 3: Fetching latest from GitHub..."
git fetch origin
if [ $? -eq 0 ]; then
    echo "✅ Fetched successfully"
else
    echo "❌ Git fetch failed!"
    exit 1
fi

# Step 4: Reset to v6.7.58 commit
echo ""
echo "Step 4: Resetting to commit 8d8ebf3 (v6.7.58)..."
if git reset --hard 8d8ebf3; then
    echo "✅ Reset to v6.7.58 successful"
else
    echo "❌ Git reset failed!"
    exit 1
fi

# Step 5: Force push to remote (optional - uncomment if needed)
echo ""
echo "Step 5: Force pushing to remote..."
read -p "Force push to origin/main? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if git push origin main --force; then
        echo "✅ Force pushed to remote"
    else
        echo "⚠️  Force push failed (may need manual push)"
    fi
else
    echo "⏭️  Skipped force push"
fi

# Step 6: Copy files to production locations
echo ""
echo "Step 6: Copying rolled-back files to production..."

# Web app HTML
if sudo cp web_app.html /var/www/quantum-nexus/web_app.html; then
    echo "  ✅ web_app.html copied"
else
    echo "  ❌ Failed to copy web_app.html"
    exit 1
fi

# Python files
if sudo cp web_server.py /root/quantum-nexus/web_server.py; then
    echo "  ✅ web_server.py copied"
else
    echo "  ❌ Failed to copy web_server.py"
    exit 1
fi

if sudo cp handlers.py /root/quantum-nexus/handlers.py; then
    echo "  ✅ handlers.py copied"
else
    echo "  ❌ Failed to copy handlers.py"
    exit 1
fi

if sudo cp bot.py /root/quantum-nexus/bot.py; then
    echo "  ✅ bot.py copied"
else
    echo "  ❌ Failed to copy bot.py"
    exit 1
fi

# Step 7: Restart services
echo ""
echo "Step 7: Restarting services..."

echo "  - Restarting quantum-nexus-web.service..."
if sudo systemctl restart quantum-nexus-web.service; then
    echo "    ✅ Web service restarted"
    sleep 2
else
    echo "    ❌ Failed to restart web service"
    exit 1
fi

echo "  - Restarting quantum-nexus.service..."
if sudo systemctl restart quantum-nexus.service; then
    echo "    ✅ Bot service restarted"
    sleep 2
else
    echo "    ❌ Failed to restart bot service"
    exit 1
fi

# Step 8: Check service status
echo ""
echo "Step 8: Checking service status..."
echo ""

echo "=== quantum-nexus-web.service ==="
sudo systemctl status quantum-nexus-web.service --no-pager -l | head -20
echo ""

echo "=== quantum-nexus.service ==="
sudo systemctl status quantum-nexus.service --no-pager -l | head -20
echo ""

# Step 9: Verify rollback
echo ""
echo "Step 9: Verifying rollback..."
CURRENT_COMMIT=$(git rev-parse HEAD)
if [ "$CURRENT_COMMIT" = "8d8ebf3" ]; then
    echo "✅ Confirmed: Rolled back to commit 8d8ebf3"
else
    echo "⚠️  Warning: Current commit is $CURRENT_COMMIT (expected 8d8ebf3)"
fi

# Step 10: Summary
echo ""
echo "=================================================="
echo "✅ v6.7.58 ROLLBACK COMPLETED!"
echo "=================================================="
echo ""
echo "Reverted to:"
echo "  Commit: 8d8ebf3"
echo "  Version: v6.7.58"
echo "  Message: fix: Complete daily tasks fixes v6.7.58"
echo ""
echo "What was rolled back:"
echo "  ❌ Recent JSON parsing error handling (was causing issues)"
echo "  ❌ Recent mining machine display fixes (was causing issues)"
echo "  ✅ Back to stable daily tasks system"
echo "  ✅ Working mining system"
echo ""
echo "Backup Location: $BACKUP_DIR"
echo ""
echo "Next Steps:"
echo "  1. Test daily tasks loading"
echo "  2. Test mining machine purchase"
echo "  3. Test user profile loading"
echo "  4. Monitor logs: journalctl -u quantum-nexus-web.service -f"
echo ""
echo "To restore from backup:"
echo "  cp $BACKUP_DIR/* /root/quantum-nexus/"
echo ""
echo "=================================================="
