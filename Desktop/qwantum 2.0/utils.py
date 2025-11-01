from datetime import datetime, timedelta
from config import OFFLINE_INCOME_DURATION
import hashlib


def format_currency(amount, decimals=2):
    """Format currency with appropriate suffixes"""
    if amount >= 1_000_000:
        return f"{amount / 1_000_000:.2f}M"
    elif amount >= 1_000:
        return f"{amount / 1_000:.2f}K"
    else:
        return f"{amount:.{decimals}f}"


def calculate_offline_income(user):
    """Calculate offline income for user"""
    if not user.last_active:
        return 0.0
    
    time_diff = (datetime.utcnow() - user.last_active).total_seconds()
    
    # Check if offline time is within limit
    if time_diff > OFFLINE_INCOME_DURATION:
        time_diff = OFFLINE_INCOME_DURATION
    
    # Calculate income (simplified formula)
    # You can adjust this based on user's cards, level, etc.
    income_per_minute = 1.0  # Base income
    
    # Add income from cards
    total_card_income = sum(
        card.income_per_minute 
        for card in user.cards 
        if card.is_active
    )
    income_per_minute += total_card_income
    
    total_income = (time_diff / 60) * income_per_minute * user.active_multiplier
    
    return total_income


def check_anti_cheat(user_id, current_time):
    """Check for anti-cheat violations"""
    from redis import Redis
    from config import REDIS_HOST, REDIS_PORT, MAX_TAPS_PER_SECOND, TAP_COOLDOWN
    
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    
    key = f"tap_history:{user_id}"
    
    # Get tap history
    history = redis_client.lrange(key, 0, -1)
    
    # Add current tap
    redis_client.lpush(key, current_time)
    
    # Keep only last second of taps
    redis_client.ltrim(key, 0, MAX_TAPS_PER_SECOND)
    
    # Check if too many taps in last second
    recent_taps = [
        float(t) 
        for t in history 
        if current_time - float(t) <= 1.0
    ]
    
    if len(recent_taps) >= MAX_TAPS_PER_SECOND:
        return False  # Possible cheat
    
    return True


def generate_tap_hash(user_id, timestamp):
    """Generate hash for tap verification"""
    data = f"{user_id}_{timestamp}"
    return hashlib.md5(data.encode()).hexdigest()[:8]


def get_top_users(db, currency="coins", limit=10):
    """Get top users by currency"""
    from models import User
    
    if currency == "coins":
        return db.query(User).order_by(User.total_earned.desc()).limit(limit).all()
    elif currency == "quanhash":
        return db.query(User).order_by(User.total_mined.desc()).limit(limit).all()
    
    return []


def get_user_rank(db, user, currency="coins"):
    """Get user rank"""
    from models import User
    
    if currency == "coins":
        users_above = db.query(User).filter(User.total_earned > user.total_earned).count()
    elif currency == "quanhash":
        users_above = db.query(User).filter(User.total_mined > user.total_mined).count()
    else:
        return 0
    
    return users_above + 1


def calculate_experience_to_level(level):
    """Calculate experience needed for next level"""
    return int(100 * (1.5 ** (level - 1)))


def upgrade_card(card):
    """Upgrade card to next level"""
    card.card_level += 1
    card.experience = 0
    card.experience_to_next_level = calculate_experience_to_level(card.card_level)
    card.income_per_minute = card.income_per_minute * 1.5  # 50% increase


def get_machine_stats(level):
    """Get mining machine statistics"""
    stats = {
        1: {"hash_rate": 0.01, "power": 1.0, "efficiency": 1.0, "cost": 10000},
        2: {"hash_rate": 0.05, "power": 2.5, "efficiency": 1.2, "cost": 50000},
        3: {"hash_rate": 0.15, "power": 5.0, "efficiency": 1.5, "cost": 200000},
        4: {"hash_rate": 0.50, "power": 10.0, "efficiency": 2.0, "cost": 1000000},
    }
    return stats.get(level, stats[1])


def calculate_mining_reward(machine):
    """Calculate mining reward for machine"""
    from datetime import datetime
    
    if not machine.is_active:
        return 0.0
    
    time_diff = (datetime.utcnow() - machine.last_mined_at).total_seconds()
    
    # Mining calculation with complexity
    hash_rate = machine.hash_rate
    efficiency = machine.efficiency
    time_factor = time_diff / 60  # Convert to minutes
    
    # Complex mining formula with diminishing returns
    base_reward = hash_rate * time_factor * efficiency
    
    # Add some randomness and complexity
    reward = base_reward * (0.8 + 0.4 * (hash_rate / 0.5))  # Scaling factor
    
    return reward











