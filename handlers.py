# Quantum Nexus v6.7.49 - Removed duplicate emoji from invoice title
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from models import User, MiningMachine, UserCard, Transaction
from keyboards import *
from utils import *
from database import get_db, generate_referral_code
from config import *
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Check for special commands BEFORE doing anything else
    if context.args and context.args[0]:
        arg = context.args[0]
        
        # Check if it's a buy_stars command FIRST
        if arg.startswith('buy_stars_'):
            logger.info(f"Received buy_stars command: {arg}")
            try:
                product_id = int(arg.split('_')[2])
                logger.info(f"Processing buy_stars for product {product_id}")
                await send_stars_invoice(update, context, product_id)
                logger.info(f"send_stars_invoice completed for product {product_id}")
                return  # Don't show main menu, just send invoice
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid buy_stars parameter: {arg}, error: {e}")
    
    # If we got here, it's a normal /start command
    logger.info(f"Processing normal /start for user {user.id}")
    
    with get_db() as db:
        # Check if user exists
        db_user = db.query(User).filter_by(telegram_id=user.id).first()
        
        if not db_user:
            # Check if user has Telegram Premium
            is_premium = getattr(user, 'is_premium', False)
            
            # Create new user
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                referral_code=generate_referral_code(),
                is_premium=is_premium
            )
            db.add(db_user)
            db.flush()  # Get the ID
            
            # Check for referral
            if context.args and context.args[0]:
                arg = context.args[0]
                
                # Check for referral - use telegram_id as referral code
                referral_value = arg
                referrer = None
                
                # First try to find by telegram_id (most common case)
                try:
                    referral_telegram_id = int(referral_value)
                    referrer = db.query(User).filter_by(telegram_id=referral_telegram_id).first()
                    print(f"Looking for referrer by telegram_id: {referral_telegram_id}, found: {referrer is not None}")
                except ValueError:
                    # Try by referral_code if it's not a number
                    referrer = db.query(User).filter_by(referral_code=referral_value).first()
                    print(f"Looking for referrer by code: {referral_value}, found: {referrer is not None}")
                
                if referrer and referrer.id != db_user.id:
                    db_user.referred_by = referrer.id
                    referrer.referrals_count += 1
                    
                    # Give bonus based on premium status - EQUAL bonuses for both
                    if is_premium:
                        db_user.coins += REFERRAL_PREMIUM_BONUS  # Referral gets full bonus
                        referrer.coins += REFERRAL_PREMIUM_BONUS  # Referrer gets FULL bonus too
                        logger.info(f"Premium user {db_user.telegram_id} was referred by {referrer.telegram_id} - both get {REFERRAL_PREMIUM_BONUS}")
                    else:
                        db_user.coins += REFERRAL_BONUS  # Referral gets full bonus
                        referrer.coins += REFERRAL_BONUS  # Referrer gets FULL bonus too
                        logger.info(f"User {db_user.telegram_id} was referred by {referrer.telegram_id} - both get {REFERRAL_BONUS}")
        
        # Update premium status for existing users
        else:
            is_premium = getattr(user, 'is_premium', False)
            if db_user.is_premium != is_premium:
                db_user.is_premium = is_premium
                logger.info(f"Updated premium status for user {db_user.telegram_id}: {is_premium}")
        
        # Calculate offline income
        offline_income = calculate_offline_income(db_user)
        if offline_income > 0:
            db_user.coins += offline_income
            db_user.total_earned += offline_income
            try:
                transaction = Transaction(
                    user_id=db_user.id,
                    transaction_type="offline_income",
                    amount=offline_income,
                    currency="coins"
                )
                db.add(transaction)
            except Exception as e:
                logger.warning(f"Could not create transaction: {e}")
        
        db_user.last_active = datetime.utcnow()
    
    message = """<b>Quantum Nexus</b>
    
Крипто-тапалка нового поколения с уникальными возможностями майнинга и пассивного дохода.

🔥 <b>Возможности:</b>
• Система тапа с энергией
• Майнинг QuanHash (обменивается на USDT)
• Пассивный доход от карточек
• Реферальная система
• Магазин бустов и улучшений
• Поддержка вывода средств

💎 <b>Что вас ждет:</b>
Развивайте свою крипто-империю, покупайте майнинг-машины, собирайте карточки для пассивного дохода и развивайтесь с друзьями!

🚀 <b>Начните прямо сейчас!</b>

Выберите действие:"""
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Открыть игру", web_app=WebAppInfo(url="https://quantum-nexus.ru/game_v4.html?" + str(int(__import__('time').time()))))
        ]
    ]
    
    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db = next(get_db())
    db_user = db.query(User).filter_by(telegram_id=user_id).first()
    
    if not db_user:
        return
    
    data = query.data
    
    if data == "main_menu":
        await show_main_menu(query, db_user)
    elif data == "tap":
        await handle_tap(query, db_user, db)
    elif data == "energy_status":
        await show_energy_status(query, db_user)
    elif data == "mining":
        await show_mining(query, db_user, db)
    elif data == "cards":
        await show_user_cards(query, db_user, db)
    elif data == "shop":
        await show_shop(query, db_user)
    elif data == "stats":
        await show_stats(query, db_user)
    elif data == "rating":
        await show_rating(query, db_user, db)
    elif data == "referrals":
        await show_referrals(query, db_user, db)
    elif data.startswith("shop_"):
        await handle_shop(query, data, db_user, db)
    elif data.startswith("buy_"):
        await handle_purchase(query, data, db_user, db)
    elif data.startswith("machine_"):
        await handle_machine(query, data, db_user, db)
    elif data.startswith("card_"):
        await handle_card(query, data, db_user, db)


async def show_main_menu(query, user):
    """Show main menu"""
    message = f"""
🏠 <b>Главное меню</b>

💰 Коины: {format_currency(user.coins)} 🪙
💎 QuanHash: {format_currency(user.quanhash)} ⚡
⚡ Энергия: {user.energy}/{user.max_energy}

Выберите действие:
    """
    
    await query.edit_message_text(
        message,
        reply_markup=get_main_menu(),
        parse_mode='HTML'
    )


async def handle_tap(query, user, db):
    """Handle tap action"""
    current_time = datetime.utcnow().timestamp()
    
    # Anti-cheat check
    if not check_anti_cheat(user.id, current_time):
        await query.answer("⚠️ Слишком быстро! Подождите немного.", show_alert=True)
        return
    
    # Check energy
    if user.energy < ENERGY_COST_PER_TAP:
        await query.answer("⚠️ Недостаточно энергии!", show_alert=True)
        return
    
    # Calculate reward
    reward = BASE_TAP_REWARD * user.active_multiplier
    
    # Update user
    user.coins += reward
    user.energy -= ENERGY_COST_PER_TAP
    user.total_taps += 1
    user.total_earned += reward
    user.last_active = datetime.utcnow()
    
    # Update multiplier if expired
    if user.multiplier_expires_at and datetime.utcnow() > user.multiplier_expires_at:
        user.active_multiplier = 1.0
        user.multiplier_expires_at = None
    
    db.commit()
    
    # Create transaction
    transaction = Transaction(
        user_id=user.id,
        transaction_type="tap",
        amount=reward,
        currency="coins"
    )
    db.add(transaction)
    db.commit()
    
    await query.answer(f"💰 +{format_currency(reward)} 🪙")


async def show_energy_status(query, user):
    """Show energy status"""
    # Regenerate energy over time
    time_since_update = (datetime.utcnow() - user.updated_at).total_seconds() / 60
    energy_to_add = int(time_since_update * ENERGY_REGEN_PER_MINUTE)
    
    if energy_to_add > 0:
        user.energy = min(user.energy + energy_to_add, user.max_energy)
        db = next(get_db())
        db_user = db.query(User).filter_by(id=user.id).first()
        db_user.energy = user.energy
        db_user.updated_at = datetime.utcnow()
        db.commit()
    
    message = f"""
⚡ <b>Энергия</b>

⚡ Текущая энергия: {user.energy}/{user.max_energy}

⚡ Энергия восстанавливается: {ENERGY_REGEN_PER_MINUTE} ед/мин
⏱️ До полной восстановления: {int((user.max_energy - user.energy) / ENERGY_REGEN_PER_MINUTE)} мин

Вы можете купить больше энергии в магазине!
    """
    
    await query.edit_message_text(
        message,
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )


async def show_mining(query, user, db):
    """Show mining menu"""
    machines = db.query(MiningMachine).filter_by(user_id=user.id).all()
    
    if not machines:
        message = f"""
🏭 <b>Майнинг</b>

У вас пока нет криптомашин! Купите первую в магазине.
        """
    else:
        message = f"""
🏭 <b>Майнинг</b>

💰 Коины: {format_currency(user.coins)} 🪙
💎 QuanHash: {format_currency(user.quanhash)} ⚡

👀 Выберите машину для управления:
        """
    
    await query.edit_message_text(
        message,
        reply_markup=get_mining_menu(db, user),
        parse_mode='HTML'
    )


async def show_user_cards(query, user, db):
    """Show user cards"""
    cards = db.query(UserCard).filter_by(user_id=user.id).all()
    
    if not cards:
        message = f"""
💳 <b>Карточки</b>

У вас пока нет карточек! Купите первую в магазине.
        """
    else:
        total_income = sum(card.income_per_minute for card in cards if card.is_active)
        message = f"""
💳 <b>Карточки</b>

📊 Всего карточек: {len(cards)}
💰 Пассивный доход: {format_currency(total_income)} 🪙/мин

👀 Выберите карточку:
        """
    
    await query.edit_message_text(
        message,
        reply_markup=get_user_cards_menu(db, user),
        parse_mode='HTML'
    )


async def show_shop(query, user):
    """Show shop menu"""
    message = f"""
🛒 <b>Магазин</b>

💰 Коины: {format_currency(user.coins)} 🪙
💎 QuanHash: {format_currency(user.quanhash)} ⚡

Выберите категорию:
    """
    
    await query.edit_message_text(
        message,
        reply_markup=get_shop_menu(),
        parse_mode='HTML'
    )


async def show_stats(query, user):
    """Show user statistics"""
    rank_coins = get_user_rank(next(get_db()), user, "coins")
    rank_hash = get_user_rank(next(get_db()), user, "quanhash")
    
    message = f"""
📊 <b>Статистика</b>

👤 <b>Профиль:</b>
💰 Коины: {format_currency(user.coins)} 🪙
💎 QuanHash: {format_currency(user.quanhash)} ⚡
⚡ Энергия: {user.energy}/{user.max_energy}

📈 <b>Достижения:</b>
👆 Всего тапов: {user.total_taps}
💵 Заработано: {format_currency(user.total_earned)} 🪙
⛏️ Добыто QuanHash: {format_currency(user.total_mined)} ⚡

🏆 <b>Рейтинг:</b>
🪙 По коинам: #{rank_coins}
⚡ По QuanHash: #{rank_hash}

👥 <b>Рефералы:</b>
📊 Всего рефералов: {user.referrals_count}
💰 Доход с рефералов: {format_currency(user.referral_income)} 🪙
    """
    
    await query.edit_message_text(
        message,
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )


async def show_rating(query, user, db):
    """Show rating/leaderboard"""
    top_coins = get_top_users(db, "coins", 10)
    top_hash = get_top_users(db, "quanhash", 10)
    
    message = "<b>🏆 Рейтинг игроков</b>\n\n"
    message += "<b>💰 Топ по коинам:</b>\n"
    
    for i, top_user in enumerate(top_coins, 1):
        message += f"{i}. {top_user.username or 'Игрок'} - {format_currency(top_user.total_earned)} 🪙\n"
    
    message += "\n<b>⚡ Топ по QuanHash:</b>\n"
    
    for i, top_user in enumerate(top_hash, 1):
        message += f"{i}. {top_user.username or 'Игрок'} - {format_currency(top_user.total_mined)} ⚡\n"
    
    await query.edit_message_text(
        message,
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )


async def show_referrals(query, user, db):
    """Show referral information"""
    message = f"""
👥 <b>Реферальная система</b>

🆔 Ваш реферальный код:
<code>{user.referral_code}</code>

📊 Статистика:
👥 Всего рефералов: {user.referrals_count}
💰 Доход с рефералов: {format_currency(user.referral_income)} 🪙

🔗 Ваша реферальная ссылка:
<code>https://t.me/{context.bot.username}?start={user.referral_code}</code>

💡 За каждого нового реферала вы получаете бонусы!
    """
    
    await query.edit_message_text(
        message,
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )


async def handle_shop(query, data, user, db):
    """Handle shop submenu"""
    if data == "shop_boosts":
        await query.edit_message_reply_markup(get_boosts_menu())
    elif data == "shop_machines":
        await query.edit_message_reply_markup(get_machines_menu())
    elif data == "shop_cards":
        await query.edit_message_reply_markup(get_cards_menu())
    elif data == "shop_energy":
        await query.edit_message_text(
            "⚡ Купить 50 энергии за 1000 🪙",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Купить", callback_data="buy_energy_50")
            ], [InlineKeyboardButton("⬅️ Назад", callback_data="shop")]])
        )


async def handle_purchase(query, data, user, db):
    """Handle purchases"""
    if data == "buy_energy_50":
        price = 1000
        if user.coins >= price:
            user.coins -= price
            user.energy = min(user.energy + 50, user.max_energy)
            db.commit()
            await query.answer("✅ Энергия куплена!")
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    # Handle other purchases similarly...


async def pre_checkout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pre-checkout query for Stars payment validation"""
    query = update.pre_checkout_query
    
    user_id = query.from_user.id
    
    with get_db() as db:
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            await query.answer(ok=False, error_message="Пользователь не найден")
            return
        
        # Validate payload
        invoice_payload = query.invoice_payload
        
        if not invoice_payload.startswith("stars_"):
            await query.answer(ok=False, error_message="Неверный invoice")
            return
        
        # Approve the checkout
        await query.answer(ok=True)


async def successful_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful Stars payment - only called when payment is REAL"""
    payment = update.message.successful_payment
    user_id = update.effective_user.id
    
    # Log the payment details
    logger.info(f"Payment received: {payment}")
    logger.info(f"Payment invoice: {payment.invoice_payload}")
    logger.info(f"Payment total amount: {payment.total_amount}")
    logger.info(f"Payment currency: {payment.currency}")
    
    # Parse payload: stars_{user_id}_{product_id}
    invoice_payload = payment.invoice_payload
    
    # Verify this is a Stars payment
    if payment.currency != "XTR":
        logger.error(f"Wrong currency: {payment.currency}, expected XTR")
        await update.message.reply_text("❌ Ошибка: неверная валюта")
        return
    
    try:
        parts = invoice_payload.split("_")
        if len(parts) != 3 or parts[0] != "stars":
            logger.error(f"Invalid payload format: {invoice_payload}")
            await update.message.reply_text("❌ Ошибка: неверный payload")
            return
        
        user_db_id = int(parts[1])
        product_id = int(parts[2])
        
        # Define product amounts - 60 items
        # Note: Products 41-50 are COMBO (handled separately), products 31-40 are QuanHash (handled separately)
        product_coins = {
            # STARTER (1-10): 20,000 to 200,000
            1: 20000, 2: 40000, 3: 60000, 4: 80000, 5: 100000, 6: 120000, 7: 140000, 8: 160000, 9: 180000, 10: 200000,
            # PREMIUM (11-20): 120,000 to 500,000
            11: 120000, 12: 160000, 13: 220000, 14: 280000, 15: 340000, 16: 380000, 17: 420000, 18: 450000, 19: 480000, 20: 500000,
            # VIP (21-30): 400,000 to 2,000,000
            21: 400000, 22: 600000, 23: 800000, 24: 1000000, 25: 1200000, 26: 1400000, 27: 1600000, 28: 1800000, 29: 1900000, 30: 2000000,
            # QUANHASH (31-40): handled in limited logic
            31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: 0, 40: 0,
            # COMBO (41-50): cards + coins handled separately
            41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0,
            # MEGA (51-60): 50,000 to 5,000,000
            51: 50000, 52: 600000, 53: 1100000, 54: 1800000, 55: 2500000, 56: 3300000, 57: 3800000, 58: 4400000, 59: 4700000, 60: 5000000
        }
        
        # Define QuanHash products (31-40): QuanHash currency from Buy Currency modal
        quanhash_products = {
            31: 500, 32: 7000, 33: 15000, 34: 30000, 35: 60000,
            36: 100000, 37: 150000, 38: 200000, 39: 250000, 40: 300000
        }
        
        # VIP products have been moved to separate VIP Shop modal (handled via different productIds)
        # Note: VIP functions in VIP Shop use different IDs to avoid conflict with Buy Currency
        vip_products = {}
        
        # Define COMBO products (41-50): cards + coins
        combo_products = {
            41: {'cards': 10, 'coins': 300000},
            42: {'cards': 20, 'coins': 800000},
            43: {'cards': 50, 'coins': 1500000},
            44: {'cards': 100, 'coins': 2500000},
            45: {'cards': 200, 'coins': 4000000},
            46: {'cards': 500, 'coins': 5500000},
            47: {'cards': 1000, 'coins': 7000000},
            48: {'cards': 2000, 'coins': 8500000},
            49: {'cards': 5000, 'coins': 10000000},
            50: {'cards': 10000, 'coins': 15000000}
        }
        
        with get_db() as db:
            user = db.query(User).filter_by(id=user_db_id, telegram_id=user_id).first()
            
            if not user:
                logger.error(f"User not found: {user_db_id}/{user_id}")
                await update.message.reply_text("❌ Ошибка: пользователь не найден")
                return
            
            # Handle VIP products - define VIP products with their effects
            vip_message = ""
            vip_products_info = {
                81: {'type': 'tap_boost', 'effect': 25, 'name': 'Звездный Шторм'},
                82: {'type': 'tap_boost', 'effect': 35, 'name': 'Черная Дыра'},
                83: {'type': 'tap_boost', 'effect': 50, 'name': 'Абсолют'},
                84: {'type': 'tap_boost', 'effect': 70, 'name': 'Имперский'},
                85: {'type': 'tap_boost', 'effect': 100, 'name': 'Легендарный'},
                86: {'type': 'energy_buy', 'effect': 1.5, 'name': 'Солнечная Корона'},
                87: {'type': 'energy_buy', 'effect': 2.25, 'name': 'Галактический Ядро'},
                88: {'type': 'energy_buy', 'effect': 3.0, 'name': 'Новая Ера'},
                89: {'type': 'energy_buy', 'effect': 4.0, 'name': 'Квантовый Реактор'},
                90: {'type': 'energy_buy', 'effect': 5.0, 'name': 'Небесный Портал'},
                91: {'type': 'energy_expand', 'effect': 3750, 'name': 'Галактический Резервуар'},
                92: {'type': 'energy_expand', 'effect': 6250, 'name': 'Квантовая Суперпозиция'},
                93: {'type': 'energy_expand', 'effect': 10000, 'name': 'Звездное Созвездие'},
                94: {'type': 'energy_expand', 'effect': 18750, 'name': 'Абсолютная Пустота'},
                95: {'type': 'energy_expand', 'effect': 37500, 'name': 'Имперская Сокровищница'},
                96: {'type': 'autobot', 'effect': 3, 'name': 'VIP Базовый Бот', 'duration': 14400},  # 240 minutes * 60 = 14400 seconds (4 hours)
                97: {'type': 'autobot', 'effect': 3.25, 'name': 'VIP Улучшенный Бот', 'duration': 43200},  # 720 minutes * 60 = 43200 seconds (12 hours)
                98: {'type': 'autobot', 'effect': 3.5, 'name': 'VIP Продвинутый Бот', 'duration': 172800},  # 2880 minutes * 60 = 172800 seconds (2 days)
                99: {'type': 'autobot', 'effect': 3.75, 'name': 'VIP Элитный Бот', 'duration': 432000},  # 7200 minutes * 60 = 432000 seconds (5 days)
                100: {'type': 'autobot', 'effect': 4, 'name': 'VIP Премиум Бот', 'duration': 864000}  # 14400 minutes * 60 = 864000 seconds (10 days)
            }
            
            if product_id in vip_products_info:
                vip_info = vip_products_info[product_id]
                
                if vip_info['type'] == 'tap_boost':
                    # Add tap boost effect
                    user.active_multiplier += vip_info['effect']
                    vip_message = f"\n\n⚡ VIP Бустер активирован!\n💪 {vip_info['name']}: +{vip_info['effect']} коинов за тап"
                    
                elif vip_info['type'] == 'energy_buy':
                    # Add energy regeneration
                    user.energy_regen_rate += vip_info['effect']
                    vip_message = f"\n\n🔋 VIP Генератор активирован!\n⚡ {vip_info['name']}: +{vip_info['effect']} энергии в секунду"
                    
                elif vip_info['type'] == 'energy_expand':
                    # Add max energy
                    user.max_energy += vip_info['effect']
                    user.energy = min(user.energy, user.max_energy)
                    vip_message = f"\n\n🔋 VIP Батарея активирована!\n📈 {vip_info['name']}: +{vip_info['effect']} максимальной энергии"
                    
                elif vip_info['type'] == 'autobot':
                    # Add autobot with proper duration
                    duration_seconds = vip_info['duration']  # duration is already in seconds
                    user.auto_tap_level = 1  # Set autobot level
                    user.auto_tap_speed = vip_info['effect']  # Set autobot speed
                    user.auto_tap_expires_at = int(time.time()) + duration_seconds  # Set expiration time
                    vip_message = f"\n\n🤖 VIP Бот активирован!\n⚡ {vip_info['name']}: автотап на {duration_seconds // 60} минут"
            elif product_id >= 71 and product_id <= 76:
                # Handle VIP mining machines (71-76)
                vip_mining_map = {
                    71: 'vip_quantum_prime',
                    72: 'vip_solar_core',
                    73: 'vip_black_hole',
                    74: 'vip_nebula',
                    75: 'vip_multiverse',
                    76: 'vip_infinity'
                }
                machine_id = vip_mining_map.get(product_id)
                
                if machine_id:
                    import json
                    vip_levels = json.loads(user.mining_vip_levels or '{}')
                    current_level = vip_levels.get(machine_id, 0)
                    new_level = current_level + 1
                    
                    # Check max level
                    if new_level > 50:
                        await update.message.reply_text("❌ Ошибка: Максимальный уровень достигнут")
                        return
                    
                    vip_levels[machine_id] = new_level
                    user.mining_vip_levels = json.dumps(vip_levels)
                    vip_message = f"\n\n🏭 VIP Машина улучшена!\n⚡ Уровень {new_level}/50"
            elif product_id >= 101 and product_id <= 116:
                # Handle VIP Cards (101-116): VIP cards with passive income
                vip_cards_map = {
                    # Per hour cards (101-106)
                    101: {'income': 300, 'name': 'VIP Silver'},
                    102: {'income': 800, 'name': 'VIP Gold'},
                    103: {'income': 1800, 'name': 'VIP Platinum'},
                    104: {'income': 4000, 'name': 'VIP Diamond'},
                    105: {'income': 9000, 'name': 'VIP Elite'},
                    106: {'income': 20000, 'name': 'VIP Ultimate'},
                    # Per minute cards (111-116)
                    111: {'income': 15, 'name': 'VIP Nova'},
                    112: {'income': 50, 'name': 'VIP Quantum'},
                    113: {'income': 150, 'name': 'VIP Cosmic'},
                    114: {'income': 350, 'name': 'VIP Stellar'},
                    115: {'income': 600, 'name': 'VIP Galaxy'},
                    116: {'income': 1000, 'name': 'VIP Infinity'}
                }
                
                card_info = vip_cards_map.get(product_id)
                if card_info:
                    # Add a UserCard for passive income
                    import random
                    new_card = UserCard(
                        user_id=user.id,
                        card_type='legendary',
                        income_per_minute=float(card_info['income']) / 60.0 if product_id >= 101 and product_id <= 106 else float(card_info['income']),
                        card_level=1,
                        experience=0,
                        experience_to_next_level=100,
                        is_active=True
                    )
                    db.add(new_card)
                    income_text = f"{card_info['income']:,} 🪙/час" if product_id >= 101 and product_id <= 106 else f"{card_info['income']:,} 🪙/мин"
                    vip_message = f"\n\n🎴 VIP Карта получена!\n💎 {card_info['name']}: {income_text}"
            elif product_id >= 31 and product_id <= 40:
                # Handle QuanHash products (31-40): QuanHash currency from Buy Currency
                quanhash_to_add = quanhash_products.get(product_id, 0)
                if quanhash_to_add == 0:
                    logger.error(f"Unknown QuanHash product: {product_id}")
                    await update.message.reply_text("❌ Ошибка: неизвестный товар QuanHash")
                    return
                
                user.quanhash += quanhash_to_add
                vip_message = f"\n\n💎 Получено: {quanhash_to_add:,} QuanHash"
            elif product_id >= 41 and product_id <= 50:
                # Handle COMBO products (41-50): cards + coins
                combo_info = combo_products.get(product_id)
                if combo_info:
                    # Add coins
                    user.coins += combo_info['coins']
                    
                    # Add cards as UserCard objects
                    import random
                    for _ in range(combo_info['cards']):
                        new_card = UserCard(
                            user_id=user.id,
                            card_type='epic',
                            income_per_minute=100.0,
                            card_level=1,
                            experience=0,
                            experience_to_next_level=100,
                            is_active=True
                        )
                        db.add(new_card)
                    
                    vip_message = f"\n\n🎴 Получено: {combo_info['cards']:,} карточек\n💰 Получено: {combo_info['coins']:,} коинов"
            else:
                # Handle regular coin products (1-20, 31-60, 51-70, 77-80)
                coins_to_add = product_coins.get(product_id, 0)
                if coins_to_add == 0:
                    logger.error(f"Unknown product: {product_id}")
                    await update.message.reply_text("❌ Ошибка: неизвестный товар")
                    return
                
                user.coins += coins_to_add
                vip_message = f"\n\n💰 Получено: {coins_to_add:,} коинов"
            
            db.commit()
            
            # Log successful payment
            if product_id in vip_products_info:
                vip_name = vip_products_info[product_id]['name']
                logger.info(f"✅ VIP Function Stars payment successful! User {user_id} bought VIP product {product_id}: {vip_name}")
            elif product_id >= 101 and product_id <= 116:
                logger.info(f"✅ VIP Card Stars payment successful! User {user_id} bought VIP card product {product_id}")
            elif product_id >= 31 and product_id <= 40:
                quanhash_added = quanhash_products.get(product_id, 0)
                logger.info(f"✅ QuanHash Stars payment successful! User {user_id} bought product {product_id} for {quanhash_added} QuanHash")
            elif product_id >= 41 and product_id <= 50:
                combo_info = combo_products.get(product_id)
                logger.info(f"✅ COMBO Stars payment successful! User {user_id} bought product {product_id}: {combo_info['cards']} cards + {combo_info['coins']} coins")
            elif product_id >= 71 and product_id <= 76:
                logger.info(f"✅ VIP Mining Stars payment successful! User {user_id} bought VIP mining product {product_id}")
            else:
                coins_to_add = product_coins.get(product_id, 0)
                logger.info(f"✅ Stars payment successful! User {user_id} bought product {product_id} for {coins_to_add} coins")
            
            # Send success message
            if product_id in vip_products_info:
                # VIP products already have message in vip_message
                await update.message.reply_text(
                    f"✨ VIP Покупка успешна!\n\n"
                    f"💎 Оплачено: {payment.total_amount} ⭐\n"
                    f"📊 Новый баланс: {user.coins:,} коинов"
                    + vip_message
                )
            elif product_id >= 31 and product_id <= 40:
                # QuanHash products already have message in vip_message
                await update.message.reply_text(
                    f"✨ QuanHash покупка успешна!\n\n"
                    f"💎 Оплачено: {payment.total_amount} ⭐\n"
                    f"📊 Новый баланс QuanHash: {user.quanhash:,} 💎"
                    + vip_message
                )
            elif product_id >= 41 and product_id <= 50:
                # COMBO products already have message in vip_message
                await update.message.reply_text(
                    f"✨ Комбо покупка успешна!\n\n"
                    f"💎 Оплачено: {payment.total_amount} ⭐\n"
                    f"📊 Новый баланс: {user.coins:,} коинов"
                    + vip_message
                )
            elif product_id >= 71 and product_id <= 76:
                # VIP Mining already have message in vip_message
                await update.message.reply_text(
                    f"✨ VIP Машина успешна!\n\n"
                    f"💎 Оплачено: {payment.total_amount} ⭐"
                    + vip_message
                )
            elif product_id >= 101 and product_id <= 116:
                # VIP Cards already have message in vip_message
                await update.message.reply_text(
                    f"✨ VIP Карта успешна!\n\n"
                    f"💎 Оплачено: {payment.total_amount} ⭐\n"
                    f"📊 Новый баланс: {user.coins:,} коинов"
                    + vip_message
                )
            else:
                coins_to_add = product_coins.get(product_id, 0)
                await update.message.reply_text(
                    f"✨ Покупка успешна!\n\n"
                    f"💎 Оплачено: {payment.total_amount} ⭐\n"
                    f"💰 Получено: {coins_to_add:,} коинов\n"
                    f"📊 Новый баланс: {user.coins:,} коинов"
                    + vip_message
                )
            
    except Exception as e:
        logger.error(f"Error processing payment: {e}", exc_info=True)
        await update.message.reply_text("❌ Ошибка при обработке платежа")


async def send_stars_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE, product_id: int):
    """Send Stars invoice with real Telegram Stars payment"""
    
    logger.info(f"=== send_stars_invoice called with product_id={product_id} ===")
    
    # Define products with Stars prices - matching web_app.html Buy Currency modal
    # VIP Functions (21-40) and VIP Cards (51-66) are handled separately in VIP Shop/Cards modals
    products = {
        # BUY CURRENCY - STARTER (1-10): 20,000 to 200,000 coins
        1: {'title': '💫 Первые шаги', 'description': '20,000 коинов', 'stars': 50, 'coins': 20000},
        2: {'title': '✨ Базовый старт', 'description': '40,000 коинов', 'stars': 120, 'coins': 40000},
        3: {'title': '⭐ Начало пути', 'description': '60,000 коинов', 'stars': 180, 'coins': 60000},
        4: {'title': '💎 Приветственный', 'description': '80,000 коинов', 'stars': 240, 'coins': 80000},
        5: {'title': '🎁 Добро пожаловать', 'description': '100,000 коинов', 'stars': 320, 'coins': 100000},
        6: {'title': '💰 Стартовый пакет', 'description': '120,000 коинов', 'stars': 400, 'coins': 120000},
        7: {'title': '⚡ Быстрый старт', 'description': '140,000 коинов', 'stars': 480, 'coins': 140000},
        8: {'title': '🎯 Первый шаг', 'description': '160,000 коинов', 'stars': 560, 'coins': 160000},
        9: {'title': '🌈 Радужный набор', 'description': '180,000 коинов', 'stars': 640, 'coins': 180000},
        10: {'title': '💫 Волшебный старт', 'description': '200,000 коинов', 'stars': 720, 'coins': 200000},
        # BUY CURRENCY - PREMIUM (11-20): 120,000 to 500,000 coins
        11: {'title': '⚡ Световой пакет', 'description': '120,000 коинов', 'stars': 300, 'coins': 120000},
        12: {'title': '🎯 Профессионал', 'description': '160,000 коинов', 'stars': 600, 'coins': 160000},
        13: {'title': '🚀 Мощный набор', 'description': '220,000 коинов', 'stars': 900, 'coins': 220000},
        14: {'title': '💎 Алмазный пакет', 'description': '280,000 коинов', 'stars': 1200, 'coins': 280000},
        15: {'title': '🔥 Огненный набор', 'description': '340,000 коинов', 'stars': 1500, 'coins': 340000},
        16: {'title': '⚡ Электронный', 'description': '380,000 коинов', 'stars': 1800, 'coins': 380000},
        17: {'title': '🌟 Звёздный пакет', 'description': '420,000 коинов', 'stars': 2100, 'coins': 420000},
        18: {'title': '💫 Космический', 'description': '450,000 коинов', 'stars': 2400, 'coins': 450000},
        19: {'title': '🎁 Подарочный VIP', 'description': '480,000 коинов', 'stars': 2700, 'coins': 480000},
        20: {'title': '🔮 Магический', 'description': '500,000 коинов', 'stars': 3000, 'coins': 500000},
        # BUY CURRENCY - VIP (21-30): 400,000 to 2,000,000 coins
        21: {'title': '💎 VIP стартовый', 'description': '400,000 коинов', 'stars': 1000, 'coins': 400000},
        22: {'title': '🚀 VIP ускорение', 'description': '600,000 коинов', 'stars': 1600, 'coins': 600000},
        23: {'title': '👑 VIP статус', 'description': '800,000 коинов', 'stars': 2400, 'coins': 800000},
        24: {'title': '⚡ VIP турбо', 'description': '1,000,000 коинов', 'stars': 3200, 'coins': 1000000},
        25: {'title': '💎 VIP королевство', 'description': '1,200,000 коинов', 'stars': 4000, 'coins': 1200000},
        26: {'title': '🔓 VIP безлимит', 'description': '1,400,000 коинов', 'stars': 5000, 'coins': 1400000},
        27: {'title': '🏆 VIP чемпион', 'description': '1,600,000 коинов', 'stars': 6000, 'coins': 1600000},
        28: {'title': '🌟 VIP легенда', 'description': '1,800,000 коинов', 'stars': 7000, 'coins': 1800000},
        29: {'title': '💎 VIP алмаз', 'description': '1,900,000 коинов', 'stars': 8000, 'coins': 1900000},
        30: {'title': '👑 VIP император', 'description': '2,000,000 коинов', 'stars': 9000, 'coins': 2000000},
        # BUY CURRENCY - QUANHASH (31-40): 500 to 300,000 QuanHash
        31: {'title': '🔮 Starter Hash', 'description': '500 QuanHash', 'stars': 150, 'coins': 0, 'quanhash': 500},
        32: {'title': '💎 Basic Hash', 'description': '7,000 QuanHash', 'stars': 300, 'coins': 0, 'quanhash': 7000},
        33: {'title': '⚡ Power Hash', 'description': '15,000 QuanHash', 'stars': 600, 'coins': 0, 'quanhash': 15000},
        34: {'title': '🔥 Fire Hash', 'description': '30,000 QuanHash', 'stars': 900, 'coins': 0, 'quanhash': 30000},
        35: {'title': '💥 Blast Hash', 'description': '60,000 QuanHash', 'stars': 1500, 'coins': 0, 'quanhash': 60000},
        36: {'title': '🌟 Stellar Hash', 'description': '100,000 QuanHash', 'stars': 2400, 'coins': 0, 'quanhash': 100000},
        37: {'title': '💎 Diamond Hash', 'description': '150,000 QuanHash', 'stars': 3600, 'coins': 0, 'quanhash': 150000},
        38: {'title': '🚀 Rocket Hash', 'description': '200,000 QuanHash', 'stars': 5100, 'coins': 0, 'quanhash': 200000},
        39: {'title': '👑 Crown Hash', 'description': '250,000 QuanHash', 'stars': 7200, 'coins': 0, 'quanhash': 250000},
        40: {'title': '💫 Ultimate Hash', 'description': '300,000 QuanHash', 'stars': 10000, 'coins': 0, 'quanhash': 300000},
        # BUY CURRENCY - COMBO (41-50): cards + coins
        41: {'title': '🎁 Стартовый мегасет', 'description': '10 карточек + 300,000 коинов', 'stars': 5000, 'coins': 0},
        42: {'title': '🔥 Горячий комбо', 'description': '20 карточек + 800,000 коинов', 'stars': 7000, 'coins': 0},
        43: {'title': '💎 Элитный набор', 'description': '50 карточек + 1,500,000 коинов', 'stars': 9000, 'coins': 0},
        44: {'title': '🚀 Мега связка', 'description': '100 карточек + 2,500,000 коинов', 'stars': 11000, 'coins': 0},
        45: {'title': '🌟 Легендарный мегасет', 'description': '200 карточек + 4,000,000 коинов', 'stars': 13000, 'coins': 0},
        46: {'title': '💎 Бриллиантовая связка', 'description': '500 карточек + 5,500,000 коинов', 'stars': 15000, 'coins': 0},
        47: {'title': '👑 Королевский комбо', 'description': '1,000 карточек + 7,000,000 коинов', 'stars': 17000, 'coins': 0},
        48: {'title': '🔥 Огненный мегасет', 'description': '2,000 карточек + 8,500,000 коинов', 'stars': 19000, 'coins': 0},
        49: {'title': '💫 Космический комбо', 'description': '5,000 карточек + 10,000,000 коинов', 'stars': 21000, 'coins': 0},
        50: {'title': '🎯 АБСОЛЮТ ВСЁ', 'description': '10,000 карточек + 15,000,000 коинов', 'stars': 24000, 'coins': 0},
        # BUY CURRENCY - MEGA (51-60): 50,000 to 5,000,000 coins
        51: {'title': '👑 VIP Всё включено', 'description': '50,000 коинов', 'stars': 1800, 'coins': 50000},
        52: {'title': '⭐ Эксклюзивный бейдж', 'description': '600,000 коинов', 'stars': 2500, 'coins': 600000},
        53: {'title': '🏆 Гарантирован топ', 'description': '1,100,000 коинов', 'stars': 4000, 'coins': 1100000},
        54: {'title': '⚡ Мгновенный доход', 'description': '1,800,000 коинов', 'stars': 6000, 'coins': 1800000},
        55: {'title': '🔓 Снять лимиты', 'description': '2,500,000 коинов', 'stars': 8000, 'coins': 2500000},
        56: {'title': '🚀 Автопрокачка', 'description': '3,300,000 коинов', 'stars': 10000, 'coins': 3300000},
        57: {'title': '💎 Приоритет помощь', 'description': '3,800,000 коинов', 'stars': 3500, 'coins': 3800000},
        58: {'title': '👑 Золотой профиль', 'description': '4,400,000 коинов', 'stars': 4500, 'coins': 4400000},
        59: {'title': '🌟 Супер статус', 'description': '4,700,000 коинов', 'stars': 7000, 'coins': 4700000},
        60: {'title': '🎯 АБСОЛЮТ ВСЁ VIP', 'description': '5,000,000 коинов', 'stars': 15000, 'coins': 5000000},
        # VIP MINING MACHINES (71-76)
        71: {'title': '⚡ Quantum Prime', 'description': 'Элитный квантовый майнер VIP уровня', 'stars': 50, 'coins': 0, 'vip_type': 'mining_machine'},
        72: {'title': '☀️ Solar Core', 'description': 'Солнечное ядро энергии VIP', 'stars': 100, 'coins': 0, 'vip_type': 'mining_machine'},
        73: {'title': '🕳️ Black Hole', 'description': 'Чёрная дыра энергии VIP', 'stars': 150, 'coins': 0, 'vip_type': 'mining_machine'},
        74: {'title': '🌫️ Nebula Ферма', 'description': 'Ферма в туманности VIP', 'stars': 250, 'coins': 0, 'vip_type': 'mining_machine'},
        75: {'title': '🌐 Multiverse Станция', 'description': 'Мультивселенная VIP', 'stars': 400, 'coins': 0, 'vip_type': 'mining_machine'},
        76: {'title': '♾️ Infinity Альянс', 'description': 'Бесконечный альянс VIP', 'stars': 750, 'coins': 0, 'vip_type': 'mining_machine'},
        # VIP FUNCTIONS for VIP Shop modal (81-100)
        81: {'title': '🌠 Звездный Шторм', 'description': 'VIP бустер, увеличивающий майнинг на +25 коин за тап. Использует энергию звездных вспышек для сверхмощного майнинга.', 'stars': 100, 'coins': 0, 'vip_type': 'tap_boost'},
        82: {'title': '🌑 Черная Дыра', 'description': 'Эксклюзивный бустер, дающий +35 коин за тап. Поглощает энергию пространства-времени для невероятной производительности.', 'stars': 200, 'coins': 0, 'vip_type': 'tap_boost'},
        83: {'title': '✨ Абсолют', 'description': 'Легендарный VIP бустер, увеличивающий майнинг на +50 коин за тап. Абсолютная власть над криптовалютными алгоритмами.', 'stars': 350, 'coins': 0, 'vip_type': 'tap_boost'},
        84: {'title': '👑 Имперский', 'description': 'Императорский бустер, дающий +70 коин за тап. Технология, достойная крипто-императоров и блокчейн-королей.', 'stars': 500, 'coins': 0, 'vip_type': 'tap_boost'},
        85: {'title': '🌟 Легендарный', 'description': 'Мифический VIP бустер, увеличивающий майнинг на +100 коин за тап. Легендарная технология из древних крипто-цивилизаций.', 'stars': 750, 'coins': 0, 'vip_type': 'tap_boost'},
        86: {'title': '☀️ Солнечная Корона', 'description': 'VIP генератор, восстанавливающий +1.5 энергии в секунду. Использует энергию солнечной короны для сверхбыстрой подзарядки.', 'stars': 120, 'coins': 0, 'vip_type': 'energy_buy'},
        87: {'title': '🌌 Галактический Ядро', 'description': 'Эксклюзивный генератор, дающий +2.25 энергии в секунду. Извлекает энергию из ядра галактики через квантовые туннели.', 'stars': 200, 'coins': 0, 'vip_type': 'energy_buy'},
        88: {'title': '💫 Новая Ера', 'description': 'Революционный генератор, восстанавливающий +3.0 энергии в секунду. Технология новой эры криптовалютного будущего.', 'stars': 300, 'coins': 0, 'vip_type': 'energy_buy'},
        89: {'title': '⚛️ Квантовый Реактор', 'description': 'Легендарный генератор, дающий +4.0 энергии в секунду. Использует квантовые флуктуации для неограниченной энергии.', 'stars': 450, 'coins': 0, 'vip_type': 'energy_buy'},
        90: {'title': '🌠 Небесный Портал', 'description': 'Мифический генератор, восстанавливающий +5.0 энергии в секунду. Подключается к энергетическим порталам небесных сфер.', 'stars': 600, 'coins': 0, 'vip_type': 'energy_buy'},
        91: {'title': '🌌 Галактический Резервуар', 'description': 'VIP накопитель, увеличивающий максимум энергии на +3750. Хранит энергию целой галактики в компактном кристалле.', 'stars': 150, 'coins': 0, 'vip_type': 'energy_expand'},
        92: {'title': '⚛️ Квантовая Суперпозиция', 'description': 'Эксклюзивный накопитель, расширяющий энергоемкость на +6250. Использует квантовую суперпозицию для бесконечного хранения.', 'stars': 250, 'coins': 0, 'vip_type': 'energy_expand'},
        93: {'title': '🌠 Звездное Созвездие', 'description': 'Легендарный накопитель, увеличивающий максимум энергии на +10000. Содержит энергию целого звездного созвездия.', 'stars': 400, 'coins': 0, 'vip_type': 'energy_expand'},
        94: {'title': '🌑 Абсолютная Пустота', 'description': 'Мифический накопитель, расширяющий энергоемкость на +18750. Использует энергию космической пустоты для хранения.', 'stars': 600, 'coins': 0, 'vip_type': 'energy_expand'},
        95: {'title': '👑 Имперская Сокровищница', 'description': 'Божественный накопитель, увеличивающий максимум энергии на +37500. Сокровищница крипто-императоров с неограниченной емкостью.', 'stars': 800, 'coins': 0, 'vip_type': 'energy_expand'},
        96: {'title': '⭐ VIP Базовый Бот', 'description': 'VIP автотап на 4 часа', 'stars': 100, 'coins': 0, 'vip_type': 'autobot'},
        97: {'title': '⭐ VIP Улучшенный Бот', 'description': 'VIP автотап на 12 часов', 'stars': 200, 'coins': 0, 'vip_type': 'autobot'},
        98: {'title': '⭐ VIP Продвинутый Бот', 'description': 'VIP автотап на 2 дня', 'stars': 350, 'coins': 0, 'vip_type': 'autobot'},
        99: {'title': '⭐ VIP Элитный Бот', 'description': 'VIP автотап на 5 дней', 'stars': 500, 'coins': 0, 'vip_type': 'autobot'},
        100: {'title': '⭐ VIP Премиум Бот', 'description': 'VIP автотап на 10 дней', 'stars': 750, 'coins': 0, 'vip_type': 'autobot'},
        # VIP CARDS for VIP Shop (101-116)
        101: {'title': '⭐ VIP Silver', 'description': 'VIP карта: +300 🪙/час', 'stars': 100, 'coins': 0, 'vip_type': 'vip_card'},
        102: {'title': '💎 VIP Gold', 'description': 'VIP карта: +800 🪙/час', 'stars': 250, 'coins': 0, 'vip_type': 'vip_card'},
        103: {'title': '👑 VIP Platinum', 'description': 'VIP карта: +1,800 🪙/час', 'stars': 500, 'coins': 0, 'vip_type': 'vip_card'},
        104: {'title': '💍 VIP Diamond', 'description': 'VIP карта: +4,000 🪙/час', 'stars': 1000, 'coins': 0, 'vip_type': 'vip_card'},
        105: {'title': '🌟 VIP Elite', 'description': 'VIP карта: +9,000 🪙/час', 'stars': 2500, 'coins': 0, 'vip_type': 'vip_card'},
        106: {'title': '⚡ VIP Ultimate', 'description': 'VIP карта: +20,000 🪙/час', 'stars': 5000, 'coins': 0, 'vip_type': 'vip_card'},
        111: {'title': '✨ VIP Nova', 'description': 'VIP карта: +15 🪙/мин', 'stars': 500, 'coins': 0, 'vip_type': 'vip_card'},
        112: {'title': '⚡ VIP Quantum', 'description': 'VIP карта: +50 🪙/мин', 'stars': 1250, 'coins': 0, 'vip_type': 'vip_card'},
        113: {'title': '🔥 VIP Cosmic', 'description': 'VIP карта: +150 🪙/мин', 'stars': 2500, 'coins': 0, 'vip_type': 'vip_card'},
        114: {'title': '🎆 VIP Stellar', 'description': 'VIP карта: +350 🪙/мин', 'stars': 5000, 'coins': 0, 'vip_type': 'vip_card'},
        115: {'title': '🌌 VIP Galaxy', 'description': 'VIP карта: +600 🪙/мин', 'stars': 10000, 'coins': 0, 'vip_type': 'vip_card'},
        116: {'title': '🌠 VIP Infinity', 'description': 'VIP карта: +1,000 🪙/мин', 'stars': 20000, 'coins': 0, 'vip_type': 'vip_card'}
    }
    
    product = products.get(product_id)
    if not product:
        logger.error(f"Invalid product_id: {product_id}")
        await update.message.reply_text("❌ Неверный товар")
        return
    
    logger.info(f"Product found: {product}")
    
    user_id = update.effective_user.id
    logger.info(f"User ID: {user_id}")
    
    try:
        with get_db() as db:
            user = db.query(User).filter_by(telegram_id=user_id).first()
            
            if not user:
                logger.error(f"User {user_id} not found in database")
                await update.message.reply_text("❌ Пользователь не найден")
                return
            
            logger.info(f"User found: {user.username}, DB ID: {user.id}")
            
            # Calculate dynamic price for VIP mining machines based on current level
            final_stars_amount = product['stars']
            if product_id >= 71 and product_id <= 76:
                # VIP Mining Machines - calculate price based on current level
                vip_mining_map = {
                    71: 'vip_quantum_prime',
                    72: 'vip_solar_core',
                    73: 'vip_black_hole',
                    74: 'vip_nebula',
                    75: 'vip_multiverse',
                    76: 'vip_infinity'
                }
                machine_id = vip_mining_map.get(product_id)
                if machine_id:
                    import json
                    vip_levels = json.loads(user.mining_vip_levels or '{}')
                    current_level = vip_levels.get(machine_id, 0)
                    
                    # Calculate price using same formula as frontend: basePrice * (1.15 ^ level)
                    base_price = product['stars']
                    final_stars_amount = int(base_price * (1.15 ** current_level))
                    logger.info(f"VIP Mining Machine {machine_id}: level {current_level}, base price {base_price}, final price {final_stars_amount}")
            
            # Send invoice with Telegram Stars
            prices = [LabeledPrice(
                label=f"{product['title']} - {product['description']}",
                amount=final_stars_amount
            )]
            
            logger.info(f"Creating invoice with title: {product['title']}")
            logger.info(f"Stars amount: {final_stars_amount}")
            logger.info(f"Chat ID: {update.effective_chat.id}")
            
            # For Telegram Stars, set provider_token to None
            invoice_result = await context.bot.send_invoice(
                chat_id=update.effective_chat.id,
                title=product['title'],
                description=product['description'],
                payload=f"stars_{user.id}_{product_id}",
                provider_token=None,  # None for Stars (not empty string!)
                currency="XTR",
                prices=prices,
                start_parameter=f"buy_stars_{product_id}"  # Add start parameter
            )
            
            logger.info(f"✅ Invoice sent successfully! Message ID: {invoice_result.message_id}")
            # Invoice is displayed by Telegram automatically, no extra message needed
            return  # Exit function without sending extra message
            
    except Exception as e:
        logger.error(f"❌ Failed to send Stars invoice: {e}", exc_info=True)
        
        # If Stars are not available, show alternative
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            f"💡 Telegram Stars недоступны в вашем регионе.\n\n"
            f"📦 Telegram Stars работают только в:\n"
            f"   • США\n"
            f"   • Япония\n"
            f"   • Южная Корея\n"
            f"   • И другие (обновляется)"
        )
