#!/bin/bash
# ФИНАЛЬНОЕ ОБНОВЛЕНИЕ - Полная замена всех файлов

echo "🚀 ФИНАЛЬНОЕ ОБНОВЛЕНИЕ"
echo "========================================="
echo ""

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Обновляем Git
echo "1️⃣ Получение последних изменений..."
cd /root/quantum-nexus
git fetch origin
git reset --hard origin/main
git pull origin main

# 2. Проверка версии файлов
echo ""
echo "2️⃣ Проверка версий:"
echo "web_app.html:"
head -n 2 web_app.html | grep -o "v[0-9]\.[0-9]"

echo "handlers.py URL:"
grep -o "web_app.html[^\"]*" handlers.py | head -1

# 3. Копируем ВСЕ файлы в веб-директорию
echo ""
echo "3️⃣ Копирование файлов..."
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo cp handlers.py /var/www/quantum-nexus/handlers.py
sudo cp web_server.py /var/www/quantum-nexus/web_server.py

# 4. Перезапускаем ВСЕ сервисы
echo ""
echo "4️⃣ Перезапуск всех сервисов..."
sudo systemctl restart quantum-nexus-web.service
sleep 2
sudo systemctl restart quantum-nexus.service
sleep 2
sudo systemctl restart nginx 2>/dev/null || sudo systemctl restart caddy 2>/dev/null || true

# 5. Проверка
echo ""
echo "5️⃣ Проверка статуса..."
sudo systemctl status quantum-nexus-web.service --no-pager | grep -E "Active:|Main PID:"
sudo systemctl status quantum-nexus.service --no-pager | grep -E "Active:|Main PID:"

echo ""
echo "========================================="
echo -e "${GREEN}✅ ГОТОВО!${NC}"
echo "========================================="
echo ""
echo "Теперь:"
echo "1. Перезапустите Telegram (полностью закройте и откройте)"
echo "2. В боте нажмите /start и откройте игру"
echo "3. Проверьте что категории обновились"

