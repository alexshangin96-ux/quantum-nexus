// Global type declarations for Quantum Nexus
declare global {
  interface Window {
    showNotification?: {
      success: (title: string, message: string, duration?: number) => string
      error: (title: string, message: string, duration?: number) => string
      warning: (title: string, message: string, duration?: number) => string
      info: (title: string, message: string, duration?: number) => string
      add: (notification: Omit<Notification, 'id'>) => string
      remove: (id: string) => void
      clear: () => void
    }
  }
}

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

export {}
