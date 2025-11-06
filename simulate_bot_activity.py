#!/usr/bin/env python3
"""
Simulate bot activity - automatically increase their total_earned and simulate farming
"""

from database import get_db
from models import User, UserCard
from datetime import datetime, timedelta
import random

def simulate_bot_activity():
    """Simulate bot activity - increase earnings, add/remove activity"""
    with get_db() as db:
        # Get all bot users (telegram_id >= 9000000000)
        bots = db.query(User).filter(User.telegram_id >= 9000000000).all()
        
        print(f"Found {len(bots)} bot users")
        
        for bot in bots:
            # Random chance to "farm" (70% chance)
            if random.random() < 0.7:
                # Add earnings (simulate farming)
                farmed_coins = random.randint(100, 5000)
                bot.coins += farmed_coins
                bot.total_earned += farmed_coins
                bot.last_active = datetime.utcnow()
                
                print(f"Bot {bot.username}: +{farmed_coins} coins")
            else:
                # Not farming now (30% chance)
                pass
        
        db.commit()
        print(f"Updated {len(bots)} bots activity")

if __name__ == '__main__':
    simulate_bot_activity()










