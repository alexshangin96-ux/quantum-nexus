#!/bin/bash
# Проверить URL в handlers.py файлах

echo "🔍 ПРОВЕРКА URL В handlers.py"
echo "========================================="
echo ""

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "1️⃣ handlers.py в /root/quantum-nexus/handlers.py:"
echo "----------------------------------------"
grep -A2 "InlineKeyboardButton.*web_app" /root/quantum-nexus/handlers.py 2>/dev/null || echo "Не найден"

echo ""
echo "2️⃣ handlers.py в /var/www/quantum-nexus/handlers.py:"
echo "----------------------------------------"
grep -A2 "InlineKeyboardButton.*web_app" /var/www/quantum-nexus/handlers.py 2>/dev/null || echo "Не найден"

echo ""
echo "3️⃣ Проверка web_server.py маршрутов:"
echo "----------------------------------------"
grep -A2 "@app.route" /root/quantum-nexus/web_server.py 2>/dev/null | head -15

echo ""
echo "4️⃣ Статус системы:"
echo "----------------------------------------"
systemctl status quantum-nexus --no-pager | grep -E "Active:|Main PID:"

echo ""
echo "========================================="


