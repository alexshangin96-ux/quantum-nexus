#!/bin/bash

echo "🔄 Принудительное обновление магазина валюты..."

cd /root/quantum-nexus

echo "📥 Получение изменений..."
git fetch origin
git reset --hard origin/main

echo "📁 Копирование web_app.html..."
cp web_app.html /var/www/quantum-nexus/
chmod 644 /var/www/quantum-nexus/web_app.html

echo "🔄 Перезапуск сервисов..."
systemctl restart quantum-nexus-web.service

echo "✅ Обновление завершено!"
echo "📊 Статус сервиса:"
systemctl status quantum-nexus-web.service --no-pager -l

echo "📋 Проверка файла:"
ls -lh /var/www/quantum-nexus/web_app.html | head -1

