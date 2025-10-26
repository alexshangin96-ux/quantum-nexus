#!/bin/bash
echo "🔍 Проверка и исправление..."

# 1. Проверить наличие .env
if [ ! -f /root/quantum-nexus/.env ]; then
    echo "📝 Создаю .env файл..."
    echo "DATABASE_URL=postgresql://quantum:quantum123@localhost:5432/quantum_nexus" > /root/quantum-nexus/.env
fi

# 2. Скопировать файлы
echo "📋 Копирую файлы..."
cp /root/quantum-nexus/web_server.py /var/www/quantum-nexus/
cp /root/quantum-nexus/admin.html /var/www/quantum-nexus/
cp /root/quantum-nexus/handlers.py /root/quantum-nexus/
cp /root/quantum-nexus/keyboards.py /root/quantum-nexus/

# 3. Установить правильные права
chown -R www-data:www-data /var/www/quantum-nexus/

# 4. Перезапустить сервисы
echo "🔄 Перезапуск сервисов..."
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web

echo "✅ Готово!"
echo ""
echo "Проверьте:"
echo "sudo systemctl status quantum-nexus-web"
