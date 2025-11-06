#!/bin/bash

# ==================================================
# Автоматический скрипт обновления Quantum Nexus
# Копирует только измененные файлы
# ==================================================

set -e  # Остановить при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}🚀 АВТОМАТИЧЕСКОЕ ОБНОВЛЕНИЕ QUANTUM NEXUS${NC}"
echo -e "${BLUE}==================================================${NC}"
echo ""

# Перейти в директорию проекта
cd /root/quantum-nexus || { echo -e "${RED}❌ Ошибка: директория /root/quantum-nexus не найдена${NC}"; exit 1; }

echo -e "${YELLOW}📥 Получение последних изменений из GitHub...${NC}"
git pull origin main || { echo -e "${RED}❌ Ошибка при git pull${NC}"; exit 1; }

echo -e "${GREEN}✅ Изменения получены${NC}"
echo ""

# Получить последний коммит
LAST_COMMIT=$(git log -1 --oneline)
echo -e "${BLUE}📝 Последний коммит: ${LAST_COMMIT}${NC}"
echo ""

# Список файлов для копирования
FILES=(
    "web_app.html"
    "web_server.py"
    "handlers.py"
    "models.py"
    "config.py"
)

# Функция для проверки изменений файла
check_file_changed() {
    local file=$1
    # Проверяем, был ли файл изменен в последнем коммите
    git diff HEAD~1 HEAD --name-only | grep -q "^${file}$" && return 0 || return 1
}

# Счетчик измененных файлов
CHANGED_COUNT=0
COPIED_COUNT=0

echo -e "${YELLOW}🔍 Проверка измененных файлов...${NC}"
echo ""

# Проверить каждый файл
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}⚠️  Файл $file не найден в репозитории${NC}"
        continue
    fi
    
    # Проверяем, был ли файл изменен
    if git diff HEAD~1 HEAD --name-only 2>/dev/null | grep -q "^${file}$" || [ "$1" == "--force" ]; then
        CHANGED_COUNT=$((CHANGED_COUNT + 1))
        echo -e "${YELLOW}📝 Обнаружены изменения в: $file${NC}"
        
        # Копировать файл
        echo -e "${BLUE}   → Копирование $file в /var/www/quantum-nexus/...${NC}"
        if sudo cp "/root/quantum-nexus/$file" "/var/www/quantum-nexus/$file"; then
            echo -e "${GREEN}   ✅ $file скопирован${NC}"
            COPIED_COUNT=$((COPIED_COUNT + 1))
        else
            echo -e "${RED}   ❌ Ошибка копирования $file${NC}"
        fi
    else
        echo -e "${NC}   ⏭️  $file без изменений (пропущен)${NC}"
    fi
done

echo ""

# Если использован флаг --force или --all, копируем все файлы
if [ "$1" == "--force" ] || [ "$1" == "--all" ]; then
    echo -e "${YELLOW}🔄 Принудительное копирование всех файлов...${NC}"
    for file in "${FILES[@]}"; do
        if [ -f "$file" ]; then
            echo -e "${BLUE}   → Копирование $file...${NC}"
            sudo cp "/root/quantum-nexus/$file" "/var/www/quantum-nexus/$file"
            echo -e "${GREEN}   ✅ $file скопирован${NC}"
        fi
    done
    COPIED_COUNT=${#FILES[@]}
fi

echo ""
echo -e "${BLUE}==================================================${NC}"
echo -e "${GREEN}📊 Статистика:${NC}"
echo -e "   Изменено файлов: $CHANGED_COUNT"
echo -e "   Скопировано файлов: $COPIED_COUNT"
echo -e "${BLUE}==================================================${NC}"
echo ""

# Перезапустить сервисы
if [ $COPIED_COUNT -gt 0 ] || [ "$1" == "--force" ] || [ "$1" == "--all" ]; then
    echo -e "${YELLOW}🔄 Перезапуск сервисов...${NC}"
    
    echo -e "${BLUE}   → Перезапуск quantum-nexus-web.service...${NC}"
    if sudo systemctl restart quantum-nexus-web.service; then
        echo -e "${GREEN}   ✅ quantum-nexus-web.service перезапущен${NC}"
    else
        echo -e "${RED}   ❌ Ошибка перезапуска quantum-nexus-web.service${NC}"
    fi
    
    echo -e "${BLUE}   → Перезапуск quantum-nexus.service...${NC}"
    if sudo systemctl restart quantum-nexus.service; then
        echo -e "${GREEN}   ✅ quantum-nexus.service перезапущен${NC}"
    else
        echo -e "${RED}   ❌ Ошибка перезапуска quantum-nexus.service${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}📊 Проверка статуса сервисов...${NC}"
    sudo systemctl status quantum-nexus-web.service --no-pager -l | head -n 5
    echo ""
    sudo systemctl status quantum-nexus.service --no-pager -l | head -n 5
else
    echo -e "${YELLOW}ℹ️  Нет изменений для копирования. Сервисы не перезапущены.${NC}"
    echo -e "${YELLOW}   Используйте --force или --all для принудительного обновления${NC}"
fi

echo ""
echo -e "${GREEN}✅ Обновление завершено!${NC}"
echo ""
echo -e "${BLUE}💡 Полезные команды:${NC}"
echo -e "   • Просмотр логов: sudo journalctl -u quantum-nexus-web.service -n 50 --no-pager"
echo -e "   • Проверка статуса: sudo systemctl status quantum-nexus-web.service"
echo -e "   • Принудительное обновление: ./update_server.sh --force"
echo -e "   • Обновить все файлы: ./update_server.sh --all"
echo ""
