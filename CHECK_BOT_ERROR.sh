#!/bin/bash
# Проверка ошибки бота

echo "🔍 ПРОВЕРКА ОШИБКИ БОТА"
echo "========================================="
echo ""

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "1️⃣ Логи бота (последние 50 строк):"
echo "----------------------------------------"
sudo journalctl -u quantum-nexus -n 50 --no-pager

echo ""
echo "2️⃣ Попытка запустить бота вручную:"
echo "----------------------------------------"
cd /root/quantum-nexus
source venv/bin/activate
python bot.py 2>&1 | head -20

echo ""
echo "3️⃣ Проверка файлов:"
echo "----------------------------------------"
ls -lh handlers.py web_server.py web_app.html bot.py 2>/dev/null

echo ""
echo "4️⃣ Проверка зависимостей:"
echo "----------------------------------------"
cd /root/quantum-nexus
source venv/bin/activate 2>/dev/null
python -c "import telegram; print('telegram OK')" 2>&1
python -c "import flask; print('flask OK')" 2>&1
python -c "import sqlalchemy; print('sqlalchemy OK')" 2>&1

echo ""
echo "========================================="
echo -e "${YELLOW}Если видите ошибку - скопируйте её${NC}"
echo "========================================="

