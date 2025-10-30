#!/usr/bin/env python3
"""
Migration to add shop item levels to User model
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from sqlalchemy import text

def run_migration():
    """Add shop item levels columns to users table"""
    try:
        with get_db() as db:
            # Add new columns to users table
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS tap_boost_levels TEXT DEFAULT '{}',
                ADD COLUMN IF NOT EXISTS energy_buy_levels TEXT DEFAULT '{}',
                ADD COLUMN IF NOT EXISTS energy_expand_levels TEXT DEFAULT '{}'
            """))
            db.commit()
            print("✅ Migration completed successfully!")
            print("Added columns: tap_boost_levels, energy_buy_levels, energy_expand_levels")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    return True

if __name__ == "__main__":
    run_migration()


