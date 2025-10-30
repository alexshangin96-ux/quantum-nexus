#!/usr/bin/env python3
"""
Migration script to add mining level fields to User table
Run this on the server after pulling the latest code
"""

from database import get_db
from models import User
import json

def migrate_mining_levels():
    """Add mining level fields to existing users"""
    try:
        with get_db() as db:
            users = db.query(User).all()
            for user in users:
                # Initialize mining level fields if they don't exist
                if not hasattr(user, 'mining_coins_levels') or user.mining_coins_levels is None:
                    user.mining_coins_levels = '{}'
                if not hasattr(user, 'mining_quanhash_levels') or user.mining_quanhash_levels is None:
                    user.mining_quanhash_levels = '{}'
                if not hasattr(user, 'mining_vip_levels') or user.mining_vip_levels is None:
                    user.mining_vip_levels = '{}'
            
            db.commit()
            print(f"Migration complete: {len(users)} users updated")
            return True
    except Exception as e:
        print(f"Migration error: {str(e)}")
        return False

if __name__ == '__main__':
    migrate_mining_levels()

