#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

products = {
    # STARTER (1-10)
    1: {'title': '💫 Первые шаги', 'coins': '200,000', 'stars': 50, 'desc': 'Получите 200,000 коинов для старта игры', 'benefit': 'Отличное начало игры', 'emoji': '🌟'},
    2: {'title': '✨ Базовый старт', 'coins': '500,000', 'stars': 120, 'desc': 'Получите 500,000 коинов для быстрого роста', 'benefit': 'Быстрый старт', 'emoji': '✨'},
    3: {'title': '🌟 Начало пути', 'coins': '800,000', 'stars': 180, 'desc': 'Получите 800,000 коинов чтобы начать прогрессию', 'benefit': 'Твёрдый фундамент', 'emoji': '⭐'},
    4: {'title': '💎 Приветственный', 'coins': '1,000,000', 'stars': 240, 'desc': 'Получите 1,000,000 коинов - великолепный старт', 'benefit': 'VIP приветствие', 'emoji': '💎'},
    5: {'title': '🎁 Добро пожаловать', 'coins': '1,500,000', 'stars': 320, 'desc': 'Получите 1,500,000 коинов для мощного старта', 'benefit': 'Максимальная выгода', 'emoji': '🎁'},
    6: {'title': '💰 Стартовый пакет', 'coins': '2,000,000', 'stars': 400, 'desc': 'Получите 2,000,000 коинов для серьёзной игры', 'benefit': 'Серьёзный старт', 'emoji': '💰'},
    7: {'title': '⚡ Быстрый старт', 'coins': '2,500,000', 'stars': 480, 'desc': 'Получите 2,500,000 коинов для молниеносного роста', 'benefit': 'Максимальная скорость', 'emoji': '⚡'},
    8: {'title': '🎯 Первый шаг', 'coins': '3,000,000', 'stars': 560, 'desc': 'Получите 3,000,000 коинов для уверенного начала', 'benefit': 'Точное попадание', 'emoji': '🎯'},
    9: {'title': '🌈 Радужный набор', 'coins': '3,500,000', 'stars': 640, 'desc': 'Получите 3,500,000 коинов для яркого старта', 'benefit': 'Разноцветные возможности', 'emoji': '🌈'},
    10: {'title': '💫 Волшебный старт', 'coins': '4,000,000', 'stars': 720, 'desc': 'Получите 4,000,000 коинов для магического начала', 'benefit': 'Волшебная сила', 'emoji': '💫'},
    
    # PREMIUM (11-20)
    11: {'title': '⚡ Световой пакет', 'coins': '1,500,000', 'stars': 300, 'desc': 'Получите 1,500,000 коинов для яркого прогресса', 'benefit': 'Световая скорость', 'emoji': '⚡'},
    12: {'title': '🎯 Профессионал', 'coins': '3,000,000', 'stars': 600, 'desc': 'Получите 3,000,000 коинов для профессиональной игры', 'benefit': 'Точность мастера', 'emoji': '🎯'},
    13: {'title': '🚀 Мощный набор', 'coins': '4,500,000', 'stars': 900, 'desc': 'Получите 4,500,000 коинов для мощного рывка', 'benefit': 'Ракетный старт', 'emoji': '🚀'},
    14: {'title': '💎 Алмазный пакет', 'coins': '6,000,000', 'stars': 1200, 'desc': 'Получите 6,000,000 коинов для алмазного прогресса', 'benefit': 'Алмазная прочность', 'emoji': '💎'},
    15: {'title': '🔥 Огненный набор', 'coins': '7,500,000', 'stars': 1500, 'desc': 'Получите 7,500,000 коинов для огненной мощи', 'benefit': 'Пылающая энергия', 'emoji': '🔥'},
    16: {'title': '⚡ Электронный', 'coins': '9,000,000', 'stars': 1800, 'desc': 'Получите 9,000,000 коинов для электронного буста', 'benefit': 'Электрическая мощь', 'emoji': '⚡'},
    17: {'title': '🌟 Звёздный пакет', 'coins': '10,500,000', 'stars': 2100, 'desc': 'Получите 10,500,000 коинов для звёздного уровня', 'benefit': 'Звёздная слава', 'emoji': '🌟'},
    18: {'title': '💫 Космический', 'coins': '12,000,000', 'stars': 2400, 'desc': 'Получите 12,000,000 коинов для космического прогресса', 'benefit': 'Космическая скорость', 'emoji': '💫'},
    19: {'title': '🎁 Подарочный VIP', 'coins': '13,500,000', 'stars': 2700, 'desc': 'Получите 13,500,000 коинов для VIP статуса', 'benefit': 'VIP подарок', 'emoji': '🎁'},
    20: {'title': '🔮 Магический', 'coins': '15,000,000', 'stars': 3000, 'desc': 'Получите 15,000,000 коинов для магического роста', 'benefit': 'Магическая сила', 'emoji': '🔮'},
    
    # VIP (21-30) - уже обновлены
    21: {'title': '💎 VIP стартовый', 'coins': '5,000,000', 'stars': 1000, 'desc': 'Получите 5,000,000 коинов для начала VIP пути', 'benefit': 'Стартовый бонус включён', 'emoji': '💎'},
    22: {'title': '🚀 VIP ускорение', 'coins': '8,000,000', 'stars': 1600, 'desc': 'Получите 8,000,000 коинов + приоритетная обработка', 'benefit': 'Ускоренное начисление', 'emoji': '🚀'},
    23: {'title': '👑 VIP статус', 'coins': '12,000,000', 'stars': 2400, 'desc': 'Получите 12,000,000 коинов + эксклюзивный бонус', 'benefit': 'Официальный VIP статус', 'emoji': '👑'},
    24: {'title': '⚡ VIP турбо', 'coins': '16,000,000', 'stars': 3200, 'desc': 'Получите 16,000,000 коинов для турбо ускорения', 'benefit': 'Турбо режим активен', 'emoji': '⚡'},
    25: {'title': '💎 VIP королевство', 'coins': '20,000,000', 'stars': 4000, 'desc': 'Получите 20,000,000 коинов для королевского статуса', 'benefit': 'Королевская привилегия', 'emoji': '💎'},
    26: {'title': '🔓 VIP безлимит', 'coins': '25,000,000', 'stars': 5000, 'desc': 'Получите 25,000,000 коинов + максимальный бонус', 'benefit': 'Безлимитные возможности', 'emoji': '🔓'},
    27: {'title': '🏆 VIP чемпион', 'coins': '30,000,000', 'stars': 6000, 'desc': 'Получите 30,000,000 коинов для чемпионского статуса', 'benefit': 'Чемпионский уровень', 'emoji': '🏆'},
    28: {'title': '🌟 VIP легенда', 'coins': '35,000,000', 'stars': 7000, 'desc': 'Получите 35,000,000 коинов для легендарного статуса', 'benefit': 'Легендарная мощь', 'emoji': '🌟'},
    29: {'title': '💎 VIP алмаз', 'coins': '40,000,000', 'stars': 8000, 'desc': 'Получите 40,000,000 коинов + все VIP бонусы', 'benefit': 'Алмазная привилегия', 'emoji': '💎'},
    30: {'title': '👑 VIP император', 'coins': '45,000,000', 'stars': 9000, 'desc': 'Получите 45,000,000 коинов + максимальные премиум бонусы', 'benefit': 'Императорский доступ', 'emoji': '👑'},
    
    # QUANHASH (31-40)
    31: {'title': '🔮 Starter Hash', 'coins': '12,000,000', 'stars': 2500, 'desc': 'Получите 1,000 QuanHash для начала майнинга', 'benefit': 'Стартовый майнинг', 'emoji': '🔮'},
    32: {'title': '💎 Basic Hash', 'coins': '15,000,000', 'stars': 3200, 'desc': 'Получите 5,000 QuanHash для базового майнинга', 'benefit': 'Базовый хэш', 'emoji': '💎'},
    33: {'title': '⚡ Power Hash', 'coins': '18,000,000', 'stars': 3900, 'desc': 'Получите 10,000 QuanHash для мощного майнинга', 'benefit': 'Мощный хэш', 'emoji': '⚡'},
    34: {'title': '🔥 Fire Hash', 'coins': '21,000,000', 'stars': 4600, 'desc': 'Получите 15,000 QuanHash для огненного майнинга', 'benefit': 'Огненная мощность', 'emoji': '🔥'},
    35: {'title': '💥 Blast Hash', 'coins': '24,000,000', 'stars': 5300, 'desc': 'Получите 25,000 QuanHash для взрывного майнинга', 'benefit': 'Взрывной потенциал', 'emoji': '💥'},
    36: {'title': '🌟 Stellar Hash', 'coins': '27,000,000', 'stars': 6000, 'desc': 'Получите 50,000 QuanHash для звёздного майнинга', 'benefit': 'Звёздная скорость', 'emoji': '🌟'},
    37: {'title': '💎 Diamond Hash', 'coins': '30,000,000', 'stars': 6700, 'desc': 'Получите 100,000 QuanHash для алмазного майнинга', 'benefit': 'Алмазная прочность', 'emoji': '💎'},
    38: {'title': '🚀 Rocket Hash', 'coins': '33,000,000', 'stars': 7400, 'desc': 'Получите 250,000 QuanHash для ракетного майнинга', 'benefit': 'Ракетная мощь', 'emoji': '🚀'},
    39: {'title': '👑 Crown Hash', 'coins': '36,000,000', 'stars': 8100, 'desc': 'Получите 500,000 QuanHash для королевского майнинга', 'benefit': 'Королевский хэш', 'emoji': '👑'},
    40: {'title': '💫 Ultimate Hash', 'coins': '40,000,000', 'stars': 9000, 'desc': 'Получите 1,000,000 QuanHash для абсолютного майнинга', 'benefit': 'Ультимейт мощь', 'emoji': '💫'},
    
    # COMBO (41-50)
    41: {'title': '🎁 Стартовый мегасет', 'coins': '25,000,000', 'stars': 5000, 'desc': 'Получите 10 карточек + 1,000,000 коинов', 'benefit': 'Стартовый комбо', 'emoji': '🎁'},
    42: {'title': '🔥 Горячий комбо', 'coins': '35,000,000', 'stars': 7000, 'desc': 'Получите 20 карточек + 10,000,000 коинов', 'benefit': 'Горячая связка', 'emoji': '🔥'},
    43: {'title': '💎 Элитный набор', 'coins': '45,000,000', 'stars': 9000, 'desc': 'Получите 50 карточек + 50,000,000 коинов', 'benefit': 'Элитная комбинация', 'emoji': '💎'},
    44: {'title': '🚀 Мега связка', 'coins': '55,000,000', 'stars': 11000, 'desc': 'Получите 100 карточек + 100,000,000 коинов', 'benefit': 'Мега сила', 'emoji': '🚀'},
    45: {'title': '🌟 Легендарный мегасет', 'coins': '65,000,000', 'stars': 13000, 'desc': 'Получите 200 карточек + 200,000,000 коинов', 'benefit': 'Легендарная мощь', 'emoji': '🌟'},
    46: {'title': '💎 Бриллиантовая связка', 'coins': '75,000,000', 'stars': 15000, 'desc': 'VIP карты + безлимитные бонусы + 75M коинов', 'benefit': 'Бриллиантовый пакет', 'emoji': '💎'},
    47: {'title': '👑 Королевский комбо', 'coins': '85,000,000', 'stars': 17000, 'desc': '300 карточек + VIP доступ + 85M коинов', 'benefit': 'Королевская мощь', 'emoji': '👑'},
    48: {'title': '🔥 Огненный мегасет', 'coins': '95,000,000', 'stars': 19000, 'desc': '500 карточек + 500,000,000 коинов', 'benefit': 'Огненная мощь', 'emoji': '🔥'},
    49: {'title': '💫 Космический комбо', 'coins': '105,000,000', 'stars': 21000, 'desc': '1000 карточек + всё VIP + 105M коинов', 'benefit': 'Космическая сила', 'emoji': '💫'},
    50: {'title': '🎯 АБСОЛЮТ ВСЁ', 'coins': '120,000,000', 'stars': 24000, 'desc': 'ВСЁ что есть в игре! Абсолютный пакет', 'benefit': 'Абсолютная мощь', 'emoji': '🎯'},
    
    # VIP FUNCTIONS (51-60) - MEGA
    51: {'title': '👑 VIP Всё включено', 'coins': '50,000,000', 'stars': 5000, 'desc': 'Все функции + эксклюзив + 50M коинов', 'benefit': 'Скидка 50%', 'emoji': '👑'},
    52: {'title': '⭐ Эксклюзивный бейдж', 'coins': '100,000,000', 'stars': 2500, 'desc': 'Уникальная метка профиля + 100M коинов', 'benefit': 'Выделяйся', 'emoji': '⭐'},
    53: {'title': '🏆 Гарантирован топ', 'coins': '150,000,000', 'stars': 4000, 'desc': 'Место в топ-100 игроков + 150M коинов', 'benefit': 'Навсегда', 'emoji': '🏆'},
    54: {'title': '⚡ Мгновенный доход', 'coins': '200,000,000', 'stars': 6000, 'desc': 'Ускорение x100 + 200M коинов', 'benefit': 'Максимум выгода', 'emoji': '⚡'},
    55: {'title': '🔓 Снять лимиты', 'coins': '250,000,000', 'stars': 8000, 'desc': 'Никаких ограничений + 250M коинов', 'benefit': 'Бесконечные возможности', 'emoji': '🔓'},
    56: {'title': '🚀 Автопрокачка', 'coins': '300,000,000', 'stars': 10000, 'desc': 'Всё автоматически + 300M коинов', 'benefit': 'Без участия', 'emoji': '🚀'},
    57: {'title': '💎 Приоритет помощь', 'coins': '350,000,000', 'stars': 3500, 'desc': 'VIP поддержка 24/7 + 350M коинов', 'benefit': 'Первым отвечаем', 'emoji': '💎'},
    58: {'title': '👑 Золотой профиль', 'coins': '400,000,000', 'stars': 4500, 'desc': 'Уникальный дизайн профиля + 400M коинов', 'benefit': 'Императорский стиль', 'emoji': '👑'},
    59: {'title': '🌟 Супер статус', 'coins': '450,000,000', 'stars': 7000, 'desc': 'Премиум права везде + 450M коинов', 'benefit': 'Всё разблокировано', 'emoji': '🌟'},
    60: {'title': '🎯 АБСОЛЮТ ВСЁ VIP', 'coins': '500,000,000', 'stars': 15000, 'desc': 'Все премиум сразу + 500M коинов', 'benefit': 'Максимальная скидка', 'emoji': '🎯'},
}

categories = {
    'starter': {'name': 'СТАРТОВЫЕ НАБОРЫ', 'color': '102,126,234', 'button_color': '#667eea'},
    'premium': {'name': 'ПРЕМИУМ НАБОРЫ', 'color': '234,179,8', 'button_color': '#f59e0b'},
    'vip': {'name': 'ПРЕМИУМ ФУНКЦИИ', 'color': '255,215,0', 'button_color': '#ffd700'},
    'limited': {'name': 'QUANHASH НАБОРЫ', 'color': '255,0,0', 'button_color': '#ff0000'},
    'ultra': {'name': 'КОМБО СЕТЫ', 'color': '128,0,128', 'button_color': '#800080'},
    'mega': {'name': 'VIP ФУНКЦИИ', 'color': '255,215,0', 'button_color': '#ffd700'},
}

for cat_id, (cat_key, cat_info) in enumerate(categories.items(), 1):
    print(f"<!-- CATEGORY {cat_id}: {cat_info['name']} ({10 if cat_id < 6 else 10} products) -->")
    print(f'<div data-category="{cat_key}" style="display:block;text-align:center;font-size:13px;font-weight:700;color:#fff;margin:8px 0 4px;">{cat_info["name"]}</div>')
    print()
    
    start = (cat_id - 1) * 10 + 1
    end = min(start + 10, 61)
    
    for i in range(start, end):
        p = products[i]
        button_color = cat_info['button_color']
        is_vip = 'vip' in cat_key.lower() or 'mega' in cat_key.lower()
        
        print(f'''                        <div data-category="{cat_key}" style="background:rgba({cat_info['color']},0.25);padding:12px;border-radius:10px;border:1px solid rgba({cat_info['color']},0.5);">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                                <div style="font-size:32px;">{p['emoji']}</div>
                                <div style="flex:1;">
                                    <div style="font-size:14px;font-weight:700;color:#fff;">{p['title']}</div>
                                    <div style="font-size:10px;color:#94a3b8;">{p['desc']}</div>
                                    <div style="font-size:9px;color:{cat_info['color']};margin-top:3px;">✅ {p['benefit']}</div>
                                </div>
                            </div>
                            <button onclick="window.open('https://t.me/qanexus_bot?start=buy_stars_{i}')" style="width:100%;padding:9px;background:linear-gradient(135deg,{button_color},{button_color});color:{"#000" if is_vip else "#fff"};border:none;border-radius:8px;cursor:pointer;font-weight:700;font-size:12px;">💰 {p['stars']} ⭐</button>
                        </div>
                        ''')
    
    print()






