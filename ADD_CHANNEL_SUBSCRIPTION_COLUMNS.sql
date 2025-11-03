-- Migration: Add Channel Subscription Tracking Columns to Users Table
-- Execute this SQL to add new columns for daily tasks channel subscription

-- Add channel_subscribed column (default false for existing users)
ALTER TABLE users ADD COLUMN IF NOT EXISTS channel_subscribed BOOLEAN DEFAULT FALSE;

-- Add channel_subscribed_at column (track when user subscribed)
ALTER TABLE users ADD COLUMN IF NOT EXISTS channel_subscribed_at TIMESTAMP NULL;

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_channel_subscribed ON users(channel_subscribed);

