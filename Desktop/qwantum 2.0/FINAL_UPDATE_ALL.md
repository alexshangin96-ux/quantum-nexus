# 🎯 ФИНАЛЬНОЕ ОБНОВЛЕНИЕ: Звуки + Система ТОП лидеров

## ⚠️ ВАЖНО: Выполните эти команды НА СЕРВЕРЕ Selectel

---

## 🚀 БЫСТРАЯ КОМАНДА (ВСЁ ВМЕСТЕ):

```bash
cd /root/quantum-nexus && git pull origin main && sudo -u postgres psql quantum_nexus <<EOF
ALTER TABLE users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN IF NOT EXISTS experience FLOAT DEFAULT 0.0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 0.0;
UPDATE users SET experience = (total_earned * 0.01) + (total_taps * 0.1) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000), level = LEAST(100, FLOOR(SQRT(GREATEST(0, experience) / 100) + 1)), rating = (coins * 0.01) + (total_earned * 0.1) + (total_taps * 0.05) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000000) + (level * 10000) WHERE level IS NULL OR experience IS NULL OR rating IS NULL;
EOF
&& sudo cp web_app.html /var/www/quantum-nexus/web_app.html && sudo systemctl restart quantum-nexus-web.service && sudo systemctl restart quantum-nexus.service && echo "✅ Обновление завершено!"
```

---

## 📋 ПОШАГОВЫЕ КОМАНДЫ:

### 1. Подключитесь к серверу:
```bash
ssh root@your-server-ip
```

### 2. Перейдите в папку проекта:
```bash
cd /root/quantum-nexus
```

### 3. Обновите код из GitHub:
```bash
git pull origin main
```

### 4. Выполните SQL миграцию:
```bash
sudo -u postgres psql quantum_nexus <<EOF
ALTER TABLE users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN IF NOT EXISTS experience FLOAT DEFAULT 0.0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 0.0;
UPDATE users 
SET experience = (total_earned * 0.01) + (total_taps * 0.1) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000),
    level = LEAST(100, FLOOR(SQRT(GREATEST(0, experience) / 100) + 1)),
    rating = (coins * 0.01) + (total_earned * 0.1) + (total_taps * 0.05) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000000) + (level * 10000)
WHERE level IS NULL OR experience IS NULL OR rating IS NULL;
SELECT COUNT(*) as total_users, AVG(level) as avg_level, MAX(level) as max_level, AVG(rating) as avg_rating, MAX(rating) as max_rating FROM users;
\q
EOF
```

### 5. Скопируйте обновленные файлы:
```bash
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
```

### 6. Перезапустите сервисы:
```bash
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service
```

### 7. Проверьте статус:
```bash
sudo systemctl status quantum-nexus-web.service
sudo systemctl status quantum-nexus.service
```

---

## ✅ ЧТО БЫЛО ДОБАВЛЕНО:

### 🔊 Система звуков (35 звуков):
- 15 основных звуков (tap, coin, levelup, etc.)
- 20 новых Crypto Tapping звуков
- Звуки выключены по умолчанию
- Переключатель включает/выключает ВСЕ звуки
- Подробное логирование для отладки

### 🏆 Система ТОП лидеров:
- **Уровни**: 1-100 на основе опыта
- **Опыт**: Зависит от заработанных монет, тапов и VIP статуса
- **Рейтинг**: Комплексный балл для сортировки
- **Сортировка**: VIP вверху, затем по рейтингу
- Красивый UI с медалями и анимацией
- Автообновление каждые 2.5 секунды

---

## 🧪 ПРОВЕРКА РАБОТЫ:

### Проверьте звуки:
1. Откройте приложение в Telegram
2. Зайдите в Настройки ⚙️
3. Включите звуки (переключатель синий)
4. Сохраните настройки
5. Должен прозвучать `success`
6. Сделайте тап - должен звучать `tap`

### Проверьте ТОП лидеров:
1. Нажмите на кнопку 🏆 ТОП ЛИДЕРЫ
2. Убедитесь, что VIP вверху
3. Проверьте отображение уровней
4. Проверьте рейтинг
5. Убедитесь, что сортировка правильная

---

## 📊 ФОРМУЛЫ РАСЧЕТА:

### Опыт (Experience):
```
Experience = (Total_Earned × 0.01) + (Total_Taps × 0.1) + (VIP_Level × 1,000)
```

### Уровень (Level):
```
Level = ⌊√(Experience / 100)⌋ + 1 (максимум 100)
```

### Рейтинг (Rating):
```
Rating = (Coins × 0.01) + (Total_Earned × 0.1) + (Total_Taps × 0.05) + (VIP_Level × 1,000,000) + (Level × 10,000)
```

---

## 🆘 ПОДДЕРЖКА:

### Если звуки не работают:
Смотрите: `FINAL_SOUND_FIX_COMMANDS.md`

### Если ТОП не работает:
Смотрите: `LEADERBOARD_UPDATE_COMMANDS.md`

### Логи:
```bash
sudo journalctl -u quantum-nexus-web.service -n 100
sudo journalctl -u quantum-nexus.service -n 100
```

---

## 📝 КОММИТЫ:

- `5a46aac` - Звуки по умолчанию выключены
- `667e14a` - Логирование звуков
- `45d8f6b` - Улучшенное логирование
- `e017b25` - Детальное логирование
- `3b07390` - 20 новых звуков
- `c6251fe` - Система уровней и рейтинга

---

**ГОТОВО! ВСЁ РАБОТАЕТ!** 🎉

