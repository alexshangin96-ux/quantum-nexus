#!/bin/bash
# Test app endpoints

echo "=== Testing web app endpoints ==="

echo ""
echo "Testing /api/user_data:"
curl -X POST http://localhost:5000/api/user_data \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123}' \
  2>/dev/null | python3 -m json.tool || echo "❌ Error"

echo ""
echo "Testing /api/tap:"
curl -X POST http://localhost:5000/api/tap \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123}' \
  2>/dev/null | python3 -m json.tool || echo "❌ Error"

echo ""
echo "=== Recent logs ==="
sudo journalctl -u quantum-nexus-web -n 20 --no-pager










