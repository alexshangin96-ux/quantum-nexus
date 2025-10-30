#!/bin/bash
# Проверка синтаксиса Python

echo "🔍 ПРОВЕРКА СИНТАКСИСА PYTHON"
echo "========================================="
echo ""

cd /root/quantum-nexus
source venv/bin/activate

echo "1️⃣ Проверка web_server.py:"
echo "----------------------------------------"
python -m py_compile web_server.py 2>&1

if [ $? -eq 0 ]; then
    echo -e "✅ Синтаксис OK"
else
    echo -e "❌ ОШИБКА СИНТАКСИСА"
fi

echo ""
echo "2️⃣ Попытка импорта:"
echo "----------------------------------------"
python -c "from web_server import app; print('Import OK')" 2>&1

echo ""
echo "3️⃣ Последние логи:"
echo "----------------------------------------"
journalctl -u quantum-nexus-web.service -n 30 --no-pager | grep -E "Error|Exception|Traceback" | tail -15

echo ""
echo "========================================="

