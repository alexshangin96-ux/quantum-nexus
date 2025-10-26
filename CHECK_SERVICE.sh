#!/bin/bash
# Check service configuration

echo "=== Checking quantum-nexus-web service ==="
sudo systemctl status quantum-nexus-web --no-pager

echo ""
echo "=== Service file content ==="
sudo cat /etc/systemd/system/quantum-nexus-web.service

echo ""
echo "=== Checking web_server.py ==="
ls -lh /root/quantum-nexus/web_server.py

echo ""
echo "=== Checking Python path ==="
which python3

echo ""
echo "=== Testing web_server.py ==="
cd /root/quantum-nexus
python3 -c "import web_server; print('✅ web_server.py imports successfully')"
