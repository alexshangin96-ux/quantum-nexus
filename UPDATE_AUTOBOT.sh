#!/bin/bash
# Обновление с добавлением автобота таймера

echo "🤖 Обновление автобота..."

cd ~/quantum-nexus

# Обновить код
git pull origin main

# Выполнить миграцию базы данных
sudo -u postgres psql -d quantum_nexus -f ADD_AUTOBOT_EXPIRES.sql

# Скопировать обновленные файлы
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo cp web_server.py /root/quantum-nexus/web_server.py

# Перезапустить сервисы
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service

echo "✅ Обновление завершено!"

