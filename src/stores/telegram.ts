import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface TelegramUser {
  id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
  is_premium?: boolean
  photo_url?: string
}

export interface TelegramWebApp {
  initData: string
  initDataUnsafe: {
    user?: TelegramUser
    auth_date?: number
    hash?: string
  }
  version: string
  platform: string
  colorScheme: 'light' | 'dark'
  themeParams: {
    bg_color?: string
    text_color?: string
    hint_color?: string
    link_color?: string
    button_color?: string
    button_text_color?: string
    secondary_bg_color?: string
  }
  isExpanded: boolean
  viewportHeight: number
  viewportStableHeight: number
  headerColor: string
  backgroundColor: string
  isClosingConfirmationEnabled: boolean
}

export const useTelegramStore = defineStore('telegram', () => {
  const isInitialized = ref(false)
  const webApp = ref<TelegramWebApp | null>(null)
  const user = ref<TelegramUser | null>(null)
  const theme = ref<'light' | 'dark'>('dark')

  const initializeTelegram = async () => {
    try {
      if (window.Telegram?.WebApp) {
        webApp.value = window.Telegram.WebApp as any
        user.value = webApp.value.initDataUnsafe?.user || null
        theme.value = webApp.value.colorScheme || 'dark'
        
        // Configure WebApp
        webApp.value.ready()
        webApp.value.expand()
        
        // Set up theme
        updateTheme()
        
        // Set up haptic feedback
        setupHapticFeedback()
        
        // Set up main button
        setupMainButton()
        
        // Set up back button
        setupBackButton()
        
        isInitialized.value = true
        
        console.log('Telegram WebApp initialized successfully')
      } else {
        console.warn('Telegram WebApp not available')
      }
    } catch (error) {
      console.error('Failed to initialize Telegram WebApp:', error)
    }
  }

  const updateTheme = () => {
    if (!webApp.value) return

    const themeParams = webApp.value.themeParams
    
    // Update CSS variables
    if (themeParams.bg_color) {
      document.documentElement.style.setProperty('--tg-theme-bg-color', themeParams.bg_color)
    }
    if (themeParams.text_color) {
      document.documentElement.style.setProperty('--tg-theme-text-color', themeParams.text_color)
    }
    if (themeParams.hint_color) {
      document.documentElement.style.setProperty('--tg-theme-hint-color', themeParams.hint_color)
    }
    if (themeParams.link_color) {
      document.documentElement.style.setProperty('--tg-theme-link-color', themeParams.link_color)
    }
    if (themeParams.button_color) {
      document.documentElement.style.setProperty('--tg-theme-button-color', themeParams.button_color)
    }
    if (themeParams.button_text_color) {
      document.documentElement.style.setProperty('--tg-theme-button-text-color', themeParams.button_text_color)
    }
  }

  const setupHapticFeedback = () => {
    if (!webApp.value?.HapticFeedback) return

    // Add haptic feedback to buttons
    document.addEventListener('click', (event) => {
      const target = event.target as HTMLElement
      if (target.classList.contains('quantum-btn') || target.closest('.quantum-btn')) {
        webApp.value?.HapticFeedback?.impactOccurred('light')
      }
    })
  }

  const setupMainButton = () => {
    if (!webApp.value?.MainButton) return

    webApp.value.MainButton.setText('Quantum Nexus')
    webApp.value.MainButton.color = '#00ffff'
    webApp.value.MainButton.textColor = '#000000'
    webApp.value.MainButton.hide()
  }

  const setupBackButton = () => {
    if (!webApp.value?.BackButton) return

    webApp.value.BackButton.hide()
  }

  const showMainButton = (text: string, callback: () => void) => {
    if (!webApp.value?.MainButton) return

    webApp.value.MainButton.setText(text)
    webApp.value.MainButton.show()
    webApp.value.MainButton.onClick(callback)
  }

  const hideMainButton = () => {
    if (!webApp.value?.MainButton) return

    webApp.value.MainButton.hide()
  }

  const showBackButton = (callback: () => void) => {
    if (!webApp.value?.BackButton) return

    webApp.value.BackButton.show()
    webApp.value.BackButton.onClick(callback)
  }

  const hideBackButton = () => {
    if (!webApp.value?.BackButton) return

    webApp.value.BackButton.hide()
  }

  const showAlert = (message: string) => {
    if (!webApp.value) return

    webApp.value.showAlert(message)
  }

  const showConfirm = (message: string): Promise<boolean> => {
    return new Promise((resolve) => {
      if (!webApp.value) {
        resolve(false)
        return
      }

      webApp.value.showConfirm(message, (confirmed) => {
        resolve(confirmed)
      })
    })
  }

  const showPopup = (params: {
    title?: string
    message: string
    buttons?: Array<{
      id: string
      type?: 'default' | 'ok' | 'close' | 'cancel' | 'destructive'
      text: string
    }>
  }): Promise<string | null> => {
    return new Promise((resolve) => {
      if (!webApp.value) {
        resolve(null)
        return
      }

      webApp.value.showPopup(params, (buttonId) => {
        resolve(buttonId)
      })
    })
  }

  const openLink = (url: string) => {
    if (!webApp.value) return

    webApp.value.openLink(url)
  }

  const openTelegramLink = (url: string) => {
    if (!webApp.value) return

    webApp.value.openTelegramLink(url)
  }

  const sendData = (data: any) => {
    if (!webApp.value) return

    webApp.value.sendData(JSON.stringify(data))
  }

  const close = () => {
    if (!webApp.value) return

    webApp.value.close()
  }

  const requestContact = (): Promise<{ granted: boolean; contact?: any }> => {
    return new Promise((resolve) => {
      if (!webApp.value) {
        resolve({ granted: false })
        return
      }

      webApp.value.requestContact((granted, contact) => {
        resolve({ granted, contact })
      })
    })
  }

  const requestWriteAccess = (): Promise<boolean> => {
    return new Promise((resolve) => {
      if (!webApp.value) {
        resolve(false)
        return
      }

      webApp.value.requestWriteAccess((granted) => {
        resolve(granted)
      })
    })
  }

  const readTextFromClipboard = (): Promise<string | null> => {
    return new Promise((resolve) => {
      if (!webApp.value) {
        resolve(null)
        return
      }

      webApp.value.readTextFromClipboard((text) => {
        resolve(text)
      })
    })
  }

  const showScanQrPopup = (params: {
    text?: string
  }): Promise<string | null> => {
    return new Promise((resolve) => {
      if (!webApp.value) {
        resolve(null)
        return
      }

      webApp.value.showScanQrPopup(params, (text) => {
        resolve(text)
      })
    })
  }

  const closeScanQrPopup = () => {
    if (!webApp.value) return

    webApp.value.closeScanQrPopup()
  }

  const openInvoice = (url: string): Promise<string> => {
    return new Promise((resolve) => {
      if (!webApp.value) {
        resolve('failed')
        return
      }

      webApp.value.openInvoice(url, (status) => {
        resolve(status)
      })
    })
  }

  const impactFeedback = (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft' = 'light') => {
    if (!webApp.value?.HapticFeedback) return

    webApp.value.HapticFeedback.impactOccurred(style)
  }

  const notificationFeedback = (type: 'error' | 'success' | 'warning' = 'success') => {
    if (!webApp.value?.HapticFeedback) return

    webApp.value.HapticFeedback.notificationOccurred(type)
  }

  const selectionFeedback = () => {
    if (!webApp.value?.HapticFeedback) return

    webApp.value.HapticFeedback.selectionChanged()
  }

  return {
    // State
    isInitialized,
    webApp,
    user,
    theme,
    
    // Actions
    initializeTelegram,
    updateTheme,
    showMainButton,
    hideMainButton,
    showBackButton,
    hideBackButton,
    showAlert,
    showConfirm,
    showPopup,
    openLink,
    openTelegramLink,
    sendData,
    close,
    requestContact,
    requestWriteAccess,
    readTextFromClipboard,
    showScanQrPopup,
    closeScanQrPopup,
    openInvoice,
    impactFeedback,
    notificationFeedback,
    selectionFeedback
  }
})