# Команды для обновления профиля на сервере

## Обновление файлов

```bash
cd /root/quantum-nexus
git pull origin main
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo systemctl restart quantum-nexus-web.service
```

## Проверка статуса

```bash
sudo systemctl status quantum-nexus-web.service
sudo journalctl -u quantum-nexus-web.service -n 50
```

## Что было добавлено:

1. **6 кнопок быстрого доступа** в профиле:
   - 🛍️ Покупки (My Purchases)
   - 🏆 Достижения (новое модальное окно!)
   - 🏅 Топ (Leaderboard)
   - 📜 История (History)
   - 👥 Рефералы (Referrals)
   - 🆘 Поддержка (Support)

2. **Красивый grid layout** с эффектами при наведении

3. **Система достижений** с прогресс-баром:
   - 👆 Первый тап
   - 🎯 Мастер тапов (100)
   - ⚡ Профи тапов (1000)
   - 💰 Миллионер (1M коинов)
   - 🃏 Первая карта
   - ⛏️ Первая машина
   - 🌟 Уровень 10
   - ⭐ Уровень 50
   - 🥉 VIP бронза
   - 🥈 VIP серебро
   - 🥇 VIP золото
   - 👥 Мастер рефералов (10 друзей)

4. **Улучшенная статистика**:
   - Отображение текущей/максимальной энергии
   - Правильное отображение усилителя тапа
   - Всё в красивом оформлении

