#!/bin/bash

echo "=== ВОССТАНОВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ==="

cd /root/quantum-nexus

echo "1. Проверка базы данных..."
sudo -u postgres psql quantum_nexus -c "SELECT COUNT(*) FROM users;"

echo "2. Проверка последнего бэкапа..."
# Check if there's a backup
if [ -f "users_backup.sql" ]; then
    echo "Найден бэкап users_backup.sql"
    read -p "Восстановить из бэкапа? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Восстановление из бэкапа..."
        sudo -u postgres psql quantum_nexus < users_backup.sql
        echo "Бэкап восстановлен"
    fi
else
    echo "Бэкап не найден"
fi

echo "3. Проверка ботов..."
source venv/bin/activate
python3 generate_bot_users.py
deactivate

echo "4. Проверка статуса..."
sudo systemctl status quantum-nexus --no-pager | head -20

echo "=== ПРОВЕРКА ЗАВЕРШЕНА ==="



