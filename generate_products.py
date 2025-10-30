#!/usr/bin/env python3
# Generate HTML for all 60 products

# Product data from handlers.py
products = [
    # STARTING (1-10)
    {'id': 1, 'cat': 'starter', 'title': '💫 Первые шаги', 'desc': '200,000 коинов', 'stars': 50, 'emoji': '🌟'},
    {'id': 2, 'cat': 'starter', 'title': '✨ Базовый', 'desc': '500,000 коинов', 'stars': 120, 'emoji': '💎'},
    {'id': 3, 'cat': 'starter', 'title': '🌟 Начало пути', 'desc': '800,000 коинов', 'stars': 180, 'emoji': '⭐'},
    {'id': 4, 'cat': 'starter', 'title': '💎 Приветственный', 'desc': '1,000,000 коинов', 'stars': 240, 'emoji': '💫'},
    {'id': 5, 'cat': 'starter', 'title': '🎁 Добро пожаловать', 'desc': '1,500,000 коинов', 'stars': 320, 'emoji': '🎁'},
    {'id': 6, 'cat': 'starter', 'title': '💰 Стартовый', 'desc': '2,000,000 коинов', 'stars': 400, 'emoji': '💰'},
    {'id': 7, 'cat': 'starter', 'title': '⚡ Быстрый старт', 'desc': '2,500,000 коинов', 'stars': 480, 'emoji': '⚡'},
    {'id': 8, 'cat': 'starter', 'title': '🎯 Первый шаг', 'desc': '3,000,000 коинов', 'stars': 560, 'emoji': '🎯'},
    {'id': 9, 'cat': 'starter', 'title': '🌈 Радуга', 'desc': '3,500,000 коинов', 'stars': 640, 'emoji': '🌈'},
    {'id': 10, 'cat': 'starter', 'title': '💫 Волшебный', 'desc': '4,000,000 коинов', 'stars': 720, 'emoji': '💫'},
    # PREMIUM (11-20)
    {'id': 11, 'cat': 'premium', 'title': '⚡ Световой', 'desc': '1,500,000 коинов', 'stars': 300, 'emoji': '⚡'},
    {'id': 12, 'cat': 'premium', 'title': '🎯 Профессионал', 'desc': '3,000,000 коинов', 'stars': 600, 'emoji': '🎯'},
    {'id': 13, 'cat': 'premium', 'title': '🚀 Мощь', 'desc': '4,500,000 коинов', 'stars': 900, 'emoji': '🚀'},
    {'id': 14, 'cat': 'premium', 'title': '💎 Алмазный', 'desc': '6,000,000 коинов', 'stars': 1200, 'emoji': '💎'},
    {'id': 15, 'cat': 'premium', 'title': '🔥 Огненный', 'desc': '7,500,000 коинов', 'stars': 1500, 'emoji': '🔥'},
    {'id': 16, 'cat': 'premium', 'title': '⚡ Электронный', 'desc': '9,000,000 коинов', 'stars': 1800, 'emoji': '⚡'},
    {'id': 17, 'cat': 'premium', 'title': '🌟 Звёздный', 'desc': '10,500,000 коинов', 'stars': 2100, 'emoji': '🌟'},
    {'id': 18, 'cat': 'premium', 'title': '💫 Космический', 'desc': '12,000,000 коинов', 'stars': 2400, 'emoji': '💫'},
    {'id': 19, 'cat': 'premium', 'title': '🎁 Подарочный VIP', 'desc': '13,500,000 коинов', 'stars': 2700, 'emoji': '🎁'},
    {'id': 20, 'cat': 'premium', 'title': '🔮 Магический', 'desc': '15,000,000 коинов', 'stars': 3000, 'emoji': '🔮'},
    # VIP (21-30)
    {'id': 21, 'cat': 'vip', 'title': '👑 Золотой статус', 'desc': '5,000,000 коинов', 'stars': 1000, 'emoji': '👑'},
    {'id': 22, 'cat': 'vip', 'title': '💸 Платиновый', 'desc': '8,000,000 коинов', 'stars': 1600, 'emoji': '💸'},
    {'id': 23, 'cat': 'vip', 'title': '💰 Титановый', 'desc': '12,000,000 коинов', 'stars': 2400, 'emoji': '💰'},
    {'id': 24, 'cat': 'vip', 'title': '👑 Императорский', 'desc': '16,000,000 коинов', 'stars': 3200, 'emoji': '👑'},
    {'id': 25, 'cat': 'vip', 'title': '🌟 Легендарный', 'desc': '20,000,000 коинов', 'stars': 4000, 'emoji': '🌟'},
    {'id': 26, 'cat': 'vip', 'title': '💎 Королевский', 'desc': '25,000,000 коинов', 'stars': 5000, 'emoji': '💎'},
    {'id': 27, 'cat': 'vip', 'title': '⭐ Мифический VIP', 'desc': '30,000,000 коинов', 'stars': 6000, 'emoji': '⭐'},
    {'id': 28, 'cat': 'vip', 'title': '🏆 Чемпионский', 'desc': '35,000,000 коинов', 'stars': 7000, 'emoji': '🏆'},
    {'id': 29, 'cat': 'vip', 'title': '👑 Абсолютный', 'desc': '40,000,000 коинов', 'stars': 8000, 'emoji': '👑'},
    {'id': 30, 'cat': 'vip', 'title': '💎 Бриллиантовый', 'desc': '45,000,000 коинов', 'stars': 9000, 'emoji': '💎'},
    # LIMITED (31-40)
    {'id': 31, 'cat': 'limited', 'title': '🔥 Файер-набор', 'desc': '12,000,000 коинов', 'stars': 2500, 'emoji': '🔥'},
    {'id': 32, 'cat': 'limited', 'title': '💥 Мега взрыв', 'desc': '15,000,000 коинов', 'stars': 3200, 'emoji': '💥'},
    {'id': 33, 'cat': 'limited', 'title': '⚡ Атомный удар', 'desc': '18,000,000 коинов', 'stars': 3900, 'emoji': '⚡'},
    {'id': 34, 'cat': 'limited', 'title': '🔥 Огненный шторм', 'desc': '21,000,000 коинов', 'stars': 4600, 'emoji': '🔥'},
    {'id': 35, 'cat': 'limited', 'title': '💥 Ядерный', 'desc': '24,000,000 коинов', 'stars': 5300, 'emoji': '💥'},
    {'id': 36, 'cat': 'limited', 'title': '⚡ Молниеносный', 'desc': '27,000,000 коинов', 'stars': 6000, 'emoji': '⚡'},
    {'id': 37, 'cat': 'limited', 'title': '🔥 Вулканический', 'desc': '30,000,000 коинов', 'stars': 6700, 'emoji': '🔥'},
    {'id': 38, 'cat': 'limited', 'title': '💥 Апокалиптический', 'desc': '33,000,000 коинов', 'stars': 7400, 'emoji': '💥'},
    {'id': 39, 'cat': 'limited', 'title': '⚡ Космический взрыв', 'desc': '36,000,000 коинов', 'stars': 8100, 'emoji': '⚡'},
    {'id': 40, 'cat': 'limited', 'title': '🔥 Финальный огонь', 'desc': '40,000,000 коинов', 'stars': 9000, 'emoji': '🔥'},
    # ULTRA (41-50)
    {'id': 41, 'cat': 'ultra', 'title': '💎 Легенда', 'desc': '25,000,000 коинов', 'stars': 5000, 'emoji': '💎'},
    {'id': 42, 'cat': 'ultra', 'title': '🌟 Мифический', 'desc': '35,000,000 коинов', 'stars': 7000, 'emoji': '🌟'},
    {'id': 43, 'cat': 'ultra', 'title': '💫 Бесконечность', 'desc': '45,000,000 коинов', 'stars': 9000, 'emoji': '💫'},
    {'id': 44, 'cat': 'ultra', 'title': '💎 Вечность', 'desc': '55,000,000 коинов', 'stars': 11000, 'emoji': '💎'},
    {'id': 45, 'cat': 'ultra', 'title': '🌟 Вселенная', 'desc': '65,000,000 коинов', 'stars': 13000, 'emoji': '🌟'},
    {'id': 46, 'cat': 'ultra', 'title': '💎 Абсолют', 'desc': '75,000,000 коинов', 'stars': 15000, 'emoji': '💎'},
    {'id': 47, 'cat': 'ultra', 'title': '🌟 Техногенезис', 'desc': '85,000,000 коинов', 'stars': 17000, 'emoji': '🌟'},
    {'id': 48, 'cat': 'ultra', 'title': '💎 Квантовый', 'desc': '95,000,000 коинов', 'stars': 19000, 'emoji': '💎'},
    {'id': 49, 'cat': 'ultra', 'title': '🌟 Феникс', 'desc': '105,000,000 коинов', 'stars': 21000, 'emoji': '🌟'},
    {'id': 50, 'cat': 'ultra', 'title': '💎 Богиня', 'desc': '120,000,000 коинов', 'stars': 24000, 'emoji': '💎'},
    # MEGA (51-60)
    {'id': 51, 'cat': 'mega', 'title': '🚀 Космос', 'desc': '50,000,000 коинов', 'stars': 10000, 'emoji': '🚀'},
    {'id': 52, 'cat': 'mega', 'title': '⭐ Вселенная', 'desc': '100,000,000 коинов', 'stars': 20000, 'emoji': '⭐'},
    {'id': 53, 'cat': 'mega', 'title': '🌌 Галактика', 'desc': '150,000,000 коинов', 'stars': 30000, 'emoji': '🌌'},
    {'id': 54, 'cat': 'mega', 'title': '🌟 Созвездие', 'desc': '200,000,000 коинов', 'stars': 40000, 'emoji': '🌟'},
    {'id': 55, 'cat': 'mega', 'title': '💫 Туманность', 'desc': '250,000,000 коинов', 'stars': 50000, 'emoji': '💫'},
    {'id': 56, 'cat': 'mega', 'title': '🚀 Вихрь', 'desc': '300,000,000 коинов', 'stars': 60000, 'emoji': '🚀'},
    {'id': 57, 'cat': 'mega', 'title': '⭐ Пульсар', 'desc': '350,000,000 коинов', 'stars': 70000, 'emoji': '⭐'},
    {'id': 58, 'cat': 'mega', 'title': '🌌 Квазар', 'desc': '400,000,000 коинов', 'stars': 80000, 'emoji': '🌌'},
    {'id': 59, 'cat': 'mega', 'title': '🌟 Чёрная дыра', 'desc': '450,000,000 коинов', 'stars': 90000, 'emoji': '🌟'},
    {'id': 60, 'cat': 'mega', 'title': '⭐ Большой взрыв', 'desc': '500,000,000 коинов', 'stars': 100000, 'emoji': '⭐'},
]

# Styling per category
category_styles = {
    'starter': {
        'bg': 'rgba(102,126,234,0.3),rgba(118,75,162,0.3)',
        'border': 'rgba(102,126,234,0.6)',
        'shadow': 'rgba(102,126,234,0.3)',
        'btn': '#667eea,#764ba2',
        'btnShadow': 'rgba(102,126,234,0.4)',
    },
    'premium': {
        'bg': 'rgba(234,179,8,0.3),rgba(251,191,36,0.3)',
        'border': 'rgba(234,179,8,0.6)',
        'shadow': 'rgba(234,179,8,0.3)',
        'btn': '#f59e0b,#d97706',
        'btnShadow': 'rgba(234,179,8,0.3)',
    },
    'vip': {
        'bg': 'rgba(255,215,0,0.3),rgba(255,255,100,0.3)',
        'border': 'rgba(255,215,0,0.6)',
        'shadow': 'rgba(255,215,0,0.4)',
        'btn': '#ffd700,#ffff66',
        'btnShadow': 'rgba(255,215,0,0.5)',
    },
    'limited': {
        'bg': 'rgba(255,0,0,0.3),rgba(255,100,100,0.3)',
        'border': 'rgba(255,0,0,0.6)',
        'shadow': 'rgba(255,0,0,0.4)',
        'btn': '#ff0000,#ff4444',
        'btnShadow': 'rgba(255,0,0,0.5)',
    },
    'ultra': {
        'bg': 'rgba(128,0,128,0.3),rgba(200,100,200,0.3)',
        'border': 'rgba(128,0,128,0.6)',
        'shadow': 'rgba(128,0,128,0.4)',
        'btn': '#800080,#a000a0',
        'btnShadow': 'rgba(128,0,128,0.6)',
    },
    'mega': {
        'bg': 'rgba(0,150,255,0.3),rgba(100,200,255,0.3)',
        'border': 'rgba(0,150,255,0.6)',
        'shadow': 'rgba(0,150,255,0.4)',
        'btn': '#00c8ff,#0096ff',
        'btnShadow': 'rgba(0,200,255,0.6)',
    },
}

# Generate HTML
html = []
current_cat = None

for p in products:
    if current_cat != p['cat']:
        # Category header
        category_titles = {
            'starter': '🎯 СТАРТОВЫЕ НАБОРЫ',
            'premium': '🚀 ПРЕМИУМ НАБОРЫ',
            'vip': '👑 VIP КОЛЛЕКЦИИ',
            'limited': '🔥 ОГРАНИЧЕННЫЕ ПРЕДЛОЖЕНИЯ',
            'ultra': '💎 УЛЬТРА НАБОРЫ',
            'mega': '🚀 МЕГА НАБОРЫ',
        }
        html.append(f'''                        <!-- CATEGORY: {p['cat'].upper()} -->
                        <div data-category="{p['cat']}" style="display:block;text-align:center;font-size:16px;font-weight:700;color:#fff;margin:8px 0 4px;text-shadow:0 0 15px rgba(102,126,234,0.5);">{category_titles[p['cat']]}</div>''')
        current_cat = p['cat']
    
    style = category_styles[p['cat']]
    # Small compact card
    card_html = f'''                        
                        <div data-category="{p['cat']}" style="background:linear-gradient(135deg,{style['bg']});padding:12px;border-radius:12px;border:2px solid {style['border']};box-shadow:0 0 20px {style['shadow']};margin-bottom:8px;">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                                <div>
                                    <div style="font-size:14px;font-weight:700;color:#fff;">{p['title']}</div>
                                    <div style="font-size:10px;color:#94a3b8;">{p['desc']}</div>
                                </div>
                                <div style="font-size:22px;">{p['emoji']}</div>
                            </div>
                            <button onclick="window.open('https://t.me/qanexus_bot?start=buy_stars_{p['id']}')" style="width:100%;padding:10px;background:linear-gradient(135deg,{style['btn']});color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:700;font-size:12px;margin-top:6px;box-shadow:0 4px 12px {style['btnShadow']};">
                                💰 Купить за {p['stars']} ⭐
                            </button>
                        </div>'''
    html.append(card_html)

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print('\n'.join(html))

