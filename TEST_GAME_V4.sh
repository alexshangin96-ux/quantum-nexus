#!/bin/bash
# Тест доступа к game_v4.html

echo "🧪 ТЕСТ ДОСТУПНОСТИ game_v4.html"
echo "========================================="
echo ""

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "1️⃣ Тест локального доступа:"
echo "----------------------------------------"
curl -s http://localhost:5000/game_v4.html | head -n 2

echo ""
echo "2️⃣ Тест через домен:"
echo "----------------------------------------"
curl -s https://quantum-nexus.ru/game_v4.html | head -n 2

echo ""
echo "3️⃣ Проверка web_server работает:"
echo "----------------------------------------"
ps aux | grep -E "web_server.py" | grep -v grep

echo ""
echo "4️⃣ Логи web_server:"
echo "----------------------------------------"
journalctl -u quantum-nexus-web.service -n 20 --no-pager | tail -10

echo ""
echo "========================================="





