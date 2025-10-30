-- Add mining level fields to users table
-- Run this SQL to add the new columns for mining machine levels

-- Add mining_coins_levels column
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS mining_coins_levels TEXT DEFAULT '{}';

-- Add mining_quanhash_levels column
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS mining_quanhash_levels TEXT DEFAULT '{}';

-- Add mining_vip_levels column
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS mining_vip_levels TEXT DEFAULT '{}';

-- Initialize existing users with empty JSON objects
UPDATE users 
SET mining_coins_levels = '{}' 
WHERE mining_coins_levels IS NULL;

UPDATE users 
SET mining_quanhash_levels = '{}' 
WHERE mining_quanhash_levels IS NULL;

UPDATE users 
SET mining_vip_levels = '{}' 
WHERE mining_vip_levels IS NULL;

-- Verify the changes
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'users' 
AND column_name LIKE 'mining_%_levels'
ORDER BY column_name;

