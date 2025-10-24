<template>
  <div class="daily-view">
    <div class="daily-header">
      <h1 class="quantum-title">Daily Quantum</h1>
      <div class="daily-info">
        <div class="info-item">
          <span class="info-icon">📅</span>
          <span class="info-text">Day {{ dailyBonus.day }} of your quantum journey</span>
        </div>
        <div class="info-item">
          <span class="info-icon">⏰</span>
          <span class="info-text">Next reset in {{ timeUntilReset }}</span>
        </div>
      </div>
    </div>

    <!-- Daily Bonus -->
    <div class="daily-bonus-section">
      <h2 class="section-title">🎁 Daily Bonus</h2>
      <div class="bonus-card" :class="{ 'bonus-claimed': dailyBonus.claimed }">
        <div class="bonus-header">
          <div class="bonus-icon">🎁</div>
          <div class="bonus-info">
            <h3 class="bonus-title">Day {{ dailyBonus.day }} Bonus</h3>
            <p class="bonus-description">Claim your daily quantum rewards!</p>
          </div>
          <div class="bonus-status" v-if="dailyBonus.claimed">
            <span class="status-icon">✅</span>
            <span class="status-text">Claimed</span>
          </div>
        </div>

        <div class="bonus-rewards">
          <div class="reward-item">
            <span class="reward-icon">⚛️</span>
            <span class="reward-amount">{{ formatNumber(dailyBonus.reward.quantumCoins) }}</span>
            <span class="reward-label">Quantum Coins</span>
          </div>
          <div class="reward-item">
            <span class="reward-icon">💎</span>
            <span class="reward-amount">{{ formatNumber(dailyBonus.reward.expCoins) }}</span>
            <span class="reward-label">EXP Coins</span>
          </div>
          <div class="reward-item">
            <span class="reward-icon">⚡</span>
            <span class="reward-amount">x{{ dailyBonus.reward.multiplier.toFixed(2) }}</span>
            <span class="reward-label">Multiplier</span>
          </div>
        </div>

        <button 
          class="bonus-btn"
          :class="{ 'btn-claimed': dailyBonus.claimed }"
          @click="claimDailyBonus"
          :disabled="dailyBonus.claimed"
        >
          <span v-if="!dailyBonus.claimed">🎁 Claim Bonus</span>
          <span v-else>✅ Already Claimed</span>
        </button>
      </div>
    </div>

    <!-- Daily Quests -->
    <div class="daily-quests-section">
      <h2 class="section-title">🎯 Daily Quests</h2>
      <div class="quests-grid">
        <div 
          v-for="quest in dailyQuests" 
          :key="quest.id"
          class="quest-card"
          :class="{ 
            'quest-completed': quest.completed, 
            'quest-claimed': quest.claimed 
          }"
        >
          <div class="quest-header">
            <div class="quest-icon">{{ getQuestIcon(quest.type) }}</div>
            <div class="quest-info">
              <h4 class="quest-title">{{ quest.title }}</h4>
              <p class="quest-description">{{ quest.description }}</p>
            </div>
            <div class="quest-status">
              <span v-if="quest.claimed" class="status-icon">✅</span>
              <span v-else-if="quest.completed" class="status-icon">🎯</span>
              <span v-else class="status-icon">⏳</span>
            </div>
          </div>

          <div class="quest-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: getQuestProgressPercent(quest) + '%' }"
              ></div>
            </div>
            <div class="progress-text">
              {{ formatNumber(quest.progress) }} / {{ formatNumber(quest.target) }}
            </div>
          </div>

          <div class="quest-rewards">
            <div class="reward-item">
              <span class="reward-icon">⚛️</span>
              <span class="reward-amount">{{ formatNumber(quest.reward.quantumCoins) }}</span>
            </div>
            <div class="reward-item">
              <span class="reward-icon">💎</span>
              <span class="reward-amount">{{ formatNumber(quest.reward.expCoins) }}</span>
            </div>
            <div class="reward-item">
              <span class="reward-icon">⚡</span>
              <span class="reward-amount">x{{ quest.reward.multiplier.toFixed(2) }}</span>
            </div>
          </div>

          <button 
            class="quest-btn"
            :class="{ 
              'btn-completed': quest.completed && !quest.claimed,
              'btn-claimed': quest.claimed,
              'btn-disabled': !quest.completed || quest.claimed
            }"
            @click="claimQuestReward(quest.id)"
            :disabled="!quest.completed || quest.claimed"
          >
            <span v-if="quest.claimed">✅ Claimed</span>
            <span v-else-if="quest.completed">🎁 Claim Reward</span>
            <span v-else>⏳ In Progress</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Weekly Challenge -->
    <div class="weekly-challenge-section">
      <h2 class="section-title">🏆 Weekly Challenge</h2>
      <div class="challenge-card">
        <div class="challenge-header">
          <div class="challenge-icon">🏆</div>
          <div class="challenge-info">
            <h3 class="challenge-title">Quantum Master</h3>
            <p class="challenge-description">Reach the top 100 players this week</p>
          </div>
          <div class="challenge-time">
            <span class="time-icon">⏰</span>
            <span class="time-text">{{ timeUntilWeeklyReset }}</span>
          </div>
        </div>

        <div class="challenge-progress">
          <div class="progress-info">
            <span class="progress-label">Current Rank</span>
            <span class="progress-value">#{{ currentRank }}</span>
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

        <div class="challenge-rewards">
          <h4 class="rewards-title">Weekly Rewards</h4>
          <div class="rewards-list">
            <div class="reward-item">
              <span class="reward-icon">🥇</span>
              <span class="reward-text">Top 10: 10,000 EXP + 5x Multiplier</span>
            </div>
            <div class="reward-item">
              <span class="reward-icon">🥈</span>
              <span class="reward-text">Top 50: 5,000 EXP + 3x Multiplier</span>
            </div>
            <div class="reward-item">
              <span class="reward-icon">🥉</span>
              <span class="reward-text">Top 100: 2,500 EXP + 2x Multiplier</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Daily Tips -->
    <div class="daily-tips">
      <h3 class="tips-title">💡 Daily Tips</h3>
      <div class="tips-content">
        <div class="tip-item">
          <span class="tip-icon">📅</span>
          <span class="tip-text">Daily bonuses increase each day - don't miss them!</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">🎯</span>
          <span class="tip-text">Complete all daily quests for maximum rewards</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">🏆</span>
          <span class="tip-text">Weekly challenges reset every Monday</span>
        </div>
        <div class="tip-item">
          <span class="tip-icon">⚡</span>
          <span class="tip-text">Multipliers stack - use them strategically</span>
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

const { dailyBonus, dailyQuests } = storeToRefs(gameStore)

const timeUntilReset = ref('')
const timeUntilWeeklyReset = ref('')
const currentRank = ref(1)

let timeInterval: NodeJS.Timeout

const formatNumber = (num: number): string => {
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return Math.floor(num).toString()
}

const getQuestIcon = (type: string): string => {
  const icons: Record<string, string> = {
    tap: '👆',
    earn: '💰',
    invest: '🏢',
    referral: '👥',
    time: '⏰'
  }
  return icons[type] || '🎯'
}

const getQuestProgressPercent = (quest: any): number => {
  return Math.min((quest.progress / quest.target) * 100, 100)
}

const claimDailyBonus = () => {
  if (dailyBonus.value.claimed) return

  const success = gameStore.claimDailyBonus()
  if (success) {
    telegramStore.showAlert('Daily bonus claimed successfully!')
    telegramStore.impactFeedback('medium')
  }
}

const claimQuestReward = (questId: string) => {
  const success = gameStore.claimQuestReward(questId)
  if (success) {
    telegramStore.showAlert('Quest reward claimed successfully!')
    telegramStore.impactFeedback('medium')
  }
}

const updateTimeUntilReset = () => {
  const now = dayjs()
  const tomorrow = now.add(1, 'day').startOf('day')
  const diff = tomorrow.diff(now)
  
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  const seconds = Math.floor((diff % (1000 * 60)) / 1000)
  
  timeUntilReset.value = `${hours}h ${minutes}m ${seconds}s`
}

const updateTimeUntilWeeklyReset = () => {
  const now = dayjs()
  const nextMonday = now.add(1, 'week').startOf('week').add(1, 'day')
  const diff = nextMonday.diff(now)
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  
  timeUntilWeeklyReset.value = `${days}d ${hours}h`
}

const getRankProgressPercent = (): number => {
  if (currentRank.value <= 10) return 100
  if (currentRank.value <= 50) return 80
  if (currentRank.value <= 100) return 60
  return Math.max(0, 100 - currentRank.value)
}

const getRankProgressText = (): string => {
  if (currentRank.value <= 10) return 'Elite Tier'
  if (currentRank.value <= 50) return 'Gold Tier'
  if (currentRank.value <= 100) return 'Silver Tier'
  return 'Bronze Tier'
}

onMounted(() => {
  updateTimeUntilReset()
  updateTimeUntilWeeklyReset()
  
  timeInterval = setInterval(() => {
    updateTimeUntilReset()
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
.daily-view {
  padding: 20px;
  min-height: 100vh;
}

.daily-header {
  margin-bottom: 30px;
}

.daily-info {
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

.daily-bonus-section {
  margin-bottom: 40px;
}

.bonus-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.bonus-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.bonus-card.bonus-claimed {
  border-color: var(--quantum-success);
  background: rgba(0, 255, 136, 0.1);
}

.bonus-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 20px;
}

.bonus-icon {
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

.bonus-info {
  flex: 1;
}

.bonus-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.bonus-description {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.bonus-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.status-icon {
  font-size: 24px;
}

.status-text {
  font-size: 12px;
  color: var(--quantum-success);
  font-weight: 600;
}

.bonus-rewards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.reward-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 12px;
  padding: 15px;
}

.reward-icon {
  font-size: 24px;
}

.reward-amount {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-primary);
}

.reward-label {
  font-size: 12px;
  color: var(--quantum-text-dim);
  text-align: center;
}

.bonus-btn {
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

.btn-claimed {
  background: rgba(100, 100, 100, 0.3);
  color: var(--quantum-text-dim);
  cursor: not-allowed;
}

.bonus-btn:hover:not(.btn-claimed) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--quantum-glow);
}

.daily-quests-section {
  margin-bottom: 40px;
}

.quests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.quest-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.quest-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.quest-card.quest-completed {
  border-color: var(--quantum-success);
}

.quest-card.quest-claimed {
  border-color: var(--quantum-text-dim);
  background: rgba(100, 100, 100, 0.1);
}

.quest-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.quest-icon {
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

.quest-info {
  flex: 1;
}

.quest-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.quest-description {
  font-size: 13px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.quest-status {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
}

.status-icon {
  font-size: 20px;
}

.quest-progress {
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

.quest-rewards {
  display: flex;
  justify-content: space-around;
  margin-bottom: 15px;
}

.quest-rewards .reward-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  background: rgba(0, 255, 255, 0.05);
  border-radius: 8px;
  padding: 8px;
}

.quest-rewards .reward-icon {
  font-size: 16px;
}

.quest-rewards .reward-amount {
  font-size: 12px;
  font-weight: 600;
  color: var(--quantum-primary);
}

.quest-btn {
  width: 100%;
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-completed {
  background: linear-gradient(45deg, var(--quantum-success), var(--quantum-accent));
  color: var(--quantum-dark);
}

.btn-claimed {
  background: rgba(100, 100, 100, 0.3);
  color: var(--quantum-text-dim);
  cursor: not-allowed;
}

.btn-disabled {
  background: rgba(100, 100, 100, 0.3);
  color: var(--quantum-text-dim);
  cursor: not-allowed;
}

.quest-btn:hover:not(.btn-claimed):not(.btn-disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--quantum-glow);
}

.weekly-challenge-section {
  margin-bottom: 40px;
}

.challenge-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.challenge-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.challenge-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 20px;
}

.challenge-icon {
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

.challenge-info {
  flex: 1;
}

.challenge-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.challenge-description {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.challenge-time {
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

.challenge-progress {
  margin-bottom: 20px;
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

.challenge-rewards {
  background: rgba(0, 255, 255, 0.05);
  border-radius: 12px;
  padding: 15px;
}

.rewards-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-primary);
  margin-bottom: 15px;
  text-align: center;
}

.rewards-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.rewards-list .reward-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 8px;
}

.rewards-list .reward-icon {
  font-size: 18px;
}

.rewards-list .reward-text {
  font-size: 13px;
  color: var(--quantum-text-dim);
}

.daily-tips {
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
  .daily-view {
    padding: 15px;
  }
  
  .quests-grid {
    grid-template-columns: 1fr;
  }
  
  .bonus-rewards {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .tips-content {
    grid-template-columns: 1fr;
  }
}
</style>
