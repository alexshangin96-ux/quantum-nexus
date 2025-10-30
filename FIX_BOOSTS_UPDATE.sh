#!/bin/bash
# Команды для обновления с исправлением бустов и автобота

echo "🔧 Обновляю код с исправлением бустов и автобота..."

cd ~/quantum-nexus

# Обновить код
git pull origin main

# Перезапустить веб-сервер
sudo systemctl restart quantum-web-server
sudo systemctl status quantum-web-server

# Перезапустить бота
sudo systemctl restart quantum-bot
sudo systemctl status quantum-bot

# Проверить логи
echo "📋 Проверьте логи веб-сервера:"
sudo journalctl -u quantum-web-server -n 30 --no-pager

echo "✅ Обновление выполнено!"






