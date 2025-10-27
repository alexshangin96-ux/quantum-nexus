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

# 2. Обновить файлы
echo "📋 Копирую файлы..."
cp web_app.html /var/www/quantum-nexus/
cp admin.html /var/www/quantum-nexus/
cp web_server.py /root/quantum-nexus/
cp models.py /root/quantum-nexus/

# 3. Обновить базу данных
echo "🗄️ Обновляю базу данных..."
sudo -u postgres psql -d quantum_nexus -c "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_passive_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
sudo -u postgres psql -d quantum_nexus -c "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_hash_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"

# 4. Перезапустить сервисы
echo "🔄 Перезапускаю сервисы..."
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
sudo systemctl restart nginx

# 5. Проверить статус
echo "✅ Проверяю статус..."
sudo systemctl status quantum-nexus --no-pager -l
sudo systemctl status quantum-nexus-web --no-pager -l
sudo systemctl status nginx --no-pager -l

echo "🎉 Обновление завершено!"

