-- Проверка всех пользователей в базе
SELECT 
    COUNT(*) as total_users,
    COUNT(CASE WHEN total_earned > 0 THEN 1 END) as users_with_earnings,
    COUNT(CASE WHEN total_taps > 0 THEN 1 END) as users_with_taps
FROM users;

-- Топ 10 пользователей по total_earned
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





