#!/bin/bash

# 🚀 Скрипт для обновления Quantum Nexus на Selectel
# Автор: SmartFix
# Дата: $(date)

echo "🚀 Начинаем обновление Quantum Nexus..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Проверка, что мы в правильной папке
if [ ! -d "/root/quantum-nexus" ]; then
    error "Папка /root/quantum-nexus не найдена!"
    exit 1
fi

cd /root/quantum-nexus

# 1. Остановка бота
log "Останавливаем бота..."
pkill -f "python.*bot.py" || warning "Бот не был запущен"
systemctl stop quantum-nexus 2>/dev/null || warning "Сервис quantum-nexus не найден"

# 2. Создание бэкапа
log "Создаем бэкап..."
BACKUP_DIR="/root/quantum-nexus-backup-$(date +%Y%m%d-%H%M%S)"
cp -r /root/quantum-nexus "$BACKUP_DIR"
log "Бэкап создан: $BACKUP_DIR"

# 3. Обновление кода
log "Обновляем код из GitHub..."
git fetch origin
git reset --hard origin/master
log "Код обновлен"

# 4. Установка зависимостей
log "Устанавливаем зависимости..."
pip install -r requirements.txt --quiet

# 5. Обновление базы данных
log "Обновляем базу данных..."
python -c "from database import init_db; init_db()" 2>/dev/null || warning "Ошибка при обновлении БД"

# 6. Запуск бота
log "Запускаем бота..."
nohup python bot.py > bot.log 2>&1 &
BOT_PID=$!

# 7. Проверка запуска
sleep 3
if ps -p $BOT_PID > /dev/null; then
    log "✅ Бот успешно запущен (PID: $BOT_PID)"
else
    error "❌ Ошибка при запуске бота!"
    log "Проверьте логи: tail -f bot.log"
    exit 1
fi

# 8. Финальная проверка
log "Проверяем статус..."
sleep 2
if pgrep -f "python.*bot.py" > /dev/null; then
    log "✅ Обновление завершено успешно!"
    log "📊 Статус бота:"
    ps aux | grep "python.*bot.py" | grep -v grep
    log "📝 Логи: tail -f bot.log"
else
    error "❌ Бот не запустился!"
    log "Проверьте логи: tail -f bot.log"
fi

echo ""
log "🎉 Обновление завершено!"
log "📁 Бэкап сохранен в: $BACKUP_DIR"
log "📝 Для проверки логов: tail -f /root/quantum-nexus/bot.log"
