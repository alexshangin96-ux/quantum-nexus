#!/bin/bash

echo "🔧 Обновление сервера Quantum Nexus..."

cd /root/quantum-nexus

echo "📥 Загрузка изменений из GitHub..."
git pull origin main

echo "📋 Копирование web_app.html..."
cp /root/quantum-nexus/web_app.html /var/www/quantum-nexus/web_app.html

echo "🔄 Перезапуск сервиса..."
systemctl restart quantum-nexus-web.service

echo "✅ Готово!"
echo ""
echo "📱 Теперь откройте бота и напишите /start"







