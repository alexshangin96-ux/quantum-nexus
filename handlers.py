from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from models import User, MiningMachine, UserCard, Transaction
from keyboards import *
from utils import *
from database import get_db, generate_referral_code
from config import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    db = next(get_db())
    
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
        db.commit()
        
        # Check for referral
        if context.args and context.args[0]:
            referral_code = context.args[0]
            referrer = db.query(User).filter_by(referral_code=referral_code).first()
            if referrer and referrer.id != db_user.id:
                db_user.referred_by = referrer.id
                referrer.referrals_count += 1
                db_user.coins += REFERRAL_BONUS
                referrer.coins += REFERRAL_BONUS // 2
                db.commit()
    
    # Calculate offline income
    offline_income = calculate_offline_income(db_user)
    if offline_income > 0:
        db_user.coins += offline_income
        db_user.total_earned += offline_income
        transaction = Transaction(
            user_id=db_user.id,
            transaction_type="offline_income",
            amount=offline_income,
            currency="coins"
        )
        db.add(transaction)
    
    db_user.last_active = datetime.utcnow()
    db.commit()
    
    message = f"""
🌟 <b>Добро пожаловать в Quantum Nexus!</b> 🌟

👤 <b>Профиль:</b>
💰 Коины: {format_currency(db_user.coins)} 🪙
💎 QuanHash: {format_currency(db_user.quanhash)} ⚡
⚡ Энергия: {db_user.energy}/{db_user.max_energy}

📊 <b>Статистика:</b>
👆 Всего тапов: {db_user.total_taps}
💵 Всего заработано: {format_currency(db_user.total_earned)} 🪙

🆔 Реферальный код: <code>{db_user.referral_code}</code>
👥 Рефералов: {db_user.referrals_count}

Выберите действие:
    """
    
    if offline_income > 0:
        message += f"\n💰 Оффлайн доход: {format_currency(offline_income)} 🪙"
    
    # Create keyboard with Web App button
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Открыть игру", web_app=WebAppInfo(url="https://quantum-nexus.ru/web_app.html"))
        ]
    ]
    
    main_keyboard = get_main_menu().inline_keyboard
    for row in main_keyboard:
        keyboard.append(row)
    
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
