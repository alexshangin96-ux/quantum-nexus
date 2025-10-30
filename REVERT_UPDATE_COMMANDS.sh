#!/bin/bash
# Команды для отката последнего обновления на сервере

echo "🔄 Откатываю последние изменения UI..."

cd ~/quantum-nexus

# Откатить web_app.html к предыдущей версии
git reset --hard HEAD~1
git pull origin main
git reset --hard origin/main

# Перезапустить веб-сервер
sudo systemctl restart quantum-web-server
sudo systemctl status quantum-web-server

# Перезапустить бота
sudo systemctl restart quantum-bot
sudo systemctl status quantum-bot

# Проверить логи
echo "📋 Проверьте логи веб-сервера:"
sudo journalctl -u quantum-web-server -n 20 --no-pager

echo "📋 Проверьте логи бота:"
sudo journalctl -u quantum-bot -n 20 --no-pager

echo "✅ Откат выполнен!"





