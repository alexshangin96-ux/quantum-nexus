#!/bin/bash

# Скрипт для обновления Quantum Nexus на сервере

echo "🚀 Начинаем обновление Quantum Nexus..."

# 1. Обновить код
echo "📥 Обновляю код из GitHub..."
cd /root/quantum-nexus
git pull origin main

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

