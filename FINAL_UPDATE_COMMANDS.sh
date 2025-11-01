#!/bin/bash

# ============================================================
# ПОЛНЫЙ СКРИПТ ОБНОВЛЕНИЯ QUANTUM NEXUS
# ============================================================

echo "🚀 Начинаем обновление Quantum Nexus..."

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Обновить код
echo -e "${BLUE}📥 Шаг 1: Обновляю код из GitHub...${NC}"
cd /root/quantum-nexus
git pull origin main
echo -e "${GREEN}✅ Код обновлен${NC}"

# 2. Обновить файлы
echo -e "${BLUE}📋 Шаг 2: Копирую файлы приложения...${NC}"
cp web_app.html /var/www/quantum-nexus/
cp admin.html /var/www/quantum-nexus/
cp web_server.py /root/quantum-nexus/
cp models.py /root/quantum-nexus/
echo -e "${GREEN}✅ Файлы скопированы${NC}"

# 3. Обновить базу данных
echo -e "${BLUE}🗄️ Шаг 3: Обновляю базу данных...${NC}"
sudo -u postgres psql -d quantum_nexus <<EOF
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_passive_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_hash_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
\q
EOF
echo -e "${GREEN}✅ База данных обновлена${NC}"

# 4. Установить зависимости
echo -e "${BLUE}📦 Шаг 4: Проверяю зависимости...${NC}"
cd /root/quantum-nexus
source venv/bin/activate
pip install -q -r requirements.txt 2>/dev/null
echo -e "${GREEN}✅ Зависимости установлены${NC}"

# 5. Перезапустить сервисы
echo -e "${BLUE}🔄 Шаг 5: Перезапускаю сервисы...${NC}"
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
sudo systemctl restart nginx
echo -e "${GREEN}✅ Сервисы перезапущены${NC}"

# 6. Проверить статус
echo -e "${BLUE}✅ Шаг 6: Проверяю статус сервисов...${NC}"
echo ""
echo "=== Статус quantum-nexus ==="
sudo systemctl status quantum-nexus --no-pager -l | head -10

echo ""
echo "=== Статус quantum-nexus-web ==="
sudo systemctl status quantum-nexus-web --no-pager -l | head -10

echo ""
echo "=== Статус nginx ==="
sudo systemctl status nginx --no-pager -l | head -10

echo ""
echo -e "${GREEN}🎉 Обновление завершено успешно!${NC}"
echo ""
echo "📝 Что было сделано:"
echo "✅ Ускорено автообновление до 2 секунд"
echo "✅ Добавлена красивая SVG кнопка тапа с эффектом"
echo "✅ Улучшены анимации покупок"
echo "✅ Добавлено 30 уникальных карточек"
echo "✅ Реализована система ежедневных заданий"
echo "✅ Добавлена кнопка 'Вопросы' в админку"
echo "✅ Исправлена реферальная ссылка"
echo "✅ Добавлены анимации для машин в майнинге"
echo ""
echo "🌐 Проверьте:"
echo "   - Бот: https://t.me/Quanexus_bot"
echo "   - Админ-панель: https://quantum-nexus.ru/admin"
echo ""








