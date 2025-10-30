-- Add auto_tap_expires_at column to users table (if not exists)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='users' AND column_name='auto_tap_expires_at'
    ) THEN
        ALTER TABLE users ADD COLUMN auto_tap_expires_at TIMESTAMP;
        RAISE NOTICE 'Column auto_tap_expires_at added';
    ELSE
        RAISE NOTICE 'Column auto_tap_expires_at already exists';
    END IF;
END $$;

-- Set existing autobots to expire in 24 hours (if they're enabled but don't have expiration)
UPDATE users 
SET auto_tap_expires_at = NOW() + INTERVAL '24 hours'
WHERE auto_tap_enabled = TRUE 
  AND (auto_tap_expires_at IS NULL OR auto_tap_expires_at < NOW())
  AND auto_tap_level > 0;

