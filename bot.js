const { Telegraf } = require('telegraf');
const axios = require('axios');

const bot = new Telegraf(process.env.BOT_TOKEN);

// Команда /start
bot.start((ctx) => {
  const keyboard = {
    inline_keyboard: [
      [{ text: '🎮 Играть в Quantum Nexus', web_app: { url: process.env.WEBAPP_URL } }],
      [{ text: '📊 Статистика', callback_data: 'stats' }],
      [{ text: '🏆 Рейтинг', callback_data: 'ranking' }]
    ]
  };
  
  ctx.reply(
    `🚀 Добро пожаловать в Quantum Nexus!\n\n` +
    `⚛️ Самая продвинутая квантумная тапалка!\n` +
    `💰 Зарабатывайте EXP и выводите реальные деньги!\n\n` +
    `🎯 Нажмите кнопку ниже, чтобы начать игру!`,
    { reply_markup: keyboard }
  );
});

// Обработка callback запросов
bot.action('stats', (ctx) => {
  ctx.answerCbQuery('📊 Статистика будет доступна в игре!');
});

bot.action('ranking', (ctx) => {
  ctx.answerCbQuery('🏆 Рейтинг будет доступен в игре!');
});

// Запуск бота
bot.launch().then(() => {
  console.log('🤖 Quantum Nexus Bot запущен!');
}).catch((error) => {
  console.error('❌ Ошибка запуска бота:', error);
});

// Graceful stop
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));