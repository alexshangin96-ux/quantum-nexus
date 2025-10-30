#!/bin/bash
# Полная проверка и исправление синтаксиса

echo "🔧 ПОЛНАЯ ПРОВЕРКА СИНТАКСИСА"
echo "========================================="
echo ""

cd /root/quantum-nexus
git pull origin main

echo "Проверка web_server.py..."
python -m py_compile web_server.py 2>&1

if [ $? -eq 0 ]; then
    echo -e "✅ Синтаксис OK"
    echo ""
    echo "Копирование файла..."
    sudo cp web_server.py /var/www/quantum-nexus/web_server.py
    
    echo "Перезапуск сервиса..."
    sudo systemctl restart quantum-nexus-web.service
    sleep 2
    
    echo "Проверка статуса..."
    sudo systemctl status quantum-nexus-web.service --no-pager | grep -E "Active:|Main PID:"
    
    echo ""
    echo "========================================="
    echo -e "✅ ГОТОВО!"
    echo "========================================="
else
    echo -e "❌ ЕСТЬ ОШИБКИ СИНТАКСИСА"
    echo "Скопируйте сообщение об ошибке выше"
fi

