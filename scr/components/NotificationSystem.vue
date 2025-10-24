<template>
  <div class="notification-system">
    <transition-group name="notification" tag="div" class="notifications-container">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        class="notification"
        :class="notification.type"
        @click="removeNotification(notification.id)"
      >
        <div class="notification-icon">
          <span v-if="notification.type === 'success'">✅</span>
          <span v-else-if="notification.type === 'error'">❌</span>
          <span v-else-if="notification.type === 'warning'">⚠️</span>
          <span v-else>ℹ️</span>
        </div>
        
        <div class="notification-content">
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-message">{{ notification.message }}</div>
        </div>
        
        <button class="notification-close" @click.stop="removeNotification(notification.id)">
          ×
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

const notifications = ref<Notification[]>([])

let notificationId = 0

const addNotification = (notification: Omit<Notification, 'id'>) => {
  const id = (++notificationId).toString()
  const newNotification: Notification = {
    id,
    duration: 5000,
    ...notification
  }
  
  notifications.value.push(newNotification)
  
  // Auto remove after duration
  if (newNotification.duration && newNotification.duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
  }
  
  return id
}

const removeNotification = (id: string) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

const clearAllNotifications = () => {
  notifications.value = []
}

// Global notification methods
const showSuccess = (title: string, message: string, duration?: number) => {
  return addNotification({ type: 'success', title, message, duration })
}

const showError = (title: string, message: string, duration?: number) => {
  return addNotification({ type: 'error', title, message, duration })
}

const showWarning = (title: string, message: string, duration?: number) => {
  return addNotification({ type: 'warning', title, message, duration })
}

const showInfo = (title: string, message: string, duration?: number) => {
  return addNotification({ type: 'info', title, message, duration })
}

// Expose methods globally
onMounted(() => {
  window.showNotification = {
    success: showSuccess,
    error: showError,
    warning: showWarning,
    info: showInfo,
    add: addNotification,
    remove: removeNotification,
    clear: clearAllNotifications
  }
})

onUnmounted(() => {
  delete window.showNotification
})

// Expose for parent components
defineExpose({
  addNotification,
  removeNotification,
  clearAllNotifications,
  showSuccess,
  showError,
  showWarning,
  showInfo
})
</script>

<style scoped>
.notification-system {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 2000;
  pointer-events: none;
}

.notifications-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: auto;
}

.notification {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 255, 0.3);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  min-width: 300px;
  max-width: 400px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification:hover {
  transform: translateX(-5px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4);
}

.notification.success {
  border-color: var(--quantum-success);
}

.notification.error {
  border-color: var(--quantum-error);
}

.notification.warning {
  border-color: var(--quantum-warning);
}

.notification.info {
  border-color: var(--quantum-primary);
}

.notification-icon {
  font-size: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--quantum-text);
  margin-bottom: 4px;
}

.notification-message {
  font-size: 13px;
  color: var(--quantum-text-dim);
  line-height: 1.4;
}

.notification-close {
  background: none;
  border: none;
  color: var(--quantum-text-dim);
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.notification-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--quantum-text);
}

/* Transitions */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}

@media (max-width: 768px) {
  .notification-system {
    top: 70px;
    right: 10px;
    left: 10px;
  }
  
  .notification {
    min-width: auto;
    max-width: none;
  }
}
</style>