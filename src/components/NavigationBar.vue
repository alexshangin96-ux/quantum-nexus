<template>
  <nav class="navigation-bar">
    <div class="nav-container">
      <div class="nav-brand">
        <span class="brand-icon">⚛️</span>
        <span class="brand-text">Quantum Nexus</span>
      </div>
      
      <div class="nav-menu">
        <router-link 
          v-for="item in navItems" 
          :key="item.name"
          :to="item.path" 
          class="nav-item"
          :class="{ active: $route.name === item.name }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </div>
      
      <div class="nav-user">
        <div class="user-info" v-if="user">
          <img v-if="user.photoUrl" :src="user.photoUrl" :alt="user.firstName" class="user-avatar">
          <div v-else class="user-avatar-placeholder">
            {{ user.firstName.charAt(0) }}
          </div>
          <span class="user-name">{{ user.firstName }}</span>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useTelegramStore } from '@/stores/telegram'

const telegramStore = useTelegramStore()

const user = computed(() => telegramStore.user)

const navItems = [
  { name: 'game', path: '/', icon: '🎮', label: 'Игра' },
  { name: 'investment', path: '/investment', icon: '🏢', label: 'Инвестиции' },
  { name: 'shop', path: '/shop', icon: '🛒', label: 'Магазин' },
  { name: 'daily', path: '/daily', icon: '📅', label: 'Ежедневно' },
  { name: 'ranking', path: '/ranking', icon: '🏆', label: 'Рейтинг' },
  { name: 'profile', path: '/profile', icon: '👤', label: 'Профиль' }
]
</script>

<style scoped>
.navigation-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(10, 10, 10, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 255, 255, 0.3);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.5);
}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: var(--quantum-primary);
}

.brand-icon {
  font-size: 24px;
  animation: quantum-pulse 2s ease-in-out infinite;
}

.nav-menu {
  display: flex;
  gap: 10px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 10px 15px;
  border-radius: 12px;
  text-decoration: none;
  color: var(--quantum-text-dim);
  transition: all 0.3s ease;
  position: relative;
  min-width: 60px;
}

.nav-item:hover {
  color: var(--quantum-primary);
  background: rgba(0, 255, 255, 0.1);
}

.nav-item.active {
  color: var(--quantum-primary);
  background: rgba(0, 255, 255, 0.2);
  box-shadow: 0 0 15px var(--quantum-glow);
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: var(--quantum-primary);
  border-radius: 1px;
}

.nav-icon {
  font-size: 20px;
}

.nav-label {
  font-size: 12px;
  font-weight: 600;
}

.nav-user {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid var(--quantum-primary);
}

.user-avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(45deg, var(--quantum-primary), var(--quantum-secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: var(--quantum-dark);
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--quantum-text);
}

@media (max-width: 768px) {
  .nav-container {
    padding: 10px 15px;
  }
  
  .nav-brand {
    font-size: 16px;
  }
  
  .nav-menu {
    gap: 5px;
  }
  
  .nav-item {
    padding: 8px 10px;
    min-width: 50px;
  }
  
  .nav-icon {
    font-size: 18px;
  }
  
  .nav-label {
    font-size: 10px;
  }
  
  .user-name {
    display: none;
  }
}

@media (max-width: 480px) {
  .nav-menu {
    gap: 2px;
  }
  
  .nav-item {
    padding: 6px 8px;
    min-width: 45px;
  }
  
  .nav-label {
    display: none;
  }
}
</style>
