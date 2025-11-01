from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
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
    logger.info(f"Processing /start for user {user.id}")
    
    with get_db() as db:
        # Check if user exists
        db_user = db.query(User).filter_by(telegram_id=user.id).first()
        
        if not db_user:
            # Create new user
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                referral_code=generate_referral_code(),
                sound_enabled=True,  # Default: sounds enabled
            )
            db.add(db_user)
            db.flush()  # Get the ID
            
            # Check for referral
            if context.args and context.args[0]:
                arg = context.args[0]
                
                # Check for referral
                referral_value = arg
                referrer = None
                
                # First try to find by telegram_id
                try:
                    referral_telegram_id = int(referral_value)
                    referrer = db.query(User).filter_by(telegram_id=referral_telegram_id).first()
                except ValueError:
                    # Try by referral_code if it's not a number
                    referrer = db.query(User).filter_by(referral_code=referral_value).first()
                
                if referrer and referrer.id != db_user.id:
                    db_user.referred_by = referrer.id
                    referrer.referrals_count += 1
                    
                    # Check if user has Telegram Premium (VIP)
                    # Premium users get bigger bonus
                    # Get premium status from Telegram user object
                    user_has_premium = getattr(user, 'is_premium', False) if hasattr(user, 'is_premium') else False
                    
                    if user_has_premium:
                        # VIP/Premium user bonus: 2000 coins
                        REFERRAL_BONUS_NEW = 2000
                        REFERRAL_BONUS_REFERRER = 500  # Referrer gets 500 coins bonus
                    else:
                        # Regular user bonus: 500 coins
                        REFERRAL_BONUS_NEW = 500
                        REFERRAL_BONUS_REFERRER = 250  # Referrer gets 250 coins bonus
                    
                    db_user.coins += REFERRAL_BONUS_NEW
                    referrer.coins += REFERRAL_BONUS_REFERRER
                    
                    logger.info(f"User {db_user.telegram_id} was referred by {referrer.telegram_id}. Bonus: {REFERRAL_BONUS_NEW} (premium: {user_has_premium})")
        
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
        db.commit()
    
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
            InlineKeyboardButton("🎮 Открыть игру", web_app=WebAppInfo(url="https://quantum-nexus.ru/game_v4.html?" + str(int(time.time()))))
        ],
        [
            InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
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
        await show_main_menu(query, db_user, db)
    elif data == "profile":
        await show_profile(query, db_user, db)
    elif data == "toggle_sound":
        await toggle_sound(query, db_user, db)
    elif data.startswith("test_sound_"):
        await test_sound(query, data, db_user, db)
    elif data == "tap":
        await handle_tap(query, db_user, db)
    elif data == "energy_status":
        await show_energy_status(query, db_user, db)
    elif data == "mining":
        await show_mining(query, db_user, db)
    elif data == "cards":
        await show_user_cards(query, db_user, db)
    elif data == "shop":
        await show_shop(query, db_user, db)
    elif data == "stats":
        await show_stats(query, db_user, db)
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
    elif data.startswith("toggle_"):
        await handle_toggle(query, data, db_user, db)


async def handle_purchase(query, data, user, db):
    """Handle purchases"""
    from utils import play_sound
    
    # Play purchase sound for all purchases
    if data.startswith("buy_"):
        play_sound(user, "purchase")
    
    if data == "buy_energy_50":
        price = 1000
        if user.coins >= price:
            user.coins -= price
            user.energy = min(user.energy + 50, user.max_energy)
            db.commit()
            await query.answer("✅ Энергия куплена!")
            await show_shop(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    # Buy boosts
    elif data == "buy_boost_multiplier_2x":
        price = BOOST_PRICES["multiplier_2x"]
        if user.coins >= price:
            user.coins -= price
            user.active_multiplier = 2.0
            user.multiplier_expires_at = datetime.utcnow() + timedelta(hours=1)
            db.commit()
            await query.answer("✅ Множитель x2 активирован на 1 час!")
            await show_shop(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    elif data == "buy_boost_multiplier_5x":
        price = BOOST_PRICES["multiplier_5x"]
        if user.coins >= price:
            user.coins -= price
            user.active_multiplier = 5.0
            user.multiplier_expires_at = datetime.utcnow() + timedelta(hours=1)
            db.commit()
            await query.answer("✅ Множитель x5 активирован на 1 час!")
            await show_shop(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    # Buy mining machines
    elif data == "buy_machine_basic":
        stats = get_machine_stats(1)
        price = stats["cost"]
        if user.coins >= price:
            user.coins -= price
            machine = MiningMachine(
                user_id=user.id,
                level=1,
                name="Базовая криптомашина",
                hash_rate=stats["hash_rate"],
                power_consumption=stats["power"],
                efficiency=stats["efficiency"]
            )
            db.add(machine)
            db.commit()
            await query.answer("✅ Криптомашина куплена!")
            await show_mining(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    elif data == "buy_machine_advanced":
        stats = get_machine_stats(2)
        price = stats["cost"]
        if user.coins >= price:
            user.coins -= price
            machine = MiningMachine(
                user_id=user.id,
                level=2,
                name="Продвинутая криптомашина",
                hash_rate=stats["hash_rate"],
                power_consumption=stats["power"],
                efficiency=stats["efficiency"]
            )
            db.add(machine)
            db.commit()
            await query.answer("✅ Криптомашина куплена!")
            await show_mining(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    # Buy cards
    elif data == "buy_card_common":
        price = CARD_PRICES["common"]
        income = CARD_INCOME["common"]
        if user.coins >= price:
            user.coins -= price
            card = UserCard(
                user_id=user.id,
                card_type="common",
                income_per_minute=income,
                experience_to_next_level=100
            )
            db.add(card)
            db.commit()
            await query.answer("✅ Карточка куплена!")
            await show_user_cards(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    elif data == "buy_card_rare":
        price = CARD_PRICES["rare"]
        income = CARD_INCOME["rare"]
        if user.coins >= price:
            user.coins -= price
            card = UserCard(
                user_id=user.id,
                card_type="rare",
                income_per_minute=income,
                experience_to_next_level=100
            )
            db.add(card)
            db.commit()
            await query.answer("✅ Карточка куплена!")
            await show_user_cards(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    elif data == "buy_card_epic":
        price = CARD_PRICES["epic"]
        income = CARD_INCOME["epic"]
        if user.coins >= price:
            user.coins -= price
            card = UserCard(
                user_id=user.id,
                card_type="epic",
                income_per_minute=income,
                experience_to_next_level=100
            )
            db.add(card)
            db.commit()
            await query.answer("✅ Карточка куплена!")
            await show_user_cards(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)
    
    elif data == "buy_card_legendary":
        price = CARD_PRICES["legendary"]
        income = CARD_INCOME["legendary"]
        if user.coins >= price:
            user.coins -= price
            card = UserCard(
                user_id=user.id,
                card_type="legendary",
                income_per_minute=income,
                experience_to_next_level=100
            )
            db.add(card)
            db.commit()
            await query.answer("✅ Карточка куплена!")
            await show_user_cards(query, user, db)
        else:
            await query.answer("⚠️ Недостаточно коинов!", show_alert=True)


async def handle_machine(query, data, user, db):
    """Handle machine interactions"""
    machine_id = int(data.split("_")[1])
    machine = db.query(MiningMachine).filter_by(id=machine_id, user_id=user.id).first()
    
    if not machine:
        await query.answer("❌ Машина не найдена!")
        return
    
    # Collect mining reward
    reward = calculate_mining_reward(machine)
    
    if reward > 0:
        user.quanhash += reward
        user.total_mined += reward
        machine.last_mined_at = datetime.utcnow()
        db.commit()
        from utils import play_sound
        play_sound(user, "mining")  # Play mining sound
        await query.answer(f"💰 +{format_currency(reward)} ⚡")
    
    # Show machine details
    message = f"""
🏭 <b>{machine.name}</b>

⚡ Hash Rate: {machine.hash_rate} H/s
🔋 Уровень: {machine.level}
⚙️ Эффективность: {machine.efficiency}x

💰 Намайнено: {format_currency(reward)} ⚡

Выберите действие:
    """
    
    keyboard = []
    if machine.is_active:
        keyboard.append([InlineKeyboardButton("⏸️ Остановить", callback_data=f"toggle_machine_{machine.id}")])
    else:
        keyboard.append([InlineKeyboardButton("▶️ Запустить", callback_data=f"toggle_machine_{machine.id}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="mining")])
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_card(query, data, user, db):
    """Handle card interactions"""
    card_id = int(data.split("_")[1])
    card = db.query(UserCard).filter_by(id=card_id, user_id=user.id).first()
    
    if not card:
        await query.answer("❌ Карточка не найдена!")
        return
    
    emoji = {"common": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟠"}.get(card.card_type, "⚪")
    
    message = f"""
{emoji} <b>Карточка</b>

📊 Тип: {card.card_type.title()}
⭐ Уровень: {card.card_level}
💰 Доход: {format_currency(card.income_per_minute)} 🪙/мин
📈 Опыт: {card.experience}/{card.experience_to_next_level}

Статус: {"✅ Активна" if card.is_active else "❌ Неактивна"}
    """
    
    keyboard = []
    keyboard.append([InlineKeyboardButton("🔄 Переключить", callback_data=f"toggle_card_{card.id}")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="cards")])
    
    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def show_referrals(query, user, db):
    """Show referral information"""
    bot_username = (await query.message.bot.get_me()).username
    
    message = f"""
👥 <b>Реферальная система</b>

🆔 Ваш реферальный код:
<code>{user.referral_code}</code>

📊 Статистика:
👥 Всего рефералов: {user.referrals_count}
💰 Доход с рефералов: {format_currency(user.referral_income)} 🪙

🔗 Ваша реферальная ссылка:
<code>https://t.me/{bot_username}?start={user.referral_code}</code>

💡 За каждого нового реферала вы получаете бонусы!
    """
    
    await query.edit_message_text(
        message,
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )


async def show_main_menu(query, user, db):
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


async def show_profile(query, user, db):
    """Show profile/settings menu"""
    sound_status = "🔊 Включены" if user.sound_enabled else "🔇 Выключены"
    
    message = f"""
⚙️ <b>Профиль и настройки</b>

👤 Пользователь: @{user.username or 'Без имени'}
💰 Коины: {format_currency(user.coins)} 🪙
💎 QuanHash: {format_currency(user.quanhash)} ⚡
⚡ Энергия: {user.energy}/{user.max_energy}

🔊 <b>Звуки:</b> {sound_status}

Выберите настройку:
    """
    
    await query.edit_message_text(
        message,
        reply_markup=get_profile_menu(user.sound_enabled),
        parse_mode='HTML'
    )


async def toggle_sound(query, user, db):
    """Toggle sound settings"""
    user.sound_enabled = not user.sound_enabled
    db.commit()
    
    status = "включены" if user.sound_enabled else "выключены"
    await query.answer(f"🔊 Звуки {status}!", show_alert=False)
    await show_profile(query, user, db)


async def test_sound(query, data, user, db):
    """Test sound playback"""
    if not user.sound_enabled:
        await query.answer("🔇 Звуки отключены! Включите их в настройках.", show_alert=True)
        return
    
    sound_type = data.replace("test_sound_", "")
    
    # Map sound types to descriptions
    sound_names = {
        "tap": "Звук тапа (Stage 1)",
        "mining": "Звук майнинга (Stage 2)",
        "purchase": "Звук покупки (Stage 3)"
    }
    
    sound_name = sound_names.get(sound_type, "Тестовый звук")
    
    # Since we're in a Telegram bot, we can't play sounds directly
    # But we can send a notification that sound would play
    # In a web app, this would trigger HTML5 audio playback
    await query.answer(f"🔊 Играет: {sound_name} (включите игру для прослушивания)", show_alert=False)
    
    # Log that sound should be played (for web app integration)
    logger.info(f"Sound test requested: {sound_type} for user {user.telegram_id}")
    
    # Trigger sound playback via utility
    from utils import play_sound
    play_sound(user, sound_type)


# Stub functions for missing handlers (to be implemented based on game logic)
async def handle_tap(query, user, db):
    """Handle tap action"""
    from utils import play_sound
    play_sound(user, "tap")
    await query.answer("💎 Тап выполнен! (Функция в разработке)", show_alert=False)


async def show_energy_status(query, user, db):
    """Show energy status"""
    message = f"""
⚡ <b>Энергия</b>

Текущая энергия: {user.energy}/{user.max_energy}
Восстановление: {user.energy_regen_rate} ед/мин

Энергия используется для тапов и других действий.
    """
    await query.edit_message_text(
        message,
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )


async def show_mining(query, user, db):
    """Show mining menu"""
    from keyboards import get_mining_menu
    message = """
🏭 <b>Майнинг</b>

Управление вашими криптомашинами.
    """
    await query.edit_message_text(
        message,
        reply_markup=get_mining_menu(db, user),
        parse_mode='HTML'
    )


async def show_user_cards(query, user, db):
    """Show user cards"""
    from keyboards import get_user_cards_menu
    message = """
💳 <b>Карточки</b>

Ваши карточки для пассивного дохода.
    """
    await query.edit_message_text(
        message,
        reply_markup=get_user_cards_menu(db, user),
        parse_mode='HTML'
    )


async def show_shop(query, user, db):
    """Show shop menu"""
    from keyboards import get_shop_menu
    message = f"""
🛒 <b>Магазин</b>

💰 Ваш баланс: {format_currency(user.coins)} 🪙

Выберите категорию:
    """
    await query.edit_message_text(
        message,
        reply_markup=get_shop_menu(),
        parse_mode='HTML'
    )


async def show_stats(query, user, db):
    """Show user statistics"""
    message = f"""
📊 <b>Статистика</b>

👤 Пользователь: @{user.username or 'Без имени'}
💰 Всего заработано: {format_currency(user.total_earned)} 🪙
💎 Всего намайнено: {format_currency(user.total_mined)} ⚡
👆 Всего тапов: {user.total_taps}

🔄 Последняя активность: {user.last_active.strftime('%d.%m.%Y %H:%M') if user.last_active else 'Никогда'}
    """
    await query.edit_message_text(
        message,
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )


async def show_rating(query, user, db):
    """Show rating/leaderboard"""
    from utils import get_top_users, get_user_rank
    top_users = get_top_users(db, "coins", 10)
    
    message = "🏆 <b>Рейтинг</b>\n\n"
    message += "<b>Топ-10 игроков:</b>\n\n"
    
    for i, top_user in enumerate(top_users, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        message += f"{emoji} @{top_user.username or 'Без имени'}: {format_currency(top_user.total_earned)} 🪙\n"
    
    user_rank = get_user_rank(db, user, "coins")
    message += f"\n📊 Ваше место: #{user_rank}"
    
    await query.edit_message_text(
        message,
        reply_markup=get_back_button(),
        parse_mode='HTML'
    )


async def handle_shop(query, data, user, db):
    """Handle shop category selection"""
    from keyboards import get_boosts_menu, get_machines_menu, get_cards_menu
    if data == "shop_boosts":
        await query.edit_message_reply_markup(get_boosts_menu())
    elif data == "shop_machines":
        await query.edit_message_reply_markup(get_machines_menu())
    elif data == "shop_cards":
        await query.edit_message_reply_markup(get_cards_menu())


async def handle_toggle(query, data, user, db):
    """Handle toggle actions (machines, cards, etc.)"""
    if data.startswith("toggle_machine_"):
        machine_id = int(data.split("_")[2])
        machine = db.query(MiningMachine).filter_by(id=machine_id, user_id=user.id).first()
        if machine:
            machine.is_active = not machine.is_active
            db.commit()
            status = "запущена" if machine.is_active else "остановлена"
            await query.answer(f"Машина {status}!", show_alert=False)
            await show_mining(query, user, db)
    elif data.startswith("toggle_card_"):
        card_id = int(data.split("_")[2])
        card = db.query(UserCard).filter_by(id=card_id, user_id=user.id).first()
        if card:
            card.is_active = not card.is_active
            db.commit()
            status = "активна" if card.is_active else "неактивна"
            await query.answer(f"Карточка {status}!", show_alert=False)
            await show_user_cards(query, user, db)
