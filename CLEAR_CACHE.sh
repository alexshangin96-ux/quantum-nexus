#!/bin/bash
# Очистка кэша для Quantum Nexus

echo "🧹 Очистка кэша..."

# Очистить кэш Nginx
systemctl reload nginx

# Перезапустить браузер в Telegram Mini App
echo ""
echo "📱 В Telegram Mini App:"
echo "1. Закройте приложение полностью"
echo "2. Очистите кэш в настройках Telegram"
echo "3. Откройте приложение заново"
echo ""

# Перезапустить сервисы
systemctl restart quantum-nexus-web
systemctl restart quantum-nexus-bot

echo "✅ Кэш очищен, сервисы перезапущены"





