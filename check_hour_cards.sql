-- Check if there are any card_hour_ cards in the database
SELECT 
    card_type, 
    COUNT(*) as count,
    MIN(card_level) as min_level,
    MAX(card_level) as max_level
FROM user_cards 
WHERE card_type LIKE 'card_hour_%'
GROUP BY card_type
ORDER BY card_type;

-- Check all card types in the database
SELECT 
    card_type, 
    COUNT(*) as count
FROM user_cards 
GROUP BY card_type
ORDER BY card_type;

-- Check if user_cards table exists
SELECT table_name 
FROM information_schema.tables 
WHERE table_name = 'user_cards';
