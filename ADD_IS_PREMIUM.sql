-- Migration: Add is_premium column to users table
-- Execute this SQL to add Telegram Premium status tracking

-- Add is_premium column
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_premium BOOLEAN DEFAULT FALSE;

-- Add comment
COMMENT ON COLUMN users.is_premium IS 'Telegram Premium subscription status';

-- Display confirmation
SELECT 'Migration completed: is_premium column added successfully' as status;

