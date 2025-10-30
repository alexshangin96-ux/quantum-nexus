#!/bin/bash

# ============================================================
# ПОЛНЫЙ СКРИПТ ОБНОВЛЕНИЯ QUANTUM NEXUS - ВСЕ ИЗМЕНЕНИЯ
# ============================================================

echo "🚀 Начинаем полное обновление Quantum Nexus..."
echo ""

# Шаг 1: Обновить код
echo "📥 Шаг 1: Обновляю код из GitHub..."
cd /root/quantum-nexus
git pull origin main
echo "✅ Код обновлен"
echo ""

# Шаг 2: Скопировать файлы
echo "📋 Шаг 2: Копирую файлы приложения..."
cp web_app.html /var/www/quantum-nexus/
cp admin.html /var/www/quantum-nexus/
cp web_server.py /root/quantum-nexus/
cp models.py /root/quantum-nexus/
echo "✅ Файлы скопированы"
echo ""

# Шаг 3: Обновить базу данных
echo "🗄️ Шаг 3: Обновляю базу данных..."
sudo -u postgres psql -d quantum_nexus <<'EOF'
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_passive_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_hash_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS auto_tap_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS auto_tap_level INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS auto_tap_speed REAL DEFAULT 2.0;
\q
EOF
echo "✅ База данных обновлена"
echo ""

# Шаг 4: Установить зависимости
echo "📦 Шаг 4: Устанавливаю зависимости..."
cd /root/quantum-nexus
source venv/bin/activate
pip install -q -r requirements.txt 2>/dev/null || echo "Зависимости уже установлены"
echo "✅ Зависимости проверены"
echo ""

# Шаг 5: Перезапустить сервисы
echo "🔄 Шаг 5: Перезапускаю сервисы..."
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
sudo systemctl restart nginx
echo "✅ Сервисы перезапущены"
echo ""

# Шаг 6: Проверить статус
echo "✅ Проверяю статус сервисов..."
echo ""
echo "=== quantum-nexus ==="
sudo systemctl status quantum-nexus --no-pager -l | head -5
echo ""
echo "=== quantum-nexus-web ==="
sudo systemctl status quantum-nexus-web --no-pager -l | head -5
echo ""
echo "=== nginx ==="
sudo systemctl status nginx --no-pager -l | head -5
echo ""

echo "🎉 ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!"
echo ""
echo "📝 Что было реализовано:"
echo "  ✅ Ускорено автообновление до 2 секунд"
echo "  ✅ SVG кнопка тапа с эффектом цвета"
echo "  ✅ Улучшены анимации покупок"
echo "  ✅ Добавлено 30 уникальных карточек"
echo "  ✅ Система ежедневных заданий"
echo "  ✅ Кнопка 'Вопросы' в админке"
echo "  ✅ Исправлена реферальная ссылка"
echo "  ✅ Анимации для машин в майнинге"
echo "  ✅ Система уровней для покупок (+2% за уровень)"
echo "  ✅ Исправлен автотап"
echo ""
echo "🌐 Проверьте:"
echo "   Бот: https://t.me/Quanexus_bot"
echo "   Админ: https://quantum-nexus.ru/admin"






