#!/bin/bash
# Автоматическая диагностика сервера Quantum Nexus
# Выполните: bash AUTO_DIAGNOSE.sh

echo "========================================="
echo "🚀 АВТОМАТИЧЕСКАЯ ДИАГНОСТИКА QUANTUM NEXUS"
echo "========================================="
echo ""

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "1️⃣ ПОИСК ВСЕХ ФАЙЛОВ web_app.html"
echo "----------------------------------------"
find / -name "web_app.html" -type f 2>/dev/null | while read file; do
    version=$(head -n 2 "$file" | grep -o "v[0-9]\.[0-9]" | head -1)
    size=$(ls -lh "$file" | awk '{print $5}')
    date=$(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1,2 | cut -d'.' -f1)
    echo -e "${file}"
    echo -e "  Версия: ${GREEN}${version}${NC}"
    echo -e "  Размер: ${size}"
    echo -e "  Дата: ${date}"
    echo ""
done

echo ""
echo "2️⃣ ПОИСК ВСЕХ ФАЙЛОВ handlers.py"
echo "----------------------------------------"
find / -name "handlers.py" -path "*/quantum-nexus*" -type f 2>/dev/null | while read file; do
    if grep -q "web_app.html" "$file" 2>/dev/null; then
        url=$(grep -o "https://quantum-nexus.ru/web_app.html[^\"]*" "$file" | head -1)
        echo -e "${file}"
        echo -e "  URL: ${GREEN}${url}${NC}"
        echo ""
    fi
done

echo ""
echo "3️⃣ ПРОВЕРКА SYSTEMD СЕРВИСОВ"
echo "----------------------------------------"
if systemctl is-active quantum-nexus-web.service >/dev/null 2>&1; then
    echo -e "quantum-nexus-web.service: ${GREEN}АКТИВЕН${NC}"
    systemctl status quantum-nexus-web.service --no-pager -l | grep -E "Active:|Main PID:|ExecStart=|WorkingDirectory="
else
    echo -e "quantum-nexus-web.service: ${RED}НЕ АКТИВЕН${NC}"
fi
echo ""

if systemctl is-active quantum-nexus.service >/dev/null 2>&1; then
    echo -e "quantum-nexus.service: ${GREEN}АКТИВЕН${NC}"
    systemctl status quantum-nexus.service --no-pager -l | grep -E "Active:|Main PID:|ExecStart=|WorkingDirectory="
else
    echo -e "quantum-nexus.service: ${RED}НЕ АКТИВЕН${NC}"
fi
echo ""

echo ""
echo "4️⃣ ПОИСК ЗАПУЩЕННЫХ ПРОЦЕССОВ"
echo "----------------------------------------"
echo "Процессы Python с bot.py:"
ps aux | grep -E "bot.py|web_server.py" | grep -v grep | while read line; do
    pid=$(echo "$line" | awk '{print $2}')
    cmd=$(echo "$line" | awk '{for(i=11;i<=NF;i++) printf "%s ", $i; print ""}')
    cwd=$(pwdx $pid 2>/dev/null | awk '{print $2}')
    echo -e "${GREEN}PID: ${pid}${NC}"
    echo -e "  Команда: ${cmd}"
    echo -e "  Директория: ${YELLOW}${cwd}${NC}"
    echo ""
done

echo ""
echo "5️⃣ ПРОВЕРКА REPOSITORY"
echo "----------------------------------------"
# Найти все .git директории с quantum-nexus
find / -name ".git" -path "*/quantum-nexus*" -type d 2>/dev/null | while read gitdir; do
    repo=$(dirname "$gitdir")
    echo -e "${YELLOW}Repository: ${repo}${NC}"
    
    # Проверка git remote
    cd "$repo" 2>/dev/null && \
    echo -e "  Remote:" && \
    git remote -v | sed 's/^/    /'
    
    # Проверка последних коммитов
    cd "$repo" 2>/dev/null && \
    echo -e "  Последние коммиты:" && \
    git log --oneline -3 2>/dev/null | sed 's/^/    /' || echo "    Не git репозиторий"
    
    # Проверка версии файлов
    if [ -f "$repo/web_app.html" ]; then
        version=$(head -n 2 "$repo/web_app.html" | grep -o "v[0-9]\.[0-9]" | head -1)
        echo -e "  web_app.html версия: ${GREEN}${version}${NC}"
    fi
    
    if [ -f "$repo/handlers.py" ]; then
        url=$(grep -o "https://quantum-nexus.ru/web_app.html[^\"]*" "$repo/handlers.py" 2>/dev/null | head -1)
        echo -e "  handlers.py URL: ${GREEN}${url}${NC}"
    fi
    
    echo ""
done

echo ""
echo "6️⃣ ПРОВЕРКА NGINX/CADDY"
echo "----------------------------------------"
echo "Проверка Nginx..."
if [ -f /etc/nginx/sites-enabled/default ]; then
    echo -e "Nginx конфигурация:" && \
    grep -r "quantum-nexus" /etc/nginx/ 2>/dev/null | head -20 | sed 's/^/  /'
else
    echo -e "${YELLOW}Nginx конфигурация не найдена${NC}"
fi

echo ""
echo "Проверка Caddy..."
if command -v caddy &> /dev/null; then
    if [ -f /etc/caddy/Caddyfile ]; then
        echo -e "Caddy конфигурация:"
        grep -A10 "quantum-nexus" /etc/caddy/Caddyfile | sed 's/^/  /'
    fi
else
    echo -e "${YELLOW}Caddy не установлен${NC}"
fi

echo ""
echo "7️⃣ САМЫЕ АКТУАЛЬНЫЕ ФАЙЛЫ"
echo "----------------------------------------"
echo "web_app.html файлы отсортированные по дате изменения:"
find / -name "web_app.html" -type f 2>/dev/null | while read file; do
    date=$(stat -c %Y "$file" 2>/dev/null)
    version=$(head -n 2 "$file" | grep -o "v[0-9]\.[0-9]" | head -1)
    echo "$date|$version|$file"
done | sort -rn | head -5 | cut -d'|' -f2,3 | sed 's/|/ -> /' | sed 's/^/  /'

echo ""
echo "handlers.py файлы отсортированные по дате изменения:"
find / -name "handlers.py" -path "*/quantum-nexus*" -type f 2>/dev/null | while read file; do
    date=$(stat -c %Y "$file" 2>/dev/null)
    url=$(grep -o "https://quantum-nexus.ru/web_app.html[^\"]*" "$file" 2>/dev/null | head -1)
    echo "$date|$url|$file"
done | sort -rn | head -3 | cut -d'|' -f2,3 | sed 's/|/ -> /' | sed 's/^/  /'

echo ""
echo "8️⃣ РЕКОМЕНДАЦИИ"
echo "----------------------------------------"
echo -e "${YELLOW}После проверки выше:${NC}"
echo "1. Найдите самый свежий web_app.html (выше v4.2)"
echo "2. Найдите handlers.py с URL содержащим v4.3"
echo "3. Убедитесь что эти файлы используются сервисами"
echo "4. Если нет - обновите нужные файлы в нужной директории"
echo ""
echo -e "${RED}После диагностики запустите:${NC}"
echo "cd /root/quantum-nexus"
echo "git pull origin main"
echo "sudo cp web_app.html /var/www/quantum-nexus/web_app.html"
echo "sudo cp handlers.py /root/quantum-nexus/handlers.py"
echo "sudo systemctl restart quantum-nexus-web.service"
echo "sudo systemctl restart quantum-nexus.service"

echo ""
echo "========================================="
echo "✅ ДИАГНОСТИКА ЗАВЕРШЕНА"
echo "========================================="

