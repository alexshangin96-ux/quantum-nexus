#!/bin/bash
# Найти где реально находятся файлы бота

echo "🔍 ПОИСК РЕАЛЬНОГО МЕСТОПОЛОЖЕНИЯ ФАЙЛОВ"
echo "========================================="
echo ""

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "1️⃣ Проверка systemd файлов бота:"
echo "----------------------------------------"
cat /etc/systemd/system/quantum-nexus.service 2>/dev/null || echo "Файл не найден"
echo ""
cat /etc/systemd/system/quantum-nexus-web.service 2>/dev/null || echo "Файл не найден"

echo ""
echo "2️⃣ Поиск всех bot.py на сервере:"
echo "----------------------------------------"
find / -name "bot.py" -type f 2>/dev/null | while read file; do
    echo "$file"
    echo "  Размер: $(ls -lh "$file" | awk '{print $5}')"
    echo "  Дата: $(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1,2 | cut -d'.' -f1)"
    echo ""
done

echo ""
echo "3️⃣ Поиск всех handlers.py на сервере:"
echo "----------------------------------------"
find / -name "handlers.py" -type f 2>/dev/null | while read file; do
    if grep -q "InlineKeyboardButton.*web_app" "$file" 2>/dev/null; then
        echo "$file"
        grep -o "web_app.html[^\"]*" "$file" | head -1
        echo ""
    fi
done

echo ""
echo "4️⃣ Поиск всех web_app.html на сервере:"
echo "----------------------------------------"
find / -name "web_app.html" -type f 2>/dev/null | while read file; do
    version=$(head -n 2 "$file" | grep -o "v[0-9]\.[0-9]" | head -1)
    echo "$file -> $version"
done

echo ""
echo "5️⃣ Проверка запущенных процессов:"
echo "----------------------------------------"
ps aux | grep -E "python.*bot|python.*web" | grep -v grep | while read line; do
    pid=$(echo "$line" | awk '{print $2}')
    cmd=$(echo "$line" | awk '{for(i=11;i<=NF;i++) printf "%s ", $i; print ""}')
    cwd=$(pwdx $pid 2>/dev/null)
    echo "PID: $pid"
    echo "  CMD: $cmd"
    echo "  CWD: $cwd"
    echo ""
done

echo ""
echo "6️⃣ Проверка Nginx/Caddy конфигурации:"
echo "----------------------------------------"
if [ -f /etc/nginx/sites-enabled/default ]; then
    echo "Nginx config:"
    cat /etc/nginx/sites-enabled/default | grep -A5 "quantum"
fi

echo ""
echo "========================================="
echo -e "${YELLOW}Скопируйте вывод и отправьте мне${NC}"
echo "========================================="





