#!/bin/bash
# Restart bot and web server

echo "🔄 Перезапуск Quantum Nexus..."

cd /root/quantum-nexus

# Update files
git pull origin main

# Copy web app
cp web_app.html /var/www/quantum-nexus/

# Restart web server
systemctl restart quantum-nexus-web

# Find and restart bot process
echo "🔍 Поиск процесса бота..."
BOT_PID=$(ps aux | grep "[b]ot.py" | awk '{print $2}')

if [ -z "$BOT_PID" ]; then
    echo "❌ Бот не найден"
    echo "📝 Запустите бота вручную:"
    echo "   cd /root/quantum-nexus"
    echo "   source venv/bin/activate"
    echo "   nohup python bot.py > bot.log 2>&1 &"
else
    echo "✅ Бот найден (PID: $BOT_PID)"
    echo "🔄 Перезапуск бота..."
    
    # Kill bot
    kill $BOT_PID
    
    # Wait a moment
    sleep 2
    
    # Start bot again
    source venv/bin/activate
    nohup python bot.py > bot.log 2>&1 &
    
    echo "✅ Бот перезапущен"
fi

# Check status
echo ""
echo "📊 Статус:"
systemctl status quantum-nexus-web --no-pager

echo ""
echo "✅ Готово!"






