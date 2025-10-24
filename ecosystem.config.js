module.exports = {
  apps: [{
    name: 'quantum-nexus-bot',
    script: 'bot.js',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      BOT_TOKEN: '8426192106:AAGGlkfOYAhaQKPp-bcL-3oHXBE50tzAMog',
      WEBAPP_URL: 'https://unlock-rent.online'
    }
  }]
};
