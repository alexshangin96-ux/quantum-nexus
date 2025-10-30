-- Create user_cards table if it doesn't exist
CREATE TABLE IF NOT EXISTS user_cards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    card_type VARCHAR(50),
    income_per_minute FLOAT,
    card_level INTEGER DEFAULT 1,
    experience INTEGER DEFAULT 0,
    experience_to_next_level INTEGER DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on user_id for better performance
CREATE INDEX IF NOT EXISTS idx_user_cards_user_id ON user_cards(user_id);

-- Create index on card_type for better performance
CREATE INDEX IF NOT EXISTS idx_user_cards_card_type ON user_cards(card_type);

-- Create index on user_id and card_type for better performance
CREATE INDEX IF NOT EXISTS idx_user_cards_user_card ON user_cards(user_id, card_type);
