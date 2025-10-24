<template>
  <div id="app" class="quantum-app">
    <!-- Particle Background -->
    <ParticleBackground />
    
    <!-- Main Navigation -->
    <NavigationBar />
    
    <!-- Router View -->
    <main class="main-content">
      <router-view />
    </main>
    
    <!-- Quantum Effects -->
    <QuantumEffects />
    
    <!-- Notifications -->
    <NotificationSystem />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useGameStore } from '@/stores/game'
import { useTelegramStore } from '@/stores/telegram'
import ParticleBackground from '@/components/ParticleBackground.vue'
import NavigationBar from '@/components/NavigationBar.vue'
import QuantumEffects from '@/components/QuantumEffects.vue'
import NotificationSystem from '@/components/NotificationSystem.vue'

const gameStore = useGameStore()
const telegramStore = useTelegramStore()

onMounted(async () => {
  // Initialize Telegram WebApp
  await telegramStore.initializeTelegram()
  
  // Initialize game data
  await gameStore.initializeGame()
  
  // Start background processes
  gameStore.startBackgroundProcesses()
})
</script>

<style scoped>
.quantum-app {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

.main-content {
  position: relative;
  z-index: 10;
  padding-top: 80px; /* Account for fixed navigation */
  min-height: calc(100vh - 80px);
}
</style>
