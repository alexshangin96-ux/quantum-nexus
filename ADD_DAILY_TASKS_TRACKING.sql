-- Migration: Add Daily Tasks Tracking Columns to Users Table
-- Execute this SQL to add new columns for daily tasks tracking

-- Add daily_tasks_completed column (default {} for existing users)
ALTER TABLE users ADD COLUMN IF NOT EXISTS daily_tasks_completed TEXT DEFAULT '{}';

-- Add last_daily_reset column (track when last reset happened)
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_daily_reset TIMESTAMP NULL;

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_last_daily_reset ON users(last_daily_reset);

