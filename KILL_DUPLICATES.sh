#!/bin/bash
# Убить все дублирующиеся процессы бота

echo "🔪 УДАЛЕНИЕ ДУБЛИРУЮЩИХСЯ ПРОЦЕССОВ БОТА"
echo "========================================="
echo ""

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "1️⃣ Найти все процессы Python с bot.py:"
echo "----------------------------------------"
ps aux | grep -E "bot.py|web_server.py" | grep -v grep

echo ""
echo "2️⃣ Убить все процессы:"
echo "----------------------------------------"
sudo pkill -f "bot.py"
sudo pkill -f "web_server.py"
sleep 2

echo ""
echo "3️⃣ Проверить что все остановлено:"
echo "----------------------------------------"
ps aux | grep -E "bot.py|web_server.py" | grep -v grep

echo ""
echo "4️⃣ Остановить systemd сервисы:"
echo "----------------------------------------"
sudo systemctl stop quantum-nexus
sudo systemctl stop quantum-nexus-web.service
sleep 1

echo ""
echo "5️⃣ Запустить сервисы заново:"
echo "----------------------------------------"
sudo systemctl start quantum-nexus-web.service
sleep 2
sudo systemctl start quantum-nexus

echo ""
echo "6️⃣ Проверить статус:"
echo "----------------------------------------"
sudo systemctl status quantum-nexus --no-pager | head -15

echo ""
echo "========================================="
echo -e "${GREEN}✅ ГОТОВО${NC}"
echo "========================================="





