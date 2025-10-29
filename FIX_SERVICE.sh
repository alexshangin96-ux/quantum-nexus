#!/bin/bash
# Fix the service and check logs

echo "=== Viewing recent logs ==="
sudo journalctl -u quantum-nexus-web -n 100 --no-pager | tail -30

echo ""
echo "=== Checking if web_server.py runs ==="
cd /root/quantum-nexus
/usr/bin/python3 -c "import sys; print(sys.path)"

echo ""
echo "=== Testing imports ==="
/usr/bin/python3 -c "from flask import Flask; print('✅ Flask OK')" 2>&1 || echo "❌ Flask missing"
/usr/bin/python3 -c "from database import get_db; print('✅ database OK')" 2>&1 || echo "❌ database error"

echo ""
echo "=== If Flask missing, installing dependencies ==="
if ! /usr/bin/python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install flask flask-cors sqlalchemy psycopg2-binary
fi

echo ""
echo "=== Testing web_server.py directly ==="
timeout 5 /usr/bin/python3 /root/quantum-nexus/web_server.py 2>&1 || echo "Script exits"


