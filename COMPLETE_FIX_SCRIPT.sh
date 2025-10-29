#!/bin/bash
# ============================================================
# ПОЛНЫЙ СКРИПТ ИСПРАВЛЕНИЯ ВСЕХ 11 ЗАДАЧ
# ============================================================

echo "🚀 Начинаем полное исправление Quantum Nexus..."
echo ""

# Обновить код
cd /root/quantum-nexus
git pull origin main

# Скопировать файлы
cp web_app.html /var/www/quantum-nexus/
cp admin.html /var/www/quantum-nexus/
cp web_server.py /root/quantum-nexus/
cp handlers.py /root/quantum-nexus/
cp models.py /root/quantum-nexus/

# Перезапустить сервисы
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
sudo systemctl restart nginx

echo "✅ Все исправления применены!"
echo ""
echo "📝 Что исправлено:"
echo "  ✅ Реферальная ссылка"
echo "  ✅ Пассивный доход - обе валюты"
echo "  ✅ Уровневая система в магазине"
echo "  ✅ Кнопка тапа - большая иконка и нежная анимация"
echo "  ✅ Поддержка - отправка в админку"
echo "  ✅ Ежедневные задания - реальный прогресс"

echo ""
echo "🌐 Проверьте:"
echo "   Бот: https://t.me/Quanexus_bot"
echo "   Админ: https://quantum-nexus.ru/admin"



