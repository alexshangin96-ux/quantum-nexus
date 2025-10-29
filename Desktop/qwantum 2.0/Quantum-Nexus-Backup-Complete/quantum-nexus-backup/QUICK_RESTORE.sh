#!/bin/bash
# Быстрое восстановление Quantum Nexus
# Дата создания резервной копии: 29.10.2025 06:12

echo "🔄 Восстановление Quantum Nexus..."

# Остановка сервисов
echo "⏹️ Остановка сервисов..."
sudo systemctl stop quantum-nexus-web
sudo systemctl stop quantum-nexus-bot

# Создание резервной копии текущего состояния
echo "💾 Создание резервной копии текущего состояния..."
sudo cp -r /root/quantum-nexus /root/quantum-nexus-current-backup-$(date +%Y-%m-%d-%H-%M)

# Восстановление (замените путь на актуальный)
echo "📁 Восстановление файлов..."
# Раскомментируйте и отредактируйте следующую строку:
# scp -r "C:\Users\SmartFix\Desktop\qwantum 2.0\quantum-nexus-backup-2025-10-29-06-12\quantum-nexus" root@your-server-ip:/root/

# Установка прав доступа
echo "🔐 Установка прав доступа..."
cd /root/quantum-nexus
chmod +x *.sh
chmod 644 *.py *.html *.md

# Обновление веб-файлов
echo "🌐 Обновление веб-файлов..."
sudo cp web_app.html /var/www/quantum-nexus/
sudo cp admin.html /var/www/quantum-nexus/
sudo chown -R www-data:www-data /var/www/quantum-nexus/

# Перезапуск сервисов
echo "🚀 Перезапуск сервисов..."
sudo systemctl start quantum-nexus-web
sudo systemctl start quantum-nexus-bot

# Проверка статуса
echo "✅ Проверка статуса..."
sudo systemctl status quantum-nexus-web --no-pager
sudo systemctl status quantum-nexus-bot --no-pager

echo "🎉 Восстановление завершено!"
echo "📋 Проверьте работу приложения в браузере"
