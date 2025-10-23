import express from 'express'
import cors from 'cors'
import axios from 'axios'
import path from 'path'
import { fileURLToPath } from 'url'
import telegramConfig from './config/telegram.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()
const PORT = process.env.PORT || 3000

// Telegram Bot API
const BOT_TOKEN = telegramConfig.botToken
const TELEGRAM_API_URL = `https://api.telegram.org/bot${BOT_TOKEN}`

// Middleware
app.use(cors())
app.use(express.json())
app.use(express.static(path.join(__dirname, 'public')))

// База данных (в реальном проекте используйте MongoDB/PostgreSQL)
let gameData = new Map()
let leaderboard = []
let nftMarketplace = []
let cryptoPrices = {
  bitcoin: 45000,
  ethereum: 3000,
  quantumToken: 0.01
}

// Инициализация NFT маркетплейса
function initializeNFTMarketplace() {
  nftMarketplace = [
    {
      id: 'quantum_crystal',
      name: 'Квантовый Кристалл',
      description: 'Редкий кристалл с квантовыми свойствами',
      rarity: 'common',
      power: 1.1,
      icon: '💎',
      price: 1000,
      color: '#00FFFF'
    },
    {
      id: 'neural_network',
      name: 'Нейронная Сеть',
      description: 'Живая нейронная сеть для обработки данных',
      rarity: 'rare',
      power: 1.25,
      icon: '🧠',
      price: 5000,
      color: '#FF0080'
    },
    {
      id: 'time_loop',
      name: 'Временная Петля',
      description: 'Загадочная петля времени и пространства',
      rarity: 'epic',
      power: 1.5,
      icon: '🌀',
      price: 15000,
      color: '#80FF00'
    },
    {
      id: 'black_hole',
      name: 'Черная Дыра',
      description: 'Мощная черная дыра с гравитационными свойствами',
      rarity: 'legendary',
      power: 2.0,
      icon: '⚫',
      price: 50000,
      color: '#000000'
    },
    {
      id: 'multiverse',
      name: 'Мультивселенная',
      description: 'Вся мультивселенная в одном токене',
      rarity: 'mythic',
      power: 3.0,
      icon: '🌌',
      price: 100000,
      color: '#8B00FF'
    }
  ]
}

// API Routes

// Получение данных игры
app.get('/api/game/:userId', (req, res) => {
  const userId = req.params.userId
  const data = gameData.get(userId) || {
    totalTaps: 0,
    energy: 100,
    maxEnergy: 100,
    coins: 0,
    level: 1,
    experience: 0,
    multiplier: 1,
    corePower: 1,
    bitcoin: 0,
    ethereum: 0,
    quantumToken: 0,
    nfts: [],
    upgrades: {
      tapPower: 1,
      energyRegen: 1,
      coinMultiplier: 1,
      experienceMultiplier: 1,
      cryptoMining: 1,
      nftDrop: 1
    },
    achievements: [],
    statistics: {
      totalPlayTime: 0,
      coinsEarned: 0,
      nftsMinted: 0,
      cryptoMined: 0
    }
  }
  
  res.json({
    success: true,
    data: data,
    cryptoPrices: cryptoPrices,
    nftMarketplace: nftMarketplace
  })
})

// Сохранение данных игры
app.post('/api/game/:userId/save', (req, res) => {
  const userId = req.params.userId
  const gameDataToSave = req.body
  
  gameData.set(userId, gameDataToSave)
  
  // Обновление рейтинга
  updateLeaderboard(userId, gameDataToSave)
  
  res.json({
    success: true,
    message: 'Данные сохранены успешно'
  })
})

// Покупка за Telegram Stars
app.post('/api/purchase/stars', async (req, res) => {
  const { itemId, price, userId } = req.body
  
  try {
    // Создаем заказ в базе данных
    const order = {
      id: Date.now().toString(),
      userId: userId,
      itemId: itemId,
      price: price,
      currency: 'stars',
      status: 'pending',
      createdAt: new Date().toISOString()
    }
    
    // Отправляем запрос в Telegram API для создания инвойса
    const telegramResponse = await axios.post(
      `${TELEGRAM_API_URL}/sendInvoice`,
      {
        chat_id: userId,
        title: `Покупка ${itemId}`,
        description: `Купить ${itemId} за ${price} звезд`,
        payload: JSON.stringify({
          orderId: order.id,
          itemId: itemId
        }),
        provider_token: '', // Для звезд не нужен
        currency: 'XTR', // Код валюты для звезд
        prices: [{
          label: itemId,
          amount: price * 100 // В копейках
        }]
      }
    )
    
    res.json({
      success: true,
      orderId: order.id,
      invoiceId: telegramResponse.data.result.invoice_id
    })
    
  } catch (error) {
    console.error('Ошибка создания заказа:', error)
    res.status(500).json({
      success: false,
      message: 'Ошибка создания заказа'
    })
  }
})

// Получение рейтинга
app.get('/api/leaderboard', (req, res) => {
  res.json({
    success: true,
    leaderboard: leaderboard.slice(0, 100) // Топ 100
  })
})

// Получение статистики
app.get('/api/stats/:userId', (req, res) => {
  const userId = req.params.userId
  const userData = gameData.get(userId)
  
  if (!userData) {
    return res.status(404).json({
      success: false,
      message: 'Пользователь не найден'
    })
  }
  
  const stats = {
    totalTaps: userData.totalTaps,
    level: userData.level,
    coins: userData.coins,
    bitcoin: userData.bitcoin,
    nftCount: userData.nfts.length,
    playTime: userData.statistics.totalPlayTime,
    rank: leaderboard.findIndex(player => player.userId === userId) + 1
  }
  
  res.json({
    success: true,
    stats: stats
  })
})

// Получение достижений
app.get('/api/achievements/:userId', (req, res) => {
  const userId = req.params.userId
  const userData = gameData.get(userId)
  
  if (!userData) {
    return res.status(404).json({
      success: false,
      message: 'Пользователь не найден'
    })
  }
  
  const achievements = [
    {
      id: 'first_tap',
      title: 'Первые Шаги',
      description: 'Сделайте первый тап',
      icon: '👆',
      unlocked: userData.totalTaps >= 1,
      reward: { coins: 100, stars: 5 }
    },
    {
      id: 'hundred_taps',
      title: 'Сотня',
      description: 'Сделайте 100 тапов',
      icon: '💯',
      unlocked: userData.totalTaps >= 100,
      reward: { coins: 1000, stars: 10 }
    },
    {
      id: 'thousand_taps',
      title: 'Тысяча',
      description: 'Сделайте 1000 тапов',
      icon: '🎯',
      unlocked: userData.totalTaps >= 1000,
      reward: { coins: 10000, stars: 25 }
    },
    {
      id: 'level_ten',
      title: 'Десятка',
      description: 'Достигните 10 уровня',
      icon: '🔟',
      unlocked: userData.level >= 10,
      reward: { coins: 5000, stars: 20 }
    },
    {
      id: 'crypto_miner',
      title: 'Криптомайнер',
      description: 'Накопите 0.001 Bitcoin',
      icon: '₿',
      unlocked: userData.bitcoin >= 0.001,
      reward: { coins: 20000, stars: 50 }
    },
    {
      id: 'nft_collector',
      title: 'Коллекционер NFT',
      description: 'Получите 5 NFT',
      icon: '🖼️',
      unlocked: userData.nfts.length >= 5,
      reward: { coins: 15000, stars: 30 }
    }
  ]
  
  res.json({
    success: true,
    achievements: achievements
  })
})

// Telegram Webhook
app.post('/webhook', async (req, res) => {
  const update = req.body
  
  try {
    if (update.message) {
      const message = update.message
      const chatId = message.chat.id
      const text = message.text
      
      if (text === '/start') {
        const keyboard = {
          inline_keyboard: [[
            {
              text: '🎮 Начать игру',
              web_app: { url: telegramConfig.webAppUrl }
            }
          ]]
        }
        
        await sendMessage(chatId, telegramConfig.welcomeMessage, keyboard)
      }
      
      if (text === '/help') {
        const helpMessage = `
❓ Помощь по Quantum Nexus:

🎮 Основные команды:
/start - Начать игру
/game - Открыть игру
/shop - Магазин за звезды
/nft - NFT коллекция
/social - Социальные функции
/ar - AR режим
/stats - Статистика
/leaderboard - Рейтинг игроков

💡 Советы:
• Тапайте по квантовому ядру для получения монет
• Покупайте улучшения для увеличения мощности
• Собирайте NFT для дополнительных бонусов
• Присоединяйтесь к гильдиям для социального взаимодействия

🆘 Поддержка:
Если у вас есть вопросы, обратитесь к @quantum_nexus_support
        `
        
        await sendMessage(chatId, helpMessage)
      }
    }
    
    if (update.pre_checkout_query) {
      // Подтверждаем платеж
      await axios.post(
        `${TELEGRAM_API_URL}/answerPreCheckoutQuery`,
        {
          pre_checkout_query_id: update.pre_checkout_query.id,
          ok: true
        }
      )
    }
    
    if (update.message && update.message.successful_payment) {
      // Обрабатываем успешный платеж
      const payment = update.message.successful_payment
      const orderData = JSON.parse(payment.invoice_payload)
      
      // Выдаем товар пользователю
      await giveItemToUser(orderData.userId, orderData.itemId)
      
      // Уведомляем пользователя
      await sendMessage(update.message.chat.id, 
        '🎉 Покупка успешна! Товар добавлен в ваш инвентарь!'
      )
    }
    
    res.json({ ok: true })
    
  } catch (error) {
    console.error('Ошибка обработки webhook:', error)
    res.status(500).json({ ok: false })
  }
})

// Функция отправки сообщения
async function sendMessage(chatId, text, keyboard = null) {
  try {
    const response = await axios.post(`${TELEGRAM_API_URL}/sendMessage`, {
      chat_id: chatId,
      text: text,
      reply_markup: keyboard,
      parse_mode: 'HTML'
    })
    return response.data
  } catch (error) {
    console.error('Ошибка отправки сообщения:', error)
  }
}

// Функция выдачи товара
async function giveItemToUser(userId, itemId) {
  const userData = gameData.get(userId)
  if (userData) {
    // Добавляем товар в инвентарь
    userData.nfts.push({
      id: itemId,
      receivedAt: new Date().toISOString()
    })
    
    gameData.set(userId, userData)
  }
}

// Обновление рейтинга
function updateLeaderboard(userId, userData) {
  const existingIndex = leaderboard.findIndex(player => player.userId === userId)
  const playerData = {
    userId: userId,
    username: userData.username || 'Игрок',
    level: userData.level,
    totalTaps: userData.totalTaps,
    coins: userData.coins,
    bitcoin: userData.bitcoin,
    nftCount: userData.nfts.length,
    lastActive: new Date().toISOString()
  }
  
  if (existingIndex >= 0) {
    leaderboard[existingIndex] = playerData
  } else {
    leaderboard.push(playerData)
  }
  
  // Сортировка по уровню и количеству тапов
  leaderboard.sort((a, b) => {
    if (a.level !== b.level) {
      return b.level - a.level
    }
    return b.totalTaps - a.totalTaps
  })
}

// Обновление цен криптовалют
function updateCryptoPrices() {
  setInterval(() => {
    cryptoPrices.bitcoin *= (0.95 + Math.random() * 0.1) // ±5% изменение
    cryptoPrices.ethereum *= (0.95 + Math.random() * 0.1)
    cryptoPrices.quantumToken *= (0.9 + Math.random() * 0.2) // ±10% изменение
    
    // Ограничения цен
    cryptoPrices.bitcoin = Math.max(10000, Math.min(100000, cryptoPrices.bitcoin))
    cryptoPrices.ethereum = Math.max(1000, Math.min(10000, cryptoPrices.ethereum))
    cryptoPrices.quantumToken = Math.max(0.001, Math.min(1, cryptoPrices.quantumToken))
  }, 30000) // Обновление каждые 30 секунд
}

// Инициализация
initializeNFTMarketplace()
updateCryptoPrices()

// Настройка команд бота
async function setupBotCommands() {
  try {
    await axios.post(`${TELEGRAM_API_URL}/setMyCommands`, {
      commands: telegramConfig.botCommands
    })
    console.log('✅ Команды бота настроены')
  } catch (error) {
    console.error('❌ Ошибка настройки команд:', error)
  }
}

// Запуск сервера
app.listen(PORT, async () => {
  console.log(`🚀 Quantum Nexus Server запущен на порту ${PORT}`)
  console.log(`📱 Telegram Bot Token: ${BOT_TOKEN.substring(0, 10)}...`)
  console.log(`🌐 WebApp доступен по адресу: ${telegramConfig.webAppUrl}`)
  
  // Настройка команд бота
  await setupBotCommands()
})

// Обработка ошибок
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason)
})

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error)
  process.exit(1)
})