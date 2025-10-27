#!/bin/bash

echo "🔄 Принудительное обновление магазина валюты..."

cd /root/quantum-nexus

echo "📥 Получение изменений..."
git fetch origin
git reset --hard origin/main

echo "🔄 Перезапуск сервисов..."
systemctl restart quantum-nexus-web.service

echo "✅ Обновление завершено!"
echo "📊 Статус сервиса:"
systemctl status quantum-nexus-web.service --no-pager -l

