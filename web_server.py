#!/usr/bin/env python3
"""
Quantum Nexus Web Server
Server for Telegram Web App
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import get_db
from models import User, MiningMachine, UserCard, Withdrawal
from utils import calculate_offline_income
from datetime import datetime
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
                    'is_frozen': getattr(u, 'is_frozen', False)
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
        
        if not user_id:
            # Try to get initData from request
            init_data = request.headers.get('X-Telegram-Init-Data')
            if init_data:
                # For now, skip validation, just log
                print(f"Init data received: {init_data[:50]}...")
        
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
            
            return jsonify({
                'coins': user.coins,
                'quanhash': user.quanhash,
                'energy': user.energy,
                'max_energy': user.max_energy,
                'total_taps': user.total_taps,
                'total_earned': user.total_earned,
                'passive_coins_per_hour': passive_coins_per_hour,
                'passive_hash_per_hour': passive_hash_per_hour
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
            
            # Calculate reward
            reward = BASE_TAP_REWARD * user.active_multiplier
            
            # Update user
            user.coins += reward
            user.energy -= ENERGY_COST_PER_TAP
            user.total_taps += 1
            user.total_earned += reward
            user.last_active = datetime.utcnow()
            
            db.commit()
            
            return jsonify({'success': True, 'reward': int(reward)})
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
    """Get shop items"""
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
            'coins': user.coins,
            'quanhash': user.quanhash
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mining', methods=['POST'])
def get_mining():
    """Get mining data"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        db = next(get_db())
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        machines = db.query(MiningMachine).filter_by(user_id=user.id).all()
        
        machines_data = []
        for machine in machines:
            machines_data.append({
                'id': machine.id,
                'name': machine.name,
                'level': machine.level,
                'hash_rate': machine.hash_rate,
                'income_per_hour': machine.hash_rate * 3600,
                'tag': 'premium' if machine.hash_rate > 0.1 else 'free'
            })
        
        return jsonify({
            'quanhash': user.quanhash,
            'machines': machines_data
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
        
        db = next(get_db())
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        cards = db.query(UserCard).filter_by(user_id=user.id).all()
        
        cards_data = []
        for card in cards:
            cards_data.append({
                'id': card.id,
                'card_type': card.card_type,
                'card_level': card.card_level,
                'income_per_minute': card.income_per_minute
            })
        
        return jsonify({
            'coins': user.coins,
            'cards': cards_data
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
        
        db = next(get_db())
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
            time_diff = (now - user.last_active).total_seconds()
            
            offline_time = min(time_diff, 3 * 60 * 60)  # 3 hours max
            offline_income = offline_time * 0.1  # 0.1 coins per second
            
            return jsonify({
                'offline_time': int(offline_time),
                'offline_income': offline_income
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
        
        if not user_id or not address:
            return jsonify({'error': 'Missing parameters'}), 400
        
        if not address.startswith('0x') or len(address) != 42:
            return jsonify({'success': False, 'error': 'Invalid BEP20 address'})
        
        db = next(get_db())
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        if user.quanhash < 500000:
            return jsonify({'success': False, 'error': 'Insufficient QuanHash'})
        
        # Create withdrawal record
        withdrawal = Withdrawal(
            user_id=user.id,
            amount=500000,
            usdt_amount=1.0,
            address=address
        )
        db.add(withdrawal)
        user.quanhash -= 500000
        
        db.commit()
        
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
            total_taps = db.query(func.sum(User.total_taps)).scalar() or 0
            total_revenue = db.query(func.sum(User.total_earned)).scalar() or 0
            pending_withdrawals = db.query(Withdrawal).filter_by(status='pending').count()
            
            # Advanced stats
            total_coins = db.query(func.sum(User.coins)).scalar() or 0
            total_quanhash = db.query(func.sum(User.quanhash)).scalar() or 0
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
        status = data.get('status')
        
        with get_db() as db:
            withdrawal = db.query(Withdrawal).filter_by(id=request_id).first()
            
            if not withdrawal:
                return jsonify({'success': False, 'error': 'Withdrawal not found'}), 404
            
            withdrawal.status = status
            withdrawal.processed_at = datetime.utcnow()
        
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
        
        db = next(get_db())
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
        elif item_type == 'double_energy':
            user.max_energy = 2000
        elif item_type == 'regen_boost':
            # TODO: Add regen boost
            pass
        elif item_type == 'common':
            card = UserCard(user_id=user.id, card_type='common', income_per_minute=0.5, is_active=True)
            db.add(card)
        elif item_type == 'rare':
            card = UserCard(user_id=user.id, card_type='rare', income_per_minute=2.0, is_active=True)
            db.add(card)
        elif item_type == 'epic':
            card = UserCard(user_id=user.id, card_type='epic', income_per_minute=10.0, is_active=True)
            db.add(card)
        elif item_type == 'legendary':
            card = UserCard(user_id=user.id, card_type='legendary', income_per_minute=50.0, is_active=True)
            db.add(card)
        elif item_type == 'auto_bot':
            # TODO: Add auto bot
            pass
        
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
        machine_type = data.get('machine_type')
        
        if not user_id or not machine_type:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        db = next(get_db())
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        machines_config = {
            'basic': {'price': 10000, 'hash_rate': 0.01, 'name': 'Базовая машина'},
            'advanced': {'price': 50000, 'hash_rate': 0.05, 'name': 'Продвинутая машина'},
            'pro': {'price': 200000, 'hash_rate': 0.2, 'name': 'Профессиональная машина'},
            'legendary': {'price': 1000000, 'hash_rate': 1.0, 'name': 'Легендарная машина'},
        }
        
        machine_config = machines_config.get(machine_type)
        if not machine_config:
            return jsonify({'success': False, 'error': 'Invalid machine type'})
        
        if user.coins < machine_config['price']:
            return jsonify({'success': False, 'error': 'Недостаточно коинов'})
        
        machine = MiningMachine(
            user_id=user.id,
            name=machine_config['name'],
            hash_rate=machine_config['hash_rate'],
            level=1
        )
        db.add(machine)
        user.coins -= machine_config['price']
        
        db.commit()
        
        return jsonify({'success': True})
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
