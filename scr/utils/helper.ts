import dayjs from 'dayjs'

// Utility functions for Quantum Nexus

export const formatNumber = (num: number): string => {
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return Math.floor(num).toString()
}

export const formatCurrency = (amount: number, currency: string = 'USD'): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

export const formatTime = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}h ${minutes}m ${secs}s`
  } else if (minutes > 0) {
    return `${minutes}m ${secs}s`
  } else {
    return `${secs}s`
  }
}

export const formatDuration = (milliseconds: number): string => {
  const seconds = Math.floor(milliseconds / 1000)
  return formatTime(seconds)
}

export const generateId = (): string => {
  return Math.random().toString(36).substr(2, 9)
}

export const generateReferralCode = (): string => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  let result = ''
  for (let i = 0; i < 8; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

export const calculateOfflineIncome = (
  expPerSecond: number,
  hoursOffline: number,
  maxHours: number,
  multiplier: number = 1
): number => {
  const effectiveHours = Math.min(hoursOffline, maxHours)
  return expPerSecond * effectiveHours * 3600 * multiplier
}

export const calculateLevelExperience = (level: number): number => {
  return Math.floor(100 * Math.pow(1.15, level))
}

export const calculatePrestigeMultiplier = (prestigeLevel: number): number => {
  return Math.pow(1.5, prestigeLevel)
}

export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

export const isValidTelegramUsername = (username: string): boolean => {
  const usernameRegex = /^[a-zA-Z0-9_]{5,32}$/
  return usernameRegex.test(username)
}

export const getRandomElement = <T>(array: T[]): T => {
  return array[Math.floor(Math.random() * array.length)]
}

export const shuffleArray = <T>(array: T[]): T[] => {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

export const clamp = (value: number, min: number, max: number): number => {
  return Math.min(Math.max(value, min), max)
}

export const lerp = (start: number, end: number, factor: number): number => {
  return start + (end - start) * factor
}

export const easeInOut = (t: number): number => {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t
}

export const easeOut = (t: number): number => {
  return 1 - Math.pow(1 - t, 3)
}

export const easeIn = (t: number): number => {
  return t * t * t
}

export const getTimeUntilReset = (): string => {
  const now = dayjs()
  const tomorrow = now.add(1, 'day').startOf('day')
  const diff = tomorrow.diff(now)
  
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  const seconds = Math.floor((diff % (1000 * 60)) / 1000)
  
  return `${hours}h ${minutes}m ${seconds}s`
}

export const getTimeUntilWeeklyReset = (): string => {
  const now = dayjs()
  const nextMonday = now.add(1, 'week').startOf('week').add(1, 'day')
  const diff = nextMonday.diff(now)
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  
  return `${days}d ${hours}h`
}

export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (error) {
    console.error('Failed to copy to clipboard:', error)
    return false
  }
}

export const shareToTelegram = (text: string, url?: string): void => {
  const shareUrl = url ? `${text}\n\n${url}` : text
  const telegramUrl = `https://t.me/share/url?url=${encodeURIComponent(shareUrl)}`
  window.open(telegramUrl, '_blank')
}

export const getDeviceType = (): 'mobile' | 'tablet' | 'desktop' => {
  const width = window.innerWidth
  if (width < 768) return 'mobile'
  if (width < 1024) return 'tablet'
  return 'desktop'
}

export const isMobile = (): boolean => {
  return getDeviceType() === 'mobile'
}

export const isTablet = (): boolean => {
  return getDeviceType() === 'tablet'
}

export const isDesktop = (): boolean => {
  return getDeviceType() === 'desktop'
}

export const getRandomColor = (): string => {
  const colors = [
    '#00ffff', '#ff00ff', '#ffff00', '#00ff88',
    '#ff4444', '#4444ff', '#ff8800', '#8800ff'
  ]
  return getRandomElement(colors)
}

export const hexToRgb = (hex: string): { r: number; g: number; b: number } | null => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null
}

export const rgbToHex = (r: number, g: number, b: number): string => {
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`
}

export const getContrastColor = (hexColor: string): string => {
  const rgb = hexToRgb(hexColor)
  if (!rgb) return '#000000'
  
  const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000
  return brightness > 128 ? '#000000' : '#ffffff'
}

export const createParticle = (
  x: number,
  y: number,
  color: string = '#00ffff',
  size: number = 2
): HTMLElement => {
  const particle = document.createElement('div')
  particle.className = 'particle'
  particle.style.position = 'absolute'
  particle.style.left = `${x}px`
  particle.style.top = `${y}px`
  particle.style.width = `${size}px`
  particle.style.height = `${size}px`
  particle.style.background = color
  particle.style.borderRadius = '50%'
  particle.style.pointerEvents = 'none'
  particle.style.zIndex = '1000'
  
  return particle
}

export const animateParticle = (
  particle: HTMLElement,
  duration: number = 1000,
  endX?: number,
  endY?: number
): Promise<void> => {
  return new Promise((resolve) => {
    const startX = parseFloat(particle.style.left)
    const startY = parseFloat(particle.style.top)
    const finalX = endX ?? startX
    const finalY = endY ?? startY - 50
    
    const startTime = Date.now()
    
    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easedProgress = easeOut(progress)
      
      const currentX = lerp(startX, finalX, easedProgress)
      const currentY = lerp(startY, finalY, easedProgress)
      const opacity = 1 - progress
      
      particle.style.left = `${currentX}px`
      particle.style.top = `${currentY}px`
      particle.style.opacity = opacity.toString()
      
      if (progress < 1) {
        requestAnimationFrame(animate)
      } else {
        particle.remove()
        resolve()
      }
    }
    
    requestAnimationFrame(animate)
  })
}

export const createFloatingText = (
  text: string,
  x: number,
  y: number,
  color: string = '#00ffff'
): HTMLElement => {
  const element = document.createElement('div')
  element.textContent = text
  element.style.position = 'absolute'
  element.style.left = `${x}px`
  element.style.top = `${y}px`
  element.style.color = color
  element.style.fontSize = '20px'
  element.style.fontWeight = 'bold'
  element.style.pointerEvents = 'none'
  element.style.zIndex = '1000'
  element.style.textShadow = '0 0 10px rgba(0, 255, 255, 0.5)'
  
  return element
}

export const animateFloatingText = (
  element: HTMLElement,
  duration: number = 1000
): Promise<void> => {
  return new Promise((resolve) => {
    const startY = parseFloat(element.style.top)
    const endY = startY - 50
    
    const startTime = Date.now()
    
    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easedProgress = easeOut(progress)
      
      const currentY = lerp(startY, endY, easedProgress)
      const opacity = 1 - progress
      const scale = 1 + progress * 0.5
      
      element.style.top = `${currentY}px`
      element.style.opacity = opacity.toString()
      element.style.transform = `scale(${scale})`
      
      if (progress < 1) {
        requestAnimationFrame(animate)
      } else {
        element.remove()
        resolve()
      }
    }
    
    requestAnimationFrame(animate)
  })
}
