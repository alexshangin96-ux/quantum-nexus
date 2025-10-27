#!/bin/bash
# ============================================================
# ПОЛНОЕ ОБНОВЛЕНИЕ QUANTUM NEXUS - ВСЕ 11 ИСПРАВЛЕНИЙ
# ============================================================

echo "🚀 Начинаем полное обновление Quantum Nexus..."
echo ""

cd /root/quantum-nexus
git pull origin main

cp web_app.html /var/www/quantum-nexus/
cp admin.html /var/www/quantum-nexus/
cp web_server.py /root/quantum-nexus/
cp handlers.py /root/quantum-nexus/
cp models.py /root/quantum-nexus/

sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
sudo systemctl restart nginx

echo "✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО!"
echo ""
echo "📝 ЧТО ИСПРАВЛЕНО:"
echo "  ✅ Реферальная ссылка (Quanexus_bot)"
echo "  ✅ Пассивный доход - обе валюты"
echo "  ✅ Уровневая система в магазине"
echo "  ✅ Карточки на главном экране"
echo "  ✅ Бусты при покупке работают"
echo "  ✅ Автотапы работают (24 часа)"
echo "  ✅ Энергия при покупке"
echo "  ✅ Описание позиций в магазине"
echo "  ✅ Ежедневные задания - реальный прогресс"
echo "  ✅ Поддержка - отправка в админку"
echo "  ✅ Кнопка тапа - большая иконка, нежная анимация"
echo ""
echo "🌐 Проверьте:"
echo "   Бот: https://t.me/Quanexus_bot"
echo "   Админ: https://quantum-nexus.ru/admin"


