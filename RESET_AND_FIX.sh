#!/bin/bash
# Откатить локальные изменения и исправить

echo "🔄 ОТКАТ И ИСПРАВЛЕНИЕ"
echo "========================================="
echo ""

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd /root/quantum-nexus

echo "1️⃣ Откат локальных изменений..."
git restore FIX_ALL_SYNTAX.sh
echo -e "${GREEN}✅ Откат выполнен${NC}"

echo ""
echo "2️⃣ Получение последних изменений..."
git pull origin main
echo -e "${GREEN}✅ Обновление получено${NC}"

echo ""
echo "3️⃣ Проверка синтаксиса..."
source venv/bin/activate
python -m py_compile web_server.py 2>&1
exit_code=$?
deactivate

if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}✅ Синтаксис OK${NC}"
    
    echo ""
    echo "4️⃣ Копирование файла..."
    sudo cp web_server.py /var/www/quantum-nexus/web_server.py
    
    echo ""
    echo "5️⃣ Перезапуск сервиса..."
    sudo systemctl restart quantum-nexus-web.service
    sleep 3
    
    echo ""
    echo "6️⃣ Проверка статуса..."
    sudo systemctl status quantum-nexus-web.service --no-pager | grep -E "Active:|Main PID:"
    
    echo ""
    echo "========================================="
    echo -e "${GREEN}✅ ВСЁ ИСПРАВЛЕНО И ЗАПУЩЕНО!${NC}"
    echo "========================================="
else
    echo -e "${RED}❌ ОШИБКИ СИНТАКСИСА${NC}"
    echo "Скопируйте сообщение об ошибке выше"
fi


