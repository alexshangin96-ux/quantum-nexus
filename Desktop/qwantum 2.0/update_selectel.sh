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

# 1. Обновление кода
log "Обновляем код из GitHub..."
git fetch origin
git reset --hard origin/master
log "Код обновлен"

# 2. Копирование обновленного файла
log "Копируем обновленный web_app.html..."
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
log "Файл скопирован"

# 3. Перезапуск сервисов
log "Перезапускаем сервисы..."
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service
log "Сервисы перезапущены"

# 4. Проверка статуса
log "Проверяем статус сервисов..."
sleep 3

# Проверка веб-сервиса
if systemctl is-active --quiet quantum-nexus-web.service; then
    log "✅ Веб-сервис работает"
else
    error "❌ Веб-сервис не запустился!"
    sudo systemctl status quantum-nexus-web.service
fi

# Проверка основного сервиса
if systemctl is-active --quiet quantum-nexus.service; then
    log "✅ Основной сервис работает"
else
    error "❌ Основной сервис не запустился!"
    sudo systemctl status quantum-nexus.service
fi

# 5. Финальная проверка
log "Проверяем статус..."
if systemctl is-active --quiet quantum-nexus-web.service && systemctl is-active --quiet quantum-nexus.service; then
    log "✅ Обновление завершено успешно!"
    log "📊 Статус сервисов:"
    sudo systemctl status quantum-nexus-web.service --no-pager -l
    sudo systemctl status quantum-nexus.service --no-pager -l
else
    error "❌ Не все сервисы запустились!"
    log "Проверьте логи:"
    log "sudo journalctl -u quantum-nexus.service -f"
    log "sudo journalctl -u quantum-nexus-web.service -f"
fi

echo ""
log "🎉 Обновление завершено!"
log "📁 Бэкап сохранен в: $BACKUP_DIR"
log "📝 Для проверки логов: tail -f /root/quantum-nexus/bot.log"
