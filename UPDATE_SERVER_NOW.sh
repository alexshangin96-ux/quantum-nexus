#!/bin/bash

echo "🔄 Обновление сервера..."

# Перейти в директорию проекта
cd /root/quantum-nexus

# Забрать последние изменения
echo "📥 Загрузка изменений..."
git pull origin main

# Скопировать web_app.html в рабочую директорию
echo "📋 Копирование файлов..."
cp /root/quantum-nexus/web_app.html /var/www/quantum-nexus/web_app.html

# Перезапустить сервис
echo "🔄 Перезапуск сервиса..."
systemctl restart quantum-nexus-web.service

echo "✅ Готово! Проверьте /start в боте."


