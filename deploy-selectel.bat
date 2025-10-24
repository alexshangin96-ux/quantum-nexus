@echo off
REM Quantum Nexus - Деплой на Selectel для Windows
REM Использование: deploy-selectel.bat <server_ip> <domain>

if "%1"=="" (
    echo Использование: %0 ^<server_ip^> ^<domain^>
    echo Пример: %0 123.456.789.0 quantum-nexus.com
    exit /b 1
)

if "%2"=="" (
    echo Использование: %0 ^<server_ip^> ^<domain^>
    echo Пример: %0 123.456.789.0 quantum-nexus.com
    exit /b 1
)

set SERVER_IP=%1
set DOMAIN=%2
set PROJECT_DIR=/var/www/quantum-nexus

echo 🚀 Quantum Nexus - Деплой на Selectel
echo ======================================
echo Сервер: %SERVER_IP%
echo Домен: %DOMAIN%
echo.

echo 📦 Устанавливаем зависимости...
ssh root@%SERVER_IP% "apt update && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs nginx certbot python3-certbot-nginx && npm install -g pm2"

echo 📁 Клонируем проект...
ssh root@%SERVER_IP% "mkdir -p %PROJECT_DIR% && cd %PROJECT_DIR% && git clone https://github.com/YOUR_USERNAME/quantum-nexus.git ."

echo ⚙️ Настраиваем проект...
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo VITE_TELEGRAM_BOT_TOKEN=8426192106:AAGGlkfOYAhaQKPp-bcL-3oHXBE50tzAMog > .env && echo VITE_API_BASE_URL=https://%DOMAIN% >> .env && echo VITE_APP_VERSION=1.0.0 >> .env && echo NODE_ENV=production >> .env"

ssh root@%SERVER_IP% "cd %PROJECT_DIR% && npm install && npm install node-telegram-bot-api express && npm run build"

echo 🤖 Создаем бота...
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo const TelegramBot = require('node-telegram-bot-api'); > bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo const express = require('express'); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo const path = require('path'); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo. >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo const token = '8426192106:AAGGlkfOYAhaQKPp-bcL-3oHXBE50tzAMog'; >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo const bot = new TelegramBot(token, { polling: true }); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo const app = express(); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo. >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo app.use(express.static(path.join(__dirname, 'dist'))); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo. >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo bot.onText(/\/start/, (msg) => { >> bot.js"
ssh root@%%SERVER_IP% "cd %PROJECT_DIR% && echo     const chatId = msg.chat.id; >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo     const firstName = msg.from.first_name; >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo     bot.sendMessage(chatId, \`🎮 Добро пожаловать в Quantum Nexus, \${firstName}!\n\n⚛️ Самая продвинутая тапалка!\n\n🚀 Нажмите кнопку ниже:\`, { >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo         reply_markup: { >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo             inline_keyboard: [[ >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo                 { >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo                     text: '🎮 Играть', >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo                     web_app: { url: 'https://%DOMAIN%' } >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo                 } >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo             ]] >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo         } >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo     }); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo }); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo. >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo const PORT = process.env.PORT ^|^| 3000; >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo app.listen(PORT, () => { >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo     console.log(\`🚀 Server running on port \${PORT}\`); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo }); >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo. >> bot.js"
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && echo console.log('🤖 Bot started!'); >> bot.js"

echo 🌐 Настраиваем Nginx...
ssh root@%SERVER_IP% "cat > /etc/nginx/sites-available/quantum-nexus << 'EOF'
server {
    listen 80;
    server_name %DOMAIN% www.%DOMAIN%;
    
    root %PROJECT_DIR%/dist;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control \"public, immutable\";
    }
}
EOF"

ssh root@%SERVER_IP% "ln -sf /etc/nginx/sites-available/quantum-nexus /etc/nginx/sites-enabled/ && rm -f /etc/nginx/sites-enabled/default && nginx -t && systemctl reload nginx"

echo 🔒 Получаем SSL сертификат...
ssh root@%SERVER_IP% "certbot --nginx -d %DOMAIN% -d www.%DOMAIN% --non-interactive --agree-tos --email alex.shangin96@gmail.com%DOMAIN%"

echo 🚀 Запускаем бота...
ssh root@%SERVER_IP% "cd %PROJECT_DIR% && pm2 start bot.js --name quantum-nexus-bot && pm2 save && pm2 startup"

echo ✅ Проверяем работу...
ssh root@%SERVER_IP% "echo 'Статус сервисов:' && systemctl status nginx --no-pager -l && pm2 status && echo 'Тест сайта:' && curl -I https://%DOMAIN%"

echo.
echo 🎉 Деплой завершен!
echo 🌐 Сайт: https://%DOMAIN%
echo 🤖 Бот готов к работе!
echo.
echo 📋 Что нужно сделать дальше:
echo 1. Настроить DNS для домена %DOMAIN%
echo 2. Настроить бота в @BotFather
echo 3. Протестировать игру
echo.
echo 🔧 Полезные команды:
echo ssh root@%SERVER_IP% "pm2 logs quantum-nexus-bot"  # Логи бота
echo ssh root@%SERVER_IP% "pm2 restart quantum-nexus-bot" # Перезапуск бота
echo ssh root@%SERVER_IP% "systemctl status nginx"       # Статус Nginx

pause