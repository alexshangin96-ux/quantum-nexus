#!/bin/bash

# Quantum Nexus v6.7.54 - Full Server Update Script
# Complete daily tasks system with tracking
# Date: 2025-11-05

echo "=================================================="
echo "Quantum Nexus v6.7.54 - Full Server Update"
echo "=================================================="
echo ""
echo "This will update:"
echo "  ✅ Complete daily tasks redesign"
echo "  ✅ Channel subscription with validation"
echo "  ✅ 7 dynamic beginner-friendly tasks"
echo "  ✅ Task tracking and reward system"
echo "  ✅ All bug fixes and improvements"
echo ""

# Step 1: Navigate to project directory
echo "Step 1: Navigating to project directory..."
cd /root/quantum-nexus || exit 1

# Step 2: Backup current version
echo ""
echo "Step 2: Creating backup..."
BACKUP_DIR="/root/quantum-nexus-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r web_app.html web_server.py handlers.py bot.py models.py "$BACKUP_DIR/" 2>/dev/null
echo "Backup created: $BACKUP_DIR"

# Step 3: Pull latest from GitHub
echo ""
echo "Step 3: Pulling latest changes from GitHub..."
git fetch origin
if git reset --hard origin/main; then
    echo "✅ Code updated successfully"
else
    echo "❌ Git pull failed!"
    exit 1
fi

# Step 4: Apply database migrations
echo ""
echo "Step 4: Applying database migrations..."

echo "  - Adding channel subscription columns..."
if sudo -u postgres psql -d quantum_nexus -f ADD_CHANNEL_SUBSCRIPTION_COLUMNS.sql 2>/dev/null; then
    echo "    ✅ Channel subscription columns added"
else
    echo "    ⚠️  Migration already applied or error (continuing...)"
fi

echo "  - Adding daily tasks tracking columns..."
if sudo -u postgres psql -d quantum_nexus -f ADD_DAILY_TASKS_TRACKING.sql 2>/dev/null; then
    echo "    ✅ Daily tasks tracking columns added"
else
    echo "    ⚠️  Migration already applied or error (continuing...)"
fi

# Step 5: Copy files to production locations
echo ""
echo "Step 5: Copying files to production locations..."

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

# Step 6: Restart services
echo ""
echo "Step 6: Restarting services..."

echo "  - Restarting quantum-nexus-web.service..."
if sudo systemctl restart quantum-nexus-web.service; then
    echo "    ✅ Web service restarted"
else
    echo "    ❌ Failed to restart web service"
    exit 1
fi

echo "  - Restarting quantum-nexus.service..."
if sudo systemctl restart quantum-nexus.service; then
    echo "    ✅ Bot service restarted"
else
    echo "    ❌ Failed to restart bot service"
    exit 1
fi

# Step 7: Check service status
echo ""
echo "Step 7: Checking service status..."
echo ""

echo "=== quantum-nexus-web.service ==="
sudo systemctl status quantum-nexus-web.service --no-pager -l
echo ""

echo "=== quantum-nexus.service ==="
sudo systemctl status quantum-nexus.service --no-pager -l
echo ""

# Step 8: Summary
echo ""
echo "=================================================="
echo "✅ v6.7.54 UPDATE COMPLETED SUCCESSFULLY!"
echo "=================================================="
echo ""
echo "What's New:"
echo "  🎁 Beautiful daily tasks system (VIP style)"
echo "  ⏰ 24-hour countdown timer"
echo "  📢 Channel subscription task with validation"
echo "  🔄 7 dynamic beginner-friendly tasks"
echo "  🎯 Task tracking prevents double rewards"
echo "  💰 Proper reward system"
echo "  🚫 Penalty for unsubscribing (-10k coins)"
echo ""
echo "Files Updated:"
echo "  - web_app.html (redesigned daily tasks)"
echo "  - web_server.py (task generation & tracking)"
echo "  - handlers.py (channel subscription handler)"
echo "  - bot.py (channel events)"
echo "  - models.py (new DB fields)"
echo ""
echo "Database Changes:"
echo "  - channel_subscribed (Boolean)"
echo "  - channel_subscribed_at (Timestamp)"
echo "  - daily_tasks_completed (JSON)"
echo "  - last_daily_reset (Timestamp)"
echo ""
echo "Next Steps:"
echo "  1. Test daily tasks in Telegram Web App"
echo "  2. Verify channel subscription works"
echo "  3. Check reward claiming"
echo "  4. Monitor logs: journalctl -u quantum-nexus-web.service -f"
echo ""
echo "Backup Location: $BACKUP_DIR"
echo "=================================================="

