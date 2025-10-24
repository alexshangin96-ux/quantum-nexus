<template>
  <div class="shop-view">
    <div class="shop-header">
      <h1 class="quantum-title">Quantum Shop</h1>
      <div class="shop-balance">
        <div class="balance-item">
          <span class="balance-icon">⭐</span>
          <span class="balance-label">Telegram Stars</span>
          <span class="balance-value">{{ telegramStars }}</span>
        </div>
      </div>
    </div>

    <div class="shop-categories">
      <button 
        v-for="category in shopCategories" 
        :key="category.id"
        class="category-btn"
        :class="{ active: selectedCategory === category.id }"
        @click="selectedCategory = category.id"
      >
        <span class="category-icon">{{ category.icon }}</span>
        <span class="category-name">{{ category.name }}</span>
      </button>
    </div>

    <!-- Special Offers -->
    <div class="special-offers" v-if="selectedCategory === 'all'">
      <h3 class="offers-title">🔥 Limited Time Offers</h3>
      <div class="offers-grid">
        <div 
          v-for="offer in specialOffers" 
          :key="offer.id"
          class="offer-card"
          :class="{ 'offer-featured': offer.featured }"
        >
          <div class="offer-badge" v-if="offer.featured">FEATURED</div>
          <div class="offer-header">
            <div class="offer-icon">{{ offer.icon }}</div>
            <div class="offer-info">
              <h4 class="offer-name">{{ offer.name }}</h4>
              <p class="offer-description">{{ offer.description }}</p>
            </div>
          </div>
          
          <div class="offer-benefits">
            <div 
              v-for="benefit in offer.benefits" 
              :key="benefit"
              class="benefit-item"
            >
              <span class="benefit-icon">✓</span>
              <span class="benefit-text">{{ benefit }}</span>
            </div>
          </div>
          
          <div class="offer-price">
            <span class="price-value">{{ offer.price }}</span>
            <span class="price-currency">⭐</span>
          </div>
          
          <button 
            class="offer-btn"
            :class="{ 'btn-featured': offer.featured }"
            @click="purchaseItem(offer)"
          >
            {{ offer.featured ? '🔥 BUY NOW' : 'Purchase' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Regular Shop Items -->
    <div class="shop-items">
      <div 
        v-for="item in filteredItems" 
        :key="item.id"
        class="shop-item"
        :class="{ 'item-owned': item.owned }"
      >
        <div class="item-header">
          <div class="item-icon">{{ item.icon }}</div>
          <div class="item-info">
            <h4 class="item-name">{{ item.name }}</h4>
            <p class="item-description">{{ item.description }}</p>
          </div>
          <div class="item-level" v-if="item.level > 0">
            <span class="level-label">Level</span>
            <span class="level-value">{{ item.level }}</span>
          </div>
        </div>

        <div class="item-effects">
          <div 
            v-for="effect in item.effects" 
            :key="effect.type"
            class="effect-item"
          >
            <span class="effect-icon">{{ getEffectIcon(effect.type) }}</span>
            <span class="effect-text">{{ effect.description }}</span>
          </div>
        </div>

        <div class="item-price">
          <span class="price-value">{{ item.price }}</span>
          <span class="price-currency">⭐</span>
          <span class="price-original" v-if="item.originalPrice && item.originalPrice > item.price">
            {{ item.originalPrice }}⭐
          </span>
        </div>

        <button 
          class="item-btn"
          :class="{ 
            'btn-buy': !item.owned, 
            'btn-upgrade': item.owned && item.maxLevel > item.level,
            'btn-max': item.owned && item.level >= item.maxLevel
          }"
          @click="purchaseItem(item)"
          :disabled="item.owned && item.level >= item.maxLevel"
        >
          <span v-if="!item.owned">Buy for {{ item.price }}⭐</span>
          <span v-else-if="item.level < item.maxLevel">Upgrade for {{ item.upgradePrice }}⭐</span>
          <span v-else>Max Level</span>
        </button>
      </div>
    </div>

    <!-- Shop Tips -->
    <div class="shop-tips">
      <h3 class="tips-title">💡 Shop Tips</h3>
      <div class="tips-content">
        <div class="tip-item">
          <span class="tip-icon">⭐</span>
          <span class="tip-text">Telegram Stars can be earned by watching ads or purchasing</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">🎯</span>
          <span class="tip-text">Focus on multipliers and auto-clickers for maximum efficiency</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">⏰</span>
          <span class="tip-text">Offline income boosters work even when you're not playing</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">🔄</span>
          <span class="tip-text">Shop items refresh daily with new offers</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { useTelegramStore } from '@/stores/telegram'

const gameStore = useGameStore()
const telegramStore = useTelegramStore()

const telegramStars = ref(0)
const selectedCategory = ref('all')

const shopCategories = [
  { id: 'all', name: 'All', icon: '🌟' },
  { id: 'multipliers', name: 'Multipliers', icon: '⚡' },
  { id: 'auto_clickers', name: 'Auto Clickers', icon: '🤖' },
  { id: 'offline_boost', name: 'Offline Boost', icon: '⏰' },
  { id: 'cosmetics', name: 'Cosmetics', icon: '🎨' },
  { id: 'special', name: 'Special', icon: '💎' }
]

const specialOffers = [
  {
    id: 'quantum_pack',
    name: 'Quantum Starter Pack',
    description: 'Perfect for new players',
    icon: '🎁',
    price: 50,
    featured: true,
    benefits: [
      '2x Tap Multiplier (24h)',
      '1000 Quantum Coins',
      '100 EXP Coins',
      'Auto Clicker Level 1'
    ]
  },
  {
    id: 'mega_boost',
    name: 'Mega Boost Pack',
    description: 'Maximum efficiency boost',
    icon: '🚀',
    price: 200,
    featured: true,
    benefits: [
      '5x Tap Multiplier (7 days)',
      '10x Offline Income (7 days)',
      '5000 Quantum Coins',
      '500 EXP Coins'
    ]
  }
]

const shopItems = [
  // Multipliers
  {
    id: 'tap_multiplier_1h',
    name: 'Tap Multiplier (1h)',
    description: 'Double your tap rewards for 1 hour',
    icon: '⚡',
    category: 'multipliers',
    price: 25,
    level: 0,
    maxLevel: 1,
    owned: false,
    upgradePrice: 0,
    effects: [
      { type: 'multiplier', description: '+100% Tap Rewards' },
      { type: 'duration', description: '1 Hour Duration' }
    ]
  },
  {
    id: 'tap_multiplier_24h',
    name: 'Tap Multiplier (24h)',
    description: 'Triple your tap rewards for 24 hours',
    icon: '⚡',
    category: 'multipliers',
    price: 100,
    level: 0,
    maxLevel: 1,
    owned: false,
    upgradePrice: 0,
    effects: [
      { type: 'multiplier', description: '+200% Tap Rewards' },
      { type: 'duration', description: '24 Hours Duration' }
    ]
  },
  
  // Auto Clickers
  {
    id: 'auto_clicker_basic',
    name: 'Basic Auto Clicker',
    description: 'Automatically taps every 5 seconds',
    icon: '🤖',
    category: 'auto_clickers',
    price: 75,
    level: 0,
    maxLevel: 10,
    owned: false,
    upgradePrice: 75,
    effects: [
      { type: 'auto_tap', description: '1 Tap per 5 seconds' },
      { type: 'upgradeable', description: 'Can be upgraded' }
    ]
  },
  {
    id: 'auto_clicker_advanced',
    name: 'Advanced Auto Clicker',
    description: 'Automatically taps every 2 seconds',
    icon: '🤖',
    category: 'auto_clickers',
    price: 300,
    level: 0,
    maxLevel: 5,
    owned: false,
    upgradePrice: 300,
    effects: [
      { type: 'auto_tap', description: '1 Tap per 2 seconds' },
      { type: 'upgradeable', description: 'Can be upgraded' }
    ]
  },
  
  // Offline Boost
  {
    id: 'offline_boost_1h',
    name: 'Offline Boost (1h)',
    description: 'Double offline income for 1 hour',
    icon: '⏰',
    category: 'offline_boost',
    price: 30,
    level: 0,
    maxLevel: 1,
    owned: false,
    upgradePrice: 0,
    effects: [
      { type: 'offline_multiplier', description: '+100% Offline Income' },
      { type: 'duration', description: '1 Hour Duration' }
    ]
  },
  {
    id: 'offline_duration_boost',
    name: 'Extended Offline Time',
    description: 'Increase offline income duration',
    icon: '⏰',
    category: 'offline_boost',
    price: 150,
    level: 0,
    maxLevel: 5,
    owned: false,
    upgradePrice: 150,
    effects: [
      { type: 'offline_duration', description: '+1 Hour Offline Duration' },
      { type: 'upgradeable', description: 'Can be upgraded' }
    ]
  },
  
  // Cosmetics
  {
    id: 'quantum_theme',
    name: 'Quantum Theme',
    description: 'Unlock exclusive quantum visual effects',
    icon: '🎨',
    category: 'cosmetics',
    price: 100,
    level: 0,
    maxLevel: 1,
    owned: false,
    upgradePrice: 0,
    effects: [
      { type: 'cosmetic', description: 'Quantum Visual Effects' },
      { type: 'exclusive', description: 'Exclusive Theme' }
    ]
  },
  {
    id: 'premium_particles',
    name: 'Premium Particles',
    description: 'Enhanced particle effects',
    icon: '✨',
    category: 'cosmetics',
    price: 80,
    level: 0,
    maxLevel: 1,
    owned: false,
    upgradePrice: 0,
    effects: [
      { type: 'cosmetic', description: 'Enhanced Particles' },
      { type: 'visual', description: 'Better Visual Experience' }
    ]
  }
]

const filteredItems = computed(() => {
  if (selectedCategory.value === 'all') {
    return shopItems
  }
  return shopItems.filter(item => item.category === selectedCategory.value)
})

const getEffectIcon = (type: string): string => {
  const icons: Record<string, string> = {
    multiplier: '⚡',
    duration: '⏰',
    auto_tap: '🤖',
    upgradeable: '📈',
    offline_multiplier: '💤',
    offline_duration: '⏳',
    cosmetic: '🎨',
    exclusive: '💎',
    visual: '✨'
  }
  return icons[type] || '📊'
}

const purchaseItem = async (item: any) => {
  if (telegramStars.value < item.price) {
    telegramStore.showAlert('Not enough Telegram Stars!')
    return
  }

  try {
    // In a real app, this would process the payment through Telegram Stars
    const success = await processTelegramStarsPayment(item.price)
    
    if (success) {
      telegramStars.value -= item.price
      applyItemEffect(item)
      telegramStore.showAlert(`Successfully purchased ${item.name}!`)
      telegramStore.impactFeedback('medium')
    } else {
      telegramStore.showAlert('Payment failed!')
    }
  } catch (error) {
    console.error('Purchase error:', error)
    telegramStore.showAlert('Purchase failed!')
  }
}

const processTelegramStarsPayment = async (amount: number): Promise<boolean> => {
  // This would integrate with Telegram Stars API
  // For now, we'll simulate the payment
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true)
    }, 1000)
  })
}

const applyItemEffect = (item: any) => {
  // Apply the item's effects to the game
  switch (item.id) {
    case 'tap_multiplier_1h':
      gameStore.addTemporaryMultiplier(2, 3600) // 2x for 1 hour
      break
    case 'tap_multiplier_24h':
      gameStore.addTemporaryMultiplier(3, 86400) // 3x for 24 hours
      break
    case 'auto_clicker_basic':
      gameStore.addAutoClicker(5000) // Every 5 seconds
      break
    case 'auto_clicker_advanced':
      gameStore.addAutoClicker(2000) // Every 2 seconds
      break
    case 'offline_boost_1h':
      gameStore.addOfflineMultiplier(2, 3600) // 2x for 1 hour
      break
    case 'offline_duration_boost':
      gameStore.increaseOfflineDuration(3600) // +1 hour
      break
    // Add more cases as needed
  }
}

const loadTelegramStars = async () => {
  // This would load the user's Telegram Stars balance
  // For now, we'll simulate it
  telegramStars.value = 500
}

onMounted(() => {
  loadTelegramStars()
})
</script>

<style scoped>
.shop-view {
  padding: 20px;
  min-height: 100vh;
}

.shop-header {
  margin-bottom: 30px;
}

.shop-balance {
  margin-top: 20px;
}

.balance-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  padding: 15px 20px;
  max-width: 300px;
}

.balance-icon {
  font-size: 24px;
}

.balance-label {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.balance-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-accent);
}

.shop-categories {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.category-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 25px;
  color: var(--quantum-text-dim);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.category-btn:hover {
  border-color: var(--quantum-primary);
  color: var(--quantum-primary);
}

.category-btn.active {
  background: rgba(0, 255, 255, 0.2);
  border-color: var(--quantum-primary);
  color: var(--quantum-primary);
  box-shadow: 0 0 15px var(--quantum-glow);
}

.category-icon {
  font-size: 16px;
}

.special-offers {
  margin-bottom: 40px;
}

.offers-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--quantum-primary);
  margin-bottom: 20px;
  text-align: center;
}

.offers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.offer-card {
  position: relative;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.offer-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.offer-card.offer-featured {
  border-color: var(--quantum-accent);
  background: linear-gradient(135deg, rgba(255, 255, 0, 0.1), rgba(26, 26, 46, 0.8));
}

.offer-badge {
  position: absolute;
  top: -10px;
  right: 20px;
  background: linear-gradient(45deg, var(--quantum-accent), var(--quantum-primary));
  color: var(--quantum-dark);
  padding: 5px 15px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.offer-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.offer-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  border-radius: 12px;
  flex-shrink: 0;
}

.offer-info {
  flex: 1;
}

.offer-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.offer-description {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.offer-benefits {
  margin-bottom: 20px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.benefit-icon {
  color: var(--quantum-success);
  font-weight: 700;
}

.benefit-text {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.offer-price {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin-bottom: 15px;
}

.price-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--quantum-accent);
}

.price-currency {
  font-size: 20px;
}

.offer-btn {
  width: 100%;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  color: var(--quantum-dark);
}

.btn-featured {
  background: linear-gradient(45deg, var(--quantum-accent), var(--quantum-primary));
  animation: quantum-pulse 2s ease-in-out infinite;
}

.offer-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--quantum-glow);
}

.shop-items {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.shop-item {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.shop-item:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.shop-item.item-owned {
  border-color: var(--quantum-success);
}

.item-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.item-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  border-radius: 12px;
  flex-shrink: 0;
}

.item-info {
  flex: 1;
}

.item-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.item-description {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.item-level {
  text-align: center;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 8px;
  padding: 8px 12px;
}

.level-label {
  display: block;
  font-size: 12px;
  color: var(--quantum-text-dim);
  margin-bottom: 2px;
}

.level-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-primary);
}

.item-effects {
  margin-bottom: 15px;
}

.effect-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.effect-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.effect-text {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.item-price {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin-bottom: 15px;
}

.price-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--quantum-accent);
}

.price-currency {
  font-size: 18px;
}

.price-original {
  font-size: 16px;
  color: var(--quantum-text-dim);
  text-decoration: line-through;
  margin-left: 10px;
}

.item-btn {
  width: 100%;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-buy {
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  color: var(--quantum-dark);
}

.btn-upgrade {
  background: linear-gradient(45deg, var(--quantum-success), var(--quantum-accent));
  color: var(--quantum-dark);
}

.btn-max {
  background: rgba(100, 100, 100, 0.3);
  color: var(--quantum-text-dim);
  cursor: not-allowed;
}

.item-btn:hover:not(.btn-max) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--quantum-glow);
}

.shop-tips {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
}

.tips-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-primary);
  margin-bottom: 15px;
  text-align: center;
}

.tips-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(0, 255, 255, 0.05);
  border-radius: 8px;
}

.tip-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.tip-text {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

@media (max-width: 768px) {
  .shop-view {
    padding: 15px;
  }
  
  .offers-grid,
  .shop-items {
    grid-template-columns: 1fr;
  }
  
  .shop-categories {
    gap: 8px;
  }
  
  .category-btn {
    padding: 10px 16px;
    font-size: 13px;
  }
  
  .tips-content {
    grid-template-columns: 1fr;
  }
}
</style>