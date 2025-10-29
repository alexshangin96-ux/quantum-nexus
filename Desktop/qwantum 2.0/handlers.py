from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from models import User, MiningMachine, UserCard, Transaction
from keyboards import *
from utils import *
from database import get_db
from config import *
import logging


async def handle_purchase(query, data, user, db):
    """Handle purchases"""
    if data == "buy_energy_50":
        price = 1000
        if user.coins >= price:
            user.coins -= price
            user.energy = min(user.energy + 50, user.max_energy)
            db.commit()
            await query.answer("✅ Энергия куплена!")
            await show_shop(query, user)
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
            await show_shop(query, user)
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
            await show_shop(query, user)
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
