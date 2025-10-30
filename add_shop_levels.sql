-- Migration to add shop item levels to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS tap_boost_levels TEXT DEFAULT '{}',
ADD COLUMN IF NOT EXISTS energy_buy_levels TEXT DEFAULT '{}',
ADD COLUMN IF NOT EXISTS energy_expand_levels TEXT DEFAULT '{}';


