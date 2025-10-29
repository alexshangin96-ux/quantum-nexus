#!/bin/bash
# Финальное обновление с исправленными бустами и автоботом

echo "🚀 Финальное обновление..."

cd ~/quantum-nexus

# Обновить код
git pull origin main

# Скопировать обновленный web_app.html
sudo cp web_app.html /var/www/quantum-nexus/

# Перезапустить веб-сервер
sudo systemctl restart quantum-web-server
sudo systemctl status quantum-web-server

# Перезапустить бота
sudo systemctl restart quantum-bot
sudo systemctl status quantum-bot

echo "✅ Обновление завершено!"
