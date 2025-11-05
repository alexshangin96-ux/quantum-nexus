-- Migration: Add Level, Experience, and Rating System to Users Table
-- Execute this SQL to add new columns for leaderboard system

-- Add level column (default 1 for existing users)
ALTER TABLE users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1;

-- Add experience column (default 0 for existing users)
ALTER TABLE users ADD COLUMN IF NOT EXISTS experience FLOAT DEFAULT 0.0;

-- Add rating column (default 0 for existing users)
ALTER TABLE users ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 0.0;

-- Update existing users with initial experience and rating based on their achievements
-- 5x slower progression: coefficients divided by 5, max level 10000
UPDATE users 
SET experience = (total_earned * 0.002) + (total_taps * 0.02) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 200),
    level = LEAST(10000, FLOOR(SQRT(GREATEST(0, experience) / 500) + 1)),
    rating = (coins * 0.002) + (total_earned * 0.02) + (total_taps * 0.01) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 200000) + (level * 2000)
WHERE level IS NULL OR experience IS NULL OR rating IS NULL;

-- Display summary
SELECT 
    COUNT(*) as total_users,
    AVG(level) as avg_level,
    MAX(level) as max_level,
    AVG(rating) as avg_rating,
    MAX(rating) as max_rating,
    AVG(experience) as avg_experience,
    MAX(experience) as max_experience
FROM users;




