#!/usr/bin/env python3
"""
Quantum Nexus Web Server
Server for Telegram Web App
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import get_db
from models import User, MiningMachine, UserCard, Withdrawal, SupportTicket, UserAchievement, Transaction
from utils import calculate_offline_income
from datetime import datetime, timedelta
from config import BASE_TAP_REWARD, ENERGY_COST_PER_TAP, MAX_ENERGY
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Helper functions for level and rating calculation
def calculate_level(experience):
    """Calculate level based on experience"""
    if experience <= 0:
        return 1
    level = int((experience / 100) ** 0.5) + 1
    return min(level, 100)  # Max level 100

def calculate_experience(total_earned, total_taps, vip_level):
    """Calculate experience from user activity"""
    base_exp = (total_earned or 0) * 0.01  # 1% from earned coins
    tap_bonus = (total_taps or 0) * 0.1  # Per tap
    vip_bonus = (vip_level or 0) * 1000  # VIP bonus
    return base_exp + tap_bonus + vip_bonus

def calculate_rating(coins, total_earned, total_taps, vip_level, level):
    """Calculate overall rating for ranking"""
    coins_score = (coins or 0) * 0.01
    earned_score = (total_earned or 0) * 0.1
    taps_score = (total_taps or 0) * 0.05
    vip_score = (vip_level or 0) * 1000000  # VIP always on top
    level_score = (level or 1) * 10000
    return coins_score + earned_score + taps_score + vip_score + level_score

@app.route('/')
def index():
    """Serve web app"""
    return send_from_directory('.', 'web_app.html')

@app.route('/game_v4.html')
def game_v4():
    """Serve new version of web app"""
    return send_from_directory('.', 'web_app.html')

@app.route('/admin')
@app.route('/admin.html')
def admin():
    """Serve admin panel"""
    return send_from_directory('.', 'admin.html')

@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    """Get all users for admin panel"""
    try:
        with get_db() as db:
            users = db.query(User).all()
            result = {
                'users': [{
                    'telegram_id': u.telegram_id,
                    'username': u.username,
                    'coins': u.coins,
                    'quanhash': u.quanhash,
                    'energy': u.energy,
                    'max_energy': u.max_energy,
                    'total_taps': u.total_taps,
                    'total_earned': u.total_earned,
                    'referrals_count': u.referrals_count,
                    'is_banned': getattr(u, 'is_banned', False),
                    'is_frozen': getattr(u, 'is_frozen', False),
                    'vip_level': getattr(u, 'vip_level', 0),
                    'vip_badge': getattr(u, 'vip_badge', None),
                    'has_premium_support': getattr(u, 'has_premium_support', False),
                    'has_golden_profile': getattr(u, 'has_golden_profile', False),
                    'has_top_place': getattr(u, 'has_top_place', False),
                    'has_unique_design': getattr(u, 'has_unique_design', False)
                } for u in users]
            }
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/add_coins', methods=['POST'])
def add_coins():
    """Add coins to user"""
    try:
        data = request.json
        user_id = data.get('user_id')
        amount = data.get('amount')
        
        if not user_id or not amount:
            return jsonify({'error': 'Missing parameters'}), 400
        
        db = next(get_db())
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.coins += amount
        db.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/set_energy', methods=['POST'])
def set_energy():
    """Set user energy"""
    try:
        data = request.json
        user_id = data.get('user_id')
        energy = data.get('energy')
        
        if not user_id or energy is None:
            return jsonify({'error': 'Missing parameters'}), 400
        
        db = next(get_db())
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.energy = min(energy, user.max_energy)
        db.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user_data', methods=['POST'])
def get_user_data():
    """Get user data"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        # Try to get user_id from init_data if not provided
        if not user_id:
            # Try multiple headers that Telegram might send
            init_data = request.headers.get('X-Telegram-Init-Data') or request.headers.get('Telegram-Init-Data') or request.headers.get('X-Init-Data')
            if init_data:
                print(f"[DEBUG] Found init_data header: {init_data[:100]}")
                # Try to extract user_id from init_data
                import urllib.parse
                init_params = urllib.parse.parse_qs(init_data)
                print(f"[DEBUG] Parsed params keys: {list(init_params.keys())}")
                if 'user' in init_params:
                    import json
                    try:
                        user_data = json.loads(init_params['user'][0])
                        user_id = user_data.get('id')
                        print(f"Extracted user_id from init_data: {user_id}")
                    except Exception as e:
                        print(f"Failed to parse init_data user: {e}")
        
        print(f"[USER_DATA] Request with user_id: {user_id}")
        
        if not user_id:
            return jsonify({'coins': 0, 'quanhash': 0, 'energy': 1000, 'max_energy': 1000, 'total_taps': 0, 'total_earned': 0, 'username': 'Unknown'}), 200
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                # Return default values if user not found (need to start bot first)
                return jsonify({'coins': 0, 'quanhash': 0, 'energy': 1000, 'max_energy': 1000, 'total_taps': 0, 'total_earned': 0, 'username': 'Unknown', 'message': 'Start bot first'}), 200
            
            # Check if user is banned or frozen (safe check for old DB schema)
            if hasattr(user, 'is_banned') and user.is_banned:
                return jsonify({
                    'error': 'Вы заблокированы',
                    'is_banned': True,
                    'ban_reason': getattr(user, 'ban_reason', None)
                }), 403
            
            if hasattr(user, 'is_frozen') and user.is_frozen:
                return jsonify({
                    'error': 'Ваш аккаунт заморожен',
                    'is_frozen': True
                }), 403
            
            # Calculate passive income
            passive_coins_per_hour = 0
            passive_hash_per_hour = 0
            
            for card in user.cards:
                if card.is_active:
                    passive_coins_per_hour += card.income_per_minute * 60
            
            for machine in user.machines:
                if machine.is_active:
                    passive_hash_per_hour += machine.hash_rate * 3600
            
            # Calculate time since last update
            current_time = datetime.utcnow()
            
            # Energy regeneration is now handled by the frontend
            # No server-side regeneration to avoid conflicts
            
            # Update passive coins if user has cards
            if passive_coins_per_hour > 0 and user.last_passive_update:
                time_diff = (current_time - user.last_passive_update).total_seconds()
                if time_diff > 0:
                    coins_to_add = (passive_coins_per_hour / 3600) * time_diff
                    user.coins += coins_to_add
                    user.last_passive_update = current_time
            
            # Update passive hash if user has machines
            if passive_hash_per_hour > 0 and user.last_hash_update:
                time_diff = (current_time - user.last_hash_update).total_seconds()
                if time_diff > 0:
                    hash_to_add = (passive_hash_per_hour / 3600) * time_diff
                    user.quanhash += hash_to_add
                    user.last_hash_update = current_time
            
            # Initialize last_passive_update if not set
            if not user.last_passive_update:
                user.last_passive_update = current_time
            if not user.last_hash_update:
                user.last_hash_update = current_time
            
            # Calculate and add referral passive income
            # This is calculated from referrals' total_earned
            if not hasattr(user, 'last_referral_update'):
                # Add attribute if doesn't exist
                from sqlalchemy import Column, DateTime
                if not hasattr(User, 'last_referral_update'):
                    # This would need a migration, but for now we'll calculate on-the-fly
                    pass
                user.last_referral_update = current_time
            
            # Update referral income every minute (to avoid spam)
            time_diff = (current_time - (user.last_referral_update if hasattr(user, 'last_referral_update') and user.last_referral_update else current_time)).total_seconds()
            if time_diff >= 60 or not hasattr(user, 'last_referral_update') or not user.last_referral_update:
                referrals = db.query(User).filter_by(referred_by=user.id).all()
                new_referral_income = 0.0
                
                for ref in referrals:
                    ref_total_earned = ref.total_earned or 0.0
                    # Base income percentage (5% for regular users, 10% for VIP)
                    base_percent = 0.05
                    if getattr(ref, 'vip_level', 0) > 0:
                        base_percent = 0.10  # VIP users give 10% instead of 5%
                    
                    # Income from this referral = percentage of their total_earned
                    ref_income = ref_total_earned * base_percent
                    new_referral_income += ref_income
                
                # Update referral income and add to coins
                income_diff = new_referral_income - (user.referral_income or 0.0)
                if income_diff > 0:
                    user.referral_income = new_referral_income
                    user.coins += income_diff  # Add the difference to coins
                    user.total_earned += income_diff  # Count as earned
                    db.commit()
            
            # Check for active multiplier
            active_multiplier = getattr(user, 'active_multiplier', 1.0)
            multiplier_expires_at = getattr(user, 'multiplier_expires_at', None)
            boost_expires_at = 0
            if multiplier_expires_at:
                boost_expires_at = int(multiplier_expires_at.timestamp() * 1000) if hasattr(multiplier_expires_at, 'timestamp') else 0
            
            # Get username
            username = getattr(user, 'username', 'Unknown')
            if username and isinstance(username, str):
                username = username[:50]  # Limit length
            else:
                username = 'Unknown'
            
            # Get purchased cards and machines
            user_cards = []
            try:
                # Card definitions to map card_type to name
                per_minute_cards = [
                    {'name': '⚡ Энергетический генератор', 'desc': 'Производит 0.5 коинов/мин', 'base_income': 0.5, 'base_price': 50000, 'rarity': 'common'},
                    {'name': '🔋 Мощная батарея', 'desc': 'Производит 1.2 коинов/мин', 'base_income': 1.2, 'base_price': 75000, 'rarity': 'common'},
                    {'name': '💎 Драгоценный кристалл', 'desc': 'Производит 2.5 коинов/мин', 'base_income': 2.5, 'base_price': 120000, 'rarity': 'rare'},
                    {'name': '⭐ Звездное ядро', 'desc': 'Производит 4.0 коинов/мин', 'base_income': 4.0, 'base_price': 200000, 'rarity': 'rare'},
                    {'name': '🔥 Плазменный реактор', 'desc': 'Производит 6.5 коинов/мин', 'base_income': 6.5, 'base_price': 350000, 'rarity': 'epic'},
                    {'name': '⚛️ Квантовый генератор', 'desc': 'Производит 10.0 коинов/мин', 'base_income': 10.0, 'base_price': 550000, 'rarity': 'epic'},
                    {'name': '🌌 Галактический мотор', 'desc': 'Производит 15.0 коинов/мин', 'base_income': 15.0, 'base_price': 850000, 'rarity': 'legendary'},
                    {'name': '👑 Императорский трон', 'desc': 'Производит 22.0 коинов/мин', 'base_income': 22.0, 'base_price': 1300000, 'rarity': 'legendary'},
                    {'name': '🐉 Драконье сердце', 'desc': 'Производит 30.0 коинов/мин', 'base_income': 30.0, 'base_price': 2000000, 'rarity': 'legendary'},
                    {'name': '💫 Бесконечность', 'desc': 'Производит 40.0 коинов/мин', 'base_income': 40.0, 'base_price': 3000000, 'rarity': 'legendary'},
                    {'name': '🧠 Нейросеть', 'desc': 'Производит 5.5 коинов/мин', 'base_income': 5.5, 'base_price': 280000, 'rarity': 'epic'},
                    {'name': '🪐 Планетарный коллайдер', 'desc': 'Производит 18.0 коинов/мин', 'base_income': 18.0, 'base_price': 1000000, 'rarity': 'legendary'},
                    {'name': '🎯 Точностный лазер', 'desc': 'Производит 3.0 коинов/мин', 'base_income': 3.0, 'base_price': 150000, 'rarity': 'rare'},
                    {'name': '🛸 Внеземной чип', 'desc': 'Производит 14.0 коинов/мин', 'base_income': 14.0, 'base_price': 750000, 'rarity': 'epic'},
                    {'name': '⚗️ Алхимический аппарат', 'desc': 'Производит 8.5 коинов/мин', 'base_income': 8.5, 'base_price': 450000, 'rarity': 'epic'},
                    {'name': '🧪 Биомедиум', 'desc': 'Производит 12.0 коинов/мин', 'base_income': 12.0, 'base_price': 650000, 'rarity': 'epic'},
                    {'name': '🌠 Новойдовый ускоритель', 'desc': 'Производит 25.0 коинов/мин', 'base_income': 25.0, 'base_price': 1700000, 'rarity': 'legendary'},
                    {'name': '🔬 Крио-модуль', 'desc': 'Производит 9.0 коинов/мин', 'base_income': 9.0, 'base_price': 500000, 'rarity': 'epic'},
                    {'name': '💻 Киберсистема', 'desc': 'Производит 35.0 коинов/мин', 'base_income': 35.0, 'base_price': 2500000, 'rarity': 'legendary'},
                    {'name': '🏆 Победный трофей', 'desc': 'Производит 50.0 коинов/мин', 'base_income': 50.0, 'base_price': 5000000, 'rarity': 'legendary'},
                ]
                per_hour_cards = [
                    {'name': '🟢 Базовая ферма', 'desc': 'Производит 5 коинов/час', 'base_income': 5, 'base_price': 1000, 'rarity': 'common'},
                    {'name': '🌱 Росток успеха', 'desc': 'Производит 12 коинов/час', 'base_income': 12, 'base_price': 2500, 'rarity': 'common'},
                    {'name': '🍀 Четырехлистник', 'desc': 'Производит 20 коинов/час', 'base_income': 20, 'base_price': 5000, 'rarity': 'common'},
                    {'name': '⚡ Ускоритель', 'desc': 'Производит 35 коинов/час', 'base_income': 35, 'base_price': 8000, 'rarity': 'rare'},
                    {'name': '🔵 Редкий артефакт', 'desc': 'Производит 55 коинов/час', 'base_income': 55, 'base_price': 15000, 'rarity': 'rare'},
                    {'name': '🟣 Эпический кристалл', 'desc': 'Производит 90 коинов/час', 'base_income': 90, 'base_price': 30000, 'rarity': 'epic'},
                    {'name': '⭐ Звездная пыль', 'desc': 'Производит 140 коинов/час', 'base_income': 140, 'base_price': 50000, 'rarity': 'epic'},
                    {'name': '🔥 Огненное ядро', 'desc': 'Производит 220 коинов/час', 'base_income': 220, 'base_price': 85000, 'rarity': 'legendary'},
                    {'name': '💎 Кристалл удачи', 'desc': 'Производит 350 коинов/час', 'base_income': 350, 'base_price': 150000, 'rarity': 'legendary'},
                    {'name': '👑 Корона власти', 'desc': 'Производит 550 коинов/час', 'base_income': 550, 'base_price': 250000, 'rarity': 'legendary'},
                    {'name': '🏆 Чемпионство', 'desc': 'Производит 850 коинов/час', 'base_income': 850, 'base_price': 400000, 'rarity': 'legendary'},
                    {'name': '🚀 Ракета мечты', 'desc': 'Производит 1300 коинов/час', 'base_income': 1300, 'base_price': 650000, 'rarity': 'legendary'},
                    {'name': '🐉 Драконье сокровище', 'desc': 'Производит 2000 коинов/час', 'base_income': 2000, 'base_price': 1000000, 'rarity': 'legendary'},
                    {'name': '🌌 Галактика', 'desc': 'Производит 3100 коинов/час', 'base_income': 3100, 'base_price': 1800000, 'rarity': 'legendary'},
                    {'name': '⚛️ Квантовый скачок', 'desc': 'Производит 5000 коинов/час', 'base_income': 5000, 'base_price': 3000000, 'rarity': 'legendary'},
                    {'name': '💫 Вечность', 'desc': 'Производит 8000 коинов/час', 'base_income': 8000, 'base_price': 5000000, 'rarity': 'legendary'},
                    {'name': '🌈 Радужный мост', 'desc': 'Производит 13000 коинов/час', 'base_income': 13000, 'base_price': 8500000, 'rarity': 'legendary'},
                    {'name': '🌠 Звездопад', 'desc': 'Производит 21000 коинов/час', 'base_income': 21000, 'base_price': 15000000, 'rarity': 'legendary'},
                    {'name': '🎆 Новогодний салют', 'desc': 'Производит 34000 коинов/час', 'base_income': 34000, 'base_price': 25000000, 'rarity': 'legendary'},
                    {'name': '🌟 Супернова', 'desc': 'Производит 55000 коинов/час', 'base_income': 55000, 'base_price': 50000000, 'rarity': 'legendary'},
                ]
                
                for card in user.cards:
                    if hasattr(card, 'is_active') and card.is_active:
                        # Map card_type to name
                        card_name = 'Unknown Card'
                        card_type = getattr(card, 'card_type', None)
                        if card_type:
                            if card_type.startswith('card_min_'):
                                idx = int(card_type.split('_')[2]) if card_type.split('_')[2].isdigit() else 0
                                if idx < len(per_minute_cards):
                                    card_name = per_minute_cards[idx]['name']
                            elif card_type.startswith('card_hour_'):
                                idx = int(card_type.split('_')[2]) if card_type.split('_')[2].isdigit() else 0
                                if idx < len(per_hour_cards):
                                    card_name = per_hour_cards[idx]['name']
                            elif hasattr(card, 'name') and card.name:
                                card_name = card.name
                        
                        user_cards.append({
                            'name': card_name,
                            'income': getattr(card, 'income_per_minute', 0) or 0,
                            'type': 'permanent'
                        })
            except Exception as e:
                print(f"Error getting cards: {e}")
                import traceback
                traceback.print_exc()
                user_cards = []
            
            user_machines = []
            try:
                for machine in user.machines:
                    if hasattr(machine, 'is_active') and machine.is_active:
                        user_machines.append({
                            'name': getattr(machine, 'name', 'Unknown Machine'),
                            'hash_rate': getattr(machine, 'hash_rate', 0) or 0,
                            'type': 'permanent'
                        })
            except Exception as e:
                print(f"Error getting machines: {e}")
                import traceback
                traceback.print_exc()
                user_machines = []
            
            # Calculate experience, level, and rating for current user
            vip_level = getattr(user, 'vip_level', 0) or 0
            experience = calculate_experience(user.total_earned, user.total_taps, vip_level)
            level = calculate_level(experience)
            rating = calculate_rating(user.coins, user.total_earned, user.total_taps, vip_level, level)
            
            # Get shop item levels
            import json
            return jsonify({
                'id': user.id,  # Add database ID
                'coins': user.coins,
                'quanhash': user.quanhash,
                'energy': user.energy,
                'max_energy': user.max_energy,
                'energy_regen_rate': getattr(user, 'energy_regen_rate', 1.0),
                'total_taps': user.total_taps,
                'total_earned': user.total_earned,
                'passive_coins_per_hour': passive_coins_per_hour,
                'passive_hash_per_hour': passive_hash_per_hour,
                'auto_tap_enabled': getattr(user, 'auto_tap_enabled', False),
                'auto_tap_level': getattr(user, 'auto_tap_level', 0),
                'auto_tap_speed': getattr(user, 'auto_tap_speed', 2.0),
                'auto_tap_expires_at': int(user.auto_tap_expires_at.timestamp() * 1000) if hasattr(user, 'auto_tap_expires_at') and user.auto_tap_expires_at else 0,
                'vip_level': getattr(user, 'vip_level', 0),
                'vip_badge': getattr(user, 'vip_badge', None),
                'has_premium_support': getattr(user, 'has_premium_support', False),
                'has_golden_profile': getattr(user, 'has_golden_profile', False),
                'has_top_place': getattr(user, 'has_top_place', False),
                'has_unique_design': getattr(user, 'has_unique_design', False),
                'active_multiplier': active_multiplier,
                'boost_expires_at': boost_expires_at,
                'username': username,
                'cards': user_cards,
                'machines': user_machines,
                'tap_boost_levels': json.loads(user.tap_boost_levels or '{}'),
                'energy_buy_levels': json.loads(user.energy_buy_levels or '{}'),
                'energy_expand_levels': json.loads(user.energy_expand_levels or '{}'),
                'level': level,
                'experience': round(experience, 2),
                'rating': round(rating, 2),
                'sound_enabled': getattr(user, 'sound_enabled', True),  # Default to True if not set
                'referral_income': user.referral_income or 0.0,
                'referrals_count': user.referrals_count or 0
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tap', methods=['POST'])
def tap():
    """Handle tap action"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required. Please start the bot first.'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found. Please start the bot first.'}), 404
            
            # Check energy
            if user.energy < ENERGY_COST_PER_TAP:
                return jsonify({'success': False, 'error': 'Недостаточно энергии!'})
            
            # Calculate VIP bonus multiplier
            vip_level = getattr(user, 'vip_level', 0)
            vip_multiplier = 1.0
            
            # Apply VIP bonuses
            if vip_level >= 1:
                vip_multiplier += 0.2  # 20% bonus for Bronze
            if vip_level >= 2:
                vip_multiplier += 0.3  # 50% total bonus for Silver
            if vip_level >= 3:
                vip_multiplier += 0.5  # 100% total bonus for Gold
            if vip_level >= 4:
                vip_multiplier += 0.5  # 150% total bonus for Platinum
            if vip_level >= 5:
                vip_multiplier += 1.0  # 250% total bonus for Diamond
            if vip_level >= 6:
                vip_multiplier += 2.0  # 450% total bonus for Absolute VIP
            
            # Calculate reward with VIP bonus and tap boost
            reward = BASE_TAP_REWARD * vip_multiplier
            
            # Apply tap boost (active_multiplier > 1 means tap boost is active)
            tap_boost = 1
            if user.active_multiplier > 1:
                # All multipliers > 1 are tap boosts (2 = +1 tap, 3 = +2 taps, etc.)
                tap_boost = int(user.active_multiplier)
                # Apply tap boost to reward (more taps = more coins)
                reward = reward * tap_boost
                # DON'T reset multiplier - keep tap boost active
            
            # Calculate energy cost based on tap boost
            energy_cost = ENERGY_COST_PER_TAP
            if user.active_multiplier > 1:
                # More tap boost = more energy cost
                energy_cost = energy_cost * (user.active_multiplier * 0.5)  # 50% increase per tap boost level
            
            # VIP users get lower energy cost
            if vip_level >= 3:
                energy_cost = max(0.5, energy_cost * 0.5)  # 50% energy cost for Gold+
            
            # Update user
            user.coins += reward
            user.energy -= energy_cost
            user.total_taps += tap_boost  # Apply tap boost to total taps
            user.total_earned += reward
            user.last_active = datetime.utcnow()
            
            db.commit()
            
            return jsonify({'success': True, 'reward': int(reward), 'vip_bonus': vip_multiplier})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['POST'])
def get_stats():
    """Get user statistics"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        db = next(get_db())
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'total_taps': user.total_taps,
            'total_earned': user.total_earned,
            'total_mined': user.total_mined,
            'coins': user.coins,
            'quanhash': user.quanhash
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shop', methods=['POST'])
def get_shop():
    """Get shop items by category"""
    try:
        data = request.json
        user_id = data.get('user_id')
        category = data.get('category', 'boosts')  # boosts, energy, cards, auto
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            # Try to find user by telegram_id first, then by id
            user = db.query(User).filter_by(telegram_id=user_id).first()
            if not user:
                user = db.query(User).filter_by(id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Define 4 categories with 20 items each
            if category == 'boosts':
                # Get user's purchased boosts count
                user_boosts = db.query(UserCard).filter_by(user_id=user.id, card_type='boosts').count() if hasattr(UserCard, 'card_type') else 0
                items = []
                for i in range(20):
                    level = 1  # Static level for now
                    base_price = 1000 * (i+1)
                    mult_value = 2 if i==0 else (5 if i==1 else 10)
                    items.append({
                        'id': f'boost_{i}',
                        'name': f'⚡ Множитель x{mult_value}',
                        'description': f'🔮 Увеличивает доход от тапов на {mult_value}х на 24 часа',
                        'price': base_price,
                        'level': level,
                        'item_type': 'multiplier_2x' if i==0 else ('multiplier_5x' if i==1 else 'multiplier_10x')
                    })
            elif category == 'energy':
                # Get user's purchased energy boosts count
                user_energy_boosts = db.query(UserCard).filter_by(user_id=user.id, card_type='energy').count() if hasattr(UserCard, 'card_type') else 0
                items = []
                for i in range(20):
                    level = (user_energy_boosts % 10) + 1
                    base_price = 500 * (i+1)
                    current_price = int(base_price * (1.02 ** (level - 1)))
                    amount = 50 * (i+1)
                    items.append({
                        'id': f'energy_{i}',
                        'name': f'⚡ Энергия +{amount}',
                        'description': f'⚡ Восполняет энергию на {amount} единиц',
                        'price': 500 * (i+1),
                        'level': 1,
                        'item_type': 'energy',
                        'amount': amount
                    })
            elif category == 'cards':
                # 40 cards: 20 per minute, 20 per hour
                # Per minute cards (expensive)
                per_minute_cards = [
                    {'name': '⚡ Энергетический генератор', 'desc': 'Производит 0.5 коинов/мин', 'base_income': 0.5, 'base_price': 50000, 'rarity': 'common'},
                    {'name': '🔋 Мощная батарея', 'desc': 'Производит 1.2 коинов/мин', 'base_income': 1.2, 'base_price': 75000, 'rarity': 'common'},
                    {'name': '💎 Драгоценный кристалл', 'desc': 'Производит 2.5 коинов/мин', 'base_income': 2.5, 'base_price': 120000, 'rarity': 'rare'},
                    {'name': '⭐ Звездный ядро', 'desc': 'Производит 4.0 коинов/мин', 'base_income': 4.0, 'base_price': 200000, 'rarity': 'rare'},
                    {'name': '🔥 Плазменный реактор', 'desc': 'Производит 6.5 коинов/мин', 'base_income': 6.5, 'base_price': 350000, 'rarity': 'epic'},
                    {'name': '⚛️ Квантовый генератор', 'desc': 'Производит 10.0 коинов/мин', 'base_income': 10.0, 'base_price': 550000, 'rarity': 'epic'},
                    {'name': '🌌 Галактический мотор', 'desc': 'Производит 15.0 коинов/мин', 'base_income': 15.0, 'base_price': 850000, 'rarity': 'legendary'},
                    {'name': '👑 Императорский трон', 'desc': 'Производит 22.0 коинов/мин', 'base_income': 22.0, 'base_price': 1300000, 'rarity': 'legendary'},
                    {'name': '🐉 Драконье сердце', 'desc': 'Производит 30.0 коинов/мин', 'base_income': 30.0, 'base_price': 2000000, 'rarity': 'legendary'},
                    {'name': '💫 Бесконечность', 'desc': 'Производит 40.0 коинов/мин', 'base_income': 40.0, 'base_price': 3000000, 'rarity': 'legendary'},
                    {'name': '🧠 Нейросеть', 'desc': 'Производит 5.5 коинов/мин', 'base_income': 5.5, 'base_price': 280000, 'rarity': 'epic'},
                    {'name': '🪐 Планетарный коллайдер', 'desc': 'Производит 18.0 коинов/мин', 'base_income': 18.0, 'base_price': 1000000, 'rarity': 'legendary'},
                    {'name': '🎯 Точностный лазер', 'desc': 'Производит 3.0 коинов/мин', 'base_income': 3.0, 'base_price': 150000, 'rarity': 'rare'},
                    {'name': '🛸 Внеземной чип', 'desc': 'Производит 14.0 коинов/мин', 'base_income': 14.0, 'base_price': 750000, 'rarity': 'epic'},
                    {'name': '⚗️ Алхимический аппарат', 'desc': 'Производит 8.5 коинов/мин', 'base_income': 8.5, 'base_price': 450000, 'rarity': 'epic'},
                    {'name': '🧪 Биомедиум', 'desc': 'Производит 12.0 коинов/мин', 'base_income': 12.0, 'base_price': 650000, 'rarity': 'epic'},
                    {'name': '🌠 Новойдовый ускоритель', 'desc': 'Производит 25.0 коинов/мин', 'base_income': 25.0, 'base_price': 1700000, 'rarity': 'legendary'},
                    {'name': '🔬 Крио-модуль', 'desc': 'Производит 9.0 коинов/мин', 'base_income': 9.0, 'base_price': 500000, 'rarity': 'epic'},
                    {'name': '💻 Киберсистема', 'desc': 'Производит 35.0 коинов/мин', 'base_income': 35.0, 'base_price': 2500000, 'rarity': 'legendary'},
                    {'name': '🏆 Победный трофей', 'desc': 'Производит 50.0 коинов/мин', 'base_income': 50.0, 'base_price': 5000000, 'rarity': 'legendary'},
                ]
                # Per hour cards (main income)
                per_hour_cards = [
                    {'name': '🟢 Базовая ферма', 'desc': 'Производит 5 коинов/час', 'base_income': 5, 'base_price': 1000, 'rarity': 'common'},
                    {'name': '🌱 Росток успеха', 'desc': 'Производит 12 коинов/час', 'base_income': 12, 'base_price': 2500, 'rarity': 'common'},
                    {'name': '🍀 Четырехлистник', 'desc': 'Производит 20 коинов/час', 'base_income': 20, 'base_price': 5000, 'rarity': 'common'},
                    {'name': '⚡ Ускоритель', 'desc': 'Производит 35 коинов/час', 'base_income': 35, 'base_price': 8000, 'rarity': 'rare'},
                    {'name': '🔵 Редкий артефакт', 'desc': 'Производит 55 коинов/час', 'base_income': 55, 'base_price': 15000, 'rarity': 'rare'},
                    {'name': '🟣 Эпический кристалл', 'desc': 'Производит 90 коинов/час', 'base_income': 90, 'base_price': 30000, 'rarity': 'epic'},
                    {'name': '⭐ Звездная пыль', 'desc': 'Производит 140 коинов/час', 'base_income': 140, 'base_price': 50000, 'rarity': 'epic'},
                    {'name': '🔥 Огненное ядро', 'desc': 'Производит 220 коинов/час', 'base_income': 220, 'base_price': 85000, 'rarity': 'legendary'},
                    {'name': '💎 Кристалл удачи', 'desc': 'Производит 350 коинов/час', 'base_income': 350, 'base_price': 150000, 'rarity': 'legendary'},
                    {'name': '👑 Корона власти', 'desc': 'Производит 550 коинов/час', 'base_income': 550, 'base_price': 250000, 'rarity': 'legendary'},
                    {'name': '🏆 Чемпионство', 'desc': 'Производит 850 коинов/час', 'base_income': 850, 'base_price': 400000, 'rarity': 'legendary'},
                    {'name': '🚀 Ракета мечты', 'desc': 'Производит 1300 коинов/час', 'base_income': 1300, 'base_price': 650000, 'rarity': 'legendary'},
                    {'name': '🐉 Драконье сокровище', 'desc': 'Производит 2000 коинов/час', 'base_income': 2000, 'base_price': 1000000, 'rarity': 'legendary'},
                    {'name': '🌌 Галактика', 'desc': 'Производит 3100 коинов/час', 'base_income': 3100, 'base_price': 1800000, 'rarity': 'legendary'},
                    {'name': '⚛️ Квантовый скачок', 'desc': 'Производит 5000 коинов/час', 'base_income': 5000, 'base_price': 3000000, 'rarity': 'legendary'},
                    {'name': '💫 Вечность', 'desc': 'Производит 8000 коинов/час', 'base_income': 8000, 'base_price': 5000000, 'rarity': 'legendary'},
                    {'name': '🌈 Радужный мост', 'desc': 'Производит 13000 коинов/час', 'base_income': 13000, 'base_price': 8500000, 'rarity': 'legendary'},
                    {'name': '🌠 Звездопад', 'desc': 'Производит 21000 коинов/час', 'base_income': 21000, 'base_price': 15000000, 'rarity': 'legendary'},
                    {'name': '🎆 Новогодний салют', 'desc': 'Производит 34000 коинов/час', 'base_income': 34000, 'base_price': 25000000, 'rarity': 'legendary'},
                    {'name': '🌟 Супернова', 'desc': 'Производит 55000 коинов/час', 'base_income': 55000, 'base_price': 50000000, 'rarity': 'legendary'},
                ]
                
                items = []
                # Check if user_cards table exists
                try:
                    user_cards = db.query(UserCard).filter_by(user_id=user.id).all()
                    print(f"Successfully queried user_cards table for user {user_id}")
                except Exception as e:
                    print(f"Error querying user_cards table: {e}")
                    return jsonify({'success': False, 'error': 'Database error'})
                
                user_card_counts = {}
                for uc in user_cards:
                    user_card_counts[uc.card_type] = user_card_counts.get(uc.card_type, 0) + 1
                
                print(f"User {user_id} cards: {user_card_counts}")
                print(f"All user cards from DB: {[(uc.card_type, uc.card_level, uc.income_per_minute) for uc in user_cards]}")
                
                for i, template in enumerate(per_minute_cards):
                    card_key = f"card_min_{i}"
                    purchases = user_card_counts.get(card_key, 0)
                    level = min(purchases + 1, 300)
                    price = int(template['base_price'] * (1.15 ** (level - 1)))
                    income = template['base_income'] * (1.10 ** (level - 1))
                    
                    print(f"PER MINUTE Card {card_key}: purchases={purchases}, level={level}, price={price}, income={income}")
                    
                    # Remove locking - all cards are available
                    is_locked = False
                    
                    items.append({
                        'id': card_key,
                        'name': template['name'],
                        'description': template['desc'],
                        'base_price': template['base_price'],
                        'price': price,
                        'level': level,
                        'rarity': template['rarity'],
                        'income': income,
                        'income_per_min': income,
                        'income_type': 'per_minute',
                        'type': 'card',
                        'currency': 'coins',
                        'is_locked': is_locked
                    })
                
                for i, template in enumerate(per_hour_cards):
                    card_key = f"card_hour_{i}"
                    purchases = user_card_counts.get(card_key, 0)
                    level = min(purchases + 1, 300)
                    price = int(template['base_price'] * (1.15 ** (level - 1)))
                    income_per_hour = template['base_income'] * (1.10 ** (level - 1))
                    income_per_min = round(income_per_hour / 60, 2)
                    
                    print(f"PER HOUR Card {card_key}: purchases={purchases}, level={level}, price={price}, income_per_hour={income_per_hour}, income_per_min={income_per_min}")
                    
                    # Remove locking - all cards are available
                    is_locked = False
                    
                    items.append({
                        'id': card_key,
                        'name': template['name'],
                        'description': template['desc'],
                        'base_price': template['base_price'],
                        'price': price,
                        'level': level,
                        'rarity': template['rarity'],
                        'income': income_per_hour,
                        'income_per_min': income_per_min,
                        'income_type': 'per_hour',
                        'type': 'card',
                        'currency': 'coins',
                        'is_locked': is_locked
                    })
            else:  # auto
                # Get user's purchased auto-bots count
                user_auto_bots = db.query(UserCard).filter_by(user_id=user.id, card_type='auto').count() if hasattr(UserCard, 'card_type') else 0
                items = []
                for i in range(20):
                    level = (user_auto_bots % 10) + 1
                    base_price = 10000 * (i+1)
                    current_price = int(base_price * (1.02 ** (level - 1)))
                    items.append({
                        'id': f'auto_{i}',
                        'name': f'🤖 Авто-бот ур. {i+1}',
                        'description': f'Автоматически тапает {2 + i} раз в секунду',
                        'price': current_price,
                        'level': level,
                        'item_type': 'auto_bot',
                        'taps_per_sec': 2 + i
                    })
            
            return jsonify({
                'coins': user.coins,
                'quanhash': user.quanhash,
                'category': category,
                'items': items
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mining', methods=['POST'])
def get_mining():
    """Get mining data with categories"""
    try:
        data = request.json
        user_id = data.get('user_id')
        category = data.get('category', 'coins')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Get machine levels from user JSON (source of truth)
            import json
            mining_levels = {}
            if category == 'coins':
                mining_levels = json.loads(user.mining_coins_levels or '{}')
            elif category == 'quanhash':
                mining_levels = json.loads(user.mining_quanhash_levels or '{}')
            elif category == 'vip':
                mining_levels = json.loads(user.mining_vip_levels or '{}')
            
            # Machine definitions for calculating income (ALL categories)
            machines_defs = {
                'coins': [
                    {'id': 'miner_cpu', 'name': 'CPU Майнер', 'baseHashPerHour': 10, 'emoji': '💻'},
                    {'id': 'miner_gpu', 'name': 'GPU Майнер', 'baseHashPerHour': 50, 'emoji': '🎮'},
                    {'id': 'miner_asic', 'name': 'ASIC Риг', 'baseHashPerHour': 200, 'emoji': '⚡'},
                    {'id': 'miner_quantum', 'name': 'Quantum Майнер', 'baseHashPerHour': 800, 'emoji': '💎'},
                    {'id': 'miner_server', 'name': 'Server Ферма', 'baseHashPerHour': 3000, 'emoji': '🖥️'},
                    {'id': 'miner_cloud', 'name': 'Cloud Риг', 'baseHashPerHour': 12000, 'emoji': '☁️'},
                    {'id': 'miner_data', 'name': 'Data Центр', 'baseHashPerHour': 50000, 'emoji': '🏢'},
                    {'id': 'miner_quantum_farm', 'name': 'Quantum Ферма', 'baseHashPerHour': 200000, 'emoji': '🌌'},
                    {'id': 'miner_neural', 'name': 'Neural Майнер', 'baseHashPerHour': 800000, 'emoji': '🧠'},
                    {'id': 'miner_cosmic', 'name': 'Cosmic Станция', 'baseHashPerHour': 3200000, 'emoji': '🚀'}
                ],
                'quanhash': [
                    {'id': 'hash_quantum_core', 'name': 'Quantum Ядро', 'baseHashPerHour': 80, 'emoji': '⚛️'},
                    {'id': 'hash_plasma_rig', 'name': 'Plasma Риг', 'baseHashPerHour': 400, 'emoji': '🔥'},
                    {'id': 'hash_stellar', 'name': 'Stellar Блок', 'baseHashPerHour': 1800, 'emoji': '⭐'},
                    {'id': 'hash_cosmic_flux', 'name': 'Cosmic Поток', 'baseHashPerHour': 7000, 'emoji': '🌊'},
                    {'id': 'hash_nova', 'name': 'Nova Ускоритель', 'baseHashPerHour': 28000, 'emoji': '🌟'},
                    {'id': 'hash_galaxy', 'name': 'Galaxy Матрица', 'baseHashPerHour': 110000, 'emoji': '🌌'},
                    {'id': 'hash_void', 'name': 'Void Порталы', 'baseHashPerHour': 450000, 'emoji': '🕳️'},
                    {'id': 'hash_eternal', 'name': 'Eternal Движитель', 'baseHashPerHour': 1800000, 'emoji': '∞'},
                    {'id': 'hash_divine', 'name': 'Divine Генератор', 'baseHashPerHour': 7200000, 'emoji': '👑'},
                    {'id': 'hash_absolute', 'name': 'Absolute Мощь', 'baseHashPerHour': 28800000, 'emoji': '⚡'}
                ],
                'vip': [
                    {'id': 'vip_quantum_prime', 'name': 'Quantum Prime', 'baseHashPerHour': 120000, 'emoji': '⚡'},
                    {'id': 'vip_solar_core', 'name': 'Solar Core', 'baseHashPerHour': 300000, 'emoji': '☀️'},
                    {'id': 'vip_black_hole', 'name': 'Black Hole', 'baseHashPerHour': 750000, 'emoji': '🕳️'},
                    {'id': 'vip_nebula', 'name': 'Nebula Ферма', 'baseHashPerHour': 2000000, 'emoji': '🌫️'},
                    {'id': 'vip_multiverse', 'name': 'Multiverse Станция', 'baseHashPerHour': 5000000, 'emoji': '🌐'},
                    {'id': 'vip_infinity', 'name': 'Infinity Альянс', 'baseHashPerHour': 12000000, 'emoji': '♾️'}
                ]
            }
            
            # Get all user machines from database (source of truth)
            user_machines_db = db.query(MiningMachine).filter_by(user_id=user.id).all()
            
            # Group machines by machine_type (or name if machine_type is null)
            machines_dict = {}
            for machine in user_machines_db:
                key = machine.machine_type if machine.machine_type else machine.name
                if key in machines_dict:
                    machines_dict[key]['count'] += 1
                    machines_dict[key]['total_income'] += machine.hash_rate * 3600
                else:
                    machines_dict[key] = {
                        'machine_id': key,
                        'name': machine.name,
                        'level': machine.level,
                        'count': 1,
                        'hash_rate': machine.hash_rate,
                        'income_per_hour': machine.hash_rate * 3600,
                        'total_income': machine.hash_rate * 3600
                    }
            
            # Calculate proper income_per_hour for grouped machines
            all_machines_data = list(machines_dict.values())
            for m in all_machines_data:
                if m['count'] > 1:
                    m['income_per_hour'] = m['total_income']
            
            # Debug logging
            print(f"=== GET_MINING REQUEST ===")
            print(f"User {user_id}, category: {category}")
            print(f"User has {len(user_machines_db)} machines in DB")
            print(f"Grouped into {len(all_machines_data)} unique machines")
            for m in all_machines_data:
                print(f"  - {m['name']}: level {m['level']}, count {m['count']}, income {m['total_income']}")
            
            # Get machine levels for current category (for shop display) from JSON
            mining_levels = {}
            if category == 'coins':
                mining_levels = json.loads(user.mining_coins_levels or '{}')
            elif category == 'quanhash':
                mining_levels = json.loads(user.mining_quanhash_levels or '{}')
            elif category == 'vip':
                mining_levels = json.loads(user.mining_vip_levels or '{}')
            
            print(f"Returning {len(all_machines_data)} machines to frontend")
            print(f"=== END GET_MINING ===")
            
            return jsonify({
                'quanhash': user.quanhash,
                'coins': user.coins,
                'category': category,
                'shop_machines': [],  # Now loaded from frontend
                'user_machines': all_machines_data,  # ALL purchased machines from all categories
                'machine_levels': mining_levels
            })
    except Exception as e:
        print(f"Error in /api/mining: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/cards', methods=['POST'])
def get_cards():
    """Get user cards"""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        telegram_id = data.get('telegram_id')
        
        if not user_id and not telegram_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = None
            if user_id:
                user = db.query(User).filter_by(id=user_id).first()
            elif telegram_id:
                user = db.query(User).filter_by(telegram_id=telegram_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            cards = db.query(UserCard).filter_by(user_id=user.id).all()
        
            cards_data = []
            total_passive_per_minute = 0
            for card in cards:
                if getattr(card, 'is_active', True):
                    total_passive_per_minute += card.income_per_minute
                cards_data.append({
                    'id': card.id,
                    'card_type': card.card_type,
                    'card_level': getattr(card, 'card_level', 1),
                    'income_per_minute': card.income_per_minute,
                    'is_active': card.is_active if hasattr(card, 'is_active') else True
                })
            
            total_passive_per_hour = total_passive_per_minute * 60
            
            return jsonify({
                'coins': user.coins,
                'cards': cards_data,
                'total_passive_per_minute': total_passive_per_minute,
                'total_passive_per_hour': total_passive_per_hour
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/referrals', methods=['POST'])
def get_referrals():
    """Get user referrals info with detailed list"""
    try:
        # Import config values
        from config import REFERRAL_INCOME_PERCENT, REFERRAL_PREMIUM_INCOME_PERCENT
        
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Get all referrals with their stats
            referrals = db.query(User).filter_by(referred_by=user.id).all()
            
            # Calculate passive income for each referral
            referral_list = []
            total_passive_income = 0.0
            premium_count = 0
            regular_count = 0
            
            for ref in referrals:
                # Calculate referral's total earnings (coins earned from all sources)
                ref_total_earned = ref.total_earned or 0.0
                
                # Determine income percentage based on premium status
                is_premium_ref = getattr(ref, 'is_premium', False)
                is_vip_ref = getattr(ref, 'vip_level', 0) > 0
                
                # Premium users give higher percentage
                if is_premium_ref:
                    base_percent = REFERRAL_PREMIUM_INCOME_PERCENT  # 10% from premium
                    premium_count += 1
                elif is_vip_ref:
                    base_percent = 0.10  # 10% from VIP (old system)
                else:
                    base_percent = REFERRAL_INCOME_PERCENT  # 5% from regular
                    regular_count += 1
                
                # Calculate income from this referral
                ref_income = ref_total_earned * base_percent
                
                referral_list.append({
                    'telegram_id': ref.telegram_id,
                    'username': ref.username or f'User{ref.telegram_id}',
                    'coins': ref.coins or 0.0,
                    'total_earned': ref_total_earned,
                    'income_from_ref': ref_income,
                    'is_premium': is_premium_ref,
                    'is_vip': is_vip_ref,
                    'referral_income_percent': base_percent * 100,
                    'joined_at': ref.created_at.isoformat() if hasattr(ref, 'created_at') and ref.created_at else None
                })
                
                total_passive_income += ref_income
            
            # Update user's referral_income if it's less than calculated
            if user.referral_income < total_passive_income:
                user.referral_income = total_passive_income
                db.commit()
            
            # Use actual count from list, not from database (fixes incorrect count)
            actual_referrals_count = len(referral_list)
            
            return jsonify({
                'referral_code': user.referral_code,
                'referrals_count': actual_referrals_count,
                'premium_referrals_count': premium_count,
                'regular_referrals_count': regular_count,
                'referral_income': total_passive_income,
                'referrals': referral_list
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_energy', methods=['POST'])
def update_energy():
    """Update user energy"""
    try:
        data = request.json
        user_id = data.get('user_id')
        energy = data.get('energy')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            user.energy = min(energy, user.max_energy)
            db.commit()
            
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline_income', methods=['POST'])
def get_offline_income():
    """Get offline income"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            now = datetime.utcnow()
            
            # Check if user was offline for significant time (more than 10 seconds)
            if user.last_active:
                time_diff = (now - user.last_active).total_seconds()
                
                # Only show offline income if user was away for more than 10 seconds
                if time_diff < 10:
                    return jsonify({
                        'offline_time': 0,
                        'offline_income': 0,
                        'offline_hash': 0
                    })
                
                offline_time = min(time_diff - 10, 3 * 60 * 60)  # 3 hours max, minus 10 seconds to exclude active time
            else:
                return jsonify({
                    'offline_time': 0,
                    'offline_income': 0,
                    'offline_hash': 0
                })
            
            # Calculate passive coins from cards during offline
            passive_coins_per_hour = 0
            for card in user.cards:
                if card.is_active:
                    passive_coins_per_hour += card.income_per_minute * 60
            
            offline_income = (passive_coins_per_hour / 3600) * offline_time
            
            # Calculate passive QuanHash from machines during offline
            passive_hash_per_hour = 0
            for machine in user.machines:
                if machine.is_active:
                    passive_hash_per_hour += machine.hash_rate * 3600
            
            offline_hash = (passive_hash_per_hour / 3600) * offline_time
            
            # Update last_active to mark user is back in app (only if there was offline income)
            if offline_time > 0:
                user.last_active = now
            
            return jsonify({
                'offline_time': int(offline_time),
                'offline_income': int(offline_income),
                'offline_hash': int(offline_hash)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/withdraw', methods=['POST'])
def create_withdraw():
    """Create withdrawal request"""
    try:
        data = request.json
        user_id = data.get('user_id')
        address = data.get('address')
        amount = data.get('amount', 500000)  # Default 500000 if not specified
        
        if not user_id or not address:
            return jsonify({'error': 'Missing parameters'}), 400
        
        if not address.startswith('0x') or len(address) != 42:
            return jsonify({'success': False, 'error': 'Invalid BEP20 address'})
        
        # Validate amount (minimum 500,000)
        if amount < 500000:
            return jsonify({'success': False, 'error': 'Минимум 500,000 QuanHash'})
        
        with get_db() as db:
            # Accept telegram_id or DB id
            user = db.query(User).filter_by(telegram_id=user_id).first()
            if not user:
                user = db.query(User).filter_by(id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            if user.quanhash < amount:
                return jsonify({'success': False, 'error': 'Недостаточно QuanHash'})
            
            # Calculate USDT amount (500,000 QuanHash = $1 USDT)
            usdt_amount = amount / 500000
            
            # Create withdrawal record with pending status
            withdrawal = Withdrawal(
                user_id=user.id,
                amount=int(amount),
                usdt_amount=usdt_amount,
                address=address,
                status='pending'  # Status: pending (in process)
            )
            db.add(withdrawal)
            db.flush()  # Get the ID before commit
            withdrawal_id = withdrawal.id
            user.quanhash -= int(amount)
            db.commit()  # Explicit commit
            print(f"Withdrawal created: id={withdrawal_id}, user_id={user.id}, amount={amount}, usdt={usdt_amount}, address={address}, status=pending")
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/withdrawals', methods=['GET'])
def get_withdrawals():
    """Get withdrawal requests"""
    try:
        with get_db() as db:
            withdrawals = db.query(Withdrawal).order_by(Withdrawal.created_at.desc()).all()
            
            requests_data = []
            for w in withdrawals:
                user = db.query(User).filter_by(id=w.user_id).first()
                requests_data.append({
                    'id': w.id,
                    'user_id': w.user_id,
                    'telegram_id': user.telegram_id if user else None,
                    'amount': int(w.amount) if w.amount else 0,
                    'usdt_amount': int(w.usdt_amount) if w.usdt_amount else 0,
                    'address': w.address,
                    'status': w.status,
                    'created_at': w.created_at.isoformat() if w.created_at else None
                })
            
            return jsonify({'requests': requests_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get comprehensive admin statistics"""
    try:
        from sqlalchemy import func
        with get_db() as db:
            # Basic stats
            total_users = db.query(User).count()
            total_taps = int(db.query(func.sum(User.total_taps)).scalar() or 0)
            total_revenue = int(db.query(func.sum(User.total_earned)).scalar() or 0)
            pending_withdrawals = db.query(Withdrawal).filter_by(status='pending').count()
            
            # Advanced stats
            total_coins = int(db.query(func.sum(User.coins)).scalar() or 0)
            total_quanhash = int(db.query(func.sum(User.quanhash)).scalar() or 0)
            total_referrals = db.query(func.sum(User.referrals_count)).scalar() or 0
            active_users = db.query(User).filter(User.total_taps > 0).count()
            banned_users = db.query(User).filter_by(is_banned=True).count() if hasattr(User, 'is_banned') else 0
            total_machines = db.query(MiningMachine).count()
            total_card_owners = db.query(UserCard).distinct(UserCard.user_id).count()
            
            return jsonify({
                'total_users': total_users,
                'total_taps': total_taps,
                'total_revenue': total_revenue,
                'pending_withdrawals': pending_withdrawals,
                'total_coins': total_coins,
                'total_quanhash': total_quanhash,
                'total_referrals': total_referrals,
                'active_users': active_users,
                'banned_users': banned_users,
                'total_machines': total_machines,
                'total_cards': total_card_owners,
                'total_activity': active_users
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/process_withdrawal', methods=['POST'])
def process_withdrawal():
    """Process withdrawal request"""
    try:
        data = request.json
        request_id = data.get('request_id')
        status = data.get('status')  # 'completed' or 'rejected'
        
        with get_db() as db:
            withdrawal = db.query(Withdrawal).filter_by(id=request_id).first()
            
            if not withdrawal:
                return jsonify({'success': False, 'error': 'Withdrawal not found'}), 404
            
            # Update status
            withdrawal.status = status
            withdrawal.processed_at = datetime.utcnow()
            
            # If rejected, return QuanHash to user
            if status == 'rejected':
                user = db.query(User).filter_by(id=withdrawal.user_id).first()
                if user:
                    user.quanhash += withdrawal.amount
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/withdrawals', methods=['GET'])
def get_admin_withdrawals():
    """Get all withdrawal requests"""
    try:
        with get_db() as db:
            withdrawals = db.query(Withdrawal).order_by(Withdrawal.created_at.desc()).all()
            
            result = {
                'requests': [{
                    'id': w.id,
                    'user_id': w.user_id,
                    'amount': int(w.amount) if w.amount else 0,
                    'usdt_amount': float(w.usdt_amount) if w.usdt_amount else 0.0,
                    'address': w.address,
                    'status': w.status,
                    'created_at': w.created_at.isoformat() if w.created_at else datetime.utcnow().isoformat(),
                    'processed_at': w.processed_at.isoformat() if w.processed_at else None
                } for w in withdrawals]
            }
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/mass_notify', methods=['POST'])
def mass_notify():
    """Send mass notification to users"""
    try:
        data = request.json
        message = data.get('message')
        user_ids = data.get('user_ids', [])
        
        if not message:
            return jsonify({'success': False, 'error': 'Message required'}), 400
        
        # Store notifications (in real implementation, send via Telegram Bot API)
        notification_data = {
            'message': message,
            'user_ids': user_ids if user_ids else 'all',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # TODO: Implement actual Telegram bot notification sending
        # from bot import send_notification
        # send_notification(user_ids, message)
        
        return jsonify({'success': True, 'notification': notification_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/modify_user', methods=['POST'])
def modify_user():
    """Modify user (add/remove coins/quanhash, ban, freeze, etc.)"""
    try:
        data = request.json
        user_id = data.get('user_id')
        action = data.get('action')
        value = data.get('value')
        
        if not user_id or not action:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            if action == 'add_coins':
                user.coins += value
            elif action == 'remove_coins':
                user.coins = max(0, user.coins - value)
            elif action == 'add_quanhash':
                user.quanhash += value
            elif action == 'remove_quanhash':
                user.quanhash = max(0, user.quanhash - value)
            elif action == 'set_energy':
                user.energy = min(value, user.max_energy)
            elif action == 'set_max_energy':
                user.max_energy = value
                user.energy = min(user.energy, value)
            elif action == 'add_max_energy':
                user.max_energy = max(0, user.max_energy + value)
                user.energy = min(user.energy, user.max_energy)
            elif action == 'set_regen_rate':
                user.energy_regen_rate = float(value)
            elif action == 'add_energy':
                user.energy = min(user.max_energy, max(0, user.energy + int(value)))
            elif action == 'set_coins':
                user.coins = value
            elif action == 'set_quanhash':
                user.quanhash = value
            elif action == 'set_multiplier':
                user.active_multiplier = float(value)
            elif action == 'add_multiplier':
                user.active_multiplier = max(0.0, float(getattr(user, 'active_multiplier', 1.0)) + float(value))
            elif action == 'set_vip_level':
                user.vip_level = int(value)
            elif action == 'ban':
                user.is_banned = True
                user.ban_reason = value if value else 'Админ бан'
            elif action == 'unban':
                user.is_banned = False
                user.ban_reason = None
            elif action == 'freeze':
                user.is_frozen = True
            elif action == 'unfreeze':
                user.is_frozen = False
            elif action == 'set_referrer':
                # Find referrer by telegram_id
                referrer_telegram_id = int(value)
                referrer = db.query(User).filter_by(telegram_id=referrer_telegram_id).first()
                if referrer:
                    old_referred_by = user.referred_by
                    user.referred_by = referrer.id
                    # Update referral counts if needed
                    if old_referred_by:
                        old_ref = db.query(User).filter_by(id=old_referred_by).first()
                        if old_ref and old_ref.referrals_count > 0:
                            old_ref.referrals_count -= 1
                    if user.referred_by:
                        referrer.referrals_count += 1
                else:
                    return jsonify({'success': False, 'error': 'Referrer not found'}), 404
            elif action == 'reset':
                user.coins = 0
                user.quanhash = 0
                user.energy = user.max_energy
                user.total_taps = 0
                user.total_earned = 0
                user.total_mined = 0
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/add_passive_coins', methods=['POST'])
def admin_add_passive_coins():
    """Admin: add passive coins income (coins per minute) via special card."""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        # accept per_min or per_hour
        per_min = data.get('per_min')
        per_hour = data.get('per_hour')
        per_min = float(per_min) if per_min is not None else (float(per_hour) / 60.0 if per_hour is not None else 0.0)
        replace = bool(data.get('replace', False))
        if not user_id:
            return jsonify({'success': False, 'error': 'Missing user_id'}), 400
        with get_db() as db:
            user = db.query(User).filter((User.telegram_id == user_id) | (User.id == user_id)).first()
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            if replace:
                db.query(UserCard).filter_by(user_id=user.id, card_type='admin_boost_coins').delete()
            if per_min != 0:
                card = UserCard(
                    user_id=user.id,
                    card_type='admin_boost_coins',
                    card_level=1,
                    income_per_minute=per_min,
                    is_active=True
                )
                db.add(card)
            db.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/add_passive_hash', methods=['POST'])
def admin_add_passive_hash():
    """Admin: add passive QuanHash (per hour) via special mining machine."""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        # accept per_hour or per_min
        per_hour = data.get('per_hour')
        per_min = data.get('per_min')
        per_hour = float(per_hour) if per_hour is not None else (float(per_min) * 60.0 if per_min is not None else 0.0)
        replace = bool(data.get('replace', False))
        if not user_id:
            return jsonify({'success': False, 'error': 'Missing user_id'}), 400
        with get_db() as db:
            user = db.query(User).filter((User.telegram_id == user_id) | (User.id == user_id)).first()
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            if replace:
                db.query(MiningMachine).filter_by(user_id=user.id, name='Admin Boost').delete()
            if per_hour != 0:
                machine = MiningMachine(
                    user_id=user.id,
                    name='Admin Boost',
                    hash_rate=per_hour / 3600.0,
                    power_consumption=0.0,
                    efficiency=1.0,
                    is_active=True
                )
                db.add(machine)
            db.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/buy', methods=['POST'])
def buy_item():
    """Buy item from shop"""
    try:
        data = request.json
        user_id = data.get('user_id')
        item_type = data.get('item_type')
        price = data.get('price')
        
        print(f"Buy item request: user_id={user_id}, item_type={item_type}, price={price}")
        print(f"Item type starts with card_hour_: {item_type.startswith('card_hour_') if item_type else False}")
        print(f"Item type starts with card_min_: {item_type.startswith('card_min_') if item_type else False}")
        
        if not user_id or not item_type or not price:
            print(f"Missing parameters: user_id={user_id}, item_type={item_type}, price={price}")
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        # Ensure price is a float
        price = float(price) if price else 0
        
        with get_db() as db:
            # Try to find user by telegram_id first, then by id
            user = db.query(User).filter_by(telegram_id=user_id).first()
            if not user:
                user = db.query(User).filter_by(id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            if user.coins < price:
                return jsonify({'success': False, 'error': 'Недостаточно коинов'})
            
            user.coins -= price
            
            # Apply item effect
            if item_type == 'multiplier_2x':
                user.active_multiplier = 2.0
                user.multiplier_expires_at = datetime.utcnow().replace(hour=23, minute=59, second=59)
            elif item_type == 'multiplier_5x':
                user.active_multiplier = 5.0
                user.multiplier_expires_at = datetime.utcnow().replace(hour=23, minute=59, second=59)
            elif item_type == 'multiplier_10x':
                user.active_multiplier = 10.0
                user.multiplier_expires_at = datetime.utcnow().replace(hour=23, minute=59, second=59)
            elif item_type == 'energy':
                # Add energy from purchase
                amount = data.get('amount', 50)
                user.energy = min(user.energy + amount, user.max_energy)
            elif item_type == 'regen_boost':
                # Increase regeneration rate
                user.energy_regen_rate = getattr(user, 'energy_regen_rate', 1) + 0.5
            elif item_type.startswith('card_min_'):
                # Per minute card
                idx = int(item_type.split('_')[2])
                user_cards = db.query(UserCard).filter_by(user_id=user.id, card_type=item_type).all()
                level = len(user_cards) + 1
                
                # Get template based on index
                per_minute_cards = [
                    {'name': '⚡ Энергетический генератор', 'desc': 'Производит 0.5 коинов/мин', 'base_income': 0.5, 'base_price': 50000, 'rarity': 'common'},
                    {'name': '🔋 Мощная батарея', 'desc': 'Производит 1.2 коинов/мин', 'base_income': 1.2, 'base_price': 75000, 'rarity': 'common'},
                    {'name': '💎 Драгоценный кристалл', 'desc': 'Производит 2.5 коинов/мин', 'base_income': 2.5, 'base_price': 120000, 'rarity': 'rare'},
                    {'name': '⭐ Звездное ядро', 'desc': 'Производит 4.0 коинов/мин', 'base_income': 4.0, 'base_price': 200000, 'rarity': 'rare'},
                    {'name': '🔥 Плазменный реактор', 'desc': 'Производит 6.5 коинов/мин', 'base_income': 6.5, 'base_price': 350000, 'rarity': 'epic'},
                    {'name': '⚛️ Квантовый генератор', 'desc': 'Производит 10.0 коинов/мин', 'base_income': 10.0, 'base_price': 550000, 'rarity': 'epic'},
                    {'name': '🌌 Галактический мотор', 'desc': 'Производит 15.0 коинов/мин', 'base_income': 15.0, 'base_price': 850000, 'rarity': 'legendary'},
                    {'name': '👑 Императорский трон', 'desc': 'Производит 22.0 коинов/мин', 'base_income': 22.0, 'base_price': 1300000, 'rarity': 'legendary'},
                    {'name': '🐉 Драконье сердце', 'desc': 'Производит 30.0 коинов/мин', 'base_income': 30.0, 'base_price': 2000000, 'rarity': 'legendary'},
                    {'name': '💫 Бесконечность', 'desc': 'Производит 40.0 коинов/мин', 'base_income': 40.0, 'base_price': 3000000, 'rarity': 'legendary'},
                    {'name': '🧠 Нейросеть', 'desc': 'Производит 5.5 коинов/мин', 'base_income': 5.5, 'base_price': 280000, 'rarity': 'epic'},
                    {'name': '🪐 Планетарный коллайдер', 'desc': 'Производит 18.0 коинов/мин', 'base_income': 18.0, 'base_price': 1000000, 'rarity': 'legendary'},
                    {'name': '🎯 Точностный лазер', 'desc': 'Производит 3.0 коинов/мин', 'base_income': 3.0, 'base_price': 150000, 'rarity': 'rare'},
                    {'name': '🛸 Внеземной чип', 'desc': 'Производит 14.0 коинов/мин', 'base_income': 14.0, 'base_price': 750000, 'rarity': 'epic'},
                    {'name': '⚗️ Алхимический аппарат', 'desc': 'Производит 8.5 коинов/мин', 'base_income': 8.5, 'base_price': 450000, 'rarity': 'epic'},
                    {'name': '🧪 Биомедиум', 'desc': 'Производит 12.0 коинов/мин', 'base_income': 12.0, 'base_price': 650000, 'rarity': 'epic'},
                    {'name': '🌠 Новойдовый ускоритель', 'desc': 'Производит 25.0 коинов/мин', 'base_income': 25.0, 'base_price': 1700000, 'rarity': 'legendary'},
                    {'name': '🔬 Крио-модуль', 'desc': 'Производит 9.0 коинов/мин', 'base_income': 9.0, 'base_price': 500000, 'rarity': 'epic'},
                    {'name': '💻 Киберсистема', 'desc': 'Производит 35.0 коинов/мин', 'base_income': 35.0, 'base_price': 2500000, 'rarity': 'legendary'},
                    {'name': '🏆 Победный трофей', 'desc': 'Производит 50.0 коинов/мин', 'base_income': 50.0, 'base_price': 5000000, 'rarity': 'legendary'},
                ]
                template = per_minute_cards[idx] if idx < len(per_minute_cards) else per_minute_cards[0]
                
                base_income = template['base_income']
                income = base_income * (1.10 ** (level - 1))
                
                card = UserCard(
                    user_id=user.id,
                    card_type=item_type,
                    card_level=level,
                    income_per_minute=income,
                    is_active=True
                )
                db.add(card)
                user.last_active = datetime.utcnow()
                db.commit()
                print(f"Added card {item_type} level {level} for user {user_id}")
            elif item_type.startswith('card_hour_'):
                # Per hour card
                idx = int(item_type.split('_')[2])
                user_cards = db.query(UserCard).filter_by(user_id=user.id, card_type=item_type).all()
                level = len(user_cards) + 1
                
                # Get template based on index
                per_hour_cards = [
                    {'name': '🟢 Базовая ферма', 'desc': 'Производит 5 коинов/час', 'base_income': 5, 'base_price': 1000, 'rarity': 'common'},
                    {'name': '🌱 Росток успеха', 'desc': 'Производит 12 коинов/час', 'base_income': 12, 'base_price': 2500, 'rarity': 'common'},
                    {'name': '🍀 Четырехлистник', 'desc': 'Производит 20 коинов/час', 'base_income': 20, 'base_price': 5000, 'rarity': 'common'},
                    {'name': '⚡ Ускоритель', 'desc': 'Производит 35 коинов/час', 'base_income': 35, 'base_price': 8000, 'rarity': 'rare'},
                    {'name': '🔵 Редкий артефакт', 'desc': 'Производит 55 коинов/час', 'base_income': 55, 'base_price': 15000, 'rarity': 'rare'},
                    {'name': '🟣 Эпический кристалл', 'desc': 'Производит 90 коинов/час', 'base_income': 90, 'base_price': 30000, 'rarity': 'epic'},
                    {'name': '⭐ Звездная пыль', 'desc': 'Производит 140 коинов/час', 'base_income': 140, 'base_price': 50000, 'rarity': 'epic'},
                    {'name': '🔥 Огненное ядро', 'desc': 'Производит 220 коинов/час', 'base_income': 220, 'base_price': 85000, 'rarity': 'legendary'},
                    {'name': '💎 Кристалл удачи', 'desc': 'Производит 350 коинов/час', 'base_income': 350, 'base_price': 150000, 'rarity': 'legendary'},
                    {'name': '👑 Корона власти', 'desc': 'Производит 550 коинов/час', 'base_income': 550, 'base_price': 250000, 'rarity': 'legendary'},
                    {'name': '🏆 Чемпионство', 'desc': 'Производит 850 коинов/час', 'base_income': 850, 'base_price': 400000, 'rarity': 'legendary'},
                    {'name': '🚀 Ракета мечты', 'desc': 'Производит 1300 коинов/час', 'base_income': 1300, 'base_price': 650000, 'rarity': 'legendary'},
                    {'name': '🐉 Драконье сокровище', 'desc': 'Производит 2000 коинов/час', 'base_income': 2000, 'base_price': 1000000, 'rarity': 'legendary'},
                    {'name': '🌌 Галактика', 'desc': 'Производит 3100 коинов/час', 'base_income': 3100, 'base_price': 1800000, 'rarity': 'legendary'},
                    {'name': '⚛️ Квантовый скачок', 'desc': 'Производит 5000 коинов/час', 'base_income': 5000, 'base_price': 3000000, 'rarity': 'legendary'},
                    {'name': '💫 Вечность', 'desc': 'Производит 8000 коинов/час', 'base_income': 8000, 'base_price': 5000000, 'rarity': 'legendary'},
                    {'name': '🌈 Радужный мост', 'desc': 'Производит 13000 коинов/час', 'base_income': 13000, 'base_price': 8500000, 'rarity': 'legendary'},
                    {'name': '🌠 Звездопад', 'desc': 'Производит 21000 коинов/час', 'base_income': 21000, 'base_price': 15000000, 'rarity': 'legendary'},
                    {'name': '🎆 Новогодний салют', 'desc': 'Производит 34000 коинов/час', 'base_income': 34000, 'base_price': 25000000, 'rarity': 'legendary'},
                    {'name': '🌟 Супернова', 'desc': 'Производит 55000 коинов/час', 'base_income': 55000, 'base_price': 50000000, 'rarity': 'legendary'},
                ]
                template = per_hour_cards[idx] if idx < len(per_hour_cards) else per_hour_cards[0]
                
                base_income = template['base_income']
                income_per_hour = base_income * (1.10 ** (level - 1))
                income_per_min = round(income_per_hour / 60, 2)
                
                card = UserCard(
                    user_id=user.id,
                    card_type=item_type,
                    card_level=level,
                    income_per_minute=income_per_min,
                    is_active=True
                )
                db.add(card)
                user.last_active = datetime.utcnow()
                db.commit()
                print(f"Added PER HOUR card {item_type} level {level} for user {user_id}")
                print(f"Card details: income_per_hour={income_per_hour}, income_per_min={income_per_min}")
            elif item_type == 'auto_bot':
                # Auto-tap bot implementation
                taps_per_sec = data.get('taps_per_sec', 2)
                user.auto_tap_enabled = True
                user.auto_tap_level = getattr(user, 'auto_tap_level', 0) + 1
                user.auto_tap_speed = taps_per_sec
                # Store expiration (24 hours)
                from datetime import timedelta
                user.auto_tap_expires_at = datetime.utcnow() + timedelta(hours=24)
                user.last_active = datetime.utcnow()
            db.commit()
            
            print(f"Successfully processed purchase for user {user_id}, item {item_type}")
            return jsonify({'success': True})
    except Exception as e:
        print(f"Error in buy_item: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buy_shop_item', methods=['POST'])
def buy_shop_item():
    """Buy item from new comprehensive shop"""
    try:
        data = request.json
        user_id = data.get('user_id')
        category = data.get('category')
        level = data.get('level')
        price = data.get('price')
        item_index = data.get('item_index', 0)  # Index of the item being purchased
        base_effect = data.get('base_effect', 1)  # Base effect from frontend
        base_price = data.get('base_price', 1000)  # Base price from frontend
        
        if not user_id or not category or not level or not price:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        with get_db() as db:
            # Accept telegram_id or DB id
            user = db.query(User).filter_by(telegram_id=user_id).first()
            if not user:
                user = db.query(User).filter_by(id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            if user.coins < price:
                return jsonify({'success': False, 'error': 'Недостаточно коинов'})
            
            user.coins -= price
            
            # Update item level in database
            import json
            if category == 'tap_boost':
                levels = json.loads(user.tap_boost_levels or '{}')
                levels[str(item_index)] = level
                user.tap_boost_levels = json.dumps(levels)
            elif category == 'energy_buy':
                levels = json.loads(user.energy_buy_levels or '{}')
                levels[str(item_index)] = level
                user.energy_buy_levels = json.dumps(levels)
            elif category == 'energy_expand':
                levels = json.loads(user.energy_expand_levels or '{}')
                levels[str(item_index)] = level
                user.energy_expand_levels = json.dumps(levels)
            
            if category == 'tap_boost':
                # Calculate the INCREMENT effect (what should be added)
                if base_effect == 1:
                    # Первая позиция всегда дает +1 прирост
                    bonus = 1
                else:
                    # Для остальных позиций используем формулу
                    current_effect = int(base_effect * (1.2 ** (level - 1))) if level > 1 else 0
                    new_effect = int(base_effect * (1.2 ** level))
                    bonus = new_effect - current_effect  # This is the increment
                
                # Add to existing tap boost (sum all tap boosts)
                current_multiplier = getattr(user, 'active_multiplier', 1)
                user.active_multiplier = current_multiplier + bonus
            elif category == 'energy_buy':
                # Calculate the INCREMENT effect (what should be added)
                current_effect = round(base_effect * (1.15 ** (level - 1)), 2) if level > 1 else 0
                new_effect = round(base_effect * (1.15 ** level), 2)
                regen_boost = new_effect - current_effect  # This is the increment
                
                current_regen_rate = getattr(user, 'energy_regen_rate', 1.0)
                user.energy_regen_rate = current_regen_rate + regen_boost
            elif category == 'energy_expand':
                # Calculate the INCREMENT effect (what should be added)
                current_effect = int(base_effect * (1.25 ** (level - 1))) if level > 1 else 0
                new_effect = int(base_effect * (1.25 ** level))
                energy_to_add = new_effect - current_effect  # This is the increment
                
                user.max_energy = getattr(user, 'max_energy', 1000) + energy_to_add
                user.energy = min(user.energy, user.max_energy)
            elif category == 'autobot':
                # Create new autobot (no time accumulation)
                duration_map = {
                    1: 15, 2: 30, 3: 60, 4: 120, 5: 240, 6: 360, 7: 720, 8: 1440, 9: 2880, 10: 4320,
                    11: 7200, 12: 10080, 13: 14400, 14: 20160, 15: 28800
                }
                speed_map = {
                    1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1,
                    11: 6, 12: 6.5, 13: 7, 14: 7.5, 15: 8
                }
                from datetime import timedelta
                duration_minutes = duration_map.get(level, 30)
                speed = speed_map.get(level, 2.0)
                
                # Create new autobot (always replace existing)
                user.auto_tap_enabled = True
                user.auto_tap_level = level
                user.auto_tap_speed = speed
                user.auto_tap_expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
            elif category == 'card':
                # Buy card - use existing card purchase logic
                # This will be handled by the existing /api/buy endpoint
                return jsonify({'success': False, 'error': 'Use /api/buy for cards'})
            
            # Update last_active for user activity
            user.last_active = datetime.utcnow()
            
            db.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_shop_levels', methods=['POST'])
def get_shop_levels():
    """Get shop item levels for user"""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        telegram_id = data.get('telegram_id')

        if not user_id and not telegram_id:
            return jsonify({'success': False, 'error': 'Missing user_id'})

        with get_db() as db:
            user = None
            if user_id:
                user = db.query(User).filter_by(id=user_id).first()
            elif telegram_id:
                user = db.query(User).filter_by(telegram_id=telegram_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            import json
            return jsonify({
                'success': True,
                'tap_boost_levels': json.loads(user.tap_boost_levels or '{}'),
                'energy_buy_levels': json.loads(user.energy_buy_levels or '{}'),
                'energy_expand_levels': json.loads(user.energy_expand_levels or '{}')
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/super_reset_user', methods=['POST'])
def super_reset_user():
    """Super reset user - complete data wipe including shop levels"""
    try:
        data = request.json
        user_id = data.get('user_id')
        # Optional granular flags (default True for backward compatibility)
        reset_energy = data.get('reset_energy', True)
        reset_shop_levels = data.get('reset_shop_levels', True)
        reset_cards_minute = data.get('reset_cards_minute', True)
        reset_cards_hour = data.get('reset_cards_hour', True)
        reset_machines = data.get('reset_machines', True)
        reset_achievements = data.get('reset_achievements', True)
        reset_transactions = data.get('reset_transactions', True)
        reset_support = data.get('reset_support', True)
        reset_withdrawals = data.get('reset_withdrawals', True)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'Missing user_id'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            # Base currencies/statistics
            user.coins = 0.0
            user.quanhash = 0.0
            if reset_energy:
                user.energy = 1000
                user.max_energy = 1000
                user.energy_regen_rate = 1.0
            user.total_taps = 0
            user.total_earned = 0.0
            user.total_mined = 0.0
            user.referral_income = 0.0
            user.referrals_count = 0
            user.active_multiplier = 1.0
            user.multiplier_expires_at = None
            
            # Reset VIP status
            user.vip_level = 0
            user.vip_badge = None
            user.vip_unique_marker = None
            user.has_premium_support = False
            user.has_golden_profile = False
            user.has_top_place = False
            user.has_unique_design = False
            
            # Reset auto-tap
            user.auto_tap_enabled = False
            user.auto_tap_level = 0
            user.auto_tap_speed = 2.0
            user.auto_tap_expires_at = None
            
            # Reset shop levels
            if reset_shop_levels:
                user.tap_boost_levels = '{}'
                user.energy_buy_levels = '{}'
                user.energy_expand_levels = '{}'
            
            # Delete mining machines
            if reset_machines:
                db.query(MiningMachine).filter_by(user_id=user.id).delete()
            
            # Delete user cards (granular)
            if reset_cards_minute and reset_cards_hour:
                db.query(UserCard).filter_by(user_id=user.id).delete()
            else:
                if reset_cards_minute:
                    db.query(UserCard).filter(UserCard.user_id == user.id, UserCard.card_type.like('card_min_%')).delete(synchronize_session=False)
                if reset_cards_hour:
                    db.query(UserCard).filter(UserCard.user_id == user.id, UserCard.card_type.like('card_hour_%')).delete(synchronize_session=False)
            
            # Delete achievements
            if reset_achievements:
                db.query(UserAchievement).filter_by(user_id=user.id).delete()
            
            # Delete transactions
            if reset_transactions:
                db.query(Transaction).filter_by(user_id=user.id).delete()
            
            # Delete support tickets
            if reset_support:
                db.query(SupportTicket).filter_by(user_id=user.id).delete()
            
            # Delete withdrawals
            if reset_withdrawals:
                db.query(Withdrawal).filter_by(user_id=user.id).delete()
            
            db.commit()
            
            return jsonify({'success': True, 'message': 'Super reset completed successfully'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buy_with_stars', methods=['POST'])
def buy_with_stars():
    """Buy shop item with Telegram stars"""
    try:
        data = request.json
        user_id = data.get('user_id')
        category = data.get('category')
        level = data.get('level')
        price = data.get('price')
        
        if not user_id or not category or not level or not price:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            # Apply the same logic as buy_shop_item but without coin deduction
            if category == 'tap_boost':
                tap_boost_map = {
                    1: 1, 2: 2, 3: 3, 4: 4, 5: 6, 6: 9, 7: 13, 8: 19, 9: 26, 10: 36,
                    11: 51, 12: 71, 13: 101, 14: 141, 15: 201, 16: 281, 17: 401, 18: 581, 19: 801, 20: 1201
                }
                bonus = tap_boost_map.get(level, level)
                current_multiplier = getattr(user, 'active_multiplier', 1)
                user.active_multiplier = current_multiplier + bonus
            elif category == 'energy_buy':
                regen_boost_map = {
                    1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0, 6: 1.2, 7: 1.4, 8: 1.6, 9: 1.8, 10: 2.0,
                    11: 3.0, 12: 4.5, 13: 6.0, 14: 8.0, 15: 10.0
                }
                regen_boost = regen_boost_map.get(level, 0.5 * level)
                current_regen_rate = getattr(user, 'energy_regen_rate', 1.0)
                user.energy_regen_rate = current_regen_rate + regen_boost
            elif category == 'energy_expand':
                expand_map = {
                    1: 100, 2: 150, 3: 250, 4: 400, 5: 600, 6: 900, 7: 1250, 8: 1750, 9: 2500, 10: 3750,
                    11: 7500, 12: 12500, 13: 20000, 14: 37500, 15: 75000
                }
                energy_to_add = expand_map.get(level, 200 * level)
                user.max_energy = getattr(user, 'max_energy', 1000) + energy_to_add
                user.energy = min(user.energy, user.max_energy)
            elif category == 'autobot':
                duration_map = {
                    1: 15, 2: 30, 3: 60, 4: 120, 5: 240, 6: 360, 7: 720, 8: 1440, 9: 2880, 10: 4320,
                    11: 7200, 12: 10080, 13: 14400, 14: 20160, 15: 28800
                }
                speed_map = {
                    1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1,
                    11: 6, 12: 6.5, 13: 7, 14: 7.5, 15: 8
                }
                from datetime import timedelta
                duration_minutes = duration_map.get(level, 30)
                speed = speed_map.get(level, 2.0)
                
                user.auto_tap_enabled = True
                user.auto_tap_level = level
                user.auto_tap_speed = speed
                user.auto_tap_expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
            
            db.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/process_star_purchase', methods=['POST'])
def process_star_purchase():
    """Process star purchase after payment confirmation"""
    try:
        data = request.json
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        category = data.get('category')
        level = data.get('level')
        
        if not user_id or not product_id:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            # Apply the purchase based on category and level
            if category == 'tap_boost':
                tap_boost_map = {
                    11: 51, 12: 71, 13: 101, 14: 141, 15: 201
                }
                bonus = tap_boost_map.get(level, 51)
                current_multiplier = getattr(user, 'active_multiplier', 1)
                user.active_multiplier = current_multiplier + bonus
            elif category == 'energy_buy':
                regen_boost_map = {
                    11: 3.0, 12: 4.5, 13: 6.0, 14: 8.0, 15: 10.0
                }
                regen_boost = regen_boost_map.get(level, 3.0)
                current_regen_rate = getattr(user, 'energy_regen_rate', 1.0)
                user.energy_regen_rate = current_regen_rate + regen_boost
            elif category == 'energy_expand':
                expand_map = {
                    11: 7500, 12: 12500, 13: 20000, 14: 37500, 15: 75000
                }
                energy_to_add = expand_map.get(level, 7500)
                user.max_energy = getattr(user, 'max_energy', 1000) + energy_to_add
                user.energy = min(user.energy, user.max_energy)
            elif category == 'autobot':
                duration_map = {
                    11: 7200, 12: 10080, 13: 14400, 14: 20160, 15: 28800
                }
                speed_map = {
                    11: 6, 12: 6.5, 13: 7, 14: 7.5, 15: 8
                }
                from datetime import timedelta
                duration_minutes = duration_map.get(level, 7200)
                speed = speed_map.get(level, 6.0)
                
                user.auto_tap_enabled = True
                user.auto_tap_level = level
                user.auto_tap_speed = speed
                user.auto_tap_expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
            elif category == 'mining_vip':
                # VIP mining machines mapping to product_ids 71-76
                # VIP machines: vip_quantum_prime, vip_solar_core, vip_black_hole, vip_nebula, vip_multiverse, vip_infinity
                vip_machine_map = {
                    71: 'vip_quantum_prime',
                    72: 'vip_solar_core',
                    73: 'vip_black_hole',
                    74: 'vip_nebula',
                    75: 'vip_multiverse',
                    76: 'vip_infinity'
                }
                machine_id = vip_machine_map.get(product_id, None)
                
                if machine_id:
                    import json
                    vip_levels = json.loads(user.mining_vip_levels or '{}')
                    current_level = vip_levels.get(machine_id, 0)
                    new_level = current_level + 1
                    
                    # Check max level
                    if new_level > 50:
                        return jsonify({'success': False, 'error': 'Maximum level reached'})
                    
                    vip_levels[machine_id] = new_level
                    user.mining_vip_levels = json.dumps(vip_levels)
            
            db.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/buy_machine', methods=['POST'])
def buy_machine():
    """Buy mining machine"""
    try:
        data = request.json
        user_id = data.get('user_id')
        machine_id = data.get('machine_id')
        price = data.get('price')
        currency = data.get('currency', 'coins')
        
        print(f"=== BUY_MACHINE REQUEST ===")
        print(f"user_id: {user_id}, machine_id: {machine_id}, price: {price}, currency: {currency}")
        
        if not user_id or not machine_id or not price:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                print(f"User not found: {user_id}")
                return jsonify({'success': False, 'error': 'User not found'})
            
            print(f"User found: id={user.id}, telegram_id={user.telegram_id}")
            
            # Check balance
            if currency == 'coins':
                if user.coins < price:
                    return jsonify({'success': False, 'error': 'Недостаточно коинов'})
                user.coins -= price
            else:  # quanhash
                if user.quanhash < price:
                    return jsonify({'success': False, 'error': 'Недостаточно QuanHash'})
                user.quanhash -= price
            
            # Machine definitions (same as frontend)
            machines_data = {
                'coins': [
                    {'id': 'miner_cpu', 'name': 'CPU Майнер', 'basePrice': 5000, 'baseHashPerHour': 10, 'emoji': '💻'},
                    {'id': 'miner_gpu', 'name': 'GPU Майнер', 'basePrice': 20000, 'baseHashPerHour': 50, 'emoji': '🎮'},
                    {'id': 'miner_asic', 'name': 'ASIC Риг', 'basePrice': 80000, 'baseHashPerHour': 200, 'emoji': '⚡'},
                    {'id': 'miner_quantum', 'name': 'Quantum Майнер', 'basePrice': 300000, 'baseHashPerHour': 800, 'emoji': '💎'},
                    {'id': 'miner_server', 'name': 'Server Ферма', 'basePrice': 1000000, 'baseHashPerHour': 3000, 'emoji': '🖥️'},
                    {'id': 'miner_cloud', 'name': 'Cloud Риг', 'basePrice': 3500000, 'baseHashPerHour': 12000, 'emoji': '☁️'},
                    {'id': 'miner_data', 'name': 'Data Центр', 'basePrice': 12000000, 'baseHashPerHour': 50000, 'emoji': '🏢'},
                    {'id': 'miner_quantum_farm', 'name': 'Quantum Ферма', 'basePrice': 40000000, 'baseHashPerHour': 200000, 'emoji': '🌌'},
                    {'id': 'miner_neural', 'name': 'Neural Майнер', 'basePrice': 150000000, 'baseHashPerHour': 800000, 'emoji': '🧠'},
                    {'id': 'miner_cosmic', 'name': 'Cosmic Станция', 'basePrice': 500000000, 'baseHashPerHour': 3200000, 'emoji': '🚀'}
                ],
                'quanhash': [
                    {'id': 'hash_quantum_core', 'name': 'Quantum Ядро', 'basePrice': 10000, 'baseHashPerHour': 80, 'emoji': '⚛️'},
                    {'id': 'hash_plasma_rig', 'name': 'Plasma Риг', 'basePrice': 50000, 'baseHashPerHour': 400, 'emoji': '🔥'},
                    {'id': 'hash_stellar', 'name': 'Stellar Блок', 'basePrice': 250000, 'baseHashPerHour': 1800, 'emoji': '⭐'},
                    {'id': 'hash_cosmic_flux', 'name': 'Cosmic Поток', 'basePrice': 1000000, 'baseHashPerHour': 7000, 'emoji': '🌊'},
                    {'id': 'hash_nova', 'name': 'Nova Ускоритель', 'basePrice': 4000000, 'baseHashPerHour': 28000, 'emoji': '🌟'},
                    {'id': 'hash_galaxy', 'name': 'Galaxy Матрица', 'basePrice': 15000000, 'baseHashPerHour': 110000, 'emoji': '🌌'},
                    {'id': 'hash_void', 'name': 'Void Порталы', 'basePrice': 60000000, 'baseHashPerHour': 450000, 'emoji': '🕳️'},
                    {'id': 'hash_eternal', 'name': 'Eternal Движитель', 'basePrice': 250000000, 'baseHashPerHour': 1800000, 'emoji': '∞'},
                    {'id': 'hash_divine', 'name': 'Divine Генератор', 'basePrice': 1000000000, 'baseHashPerHour': 7200000, 'emoji': '👑'},
                    {'id': 'hash_absolute', 'name': 'Absolute Мощь', 'basePrice': 4000000000, 'baseHashPerHour': 28800000, 'emoji': '⚡'}
                ]
            }
            
            # Find machine definition
            machine_def = None
            for cat in machines_data.values():
                for m in cat:
                    if m['id'] == machine_id:
                        machine_def = m
                        break
                if machine_def:
                    break
            
            if not machine_def:
                return jsonify({'success': False, 'error': 'Invalid machine ID'})
            
            # Get current level from user's JSON field (this is the source of truth)
            import json
            current_level = 0
            if currency == 'coins':
                levels = json.loads(user.mining_coins_levels or '{}')
                current_level = levels.get(machine_id, 0)
            elif currency == 'quanhash':
                levels = json.loads(user.mining_quanhash_levels or '{}')
                current_level = levels.get(machine_id, 0)
            
            print(f"Current level from JSON: {current_level}")
            
            # Check if machine already exists in database
            existing = db.query(MiningMachine).filter_by(
                user_id=user.id, 
                machine_type=machine_id
            ).first()
            
            new_level = current_level + 1
            
            print(f"New level: {new_level}")
            
            # Check max level (50)
            if new_level > 50:
                print(f"Max level reached: {new_level}")
                return jsonify({'success': False, 'error': 'Maximum level reached'})
            
            # Calculate hash_per_hour - level in DB is 1-based, but calculation should use current_level
            # When current_level=0 (first purchase), hash should be baseHashPerHour * 1.15^0 = baseHashPerHour
            hash_per_hour = int(machine_def['baseHashPerHour'] * (1.15 ** current_level))
            
            print(f"Creating machine: name={machine_def['name']}, hash_per_hour={hash_per_hour}, level={new_level}")
            
            machine = MiningMachine(
                user_id=user.id,
                name=machine_def['name'],
                hash_rate=hash_per_hour / 3600.0,
                level=new_level,
                machine_type=machine_id
            )
            db.add(machine)
            
            # Update levels in user's JSON field
            if currency == 'coins':
                levels = json.loads(user.mining_coins_levels or '{}')
                levels[machine_id] = new_level
                user.mining_coins_levels = json.dumps(levels)
            elif currency == 'quanhash':
                levels = json.loads(user.mining_quanhash_levels or '{}')
                levels[machine_id] = new_level
                user.mining_quanhash_levels = json.dumps(levels)
            
            print(f"Committing to database...")
            db.commit()
            
            # Debug logging
            print(f"Machine purchased successfully: {machine_id}, level: {new_level}, hash_per_hour: {hash_per_hour}")
            print(f"=== END BUY_MACHINE ===")
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error buying machine: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/api/confirm_stars_payment', methods=['POST'])
def confirm_stars_payment():
    """Confirm Stars payment and add coins"""
    try:
        data = request.json
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        
        if not user_id or not product_id:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        # Define products
        products = {
            1: {'coins': 1000000},
            2: {'coins': 5000000}
        }
        
        product = products.get(product_id)
        if not product:
            return jsonify({'success': False, 'error': 'Invalid product'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            # Add coins after payment confirmation
            user.coins += product['coins']
            db.commit()
            
            return jsonify({
                'success': True,
                'coins_added': product['coins'],
                'new_balance': user.coins
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buy_energy', methods=['POST'])
def buy_energy():
    """Buy energy"""
    try:
        data = request.json
        user_id = data.get('user_id')
        amount = data.get('amount')
        price = data.get('price')
        
        if not user_id or not amount or not price:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        db = next(get_db())
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        if user.coins < price:
            return jsonify({'success': False, 'error': 'Недостаточно коинов'})
        
        user.energy = min(user.energy + amount, user.max_energy)
        user.coins -= price
        db.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/support', methods=['POST'])
def create_support_ticket():
    """Create support ticket"""
    try:
        data = request.json
        user_id = data.get('user_id')
        topic = data.get('topic')
        message = data.get('message')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400
        if not topic:
            return jsonify({'success': False, 'error': 'Topic required'}), 400
        if not message:
            return jsonify({'success': False, 'error': 'Message required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            support_ticket = SupportTicket(
                user_id=user.id,
                topic=topic,
                message=message,
                status='pending'  # Статус "в процессе"
            )
            db.add(support_ticket)
            # Transaction is committed automatically by the context manager
            
            # Send notification to admin chat
            try:
                from telegram import Bot
                from config import BOT_TOKEN
                bot = Bot(token=BOT_TOKEN)
                
                admin_message = f"💬 Новый вопрос от {user.username if user else 'Unknown'}:\n\nТема: {topic}\n\n{message}"
                
                import asyncio
                asyncio.run(bot.send_message(
                    chat_id="@SmartFix_Nsk",
                    text=admin_message
                ))
            except Exception as e:
                print(f"Failed to send to admin chat: {e}")
        
        return jsonify({'success': True, 'message': 'Сообщение отправлено!'})
    except Exception as e:
        print(f"Support ticket error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/user_support', methods=['POST'])
def get_user_support():
    """Get user's support tickets"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            tickets = db.query(SupportTicket).filter_by(user_id=user.id).order_by(SupportTicket.created_at.desc()).limit(20).all()
            
            tickets_data = []
            for ticket in tickets:
                # If ticket has an answer, show status as "answered" to user, regardless of database status
                display_status = 'answered' if ticket.answer else ticket.status
                tickets_data.append({
                    'id': ticket.id,
                    'topic': ticket.topic,
                    'message': ticket.message,
                    'answer': ticket.answer,
                    'status': display_status,  # Show "answered" if there's an answer
                    'is_read': ticket.is_read if hasattr(ticket, 'is_read') else False,
                    'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
                    'answered_at': ticket.answered_at.isoformat() if ticket.answered_at else None
                })
            
            return jsonify({'tickets': tickets_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mark_tickets_read', methods=['POST'])
def mark_tickets_read():
    """Mark all user's answered tickets as read"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Mark all answered tickets as read
            answered_tickets = db.query(SupportTicket).filter(
                SupportTicket.user_id == user.id,
                SupportTicket.answer.isnot(None)
            ).all()
            for ticket in answered_tickets:
                ticket.is_read = True
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/support', methods=['GET'])
def get_support_tickets():
    """Get all support tickets"""
    try:
        with get_db() as db:
            tickets = db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).all()
            
            # Count unread tickets (pending status)
            unread_count = db.query(SupportTicket).filter_by(status='pending').count()
            
            tickets_data = []
            for t in tickets:
                user = db.query(User).filter_by(id=t.user_id).first()
                tickets_data.append({
                    'id': t.id,
                    'user_id': t.user_id,
                    'telegram_id': user.telegram_id if user else None,
                    'username': user.username if user else 'Unknown',
                    'topic': t.topic,
                    'message': t.message,
                    'status': t.status,
                    'created_at': t.created_at.isoformat() if t.created_at else None
                })
            
            return jsonify({'tickets': tickets_data, 'unread_count': unread_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/unread_count', methods=['GET'])
def get_unread_count():
    """Get unread support tickets count"""
    try:
        with get_db() as db:
            unread_count = db.query(SupportTicket).filter_by(status='pending').count()
            return jsonify({'unread_count': unread_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/withdrawal_count', methods=['GET'])
def get_withdrawal_count():
    """Get pending withdrawal requests count"""
    try:
        with get_db() as db:
            withdrawal_count = db.query(Withdrawal).filter_by(status='pending').count()
            return jsonify({'count': withdrawal_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/answer_ticket', methods=['POST'])
def answer_ticket():
    """Answer support ticket and notify user"""
    try:
        data = request.json
        ticket_id = data.get('ticket_id')
        answer = data.get('answer')
        
        if not ticket_id or not answer:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        with get_db() as db:
            ticket = db.query(SupportTicket).filter_by(id=ticket_id).first()
            
            if not ticket:
                return jsonify({'success': False, 'error': 'Ticket not found'}), 404
            
            # Update ticket status
            ticket.status = 'answered'
            ticket.answered_at = datetime.utcnow()
            
            # Get user
            user = db.query(User).filter_by(id=ticket.user_id).first()
            
            # Save answer to ticket (user will see it in app)
            ticket.answer = answer
            
            # Send notification to user via Telegram
            if user:
                try:
                    from telegram import Bot
                    from config import BOT_TOKEN
                    bot = Bot(token=BOT_TOKEN)
                    
                    notification = f"💬 Ответ на ваш вопрос:\n\n{ticket.topic}\n\n{answer}"
                    
                    import asyncio
                    asyncio.run(bot.send_message(
                        chat_id=user.telegram_id,
                        text=notification
                    ))
                except Exception as e:
                    print(f"Failed to send notification to user: {e}")
            
            # Also send to admin chat
            try:
                from telegram import Bot
                from config import BOT_TOKEN
                bot = Bot(token=BOT_TOKEN)
                
                admin_message = f"💬 Новый вопрос от {user.username}:\n\nТема: {ticket.topic}\n\n{ticket.message}"
                
                import asyncio
                asyncio.run(bot.send_message(
                    chat_id="@SmartFix_Nsk",
                    text=admin_message
                ))
            except Exception as e:
                print(f"Failed to send to admin chat: {e}")
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/delete_ticket', methods=['POST'])
def delete_ticket():
    """Delete support ticket"""
    try:
        data = request.json
        ticket_id = data.get('ticket_id')
        
        if not ticket_id:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        with get_db() as db:
            ticket = db.query(SupportTicket).filter_by(id=ticket_id).first()
            
            if not ticket:
                return jsonify({'success': False, 'error': 'Ticket not found'}), 404
            
            db.delete(ticket)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/archive_ticket', methods=['POST'])
def archive_ticket():
    """Archive support ticket (mark as resolved)"""
    try:
        data = request.json
        ticket_id = data.get('ticket_id')
        
        if not ticket_id:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        with get_db() as db:
            ticket = db.query(SupportTicket).filter_by(id=ticket_id).first()
            
            if not ticket:
                return jsonify({'success': False, 'error': 'Ticket not found'}), 404
            
            # Mark as resolved for archive, but keep status as "answered" so user sees it as "ready"
            ticket.status = 'resolved'
            if not ticket.answered_at:
                ticket.answered_at = datetime.utcnow()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/set_vip', methods=['POST'])
def set_vip():
    """Set VIP status and privileges for user"""
    try:
        data = request.json
        user_id = data.get('user_id')
        vip_data = data.get('vip_data')
        
        if not user_id or not vip_data:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            # Update VIP fields if they exist on User model
            if hasattr(user, 'vip_level'):
                user.vip_level = vip_data.get('vip_level', 0)
            if hasattr(user, 'vip_badge'):
                user.vip_badge = vip_data.get('vip_badge', None)
            if hasattr(user, 'has_premium_support'):
                user.has_premium_support = vip_data.get('has_premium_support', False)
            if hasattr(user, 'has_golden_profile'):
                user.has_golden_profile = vip_data.get('has_golden_profile', False)
            if hasattr(user, 'has_top_place'):
                user.has_top_place = vip_data.get('has_top_place', False)
            if hasattr(user, 'has_unique_design'):
                user.has_unique_design = vip_data.get('has_unique_design', False)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/daily_tasks', methods=['POST'])
def get_daily_tasks():
    """Get daily tasks for user"""
    try:
        import random
        import datetime
        import json
        
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Count user cards
            cards_count = db.query(UserCard).filter_by(user_id=user.id).count()
            
            # Get already completed tasks for today
            today_str = datetime.date.today().isoformat()
            completed_tasks = json.loads(user.daily_tasks_completed or '{}')
            today_completed = completed_tasks.get(today_str, [])
            
            # Dynamic tasks pool for a year (365 days worth of variety)
            today = datetime.date.today()
            day_of_year = today.timetuple().tm_yday
            random.seed(day_of_year)  # Same tasks for same day
            
            dynamic_task_pool = [
                {'emoji': '👆', 'base_reward': 500, 'descriptions': [
                    ('Сделайте 10 тапов', 10),
                    ('Сделайте 25 тапов', 25),
                    ('Сделайте 50 тапов', 50),
                ]},
                {'emoji': '⚡', 'base_reward': 1000, 'descriptions': [
                    ('Заработайте 500 коинов', 500),
                    ('Заработайте 1000 коинов', 1000),
                    ('Заработайте 2000 коинов', 2000),
                ]},
                {'emoji': '💎', 'base_reward': 1500, 'descriptions': [
                    ('Заработайте 100 QuanHash', 100),
                    ('Заработайте 250 QuanHash', 250),
                    ('Заработайте 500 QuanHash', 500),
                ]},
                {'emoji': '💳', 'base_reward': 2000, 'descriptions': [
                    ('Купите 1 карточку', 1),
                    ('Купите 2 карточки', 2),
                    ('Купите 5 карточек', 5),
                ]},
                {'emoji': '👥', 'base_reward': 2500, 'descriptions': [
                    ('Пригласите 1 друга', 1),
                    ('Пригласите 2 друга', 2),
                    ('Пригласите 3 друга', 3),
                ]},
                {'emoji': '🎯', 'base_reward': 3000, 'descriptions': [
                    ('Откройте магазин', 1),
                    ('Используйте буст', 1),
                    ('Купите любой товар', 1),
                ]},
                {'emoji': '🌙', 'base_reward': 3500, 'descriptions': [
                    ('Вернитесь через 2 часа', 2),
                    ('Вернитесь через 4 часа', 4),
                    ('Вернитесь через 6 часов', 6),
                ]},
            ]
            
            # Pick 7 random tasks
            selected_tasks = random.sample(dynamic_task_pool, 7)
            
            # Build tasks list
            tasks = []
            
            # Task 1: Permanent channel subscription
            is_channel_subscribed = getattr(user, 'channel_subscribed', False)
            task_1_claimed = 1 in today_completed
            tasks.append({
                'id': 1,
                'name': 'Подписка на канал',
                'emoji': '📢',
                'description': 'Подпишитесь на канал Quantum Nexus для эксклюзивных новостей',
                'reward': 3000,
                'progress': 1 if is_channel_subscribed else 0,
                'target': 1,
                'completed': is_channel_subscribed,
                'claimed': task_1_claimed,
                'type': 'channel_subscription',
                'channel_url': 'https://t.me/quantum_nexus',
                'channel_name': '@quantum_nexus'
            })
            
            # Tasks 2-8: Dynamic tasks
            for idx, task_template in enumerate(selected_tasks, 2):
                desc_data = random.choice(task_template['descriptions'])
                task_desc, target = desc_data
                reward = task_template['base_reward']
                
                # Check if task was already claimed
                task_claimed = idx in today_completed
                
                # Calculate progress based on task type
                if 'тапов' in task_desc:
                    progress = min(user.total_taps, target)
                    completed = user.total_taps >= target
                elif 'коинов' in task_desc:
                    progress = min(int(user.coins), target)
                    completed = user.coins >= target
                elif 'QuanHash' in task_desc:
                    progress = min(int(user.quanhash), target)
                    completed = user.quanhash >= target
                elif 'карточк' in task_desc:
                    progress = min(cards_count, target)
                    completed = cards_count >= target
                elif 'друга' in task_desc:
                    progress = min(user.referrals_count, target)
                    completed = user.referrals_count >= target
                elif 'Вернитесь' in task_desc:
                    # Check last active time
                    if user.last_active:
                        hours_passed = (datetime.datetime.utcnow() - user.last_active).total_seconds() / 3600
                        progress = 1 if hours_passed >= target else 0
                        completed = hours_passed >= target
                    else:
                        progress = 0
                        completed = False
                elif 'Откройте магазин' in task_desc or 'Используйте буст' in task_desc or 'Купите любой товар' in task_desc:
                    # Simple completion tasks - just mark as completed if user has activity
                    progress = 1
                    completed = True
                else:
                    progress = 0
                    completed = False
                
                tasks.append({
                    'id': idx,
                    'name': task_desc.split(' ')[0] + ' ' + task_desc.split(' ')[1] if len(task_desc.split(' ')) > 1 else task_desc,
                    'emoji': task_template['emoji'],
                    'description': task_desc,
                    'reward': reward,
                    'progress': progress,
                    'target': target,
                    'completed': completed,
                    'claimed': task_claimed
                })
            
            return jsonify({'tasks': tasks})
    except Exception as e:
        print(f"Daily tasks error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/claim_task', methods=['POST'])
def claim_task():
    """Claim task reward"""
    try:
        import random
        import datetime
        import json
        
        data = request.json
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        
        if not user_id or not task_id:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            # Check if task was already completed today
            today_str = datetime.date.today().isoformat()
            completed_tasks = json.loads(user.daily_tasks_completed or '{}')
            today_completed = completed_tasks.get(today_str, [])
            
            if task_id in today_completed:
                print(f"Task {task_id} already completed today by user {user_id}")
                return jsonify({'success': False, 'error': 'Task already completed today'})
            
            # Regenerate tasks to get the reward for this specific task
            today = datetime.date.today()
            day_of_year = today.timetuple().tm_yday
            random.seed(day_of_year)
            
            # Recreate task pool to find the task
            dynamic_task_pool = [
                {'emoji': '👆', 'base_reward': 500},
                {'emoji': '⚡', 'base_reward': 1000},
                {'emoji': '💎', 'base_reward': 1500},
                {'emoji': '💳', 'base_reward': 2000},
                {'emoji': '👥', 'base_reward': 2500},
                {'emoji': '🎯', 'base_reward': 3000},
                {'emoji': '🌙', 'base_reward': 3500},
            ]
            
            selected_tasks = random.sample(dynamic_task_pool, 7)
            
            # Task 1 is channel subscription (3000)
            if task_id == 1:
                reward = 3000
            elif task_id >= 2 and task_id <= 8:
                # Get reward from the dynamic task
                task_idx = task_id - 2
                if task_idx < len(selected_tasks):
                    reward = selected_tasks[task_idx]['base_reward']
                else:
                    reward = 500  # Default reward
            else:
                reward = 0
            
            # Add reward and mark task as completed
            user.coins += reward
            today_completed.append(task_id)
            completed_tasks[today_str] = today_completed
            user.daily_tasks_completed = json.dumps(completed_tasks)
            db.commit()
            
            print(f"Task {task_id} claimed by user {user_id}, reward: {reward}, new balance: {user.coins}")
            
            return jsonify({'success': True, 'reward': reward})
    except Exception as e:
        import traceback
        print(f"Claim task error: {e}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/verify_channel_subscription', methods=['POST'])
def verify_channel_subscription():
    """Verify user subscribed to channel"""
    try:
        from telegram import Bot
        from config import BOT_TOKEN
        import asyncio
        import datetime
        
        data = request.json
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'Missing user_id'})
        
        # Use async to check channel membership
        async def check_membership():
            try:
                bot = Bot(token=BOT_TOKEN)
                member = await bot.get_chat_member(chat_id="@quantum_nexus", user_id=user_id)
                # Check if user is a member, administrator, or creator
                print(f"Channel membership check for user {user_id}: {member.status}")
                return member.status in ['member', 'administrator', 'creator']
            except Exception as e:
                print(f"Channel membership check error: {e}")
                return False
        
        # Run async function
        try:
            is_subscribed = asyncio.run(check_membership())
        except Exception as e:
            print(f"Async run error: {e}")
            is_subscribed = False
        
        print(f"User {user_id} subscription status: {is_subscribed}")
        
        if is_subscribed:
            with get_db() as db:
                user = db.query(User).filter_by(telegram_id=user_id).first()
                if user:
                    # Mark as subscribed (but don't give reward here - that's done in claim_task)
                    if not user.channel_subscribed:
                        print(f"Marking user {user_id} as subscribed to channel")
                        user.channel_subscribed = True
                        user.channel_subscribed_at = datetime.datetime.utcnow()
                        db.commit()
                        print(f"User marked as subscribed")
                    return jsonify({'success': True, 'subscribed': True})
                else:
                    print(f"User {user_id} not found in database")
                    return jsonify({'success': False, 'error': 'User not found'})
        else:
            print(f"User {user_id} is not subscribed")
            return jsonify({'success': True, 'subscribed': False})
            
    except Exception as e:
        import traceback
        print(f"Channel verification error: {e}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history', methods=['POST'])
def get_transaction_history():
    """Get user transaction history"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Get transactions (skip if table doesn't exist)
            try:
                transactions = db.query(Transaction).filter_by(user_id=user.id).order_by(Transaction.created_at.desc()).limit(100).all()
            except Exception as e:
                print(f"Warning: Transaction table not available: {e}")
                transactions = []
            
            # Get withdrawals
            withdrawals = db.query(Withdrawal).filter_by(user_id=user.id).order_by(Withdrawal.created_at.desc()).all()
            
            history = []
            
            # Add transactions
            for t in transactions:
                history.append({
                    'type': t.transaction_type,
                    'amount': t.amount,
                    'currency': t.currency,
                    'date': t.created_at.isoformat() if t.created_at else None,
                    'timestamp': t.created_at.timestamp() if t.created_at else 0
                })
            
            # Add withdrawals (sorted by timestamp descending)
            withdrawal_list = []
            for w in withdrawals:
                # Map status to Russian
                status_map = {
                    'pending': 'В процессе',
                    'completed': 'Выплачено',
                    'rejected': 'Отклонено'
                }
                status_text = status_map.get(w.status, w.status)
                
                withdrawal_list.append({
                    'type': 'withdrawal',
                    'amount': w.usdt_amount,
                    'currency': 'usd',
                    'status': status_text,  # Status in Russian
                    'status_code': w.status,  # Original status code
                    'address': w.address,  # BEP20 address
                    'date': w.created_at.isoformat() if w.created_at else None,
                    'timestamp': w.created_at.timestamp() if w.created_at else 0
                })
            
            # Sort withdrawals by timestamp descending and return only last 3
            withdrawal_list.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
            
            print(f"Returning {len(withdrawal_list[:3])} withdrawals for user_id={user.id}")
            for w in withdrawal_list[:3]:
                print(f"  - amount={w['amount']}, address={w['address']}, status={w['status']}")
            
            return jsonify({'history': withdrawal_list[:3]})  # Return only last 3 withdrawals
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buy_vip_machine', methods=['POST'])
def buy_vip_machine():
    """Buy VIP exclusive mining machine"""
    try:
        data = request.json
        user_id = data.get('user_id')
        machine_type = data.get('machine_type')
        
        if not user_id or not machine_type:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            # Check VIP level
            vip_level = getattr(user, 'vip_level', 0)
            
            prices = {
                'quantum_pro': 50000000,
                'absolute_pro': 100000000
            }
            
            required_levels = {
                'quantum_pro': 5,
                'absolute_pro': 6
            }
            
            price = prices.get(machine_type, 0)
            required_level = required_levels.get(machine_type, 999)
            
            if vip_level < required_level:
                return jsonify({'success': False, 'error': f'Требуется VIP уровень {required_level}'}), 403
            
            if user.coins < price:
                return jsonify({'success': False, 'error': 'Недостаточно коинов'}), 400
            
            # Create VIP machine
            from models import MiningMachine
            
            hash_rates = {
                'quantum_pro': 500.0,
                'absolute_pro': 1000.0
            }
            
            vip_machine = MiningMachine(
                user_id=user.id,
                level=100,
                name=machine_type,
                hash_rate=hash_rates.get(machine_type, 100.0),
                power_consumption=0.0,
                efficiency=2.0,
                machine_type='vip'
            )
            
            user.coins -= price
            db.add(vip_machine)
            db.commit()
            
            return jsonify({'success': True, 'message': 'VIP машина куплена!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buy_vip_boost', methods=['POST'])
def buy_vip_boost():
    """Buy VIP exclusive boost"""
    try:
        data = request.json
        user_id = data.get('user_id')
        boost_type = data.get('boost_type')
        
        if not user_id or not boost_type:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            vip_level = getattr(user, 'vip_level', 0)
            
            boost_data = {
                'vip_boost_20x': {'price': 5000000, 'multiplier': 20, 'duration': 3600, 'min_level': 3},
                'diamond_boost_50x': {'price': 20000000, 'multiplier': 50, 'duration': 86400, 'min_level': 5}
            }
            
            boost_info = boost_data.get(boost_type)
            if not boost_info:
                return jsonify({'success': False, 'error': 'Unknown boost'}), 400
            
            if vip_level < boost_info['min_level']:
                return jsonify({'success': False, 'error': f'Требуется VIP уровень {boost_info["min_level"]}'}), 403
            
            if user.coins < boost_info['price']:
                return jsonify({'success': False, 'error': 'Недостаточно коинов'}), 400
            
            # Apply boost
            user.active_multiplier = boost_info['multiplier']
            user.multiplier_expires_at = datetime.utcnow() + timedelta(seconds=boost_info['duration'])
            user.coins -= boost_info['price']
            
            db.commit()
            
            return jsonify({'success': True, 'message': f'VIP буст x{boost_info["multiplier"]} активирован!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buy_vip_card', methods=['POST'])
def buy_vip_card():
    """Buy VIP exclusive card"""
    try:
        data = request.json
        user_id = data.get('user_id')
        card_type = data.get('card_type')
        
        if not user_id or not card_type:
            return jsonify({'success': False, 'error': 'Missing parameters'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            vip_level = getattr(user, 'vip_level', 0)
            
            card_data = {
                'diamond': {'price': 50000000, 'income': 500000, 'min_level': 5}
            }
            
            card_info = card_data.get(card_type)
            if not card_info:
                return jsonify({'success': False, 'error': 'Unknown card type'}), 400
            
            if vip_level < card_info['min_level']:
                return jsonify({'success': False, 'error': f'Требуется VIP уровень {card_info["min_level"]}'}), 403
            
            if user.coins < card_info['price']:
                return jsonify({'success': False, 'error': 'Недостаточно коинов'}), 400
            
            # Create VIP card
            from models import Card
            
            vip_card = Card(
                user_id=user.id,
                name=f'VIP {card_type.capitalize()}',
                description='VIP карточка с эксклюзивным доходом',
                income=card_info['income'],
                rarity='vip',
                card_type='vip'
            )
            
            user.coins -= card_info['price']
            db.add(vip_card)
            db.commit()
            
            return jsonify({'success': True, 'message': 'VIP карточка куплена!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/top_users', methods=['POST'])
def get_top_users():
    """Get top 100 users by total earnings, VIPs first"""
    try:
        data = request.json
        limit = data.get('limit', 100)
        current_user_id = data.get('user_id', None)  # Get current user ID for "find yourself"
        
        with get_db() as db:
            # Fetch more users to filter
            users = db.query(User).filter(User.total_taps > 0).order_by(User.total_earned.desc()).limit(limit * 2).all()
            
            print(f"[TOP_USERS] Found {len(users)} users in database")
            
            top_users = []
            for u in users:
                # Calculate passive income from cards
                passive_income = 0
                try:
                    cards = u.cards if hasattr(u, 'cards') else []
                    for card in cards:
                        if card and getattr(card, 'is_active', True):
                            passive_income += getattr(card, 'income_per_minute', 0) or 0
                except Exception as e:
                    print(f"[TOP_USERS] Error calculating passive income: {e}")
                
                # Convert to per hour for display
                passive_income_per_hour = int(passive_income * 60) if passive_income else 0
                
                # For bots, set a stable passive income (10 to 2000 per hour)
                if hasattr(u, 'telegram_id') and u.telegram_id >= 9000000000:  # Bot user
                    # Use user's ID as seed for stable random value
                    import hashlib
                    stable_seed = int(hashlib.md5(str(u.telegram_id).encode()).hexdigest()[:8], 16) % 1000000
                    passive_income_per_hour = stable_seed % 1990 + 10  # Stable between 10 and 2000
                
                vip_level = getattr(u, 'vip_level', 0) or 0
                vip_badge = getattr(u, 'vip_badge', None) or ""
                
                # Calculate experience, level, and rating
                experience = calculate_experience(u.total_earned, u.total_taps, vip_level)
                level = calculate_level(experience)
                rating = calculate_rating(u.coins, u.total_earned, u.total_taps, vip_level, level)
                
                top_users.append({
                    'username': u.username or 'Unknown',
                    'total_earned': int(u.total_earned or 0),
                    'coins': int(u.coins or 0),
                    'level': level,
                    'experience': round(experience, 2),
                    'rating': round(rating, 2),
                    'vip_level': vip_level,
                    'vip_badge': vip_badge,
                    'passive_income': passive_income_per_hour,
                    'quanhash': int(getattr(u, 'quanhash', 0) or 0),
                    'total_taps': int(u.total_taps or 0),
                    'telegram_id': int(getattr(u, 'telegram_id', 0))  # Add telegram_id for matching
                })
            
            # Sort: VIPs first (by VIP level DESC), then by rating DESC
            top_users.sort(key=lambda x: (-x['vip_level'], -x['rating']))
            
            # Find current user's position if requested
            current_user_pos = None
            current_user_data = None
            if current_user_id:
                for idx, user_data in enumerate(top_users):
                    if user_data['telegram_id'] == current_user_id:
                        current_user_pos = idx + 1  # 1-based position
                        current_user_data = user_data
                        break
            
            # Return only top 100
            top_users = top_users[:100]
            
            # Remove telegram_id from response (not needed by frontend)
            for user_data in top_users:
                if 'telegram_id' in user_data:
                    del user_data['telegram_id']
            
            print(f"[TOP_USERS] Returning {len(top_users)} users")
            response = {'users': top_users}
            if current_user_pos and current_user_data:
                # Remove telegram_id from current user data
                if 'telegram_id' in current_user_data:
                    del current_user_data['telegram_id']
                response['current_user'] = current_user_data
                response['current_user_position'] = current_user_pos
            return jsonify(response)
    except Exception as e:
        print(f"[TOP_USERS] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/toggle_autobot', methods=['POST'])
def toggle_autobot():
    """Toggle autobot on/off"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            # Check if autobot is expired
            auto_tap_expires_at = getattr(user, 'auto_tap_expires_at', None)
            if auto_tap_expires_at and auto_tap_expires_at < datetime.utcnow():
                # Autobot expired
                user.auto_tap_enabled = False
                db.commit()
                return jsonify({
                    'success': False,
                    'error': 'Срок действия автобота истёк'
                })
            
            # Toggle auto_tap_enabled
            current_state = getattr(user, 'auto_tap_enabled', False)
            user.auto_tap_enabled = not current_state
            
            db.commit()
            
            return jsonify({
                'success': True,
                'auto_tap_enabled': user.auto_tap_enabled
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/reset_user', methods=['POST'])
def reset_user():
    """User reset with different types"""
    try:
        data = request.json
        user_id = data.get('user_id')
        reset_type = data.get('reset_type', 'full')  # 'full' or 'soft'
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            if reset_type == 'full':
                # ПОЛНЫЙ СБРОС - все данные обнуляются
                user.coins = 0
                user.quanhash = 0
                user.energy = 100  # Начальная энергия
                user.max_energy = 100  # Начальный максимум энергии
                user.energy_regen_rate = 1.0  # Скорость восстановления энергии
                user.total_taps = 0
                user.total_earned = 0
                user.total_mined = 0
                user.active_multiplier = 1.0
                user.multiplier_expires_at = None
                user.auto_tap_enabled = False
                user.auto_tap_level = 0
                user.auto_tap_speed = 1.0
                user.auto_tap_expires_at = None
                user.auto_tap_item_id = None
                user.last_active = datetime.utcnow()
                user.last_passive_update = datetime.utcnow()
                user.last_hash_update = datetime.utcnow()
                
                # Reset VIP status
                user.vip_level = 0
                user.vip_badge = None
                user.has_premium_support = False
                user.has_golden_profile = False
                user.has_top_place = False
                user.has_unique_design = False
                
                # Remove all user cards
                db.query(UserCard).filter_by(user_id=user.id).delete()
                
                # Remove all user machines
                db.query(MiningMachine).filter_by(user_id=user.id).delete()
                
                # Remove all user withdrawals
                db.query(Withdrawal).filter_by(user_id=user.id).delete()
                
                # Remove all user support tickets
                db.query(SupportTicket).filter_by(user_id=user.id).delete()
                
                message = 'Пользователь полностью обнулен'
                
            elif reset_type == 'soft':
                # МЯГКИЙ СБРОС - только прогресс, но сохраняем базовые ресурсы
                user.total_taps = 0
                user.total_earned = 0
                user.total_mined = 0
                user.active_multiplier = 1.0
                user.multiplier_expires_at = None
                user.auto_tap_enabled = False
                user.auto_tap_level = 0
                user.auto_tap_speed = 1.0
                user.auto_tap_expires_at = None
                user.auto_tap_item_id = None
                user.last_active = datetime.utcnow()
                user.last_passive_update = datetime.utcnow()
                user.last_hash_update = datetime.utcnow()
                
                # Reset VIP status
                user.vip_level = 0
                user.vip_badge = None
                user.has_premium_support = False
                user.has_golden_profile = False
                user.has_top_place = False
                user.has_unique_design = False
                
                # Remove all user cards
                db.query(UserCard).filter_by(user_id=user.id).delete()
                
                # Remove all user machines
                db.query(MiningMachine).filter_by(user_id=user.id).delete()
                
                # Remove all user withdrawals
                db.query(Withdrawal).filter_by(user_id=user.id).delete()
                
                # Remove all user support tickets
                db.query(SupportTicket).filter_by(user_id=user.id).delete()
                
                message = 'Прогресс пользователя сброшен (ресурсы сохранены)'
            
            db.commit()
            
            return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/update_sound_settings', methods=['POST'])
def update_sound_settings():
    """Update user sound settings"""
    try:
        data = request.json
        user_id = data.get('user_id')
        sound_enabled = data.get('sound_enabled', True)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            # Update sound setting
            user.sound_enabled = bool(sound_enabled)
            db.commit()
            
            return jsonify({'success': True, 'sound_enabled': user.sound_enabled})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/update_username', methods=['POST'])
def update_username():
    """Update user username with uniqueness check"""
    try:
        data = request.json
        user_id = data.get('user_id')
        username = data.get('username')
        
        if not user_id or not username:
            return jsonify({'success': False, 'error': 'User ID and username required'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            # Check if username already exists for another user
            existing_user = db.query(User).filter_by(username=username).first()
            if existing_user and existing_user.telegram_id != user_id:
                return jsonify({'success': False, 'error': 'Такое имя пользователя уже существует'})
            
            user.username = username
            db.commit()
            
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
