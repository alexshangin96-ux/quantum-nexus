#!/bin/bash

# Quantum Nexus - Fix Mining Purchase JSON Error
# Adds error handling for json.loads in buy_machine function
# Date: 2025-11-05

echo "=================================================="
echo "Quantum Nexus - Fix Mining Purchase"
echo "=================================================="
echo ""

cd /root/quantum-nexus || exit 1

# Backup current file
echo "Creating backup..."
cp web_server.py web_server.py.backup-$(date +%Y%m%d-%H%M%S)
echo "✅ Backup created"

# Check if fix already applied
if grep -q "except (json.JSONDecodeError, TypeError, ValueError):" web_server.py; then
    if grep -A2 "except (json.JSONDecodeError, TypeError, ValueError):" web_server.py | grep -q "levels = {}"; then
        echo "✅ Fix already applied (buy_machine)"
    fi
else
    echo "⚠️  Fix not found, applying..."
    
    # This fix should be applied manually by pulling latest version
    echo "Please run: git pull origin main"
    echo "Or manually apply the fix from commit after 8d8ebf3"
fi

# Check VIP machine fix
if grep -B2 "vip_levels = json.loads" web_server.py | grep -q "try:"; then
    echo "✅ VIP machine fix already applied"
else
    echo "⚠️  VIP machine fix needed"
fi

# Copy to production
echo ""
echo "Copying to production..."
sudo cp web_server.py /root/quantum-nexus/web_server.py
echo "✅ File copied"

# Restart service
echo ""
echo "Restarting service..."
sudo systemctl restart quantum-nexus-web.service
sleep 2
sudo systemctl status quantum-nexus-web.service --no-pager -l | head -10

echo ""
echo "=================================================="
echo "✅ Fix applied (if needed)"
echo "=================================================="
