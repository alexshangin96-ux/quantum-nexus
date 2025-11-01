from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from models import MiningMachine, UserCard


def get_main_menu():
    """Main game menu"""
    keyboard = [
        [
            InlineKeyboardButton("💎 Тап", callback_data="tap"),
            InlineKeyboardButton("⚡ Энергия", callback_data="energy_status"),
        ],
        [
            InlineKeyboardButton("🏭 Майнинг", callback_data="mining"),
            InlineKeyboardButton("💳 Карточки", callback_data="cards"),
        ],
        [
            InlineKeyboardButton("🛒 Магазин", callback_data="shop"),
            InlineKeyboardButton("📊 Статистика", callback_data="stats"),
        ],
        [
            InlineKeyboardButton("🏆 Рейтинг", callback_data="rating"),
            InlineKeyboardButton("👥 Рефералы", callback_data="referrals"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_shop_menu():
    """Shop menu"""
    keyboard = [
        [InlineKeyboardButton("⚡ Бусты", callback_data="shop_boosts")],
        [InlineKeyboardButton("🏭 Криптомашины", callback_data="shop_machines")],
        [InlineKeyboardButton("💳 Карточки", callback_data="shop_cards")],
        [InlineKeyboardButton("⚡ Энергия", callback_data="shop_energy")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_boosts_menu():
    """Boosts shop menu"""
    keyboard = [
        [
            InlineKeyboardButton("2x Множитель (1000 🪙)", callback_data="buy_boost_multiplier_2x"),
        ],
        [
            InlineKeyboardButton("5x Множитель (5000 🪙)", callback_data="buy_boost_multiplier_5x"),
        ],
        [
            InlineKeyboardButton("⚡ Бустер энергии (500 🪙)", callback_data="buy_boost_energy_booster"),
        ],
        [
            InlineKeyboardButton("⛏️ Буст майнинга (2000 🪙)", callback_data="buy_boost_mining"),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="shop")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_machines_menu():
    """Mining machines shop menu"""
    keyboard = [
        [
            InlineKeyboardButton("💎 Базовая машина (10k 🪙)", callback_data="buy_machine_basic"),
        ],
        [
            InlineKeyboardButton("⚡ Продвинутая (50k 🪙)", callback_data="buy_machine_advanced"),
        ],
        [
            InlineKeyboardButton("🚀 Профессиональная (200k 🪙)", callback_data="buy_machine_pro"),
        ],
        [
            InlineKeyboardButton("👑 Легендарная (1M 🪙)", callback_data="buy_machine_legendary"),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="shop")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cards_menu():
    """Cards shop menu"""
    keyboard = [
        [
            InlineKeyboardButton("🟢 Обычная (500 🪙)", callback_data="buy_card_common"),
        ],
        [
            InlineKeyboardButton("🔵 Редкая (2000 🪙)", callback_data="buy_card_rare"),
        ],
        [
            InlineKeyboardButton("🟣 Эпическая (10000 🪙)", callback_data="buy_card_epic"),
        ],
        [
            InlineKeyboardButton("🟠 Легендарная (50000 🪙)", callback_data="buy_card_legendary"),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="shop")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_mining_menu(db, user):
    """Mining menu with user machines"""
    keyboard = []
    
    # Get user machines
    machines = db.query(MiningMachine).filter_by(user_id=user.id).all()
    
    if machines:
        for machine in machines:
            status = "✅" if machine.is_active else "❌"
            keyboard.append([
                InlineKeyboardButton(
                    f"{status} {machine.name} Lv.{machine.level}",
                    callback_data=f"machine_{machine.id}"
                )
            ])
    
    keyboard.append([InlineKeyboardButton("➕ Купить машину", callback_data="shop_machines")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)


def get_user_cards_menu(db, user):
    """User cards menu"""
    keyboard = []
    
    # Get user cards
    cards = db.query(UserCard).filter_by(user_id=user.id).all()
    
    if cards:
        for card in cards:
            emoji = {"common": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟠"}.get(card.card_type, "⚪")
            status = "✅" if card.is_active else "❌"
            keyboard.append([
                InlineKeyboardButton(
                    f"{emoji} {status} {card.card_type.title()} Lv.{card.card_level}",
                    callback_data=f"card_{card.id}"
                )
            ])
    
    keyboard.append([InlineKeyboardButton("➕ Купить карточку", callback_data="shop_cards")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)


def get_back_button():
    """Back button"""
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]])


def confirm_action(action_id):
    """Confirm action buttons"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Да", callback_data=f"confirm_{action_id}"),
            InlineKeyboardButton("❌ Нет", callback_data="cancel_action"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)











