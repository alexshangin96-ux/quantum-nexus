#!/bin/bash

echo "=== Проверка баз данных PostgreSQL ==="
sudo -u postgres psql -l

echo ""
echo "=== Статистика пользователей ==="
sudo -u postgres psql quantum_nexus -c "
SELECT 
    COUNT(*) as total_users,
    COUNT(CASE WHEN total_earned > 0 THEN 1 END) as users_with_earnings,
    COUNT(CASE WHEN total_taps > 0 THEN 1 END) as users_with_taps
FROM users;
"

echo ""
echo "=== Топ 10 пользователей по total_earned ==="
sudo -u postgres psql quantum_nexus -c "
SELECT 
    username,
    total_earned,
    total_taps,
    coins,
    level,
    vip_level
FROM users 
ORDER BY total_earned DESC 
LIMIT 10;
"

