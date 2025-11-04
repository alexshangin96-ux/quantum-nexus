#!/bin/bash

# Quantum Nexus - Update Script
# Date: 2025-11-05
# Fix: Daily tasks modal not opening

echo "=================================================="
echo "Quantum Nexus - Fix: Daily Tasks Modal"
echo "=================================================="
echo ""
echo "This will fix:"
echo "  ✅ Error handling in openDailyBonus"
echo "  ✅ Safety checks for modal creation"
echo "  ✅ Better error messages"
echo ""

cd /root/quantum-nexus || exit 1

# Backup
BACKUP_DIR="/root/quantum-nexus-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r web_app.html "$BACKUP_DIR/" 2>/dev/null
echo "✅ Backup created: $BACKUP_DIR"

# Update
git merge --abort 2>/dev/null
git reset --hard HEAD
git fetch origin
git pull origin main

# Copy to production
sudo cp web_app.html /var/www/quantum-nexus/web_app.html

# Restart
sudo systemctl restart quantum-nexus-web.service

echo ""
echo "✅ Update complete!"
echo "Backup: $BACKUP_DIR"
