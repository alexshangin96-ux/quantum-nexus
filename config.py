import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = "8426192106:AAGGlkfOYAhaQKPp-bcL-3oHXBE50tzAMog"
APP_URL = "https://quantum-nexus.ru/"

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://quantum:your_secure_password@localhost:5432/quantum_nexus")

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Game Configuration
OFFLINE_INCOME_DURATION = 3 * 60 * 60  # 3 hours in seconds
ENERGY_REGEN_PER_MINUTE = 1
MAX_ENERGY = 100

# Tap Configuration
BASE_TAP_REWARD = 1
ENERGY_COST_PER_TAP = 1

# Mining Configuration
MINING_CYCLE_DURATION = 300  # 5 minutes
BASE_HASH_RATE = 0.01

# Anti-cheat Configuration
MAX_TAPS_PER_SECOND = 5
TAP_COOLDOWN = 0.2  # seconds

# Referral Configuration
REFERRAL_BONUS = 100
REFERRAL_INCOME_PERCENT = 0.05

# Shop Prices
BOOST_PRICES = {
    "multiplier_2x": 1000,
    "multiplier_5x": 5000,
    "energy_booster": 500,
    "mining_boost": 2000,
}

# Cards
CARD_PRICES = {
    "common": 500,
    "rare": 2000,
    "epic": 10000,
    "legendary": 50000,
}

CARD_INCOME = {
    "common": 0.5,
    "rare": 2.0,
    "epic": 10.0,
    "legendary": 50.0,
}
