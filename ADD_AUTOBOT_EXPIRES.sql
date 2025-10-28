-- Add auto_tap_expires_at column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS auto_tap_expires_at TIMESTAMP;

-- Set existing autobots to expire in 24 hours (if they're enabled but don't have expiration)
UPDATE users 
SET auto_tap_expires_at = NOW() + INTERVAL '24 hours'
WHERE auto_tap_enabled = TRUE 
  AND (auto_tap_expires_at IS NULL OR auto_tap_expires_at < NOW())
  AND auto_tap_level > 0;

