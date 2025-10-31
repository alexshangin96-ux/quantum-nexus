// Generate 150 achievements for Quantum Nexus

const achievements = [];

// Helper to generate achievements
function addAchievement(id, title, desc, unlocked, icon, category, color) {
    achievements.push({id, title, desc, unlocked, icon, category, color});
}

// TAPS (12 achievements)
const taps = [1, 10, 100, 1000, 10000, 100000, 500000, 1000000, 5000000, 10000000, 50000000, 100000000];
const tapsEmojis = ['👆', '🎯', '⚡', '🔥', '💥', '👑', '💀', '😈', '∞', '🌌', '🌀', '⚡'];
const tapsTitles = ['Первый тап', 'Новичок', 'Мастер', 'Профи', 'Легенда', 'Бог', 'Титан', 'Абсолют', 'Бесконечность', 'Вселенная', 'Мультивселенная', 'КОСМОС'];
taps.forEach((threshold, idx) => {
    addAchievement(`taps_${idx}`, `${tapsEmojis[idx]} ${tapsTitles[idx]}`, `Сделайте ${threshold === 1 ? 'первый тап' : threshold.toLocaleString() + ' тапов'}`, false, tapsEmojis[idx], 'taps', '#60a5fa');
});

// COINS (9 achievements)
const coins = [1000000, 5000000, 10000000, 50000000, 100000000, 500000000, 1000000000, 5000000000, 10000000000];
const coinsEmojis = ['💰', '💸', '💎', '🏆', '👑', '⭐', '🌟', '✨', '💫'];
const coinsTitles = ['Миллионер', 'Тиран', 'Магнат', 'Олигарх', 'Империя', 'Федерация', 'КОСМОС', 'БЕСКОНЕЧНОСТЬ', 'ВСЕЛЕННАЯ'];
coins.forEach((threshold, idx) => {
    const value = threshold / 1000000;
    addAchievement(`coins_${idx}`, `${coinsEmojis[idx]} ${coinsTitles[idx]}`, `Заработайте ${value.toFixed(value >= 1000 ? 0 : 1)}M коинов`, false, coinsEmojis[idx], 'coins', '#fbbf24');
});

// CARDS (9 achievements)
const cards = [1, 5, 10, 25, 50, 100, 250, 500, 1000];
const cardsEmojis = ['🃏', '🃏', '🎴', '🃏', '🎴', '🃏', '🎴', '🃏', '🎴'];
const cardsTitles = ['Первая карта', 'Коллекционер', 'Коллекционер+', 'Мастер', 'Мастер карт', 'Легенда', 'Бог карт', 'КОСМОС', 'ВСЕЛЕННАЯ'];
cards.forEach((threshold, idx) => {
    addAchievement(`cards_${idx}`, `${cardsEmojis[idx]} ${cardsTitles[idx]}`, `Купите ${threshold} ${threshold === 1 ? 'карту' : threshold < 5 ? 'карты' : 'карт'}`, false, cardsEmojis[idx], 'cards', '#8b5cf6');
});

// MINING (9 achievements)
const mining = [1, 5, 10, 25, 50, 100, 250, 500, 1000];
const miningEmojis = ['⛏️', '🏭', '🏗️', '⚙️', '🏭', '🏗️', '⚙️', '🏭', '🏗️'];
const miningTitles = ['Первая машина', 'Цех', 'Фабрика', 'Завод', 'Мегафабрика', 'Корпорация', 'Конгломерат', 'КОСМОС', 'ВСЕЛЕННАЯ'];
mining.forEach((threshold, idx) => {
    addAchievement(`mining_${idx}`, `${miningEmojis[idx]} ${miningTitles[idx]}`, `Купите ${threshold} ${threshold === 1 ? 'машину' : threshold < 5 ? 'машины' : 'машин'}`, false, miningEmojis[idx], 'mining', '#10b981');
});

// LEVELS (10 achievements)
const levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
const levelEmojis = ['🌟', '⭐', '✨', '💫', '🌟', '⭐', '✨', '💫', '🌟', '💫'];
const levelTitles = ['Уровень 10', 'Уровень 20', 'Уровень 30', 'Уровень 40', 'Уровень 50', 'Уровень 60', 'Уровень 70', 'Уровень 80', 'Уровень 90', 'МАКСИМУМ'];
levels.forEach((threshold, idx) => {
    addAchievement(`level_${idx}`, `${levelEmojis[idx]} ${levelTitles[idx]}`, `Достигните ${threshold} уровня`, false, levelEmojis[idx], 'level', '#a78bfa');
});

// VIP (10 achievements)
for (let i = 1; i <= 10; i++) {
    const vipEmojis = ['🥉', '🥈', '🥇', '💎', '👑', '💍', '👑', '👑', '👑', '👑'];
    const vipTitles = ['VIP бронза', 'VIP серебро', 'VIP золото', 'VIP платина', 'VIP ДИАМОНД', 'VIP LEGEND', 'VIP MEGA', 'VIP ULTRA', 'VIP MASTER', 'VIP GOD'];
    addAchievement(`vip_${i-1}`, `${vipEmojis[i-1]} ${vipTitles[i-1]}`, `VIP уровень ${i}`, false, vipEmojis[i-1], 'vip', '#ffd700');
}

// SOCIAL (7 achievements)
const social = [1, 5, 10, 25, 50, 100, 500];
const socialEmojis = ['👥', '👫', '🌐', '👬', '👭', '🤝', '🙌'];
const socialTitles = ['Первый друг', 'Маг', 'Мастер', 'Лидер', 'Легенда', 'КОСМОС', 'ВСЕЛЕННАЯ'];
social.forEach((threshold, idx) => {
    addAchievement(`social_${idx}`, `${socialEmojis[idx]} ${socialTitles[idx]}`, `Пригласите ${threshold} ${threshold === 1 ? 'друга' : threshold < 5 ? 'друзей' : 'друзей'}`, false, socialEmojis[idx], 'social', '#ec4899');
});

// ENERGY (10 achievements)
const energy = [10, 100, 1000, 10000, 100000, 10, 100, 1000, 100, 1000];
const energyEmojis = ['⚡', '⚡', '⚡', '⚡', '⚡', '🔄', '🔄', '🔄', '💯', '💯'];
const energyTitles = ['Энергия 10', 'Энергия 100', 'Энергия 1K', 'Энергия 10K', 'Энергия 100K', 'Пополнений 10', 'Пополнений 100', 'Пополнений 1K', 'За раз 100', 'За раз 1K'];
const energyDescs = [
    'Используйте 10 энергии',
    'Используйте 100 энергии',
    'Используйте 1,000 энергии',
    'Используйте 10,000 энергии',
    'Используйте 100,000 энергии',
    'Пополните энергию 10 раз',
    'Пополните энергию 100 раз',
    'Пополните энергию 1,000 раз',
    'Получите 100 энергии за раз',
    'Получите 1,000 энергии за раз'
];
energy.forEach((threshold, idx) => {
    addAchievement(`energy_${idx}`, `${energyEmojis[idx]} ${energyTitles[idx]}`, energyDescs[idx], false, energyEmojis[idx], 'energy', '#ef4444');
});

// SHOP PURCHASES (15 achievements)
const shop = [1, 10, 50, 100, 500, 1000, 1, 1, 1, 1, 1000000, 10000000, 100000000, 1000000000, 10000000000];
const shopEmojis = ['🛍️', '🛍️', '🛍️', '🛍️', '🛍️', '🛍️', '💪', '⚡', '📈', '🤖', '💸', '💸', '💸', '💸', '💸'];
const shopTitles = ['Первая покупка', 'Покупатель', 'Магазинщик', 'Тратитель', 'Расточитель', 'Шопоголик', 'Усилитель', 'Восстановление', 'Расширение', 'Автобот', 'Потрачено 1M', 'Потрачено 10M', 'Потрачено 100M', 'Потрачено 1B', 'Потрачено 10B'];
const shopDescs = [
    'Купите 1 предмет',
    'Купите 10 предметов',
    'Купите 50 предметов',
    'Купите 100 предметов',
    'Купите 500 предметов',
    'Купите 1,000 предметов',
    'Купите усилитель тапа',
    'Купите восстановление энергии',
    'Купите расширение энергии',
    'Купите автобота',
    'Потратьте 1M коинов',
    'Потратьте 10M коинов',
    'Потратьте 100M коинов',
    'Потратьте 1B коинов',
    'Потратьте 10B коинов'
];
shop.forEach((threshold, idx) => {
    addAchievement(`shop_${idx}`, `${shopEmojis[idx]} ${shopTitles[idx]}`, shopDescs[idx], false, shopEmojis[idx], 'shop', '#06b6d4');
});

// TIME PLAYED (10 achievements)
const timeDays = [1, 7, 30, 100, 365];
const timeLogins = [10, 100, 1000];
const timeOffline = [10, 100];
const timeEmojis = ['📅', '📆', '📊', '🗓️', '📆', '🎮', '🎮', '🎮', '🏆', '🏆'];
const timeTitles = ['1 день', '7 дней', '30 дней', '100 дней', '365 дней', '10 входов', '100 входов', '1,000 входов', '10 офлайн', '100 офлайн'];
const timeDescs = [
    'Играйте 1 день',
    'Играйте 7 дней',
    'Играйте 30 дней',
    'Играйте 100 дней',
    'Играйте 365 дней',
    'Зайте 10 раз',
    'Зайдите 100 раз',
    'Зайдите 1,000 раз',
    'Получите 10 офлайн-наград',
    'Получите 100 офлайн-наград'
];
[...timeDays, ...timeLogins, ...timeOffline].forEach((threshold, idx) => {
    addAchievement(`time_${idx}`, `${timeEmojis[idx]} ${timeTitles[idx]}`, timeDescs[idx], false, timeEmojis[idx], 'time', '#8b5cf6');
});

// MINING INCOME (10 achievements)
const miningIncome = [100, 1000, 10000, 100000, 1000000, 10, 100, 1000, 1, 7];
const miningEmojis2 = ['⛏️', '⛏️', '⛏️', '⛏️', '⛏️', '🎁', '🎁', '🎁', '🕐', '🕐'];
const miningTitles2 = ['100 QH', '1K QH', '10K QH', '100K QH', '1M QH', '10 бонусов', '100 бонусов', '1K бонусов', '24 часа', '7 дней'];
const miningDescs = [
    'Добыть 100 QuanHash',
    'Добыть 1,000 QuanHash',
    'Добыть 10,000 QuanHash',
    'Добыть 100,000 QuanHash',
    'Добыть 1,000,000 QuanHash',
    'Получить 10 бонусов',
    'Получить 100 бонусов',
    'Получить 1,000 бонусов',
    'Майнить 24 часа подряд',
    'Майнить 7 дней подряд'
];
miningIncome.forEach((threshold, idx) => {
    addAchievement(`mining_inc_${idx}`, `${miningEmojis2[idx]} ${miningTitles2[idx]}`, miningDescs[idx], false, miningEmojis2[idx], 'mining_inc', '#14b8a6');
});

// ACCURACY (10 achievements)
const accuracy = [10, 50, 100, 500, 1000, 100, 1000, 10000, 100000, 1000000];
const accuracyEmojis = ['🎯', '🎯', '🎯', '🎯', '🎯', '⚡', '⚡', '⚡', '⚡', '⚡'];
const accuracyTitles = ['10 подряд', '50 подряд', '100 подряд', '500 подряд', '1K подряд', '100/мин', '1K/5мин', '10K/час', '100K/день', '1M/неделя'];
const accuracyDescs = [
    '10 тапов подряд',
    '50 тапов подряд',
    '100 тапов подряд',
    '500 тапов подряд',
    '1,000 тапов подряд',
    'Сделайте 100 тапов за минуту',
    'Сделайте 1,000 тапов за 5 минут',
    'Сделайте 10,000 тапов за час',
    'Сделайте 100,000 тапов за день',
    'Сделайте 1,000,000 тапов за неделю'
];
accuracy.forEach((threshold, idx) => {
    addAchievement(`accuracy_${idx}`, `${accuracyEmojis[idx]} ${accuracyTitles[idx]}`, accuracyDescs[idx], false, accuracyEmojis[idx], 'accuracy', '#f59e0b');
});

// CHAT/COMMUNITY (10 achievements)
const chat = [1, 10, 100, 1000, 1, 10, 50, 1, 10, 100];
const chatEmojis = ['💬', '💬', '💬', '💬', '🤝', '🤝', '🤝', '❤️', '❤️', '❤️'];
const chatTitles = ['1 сообщение', '10 сообщений', '100 сообщений', '1K сообщений', 'Помощь 1', 'Помощь 10', 'Помощь 50', '1 лайк', '10 лайков', '100 лайков'];
const chatDescs = [
    'Напишите в чат 1 раз',
    'Напишите в чат 10 раз',
    'Напишите в чат 100 раз',
    'Напишите в чат 1,000 раз',
    'Помогите новичку',
    'Помогите 10 новичкам',
    'Помогите 50 новичкам',
    'Получите лайк',
    'Получите 10 лайков',
    'Получите 100 лайков'
];
chat.forEach((threshold, idx) => {
    addAchievement(`chat_${idx}`, `${chatEmojis[idx]} ${chatTitles[idx]}`, chatDescs[idx], false, chatEmojis[idx], 'chat', '#ec4899');
});

// EVENTS (10 achievements)
const events = [1, 10, 50, 100, 1, 10, 50, 1, 10, 50];
const eventEmojis = ['🎉', '🎉', '🎉', '🎉', '🏆', '🏆', '🏆', '🥇', '🥇', '🥇'];
const eventTitles = ['1 событие', '10 событий', '50 событий', '100 событий', 'Побед 1', 'Побед 10', 'Побед 50', '1 место', '1 место x10', '1 место x50'];
const eventDescs = [
    'Участвуйте в событии 1 раз',
    'Участвуйте в 10 событиях',
    'Участвуйте в 50 событиях',
    'Участвуйте в 100 событиях',
    'Выиграйте событие 1 раз',
    'Выиграйте событие 10 раз',
    'Выиграйте событие 50 раз',
    'Заньте 1 место',
    'Заньте 1 место 10 раз',
    'Заньте 1 место 50 раз'
];
events.forEach((threshold, idx) => {
    addAchievement(`event_${idx}`, `${eventEmojis[idx]} ${eventTitles[idx]}`, eventDescs[idx], false, eventEmojis[idx], 'event', '#10b981');
});

// RANKINGS (10 achievements)
const rankings = [100, 50, 25, 10, 5, 1, 1, 1, 1, 1];
const rankEmojis = ['📊', '📊', '📊', '📊', '📊', '👑', '📅', '📅', '⭐', '🌟'];
const rankTitles = ['ТОП-100', 'ТОП-50', 'ТОП-25', 'ТОП-10', 'ТОП-5', '№1', 'Неделя в ТОП-10', 'Месяц в ТОП-10', 'ТОП-3', 'Легенда'];
const rankDescs = [
    'Войдите в топ 100',
    'Войдите в топ 50',
    'Войдите в топ 25',
    'Войдите в топ 10',
    'Войдите в топ 5',
    'Заньте 1 место',
    'Продержитесь в топ 10 неделю',
    'Продержитесь в топ 10 месяц',
    'Будьте в топ 3 по всем',
    'Станьте легендой'
];
rankings.forEach((threshold, idx) => {
    addAchievement(`rank_${idx}`, `${rankEmojis[idx]} ${rankTitles[idx]}`, rankDescs[idx], false, rankEmojis[idx], 'rank', '#fbbf24');
});

// WITHDRAWS (5 achievements)
const withdraws = [1, 10, 100, 1000000, 10000000];
const withdrawEmojis = ['💸', '💸', '💸', '💸', '💸'];
const withdrawTitles = ['Первый вывод', '10 выводов', '100 выводов', '1M QH', '10M QH'];
const withdrawDescs = [
    'Выведите средства 1 раз',
    'Выведите средства 10 раз',
    'Выведите средства 100 раз',
    'Выведите 1,000,000 QuanHash',
    'Выведите 10,000,000 QuanHash'
];
withdraws.forEach((threshold, idx) => {
    addAchievement(`withdraw_${idx}`, `${withdrawEmojis[idx]} ${withdrawTitles[idx]}`, withdrawDescs[idx], false, withdrawEmojis[idx], 'withdraw', '#6366f1');
});

// DAILIES (10 achievements)
const dailies = [1, 10, 50, 100, 365, 7, 30, 100, 1, 1];
const dailyEmojis = ['📋', '📋', '📋', '📋', '📋', '📦', '📦', '📦', '✅', '✅'];
const dailyTitles = ['1 задание', '10 заданий', '50 заданий', '100 заданий', '365 заданий', '7 дней', '30 дней', '100 дней', 'Все в день', 'Все в неделю'];
const dailyDescs = [
    'Выполните 1 задание',
    'Выполните 10 заданий',
    'Выполните 50 заданий',
    'Выполните 100 заданий',
    'Выполните 365 заданий',
    'Получите бонус 7 дней',
    'Получите бонус 30 дней',
    'Получите бонус 100 дней',
    'Выполните все за день',
    'Выполните все за неделю'
];
dailies.forEach((threshold, idx) => {
    addAchievement(`daily_${idx}`, `${dailyEmojis[idx]} ${dailyTitles[idx]}`, dailyDescs[idx], false, dailyEmojis[idx], 'daily', '#0ea5e9');
});

console.log(`Generated ${achievements.length} achievements`);
console.log(JSON.stringify(achievements, null, 2));

