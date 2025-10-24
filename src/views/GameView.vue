<template>
  <div class="game-view">
    <!-- Header with stats -->
    <div class="game-header">
      <div class="stats-container">
        <div class="stat-item">
          <div class="stat-icon">⚛️</div>
          <div class="stat-info">
            <div class="stat-label">Quantum Coins</div>
            <div class="stat-value quantum-text-glow">{{ formatNumber(stats.quantumCoins) }}</div>
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-icon">💎</div>
          <div class="stat-info">
            <div class="stat-label">EXP Coins</div>
            <div class="stat-value quantum-text-glow">{{ formatNumber(stats.expCoins) }}</div>
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-icon">⭐</div>
          <div class="stat-info">
            <div class="stat-label">Level</div>
            <div class="stat-value quantum-text-glow">{{ stats.level }}</div>
          </div>
        </div>
      </div>
      
      <div class="exp-bar">
        <div class="exp-progress" :style="{ width: expProgressPercent + '%' }"></div>
        <div class="exp-text">{{ formatNumber(stats.experience) }} / {{ formatNumber(nextLevelExperience) }}</div>
      </div>
    </div>

    <!-- Main tap area -->
    <div class="tap-area" @click="handleTap">
      <div class="quantum-core" :class="{ 'quantum-pulse': isTapping }">
        <div class="core-inner">
          <div class="core-glow"></div>
          <div class="core-particles">
            <div v-for="i in 8" :key="i" class="particle" :style="{ '--delay': i * 0.5 + 's' }"></div>
          </div>
        </div>
      </div>
      
      <div class="tap-instructions">
        <h2 class="quantum-title">QUANTUM NEXUS</h2>
        <p class="tap-hint">Tap the quantum core to generate energy!</p>
        <div class="multiplier-display">
          <span class="multiplier-label">Multiplier:</span>
          <span class="multiplier-value quantum-text-glow">x{{ stats.multiplier.toFixed(2) }}</span>
        </div>
      </div>
    </div>

    <!-- Passive income display -->
    <div class="passive-income" v-if="totalExpPerSecond > 0">
      <div class="passive-icon">⚡</div>
      <div class="passive-info">
        <div class="passive-label">Passive EXP/sec</div>
        <div class="passive-value quantum-text-glow">{{ formatNumber(totalExpPerSecond) }}</div>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="quick-actions">
      <button class="quantum-btn" @click="$router.push('/investment')">
        <span class="btn-icon">🏢</span>
        Investments
      </button>
      
      <button class="quantum-btn" @click="$router.push('/shop')">
        <span class="btn-icon">🛒</span>
        Shop
      </button>
      
      <button class="quantum-btn" @click="$router.push('/daily')">
        <span class="btn-icon">📅</span>
        Daily
      </button>
    </div>

    <!-- Tap effects -->
    <div class="tap-effects" ref="tapEffects"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { useTelegramStore } from '@/stores/telegram'
import { gsap } from 'gsap'

const gameStore = useGameStore()
const telegramStore = useTelegramStore()

const { stats, totalExpPerSecond, nextLevelExperience } = storeToRefs(gameStore)

const isTapping = ref(false)
const tapEffects = ref<HTMLElement>()

// Computed properties
const expProgressPercent = computed(() => {
  return (stats.value.experience / nextLevelExperience.value) * 100
})

// Methods
const formatNumber = (num: number): string => {
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return Math.floor(num).toString()
}

const handleTap = () => {
  isTapping.value = true
  
  // Game logic
  gameStore.tap()
  
  // Visual effects
  createTapEffect()
  
  // Haptic feedback
  telegramStore.impactFeedback('light')
  
  // Reset tapping state
  setTimeout(() => {
    isTapping.value = false
  }, 150)
}

const createTapEffect = () => {
  if (!tapEffects.value) return

  const effect = document.createElement('div')
  effect.className = 'tap-effect'
  effect.innerHTML = `+${formatNumber(stats.value.multiplier)}`
  
  // Random position around the core
  const angle = Math.random() * Math.PI * 2
  const distance = 50 + Math.random() * 100
  const x = Math.cos(angle) * distance
  const y = Math.sin(angle) * distance
  
  effect.style.left = `calc(50% + ${x}px)`
  effect.style.top = `calc(50% + ${y}px)`
  
  tapEffects.value.appendChild(effect)
  
  // Animate effect
  gsap.fromTo(effect, 
    { 
      opacity: 1, 
      scale: 0.5, 
      y: 0 
    },
    { 
      opacity: 0, 
      scale: 1.5, 
      y: -50, 
      duration: 1, 
      ease: 'power2.out',
      onComplete: () => {
        effect.remove()
      }
    }
  )
}

// Lifecycle
onMounted(() => {
  // Initialize tap effects container
  if (tapEffects.value) {
    tapEffects.value.style.position = 'absolute'
    tapEffects.value.style.top = '0'
    tapEffects.value.style.left = '0'
    tapEffects.value.style.width = '100%'
    tapEffects.value.style.height = '100%'
    tapEffects.value.style.pointerEvents = 'none'
    tapEffects.value.style.zIndex = '5'
  }
})
</script>

<style scoped>
.game-view {
  min-height: 100vh;
  padding: 20px;
  position: relative;
  background: radial-gradient(circle at center, rgba(0, 255, 255, 0.1) 0%, transparent 70%);
}

.game-header {
  margin-bottom: 30px;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  border-color: var(--quantum-primary);
  box-shadow: 0 0 15px var(--quantum-glow);
}

.stat-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
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
  font-size: 12px;
  color: var(--quantum-text-dim);
  margin-bottom: 5px;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
}

.exp-bar {
  position: relative;
  height: 20px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.exp-progress {
  height: 100%;
  background: linear-gradient(90deg, var(--quantum-primary), var(--quantum-secondary));
  border-radius: 10px;
  transition: width 0.3s ease;
  position: relative;
}

.exp-progress::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.exp-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 12px;
  font-weight: 600;
  color: var(--quantum-text);
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
}

.tap-area {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  margin-bottom: 30px;
  cursor: pointer;
}

.quantum-core {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--quantum-primary) 0%, var(--quantum-secondary) 50%, var(--quantum-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 0 50px var(--quantum-glow);
}

.quantum-core:hover {
  transform: scale(1.05);
  box-shadow: 0 0 80px var(--quantum-glow);
}

.quantum-core.quantum-pulse {
  animation: quantum-pulse 0.15s ease-out;
}

.core-inner {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.core-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, var(--quantum-accent) 0%, transparent 70%);
  animation: quantum-rotate 4s linear infinite;
}

.core-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--quantum-accent);
  border-radius: 50%;
  animation: orbit 3s linear infinite;
  animation-delay: var(--delay);
}

.particle:nth-child(1) { top: 0; left: 50%; transform: translateX(-50%); }
.particle:nth-child(2) { top: 25%; right: 0; transform: translateY(-50%); }
.particle:nth-child(3) { bottom: 25%; right: 0; transform: translateY(50%); }
.particle:nth-child(4) { bottom: 0; left: 50%; transform: translateX(-50%); }
.particle:nth-child(5) { bottom: 25%; left: 0; transform: translateY(50%); }
.particle:nth-child(6) { top: 25%; left: 0; transform: translateY(-50%); }
.particle:nth-child(7) { top: 50%; left: 25%; transform: translate(-50%, -50%); }
.particle:nth-child(8) { top: 50%; right: 25%; transform: translate(50%, -50%); }

@keyframes orbit {
  from { transform: rotate(0deg) translateX(75px) rotate(0deg); }
  to { transform: rotate(360deg) translateX(75px) rotate(-360deg); }
}

.tap-instructions {
  text-align: center;
  margin-top: 30px;
}

.tap-hint {
  color: var(--quantum-text-dim);
  margin-bottom: 15px;
  font-size: 16px;
}

.multiplier-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 20px;
  padding: 10px 20px;
}

.multiplier-label {
  color: var(--quantum-text-dim);
  font-size: 14px;
}

.multiplier-value {
  font-size: 18px;
  font-weight: 700;
}

.passive-income {
  position: fixed;
  top: 20px;
  right: 20px;
  background: rgba(26, 26, 46, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 100;
}

.passive-icon {
  font-size: 20px;
  color: var(--quantum-accent);
}

.passive-info {
  text-align: center;
}

.passive-label {
  font-size: 12px;
  color: var(--quantum-text-dim);
  margin-bottom: 5px;
}

.passive-value {
  font-size: 16px;
  font-weight: 700;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-top: 30px;
}

.btn-icon {
  margin-right: 8px;
  font-size: 18px;
}

.tap-effect {
  position: absolute;
  font-size: 20px;
  font-weight: 700;
  color: var(--quantum-accent);
  text-shadow: 0 0 10px var(--quantum-glow);
  pointer-events: none;
  z-index: 10;
}

@media (max-width: 768px) {
  .game-view {
    padding: 15px;
  }
  
  .quantum-core {
    width: 150px;
    height: 150px;
  }
  
  .core-inner {
    width: 120px;
    height: 120px;
  }
  
  .passive-income {
    position: relative;
    top: auto;
    right: auto;
    margin-bottom: 20px;
  }
  
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>