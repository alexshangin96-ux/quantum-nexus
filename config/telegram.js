const TelegramBot = require('node-telegram-bot-api');

// Токен бота
const token = '8426192106:AAGGlkfOYAhaQKPp-bcL-3oHXBE50tzAMog';

// Создаем экземпляр бота
const bot = new TelegramBot(token, { polling: true });

// Хранилище данных пользователей
const userData = {};

// Система достижений
const achievements = {
    first_tap: { name: '🎯 Первый тап', description: 'Сделайте первый тап', reward: 100, stars: 0 },
    level_5: { name: '⭐ Уровень 5', description: 'Достигните 5 уровня', reward: 500, stars: 0 },
    level_10: { name: '🌟 Уровень 10', description: 'Достигните 10 уровня', reward: 1000, stars: 0 },
    level_25: { name: '💎 Уровень 25', description: 'Достигните 25 уровня', reward: 2500, stars: 0 },
    level_50: { name: '👑 Уровень 50', description: 'Достигните 50 уровня', reward: 5000, stars: 0 },
    level_100: { name: '🏆 Уровень 100', description: 'Достигните 100 уровня', reward: 10000, stars: 0 },
    bitcoin_0_01: { name: '₿ Bitcoin коллекционер', description: 'Накопите 0.01 Bitcoin', reward: 2000, stars: 0 },
    bitcoin_0_1: { name: '₿ Bitcoin миллионер', description: 'Накопите 0.1 Bitcoin', reward: 10000, stars: 0 },
    taps_1000: { name: '🎯 Тапер', description: 'Сделайте 1000 тапов', reward: 1500, stars: 0 },
    taps_10000: { name: '🎯 Мастер тапов', description: 'Сделайте 10000 тапов', reward: 8000, stars: 0 },
    taps_50000: { name: '🎯 Легенда тапов', description: 'Сделайте 50000 тапов', reward: 25000, stars: 0 },
    multiplier_10: { name: '⚡ Множитель x10', description: 'Достигните множителя x10', reward: 3000, stars: 0 },
    multiplier_50: { name: '⚡ Множитель x50', description: 'Достигните множителя x50', reward: 15000, stars: 0 },
    coins_100000: { name: '💰 Богач', description: 'Накопите 100000 монет', reward: 5000, stars: 0 },
    coins_1000000: { name: '💰 Миллионер', description: 'Накопите 1000000 монет', reward: 20000, stars: 0 },
    energy_500: { name: '⚡ Энергетик', description: 'Достигните 500 энергии', reward: 2000, stars: 0 },
    energy_1000: { name: '⚡ Энергетический титан', description: 'Достигните 1000 энергии', reward: 8000, stars: 0 },
    daily_player: { name: '📅 Ежедневный игрок', description: 'Играйте 7 дней подряд', reward: 1000, stars: 0 },
    weekly_player: { name: '📅 Недельный игрок', description: 'Играйте 30 дней подряд', reward: 5000, stars: 0 },
    monthly_player: { name: '📅 Месячный игрок', description: 'Играйте 100 дней подряд', reward: 15000, stars: 0 },
    vip_member: { name: '💎 VIP участник', description: 'Станьте VIP участником', reward: 0, stars: 100 },
    premium_player: { name: '👑 Премиум игрок', description: 'Станьте премиум игроком', reward: 0, stars: 500 },
    legend_player: { name: '🏆 Легендарный игрок', description: 'Станьте легендарным игроком', reward: 0, stars: 1000 }
};

// Система бустеров
const boosters = {
    double_coins: { name: '💰 x2 Монеты', description: 'Удваивает монеты на 1 час', price: 1000, stars: 0, duration: 3600000 },
    triple_coins: { name: '💰 x3 Монеты', description: 'Утраивает монеты на 30 минут', price: 2500, stars: 0, duration: 1800000 },
    infinite_energy: { name: '⚡ Бесконечная энергия', description: 'Бесконечная энергия на 1 час', price: 5000, stars: 0, duration: 3600000 },
    auto_tap: { name: '🤖 Авто-тап', description: 'Автоматические тапы на 30 минут', price: 3000, stars: 0, duration: 1800000 },
    lucky_tap: { name: '🍀 Счастливый тап', description: 'Шанс получить x10 монет на 1 час', price: 2000, stars: 0, duration: 3600000 },
    mega_multiplier: { name: '🚀 Мега множитель', description: 'x5 множитель на 1 час', price: 0, stars: 50, duration: 3600000 },
    quantum_boost: { name: '⚛️ Квантовый буст', description: 'x10 множитель на 30 минут', price: 0, stars: 100, duration: 1800000 },
    cosmic_power: { name: '🌌 Космическая сила', description: 'x20 множитель на 15 минут', price: 0, stars: 200, duration: 900000 },
    divine_blessing: { name: '✨ Божественное благословение', description: 'x50 множитель на 10 минут', price: 0, stars: 500, duration: 600000 }
};

// Система подписок
const subscriptions = {
    vip: { name: '💎 VIP', description: 'VIP статус на 7 дней', price: 0, stars: 100, benefits: ['+50% монет', '+25% энергии', 'Эксклюзивные бустеры'] },
    premium: { name: '👑 Premium', description: 'Premium статус на 30 дней', price: 0, stars: 500, benefits: ['+100% монет', '+50% энергии', 'Все бустеры', 'Приоритетная поддержка'] },
    legend: { name: '🏆 Legend', description: 'Legend статус на 90 дней', price: 0, stars: 1000, benefits: ['+200% монет', '+100% энергии', 'Все бустеры', 'Эксклюзивные достижения', 'Персональный менеджер'] }
};

// Система одноразовых акций
const limitedOffers = {
    mega_pack: { 
        name: '🎁 Мега Пакет', 
        description: 'x100 множитель + 100000 монет + 1000 энергии на 24 часа', 
        stars: 200, 
        duration: 86400000,
        benefits: {
            multiplier: 100,
            coins: 100000,
            energy: 1000,
            maxEnergy: 1000
        }
    },
    cosmic_bundle: { 
        name: '🌌 Космический Бандл', 
        description: 'x500 множитель + 500000 монет + 5000 энергии на 24 часа', 
        stars: 500, 
        duration: 86400000,
        benefits: {
            multiplier: 500,
            coins: 500000,
            energy: 5000,
            maxEnergy: 5000
        }
    },
    divine_package: { 
        name: '✨ Божественный Пакет', 
        description: 'x1000 множитель + 1000000 монет + 10000 энергии на 24 часа', 
        stars: 1000, 
        duration: 86400000,
        benefits: {
            multiplier: 1000,
            coins: 1000000,
            energy: 10000,
            maxEnergy: 10000
        }
    },
    quantum_supreme: { 
        name: '⚛️ Квантовый Суприм', 
        description: 'x2000 множитель + 2000000 монет + 20000 энергии на 24 часа', 
        stars: 2000, 
        duration: 86400000,
        benefits: {
            multiplier: 2000,
            coins: 2000000,
            energy: 20000,
            maxEnergy: 20000
        }
    },
    ultimate_power: { 
        name: '🏆 Ультимат Пауэр', 
        description: 'x5000 множитель + 5000000 монет + 50000 энергии на 24 часа', 
        stars: 5000, 
        duration: 86400000,
        benefits: {
            multiplier: 5000,
            coins: 5000000,
            energy: 50000,
            maxEnergy: 50000
        }
    },
    legendary_boost: { 
        name: '👑 Легендарный Буст', 
        description: 'x10000 множитель + 10000000 монет + 100000 энергии на 24 часа', 
        stars: 10000, 
        duration: 86400000,
        benefits: {
            multiplier: 10000,
            coins: 10000000,
            energy: 100000,
            maxEnergy: 100000
        }
    }
};

// Команда /start
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const username = msg.from.username || msg.from.first_name || 'user_' + msg.from.id;
    
    if (!userData[chatId]) {
        userData[chatId] = {
            username: username,
            gameData: {
                totalTaps: 0,
                coins: 0,
                level: 1,
                bitcoin: 0,
                multiplier: 1,
                energy: 100,
                maxEnergy: 100,
                achievements: [],
                lastEnergyUpdate: Date.now(),
                lastDailyReward: 0,
                consecutiveDays: 0,
                boosters: {},
                prestige: 0,
                prestigePoints: 0,
                lastPrestige: 0,
                stars: 0,
                subscription: null,
                subscriptionExpiry: 0,
                vipLevel: 0,
                premiumLevel: 0,
                legendLevel: 0,
                lastAutoTap: 0,
                autoTapLevel: 0,
                lastQuantumBoost: 0,
                quantumBoostLevel: 0,
                lastCosmicPower: 0,
                cosmicPowerLevel: 0,
                lastDivineBlessing: 0,
                divineBlessingLevel: 0,
                lastMegaMultiplier: 0,
                megaMultiplierLevel: 0,
                lastInfiniteEnergy: 0,
                infiniteEnergyLevel: 0,
                lastLuckyTap: 0,
                luckyTapLevel: 0,
                lastTripleCoins: 0,
                tripleCoinsLevel: 0,
                lastDoubleCoins: 0,
                doubleCoinsLevel: 0,
                lastAutoTap: 0,
                autoTapLevel: 0,
                limitedOffers: {},
                lastLimitedOffer: 0
            }
        };
    }
    
    const user = userData[chatId];
    const welcomeMessage = `
🚀 **QUANTUM NEXUS** - Квантовая Игра

👤 **Игрок:** ${user.username}
💰 **Монеты:** ${Math.floor(user.gameData.coins).toLocaleString()}
📈 **Уровень:** ${user.gameData.level}
₿ **Bitcoin:** ${user.gameData.bitcoin.toFixed(3)}
⚡ **Множитель:** ${user.gameData.multiplier.toFixed(1)}x
⚡ **Энергия:** ${user.gameData.energy}/${user.gameData.maxEnergy}
👑 **Престиж:** ${user.gameData.prestige}
⭐ **Звезды:** ${user.gameData.stars}

${user.gameData.subscription ? `💎 **Подписка:** ${user.gameData.subscription}` : ''}
${Object.keys(user.gameData.limitedOffers).length > 0 ? `🎁 **Активные акции:** ${Object.keys(user.gameData.limitedOffers).join(', ')}` : ''}

🎯 **Цель:** Тапайте для получения монет и повышения уровня!

**Выберите действие:**
    `;
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🎯 Играть', callback_data: 'play_game' },
                { text: '📊 Статистика', callback_data: 'show_stats' }
            ],
            [
                { text: '🏆 Достижения', callback_data: 'show_achievements' },
                { text: '🛒 Магазин', callback_data: 'show_shop' }
            ],
            [
                { text: '🎁 Ежедневная награда', callback_data: 'daily_reward' },
                { text: '👑 Престиж', callback_data: 'show_prestige' }
            ],
            [
                { text: '⭐ Звезды', callback_data: 'show_stars' },
                { text: '💎 Подписки', callback_data: 'show_subscriptions' }
            ],
            [
                { text: '🔥 Ограниченные акции', callback_data: 'show_limited_offers' }
            ],
            [
                { text: '🔄 Сбросить данные', callback_data: 'reset_data' }
            ]
        ]
    };
    
    bot.sendMessage(chatId, welcomeMessage, { 
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
});

// Обработка нажатий на кнопки
bot.on('callback_query', async (callbackQuery) => {
    const message = callbackQuery.message;
    const chatId = message.chat.id;
    const data = callbackQuery.data;
    
    if (!userData[chatId]) {
        userData[chatId] = {
            username: message.from.username || message.from.first_name || 'user_' + message.from.id,
            gameData: {
                totalTaps: 0,
                coins: 0,
                level: 1,
                bitcoin: 0,
                multiplier: 1,
                energy: 100,
                maxEnergy: 100,
                achievements: [],
                lastEnergyUpdate: Date.now(),
                lastDailyReward: 0,
                consecutiveDays: 0,
                boosters: {},
                prestige: 0,
                prestigePoints: 0,
                lastPrestige: 0,
                stars: 0,
                subscription: null,
                subscriptionExpiry: 0,
                vipLevel: 0,
                premiumLevel: 0,
                legendLevel: 0,
                lastAutoTap: 0,
                autoTapLevel: 0,
                lastQuantumBoost: 0,
                quantumBoostLevel: 0,
                lastCosmicPower: 0,
                cosmicPowerLevel: 0,
                lastDivineBlessing: 0,
                divineBlessingLevel: 0,
                lastMegaMultiplier: 0,
                megaMultiplierLevel: 0,
                lastInfiniteEnergy: 0,
                infiniteEnergyLevel: 0,
                lastLuckyTap: 0,
                luckyTapLevel: 0,
                lastTripleCoins: 0,
                tripleCoinsLevel: 0,
                lastDoubleCoins: 0,
                doubleCoinsLevel: 0,
                lastAutoTap: 0,
                autoTapLevel: 0,
                limitedOffers: {},
                lastLimitedOffer: 0
            }
        };
    }
    
    switch (data) {
        case 'play_game':
            await playGame(chatId, message);
            break;
        case 'show_stats':
            showStats(chatId, message);
            break;
        case 'show_achievements':
            showAchievements(chatId, message);
            break;
        case 'show_shop':
            showShop(chatId, message);
            break;
        case 'daily_reward':
            claimDailyReward(chatId, message);
            break;
        case 'show_prestige':
            showPrestige(chatId, message);
            break;
        case 'show_stars':
            showStars(chatId, message);
            break;
        case 'show_subscriptions':
            showSubscriptions(chatId, message);
            break;
        case 'show_limited_offers':
            showLimitedOffers(chatId, message);
            break;
        case 'reset_data':
            resetData(chatId, message);
            break;
        case 'tap':
            await tap(chatId, message);
            break;
        case 'buy_multiplier':
            buyMultiplier(chatId, message);
            break;
        case 'buy_energy':
            buyEnergy(chatId, message);
            break;
        case 'buy_booster':
            showBoosters(chatId, message);
            break;
        case 'prestige':
            doPrestige(chatId, message);
            break;
        case 'main_menu':
            showMainMenu(chatId, message);
            break;
    }
    
    bot.answerCallbackQuery(callbackQuery.id);
});

// Функция игры
async function playGame(chatId, message) {
    const user = userData[chatId];
    updateEnergy(user);
    updateBoosters(user);
    updateAutoTap(user);
    updateLimitedOffers(user);
    
    const gameMessage = `
🎮 **QUANTUM NEXUS**

👤 **Игрок:** ${user.username}
💰 **Монеты:** ${Math.floor(user.gameData.coins).toLocaleString()}
📈 **Уровень:** ${user.gameData.level}
₿ **Bitcoin:** ${user.gameData.bitcoin.toFixed(3)}
⚡ **Множитель:** ${user.gameData.multiplier.toFixed(1)}x
⚡ **Энергия:** ${user.gameData.energy}/${user.gameData.maxEnergy}
👑 **Престиж:** ${user.gameData.prestige}
⭐ **Звезды:** ${user.gameData.stars}

${user.gameData.subscription ? `💎 **Подписка:** ${user.gameData.subscription}` : ''}
${Object.keys(user.gameData.limitedOffers).length > 0 ? `🎁 **Активные акции:** ${Object.keys(user.gameData.limitedOffers).join(', ')}` : ''}

${user.gameData.energy > 0 ? '🎯 **Нажмите "Тап" чтобы получить монеты!**' : '⚠️ **Недостаточно энергии! Подождите восстановления.**'}

${Object.keys(user.gameData.boosters).length > 0 ? '🔥 **Активные бустеры:** ' + Object.keys(user.gameData.boosters).join(', ') : ''}
    `;
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🎯 ТАП', callback_data: 'tap' },
                { text: '📊 Статистика', callback_data: 'show_stats' }
            ],
            [
                { text: '🏆 Достижения', callback_data: 'show_achievements' },
                { text: '🛒 Магазин', callback_data: 'show_shop' }
            ],
            [
                { text: '🎁 Ежедневная награда', callback_data: 'daily_reward' },
                { text: '👑 Престиж', callback_data: 'show_prestige' }
            ],
            [
                { text: '⭐ Звезды', callback_data: 'show_stars' },
                { text: '💎 Подписки', callback_data: 'show_subscriptions' }
            ],
            [
                { text: '🔥 Ограниченные акции', callback_data: 'show_limited_offers' }
            ],
            [
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(gameMessage, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция тапа
async function tap(chatId, message) {
    const user = userData[chatId];
    updateEnergy(user);
    updateBoosters(user);
    updateAutoTap(user);
    updateLimitedOffers(user);
    
    if (user.gameData.energy <= 0) {
        bot.answerCallbackQuery(message.id, { text: 'Недостаточно энергии!' });
        return;
    }
    
    user.gameData.totalTaps++;
    
    // Расчет монет с учетом бустеров, подписок и акций
    let coinsEarned = user.gameData.multiplier;
    if (user.gameData.boosters.double_coins) coinsEarned *= 2;
    if (user.gameData.boosters.triple_coins) coinsEarned *= 3;
    if (user.gameData.boosters.mega_multiplier) coinsEarned *= 5;
    if (user.gameData.boosters.quantum_boost) coinsEarned *= 10;
    if (user.gameData.boosters.cosmic_power) coinsEarned *= 20;
    if (user.gameData.boosters.divine_blessing) coinsEarned *= 50;
    if (user.gameData.boosters.lucky_tap && Math.random() < 0.1) coinsEarned *= 10;
    
    // Бонусы от подписок
    if (user.gameData.subscription === 'vip') coinsEarned *= 1.5;
    if (user.gameData.subscription === 'premium') coinsEarned *= 2;
    if (user.gameData.subscription === 'legend') coinsEarned *= 3;
    
    // Бонусы от ограниченных акций
    Object.keys(user.gameData.limitedOffers).forEach(offerId => {
        const offer = limitedOffers[offerId];
        if (offer.benefits.multiplier) {
            coinsEarned *= offer.benefits.multiplier;
        }
    });
    
    user.gameData.coins += coinsEarned;
    user.gameData.energy--;
    
    // Проверка уровня
    const newLevel = Math.floor(user.gameData.totalTaps / 100) + 1;
    if (newLevel > user.gameData.level) {
        user.gameData.level = newLevel;
        user.gameData.multiplier += 0.1;
        user.gameData.maxEnergy += 10;
        user.gameData.energy = user.gameData.maxEnergy;
        
        bot.answerCallbackQuery(message.id, { text: `🎉 Новый уровень ${user.gameData.level}!` });
    }
    
    // Проверка Bitcoin
    if (user.gameData.totalTaps % 1000 === 0) {
        user.gameData.bitcoin += 0.001;
        bot.answerCallbackQuery(message.id, { text: '₿ Получен Bitcoin!' });
    }
    
    // Проверка достижений
    checkAchievements(user);
    
    // Сохраняем данные на сервере
    try {
        const response = await fetch(`http://localhost:3000/api/game/${user.username}/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user.gameData)
        });
        
        if (response.ok) {
            console.log('Данные сохранены для пользователя:', user.username);
        }
    } catch (error) {
        console.error('Ошибка сохранения данных:', error);
    }
    
    // Обновляем интерфейс
    await playGame(chatId, message);
}

// Функция показа ограниченных акций
function showLimitedOffers(chatId, message) {
    const user = userData[chatId];
    
    let offersText = '🔥 **Ограниченные акции**\n\n';
    offersText += '**Супер-выгодные предложения на 24 часа!**\n\n';
    
    Object.keys(limitedOffers).forEach(offerId => {
        const offer = limitedOffers[offerId];
        offersText += `**${offer.name}**\n${offer.description}\n⭐ Цена: ${offer.stars} звезд\n\n`;
    });
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🎁 Мега Пакет (200⭐)', callback_data: 'buy_offer_mega_pack' },
                { text: '🌌 Космический Бандл (500⭐)', callback_data: 'buy_offer_cosmic_bundle' }
            ],
            [
                { text: '✨ Божественный Пакет (1000⭐)', callback_data: 'buy_offer_divine_package' },
                { text: '⚛️ Квантовый Суприм (2000⭐)', callback_data: 'buy_offer_quantum_supreme' }
            ],
            [
                { text: '🏆 Ультимат Пауэр (5000⭐)', callback_data: 'buy_offer_ultimate_power' },
                { text: '👑 Легендарный Буст (10000⭐)', callback_data: 'buy_offer_legendary_boost' }
            ],
            [
                { text: '⭐ Звезды', callback_data: 'show_stars' },
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(offersText, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция покупки ограниченной акции
function buyLimitedOffer(chatId, message, offerId) {
    const user = userData[chatId];
    const offer = limitedOffers[offerId];
    
    if (user.gameData.stars >= offer.stars) {
        user.gameData.stars -= offer.stars;
        user.gameData.limitedOffers[offerId] = Date.now() + offer.duration;
        
        // Применяем бонусы
        if (offer.benefits.coins) {
            user.gameData.coins += offer.benefits.coins;
        }
        if (offer.benefits.energy) {
            user.gameData.energy = Math.min(user.gameData.maxEnergy, user.gameData.energy + offer.benefits.energy);
        }
        if (offer.benefits.maxEnergy) {
            user.gameData.maxEnergy = Math.max(user.gameData.maxEnergy, offer.benefits.maxEnergy);
        }
        
        const offerMessage = `
🎁 **${offer.name} активирована!**

💰 **Получено монет:** ${offer.benefits.coins ? offer.benefits.coins.toLocaleString() : 0}
⚡ **Энергия:** ${offer.benefits.energy ? offer.benefits.energy : 0}
⚡ **Максимальная энергия:** ${offer.benefits.maxEnergy ? offer.benefits.maxEnergy : 0}
⚡ **Множитель:** x${offer.benefits.multiplier ? offer.benefits.multiplier : 1}

**Акция действует 24 часа!**
        `;
        
        const keyboard = {
            inline_keyboard: [
                [
                    { text: '🎮 Играть', callback_data: 'play_game' },
                    { text: '📊 Статистика', callback_data: 'show_stats' }
                ],
                [
                    { text: '🏠 Главное меню', callback_data: 'main_menu' }
                ]
            ]
        };
        
        bot.editMessageText(offerMessage, {
            chat_id: chatId,
            message_id: message.message_id,
            reply_markup: keyboard,
            parse_mode: 'Markdown'
        });
    } else {
        bot.answerCallbackQuery(message.id, { text: '❌ Недостаточно звезд!' });
    }
}

// Функция показа статистики
function showStats(chatId, message) {
    const user = userData[chatId];
    updateEnergy(user);
    
    const statsMessage = `
📊 **Статистика игрока** ${user.username}

🎯 **Всего тапов:** ${user.gameData.totalTaps.toLocaleString()}
💰 **Монеты:** ${Math.floor(user.gameData.coins).toLocaleString()}
📈 **Уровень:** ${user.gameData.level}
₿ **Bitcoin:** ${user.gameData.bitcoin.toFixed(3)}
⚡ **Множитель:** ${user.gameData.multiplier.toFixed(1)}x
⚡ **Энергия:** ${user.gameData.energy}/${user.gameData.maxEnergy}
👑 **Престиж:** ${user.gameData.prestige}
⭐ **Звезды:** ${user.gameData.stars}
🏆 **Достижения:** ${user.gameData.achievements.length}/${Object.keys(achievements).length}

📅 **Дней подряд:** ${user.gameData.consecutiveDays}
${user.gameData.subscription ? `💎 **Подписка:** ${user.gameData.subscription}` : ''}
${Object.keys(user.gameData.limitedOffers).length > 0 ? `🎁 **Активные акции:** ${Object.keys(user.gameData.limitedOffers).join(', ')}` : ''}
    `;
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🎮 Играть', callback_data: 'play_game' },
                { text: '🏆 Достижения', callback_data: 'show_achievements' }
            ],
            [
                { text: '🛒 Магазин', callback_data: 'show_shop' },
                { text: '👑 Престиж', callback_data: 'show_prestige' }
            ],
            [
                { text: '⭐ Звезды', callback_data: 'show_stars' },
                { text: '💎 Подписки', callback_data: 'show_subscriptions' }
            ],
            [
                { text: '🔥 Ограниченные акции', callback_data: 'show_limited_offers' }
            ],
            [
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(statsMessage, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция показа достижений
function showAchievements(chatId, message) {
    const user = userData[chatId];
    
    let achievementsText = '🏆 **Достижения**\n\n';
    
    Object.keys(achievements).forEach(achievementId => {
        const achievement = achievements[achievementId];
        const isUnlocked = user.gameData.achievements.includes(achievementId);
        const status = isUnlocked ? '✅' : '❌';
        achievementsText += `${status} **${achievement.name}**\n${achievement.description}\n💰 Награда: ${achievement.reward} монет`;
        if (achievement.stars > 0) {
            achievementsText += ` + ${achievement.stars} ⭐`;
        }
        achievementsText += '\n\n';
    });
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🎮 Играть', callback_data: 'play_game' },
                { text: '📊 Статистика', callback_data: 'show_stats' }
            ],
            [
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(achievementsText, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция показа магазина
function showShop(chatId, message) {
    const user = userData[chatId];
    
    const shopMessage = `
🛒 **Магазин Quantum Nexus**

💰 **Ваши монеты:** ${Math.floor(user.gameData.coins).toLocaleString()}
⭐ **Ваши звезды:** ${user.gameData.stars}

**Доступные покупки:**

🔢 **Увеличить множитель** - 1000 монет
⚡ **Восстановить энергию** - 500 монет
🎁 **Бустеры** - Различные цены
    `;
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🔢 Увеличить множитель (1000)', callback_data: 'buy_multiplier' },
                { text: '⚡ Восстановить энергию (500)', callback_data: 'buy_energy' }
            ],
            [
                { text: '🎁 Бустеры', callback_data: 'buy_booster' }
            ],
            [
                { text: '🎮 Играть', callback_data: 'play_game' },
                { text: '📊 Статистика', callback_data: 'show_stats' }
            ],
            [
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(shopMessage, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция показа бустеров
function showBoosters(chatId, message) {
    const user = userData[chatId];
    
    let boostersText = '🎁 **Бустеры**\n\n';
    
    Object.keys(boosters).forEach(boosterId => {
        const booster = boosters[boosterId];
        boostersText += `**${booster.name}**\n${booster.description}\n`;
        if (booster.price > 0) {
            boostersText += `💰 Цена: ${booster.price} монет\n\n`;
        } else {
            boostersText += `⭐ Цена: ${booster.stars} звезд\n\n`;
        }
    });
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '💰 x2 Монеты (1000)', callback_data: 'buy_booster_double_coins' },
                { text: '💰 x3 Монеты (2500)', callback_data: 'buy_booster_triple_coins' }
            ],
            [
                { text: '⚡ Бесконечная энергия (5000)', callback_data: 'buy_booster_infinite_energy' },
                { text: '🤖 Авто-тап (3000)', callback_data: 'buy_booster_auto_tap' }
            ],
            [
                { text: '🍀 Счастливый тап (2000)', callback_data: 'buy_booster_lucky_tap' }
            ],
            [
                { text: '🚀 Мега множитель (50⭐)', callback_data: 'buy_booster_mega_multiplier' },
                { text: '⚛️ Квантовый буст (100⭐)', callback_data: 'buy_booster_quantum_boost' }
            ],
            [
                { text: '🌌 Космическая сила (200⭐)', callback_data: 'buy_booster_cosmic_power' },
                { text: '✨ Божественное благословение (500⭐)', callback_data: 'buy_booster_divine_blessing' }
            ],
            [
                { text: '🛒 Магазин', callback_data: 'show_shop' },
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(boostersText, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция показа звезд
function showStars(chatId, message) {
    const user = userData[chatId];
    
    const starsMessage = `
⭐ **Звезды Telegram**

**Ваши звезды:** ${user.gameData.stars}

**Звезды можно получить:**
• Покупка в Telegram
• Достижения
• Ежедневные награды
• Престиж

**Звезды можно потратить на:**
• Премиум бустеры
• Подписки
• Ограниченные акции
• Эксклюзивные функции
    `;
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🎁 Бустеры', callback_data: 'buy_booster' },
                { text: '💎 Подписки', callback_data: 'show_subscriptions' }
            ],
            [
                { text: '🔥 Ограниченные акции', callback_data: 'show_limited_offers' }
            ],
            [
                { text: '🎮 Играть', callback_data: 'play_game' },
                { text: '📊 Статистика', callback_data: 'show_stats' }
            ],
            [
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(starsMessage, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция показа подписок
function showSubscriptions(chatId, message) {
    const user = userData[chatId];
    
    let subscriptionsText = '💎 **Подписки**\n\n';
    
    Object.keys(subscriptions).forEach(subscriptionId => {
        const subscription = subscriptions[subscriptionId];
        subscriptionsText += `**${subscription.name}**\n${subscription.description}\n⭐ Цена: ${subscription.stars} звезд\n`;
        subscriptionsText += `**Преимущества:**\n`;
        subscription.benefits.forEach(benefit => {
            subscriptionsText += `• ${benefit}\n`;
        });
        subscriptionsText += '\n';
    });
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '💎 VIP (100⭐)', callback_data: 'buy_subscription_vip' },
                { text: '👑 Premium (500⭐)', callback_data: 'buy_subscription_premium' }
            ],
            [
                { text: '🏆 Legend (1000⭐)', callback_data: 'buy_subscription_legend' }
            ],
            [
                { text: '⭐ Звезды', callback_data: 'show_stars' },
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(subscriptionsText, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция ежедневной награды
function claimDailyReward(chatId, message) {
    const user = userData[chatId];
    const now = Date.now();
    const dayInMs = 24 * 60 * 60 * 1000;
    
    if (now - user.gameData.lastDailyReward >= dayInMs) {
        const reward = 1000 + (user.gameData.consecutiveDays * 100);
        const starsReward = Math.floor(reward / 1000);
        user.gameData.coins += reward;
        user.gameData.stars += starsReward;
        user.gameData.consecutiveDays++;
        user.gameData.lastDailyReward = now;
        
        const rewardMessage = `
🎁 **Ежедневная награда получена!**

💰 **Награда:** ${reward} монет
⭐ **Звезды:** ${starsReward}
📅 **Дней подряд:** ${user.gameData.consecutiveDays}

**Приходите завтра за большей наградой!**
        `;
        
        const keyboard = {
            inline_keyboard: [
                [
                    { text: '🎮 Играть', callback_data: 'play_game' },
                    { text: '📊 Статистика', callback_data: 'show_stats' }
                ],
                [
                    { text: '🏠 Главное меню', callback_data: 'main_menu' }
                ]
            ]
        };
        
        bot.editMessageText(rewardMessage, {
            chat_id: chatId,
            message_id: message.message_id,
            reply_markup: keyboard,
            parse_mode: 'Markdown'
        });
    } else {
        const timeLeft = dayInMs - (now - user.gameData.lastDailyReward);
        const hoursLeft = Math.floor(timeLeft / (60 * 60 * 1000));
        const minutesLeft = Math.floor((timeLeft % (60 * 60 * 1000)) / (60 * 1000));
        
        bot.answerCallbackQuery(message.id, { text: `⏰ Следующая награда через ${hoursLeft}ч ${minutesLeft}м` });
    }
}

// Функция показа престижа
function showPrestige(chatId, message) {
    const user = userData[chatId];
    
    const prestigeMessage = `
👑 **Престиж**

**Текущий престиж:** ${user.gameData.prestige}
**Очки престижа:** ${user.gameData.prestigePoints}

**Престиж сбрасывает:**
• Уровень до 1
• Монеты до 0
• Множитель до 1

**Но дает:**
• +0.1x множитель за каждый престиж
• +10 энергии за каждый престиж
• Очки престижа для покупки улучшений
• Звезды за престиж

**Для престижа нужно:** 50 уровень
    `;
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '👑 Престиж', callback_data: 'prestige' }
            ],
            [
                { text: '🎮 Играть', callback_data: 'play_game' },
                { text: '📊 Статистика', callback_data: 'show_stats' }
            ],
            [
                { text: '🏠 Главное меню', callback_data: 'main_menu' }
            ]
        ]
    };
    
    bot.editMessageText(prestigeMessage, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция престижа
function doPrestige(chatId, message) {
    const user = userData[chatId];
    
    if (user.gameData.level >= 50) {
        user.gameData.prestige++;
        user.gameData.prestigePoints += user.gameData.level;
        user.gameData.stars += Math.floor(user.gameData.level / 10);
        user.gameData.level = 1;
        user.gameData.coins = 0;
        user.gameData.multiplier = 1 + (user.gameData.prestige * 0.1);
        user.gameData.maxEnergy = 100 + (user.gameData.prestige * 10);
        user.gameData.energy = user.gameData.maxEnergy;
        
        const prestigeMessage = `
👑 **Престиж выполнен!**

**Новый престиж:** ${user.gameData.prestige}
**Очки престижа:** ${user.gameData.prestigePoints}
**Звезды получены:** ${Math.floor(user.gameData.level / 10)}
**Новый множитель:** ${user.gameData.multiplier.toFixed(1)}x
**Новая энергия:** ${user.gameData.maxEnergy}

**Начните новое путешествие!**
        `;
        
        const keyboard = {
            inline_keyboard: [
                [
                    { text: '🎮 Играть', callback_data: 'play_game' },
                    { text: '📊 Статистика', callback_data: 'show_stats' }
                ],
                [
                    { text: '🏠 Главное меню', callback_data: 'main_menu' }
                ]
            ]
        };
        
        bot.editMessageText(prestigeMessage, {
            chat_id: chatId,
            message_id: message.message_id,
            reply_markup: keyboard,
            parse_mode: 'Markdown'
        });
    } else {
        bot.answerCallbackQuery(message.id, { text: '❌ Нужен 50 уровень для престижа!' });
    }
}

// Функция покупки множителя
function buyMultiplier(chatId, message) {
    const user = userData[chatId];
    
    if (user.gameData.coins >= 1000) {
        user.gameData.coins -= 1000;
        user.gameData.multiplier += 0.5;
        
        bot.answerCallbackQuery(message.id, { text: '✅ Множитель увеличен!' });
        showShop(chatId, message);
    } else {
        bot.answerCallbackQuery(message.id, { text: '❌ Недостаточно монет!' });
    }
}

// Функция покупки энергии
function buyEnergy(chatId, message) {
    const user = userData[chatId];
    
    if (user.gameData.coins >= 500) {
        user.gameData.coins -= 500;
        user.gameData.energy = user.gameData.maxEnergy;
        
        bot.answerCallbackQuery(message.id, { text: '✅ Энергия восстановлена!' });
        showShop(chatId, message);
    } else {
        bot.answerCallbackQuery(message.id, { text: '❌ Недостаточно монет!' });
    }
}

// Функция покупки бустера
function buyBooster(chatId, message, boosterId) {
    const user = userData[chatId];
    const booster = boosters[boosterId];
    
    if (booster.price > 0) {
        if (user.gameData.coins >= booster.price) {
            user.gameData.coins -= booster.price;
            user.gameData.boosters[boosterId] = Date.now() + booster.duration;
            
            bot.answerCallbackQuery(message.id, { text: `✅ ${booster.name} активирован!` });
            showBoosters(chatId, message);
        } else {
            bot.answerCallbackQuery(message.id, { text: '❌ Недостаточно монет!' });
        }
    } else {
        if (user.gameData.stars >= booster.stars) {
            user.gameData.stars -= booster.stars;
            user.gameData.boosters[boosterId] = Date.now() + booster.duration;
            
            bot.answerCallbackQuery(message.id, { text: `✅ ${booster.name} активирован!` });
            showBoosters(chatId, message);
        } else {
            bot.answerCallbackQuery(message.id, { text: '❌ Недостаточно звезд!' });
        }
    }
}

// Функция покупки подписки
function buySubscription(chatId, message, subscriptionId) {
    const user = userData[chatId];
    const subscription = subscriptions[subscriptionId];
    
    if (user.gameData.stars >= subscription.stars) {
        user.gameData.stars -= subscription.stars;
        user.gameData.subscription = subscriptionId;
        user.gameData.subscriptionExpiry = Date.now() + (subscriptionId === 'vip' ? 7 : subscriptionId === 'premium' ? 30 : 90) * 24 * 60 * 60 * 1000;
        
        bot.answerCallbackQuery(message.id, { text: `✅ ${subscription.name} активирована!` });
        showSubscriptions(chatId, message);
    } else {
        bot.answerCallbackQuery(message.id, { text: '❌ Недостаточно звезд!' });
    }
}

// Функция сброса данных
function resetData(chatId, message) {
    const user = userData[chatId];
    
    user.gameData = {
        totalTaps: 0,
        coins: 0,
        level: 1,
        bitcoin: 0,
        multiplier: 1,
        energy: 100,
        maxEnergy: 100,
        achievements: [],
        lastEnergyUpdate: Date.now(),
        lastDailyReward: 0,
        consecutiveDays: 0,
        boosters: {},
        prestige: 0,
        prestigePoints: 0,
        lastPrestige: 0,
        stars: 0,
        subscription: null,
        subscriptionExpiry: 0,
        vipLevel: 0,
        premiumLevel: 0,
        legendLevel: 0,
        lastAutoTap: 0,
        autoTapLevel: 0,
        lastQuantumBoost: 0,
        quantumBoostLevel: 0,
        lastCosmicPower: 0,
        cosmicPowerLevel: 0,
        lastDivineBlessing: 0,
        divineBlessingLevel: 0,
        lastMegaMultiplier: 0,
        megaMultiplierLevel: 0,
        lastInfiniteEnergy: 0,
        infiniteEnergyLevel: 0,
        lastLuckyTap: 0,
        luckyTapLevel: 0,
        lastTripleCoins: 0,
        tripleCoinsLevel: 0,
        lastDoubleCoins: 0,
        doubleCoinsLevel: 0,
        lastAutoTap: 0,
        autoTapLevel: 0,
        limitedOffers: {},
        lastLimitedOffer: 0
    };
    
    const resetMessage = `
🔄 **Данные сброшены!**

👤 **Игрок:** ${user.username}
💰 **Монеты:** 0
📈 **Уровень:** 1
⚡ **Энергия:** 100/100

🎯 **Нажмите "Играть" чтобы начать заново!**
    `;
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🎯 Играть', callback_data: 'play_game' },
                { text: '📊 Статистика', callback_data: 'show_stats' }
            ]
        ]
    };
    
    bot.editMessageText(resetMessage, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция главного меню
function showMainMenu(chatId, message) {
    const user = userData[chatId];
    
    const mainMessage = `
🚀 **QUANTUM NEXUS** - Квантовая Игра

👤 **Игрок:** ${user.username}
💰 **Монеты:** ${Math.floor(user.gameData.coins).toLocaleString()}
📈 **Уровень:** ${user.gameData.level}
⚡ **Энергия:** ${user.gameData.energy}/${user.gameData.maxEnergy}
👑 **Престиж:** ${user.gameData.prestige}
⭐ **Звезды:** ${user.gameData.stars}

${user.gameData.subscription ? `💎 **Подписка:** ${user.gameData.subscription}` : ''}
${Object.keys(user.gameData.limitedOffers).length > 0 ? `🎁 **Активные акции:** ${Object.keys(user.gameData.limitedOffers).join(', ')}` : ''}

**Выберите действие:**
    `;
    
    const keyboard = {
        inline_keyboard: [
            [
                { text: '🎯 Играть', callback_data: 'play_game' },
                { text: '📊 Статистика', callback_data: 'show_stats' }
            ],
            [
                { text: '🏆 Достижения', callback_data: 'show_achievements' },
                { text: '🛒 Магазин', callback_data: 'show_shop' }
            ],
            [
                { text: '🎁 Ежедневная награда', callback_data: 'daily_reward' },
                { text: '👑 Престиж', callback_data: 'show_prestige' }
            ],
            [
                { text: '⭐ Звезды', callback_data: 'show_stars' },
                { text: '💎 Подписки', callback_data: 'show_subscriptions' }
            ],
            [
                { text: '🔥 Ограниченные акции', callback_data: 'show_limited_offers' }
            ],
            [
                { text: '🔄 Сбросить данные', callback_data: 'reset_data' }
            ]
        ]
    };
    
    bot.editMessageText(mainMessage, {
        chat_id: chatId,
        message_id: message.message_id,
        reply_markup: keyboard,
        parse_mode: 'Markdown'
    });
}

// Функция обновления энергии
function updateEnergy(user) {
    const now = Date.now();
    const timePassed = now - user.gameData.lastEnergyUpdate;
    const energyToAdd = Math.floor(timePassed / 5000); // 1 энергия каждые 5 секунд
    
    if (energyToAdd > 0) {
        user.gameData.energy = Math.min(user.gameData.maxEnergy, user.gameData.energy + energyToAdd);
        user.gameData.lastEnergyUpdate = now;
    }
}

// Функция обновления бустеров
function updateBoosters(user) {
    const now = Date.now();
    Object.keys(user.gameData.boosters).forEach(boosterId => {
        if (now >= user.gameData.boosters[boosterId]) {
            delete user.gameData.boosters[boosterId];
        }
    });
}

// Функция обновления ограниченных акций
function updateLimitedOffers(user) {
    const now = Date.now();
    Object.keys(user.gameData.limitedOffers).forEach(offerId => {
        if (now >= user.gameData.limitedOffers[offerId]) {
            delete user.gameData.limitedOffers[offerId];
        }
    });
}

// Функция обновления авто-тапа
function updateAutoTap(user) {
    if (user.gameData.boosters.auto_tap) {
        const now = Date.now();
        const timePassed = now - user.gameData.lastAutoTap;
        
        if (timePassed >= 1000) { // Авто-тап каждую секунду
            user.gameData.totalTaps++;
            user.gameData.coins += user.gameData.multiplier;
            user.gameData.lastAutoTap = now;
        }
    }
}

// Функция проверки достижений
function checkAchievements(user) {
    Object.keys(achievements).forEach(achievementId => {
        if (!user.gameData.achievements.includes(achievementId)) {
            let condition = false;
            
            switch (achievementId) {
                case 'first_tap':
                    condition = user.gameData.totalTaps >= 1;
                    break;
                case 'level_5':
                    condition = user.gameData.level >= 5;
                    break;
                case 'level_10':
                    condition = user.gameData.level >= 10;
                    break;
                case 'level_25':
                    condition = user.gameData.level >= 25;
                    break;
                case 'level_50':
                    condition = user.gameData.level >= 50;
                    break;
                case 'level_100':
                    condition = user.gameData.level >= 100;
                    break;
                case 'bitcoin_0_01':
                    condition = user.gameData.bitcoin >= 0.01;
                    break;
                case 'bitcoin_0_1':
                    condition = user.gameData.bitcoin >= 0.1;
                    break;
                case 'taps_1000':
                    condition = user.gameData.totalTaps >= 1000;
                    break;
                case 'taps_10000':
                    condition = user.gameData.totalTaps >= 10000;
                    break;
                case 'taps_50000':
                    condition = user.gameData.totalTaps >= 50000;
                    break;
                case 'multiplier_10':
                    condition = user.gameData.multiplier >= 10;
                    break;
                case 'multiplier_50':
                    condition = user.gameData.multiplier >= 50;
                    break;
                case 'coins_100000':
                    condition = user.gameData.coins >= 100000;
                    break;
                case 'coins_1000000':
                    condition = user.gameData.coins >= 1000000;
                    break;
                case 'energy_500':
                    condition = user.gameData.maxEnergy >= 500;
                    break;
                case 'energy_1000':
                    condition = user.gameData.maxEnergy >= 1000;
                    break;
                case 'daily_player':
                    condition = user.gameData.consecutiveDays >= 7;
                    break;
                case 'weekly_player':
                    condition = user.gameData.consecutiveDays >= 30;
                    break;
                case 'monthly_player':
                    condition = user.gameData.consecutiveDays >= 100;
                    break;
                case 'vip_member':
                    condition = user.gameData.subscription === 'vip';
                    break;
                case 'premium_player':
                    condition = user.gameData.subscription === 'premium';
                    break;
                case 'legend_player':
                    condition = user.gameData.subscription === 'legend';
                    break;
            }
            
            if (condition) {
                user.gameData.achievements.push(achievementId);
                user.gameData.coins += achievements[achievementId].reward;
                user.gameData.stars += achievements[achievementId].stars;
            }
        }
    });
}

// Восстановление энергии каждые 5 секунд
setInterval(() => {
    Object.keys(userData).forEach(chatId => {
        const user = userData[chatId];
        updateEnergy(user);
        updateBoosters(user);
        updateAutoTap(user);
        updateLimitedOffers(user);
    });
}, 5000);

console.log('🚀 Quantum Nexus Premium Telegram Bot с ограниченными акциями запущен!');
