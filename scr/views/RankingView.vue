<template>
  <div class="ranking-view">
    <div class="ranking-header">
      <h1 class="quantum-title">Quantum Rankings</h1>
      <div class="ranking-info">
        <div class="info-item">
          <span class="info-icon">🏆</span>
          <span class="info-text">Your Rank: #{{ userRank }}</span>
        </div>
        <div class="info-item">
          <span class="info-icon">⭐</span>
          <span class="info-text">Total Players: {{ totalPlayers }}</span>
        </div>
      </div>
    </div>

    <!-- Ranking Categories -->
    <div class="ranking-categories">
      <button 
        v-for="category in rankingCategories" 
        :key="category.id"
        class="category-btn"
        :class="{ active: selectedCategory === category.id }"
        @click="selectedCategory = category.id"
      >
        <span class="category-icon">{{ category.icon }}</span>
        <span class="category-name">{{ category.name }}</span>
      </button>
    </div>

    <!-- Top Players -->
    <div class="top-players-section">
      <h2 class="section-title">🏆 Top Players</h2>
      <div class="top-players">
        <div 
          v-for="(player, index) in topPlayers" 
          :key="player.id"
          class="player-card"
          :class="{ 
            'player-gold': index === 0,
            'player-silver': index === 1,
            'player-bronze': index === 2,
            'player-current': player.id === currentUserId
          }"
        >
          <div class="player-rank">
            <span class="rank-number">{{ index + 1 }}</span>
            <span class="rank-medal" v-if="index < 3">{{ getMedalIcon(index) }}</span>
          </div>
          
          <div class="player-info">
            <div class="player-avatar">
              <img v-if="player.avatar" :src="player.avatar" :alt="player.name">
              <div v-else class="avatar-placeholder">{{ player.name.charAt(0) }}</div>
            </div>
            <div class="player-details">
              <h4 class="player-name">{{ player.name }}</h4>
              <p class="player-level">Level {{ player.level }}</p>
            </div>
          </div>
          
          <div class="player-stats">
            <div class="stat-item">
              <span class="stat-label">EXP</span>
              <span class="stat-value">{{ formatNumber(player.expCoins) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Taps</span>
              <span class="stat-value">{{ formatNumber(player.totalTaps) }}</span>
            </div>
          </div>
          
          <div class="player-score">
            <span class="score-label">Score</span>
            <span class="score-value">{{ formatNumber(player.score) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Weekly Rewards -->
    <div class="weekly-rewards-section">
      <h2 class="section-title">🎁 Weekly Rewards</h2>
      <div class="rewards-card">
        <div class="rewards-header">
          <div class="rewards-icon">🎁</div>
          <div class="rewards-info">
            <h3 class="rewards-title">Weekly Competition</h3>
            <p class="rewards-description">Compete for amazing rewards every week!</p>
          </div>
          <div class="rewards-time">
            <span class="time-icon">⏰</span>
            <span class="time-text">{{ timeUntilWeeklyReset }}</span>
          </div>
        </div>

        <div class="rewards-tiers">
          <div class="tier-item">
            <div class="tier-rank">🥇</div>
            <div class="tier-info">
              <h4 class="tier-title">Gold Tier (Top 10)</h4>
              <div class="tier-rewards">
                <span class="reward-item">10,000 EXP</span>
                <span class="reward-item">5x Multiplier (7 days)</span>
                <span class="reward-item">Exclusive Avatar</span>
              </div>
            </div>
          </div>
          
          <div class="tier-item">
            <div class="tier-rank">🥈</div>
            <div class="tier-info">
              <h4 class="tier-title">Silver Tier (Top 50)</h4>
              <div class="tier-rewards">
                <span class="reward-item">5,000 EXP</span>
                <span class="reward-item">3x Multiplier (7 days)</span>
                <span class="reward-item">Premium Theme</span>
              </div>
            </div>
          </div>
          
          <div class="tier-item">
            <div class="tier-rank">🥉</div>
            <div class="tier-info">
              <h4 class="tier-title">Bronze Tier (Top 100)</h4>
              <div class="tier-rewards">
                <span class="reward-item">2,500 EXP</span>
                <span class="reward-item">2x Multiplier (7 days)</span>
                <span class="reward-item">Special Particles</span>
              </div>
            </div>
          </div>
        </div>

        <div class="rewards-progress">
          <div class="progress-info">
            <span class="progress-label">Your Current Rank</span>
            <span class="progress-value">#{{ userRank }}</span>
          </div>
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: getRankProgressPercent() + '%' }"
            ></div>
          </div>
          <div class="progress-text">
            {{ getRankProgressText() }}
          </div>
        </div>
      </div>
    </div>

    <!-- Achievement Leaderboard -->
    <div class="achievements-section">
      <h2 class="section-title">🏅 Achievement Leaders</h2>
      <div class="achievements-grid">
        <div 
          v-for="achievement in achievementLeaders" 
          :key="achievement.id"
          class="achievement-card"
        >
          <div class="achievement-header">
            <div class="achievement-icon">{{ achievement.icon }}</div>
            <div class="achievement-info">
              <h4 class="achievement-name">{{ achievement.name }}</h4>
              <p class="achievement-description">{{ achievement.description }}</p>
            </div>
          </div>
          
          <div class="achievement-leader">
            <div class="leader-avatar">
              <img v-if="achievement.leader.avatar" :src="achievement.leader.avatar" :alt="achievement.leader.name">
              <div v-else class="avatar-placeholder">{{ achievement.leader.name.charAt(0) }}</div>
            </div>
            <div class="leader-info">
              <h5 class="leader-name">{{ achievement.leader.name }}</h5>
              <p class="leader-score">{{ formatNumber(achievement.leader.score) }} points</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Ranking Tips -->
    <div class="ranking-tips">
      <h3 class="tips-title">💡 Ranking Tips</h3>
      <div class="tips-content">
        <div class="tip-item">
          <span class="tip-icon">⚡</span>
          <span class="tip-text">Higher multipliers give more EXP per tap</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">🏢</span>
          <span class="tip-text">Investments provide passive EXP income</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">📅</span>
          <span class="tip-text">Complete daily quests for bonus multipliers</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">👥</span>
          <span class="tip-text">Refer friends for additional EXP bonuses</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { useTelegramStore } from '@/stores/telegram'
import dayjs from 'dayjs'

const gameStore = useGameStore()
const telegramStore = useTelegramStore()

const { stats } = storeToRefs(gameStore)

const selectedCategory = ref('exp')
const userRank = ref(1)
const totalPlayers = ref(10000)
const currentUserId = ref('current-user')
const timeUntilWeeklyReset = ref('')

let timeInterval: NodeJS.Timeout

const rankingCategories = [
  { id: 'exp', name: 'EXP Coins', icon: '💎' },
  { id: 'taps', name: 'Total Taps', icon: '👆' },
  { id: 'level', name: 'Level', icon: '⭐' },
  { id: 'investments', name: 'Investments', icon: '🏢' },
  { id: 'referrals', name: 'Referrals', icon: '👥' }
]

const topPlayers = ref([
  {
    id: 'player-1',
    name: 'QuantumMaster',
    level: 150,
    expCoins: 2500000,
    totalTaps: 500000,
    score: 2750000,
    avatar: null
  },
  {
    id: 'player-2',
    name: 'NexusPro',
    level: 145,
    expCoins: 2400000,
    totalTaps: 480000,
    score: 2640000,
    avatar: null
  },
  {
    id: 'player-3',
    name: 'TapKing',
    level: 140,
    expCoins: 2300000,
    totalTaps: 460000,
    score: 2530000,
    avatar: null
  },
  {
    id: 'current-user',
    name: 'You',
    level: stats.value.level,
    expCoins: stats.value.expCoins,
    totalTaps: stats.value.totalTaps,
    score: stats.value.expCoins + stats.value.totalTaps * 0.1,
    avatar: null
  },
  {
    id: 'player-5',
    name: 'QuantumRookie',
    level: 135,
    expCoins: 2200000,
    totalTaps: 440000,
    score: 2420000,
    avatar: null
  }
])

const achievementLeaders = ref([
  {
    id: 'tap-master',
    name: 'Tap Master',
    description: 'Most taps in a single session',
    icon: '👆',
    leader: {
      name: 'TapKing',
      score: 50000,
      avatar: null
    }
  },
  {
    id: 'investment-guru',
    name: 'Investment Guru',
    description: 'Highest investment portfolio value',
    icon: '🏢',
    leader: {
      name: 'QuantumMaster',
      score: 1000000,
      avatar: null
    }
  },
  {
    id: 'referral-champion',
    name: 'Referral Champion',
    description: 'Most successful referrals',
    icon: '👥',
    leader: {
      name: 'NexusPro',
      score: 50,
      avatar: null
    }
  },
  {
    id: 'daily-warrior',
    name: 'Daily Warrior',
    description: 'Longest daily streak',
    icon: '📅',
    leader: {
      name: 'QuantumRookie',
      score: 365,
      avatar: null
    }
  }
])

const formatNumber = (num: number): string => {
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return Math.floor(num).toString()
}

const getMedalIcon = (index: number): string => {
  const medals = ['🥇', '🥈', '🥉']
  return medals[index] || ''
}

const getRankProgressPercent = (): number => {
  if (userRank.value <= 10) return 100
  if (userRank.value <= 50) return 80
  if (userRank.value <= 100) return 60
  return Math.max(0, 100 - userRank.value)
}

const getRankProgressText = (): string => {
  if (userRank.value <= 10) return 'Elite Tier'
  if (userRank.value <= 50) return 'Gold Tier'
  if (userRank.value <= 100) return 'Silver Tier'
  return 'Bronze Tier'
}

const updateTimeUntilWeeklyReset = () => {
  const now = dayjs()
  const nextMonday = now.add(1, 'week').startOf('week').add(1, 'day')
  const diff = nextMonday.diff(now)
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  
  timeUntilWeeklyReset.value = `${days}d ${hours}h`
}

onMounted(() => {
  updateTimeUntilWeeklyReset()
  
  timeInterval = setInterval(() => {
    updateTimeUntilWeeklyReset()
  }, 1000)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
.ranking-view {
  padding: 20px;
  min-height: 100vh;
}

.ranking-header {
  margin-bottom: 30px;
}

.ranking-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  padding: 15px 20px;
}

.info-icon {
  font-size: 20px;
}

.info-text {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--quantum-primary);
  margin-bottom: 20px;
  text-align: center;
}

.ranking-categories {
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

.top-players-section {
  margin-bottom: 40px;
}

.top-players {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.player-card {
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.player-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.player-card.player-gold {
  border-color: #ffd700;
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(26, 26, 46, 0.8));
}

.player-card.player-silver {
  border-color: #c0c0c0;
  background: linear-gradient(135deg, rgba(192, 192, 192, 0.1), rgba(26, 26, 46, 0.8));
}

.player-card.player-bronze {
  border-color: #cd7f32;
  background: linear-gradient(135deg, rgba(205, 127, 50, 0.1), rgba(26, 26, 46, 0.8));
}

.player-card.player-current {
  border-color: var(--quantum-primary);
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(26, 26, 46, 0.8));
}

.player-rank {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  min-width: 60px;
}

.rank-number {
  font-size: 24px;
  font-weight: 700;
  color: var(--quantum-primary);
}

.rank-medal {
  font-size: 20px;
}

.player-info {
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
}

.player-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid var(--quantum-primary);
}

.player-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: var(--quantum-dark);
  font-size: 18px;
}

.player-details {
  flex: 1;
}

.player-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.player-level {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.player-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.stat-label {
  font-size: 12px;
  color: var(--quantum-text-dim);
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--quantum-primary);
}

.player-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  min-width: 80px;
}

.score-label {
  font-size: 12px;
  color: var(--quantum-text-dim);
}

.score-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-accent);
}

.weekly-rewards-section {
  margin-bottom: 40px;
}

.rewards-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.rewards-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.rewards-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 20px;
}

.rewards-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, var(--quantum-accent), var(--quantum-primary));
  border-radius: 12px;
  flex-shrink: 0;
}

.rewards-info {
  flex: 1;
}

.rewards-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.rewards-description {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.rewards-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.time-icon {
  font-size: 20px;
}

.time-text {
  font-size: 12px;
  color: var(--quantum-text-dim);
  font-weight: 600;
}

.rewards-tiers {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.tier-item {
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(0, 255, 255, 0.05);
  border-radius: 12px;
  padding: 15px;
}

.tier-rank {
  font-size: 32px;
  flex-shrink: 0;
}

.tier-info {
  flex: 1;
}

.tier-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 8px;
}

.tier-rewards {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.reward-item {
  background: rgba(0, 255, 255, 0.1);
  color: var(--quantum-primary);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.rewards-progress {
  background: rgba(0, 255, 255, 0.05);
  border-radius: 12px;
  padding: 15px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.progress-label {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.progress-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-primary);
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

.achievements-section {
  margin-bottom: 40px;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.achievement-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.achievement-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.achievement-icon {
  font-size: 28px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  border-radius: 10px;
  flex-shrink: 0;
}

.achievement-info {
  flex: 1;
}

.achievement-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.achievement-description {
  font-size: 13px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.achievement-leader {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(0, 255, 255, 0.05);
  border-radius: 8px;
  padding: 10px;
}

.leader-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid var(--quantum-primary);
}

.leader-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.leader-info {
  flex: 1;
}

.leader-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--quantum-text);
  margin-bottom: 2px;
}

.leader-score {
  font-size: 12px;
  color: var(--quantum-text-dim);
}

.ranking-tips {
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
  .ranking-view {
    padding: 15px;
  }
  
  .player-card {
    flex-direction: column;
    text-align: center;
  }
  
  .player-stats {
    justify-content: center;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .tips-content {
    grid-template-columns: 1fr;
  }
}
</style>