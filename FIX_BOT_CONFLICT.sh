#!/bin/bash

echo "=== Остановка всех процессов бота ==="
sudo systemctl stop quantum-nexus
sleep 2

echo "=== Принудительное завершение всех Python процессов с bot.py ==="
sudo pkill -9 -f "python.*bot.py"
sudo pkill -9 -f "python3.*bot.py"
sleep 2

echo "=== Проверка, что процессы остановлены ==="
ps aux | grep "bot.py" | grep -v grep || echo "Все процессы bot.py остановлены ✓"

echo "=== Очистка старых обновлений ==="
cd /root/quantum-nexus
sudo rm -f .updates_pending
sudo rm -f .bot_updates
sudo rm -f .telegram_bot_state

echo "=== Запуск бота ==="
sudo systemctl start quantum-nexus
sleep 3

echo "=== Статус бота ==="
sudo systemctl status quantum-nexus --no-pager | head -20

echo "=== Проверка логов ==="
sudo journalctl -u quantum-nexus -n 20 --no-pager | grep -E "(ERROR|Starting|Bot is starting)" || echo "Логи чисты"

echo "=== Готово! ==="






