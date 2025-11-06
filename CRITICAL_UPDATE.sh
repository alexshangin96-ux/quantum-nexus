#!/bin/bash

echo "🔴 КРИТИЧЕСКОЕ ОБНОВЛЕНИЕ МАГАЗИНА ВАЛЮТЫ"
echo "=========================================="

cd /root/quantum-nexus

echo "📥 Получение ВСЕХ изменений..."
git fetch --all
git reset --hard origin/main

echo "📋 ПРОВЕРКА: Что в web_app.html?"
head -n 3 web_app.html

echo "🔄 Полная перезагрузка сервиса..."
systemctl stop quantum-nexus-web.service
sleep 2
systemctl start quantum-nexus-web.service
systemctl status quantum-nexus-web.service --no-pager -l

echo ""
echo "✅ ОБНОВЛЕНО! Откройте /start в боте заново"










