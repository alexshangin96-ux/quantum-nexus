#!/usr/bin/env python3
"""
Generate 137 fake bot users for Quantum Nexus
Creates realistic usernames and simulates earnings
"""

import random
from database import get_db, generate_referral_code
from models import User
from datetime import datetime, timedelta

# Realistic Russian usernames (first part)
first_names = [
    "Алексей", "Дмитрий", "Сергей", "Андрей", "Александр", "Максим", "Иван", "Михаил",
    "Никита", "Артем", "Владимир", "Илья", "Егор", "Антон", "Евгений", "Павел",
    "Станислав", "Вадим", "Матвей", "Денис", "Тимур", "Роман", "Глеб", "Дмитрий",
    "Игорь", "Олег", "Владислав", "Александр", "Артём", "Родион", "Константин",
    "Даниил", "Кирилл", "Валентин", "Виктор", "Юрий", "Егор", "Фёдор", "Кирилл"
]

# Realistic Russian usernames (second part)
second_names = [
    "Petrov1992", "Ivanov2020", "Sidorov_Pro", "KozlovGamer", "Sokolov77",
    "Lebedev_Alex", "NovikovMax", "MorozovTop", "VolkovPro", "AlekseevPower",
    "OrlovGaming", "Makarena1988", "SergeiYT", "DmitriyGamer", "AlexPro",
    "MaxPlayer", "IvanTop", "MishaGaming", "NikitaPower", "ArtemPro",
    "VladGamer", "IlyaBest", "EgorYT", "AntonPro", "Zhenya2021",
    "PavelTop", "StasPower", "VadimPro", "MatveyGaming", "DenisYT",
    "TimurBest", "RomanPower", "GlebPro", "DimaGamer", "IgorTop",
    "OlegPro", "VladislavGaming", "SashaPower", "ArtyomBest", "RodionPro"
]

# Username patterns
patterns = [
    lambda f, s: f"{f}{random.randint(89, 99)}",
    lambda f, s: f"{s}{random.randint(2000, 2024)}",
    lambda f, s: f"{f}_Pro",
    lambda f, s: f"{s}",
    lambda f, s: f"{f}Gaming",
    lambda f, s: f"{s}_Gamer",
    lambda f, s: f"{f}{random.choice(['_YT', '_Ru', '_Best'])}",
    lambda f, s: f"{s}_{random.choice(['Top', 'Power', 'Pro'])}",
]

def generate_realistic_username():
    """Generate a realistic Russian username"""
    first = random.choice(first_names)
    second = random.choice(second_names)
    pattern = random.choice(patterns)
    username = pattern(first, second)
    # Sometimes add numbers
    if random.random() < 0.3:
        username = f"{username}{random.randint(1, 999)}"
    return username

def generate_bot_users():
    """Generate 137 bot users with realistic data"""
    with get_db() as db:
        existing_users = db.query(User).count()
        print(f"Current users in database: {existing_users}")
        
        if existing_users >= 1000:
            print("Too many users in database, skipping generation")
            return
        
        # Check if bots already exist (check for high telegram_ids)
        bot_count = db.query(User).filter(User.telegram_id >= 9000000000).count()
        if bot_count >= 137:
            print(f"Already have {bot_count} bots, skipping generation")
            return
        
        # Generate usernames and ensure uniqueness
        usernames = set()
        while len(usernames) < 137:
            username = generate_realistic_username()
            if username not in usernames:
                usernames.add(username)
        
        usernames_list = list(usernames)
        
        # Create bots with varying activity levels
        for i, username in enumerate(usernames_list):
            # Random telegram ID (larger than any real user)
            telegram_id = 9000000000 + random.randint(1, 999999999)
            
            # Varying activity levels
            if i < 10:
                # Top 10 bots (very active)
                total_taps = random.randint(15000, 50000)
                total_earned = random.randint(500000, 2000000)
                coins = random.randint(50000, 200000)
                quanhash = random.randint(10000, 50000)
                vip_level = random.choice([0, 0, 1, 2, 3])  # Some VIPs
            elif i < 30:
                # Active bots
                total_taps = random.randint(5000, 15000)
                total_earned = random.randint(100000, 500000)
                coins = random.randint(10000, 50000)
                quanhash = random.randint(5000, 10000)
                vip_level = 0
            elif i < 70:
                # Moderate activity
                total_taps = random.randint(1000, 5000)
                total_earned = random.randint(50000, 100000)
                coins = random.randint(5000, 10000)
                quanhash = random.randint(1000, 5000)
                vip_level = 0
            else:
                # Low activity (new users)
                total_taps = random.randint(100, 1000)
                total_earned = random.randint(10000, 50000)
                coins = random.randint(1000, 5000)
                quanhash = random.randint(500, 1000)
                vip_level = 0
            
            # Random last active time (within last 24 hours)
            last_active = datetime.utcnow() - timedelta(hours=random.randint(0, 24))
            
            # Create user
            user = User(
                telegram_id=telegram_id,
                username=username,
                coins=coins,
                quanhash=quanhash,
                energy=random.randint(500, 1000),
                max_energy=1000,
                total_taps=total_taps,
                total_earned=float(total_earned),
                total_mined=float(quanhash),
                vip_level=vip_level,
                last_active=last_active,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                updated_at=datetime.utcnow()
            )
            
            # Set VIP badge if VIP
            if vip_level > 0:
                badges = {1: "Bronze", 2: "Silver", 3: "Gold", 4: "Platinum", 5: "Diamond", 6: "Absolute"}
                user.vip_badge = badges.get(vip_level, None)
                user.has_top_place = True if vip_level >= 3 else False
                user.has_golden_profile = True if vip_level >= 3 else False
            
            db.add(user)
            
            if (i + 1) % 20 == 0:
                print(f"Generated {i + 1} bots...")
        
        db.flush()  # Get IDs before commit
        db.commit()
        print(f"Successfully generated 137 bot users!")
        print(f"Total users in database: {db.query(User).count()}")

if __name__ == '__main__':
    generate_bot_users()

