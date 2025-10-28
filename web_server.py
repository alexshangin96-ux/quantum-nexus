#!/usr/bin/env python3
"""
Quantum Nexus Web Server
Server for Telegram Web App
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import get_db
from models import User, MiningMachine, UserCard, Withdrawal, SupportTicket
from utils import calculate_offline_income
from datetime import datetime, timedelta
from config import BASE_TAP_REWARD, ENERGY_COST_PER_TAP, MAX_ENERGY
import os

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    """Serve web app"""
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
            
            # Energy regeneration while offline (1 per second)
            if user.last_active:
                offline_seconds = (current_time - user.last_active).total_seconds()
                # Regenerate energy (1 per second, max to max_energy)
                if offline_seconds > 1:  # Only if offline for more than 1 second
                    energy_regen = min(int(offline_seconds), user.max_energy - user.energy)
                    if energy_regen > 0:
                        user.energy = min(user.energy + energy_regen, user.max_energy)
            
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
                for card in user.cards:
                    if hasattr(card, 'is_active') and card.is_active:
                        user_cards.append({
                            'name': getattr(card, 'name', 'Unknown Card'),
                            'income': getattr(card, 'income_per_minute', 0) or 0,
                            'type': 'permanent'
                        })
            except Exception as e:
                print(f"Error getting cards: {e}")
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
                user_machines = []
            
            return jsonify({
                'coins': user.coins,
                'quanhash': user.quanhash,
                'energy': user.energy,
                'max_energy': user.max_energy,
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
                'machines': user_machines
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
            
            # Calculate reward with VIP bonus
            reward = BASE_TAP_REWARD * user.active_multiplier * vip_multiplier
            
            # VIP users get lower energy cost
            energy_cost = ENERGY_COST_PER_TAP
            if vip_level >= 3:
                energy_cost = max(0.5, energy_cost * 0.5)  # 50% energy cost for Gold+
            
            # Update user
            user.coins += reward
            user.energy -= energy_cost
            user.total_taps += 1
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
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
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
                user_cards = db.query(UserCard).filter_by(user_id=user.id).all()
                user_card_counts = {}
                for uc in user_cards:
                    user_card_counts[uc.card_type] = user_card_counts.get(uc.card_type, 0) + 1
                
                for i, template in enumerate(per_minute_cards):
                    card_key = f"card_min_{i}"
                    purchases = user_card_counts.get(card_key, 0)
                    level = min(purchases + 1, 300)
                    price = int(template['base_price'] * (1.15 ** (level - 1)))
                    income = template['base_income'] * (1.10 ** (level - 1))
                    
                    # Unlock card if previous card reached level 5
                    is_locked = i > 0 and user_card_counts.get(f"card_min_{i-1}", 0) < 5
                    
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
                    income = template['base_income'] * (1.10 ** (level - 1))
                    income_per_min = round(income / 60, 2)
                    
                    # Unlock card if previous card reached level 5
                    is_locked = i > 0 and user_card_counts.get(f"card_hour_{i-1}", 0) < 5
                    
                    items.append({
                        'id': card_key,
                        'name': template['name'],
                        'description': template['desc'],
                        'base_price': template['base_price'],
                        'price': price,
                        'level': level,
                        'rarity': template['rarity'],
                        'income': income,
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
        category = data.get('category', 'starter')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Generate 30 machines for each category
            if category == 'starter':
                # Machines for coins (starting from 5000)
                machines = [
                    {'id': f'starter_{i}', 'name': f'Стартовая машина #{i+1}', 'price': 5000 + i*5000, 'hash_rate': round(0.05*(i+1), 2), 'currency': 'coins', 'hash_per_hour': round(0.05*(i+1)*3600)}
                    for i in range(30)
                ]
            else:
                # Machines for QuanHash
                machines = [
                    {'id': f'premium_{i}', 'name': f'Премиум машина #{i+1}', 'price': 50 + i*50, 'hash_rate': round(0.5*(i+1), 2), 'currency': 'quanhash', 'hash_per_hour': round(0.5*(i+1)*3600)}
                    for i in range(30)
                ]
            
            user_machines = db.query(MiningMachine).filter_by(user_id=user.id).all()
            machines_data = []
            for machine in user_machines:
                machines_data.append({
                    'id': machine.id,
                    'name': machine.name,
                    'level': machine.level,
                    'hash_rate': machine.hash_rate,
                    'income_per_hour': machine.hash_rate * 3600,
                })
            
            return jsonify({
                'quanhash': user.quanhash,
                'coins': user.coins,
                'category': category,
                'shop_machines': machines,
                'user_machines': machines_data
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cards', methods=['POST'])
def get_cards():
    """Get user cards"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
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
    """Get user referrals info"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({
                'referral_code': user.referral_code,
                'referrals_count': user.referrals_count,
                'referral_income': user.referral_income
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
                    # Update last_active to now (user is active in app)
                    user.last_active = now
                    return jsonify({
                        'offline_time': 0,
                        'offline_income': 0,
                        'offline_hash': 0
                    })
                
                offline_time = min(time_diff - 10, 3 * 60 * 60)  # 3 hours max, minus 10 seconds to exclude active time
            else:
                user.last_active = now
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
            
            # Update last_active to mark user is back in app
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
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
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
            elif action == 'set_coins':
                user.coins = value
            elif action == 'set_quanhash':
                user.quanhash = value
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


@app.route('/api/buy', methods=['POST'])
def buy_item():
    """Buy item from shop"""
    try:
        data = request.json
        user_id = data.get('user_id')
        item_type = data.get('item_type')
        price = data.get('price')
        
        if not user_id or not item_type or not price:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        # Ensure price is a float
        price = float(price) if price else 0
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
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
            elif item_type == 'auto_bot':
                # Auto-tap bot implementation
                taps_per_sec = data.get('taps_per_sec', 2)
                user.auto_tap_enabled = True
                user.auto_tap_level = getattr(user, 'auto_tap_level', 0) + 1
                user.auto_tap_speed = taps_per_sec
                # Store expiration (24 hours)
                from datetime import timedelta
                user.auto_tap_expires_at = datetime.utcnow() + timedelta(hours=24)
            
            db.commit()
            return jsonify({'success': True})
    except Exception as e:
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
        
        if not user_id or not category or not level or not price:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            if user.coins < price:
                return jsonify({'success': False, 'error': 'Недостаточно коинов'})
            
            user.coins -= price
            
            if category == 'tap_boost':
                # Increase tap reward (store in active_multiplier or create new field)
                user.active_multiplier = max(getattr(user, 'active_multiplier', 1), level)
            elif category == 'energy_buy':
                # Restore energy
                item_data = window.shopData['energy_buy']['items'][level - 1] if 'window' in dir() else None
                energy_to_restore = 50 * level  # Default formula
                if item_data:
                    energy_to_restore = item_data['bonus']
                user.energy = min(user.energy + energy_to_restore, user.max_energy)
            elif category == 'energy_expand':
                # Expand max energy
                item_data = window.shopData['energy_expand']['items'][level - 1] if 'window' in dir() else None
                energy_to_add = 200 * level  # Default formula
                if item_data:
                    energy_to_add = item_data['bonus']
                user.max_energy = getattr(user, 'max_energy', 1000) + energy_to_add
                user.energy = min(user.energy, user.max_energy)
            elif category == 'autobot':
                # Activate autobot
                item_data = window.shopData['autobot']['items'][level - 1] if 'window' in dir() else None
                from datetime import timedelta
                duration_minutes = item_data['duration'] if item_data else 30
                speed = item_data['speed'] if item_data else 2.0
                user.auto_tap_enabled = True
                user.auto_tap_level = level
                user.auto_tap_speed = speed
                user.auto_tap_expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
            
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
        
        if not user_id or not machine_id or not price:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            # Check balance
            if currency == 'coins':
                if user.coins < price:
                    return jsonify({'success': False, 'error': 'Недостаточно коинов'})
                user.coins -= price
            else:  # quanhash
                if user.quanhash < price:
                    return jsonify({'success': False, 'error': 'Недостаточно QuanHash'})
                user.quanhash -= price
            
            # Parse machine info from ID (format: starter_0, premium_15, etc)
            parts = machine_id.split('_')
            if len(parts) != 2:
                return jsonify({'success': False, 'error': 'Invalid machine ID'})
            
            machine_num = int(parts[1])
            if parts[0] == 'starter':
                hash_rate = round(0.05 * (machine_num + 1), 2)
                name = f'Стартовая машина #{machine_num + 1}'
            else:  # premium
                hash_rate = round(0.5 * (machine_num + 1), 2)
                name = f'Премиум машина #{machine_num + 1}'
            
            machine = MiningMachine(
                user_id=user.id,
                name=name,
                hash_rate=hash_rate,
                level=1,
                machine_type=machine_id
            )
            db.add(machine)
        
        return jsonify({'success': True})
    except Exception as e:
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
            
            # Get tasks with real progress
            tasks = [
                {
                    'id': 1,
                    'name': 'Ежедневный вход',
                    'emoji': '🚪',
                    'description': 'Зайдите в приложение',
                    'reward': 100,
                    'progress': 1,
                    'target': 1,
                    'completed': True
                },
                {
                    'id': 2,
                    'name': 'Тап мастер',
                    'emoji': '👆',
                    'description': f'Сделайте 100 тапов',
                    'reward': 500,
                    'progress': min(user.total_taps, 100),
                    'target': 100,
                    'completed': user.total_taps >= 100
                },
                {
                    'id': 3,
                    'name': 'Майнинг',
                    'emoji': '⚡',
                    'description': f'Заработайте 1000 QuanHash',
                    'reward': 1000,
                    'progress': min(int(user.quanhash), 1000),
                    'target': 1000,
                    'completed': user.quanhash >= 1000
                },
                {
                    'id': 4,
                    'name': 'Коллекционер',
                    'emoji': '💳',
                    'description': f'Купите 5 карточек',
                    'reward': 1500,
                    'progress': min(cards_count, 5),
                    'target': 5,
                    'completed': cards_count >= 5
                },
                {
                    'id': 5,
                    'name': 'Реферал',
                    'emoji': '👥',
                    'description': f'Пригласите 1 друга',
                    'reward': 2000,
                    'progress': min(user.referrals_count, 1),
                    'target': 1,
                    'completed': user.referrals_count >= 1
                },
            ]
            
            return jsonify({'tasks': tasks})
    except Exception as e:
        print(f"Daily tasks error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/claim_task', methods=['POST'])
def claim_task():
    """Claim task reward"""
    try:
        data = request.json
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        
        if not user_id or not task_id:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'})
            
            # Add reward (for task 1 - daily login)
            if task_id == 1:
                user.coins += 100
            
            return jsonify({'success': True})
    except Exception as e:
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
                
                top_users.append({
                    'username': u.username or 'Unknown',
                    'total_earned': int(u.total_earned or 0),
                    'coins': int(u.coins or 0),
                    'level': 1,  # Hardcoded, no level field in User model
                    'vip_level': vip_level,
                    'vip_badge': vip_badge,
                    'passive_income': passive_income_per_hour,
                    'quanhash': int(getattr(u, 'quanhash', 0) or 0),
                    'total_taps': int(u.total_taps or 0)
                })
            
            # Sort ONLY by total_earned (coins earned), ignore VIP for ranking
            top_users.sort(key=lambda x: -x['total_earned'])
            
            # Return only top 100
            top_users = top_users[:100]
            
            print(f"[TOP_USERS] Returning {len(top_users)} users")
            return jsonify({'users': top_users})
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
