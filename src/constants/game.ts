// Game constants
export const GAME_CONFIG = {
  // Currency rates
  EXP_TO_USD_RATE: 100000, // 100,000 EXP = 1 USD
  WITHDRAWAL_FEE: 0.05, // 5% fee
  
  // Tap mechanics
  BASE_TAP_VALUE: 1,
  LEVEL_MULTIPLIER: 1.1,
  MAX_LEVEL: 1000,
  
  // Investment categories
  INVESTMENT_CATEGORIES: [
    {
      id: 'quantum',
      name: 'Quantum Core',
      basePrice: 1000,
      baseIncome: 10,
      description: 'Р‘Р°Р·РѕРІС‹Р№ РіРµРЅРµСЂР°С‚РѕСЂ РєРІР°РЅС‚СѓРјРЅРѕР№ СЌРЅРµСЂРіРёРё'
    },
    {
      id: 'crypto',
      name: 'Crypto Miner',
      basePrice: 5000,
      baseIncome: 50,
      description: 'РњР°Р№РЅРёРЅРі РєСЂРёРїС‚РѕРІР°Р»СЋС‚С‹'
    },
    {
      id: 'stocks',
      name: 'Stock Portfolio',
      basePrice: 25000,
      baseIncome: 250,
      description: 'РРЅРІРµСЃС‚РёС†РёРё РІ Р°РєС†РёРё'
    },
    {
      id: 'realestate',
      name: 'Real Estate',
      basePrice: 100000,
      baseIncome: 1000,
      description: 'РќРµРґРІРёР¶РёРјРѕСЃС‚СЊ'
    },
    {
      id: 'tech',
      name: 'AI Company',
      basePrice: 500000,
      baseIncome: 5000,
      description: 'РСЃРєСѓСЃСЃС‚РІРµРЅРЅС‹Р№ РёРЅС‚РµР»Р»РµРєС‚'
    }
  ],
  
  // Daily bonuses
  DAILY_BONUS_BASE: 100,
  DAILY_BONUS_MULTIPLIER: 1.1,
  MAX_DAILY_STREAK: 365,
  
  // Offline income
  OFFLINE_DURATION: 3 * 60 * 60 * 1000, // 3 hours in milliseconds
  OFFLINE_MULTIPLIER: 1.0,
  
  // Shop items
  SHOP_ITEMS: [
    {
      id: 'tap_multiplier_1h',
      name: 'РњРЅРѕР¶РёС‚РµР»СЊ С‚Р°РїР°РЅРёСЏ (1С‡)',
      price: 10,
      type: 'tap_multiplier',
      duration: 60 * 60 * 1000, // 1 hour
      value: 2.0
    },
    {
      id: 'tap_multiplier_24h',
      name: 'РњРЅРѕР¶РёС‚РµР»СЊ С‚Р°РїР°РЅРёСЏ (24С‡)',
      price: 200,
      type: 'tap_multiplier',
      duration: 24 * 60 * 60 * 1000, // 24 hours
      value: 3.0
    },
    {
      id: 'auto_clicker_basic',
      name: 'РђРІС‚Рѕ-РєР»РёРєРµСЂ (Р±Р°Р·РѕРІС‹Р№)',
      price: 50,
      type: 'auto_clicker',
      duration: 60 * 60 * 1000, // 1 hour
      value: 1
    },
    {
      id: 'auto_clicker_advanced',
      name: 'РђРІС‚Рѕ-РєР»РёРєРµСЂ (РїСЂРѕРґРІРёРЅСѓС‚С‹Р№)',
      price: 500,
      type: 'auto_clicker',
      duration: 24 * 60 * 60 * 1000, // 24 hours
      value: 5
    },
    {
      id: 'offline_multiplier',
      name: 'РћС„С„Р»Р°Р№РЅ РјРЅРѕР¶РёС‚РµР»СЊ',
      price: 100,
      type: 'offline_multiplier',
      duration: 7 * 24 * 60 * 60 * 1000, // 7 days
      value: 2.0
    },
    {
      id: 'offline_duration',
      name: 'РЈРІРµР»РёС‡РµРЅРёРµ РѕС„С„Р»Р°Р№РЅ РІСЂРµРјРµРЅРё',
      price: 200,
      type: 'offline_duration',
      duration: 30 * 24 * 60 * 60 * 1000, // 30 days
      value: 6 * 60 * 60 * 1000 // +6 hours
    }
  ],
  
  // Referral system
  REFERRAL_REWARD_INVITER: 1000, // EXP for inviter
  REFERRAL_REWARD_INVITED: 500, // EXP for invited
  REFERRAL_MULTIPLIER_DURATION: 24 * 60 * 60 * 1000, // 24 hours
  
  // Ranking rewards
  RANKING_REWARDS: {
    gold: { exp: 10000, multiplier: 5.0 }, // Top 10
    silver: { exp: 5000, multiplier: 3.0 }, // Top 50
    bronze: { exp: 2500, multiplier: 2.0 } // Top 100
  },
  
  // Achievements
  ACHIEVEMENTS: [
    {
      id: 'first_tap',
      name: 'РџРµСЂРІС‹Р№ С‚Р°Рї',
      description: 'РЎРґРµР»Р°Р№С‚Рµ РїРµСЂРІС‹Р№ С‚Р°Рї',
      condition: { taps: 1 },
      reward: { exp: 100, coins: 1000 }
    },
    {
      id: 'tap_master',
      name: 'РњР°СЃС‚РµСЂ С‚Р°РїР°РЅРёСЏ',
      description: 'РЎРґРµР»Р°Р№С‚Рµ 10,000 С‚Р°РїРѕРІ',
      condition: { taps: 10000 },
      reward: { exp: 1000, coins: 10000 }
    },
    {
      id: 'quantum_investor',
      name: 'РљРІР°РЅС‚СѓРјРЅС‹Р№ РёРЅРІРµСЃС‚РѕСЂ',
      description: 'РљСѓРїРёС‚Рµ 5 РёРЅРІРµСЃС‚РёС†РёР№',
      condition: { investments: 5 },
      reward: { exp: 2000, coins: 20000 }
    },
    {
      id: 'referral_champion',
      name: 'Р§РµРјРїРёРѕРЅ СЂРµС„РµСЂР°Р»РѕРІ',
      description: 'РџСЂРёРіР»Р°СЃРёС‚Рµ 10 РґСЂСѓР·РµР№',
      condition: { referrals: 10 },
      reward: { exp: 5000, coins: 50000 }
    },
    {
      id: 'exp_collector',
      name: 'РљРѕР»Р»РµРєС†РёРѕРЅРµСЂ EXP',
      description: 'Р—Р°СЂР°Р±РѕС‚Р°Р№С‚Рµ 1,000,000 EXP',
      condition: { exp: 1000000 },
      reward: { exp: 10000, coins: 100000 }
    },
    {
      id: 'level_master',
      name: 'РњР°СЃС‚РµСЂ СѓСЂРѕРІРЅРµР№',
      description: 'Р”РѕСЃС‚РёРіРЅРёС‚Рµ 100 СѓСЂРѕРІРЅСЏ',
      condition: { level: 100 },
      reward: { exp: 5000, coins: 50000 }
    }
  ],
  
  // Daily quests
  DAILY_QUESTS: [
    {
      id: 'quantum_tapper',
      name: 'РљРІР°РЅС‚СѓРјРЅС‹Р№ С‚Р°РїРµСЂ',
      description: 'РўР°РїРЅРёС‚Рµ 1000 СЂР°Р·',
      condition: { taps: 1000 },
      reward: { exp: 500, coins: 5000 }
    },
    {
      id: 'exp_collector',
      name: 'РљРѕР»Р»РµРєС†РёРѕРЅРµСЂ EXP',
      description: 'Р—Р°СЂР°Р±РѕС‚Р°Р№С‚Рµ 1000 EXP',
      condition: { exp: 1000 },
      reward: { exp: 200, coins: 2000 }
    },
    {
      id: 'quantum_investor',
      name: 'РљРІР°РЅС‚СѓРјРЅС‹Р№ РёРЅРІРµСЃС‚РѕСЂ',
      description: 'РџРѕС‚СЂР°С‚СЊС‚Рµ 5000 РєРІР°РЅС‚СѓРј РјРѕРЅРµС‚ РЅР° РёРЅРІРµСЃС‚РёС†РёРё',
      condition: { coinsSpent: 5000 },
      reward: { exp: 300, coins: 3000 }
    }
  ]
}

export const TELEGRAM_CONFIG = {
  BOT_TOKEN: '8426192106:AAGGlkfOYAhaQKPp-bcL-3oHXBE50tzAMog',
  WEBAPP_URL: 'http://unlock-rent.online/'
}
