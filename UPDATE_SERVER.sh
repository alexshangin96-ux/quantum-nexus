#!/bin/bash
# Скрипт обновления Quantum Nexus на сервере Selectel

echo "🚀 Начинаем обновление Quantum Nexus..."

# Переходим в директорию проекта
cd /root/quantum-nexus || { echo "❌ Директория не найдена!"; exit 1; }

# Получаем последние изменения из GitHub
echo "📥 Получаем последние изменения..."
git pull origin main || { echo "❌ Ошибка получения изменений!"; exit 1; }

# Копируем обновленный файл админ-панели
echo "📋 Копируем админ-панель..."
cp admin.html /var/www/quantum-nexus/ || { echo "❌ Ошибка копирования!"; exit 1; }

# Перезапускаем веб-сервер
echo "🔄 Перезапускаем веб-сервер..."
systemctl restart quantum-nexus-web || { echo "❌ Ошибка перезапуска!"; exit 1; }

# Проверяем статус
echo "✅ Проверяем статус..."
sleep 2
systemctl status quantum-nexus-web

echo ""
echo "✨ Обновление завершено успешно!"
echo "📊 Админ-панель: https://quantum-nexus.ru/admin"
