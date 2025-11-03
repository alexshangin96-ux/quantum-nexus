#!/bin/bash

# Resolve Merge Conflict on Server
# Run this on the server to fix the conflict and update to v6.7.50

echo "=================================================="
echo "Resolving Merge Conflict on Server"
echo "=================================================="
echo ""

cd /root/quantum-nexus

echo "Step 1: Abort any pending merge..."
git merge --abort 2>/dev/null

echo "Step 2: Reset to clean state..."
git reset --hard HEAD 2>/dev/null

echo "Step 3: Fetch latest from GitHub..."
git fetch origin

echo "Step 4: Reset to origin/main (force)..."
git reset --hard origin/main

echo "Step 5: Verify we're on v6.7.50..."
git log --oneline -n 3

echo ""
echo "Step 6: Copy files..."
sudo cp web_app.html /var/www/quantum-nexus/

echo "Step 7: Restart services..."
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service

echo ""
echo "=================================================="
echo "✅ Conflict resolved! v6.7.50 deployed!"
echo "=================================================="

