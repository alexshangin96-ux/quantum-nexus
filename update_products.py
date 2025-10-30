#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Этот скрипт генерирует обновленные карточки товаров с полными описаниями

products = [
    # Starter (1-10)
    {'id': 1, 'cat': 'starter', 'emoji': '🌟', 'title': 'Первые шаги', 'desc': 'Получите 200,000 коинов для старта игры', 'benefit': 'Отличное начало игры', 'stars': 50},
    {'id': 2, 'cat': 'starter', 'emoji': '✨', 'title': 'Базовый старт', 'desc': 'Получите 500,000 коинов для быстрого роста', 'benefit': 'Быстрый старт', 'stars': 120},
    {'id': 3, 'cat': 'starter', 'emoji': '⭐', 'title': 'Начало пути', 'desc': 'Получите 800,000 коинов чтобы начать прогрессию', 'benefit': 'Твёрдый фундамент', 'stars': 180},
    {'id': 4, 'cat': 'starter', 'emoji': '💎', 'title': 'Приветственный', 'desc': 'Получите 1,000,000 коинов - великолепный старт', 'benefit': 'VIP приветствие', 'stars': 240},
    {'id': 5, 'cat': 'starter', 'emoji': '🎁', 'title': 'Добро пожаловать', 'desc': 'Получите 1,500,000 коинов для мощного старта', 'benefit': 'Максимальная выгода', 'stars': 320},
    {'id': 6, 'cat': 'starter', 'emoji': '💰', 'title': 'Стартовый пакет', 'desc': 'Получите 2,000,000 коинов для серьёзной игры', 'benefit': 'Серьёзный старт', 'stars': 400},
    {'id': 7, 'cat': 'starter', 'emoji': '⚡', 'title': 'Быстрый старт', 'desc': 'Получите 2,500,000 коинов для молниеносного роста', 'benefit': 'Максимальная скорость', 'stars': 480},
    {'id': 8, 'cat': 'starter', 'emoji': '🎯', 'title': 'Первый шаг', 'desc': 'Получите 3,000,000 коинов для уверенного начала', 'benefit': 'Точное попадание', 'stars': 560},
    {'id': 9, 'cat': 'starter', 'emoji': '🌈', 'title': 'Радужный набор', 'desc': 'Получите 3,500,000 коинов для яркого старта', 'benefit': 'Разноцветные возможности', 'stars': 640},
    {'id': 10, 'cat': 'starter', 'emoji': '💫', 'title': 'Волшебный старт', 'desc': 'Получите 4,000,000 коинов для магического начала', 'benefit': 'Волшебная сила', 'stars': 720},
    
    # Premium (11-20)
    {'id': 11, 'cat': 'premium', 'emoji': '⚡', 'title': 'Световой пакет', 'desc': 'Получите 1,500,000 коинов для яркого прогресса', 'benefit': 'Световая скорость', 'stars': 300},
    {'id': 12, 'cat': 'premium', 'emoji': '🎯', 'title': 'Профессионал', 'desc': 'Получите 3,000,000 коинов для профессиональной игры', 'benefit': 'Точность мастера', 'stars': 600},
    {'id': 13, 'cat': 'premium', 'emoji': '🚀', 'title': 'Мощный набор', 'desc': 'Получите 4,500,000 коинов для мощного рывка', 'benefit': 'Ракетный старт', 'stars': 900},
    {'id': 14, 'cat': 'premium', 'emoji': '💎', 'title': 'Алмазный пакет', 'desc': 'Получите 6,000,000 коинов для алмазного прогресса', 'benefit': 'Алмазная прочность', 'stars': 1200},
    {'id': 15, 'cat': 'premium', 'emoji': '🔥', 'title': 'Огненный набор', 'desc': 'Получите 7,500,000 коинов для огненной мощи', 'benefit': 'Пылающая энергия', 'stars': 1500},
    {'id': 16, 'cat': 'premium', 'emoji': '⚡', 'title': 'Электронный', 'desc': 'Получите 9,000,000 коинов для электронного буста', 'benefit': 'Электрическая мощь', 'stars': 1800},
    {'id': 17, 'cat': 'premium', 'emoji': '🌟', 'title': 'Звёздный пакет', 'desc': 'Получите 10,500,000 коинов для звёздного уровня', 'benefit': 'Звёздная слава', 'stars': 2100},
    {'id': 18, 'cat': 'premium', 'emoji': '💫', 'title': 'Космический', 'desc': 'Получите 12,000,000 коинов для космического прогресса', 'benefit': 'Космическая скорость', 'stars': 2400},
    {'id': 19, 'cat': 'premium', 'emoji': '🎁', 'title': 'Подарочный VIP', 'desc': 'Получите 13,500,000 коинов для VIP статуса', 'benefit': 'VIP подарок', 'stars': 2700},
    {'id': 20, 'cat': 'premium', 'emoji': '🔮', 'title': 'Магический', 'desc': 'Получите 15,000,000 коинов для магического роста', 'benefit': 'Магическая сила', 'stars': 3000},
    
    # VIP (21-30) - уже обновлены
    {'id': 21, 'cat': 'vip', 'emoji': '💎', 'title': 'VIP стартовый', 'desc': 'Получите 5,000,000 коинов для начала VIP пути', 'benefit': 'Стартовый бонус включён', 'stars': 1000},
    {'id': 22, 'cat': 'vip', 'emoji': '🚀', 'title': 'VIP ускорение', 'desc': 'Получите 8,000,000 коинов + приоритетная обработка', 'benefit': 'Ускоренное начисление', 'stars': 1600},
    {'id': 23, 'cat': 'vip', 'emoji': '👑', 'title': 'VIP статус', 'desc': 'Получите 12,000,000 коинов + эксклюзивный бонус', 'benefit': 'Официальный VIP статус', 'stars': 2400},
    {'id': 24, 'cat': 'vip', 'emoji': '⚡', 'title': 'VIP турбо', 'desc': 'Получите 16,000,000 коинов для турбо ускорения', 'benefit': 'Турбо режим активен', 'stars': 3200},
    {'id': 25, 'cat': 'vip', 'emoji': '💎', 'title': 'VIP королевство', 'desc': 'Получите 20,000,000 коинов для королевского статуса', 'benefit': 'Королевская привилегия', 'stars': 4000},
    {'id': 26, 'cat': 'vip', 'emoji': '🔓', 'title': 'VIP безлимит', 'desc': 'Получите 25,000,000 коинов + максимальный бонус', 'benefit': 'Безлимитные возможности', 'stars': 5000},
    {'id': 27, 'cat': 'vip', 'emoji': '🏆', 'title': 'VIP чемпион', 'desc': 'Получите 30,000,000 коинов для чемпионского статуса', 'benefit': 'Чемпионский уровень', 'stars': 6000},
    {'id': 28, 'cat': 'vip', 'emoji': '🌟', 'title': 'VIP легенда', 'desc': 'Получите 35,000,000 коинов для легендарного статуса', 'benefit': 'Легендарная мощь', 'stars': 7000},
    {'id': 29, 'cat': 'vip', 'emoji': '💎', 'title': 'VIP алмаз', 'desc': 'Получите 40,000,000 коинов + все VIP бонусы', 'benefit': 'Алмазная привилегия', 'stars': 8000},
    {'id': 30, 'cat': 'vip', 'emoji': '👑', 'title': 'VIP император', 'desc': 'Получите 45,000,000 коинов + максимальные премиум бонусы', 'benefit': 'Императорский доступ', 'stars': 9000},
    
    # QuanHash (31-40)
    {'id': 31, 'cat': 'limited', 'emoji': '🔮', 'title': 'Starter Hash', 'desc': 'Получите 1,000 QuanHash для начала майнинга', 'benefit': 'Стартовый майнинг', 'stars': 2500},
    {'id': 32, 'cat': 'limited', 'emoji': '💎', 'title': 'Basic Hash', 'desc': 'Получите 5,000 QuanHash для базового майнинга', 'benefit': 'Базовый хэш', 'stars': 3200},
    {'id': 33, 'cat': 'limited', 'emoji': '⚡', 'title': 'Power Hash', 'desc': 'Получите 10,000 QuanHash для мощного майнинга', 'benefit': 'Мощный хэш', 'stars': 3900},
    {'id': 34, 'cat': 'limited', 'emoji': '🔥', 'title': 'Fire Hash', 'desc': 'Получите 15,000 QuanHash для огненного майнинга', 'benefit': 'Огненная мощность', 'stars': 4600},
    {'id': 35, 'cat': 'limited', 'emoji': '💥', 'title': 'Blast Hash', 'desc': 'Получите 25,000 QuanHash для взрывного майнинга', 'benefit': 'Взрывной потенциал', 'stars': 5300},
    {'id': 36, 'cat': 'limited', 'emoji': '🌟', 'title': 'Stellar Hash', 'desc': 'Получите 50,000 QuanHash для звёздного майнинга', 'benefit': 'Звёздная скорость', 'stars': 6000},
    {'id': 37, 'cat': 'limited', 'emoji': '💎', 'title': 'Diamond Hash', 'desc': 'Получите 100,000 QuanHash для алмазного майнинга', 'benefit': 'Алмазная прочность', 'stars': 6700},
    {'id': 38, 'cat': 'limited', 'emoji': '🚀', 'title': 'Rocket Hash', 'desc': 'Получите 250,000 QuanHash для ракетного майнинга', 'benefit': 'Ракетная мощь', 'stars': 7400},
    {'id': 39, 'cat': 'limited', 'emoji': '👑', 'title': 'Crown Hash', 'desc': 'Получите 500,000 QuanHash для королевского майнинга', 'benefit': 'Королевский хэш', 'stars': 8100},
    {'id': 40, 'cat': 'limited', 'emoji': '💫', 'title': 'Ultimate Hash', 'desc': 'Получите 1,000,000 QuanHash для абсолютного майнинга', 'benefit': 'Ультимейт мощь', 'stars': 9000},
    
    # Combo (41-50)
    {'id': 41, 'cat': 'ultra', 'emoji': '🎁', 'title': 'Стартовый мегасет', 'desc': 'Получите 10 карточек + 1,000,000 коинов', 'benefit': 'Стартовый комбо', 'stars': 5000},
    {'id': 42, 'cat': 'ultra', 'emoji': '🔥', 'title': 'Горячий комбо', 'desc': 'Получите 20 карточек + 10,000,000 коинов', 'benefit': 'Горячая связка', 'stars': 7000},
    {'id': 43, 'cat': 'ultra', 'emoji': '💎', 'title': 'Элитный набор', 'desc': 'Получите 50 карточек + 50,000,000 коинов', 'benefit': 'Элитная комбинация', 'stars': 9000},
    {'id': 44, 'cat': 'ultra', 'emoji': '🚀', 'title': 'Мега связка', 'desc': 'Получите 100 карточек + 100,000,000 коинов', 'benefit': 'Мега сила', 'stars': 11000},
    {'id': 45, 'cat': 'ultra', 'emoji': '🌟', 'title': 'Легендарный мегасет', 'desc': 'Получите 200 карточек + 200,000,000 коинов', 'benefit': 'Легендарная мощь', 'stars': 13000},
    {'id': 46, 'cat': 'ultra', 'emoji': '💎', 'title': 'Бриллиантовая связка', 'desc': 'VIP карты + безлимитные бонусы + 75M коинов', 'benefit': 'Бриллиантовый пакет', 'stars': 15000},
    {'id': 47, 'cat': 'ultra', 'emoji': '👑', 'title': 'Королевский комбо', 'desc': '300 карточек + VIP доступ + 85M коинов', 'benefit': 'Королевская мощь', 'stars': 17000},
    {'id': 48, 'cat': 'ultra', 'emoji': '🔥', 'title': 'Огненный мегасет', 'desc': '500 карточек + 500,000,000 коинов', 'benefit': 'Огненная мощь', 'stars': 19000},
    {'id': 49, 'cat': 'ultra', 'emoji': '💫', 'title': 'Космический комбо', 'desc': '1000 карточек + всё VIP + 105M коинов', 'benefit': 'Космическая сила', 'stars': 21000},
    {'id': 50, 'cat': 'ultra', 'emoji': '🎯', 'title': 'АБСОЛЮТ ВСЁ', 'desc': 'ВСЁ что есть в игре! Абсолютный пакет', 'benefit': 'Абсолютная мощь', 'stars': 24000},
    
    # VIP Functions (51-60) - MEGA
    {'id': 51, 'cat': 'mega', 'emoji': '👑', 'title': 'VIP Всё включено', 'desc': 'Все функции + эксклюзив + 50M коинов', 'benefit': 'Скидка 50%', 'stars': 5000},
    {'id': 52, 'cat': 'mega', 'emoji': '⭐', 'title': 'Эксклюзивный бейдж', 'desc': 'Уникальная метка профиля + 100M коинов', 'benefit': 'Выделяйся', 'stars': 2500},
    {'id': 53, 'cat': 'mega', 'emoji': '🏆', 'title': 'Гарантирован топ', 'desc': 'Место в топ-100 игроков + 150M коинов', 'benefit': 'Навсегда', 'stars': 4000},
    {'id': 54, 'cat': 'mega', 'emoji': '⚡', 'title': 'Мгновенный доход', 'desc': 'Ускорение x100 + 200M коинов', 'benefit': 'Максимум выгода', 'stars': 6000},
    {'id': 55, 'cat': 'mega', 'emoji': '🔓', 'title': 'Снять лимиты', 'desc': 'Никаких ограничений + 250M коинов', 'benefit': 'Бесконечные возможности', 'stars': 8000},
    {'id': 56, 'cat': 'mega', 'emoji': '🚀', 'title': 'Автопрокачка', 'desc': 'Всё автоматически + 300M коинов', 'benefit': 'Без участия', 'stars': 10000},
    {'id': 57, 'cat': 'mega', 'emoji': '💎', 'title': 'Приоритет помощь', 'desc': 'VIP поддержка 24/7 + 350M коинов', 'benefit': 'Первым отвечаем', 'stars': 3500},
    {'id': 58, 'cat': 'mega', 'emoji': '👑', 'title': 'Золотой профиль', 'desc': 'Уникальный дизайн профиля + 400M коинов', 'benefit': 'Императорский стиль', 'stars': 4500},
    {'id': 59, 'cat': 'mega', 'emoji': '🌟', 'title': 'Супер статус', 'desc': 'Премиум права везде + 450M коинов', 'benefit': 'Всё разблокировано', 'stars': 7000},
    {'id': 60, 'cat': 'mega', 'emoji': '🎯', 'title': 'АБСОЛЮТ ВСЁ VIP', 'desc': 'Все премиум сразу + 500M коинов', 'benefit': 'Максимальная скидка', 'stars': 15000},
]

for p in products:
    cat_info = {
        'starter': {'color': '102,126,234', 'btn_color': '#667eea'},
        'premium': {'color': '234,179,8', 'btn_color': '#f59e0b'},
        'vip': {'color': '255,215,0', 'btn_color': '#ffd700'},
        'limited': {'color': '255,0,0', 'btn_color': '#ff0000'},
        'ultra': {'color': '128,0,128', 'btn_color': '#800080'},
        'mega': {'color': '255,215,0', 'btn_color': '#ffd700'},
    }
    
    colors = cat_info[p['cat']]
    btn_color = colors['btn_color']
    is_vip = p['cat'] in ['vip', 'mega']
    
    print(f"""
                        <div data-category="{p['cat']}" style="background:rgba({colors['color']},0.25);padding:12px;border-radius:10px;border:1px solid rgba({colors['color']},0.5);">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                                <div style="font-size:32px;">{p['emoji']}</div>
                                <div style="flex:1;">
                                    <div style="font-size:15px;font-weight:700;color:#fff;">{p['emoji']} {p['title']}</div>
                                    <div style="font-size:11px;color:#94a3b8;margin-top:4px;">{p['desc']}</div>
                                    <div style="font-size:10px;color:{colors['color']};margin-top:4px;">✅ {p['benefit']}</div>
                                </div>
                            </div>
                            <button onclick="window.open('https://t.me/qanexus_bot?start=buy_stars_{p['id']}')" style="width:100%;padding:9px;background:linear-gradient(135deg,{btn_color},{btn_color});color:{"#000" if is_vip else "#fff"};border:none;border-radius:8px;cursor:pointer;font-weight:700;font-size:12px;">💰 {p['stars']} ⭐</button>
                        </div>
                        """)






