#!/bin/bash

echo "=== ПОЛНОЕ ОБНОВЛЕНИЕ QUANTUM NEXUS ==="

cd /root/quantum-nexus

echo "1. Остановка сервисов..."
sudo systemctl stop quantum-nexus
sudo systemctl stop quantum-nexus-web

echo "2. Очистка локальных изменений..."
git reset --hard HEAD
git clean -fd

echo "3. Pull последних изменений..."
git pull origin main

echo "4. Копирование web_app.html в /var/www/quantum-nexus/"
sudo cp web_app.html /var/www/quantum-nexus/web_app.html

echo "5. Установка прав..."
sudo chmod 644 /var/www/quantum-nexus/web_app.html

echo "6. Генерация ботов (если нужно)..."
source venv/bin/activate
python3 generate_bot_users.py

echo "7. Перезапуск сервисов..."
sudo systemctl start quantum-nexus
sudo systemctl start quantum-nexus-web

echo "8. Проверка статуса..."
sudo systemctl status quantum-nexus --no-pager | head -10
sudo systemctl status quantum-nexus-web --no-pager | head -10

echo "=== ОБНОВЛЕНИЕ ЗАВЕРШЕНО ==="

