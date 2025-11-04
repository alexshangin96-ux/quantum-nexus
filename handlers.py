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
            # Create new user
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                referral_code=generate_referral_code(),
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
                    db_user.coins += REFERRAL_BONUS
                    referrer.coins += REFERRAL_BONUS // 2
                    logger.info(f"User {db_user.telegram_id} was referred by {referrer.telegram_id}")
        
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
            InlineKeyboardButton("🎮 Открыть игру", web_app=WebAppInfo(url="https://quantum-nexus.ru/web_app.html?v=4.0&t=" + str(int(__import__('time').time()))))
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
        product_coins = {
            1: 200000, 2: 500000, 3: 800000, 4: 1000000, 5: 1500000, 6: 2000000, 7: 2500000, 8: 3000000, 9: 3500000, 10: 4000000,
            11: 1500000, 12: 3000000, 13: 4500000, 14: 6000000, 15: 7500000, 16: 9000000, 17: 10500000, 18: 12000000, 19: 13500000, 20: 15000000,
            21: 5000000, 22: 8000000, 23: 12000000, 24: 16000000, 25: 20000000, 26: 25000000, 27: 30000000, 28: 35000000, 29: 40000000, 30: 45000000,
            31: 12000000, 32: 15000000, 33: 18000000, 34: 21000000, 35: 24000000, 36: 27000000, 37: 30000000, 38: 33000000, 39: 36000000, 40: 40000000,
            41: 25000000, 42: 35000000, 43: 45000000, 44: 55000000, 45: 65000000, 46: 75000000, 47: 85000000, 48: 95000000, 49: 105000000, 50: 120000000,
            51: 50000000, 52: 100000000, 53: 150000000, 54: 200000000, 55: 250000000, 56: 300000000, 57: 350000000, 58: 400000000, 59: 450000000, 60: 500000000
        }
        
        # Define VIP products (21-40) with special effects
        vip_products = {
            21: {'type': 'tap_boost', 'effect': 51, 'name': 'Звездный Шторм'},
            22: {'type': 'tap_boost', 'effect': 71, 'name': 'Черная Дыра'},
            23: {'type': 'tap_boost', 'effect': 101, 'name': 'Абсолют'},
            24: {'type': 'tap_boost', 'effect': 141, 'name': 'Имперский'},
            25: {'type': 'tap_boost', 'effect': 201, 'name': 'Легендарный'},
            26: {'type': 'energy_buy', 'effect': 3.0, 'name': 'Солнечная Корона'},
            27: {'type': 'energy_buy', 'effect': 4.5, 'name': 'Галактический Ядро'},
            28: {'type': 'energy_buy', 'effect': 6.0, 'name': 'Новая Ера'},
            29: {'type': 'energy_buy', 'effect': 8.0, 'name': 'Квантовый Реактор'},
            30: {'type': 'energy_buy', 'effect': 10.0, 'name': 'Небесный Портал'},
            31: {'type': 'energy_expand', 'effect': 7500, 'name': 'Галактический Резервуар'},
            32: {'type': 'energy_expand', 'effect': 12500, 'name': 'Квантовая Суперпозиция'},
            33: {'type': 'energy_expand', 'effect': 20000, 'name': 'Звездное Созвездие'},
            34: {'type': 'energy_expand', 'effect': 37500, 'name': 'Абсолютная Пустота'},
            35: {'type': 'energy_expand', 'effect': 75000, 'name': 'Имперская Сокровищница'},
            36: {'type': 'autobot', 'effect': 6, 'name': 'Океанский Майнер', 'duration': 7200},
            37: {'type': 'autobot', 'effect': 6.5, 'name': 'Квантовый Процессор', 'duration': 10080},
            38: {'type': 'autobot', 'effect': 7, 'name': 'Небесный Сервер', 'duration': 14400},
            39: {'type': 'autobot', 'effect': 7.5, 'name': 'Вулканический Реактор', 'duration': 20160},
            40: {'type': 'autobot', 'effect': 8, 'name': 'Звездная Власть', 'duration': 28800}
        }
        
        with get_db() as db:
            user = db.query(User).filter_by(id=user_db_id, telegram_id=user_id).first()
            
            if not user:
                logger.error(f"User not found: {user_db_id}/{user_id}")
                await update.message.reply_text("❌ Ошибка: пользователь не найден")
                return
            
            # Handle VIP products (21-30)
            vip_message = ""
            if product_id in vip_products:
                vip_info = vip_products[product_id]
                
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
            elif product_id >= 41 and product_id <= 50:
                # Handle COMBO products (41-50): cards + coins
                combo_products = {
                    41: {'cards': 10, 'coins': 25000000},
                    42: {'cards': 20, 'coins': 35000000},
                    43: {'cards': 50, 'coins': 45000000},
                    44: {'cards': 100, 'coins': 55000000},
                    45: {'cards': 200, 'coins': 65000000},
                    46: {'cards': 500, 'coins': 75000000},
                    47: {'cards': 1000, 'coins': 85000000},
                    48: {'cards': 2000, 'coins': 95000000},
                    49: {'cards': 5000, 'coins': 105000000},
                    50: {'cards': 10000, 'coins': 15000000}  # Special: АБСОЛЮТ ВСЁ
                }
                
                combo_info = combo_products.get(product_id)
                if not combo_info:
                    logger.error(f"Unknown combo product: {product_id}")
                    await update.message.reply_text("❌ Ошибка: неизвестный комбо-товар")
                    return
                
                # Add coins
                user.coins += combo_info['coins']
                
                # Add cards as UserCard objects
                import random
                cards_added = 0
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
                    cards_added += 1
                
                # Flush to ensure cards are added before commit
                db.flush()
                
                # Verify cards were added
                cards_count_after = db.query(UserCard).filter_by(user_id=user.id).count()
                logger.info(f"Cards added: {cards_added}, total cards for user {user.id}: {cards_count_after}")
                
                vip_message = f"\n\n🎴 Получено: {combo_info['cards']:,} карточек\n💰 Получено: {combo_info['coins']:,} коинов"
            else:
                # Handle regular coin products (1-20, 31-40, 51-60)
                coins_to_add = product_coins.get(product_id, 0)
                if coins_to_add == 0:
                    logger.error(f"Unknown product: {product_id}")
                    await update.message.reply_text("❌ Ошибка: неизвестный товар")
                    return
                
                user.coins += coins_to_add
                vip_message = f"\n\n💰 Получено: {coins_to_add:,} коинов"
            
            db.commit()
            
            # Log successful payment
            if product_id in vip_products:
                logger.info(f"✅ VIP Stars payment successful! User {user_id} bought VIP product {product_id}: {vip_products[product_id]['name']}")
                await update.message.reply_text(
                    f"✨ VIP Покупка успешна!\n\n"
                    f"💎 Оплачено: {payment.total_amount} ⭐\n"
                    f"📊 Новый баланс: {user.coins:,} коинов"
                    + vip_message
                )
            elif product_id >= 41 and product_id <= 50:
                combo_info = combo_products.get(product_id)
                logger.info(f"✅ COMBO Stars payment successful! User {user_id} bought product {product_id}: {combo_info['cards']} cards + {combo_info['coins']} coins")
                await update.message.reply_text(
                    f"✨ Комбо покупка успешна!\n\n"
                    f"💎 Оплачено: {payment.total_amount} ⭐\n"
                    f"📊 Новый баланс: {user.coins:,} коинов"
                    + vip_message
                )
            else:
                coins_to_add = product_coins.get(product_id, 0)
                logger.info(f"✅ Stars payment successful! User {user_id} bought product {product_id} for {coins_to_add} coins")
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
    
    # Define products with Stars prices - 60 items
    products = {
        # STARTING (1-10)
        1: {'title': '💫 Первые шаги', 'description': '200,000 коинов', 'stars': 50, 'coins': 200000},
        2: {'title': '✨ Базовый', 'description': '500,000 коинов', 'stars': 120, 'coins': 500000},
        3: {'title': '🌟 Начало пути', 'description': '800,000 коинов', 'stars': 180, 'coins': 800000},
        4: {'title': '💎 Приветственный', 'description': '1,000,000 коинов', 'stars': 240, 'coins': 1000000},
        5: {'title': '🎁 Добро пожаловать', 'description': '1,500,000 коинов', 'stars': 320, 'coins': 1500000},
        6: {'title': '💰 Стартовый', 'description': '2,000,000 коинов', 'stars': 400, 'coins': 2000000},
        7: {'title': '⚡ Быстрый старт', 'description': '2,500,000 коинов', 'stars': 480, 'coins': 2500000},
        8: {'title': '🎯 Первый шаг', 'description': '3,000,000 коинов', 'stars': 560, 'coins': 3000000},
        9: {'title': '🌈 Радуга', 'description': '3,500,000 коинов', 'stars': 640, 'coins': 3500000},
        10: {'title': '💫 Волшебный', 'description': '4,000,000 коинов', 'stars': 720, 'coins': 4000000},
        # PREMIUM (11-20)
        11: {'title': '⚡ Световой', 'description': '1,500,000 коинов', 'stars': 300, 'coins': 1500000},
        12: {'title': '🎯 Профессионал', 'description': '3,000,000 коинов', 'stars': 600, 'coins': 3000000},
        13: {'title': '🚀 Мощь', 'description': '4,500,000 коинов', 'stars': 900, 'coins': 4500000},
        14: {'title': '💎 Алмазный', 'description': '6,000,000 коинов', 'stars': 1200, 'coins': 6000000},
        15: {'title': '🔥 Огненный', 'description': '7,500,000 коинов', 'stars': 1500, 'coins': 7500000},
        16: {'title': '⚡ Электронный', 'description': '9,000,000 коинов', 'stars': 1800, 'coins': 9000000},
        17: {'title': '🌟 Звёздный', 'description': '10,500,000 коинов', 'stars': 2100, 'coins': 10500000},
        18: {'title': '💫 Космический', 'description': '12,000,000 коинов', 'stars': 2400, 'coins': 12000000},
        19: {'title': '🎁 Подарочный VIP', 'description': '13,500,000 коинов', 'stars': 2700, 'coins': 13500000},
        20: {'title': '🔮 Магический', 'description': '15,000,000 коинов', 'stars': 3000, 'coins': 15000000},
        # VIP → PREMIUM FUNCTIONS (21-30)
        21: {'title': '🌠 Звездный Шторм', 'description': 'VIP бустер, увеличивающий майнинг на +51 коин за тап. Использует энергию звездных вспышек для сверхмощного майнинга.', 'stars': 100, 'coins': 0},
        22: {'title': '🌑 Черная Дыра', 'description': 'Эксклюзивный бустер, дающий +71 коин за тап. Поглощает энергию пространства-времени для невероятной производительности.', 'stars': 200, 'coins': 0},
        23: {'title': '✨ Абсолют', 'description': 'Легендарный VIP бустер, увеличивающий майнинг на +101 коин за тап. Абсолютная власть над криптовалютными алгоритмами.', 'stars': 350, 'coins': 0},
        24: {'title': '👑 Имперский', 'description': 'Императорский бустер, дающий +141 коин за тап. Технология, достойная крипто-императоров и блокчейн-королей.', 'stars': 500, 'coins': 0},
        25: {'title': '🌟 Легендарный', 'description': 'Мифический VIP бустер, увеличивающий майнинг на +201 коин за тап. Легендарная технология из древних крипто-цивилизаций.', 'stars': 750, 'coins': 0},
        26: {'title': '☀️ Солнечная Корона', 'description': 'VIP генератор, восстанавливающий +3.0 энергии в секунду. Использует энергию солнечной короны для сверхбыстрой подзарядки.', 'stars': 120, 'coins': 0},
        27: {'title': '🌌 Галактический Ядро', 'description': 'Эксклюзивный генератор, дающий +4.5 энергии в секунду. Извлекает энергию из ядра галактики через квантовые туннели.', 'stars': 200, 'coins': 0},
        28: {'title': '💫 Новая Ера', 'description': 'Революционный генератор, восстанавливающий +6.0 энергии в секунду. Технология новой эры криптовалютного будущего.', 'stars': 300, 'coins': 0},
        29: {'title': '⚛️ Квантовый Реактор', 'description': 'Легендарный генератор, дающий +8.0 энергии в секунду. Использует квантовые флуктуации для неограниченной энергии.', 'stars': 450, 'coins': 0},
        30: {'title': '🌠 Небесный Портал', 'description': 'Мифический генератор, восстанавливающий +10.0 энергии в секунду. Подключается к энергетическим порталам небесных сфер.', 'stars': 600, 'coins': 0},
        # VIP ENERGY EXPAND (31-35)
        31: {'title': '🌌 Галактический Резервуар', 'description': 'VIP накопитель, увеличивающий максимум энергии на +7500. Хранит энергию целой галактики в компактном кристалле.', 'stars': 150, 'coins': 0},
        32: {'title': '⚛️ Квантовая Суперпозиция', 'description': 'Эксклюзивный накопитель, расширяющий энергоемкость на +12500. Использует квантовую суперпозицию для бесконечного хранения.', 'stars': 250, 'coins': 0},
        33: {'title': '🌠 Звездное Созвездие', 'description': 'Легендарный накопитель, увеличивающий максимум энергии на +20000. Содержит энергию целого звездного созвездия.', 'stars': 400, 'coins': 0},
        34: {'title': '🌑 Абсолютная Пустота', 'description': 'Мифический накопитель, расширяющий энергоемкость на +37500. Использует энергию космической пустоты для хранения.', 'stars': 600, 'coins': 0},
        35: {'title': '👑 Имперская Сокровищница', 'description': 'Божественный накопитель, увеличивающий максимум энергии на +75000. Сокровищница крипто-императоров с неограниченной емкостью.', 'stars': 800, 'coins': 0},
        # VIP AUTOBOTS (36-40)
        36: {'title': '🌊 Океанский Майнер', 'description': 'VIP майнинг-бот на 5 дней со скоростью 6 тапов/сек. Использует энергию океанских течений для непрерывного майнинга.', 'stars': 100, 'coins': 0},
        37: {'title': '⚛️ Квантовый Процессор', 'description': 'Эксклюзивный бот на 7 дней со скоростью 6.5 тапов/сек. Использует квантовые вычисления для максимальной эффективности.', 'stars': 200, 'coins': 0},
        38: {'title': '🌠 Небесный Сервер', 'description': 'Легендарный бот на 10 дней со скоростью 7 тапов/сек. Орбитальный сервер, добывающий криптовалюту в космосе.', 'stars': 350, 'coins': 0},
        39: {'title': '🌋 Вулканический Реактор', 'description': 'Мифический бот на 14 дней со скоростью 7.5 тапов/сек. Использует энергию вулканической магмы для сверхмощного майнинга.', 'stars': 500, 'coins': 0},
        40: {'title': '🌟 Звездная Власть', 'description': 'Божественный бот на 20 дней со скоростью 8 тапов/сек. Власть над звездами для добычи криптовалюты космического уровня.', 'stars': 750, 'coins': 0},
        # ULTRA → COMBO SETS (41-50)
        41: {'title': '🎁 Стартовый мегасет', 'description': '10 карточек + 1M коинов', 'stars': 5000, 'coins': 25000000},
        42: {'title': '🔥 Горячий комбо', 'description': '20 карточек + 10M коинов', 'stars': 7000, 'coins': 35000000},
        43: {'title': '💎 Элитный набор', 'description': '50 карточек + 50M коинов', 'stars': 9000, 'coins': 45000000},
        44: {'title': '🚀 Мега связка', 'description': '100 карточек + 100M коинов', 'stars': 11000, 'coins': 55000000},
        45: {'title': '🌟 Легендарный мегасет', 'description': '200 карточек + 200M', 'stars': 13000, 'coins': 65000000},
        46: {'title': '💎 Бриллиантовая связка', 'description': 'VIP карты + безлимит', 'stars': 15000, 'coins': 75000000},
        47: {'title': '👑 Королевский комбо', 'description': '300 карт + VIP доступ', 'stars': 17000, 'coins': 85000000},
        48: {'title': '🔥 Огненный мегасет', 'description': '500 карт + 500M', 'stars': 19000, 'coins': 95000000},
        49: {'title': '💫 Космический комбо', 'description': '1000 карт + всё VIP', 'stars': 21000, 'coins': 105000000},
        50: {'title': '🎯 АБСОЛЮТ ВСЁ', 'description': 'ВСЁ что есть в игре!', 'stars': 24000, 'coins': 120000000},
        # VIP STATUSES (51-60)
        51: {'title': '🥉 Bronze VIP', 'description': '✅ Premium Support, Уникальный маркер, +20% к тапу', 'stars': 300, 'coins': 2000000},
        52: {'title': '🥈 Silver VIP', 'description': '✅ Premium Support, Уникальный маркер, Top Place, +50% к тапу', 'stars': 600, 'coins': 5000000},
        53: {'title': '🥇 Gold VIP', 'description': '✅ Premium Support, Golden Profile, Top Place, Unique Design, +100% к тапу, -50% энергии', 'stars': 1000, 'coins': 10000000},
        54: {'title': '💎 Platinum VIP', 'description': '✅ Все из Gold VIP, VIP Турниры, Частицы, +150% к тапу', 'stars': 1500, 'coins': 20000000},
        55: {'title': '💠 Diamond VIP', 'description': '✅ Все из Platinum VIP, Корона, 0% комиссия, +250% к тапу, VIP Boost 50x', 'stars': 2000, 'coins': 50000000},
        56: {'title': '👑 Absolute VIP', 'description': '✅ Все из Diamond VIP, Аура, Радуга, +450% к тапу, VIP Машины', 'stars': 3000, 'coins': 100000000},
        57: {'title': '⭐ Пульсар', 'description': '350,000,000 коинов', 'stars': 70000, 'coins': 350000000},
        58: {'title': '🌌 Квазар', 'description': '400,000,000 коинов', 'stars': 80000, 'coins': 400000000},
        59: {'title': '🌟 Чёрная дыра', 'description': '450,000,000 коинов', 'stars': 90000, 'coins': 450000000},
        60: {'title': '⭐ Большой взрыв', 'description': '500,000,000 коинов', 'stars': 100000, 'coins': 500000000}
    }
    
    product = products.get(product_id)
    if not product:
        logger.error(f"Invalid product_id: {product_id}")
        await update.message.reply_text("❌ Неверный товар")
        return
    
    logger.info(f"Product found: {product}")
    
    user_id = update.effective_user.id
    logger.info(f"User ID: {user_id}")
    
    with get_db() as db:
        user = db.query(User).filter_by(telegram_id=user_id).first()
        
        if not user:
            logger.error(f"User {user_id} not found in database")
            await update.message.reply_text("❌ Пользователь не найден")
            return
        
        logger.info(f"User found: {user.username}, DB ID: {user.id}")
        
        try:
            # Send invoice with Telegram Stars
            prices = [LabeledPrice(
                label=f"{product['title']} - {product['description']}",
                amount=product['stars']
            )]
            
            logger.info(f"Creating invoice with title: {product['title']}")
            logger.info(f"Stars amount: {product['stars']}")
            logger.info(f"Chat ID: {update.effective_chat.id}")
            
            # For Telegram Stars, set provider_token to None
            invoice_result = await context.bot.send_invoice(
                chat_id=update.effective_chat.id,
                title=f"💎 {product['title']}",
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


async def channel_subscription_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle channel subscription/unsubscription events for daily tasks"""
    try:
        logger.info(f"Channel subscription handler called: update={update}")
        
        # Check if update has chat_member
        if not update.chat_member:
            logger.warning("Channel subscription handler: no chat_member in update")
            return
            
        # Only handle updates for quantum_nexus channel
        chat = update.chat_member.chat
        logger.info(f"Channel subscription handler: chat={chat}, chat.id={chat.id}, chat.username={getattr(chat, 'username', None)}")
        
        # Check both username and ID for quantum_nexus channel
        channel_username = getattr(chat, 'username', None)
        channel_id = getattr(chat, 'id', None)
        
        # Accept if username matches OR if we need to check by ID
        # Note: For now, accept all channel updates to debug
        if channel_username and channel_username != 'quantum_nexus':
            logger.warning(f"Channel subscription handler: wrong channel username: {channel_username}, skipping")
            return
        
        user = update.chat_member.from_user
        old_status = update.chat_member.old_chat_member.status
        new_status = update.chat_member.new_chat_member.status
        
        # Check if user unsubscribed
        was_member = old_status in ['member', 'administrator', 'creator']
        is_now_member = new_status in ['member', 'administrator', 'creator']
        
        with get_db() as db:
            db_user = db.query(User).filter_by(telegram_id=user.id).first()
            
            if db_user:
                if was_member and not is_now_member:
                    # User unsubscribed - apply penalty ALWAYS
                    logger.info(f"User {user.id} unsubscribed: was_member={was_member}, is_now_member={is_now_member}")
                    penalty = 10000
                    old_coins = db_user.coins
                    db_user.coins = max(0, db_user.coins - penalty)  # Can't go below 0
                    db_user.channel_subscribed = False
                    db_user.channel_subscribed_at = None
                    
                    # Reset task 1 (channel subscription) in daily_tasks_completed
                    import json
                    try:
                        daily_completed = json.loads(db_user.daily_tasks_completed or '{}')
                        logger.info(f"Before reset: daily_tasks_completed={daily_completed}")
                        if '1' in daily_completed or 1 in daily_completed:
                            daily_completed = {k: v for k, v in daily_completed.items() if str(k) != '1' and k != 1}
                            db_user.daily_tasks_completed = json.dumps(daily_completed)
                            logger.info(f"After reset: daily_tasks_completed={daily_completed}")
                    except Exception as e:
                        logger.error(f"Error resetting daily_tasks_completed: {e}")
                    
                    db.commit()
                    logger.info(f"Penalty applied: user {user.id}, coins {old_coins} -> {db_user.coins}")
                    
                    # Notify user about penalty immediately
                    try:
                        bot = context.bot
                        notification = (
                            f"⚠️ Штраф за отписку от канала!\n\n"
                            f"❌ Вы отписались от канала @quantum_nexus\n"
                            f"💸 Штраф: -{penalty:,} коинов\n\n"
                            f"📢 Подпишитесь снова, чтобы вернуть задание!"
                        )
                        await bot.send_message(chat_id=user.id, text=notification)
                        logger.info(f"Notification sent to user {user.id}")
                    except Exception as e:
                        logger.error(f"Error sending notification to user {user.id}: {e}")
                elif not was_member and is_now_member:
                    # User subscribed - update status
                    if not db_user.channel_subscribed:
                        db_user.channel_subscribed = True
                        db_user.channel_subscribed_at = datetime.utcnow()
                        db.commit()
                        logger.info(f"User {user.id} subscribed to channel")
                        
    except Exception as e:
        logger.error(f"Channel subscription handler error: {e}", exc_info=True)
