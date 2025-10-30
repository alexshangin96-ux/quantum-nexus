#!/bin/bash

echo "🚀 Обновление всех 60 карточек товаров..."
echo ""

cd /root/quantum-nexus

echo "📥 Получение обновлений из GitHub..."
git pull origin main

echo ""
echo "🔄 Перезапуск веб-сервиса..."
systemctl restart quantum-nexus-web.service

echo ""
echo "✅ Обновление завершено!"
echo "📱 Откройте приложение в Telegram и проверьте раздел 'Купить валюту'"
echo ""
echo "Проверьте все 6 категорий:"
echo "  🎯 СТАРТОВЫЕ НАБОРЫ (1-10)"
echo "  🚀 ПРЕМИУМ НАБОРЫ (11-20)"
echo "  ⭐ ПРЕМИУМ ФУНКЦИИ (21-30)"
echo "  🔮 QUANHASH НАБОРЫ (31-40)"
echo "  🎁 КОМБО СЕТЫ (41-50)"
echo "  👑 VIP ФУНКЦИИ (51-60)"





