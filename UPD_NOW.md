# 🚀 КОМАНДЫ ДЛЯ ОБНОВЛЕНИЯ СЕРВЕРА

## Быстрое обновление (одной строкой):

```bash
cd ~/quantum-nexus && git pull origin main && sudo cp web_app.html /var/www/quantum-nexus/ && sudo systemctl restart quantum-nexus-web.service && sudo systemctl restart quantum-nexus && echo "✅ Обновлено!"
```

## Пошаговое обновление:

```bash
# 1. Подключитесь к серверу
ssh root@your-server-ip

# 2. Перейдите в директорию проекта
cd ~/quantum-nexus

# 3. Получите последние изменения
git pull origin main

# 4. Скопируйте обновленный файл
sudo cp web_app.html /var/www/quantum-nexus/

# 5. Перезапустите сервисы
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus

# 6. Готово! Используйте /start в боте
```

## Или через автоматический скрипт:

```bash
cd ~/quantum-nexus
bash UPDATE_VIP_NOW.sh
```

---

## ✅ Что обновилось:

### В профиле:
- ✅ Компактная статистика (все влезает)
- ✅ Убраны дробные числа
- ✅ Кнопка "Купить VIP" для не-VIP пользователей

### VIP пакеты:
- 🥉 Bronze VIP - 50 ⭐
- 🥈 Silver VIP - 100 ⭐
- 🥇 Gold VIP - 200 ⭐
- 💎 Platinum VIP - 500 ⭐
- 💠 Diamond VIP - 1000 ⭐
- 👑 Absolute VIP - 2000 ⭐

---

**После обновления используйте `/start` в боте для обновления кеша!**



