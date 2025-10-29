#!/bin/bash
# Complete server restart with all fixes

cd /root/quantum-nexus

echo "=== 1. Updating code from GitHub ==="
git fetch origin
git reset --hard origin/main
git clean -fd

echo ""
echo "=== 2. Checking files ==="
ls -lh *.py *.html

echo ""
echo "=== 3. Restarting services ==="
sudo systemctl stop quantum-nexus-web
sleep 2
sudo systemctl start quantum-nexus-web
sudo systemctl enable quantum-nexus-web

echo ""
echo "=== 4. Checking service status ==="
sudo systemctl status quantum-nexus-web --no-pager | head -20

echo ""
echo "=== 5. Recent logs ==="
sudo journalctl -u quantum-nexus-web -n 50 --no-pager

echo ""
echo "✅ Server restarted!"
echo "Visit: https://quantum-nexus.ru/admin"


