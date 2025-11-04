#!/bin/bash

# Quantum Nexus - Update Script for Channel Subscription Validation Fixes
# Date: 2025-11-05
# Version: Channel Subscription Validation Improvements

echo "=================================================="
echo "Quantum Nexus - Channel Subscription Fix Update"
echo "=================================================="
echo ""
echo "This will update:"
echo "  ✅ Real Telegram API subscription validation"
echo "  ✅ Improved UI after subscription verification"
echo "  ✅ Fixed task timer display (show after tasks load)"
echo "  ✅ Better penalty notification messages"
echo ""

# Step 1: Navigate to project directory
echo "Step 1: Navigating to project directory..."
cd /root/quantum-nexus || exit 1

# Step 2: Backup current version
echo ""
echo "Step 2: Creating backup..."
BACKUP_DIR="/root/quantum-nexus-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r web_app.html web_server.py handlers.py "$BACKUP_DIR/" 2>/dev/null
echo "✅ Backup created: $BACKUP_DIR"

# Step 3: Resolve any conflicts and pull latest
echo ""
echo "Step 3: Resolving conflicts and pulling latest changes..."

# Abort any active merge
git merge --abort 2>/dev/null

# Reset uncommitted changes
git reset --hard HEAD

# Fetch and pull latest
git fetch origin
if git pull origin main; then
    echo "✅ Code updated successfully"
else
    echo "❌ Git pull failed!"
    echo "Attempting to resolve..."
    git reset --hard origin/main
    echo "✅ Reset to origin/main"
fi

# Step 4: Copy files to production locations
echo ""
echo "Step 4: Copying files to production locations..."

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

# Step 5: Restart services
echo ""
echo "Step 5: Restarting services..."

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

# Step 6: Check service status
echo ""
echo "Step 6: Checking service status..."
echo ""

echo "=== quantum-nexus-web.service ==="
sudo systemctl status quantum-nexus-web.service --no-pager -l | head -20
echo ""

echo "=== quantum-nexus.service ==="
sudo systemctl status quantum-nexus.service --no-pager -l | head -20
echo ""

# Step 7: Verify update
echo ""
echo "Step 7: Verifying update..."
CURRENT_COMMIT=$(git rev-parse HEAD)
echo "Current commit: $CURRENT_COMMIT"
echo ""

# Step 8: Summary
echo ""
echo "=================================================="
echo "✅ UPDATE COMPLETED SUCCESSFULLY!"
echo "=================================================="
echo ""
echo "What's Updated:"
echo "  ✅ Real Telegram API subscription validation"
echo "  ✅ Tasks reload after subscription verification"
echo "  ✅ Timer shows after tasks load (not before)"
echo "  ✅ Improved penalty notifications"
echo ""
echo "Files Updated:"
echo "  - web_app.html (improved UX for subscription)"
echo "  - web_server.py (real API validation)"
echo "  - handlers.py (better penalty notifications)"
echo ""
echo "Backup Location: $BACKUP_DIR"
echo ""
echo "Next Steps:"
echo "  1. Test channel subscription verification"
echo "  2. Test penalty on unsubscribe"
echo "  3. Verify timer shows after tasks"
echo "  4. Monitor logs: journalctl -u quantum-nexus-web.service -f"
echo ""
echo "=================================================="
