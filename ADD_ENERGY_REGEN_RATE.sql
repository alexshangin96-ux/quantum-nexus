-- Add energy regeneration rate column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS energy_regen_rate FLOAT DEFAULT 1.0;

-- Update existing users to have default regeneration rate
UPDATE users SET energy_regen_rate = 1.0 WHERE energy_regen_rate IS NULL;


