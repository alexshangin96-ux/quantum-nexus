#!/bin/bash
# СРОЧНОЕ ИСПРАВЛЕНИЕ - Обновление файлов на правильные версии

echo "🔧 СРОЧНОЕ ИСПРАВЛЕНИЕ"
echo "========================================="
echo ""

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Обновляем Git
echo "1️⃣ Получение последних изменений из GitHub..."
cd /root/quantum-nexus
git pull origin main

# 2. Проверяем версию файлов
echo ""
echo "2️⃣ Проверка версий файлов..."
echo "web_app.html:"
head -n 2 /root/quantum-nexus/web_app.html
echo ""
echo "handlers.py URL:"
grep "web_app.html?v=" /root/quantum-nexus/handlers.py | head -1

# 3. Копируем файлы
echo ""
echo "3️⃣ Копирование файлов..."
sudo cp /root/quantum-nexus/web_app.html /var/www/quantum-nexus/web_app.html
sudo cp /root/quantum-nexus/handlers.py /var/www/quantum-nexus/handlers.py
sudo cp /root/quantum-nexus/web_server.py /var/www/quantum-nexus/web_server.py

# 4. Проверяем что скопировалось
echo ""
echo "4️⃣ Проверка скопированных файлов..."
echo "Файл на веб-сервере:"
head -n 2 /var/www/quantum-nexus/web_app.html
echo ""
echo "handlers.py на веб-сервере:"
grep "web_app.html?v=" /var/www/quantum-nexus/handlers.py 2>/dev/null | head -1 || echo "Файл не найден"

# 5. Перезапускаем сервисы
echo ""
echo "5️⃣ Перезапуск сервисов..."
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service

# 6. Проверка статуса
echo ""
echo "6️⃣ Проверка статуса сервисов..."
sudo systemctl status quantum-nexus-web.service --no-pager -l | head -15
echo ""
sudo systemctl status quantum-nexus.service --no-pager -l | head -15

echo ""
echo "========================================="
echo -e "${GREEN}✅ ИСПРАВЛЕНИЕ ЗАВЕРШЕНО${NC}"
echo "========================================="
echo ""
echo "Теперь проверьте версию на веб-сервере:"
echo "curl https://quantum-nexus.ru/web_app.html | head -n 2"





