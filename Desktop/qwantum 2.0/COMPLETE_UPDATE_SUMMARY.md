# 🎯 ПОЛНАЯ ИНСТРУКЦИЯ ПО ОБНОВЛЕНИЮ

## ✅ ВСЁ ГОТОВО И ОТПРАВЛЕНО НА GITHUB!

---

## 🚀 ГЛАВНАЯ КОМАНДА (Копируйте и вставьте ВСЮ строку):

```bash
cd /root/quantum-nexus && git pull origin main && chmod +x UPDATE_COMMANDS_FIXED.sh && ./UPDATE_COMMANDS_FIXED.sh
```

**Эта команда сделает ВСЁ автоматически!**

---

## 📋 ЧТО ДОБАВЛЕНО:

### 🔊 Система звуков (35 звуков):
- ✅ Звук выключен по умолчанию
- ✅ Переключатель включает/выключает ВСЕ звуки
- ✅ 20 новых Crypto Tapping звуков
- ✅ Полное логирование для отладки
- ✅ Автоматическое управление AudioContext

### 🏆 Система ТОП лидеров:
- ✅ **Уровни**: 1-100 на основе опыта
- ✅ **Опыт**: Зависит от заработанных монет, тапов и VIP
- ✅ **Рейтинг**: Комплексный балл для сортировки
- ✅ **Сортировка**: VIP всегда вверху, затем по рейтингу
- ✅ Красивый UI с медалями
- ✅ Автообновление каждые 2.5 секунды
- ✅ Кнопка "Обновить" вручную

---

## 📁 ФАЙЛЫ ДОКУМЕНТАЦИИ:

1. **`EXECUTE_ON_SERVER.sh`** - Главная команда для сервера
2. **`quantum-nexus/UPDATE_COMMANDS_FIXED.sh`** - Полный скрипт обновления
3. **`quantum-nexus/ADD_LEVEL_SYSTEM.sql`** - SQL миграция
4. **`FINAL_UPDATE_ALL.md`** - Инструкция по обновлению
5. **`LEADERBOARD_UPDATE_COMMANDS.md`** - Детальная инструкция по БД
6. **`FINAL_SOUND_FIX_COMMANDS.md`** - Отладка звуков
7. **`UPDATE_SOUNDS_SYSTEM.md`** - Гайд по звукам

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

**VIP всегда вверху благодаря множителю ×1,000,000!**

---

## ✅ ПРОВЕРКА ПОСЛЕ ОБНОВЛЕНИЯ:

### Звуки:
1. Откройте приложение
2. Настройки → Включите звуки
3. Сохраните
4. Должен прозвучать sound `success`
5. Тап должен играть sound `tap`

### ТОП лидеры:
1. Нажмите 🏆
2. Убедитесь что VIP вверху
3. Проверьте отображение уровней
4. Проверьте рейтинг
5. Проверьте автообновление

---

## 🆘 ПОДДЕРЖКА:

### Логи сервера:
```bash
sudo journalctl -u quantum-nexus-web.service -n 100
sudo journalctl -u quantum-nexus.service -n 100
```

### Откат миграции БД (если нужно):
```bash
sudo -u postgres psql quantum_nexus
ALTER TABLE users DROP COLUMN IF EXISTS level;
ALTER TABLE users DROP COLUMN IF EXISTS experience;
ALTER TABLE users DROP COLUMN IF EXISTS rating;
\q
```

### Откат кода:
```bash
cd /root/quantum-nexus
git reset --hard HEAD~1
sudo systemctl restart quantum-nexus-web.service
```

---

## 📝 КОММИТЫ:

- `5a46aac` - Звуки отключены по умолчанию
- `667e14a` - Логирование звуков
- `45d8f6b` - Улучшенное логирование
- `e017b25` - Детальное логирование
- `3b07390` - 20 новых звуков
- `c6251fe` - Система уровней и рейтинга
- `aa5ec7a` - Исправленный скрипт

---

**🎉 ВСЁ ГОТОВО! ВЫПОЛНИТЕ КОМАНДУ НА СЕРВЕРЕ!** 🎉

