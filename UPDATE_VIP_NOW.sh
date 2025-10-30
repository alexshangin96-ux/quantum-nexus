#!/bin/bash
# ОБНОВЛЕНИЕ VIP ФУНКЦИЙ НА СЕРВЕРЕ
# Выполните на сервере для активации всех VIP функций

echo "🚀 ОБНОВЛЕНИЕ VIP ФУНКЦИЙ..."
echo ""

# 1. Переходим в директорию проекта
cd ~/quantum-nexus || cd /root/quantum-nexus

# 2. Получаем последние изменения
echo "📥 Получение обновлений..."
git pull origin main

# 3. Копируем обновленный web_app.html
echo "📁 Копирование web_app.html..."
sudo cp web_app.html /var/www/quantum-nexus/

# 4. Перезапускаем сервисы
echo "🔄 Перезапуск сервисов..."
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus

echo ""
echo "✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО!"
echo ""
echo "✨ Теперь доступны все VIP функции:"
echo "  👑 VIP Бусты (x20, x50)"
echo "  🎉 VIP Турниры и События"
echo "  💳 VIP Карточки"
echo "  💸 VIP Бонусы при выводе (0% комиссия)"
echo "  ✨ VIP Визуальные эффекты"
echo "  🤖 VIP Машины"
echo "  🎮 VIP Привилегии"
echo ""
echo "🌐 Примените через /start в боте для обновления кеша!"






