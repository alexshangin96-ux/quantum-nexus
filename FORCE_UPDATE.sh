#!/bin/bash
# Полное обновление Quantum Nexus на сервере

echo "🔧 Обновление Quantum Nexus..."

# Перейти в директорию проекта
cd /root/quantum-nexus

# Получить последние изменения
echo "📥 Получение изменений из Git..."
git fetch origin
git reset --hard origin/main
git pull origin main

# Скопировать веб-приложение
echo "📁 Обновление веб-приложения..."
cp web_app.html /var/www/quantum-nexus/
chmod 644 /var/www/quantum-nexus/web_app.html

# Перезапустить сервисы
echo "🔄 Перезапуск сервисов..."
systemctl restart quantum-nexus-bot
systemctl restart quantum-nexus-web

# Проверить статус
echo "✅ Проверка статуса..."
systemctl status quantum-nexus-bot --no-pager -l
systemctl status quantum-nexus-web --no-pager -l

echo ""
echo "✅ Обновление завершено!"
echo ""
echo "📝 Проверьте логи бота:"
echo "   journalctl -u quantum-nexus-bot -f"
echo ""
echo "📝 Проверьте логи веб-сервера:"
echo "   journalctl -u quantum-nexus-web -f"
