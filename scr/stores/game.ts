    addTemporaryMultiplier,
    addAutoClicker,
    addOfflineMultiplier,
    increaseOfflineDuration,
    resetGameUser {
  id: string
  username: string
  firstName: string
  lastName?: string
  languageCode?: string
  isPremium?: boolean
  photoUrl?: string
}

export interface GameStats {
  quantumCoins: number
  expCoins: number
  totalTaps: number
  level: number
  experience: number
  experienceToNext: number
  multiplier: number
  autoClickerLevel: number
  prestigeLevel: number
  achievements: string[]
  lastActive: string
  totalPlayTime: number
  referralCode: string
  referredBy?: string
  referralsCount: number
  referralsEarnings: number
}

export interface Investment {
  id: string
  name: string
  description: string
  cost: number
  expPerSecond: number
  level: number
  maxLevel: number
  upgradeCost: number
  owned: boolean
  category: 'quantum' | 'crypto' | 'stocks' | 'real_estate' | 'tech'
}

export interface DailyBonus {
  day: number
  claimed: boolean
  reward: {
    quantumCoins: number
    expCoins: number
    multiplier: number
  }
}

export interface DailyQuest {
  id: string
  title: string
  description: string
  type: 'tap' | 'earn' | 'invest' | 'referral' | 'time'
  target: number
  progress: number
  reward: {
    quantumCoins: number
    expCoins: number
    multiplier: number
  }
  completed: boolean
  claimed: boolean
}

export const useGameStore = defineStore('game', () => {
  // User data
  const user = ref<User | null>(null)
  const stats = ref<GameStats>({
    quantumCoins: 0,
    expCoins: 0,
    totalTaps: 0,
    level: 1,
    experience: 0,
    experienceToNext: 100,
    multiplier: 1,
    autoClickerLevel: 0,
    prestigeLevel: 0,
    achievements: [],
    lastActive: dayjs().toISOString(),
    totalPlayTime: 0,
    referralCode: '',
    referralsCount: 0,
    referralsEarnings: 0
  })

  // Investments
  const investments = ref<Investment[]>([])
  const offlineIncomeMultiplier = ref(1)
  const offlineIncomeDuration = ref(3) // hours

  // Daily system
  const dailyBonus = ref<DailyBonus>({
    day: 1,
    claimed: false,
    reward: {
      quantumCoins: 100,
      expCoins: 10,
      multiplier: 1.1
    }
  })

  const dailyQuests = ref<DailyQuest[]>([])

  // Game state
  const isPlaying = ref(false)
  const lastSaveTime = ref(dayjs().toISOString())
  const backgroundProcesses = ref<NodeJS.Timeout[]>([])

  // Computed properties
  const totalExpPerSecond = computed(() => {
    return investments.value
      .filter(inv => inv.owned)
      .reduce((total, inv) => total + (inv.expPerSecond * inv.level), 0)
  })

  const canAffordInvestment = computed(() => {
    return (investment: Investment) => {
      if (investment.owned) {
        return stats.value.quantumCoins >= investment.upgradeCost
      }
      return stats.value.quantumCoins >= investment.cost
    }
  })

  const nextLevelExperience = computed(() => {
    return Math.floor(100 * Math.pow(1.15, stats.value.level))
  })

  const prestigeMultiplier = computed(() => {
    return Math.pow(1.5, stats.value.prestigeLevel)
  })

  // Actions
  const initializeGame = async () => {
    try {
      // Load user data from Telegram
      const telegramData = window.Telegram?.WebApp?.initDataUnsafe?.user
      if (telegramData) {
        user.value = {
          id: telegramData.id.toString(),
          username: telegramData.username || '',
          firstName: telegramData.first_name,
          lastName: telegramData.last_name,
          languageCode: telegramData.language_code,
          isPremium: telegramData.is_premium || false,
          photoUrl: telegramData.photo_url
        }
        
        // Generate referral code
        stats.value.referralCode = generateReferralCode()
      }

      // Initialize investments
      initializeInvestments()
      
      // Initialize daily quests
      initializeDailyQuests()
      
      // Load saved data
      await loadGameData()
      
      // Calculate offline income
      calculateOfflineIncome()
      
    } catch (error) {
      console.error('Failed to initialize game:', error)
    }
  }

  const initializeInvestments = () => {
    investments.value = [
      {
        id: 'quantum_core',
        name: 'Quantum Core',
        description: 'Basic quantum energy generator',
        cost: 100,
        expPerSecond: 0.1,
        level: 0,
        maxLevel: 100,
        upgradeCost: 100,
        owned: false,
        category: 'quantum'
      },
      {
        id: 'crypto_miner',
        name: 'Crypto Miner',
        description: 'Mines cryptocurrency for EXP',
        cost: 1000,
        expPerSecond: 1,
        level: 0,
        maxLevel: 50,
        upgradeCost: 1000,
        owned: false,
        category: 'crypto'
      },
      {
        id: 'stock_portfolio',
        name: 'Stock Portfolio',
        description: 'Diversified stock investments',
        cost: 10000,
        expPerSecond: 10,
        level: 0,
        maxLevel: 25,
        upgradeCost: 10000,
        owned: false,
        category: 'stocks'
      },
      {
        id: 'real_estate',
        name: 'Real Estate',
        description: 'Property investments',
        cost: 100000,
        expPerSecond: 100,
        level: 0,
        maxLevel: 20,
        upgradeCost: 100000,
        owned: false,
        category: 'real_estate'
      },
      {
        id: 'ai_company',
        name: 'AI Company',
        description: 'Artificial intelligence enterprise',
        cost: 1000000,
        expPerSecond: 1000,
        level: 0,
        maxLevel: 15,
        upgradeCost: 1000000,
        owned: false,
        category: 'tech'
      }
    ]
  }

  const initializeDailyQuests = () => {
    dailyQuests.value = [
      {
        id: 'tap_1000',
        title: 'Quantum Tapper',
        description: 'Tap 1000 times',
        type: 'tap',
        target: 1000,
        progress: 0,
        reward: {
          quantumCoins: 500,
          expCoins: 50,
          multiplier: 1.2
        },
        completed: false,
        claimed: false
      },
      {
        id: 'earn_exp',
        title: 'EXP Collector',
        description: 'Earn 1000 EXP',
        type: 'earn',
        target: 1000,
        progress: 0,
        reward: {
          quantumCoins: 1000,
          expCoins: 100,
          multiplier: 1.1
        },
        completed: false,
        claimed: false
      },
      {
        id: 'invest_quantum',
        title: 'Quantum Investor',
        description: 'Spend 5000 Quantum Coins on investments',
        type: 'invest',
        target: 5000,
        progress: 0,
        reward: {
          quantumCoins: 2000,
          expCoins: 200,
          multiplier: 1.15
        },
        completed: false,
        claimed: false
      }
    ]
  }

  const generateReferralCode = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    let result = ''
    for (let i = 0; i < 8; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    return result
  }

  const tap = () => {
    const baseReward = 1 * stats.value.multiplier * prestigeMultiplier.value
    const expReward = baseReward * 0.1
    
    stats.value.quantumCoins += baseReward
    stats.value.expCoins += expReward
    stats.value.totalTaps++
    stats.value.experience += expReward
    
    // Check for level up
    if (stats.value.experience >= nextLevelExperience.value) {
      levelUp()
    }
    
    // Update quest progress
    updateQuestProgress('tap', 1)
    
    // Haptic feedback
    window.Telegram?.WebApp?.HapticFeedback?.impactOccurred('light')
  }

  const levelUp = () => {
    stats.value.level++
    stats.value.experience = 0
    stats.value.experienceToNext = nextLevelExperience.value
    stats.value.multiplier += 0.1
    
    // Reward for level up
    stats.value.quantumCoins += stats.value.level * 100
    stats.value.expCoins += stats.value.level * 10
    
    // Haptic feedback
    window.Telegram?.WebApp?.HapticFeedback?.notificationOccurred('success')
  }

  const buyInvestment = (investmentId: string) => {
    const investment = investments.value.find(inv => inv.id === investmentId)
    if (!investment) return false

    const cost = investment.owned ? investment.upgradeCost : investment.cost
    
    if (stats.value.quantumCoins >= cost) {
      stats.value.quantumCoins -= cost
      
      if (!investment.owned) {
        investment.owned = true
        investment.level = 1
      } else {
        investment.level++
      }
      
      // Update upgrade cost
      investment.upgradeCost = Math.floor(investment.upgradeCost * 1.15)
      
      // Update quest progress
      updateQuestProgress('invest', cost)
      
      // Haptic feedback
      window.Telegram?.WebApp?.HapticFeedback?.impactOccurred('medium')
      
      return true
    }
    
    return false
  }

  const updateQuestProgress = (type: string, amount: number) => {
    dailyQuests.value.forEach(quest => {
      if (quest.type === type && !quest.completed) {
        quest.progress += amount
        if (quest.progress >= quest.target) {
          quest.completed = true
          window.Telegram?.WebApp?.HapticFeedback?.notificationOccurred('success')
        }
      }
    })
  }

  const claimQuestReward = (questId: string) => {
    const quest = dailyQuests.value.find(q => q.id === questId)
    if (!quest || !quest.completed || quest.claimed) return false

    stats.value.quantumCoins += quest.reward.quantumCoins
    stats.value.expCoins += quest.reward.expCoins
    stats.value.multiplier *= quest.reward.multiplier
    quest.claimed = true

    return true
  }

  const claimDailyBonus = () => {
    if (dailyBonus.value.claimed) return false

    stats.value.quantumCoins += dailyBonus.value.reward.quantumCoins
    stats.value.expCoins += dailyBonus.value.reward.expCoins
    stats.value.multiplier *= dailyBonus.value.reward.multiplier
    dailyBonus.value.claimed = true

    // Increase next day's bonus
    dailyBonus.value.day++
    dailyBonus.value.reward.quantumCoins = Math.floor(dailyBonus.value.reward.quantumCoins * 1.1)
    dailyBonus.value.reward.expCoins = Math.floor(dailyBonus.value.reward.expCoins * 1.1)

    return true
  }

  const calculateOfflineIncome = () => {
    const lastActive = dayjs(stats.value.lastActive)
    const now = dayjs()
    const hoursOffline = now.diff(lastActive, 'hour', true)
    
    if (hoursOffline > 0) {
      const maxHours = offlineIncomeDuration.value
      const effectiveHours = Math.min(hoursOffline, maxHours)
      const offlineExp = totalExpPerSecond.value * effectiveHours * 3600 * offlineIncomeMultiplier.value
      
      stats.value.expCoins += offlineExp
    }
    
    stats.value.lastActive = now.toISOString()
  }

  const startBackgroundProcesses = () => {
    // Auto-save every 30 seconds
    const saveInterval = setInterval(() => {
      saveGameData()
    }, 30000)
    
    // Update EXP every second
    const expInterval = setInterval(() => {
      if (totalExpPerSecond.value > 0) {
        stats.value.expCoins += totalExpPerSecond.value
      }
    }, 1000)
    
    backgroundProcesses.value.push(saveInterval, expInterval)
  }

  const saveGameData = async () => {
    try {
      const gameData = {
        stats: stats.value,
        investments: investments.value,
        dailyBonus: dailyBonus.value,
        dailyQuests: dailyQuests.value,
        offlineIncomeMultiplier: offlineIncomeMultiplier.value,
        offlineIncomeDuration: offlineIncomeDuration.value,
        lastSaveTime: dayjs().toISOString()
      }
      
      // In a real app, this would save to a backend
      localStorage.setItem('quantum-nexus-save', JSON.stringify(gameData))
    } catch (error) {
      console.error('Failed to save game data:', error)
    }
  }

  const loadGameData = async () => {
    try {
      const savedData = localStorage.getItem('quantum-nexus-save')
      if (savedData) {
        const gameData = JSON.parse(savedData)
        
        stats.value = { ...stats.value, ...gameData.stats }
        investments.value = gameData.investments || investments.value
        dailyBonus.value = gameData.dailyBonus || dailyBonus.value
        dailyQuests.value = gameData.dailyQuests || dailyQuests.value
        offlineIncomeMultiplier.value = gameData.offlineIncomeMultiplier || 1
        offlineIncomeDuration.value = gameData.offlineIncomeDuration || 3
      }
    } catch (error) {
      console.error('Failed to load game data:', error)
    }
  }

  const withdrawExp = (amount: number) => {
    if (stats.value.expCoins >= amount) {
      stats.value.expCoins -= amount
      const usdAmount = amount / 100000 // 100000 EXP = 1 USD
      
      // In a real app, this would process the withdrawal
      return { success: true, usdAmount }
    }
    return { success: false, usdAmount: 0 }
  }

  const addTemporaryMultiplier = (multiplier: number, duration: number) => {
    // Add temporary multiplier logic
    stats.value.multiplier *= multiplier
    setTimeout(() => {
      stats.value.multiplier /= multiplier
    }, duration * 1000)
  }

  const addAutoClicker = (interval: number) => {
    // Add auto-clicker logic
    const autoClickInterval = setInterval(() => {
      tap()
    }, interval)
    
    // Store interval for cleanup
    backgroundProcesses.value.push(autoClickInterval)
  }

  const addOfflineMultiplier = (multiplier: number, duration: number) => {
    // Add offline multiplier logic
    offlineIncomeMultiplier.value *= multiplier
    setTimeout(() => {
      offlineIncomeMultiplier.value /= multiplier
    }, duration * 1000)
  }

  const increaseOfflineDuration = (additionalHours: number) => {
    // Increase offline duration
    offlineIncomeDuration.value += additionalHours / 3600
  }

  const resetGame = () => {
    // Reset all game data
    stats.value = {
      quantumCoins: 0,
      expCoins: 0,
      totalTaps: 0,
      level: 1,
      experience: 0,
      experienceToNext: 100,
      multiplier: 1,
      autoClickerLevel: 0,
      prestigeLevel: 0,
      achievements: [],
      lastActive: dayjs().toISOString(),
      totalPlayTime: 0,
      referralCode: generateReferralCode(),
      referralsCount: 0,
      referralsEarnings: 0
    }
    
    investments.value.forEach(inv => {
      inv.level = 0
      inv.owned = false
      inv.upgradeCost = inv.cost
    })
    
    dailyBonus.value = {
      day: 1,
      claimed: false,
      reward: {
        quantumCoins: 100,
        expCoins: 10,
        multiplier: 1.1
      }
    }
    
    dailyQuests.value.forEach(quest => {
      quest.progress = 0
      quest.completed = false
      quest.claimed = false
    })
    
    offlineIncomeMultiplier.value = 1
    offlineIncomeDuration.value = 3
  }

  return {
    // State
    user,
    stats,
    investments,
    dailyBonus,
    dailyQuests,
    offlineIncomeMultiplier,
    offlineIncomeDuration,
    isPlaying,
    lastSaveTime,
    
    // Computed
    totalExpPerSecond,
    canAffordInvestment,
    nextLevelExperience,
    prestigeMultiplier,
    
    // Actions
    initializeGame,
    tap,
    buyInvestment,
    claimQuestReward,
    claimDailyBonus,
    calculateOfflineIncome,
    startBackgroundProcesses,
    saveGameData,
    loadGameData,
    withdrawExp,
    updateQuestProgress,
    addTemporaryMultiplier,
    addAutoClicker,
    addOfflineMultiplier,
    increaseOfflineDuration,
    resetGame
  }
})
