// config/telegram.js
export const telegramConfig = {
  // Bot Token
  botToken: '8426192106:AAGGlkfOYAhaQKPp-bcL-3oHXBE50tzAMog',
  
  // WebApp URL
  webAppUrl: process.env.WEBAPP_URL || 'https://your-domain.com/quantum-nexus.html',
  
  // Webhook URL
  webhookUrl: process.env.WEBHOOK_URL || 'https://your-domain.com/webhook',
  
  // Bot команды на русском
  botCommands: [
    { command: 'start', description: '🚀 Начать игру Quantum Nexus' },
    { command: 'game', description: '🎮 Открыть игру' },
    { command: 'shop', description: '🛒 Магазин за звезды' },
    { command: 'nft', description: '🖼️ NFT коллекция' },
    { command: 'social', description: '👥 Социальные функции' },
    { command: 'ar', description: '🥽 AR режим' },
    { command: 'stats', description: '📊 Статистика' },
    { command: 'leaderboard', description: '🏆 Рейтинг игроков' },
    { command: 'help', description: '❓ Помощь и поддержка' }
  ],
  
  // Приветственное сообщение
  welcomeMessage: `
🚀 Добро пожаловать в Quantum Nexus!

Это ультрасовременная тапалка с интеграцией:
• ⭐ Telegram Stars - быстрые покупки
• 💰 Криптовалюты - Bitcoin, Ethereum
• 🖼️ NFT коллекции - уникальные токены
• 🥽 AR/VR режим - иммерсивный опыт
• 🤖 AI-ассистент - персональная помощь
• 👥 Социальные функции - гильдии и чаты

Нажмите кнопку ниже, чтобы начать игру!
  `,
  
  // Настройки WebApp
  webAppSettings: {
    title: 'Quantum Nexus',
    description: 'Ультимативная Тапалка Революция',
    photo: 'https://your-domain.com/quantum-nexus-preview.jpg',
    text: '🎮 Играть в Quantum Nexus',
    buttonText: '🚀 Начать игру'
  },
  
  // Настройки уведомлений
  notifications: {
    levelUp: '🎉 Поздравляем! Вы достигли {level} уровня!',
    achievement: '🏆 Достижение разблокировано: {title}',
    nftReceived: '🖼️ Новый NFT: {name} ({rarity})',
    starPurchase: '⭐ Покупка за звезды: {item} за {price} ⭐',
    cryptoEarned: '💰 Получено {amount} {currency}',
    guildJoined: '👥 Вы присоединились к гильдии "{guild}"',
    tournamentWin: '🏆 Поздравляем с победой в турнире!'
  },
  
  // Настройки вибрации
  hapticFeedback: {
    tap: 'medium',
    levelUp: 'success',
    achievement: 'success',
    purchase: 'light',
    error: 'error',
    warning: 'warning'
  },
  
  // Настройки темы
  theme: {
    primaryColor: '#00FFFF',
    secondaryColor: '#FF0080',
    backgroundColor: '#0A0A0A',
    textColor: '#FFFFFF',
    accentColor: '#80FF00'
  },
  
  // Настройки безопасности
  security: {
    validateAuthData: true,
    checkSignature: true,
    rateLimit: {
      taps: 100, // Максимум тапов в минуту
      purchases: 10, // Максимум покупок в минуту
      messages: 5 // Максимум сообщений в минуту
    }
  }
}

// Экспорт для использования в других модулях
export default telegramConfig
