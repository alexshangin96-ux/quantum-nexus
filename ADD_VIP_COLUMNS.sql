-- Add VIP columns to users table
-- Use ALTER TABLE with error handling for SQLite

-- vip_level
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL UNIQUE,
    username VARCHAR(255),
    coins FLOAT DEFAULT 0.0,
    quanhash FLOAT DEFAULT 0.0,
    energy INTEGER DEFAULT 1000,
    max_energy INTEGER DEFAULT 1000,
    total_taps INTEGER DEFAULT 0,
    total_earned FLOAT DEFAULT 0.0,
    total_mined FLOAT DEFAULT 0.0,
    referral_code VARCHAR(50) UNIQUE,
    referred_by INTEGER,
    referral_income FLOAT DEFAULT 0.0,
    referrals_count INTEGER DEFAULT 0,
    active_multiplier FLOAT DEFAULT 1.0,
    multiplier_expires_at TIMESTAMP,
    is_banned BOOLEAN DEFAULT 0,
    is_frozen BOOLEAN DEFAULT 0,
    ban_reason VARCHAR(255),
    vip_level INTEGER DEFAULT 0,
    vip_badge VARCHAR(50),
    vip_unique_marker VARCHAR(50),
    has_premium_support BOOLEAN DEFAULT 0,
    has_golden_profile BOOLEAN DEFAULT 0,
    has_top_place BOOLEAN DEFAULT 0,
    has_unique_design BOOLEAN DEFAULT 0,
    auto_tap_enabled BOOLEAN DEFAULT 0,
    auto_tap_level INTEGER DEFAULT 0,
    auto_tap_speed FLOAT DEFAULT 2.0,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_passive_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_hash_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMIT;

-- The Python models will handle the table creation automatically

