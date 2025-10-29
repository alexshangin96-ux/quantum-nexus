#!/bin/bash
# Обновление только веб-приложения (без системных сервисов)

echo "🌐 Обновление веб-приложения..."

cd ~/quantum-nexus

# Обновить код
git pull origin main

# Скопировать обновленный web_app.html в веб-директорию
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo chmod 644 /var/www/quantum-nexus/web_app.html

# Если есть admin.html
if [ -f "admin.html" ]; then
    sudo cp admin.html /var/www/quantum-nexus/admin.html
    sudo chmod 644 /var/www/quantum-nexus/admin.html
fi

# Перезапустить веб-сервер Flask (если есть процесс)
pkill -f "python.*web_server.py" || true
sleep 2

# Запустить веб-сервер в фоне
nohup python3 web_server.py > /dev/null 2>&1 &

echo "✅ Веб-приложение обновлено!"
echo "📋 Проверьте: http://your-server:5000"



