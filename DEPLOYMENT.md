# Quantum Nexus - Deployment Guide

## 🚀 Quick Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
npm run build
vercel --prod
```

3. **Configure Environment Variables**
- Go to Vercel Dashboard → Project Settings → Environment Variables
- Add: `VITE_TELEGRAM_BOT_TOKEN=your_bot_token`

### Option 2: Netlify

1. **Install Netlify CLI**
```bash
npm i -g netlify-cli
```

2. **Deploy**
```bash
npm run build
netlify deploy --prod --dir=dist
```

3. **Configure Environment Variables**
- Go to Netlify Dashboard → Site Settings → Environment Variables
- Add: `VITE_TELEGRAM_BOT_TOKEN=your_bot_token`

### Option 3: GitHub Pages

1. **Install gh-pages**
```bash
npm install --save-dev gh-pages
```

2. **Add deploy script to package.json**
```json
{
  "scripts": {
    "deploy": "npm run build && gh-pages -d dist"
  }
}
```

3. **Deploy**
```bash
npm run deploy
```

## 🤖 Telegram Bot Setup

### 1. Create Bot

1. Message @BotFather on Telegram
2. Send `/newbot`
3. Choose bot name: `Quantum Nexus`
4. Choose username: `quantum_nexus_bot`
5. Save the bot token

### 2. Configure WebApp

1. Send `/newapp` to @BotFather
2. Select your bot
3. Enter app title: `Quantum Nexus`
4. Enter app description: `Advanced quantum tap game with investments and real money withdrawal`
5. Upload app icon (use `public/quantum-icon.svg`)
6. Enter WebApp URL: `https://your-domain.com`
7. Save the WebApp URL

### 3. Set Bot Commands

Send these commands to @BotFather:

```
/setcommands
@quantum_nexus_bot
start - Start playing Quantum Nexus
play - Open the game
shop - Open shop
profile - View profile
help - Get help
```

### 4. Enable Payments (Optional)

If you want to use Telegram Stars:

1. Send `/mybots` to @BotFather
2. Select your bot
3. Bot Settings → Payments
4. Connect payment provider
5. Configure payment settings

## 🔧 Environment Configuration

### Required Variables

```env
VITE_TELEGRAM_BOT_TOKEN=8426192106:AAGGlkfOYAhaQKPp-bcL-3oHXBE50tzAMog
VITE_API_BASE_URL=https://your-api-domain.com
VITE_APP_VERSION=1.0.0
```

### Optional Variables

```env
VITE_DEBUG_MODE=false
VITE_ANALYTICS_ID=your_analytics_id
VITE_SENTRY_DSN=your_sentry_dsn
```

## 📱 Mobile Optimization

### PWA Configuration

1. **Create manifest.json**
```json
{
  "name": "Quantum Nexus",
  "short_name": "QuantumNexus",
  "description": "Advanced quantum tap game",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0a0a",
  "theme_color": "#00ffff",
  "icons": [
    {
      "src": "/quantum-icon.svg",
      "sizes": "any",
      "type": "image/svg+xml"
    }
  ]
}
```

2. **Add to index.html**
```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#00ffff">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
```

### Service Worker

Create `public/sw.js` for offline functionality:

```javascript
const CACHE_NAME = 'quantum-nexus-v1'
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/quantum-icon.svg'
]

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  )
})

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  )
})
```

## 🔒 Security Configuration

### HTTPS Setup

1. **Get SSL Certificate**
   - Use Let's Encrypt (free)
   - Or cloud provider SSL

2. **Force HTTPS**
```javascript
// In main.ts
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
  location.replace(`https:${location.href.substring(location.protocol.length)}`)
}
```

### Content Security Policy

Add to `index.html`:

```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://telegram.org;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.telegram.org;
  frame-src https://telegram.org;
">
```

## 📊 Analytics Setup

### Google Analytics

1. **Install gtag**
```bash
npm install gtag
```

2. **Add to main.ts**
```typescript
import { gtag } from 'gtag'

gtag('config', 'GA_MEASUREMENT_ID')
```

### Custom Analytics

Track game events:

```typescript
const trackEvent = (event: string, data?: any) => {
  if (typeof gtag !== 'undefined') {
    gtag('event', event, data)
  }
}

// Usage
trackEvent('tap', { level: stats.level })
trackEvent('investment_purchase', { investment_id: 'quantum_core' })
trackEvent('withdrawal_request', { amount: withdrawalAmount })
```

## 🧪 Testing

### Unit Tests

```bash
npm run test
```

### E2E Tests

```bash
npm run test:e2e
```

### Performance Testing

```bash
npm run build
npm run preview
# Test with Lighthouse
```

## 📈 Monitoring

### Error Tracking

1. **Install Sentry**
```bash
npm install @sentry/vue
```

2. **Configure**
```typescript
import * as Sentry from '@sentry/vue'

Sentry.init({
  app,
  dsn: 'YOUR_SENTRY_DSN',
  environment: process.env.NODE_ENV
})
```

### Performance Monitoring

```typescript
// Track loading times
const startTime = performance.now()
// ... game initialization
const loadTime = performance.now() - startTime
trackEvent('game_load_time', { duration: loadTime })
```

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Quantum Nexus

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 🚨 Troubleshooting

### Common Issues

1. **Telegram WebApp not loading**
   - Check HTTPS certificate
   - Verify WebApp URL in bot settings
   - Check browser console for errors

2. **Build failures**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check TypeScript errors: `npm run type-check`
   - Verify all dependencies are installed

3. **Performance issues**
   - Enable code splitting
   - Optimize images
   - Use lazy loading
   - Check bundle size: `npm run build -- --analyze`

### Debug Mode

Enable debug logging:

```typescript
const DEBUG = import.meta.env.VITE_DEBUG_MODE === 'true'

if (DEBUG) {
  console.log('Quantum Nexus Debug Mode Enabled')
  window.quantumDebug = {
    gameStore,
    telegramStore,
    stats: () => stats.value,
    resetGame: () => gameStore.resetGame()
  }
}
```

## 📞 Support

- **Documentation**: Check README.md
- **Issues**: GitHub Issues
- **Discord**: [Your Discord Server]
- **Telegram**: @your_support_bot

---

**Ready to launch Quantum Nexus? Follow this guide and become the ultimate quantum master! 🚀⚛️**