from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
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
            InlineKeyboardButton("🎮 Открыть игру", web_app=WebAppInfo(url="https://quantum-nexus.ru/web_app.html"))
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
        
        # Define product amounts
        product_coins = {
            1: 1000000,
            2: 5000000
        }
        
        coins_to_add = product_coins.get(product_id, 0)
        
        if coins_to_add == 0:
            logger.error(f"Unknown product: {product_id}")
            await update.message.reply_text("❌ Ошибка: неизвестный товар")
            return
        
        with get_db() as db:
            user = db.query(User).filter_by(id=user_db_id, telegram_id=user_id).first()
            
            if not user:
                logger.error(f"User not found: {user_db_id}/{user_id}")
                await update.message.reply_text("❌ Ошибка: пользователь не найден")
                return
            
            # Add coins
            user.coins += coins_to_add
            db.commit()
            
            # Log successful payment
            logger.info(f"✅ Stars payment successful! User {user_id} bought product {product_id} for {coins_to_add} coins")
            
            await update.message.reply_text(
                f"✨ Покупка успешна!\n\n"
                f"💎 Оплачено: {payment.total_amount} ⭐\n"
                f"💰 Получено: {coins_to_add:,} коинов\n\n"
                f"📊 Новый баланс: {user.coins:,} коинов"
            )
            
    except Exception as e:
        logger.error(f"Error processing payment: {e}", exc_info=True)
        await update.message.reply_text("❌ Ошибка при обработке платежа")


async def send_stars_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE, product_id: int):
    """Send Stars invoice with real Telegram Stars payment"""
    
    logger.info(f"=== send_stars_invoice called with product_id={product_id} ===")
    
    # Define products with Stars prices
    products = {
        1: {
            'title': 'Стартовый пакет',
            'description': '1,000,000 коинов',
            'stars': 10,  # Stars
            'coins': 1000000
        },
        2: {
            'title': 'Премиум пакет',
            'description': '5,000,000 коинов',
            'stars': 40,  # Stars
            'coins': 5000000
        }
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
            await update.message.reply_text(f"✅ Invoice отправлен! Проверьте сообщение выше.")
            
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
