import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'

// Initialize Telegram WebApp
declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        initData: string
        initDataUnsafe: any
        version: string
        platform: string
        colorScheme: 'light' | 'dark'
        themeParams: any
        isExpanded: boolean
        viewportHeight: number
        viewportStableHeight: number
        headerColor: string
        backgroundColor: string
        isClosingConfirmationEnabled: boolean
        BackButton: {
          isVisible: boolean
          onClick: (callback: () => void) => void
          offClick: (callback: () => void) => void
          show: () => void
          hide: () => void
        }
        MainButton: {
          text: string
          color: string
          textColor: string
          isVisible: boolean
          isActive: boolean
          isProgressVisible: boolean
          setText: (text: string) => void
          onClick: (callback: () => void) => void
          offClick: (callback: () => void) => void
          show: () => void
          hide: () => void
          enable: () => void
          disable: () => void
          showProgress: (leaveActive?: boolean) => void
          hideProgress: () => void
          setParams: (params: any) => void
        }
        HapticFeedback: {
          impactOccurred: (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => void
          notificationOccurred: (type: 'error' | 'success' | 'warning') => void
          selectionChanged: () => void
        }
        ready: () => void
        expand: () => void
        close: () => void
        sendData: (data: any) => void
        openLink: (url: string, options?: any) => void
        openTelegramLink: (url: string) => void
        openInvoice: (url: string, callback?: (status: string) => void) => void
        showPopup: (params: any, callback?: (buttonId: string) => void) => void
        showAlert: (message: string, callback?: () => void) => void
        showConfirm: (message: string, callback?: (confirmed: boolean) => void) => void
        showScanQrPopup: (params: any, callback?: (text: string) => void) => void
        closeScanQrPopup: () => void
        readTextFromClipboard: (callback?: (text: string) => void) => void
        requestWriteAccess: (callback?: (granted: boolean) => void) => void
        requestContact: (callback?: (granted: boolean, contact?: any) => void) => void
      }
    }
  }
}

const app = createApp(App)
const pinia = createPinia()

// Initialize Telegram WebApp
if (window.Telegram?.WebApp) {
  window.Telegram.WebApp.ready()
  window.Telegram.WebApp.expand()
  
  // Set theme colors
  document.documentElement.style.setProperty('--tg-theme-bg-color', window.Telegram.WebApp.backgroundColor)
  document.documentElement.style.setProperty('--tg-theme-text-color', window.Telegram.WebApp.themeParams.text_color)
  document.documentElement.style.setProperty('--tg-theme-hint-color', window.Telegram.WebApp.themeParams.hint_color)
  document.documentElement.style.setProperty('--tg-theme-link-color', window.Telegram.WebApp.themeParams.link_color)
  document.documentElement.style.setProperty('--tg-theme-button-color', window.Telegram.WebApp.themeParams.button_color)
  document.documentElement.style.setProperty('--tg-theme-button-text-color', window.Telegram.WebApp.themeParams.button_text_color)
}

app.use(pinia)
app.use(router)
app.mount('#app')