<template>
  <div class="profile-view">
    <div class="profile-header">
      <div class="user-card">
        <div class="user-avatar">
          <img v-if="user?.photoUrl" :src="user.photoUrl" :alt="user.firstName">
          <div v-else class="avatar-placeholder">{{ user?.firstName?.charAt(0) || 'U' }}</div>
        </div>
        
        <div class="user-info">
          <h1 class="user-name">{{ user?.firstName }} {{ user?.lastName }}</h1>
          <p class="user-username" v-if="user?.username">@{{ user.username }}</p>
          <div class="user-badges">
            <span class="badge premium" v-if="user?.isPremium">⭐ Premium</span>
            <span class="badge level">Level {{ stats.level }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Stats -->
    <div class="profile-stats">
      <h2 class="section-title">📊 Your Statistics</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">⚛️</div>
          <div class="stat-info">
            <div class="stat-label">Quantum Coins</div>
            <div class="stat-value">{{ formatNumber(stats.quantumCoins) }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">💎</div>
          <div class="stat-info">
            <div class="stat-label">EXP Coins</div>
            <div class="stat-value">{{ formatNumber(stats.expCoins) }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">👆</div>
          <div class="stat-info">
            <div class="stat-label">Total Taps</div>
            <div class="stat-value">{{ formatNumber(stats.totalTaps) }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-info">
            <div class="stat-label">Level</div>
            <div class="stat-value">{{ stats.level }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">⚡</div>
          <div class="stat-info">
            <div class="stat-label">Multiplier</div>
            <div class="stat-value">x{{ stats.multiplier.toFixed(2) }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">🏢</div>
          <div class="stat-info">
            <div class="stat-label">Investments</div>
            <div class="stat-value">{{ ownedInvestments }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Referral System -->
    <div class="referral-section">
      <h2 class="section-title">👥 Referral System</h2>
      
      <div class="referral-card">
        <div class="referral-header">
          <div class="referral-icon">🎁</div>
          <div class="referral-info">
            <h3 class="referral-title">Invite Friends & Earn</h3>
            <p class="referral-description">Share your referral code and earn rewards when friends join!</p>
          </div>
        </div>

        <div class="referral-code">
          <div class="code-label">Your Referral Code</div>
          <div class="code-container">
            <input 
              type="text" 
              :value="stats.referralCode" 
              readonly 
              class="code-input"
              ref="referralCodeInput"
            >
            <button class="copy-btn" @click="copyReferralCode">
              <span class="copy-icon">📋</span>
              Copy
            </button>
          </div>
        </div>

        <div class="referral-stats">
          <div class="referral-stat">
            <span class="stat-label">Referrals</span>
            <span class="stat-value">{{ stats.referralsCount }}</span>
          </div>
          <div class="referral-stat">
            <span class="stat-label">Earnings</span>
            <span class="stat-value">{{ formatNumber(stats.referralsEarnings) }} EXP</span>
          </div>
        </div>

        <div class="referral-rewards">
          <h4 class="rewards-title">Referral Rewards</h4>
          <div class="rewards-list">
            <div class="reward-item">
              <span class="reward-icon">🎁</span>
              <span class="reward-text">You get 1000 EXP when friend joins</span>
            </div>
            <div class="reward-item">
              <span class="reward-icon">💰</span>
              <span class="reward-text">Friend gets 500 EXP bonus</span>
            </div>
            <div class="reward-item">
              <span class="reward-icon">⚡</span>
              <span class="reward-text">Both get 1.5x multiplier for 24h</span>
            </div>
          </div>
        </div>

        <div class="referral-share">
          <button class="share-btn telegram" @click="shareToTelegram">
            <span class="share-icon">📱</span>
            Share to Telegram
          </button>
          <button class="share-btn copy" @click="copyShareText">
            <span class="share-icon">📋</span>
            Copy Share Text
          </button>
        </div>
      </div>
    </div>

    <!-- Withdrawal System -->
    <div class="withdrawal-section">
      <h2 class="section-title">💸 Withdraw EXP</h2>
      
      <div class="withdrawal-card">
        <div class="withdrawal-header">
          <div class="withdrawal-icon">💰</div>
          <div class="withdrawal-info">
            <h3 class="withdrawal-title">Convert EXP to USD</h3>
            <p class="withdrawal-description">Exchange rate: 100,000 EXP = 1 USD</p>
          </div>
        </div>

        <div class="withdrawal-form">
          <div class="form-group">
            <label class="form-label">Amount to Withdraw</label>
            <div class="input-group">
              <input 
                type="number" 
                v-model="withdrawalAmount" 
                :max="stats.expCoins"
                :min="100000"
                step="100000"
                class="withdrawal-input"
                placeholder="Enter amount in EXP"
              >
              <span class="input-suffix">EXP</span>
            </div>
            <div class="form-hint">
              Minimum: 100,000 EXP (1 USD)
            </div>
          </div>

          <div class="withdrawal-preview">
            <div class="preview-item">
              <span class="preview-label">EXP Amount:</span>
              <span class="preview-value">{{ formatNumber(withdrawalAmount) }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">USD Amount:</span>
              <span class="preview-value">${{ (withdrawalAmount / 100000).toFixed(2) }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">Processing Fee:</span>
              <span class="preview-value">${{ (withdrawalAmount / 100000 * 0.05).toFixed(2) }}</span>
            </div>
            <div class="preview-item total">
              <span class="preview-label">You'll Receive:</span>
              <span class="preview-value">${{ (withdrawalAmount / 100000 * 0.95).toFixed(2) }}</span>
            </div>
          </div>

          <button 
            class="withdrawal-btn"
            :disabled="withdrawalAmount < 100000 || withdrawalAmount > stats.expCoins"
            @click="processWithdrawal"
          >
            <span class="btn-icon">💸</span>
            Request Withdrawal
          </button>
        </div>
      </div>
    </div>

    <!-- Achievements -->
    <div class="achievements-section">
      <h2 class="section-title">🏅 Achievements</h2>
      <div class="achievements-grid">
        <div 
          v-for="achievement in achievements" 
          :key="achievement.id"
          class="achievement-card"
          :class="{ 'achievement-unlocked': achievement.unlocked }"
        >
          <div class="achievement-icon">{{ achievement.icon }}</div>
          <div class="achievement-info">
            <h4 class="achievement-name">{{ achievement.name }}</h4>
            <p class="achievement-description">{{ achievement.description }}</p>
            <div class="achievement-progress" v-if="!achievement.unlocked">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: achievement.progress + '%' }"
                ></div>
              </div>
              <div class="progress-text">{{ achievement.progress }}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Settings -->
    <div class="settings-section">
      <h2 class="section-title">⚙️ Settings</h2>
      <div class="settings-card">
        <div class="setting-item">
          <div class="setting-info">
            <h4 class="setting-name">Haptic Feedback</h4>
            <p class="setting-description">Vibration feedback for taps and actions</p>
          </div>
          <div class="setting-control">
            <label class="toggle">
              <input type="checkbox" v-model="settings.hapticFeedback">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
        
        <div class="setting-item">
          <div class="setting-info">
            <h4 class="setting-name">Sound Effects</h4>
            <p class="setting-description">Audio feedback for game actions</p>
          </div>
          <div class="setting-control">
            <label class="toggle">
              <input type="checkbox" v-model="settings.soundEffects">
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
        
        <div class="setting-item">
          <div class="setting-info">
            <h4 class="setting-name">Auto-Save</h4>
            <p class="setting-description">Automatically save progress</p>
          </div>
          <div class="setting-control">
            <label class="toggle">
              <input type="checkbox" v-model="settings.autoSave" disabled>
              <span class="toggle-slider"></span>
            </label>
          </div>
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

const { user, stats, investments } = storeToRefs(gameStore)

const referralCodeInput = ref<HTMLInputElement>()
const withdrawalAmount = ref(100000)

const settings = ref({
  hapticFeedback: true,
  soundEffects: false,
  autoSave: true
})

const ownedInvestments = computed(() => {
  return investments.value.filter(inv => inv.owned).length
})

const achievements = ref([
  {
    id: 'first-tap',
    name: 'First Tap',
    description: 'Tap the quantum core for the first time',
    icon: '👆',
    unlocked: true,
    progress: 100
  },
  {
    id: 'tap-master',
    name: 'Tap Master',
    description: 'Reach 10,000 total taps',
    icon: '👆',
    unlocked: stats.value.totalTaps >= 10000,
    progress: Math.min((stats.value.totalTaps / 10000) * 100, 100)
  },
  {
    id: 'quantum-investor',
    name: 'Quantum Investor',
    description: 'Own 5 different investments',
    icon: '🏢',
    unlocked: ownedInvestments.value >= 5,
    progress: Math.min((ownedInvestments.value / 5) * 100, 100)
  },
  {
    id: 'referral-champion',
    name: 'Referral Champion',
    description: 'Refer 10 friends',
    icon: '👥',
    unlocked: stats.value.referralsCount >= 10,
    progress: Math.min((stats.value.referralsCount / 10) * 100, 100)
  },
  {
    id: 'exp-collector',
    name: 'EXP Collector',
    description: 'Accumulate 1,000,000 EXP',
    icon: '💎',
    unlocked: stats.value.expCoins >= 1000000,
    progress: Math.min((stats.value.expCoins / 1000000) * 100, 100)
  },
  {
    id: 'level-master',
    name: 'Level Master',
    description: 'Reach level 100',
    icon: '⭐',
    unlocked: stats.value.level >= 100,
    progress: Math.min((stats.value.level / 100) * 100, 100)
  }
])

const formatNumber = (num: number): string => {
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return Math.floor(num).toString()
}

const copyReferralCode = async () => {
  if (!referralCodeInput.value) return
  
  try {
    await navigator.clipboard.writeText(stats.value.referralCode)
    telegramStore.showAlert('Referral code copied to clipboard!')
    telegramStore.impactFeedback('light')
  } catch (error) {
    console.error('Failed to copy:', error)
    telegramStore.showAlert('Failed to copy referral code')
  }
}

const shareToTelegram = () => {
  const shareText = `🎮 Join me in Quantum Nexus - the most advanced tap game!\n\nUse my referral code: ${stats.value.referralCode}\n\nGet 500 EXP bonus and 1.5x multiplier for 24 hours!\n\n#QuantumNexus #TapGame`
  
  const telegramUrl = `https://t.me/share/url?url=${encodeURIComponent(shareText)}`
  telegramStore.openLink(telegramUrl)
}

const copyShareText = async () => {
  const shareText = `🎮 Join me in Quantum Nexus - the most advanced tap game!\n\nUse my referral code: ${stats.value.referralCode}\n\nGet 500 EXP bonus and 1.5x multiplier for 24 hours!\n\n#QuantumNexus #TapGame`
  
  try {
    await navigator.clipboard.writeText(shareText)
    telegramStore.showAlert('Share text copied to clipboard!')
    telegramStore.impactFeedback('light')
  } catch (error) {
    console.error('Failed to copy:', error)
    telegramStore.showAlert('Failed to copy share text')
  }
}

const processWithdrawal = async () => {
  if (withdrawalAmount.value < 100000 || withdrawalAmount.value > stats.value.expCoins) {
    telegramStore.showAlert('Invalid withdrawal amount!')
    return
  }

  const confirmed = await telegramStore.showConfirm(
    `Are you sure you want to withdraw ${formatNumber(withdrawalAmount.value)} EXP for $${(withdrawalAmount.value / 100000 * 0.95).toFixed(2)}?`
  )

  if (confirmed) {
    const result = gameStore.withdrawExp(withdrawalAmount.value)
    
    if (result.success) {
      telegramStore.showAlert('Withdrawal request submitted successfully!')
      telegramStore.impactFeedback('medium')
      withdrawalAmount.value = 100000
    } else {
      telegramStore.showAlert('Withdrawal failed!')
    }
  }
}

onMounted(() => {
  // Load settings from localStorage
  const savedSettings = localStorage.getItem('quantum-nexus-settings')
  if (savedSettings) {
    settings.value = { ...settings.value, ...JSON.parse(savedSettings) }
  }
})
</script>

<style scoped>
.profile-view {
  padding: 20px;
  min-height: 100vh;
}

.profile-header {
  margin-bottom: 30px;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.user-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--quantum-primary);
  flex-shrink: 0;
}

.user-avatar img {
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
  font-size: 32px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.user-username {
  font-size: 16px;
  color: var(--quantum-text-dim);
  margin-bottom: 10px;
}

.user-badges {
  display: flex;
  gap: 10px;
}

.badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.badge.premium {
  background: linear-gradient(45deg, var(--quantum-accent), var(--quantum-primary));
  color: var(--quantum-dark);
}

.badge.level {
  background: rgba(0, 255, 255, 0.2);
  color: var(--quantum-primary);
  border: 1px solid var(--quantum-primary);
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--quantum-primary);
  margin-bottom: 20px;
  text-align: center;
}

.profile-stats {
  margin-bottom: 40px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
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

.referral-section {
  margin-bottom: 40px;
}

.referral-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.referral-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.referral-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 20px;
}

.referral-icon {
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

.referral-info {
  flex: 1;
}

.referral-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.referral-description {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.referral-code {
  margin-bottom: 20px;
}

.code-label {
  font-size: 14px;
  color: var(--quantum-text-dim);
  margin-bottom: 10px;
}

.code-container {
  display: flex;
  gap: 10px;
}

.code-input {
  flex: 1;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  color: var(--quantum-text);
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  letter-spacing: 2px;
}

.copy-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  border: none;
  border-radius: 8px;
  color: var(--quantum-dark);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.copy-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--quantum-glow);
}

.copy-icon {
  font-size: 16px;
}

.referral-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.referral-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 12px;
  padding: 15px;
}

.referral-stat .stat-label {
  font-size: 12px;
  color: var(--quantum-text-dim);
}

.referral-stat .stat-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-primary);
}

.referral-rewards {
  margin-bottom: 20px;
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

.reward-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(0, 255, 255, 0.05);
  border-radius: 8px;
}

.reward-icon {
  font-size: 18px;
}

.reward-text {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.referral-share {
  display: flex;
  gap: 10px;
}

.share-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.share-btn.telegram {
  background: linear-gradient(45deg, #0088cc, #00a8ff);
  color: white;
}

.share-btn.copy {
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  color: var(--quantum-dark);
}

.share-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--quantum-glow);
}

.share-icon {
  font-size: 16px;
}

.withdrawal-section {
  margin-bottom: 40px;
}

.withdrawal-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.withdrawal-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.withdrawal-header {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 20px;
}

.withdrawal-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, var(--quantum-success), var(--quantum-accent));
  border-radius: 12px;
  flex-shrink: 0;
}

.withdrawal-info {
  flex: 1;
}

.withdrawal-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.withdrawal-description {
  font-size: 14px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.withdrawal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-label {
  font-size: 14px;
  color: var(--quantum-text-dim);
  font-weight: 600;
}

.input-group {
  display: flex;
  gap: 10px;
}

.withdrawal-input {
  flex: 1;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  color: var(--quantum-text);
  font-size: 16px;
}

.input-suffix {
  padding: 12px 16px;
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  color: var(--quantum-primary);
  font-size: 14px;
  font-weight: 600;
}

.form-hint {
  font-size: 12px;
  color: var(--quantum-text-dim);
}

.withdrawal-preview {
  background: rgba(0, 255, 255, 0.05);
  border-radius: 12px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-item.total {
  border-top: 1px solid rgba(0, 255, 255, 0.3);
  padding-top: 10px;
  font-weight: 700;
}

.preview-label {
  font-size: 14px;
  color: var(--quantum-text-dim);
}

.preview-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--quantum-primary);
}

.preview-item.total .preview-value {
  color: var(--quantum-success);
}

.withdrawal-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 15px 30px;
  background: linear-gradient(45deg, var(--quantum-success), var(--quantum-accent));
  border: none;
  border-radius: 12px;
  color: var(--quantum-dark);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.withdrawal-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--quantum-glow);
}

.withdrawal-btn:disabled {
  background: rgba(100, 100, 100, 0.3);
  color: var(--quantum-text-dim);
  cursor: not-allowed;
}

.btn-icon {
  font-size: 18px;
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
  display: flex;
  align-items: flex-start;
  gap: 15px;
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

.achievement-card.achievement-unlocked {
  border-color: var(--quantum-success);
  background: rgba(0, 255, 136, 0.1);
}

.achievement-icon {
  font-size: 32px;
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
  margin-bottom: 10px;
}

.achievement-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--quantum-primary), var(--quantum-secondary));
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 12px;
  color: var(--quantum-text-dim);
  font-weight: 600;
}

.settings-section {
  margin-bottom: 40px;
}

.settings-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.settings-card:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 25px var(--quantum-glow);
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info {
  flex: 1;
}

.setting-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--quantum-text);
  margin-bottom: 5px;
}

.setting-description {
  font-size: 13px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.setting-control {
  flex-shrink: 0;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(100, 100, 100, 0.3);
  transition: 0.3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

.toggle input:checked + .toggle-slider {
  background-color: var(--quantum-primary);
}

.toggle input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

@media (max-width: 768px) {
  .profile-view {
    padding: 15px;
  }
  
  .user-card {
    flex-direction: column;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .code-container {
    flex-direction: column;
  }
  
  .referral-share {
    flex-direction: column;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
}
</style>