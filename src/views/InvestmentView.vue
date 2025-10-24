<template>
  <div class="investment-view">
    <div class="investment-header">
      <h1 class="quantum-title">Quantum Investments</h1>
      <div class="investment-stats">
        <div class="stat-card">
          <div class="stat-icon">⚡</div>
          <div class="stat-info">
            <div class="stat-label">Total EXP/sec</div>
            <div class="stat-value quantum-text-glow">{{ formatNumber(totalExpPerSecond) }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <div class="stat-label">Quantum Coins</div>
            <div class="stat-value quantum-text-glow">{{ formatNumber(stats.quantumCoins) }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">💎</div>
          <div class="stat-info">
            <div class="stat-label">EXP Coins</div>
            <div class="stat-value quantum-text-glow">{{ formatNumber(stats.expCoins) }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="investment-categories">
      <button 
        v-for="category in categories" 
        :key="category.id"
        class="category-btn"
        :class="{ active: selectedCategory === category.id }"
        @click="selectedCategory = category.id"
      >
        <span class="category-icon">{{ category.icon }}</span>
        <span class="category-name">{{ category.name }}</span>
      </button>
    </div>

    <div class="investments-grid">
      <div 
        v-for="investment in filteredInvestments" 
        :key="investment.id"
        class="investment-card"
        :class="{ owned: investment.owned, affordable: canAffordInvestment(investment) }"
      >
        <div class="investment-header-card">
          <div class="investment-icon">{{ getInvestmentIcon(investment.category) }}</div>
          <div class="investment-info">
            <h3 class="investment-name">{{ investment.name }}</h3>
            <p class="investment-description">{{ investment.description }}</p>
          </div>
          <div class="investment-level" v-if="investment.owned">
            <span class="level-label">Level</span>
            <span class="level-value">{{ investment.level }}</span>
          </div>
        </div>

        <div class="investment-stats-card">
          <div class="stat-row">
            <span class="stat-label">EXP/sec:</span>
            <span class="stat-value quantum-text">{{ formatNumber(investment.expPerSecond * investment.level) }}</span>
          </div>
          
          <div class="stat-row" v-if="investment.owned">
            <span class="stat-label">Next Level:</span>
            <span class="stat-value">{{ formatNumber(investment.upgradeCost) }}</span>
          </div>
          
          <div class="stat-row" v-else>
            <span class="stat-label">Cost:</span>
            <span class="stat-value">{{ formatNumber(investment.cost) }}</span>
          </div>
        </div>

        <div class="investment-progress" v-if="investment.owned">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: getProgressPercent(investment) + '%' }"
            ></div>
          </div>
          <div class="progress-text">
            {{ investment.level }} / {{ investment.maxLevel }}
          </div>
        </div>

        <button 
          class="investment-btn"
          :class="{ 
            'btn-buy': !investment.owned, 
            'btn-upgrade': investment.owned,
            'btn-disabled': !canAffordInvestment(investment) || (investment.owned && investment.level >= investment.maxLevel)
          }"
          @click="handleInvestmentAction(investment)"
          :disabled="!canAffordInvestment(investment) || (investment.owned && investment.level >= investment.maxLevel)"
        >
          <span v-if="!investment.owned">Buy for {{ formatNumber(investment.cost) }}</span>
          <span v-else-if="investment.level < investment.maxLevel">Upgrade for {{ formatNumber(investment.upgradeCost) }}</span>
          <span v-else>Max Level</span>
        </button>
      </div>
    </div>

    <!-- Investment Tips -->
    <div class="investment-tips">
      <h3 class="tips-title">💡 Investment Tips</h3>
      <div class="tips-content">
        <div class="tip-item">
          <span class="tip-icon">⚛️</span>
          <span class="tip-text">Start with Quantum Core for steady EXP generation</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">📈</span>
          <span class="tip-text">Higher level investments provide exponential returns</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">🎯</span>
          <span class="tip-text">Focus on one investment category for maximum efficiency</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">⏰</span>
          <span class="tip-text">EXP generates continuously, even when offline</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useGameStore } from '@/stores/game'
import { useTelegramStore } from '@/stores/telegram'
import type { Investment } from '@/stores/game'

const gameStore = useGameStore()
const telegramStore = useTelegramStore()

const { stats, investments, totalExpPerSecond, canAffordInvestment } = storeToRefs(gameStore)

const selectedCategory = ref<string>('all')

const categories = [
  { id: 'all', name: 'All', icon: '🌟' },
  { id: 'quantum', name: 'Quantum', icon: '⚛️' },
  { id: 'crypto', name: 'Crypto', icon: '₿' },
  { id: 'stocks', name: 'Stocks', icon: '📈' },
  { id: 'real_estate', name: 'Real Estate', icon: '🏠' },
  { id: 'tech', name: 'Tech', icon: '🤖' }
]

const filteredInvestments = computed(() => {
  if (selectedCategory.value === 'all') {
    return investments.value
  }
  return investments.value.filter(inv => inv.category === selectedCategory.value)
})

const formatNumber = (num: number): string => {
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return Math.floor(num).toString()
}

const getInvestmentIcon = (category: string): string => {
  const icons: Record<string, string> = {
    quantum: '⚛️',
    crypto: '₿',
    stocks: '📈',
    real_estate: '🏠',
    tech: '🤖'
  }
  return icons[category] || '💼'
}

const getProgressPercent = (investment: Investment): number => {
  return (investment.level / investment.maxLevel) * 100
}

const handleInvestmentAction = (investment: Investment) => {
  if (!canAffordInvestment.value(investment)) {
    telegramStore.showAlert('Not enough Quantum Coins!')
    return
  }

  if (investment.owned && investment.level >= investment.maxLevel) {
    telegramStore.showAlert('Investment is at maximum level!')
    return
  }

  const success = gameStore.buyInvestment(investment.id)
  
  if (success) {
    const action = investment.owned ? 'upgraded' : 'purchased'
    telegramStore.showAlert(`Successfully ${action} ${investment.name}!`)
    telegramStore.impactFeedback('medium')
  } else {
    telegramStore.showAlert('Purchase failed!')
  }
}
</script>

<style scoped>
.investment-view {
  padding: 20px;
  min-height: 100vh;
}

.investment-header {
  margin-bottom: 30px;
}

.investment-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.stat-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 20px var(--quantum-glow);
}

.stat-icon {
  font-size: 28px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  border-radius: 50%;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: var(--quantum-text-dim);
  margin-bottom: 5px;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
}

.investment-categories {
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

.investments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.investment-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.investment-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.investment-card.owned {
  border-color: var(--quantum-success);
}

.investment-card.affordable {
  border-color: var(--quantum-accent);
}

.investment-header-card {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.investment-icon {
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

.investment-info {
  flex: 1;
}

.investment-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.investment-description {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.investment-level {
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

.investment-stats-card {
  margin-bottom: 15px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.stat-row .stat-label {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.stat-row .stat-value {
  font-size: 14px;
  font-weight: 600;
}

.investment-progress {
  margin-bottom: 15px;
}

.progress-bar {
  height: 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--quantum-primary), var(--quantum-secondary));
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-size: 12px;
  color: var(--quantum-text-dim);
}

.investment-btn {
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

.btn-disabled {
  background: rgba(100, 100, 100, 0.3);
  color: var(--quantum-text-dim);
  cursor: not-allowed;
}

.investment-btn:hover:not(.btn-disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--quantum-glow);
}

.investment-tips {
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
  .investment-view {
    padding: 15px;
  }
  
  .investment-stats {
    grid-template-columns: 1fr;
  }
  
  .investments-grid {
    grid-template-columns: 1fr;
  }
  
  .investment-categories {
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