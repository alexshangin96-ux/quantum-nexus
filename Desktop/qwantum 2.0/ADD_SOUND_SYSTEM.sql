-- Migration: Add Sound System to Users Table
-- Execute this SQL to add sound settings column for existing users

-- Add sound_enabled column (default TRUE for existing users)
ALTER TABLE users ADD COLUMN IF NOT EXISTS sound_enabled BOOLEAN DEFAULT TRUE;

-- Update existing users to have sounds enabled by default
UPDATE users SET sound_enabled = TRUE WHERE sound_enabled IS NULL;

