-- Update Levels and Rating System to 10000 max level with 5x slower progression
-- Execute this SQL to update all existing users with new formulas

-- Update ALL users with new experience, level, and rating formulas
-- 5x slower progression: coefficients divided by 5, max level 10000
UPDATE users 
SET experience = (total_earned * 0.002) + (total_taps * 0.02) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 200),
    level = LEAST(10000, FLOOR(SQRT(GREATEST(0, (total_earned * 0.002) + (total_taps * 0.02) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 200)) / 500) + 1)),
    rating = (coins * 0.002) + (total_earned * 0.02) + (total_taps * 0.01) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 200000) + (LEAST(10000, FLOOR(SQRT(GREATEST(0, (total_earned * 0.002) + (total_taps * 0.02) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 200)) / 500) + 1)) * 2000);

-- Display summary after update
SELECT 
    COUNT(*) as total_users,
    AVG(level) as avg_level,
    MAX(level) as max_level,
    AVG(rating) as avg_rating,
    MAX(rating) as max_rating,
    AVG(experience) as avg_experience,
    MAX(experience) as max_experience
FROM users;

