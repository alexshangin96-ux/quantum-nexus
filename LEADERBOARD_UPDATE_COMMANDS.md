# 🏆 Команды для обновления системы ТОП лидеров

## ⚠️ ВАЖНО: Эти команды нужно выполнить НА СЕРВЕРЕ Selectel

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

### 4. Выполните SQL миграцию для добавления полей в базу данных:

#### Вариант A: Через psql (PostgreSQL):
```bash
# Подключитесь к PostgreSQL
sudo -u postgres psql quantum_nexus

# Выполните миграцию
ALTER TABLE users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN IF NOT EXISTS experience FLOAT DEFAULT 0.0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 0.0;

# Обновите существующих пользователей
UPDATE users 
SET experience = (total_earned * 0.01) + (total_taps * 0.1) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000),
    level = LEAST(100, FLOOR(SQRT(GREATEST(0, experience) / 100) + 1)),
    rating = (coins * 0.01) + (total_earned * 0.1) + (total_taps * 0.05) + ((CASE WHEN vip_level IS NOT NULL THEN vip_level ELSE 0 END) * 1000000) + (level * 10000)
WHERE level IS NULL OR experience IS NULL OR rating IS NULL;

# Проверьте результат
SELECT COUNT(*) as total_users, AVG(level) as avg_level, MAX(level) as max_level, AVG(rating) as avg_rating, MAX(rating) as max_rating FROM users;

# Выход
\q
```

#### Вариант B: Через Python скрипт:
```bash
cd /root/quantum-nexus
python3 <<EOF
from database import get_db
from models import User
import math

def calculate_level(experience):
    if experience <= 0:
        return 1
    level = int((experience / 100) ** 0.5) + 1
    return min(level, 100)

def calculate_experience(total_earned, total_taps, vip_level):
    base_exp = (total_earned or 0) * 0.01
    tap_bonus = (total_taps or 0) * 0.1
    vip_bonus = (vip_level or 0) * 1000
    return base_exp + tap_bonus + vip_bonus

def calculate_rating(coins, total_earned, total_taps, vip_level, level):
    coins_score = (coins or 0) * 0.01
    earned_score = (total_earned or 0) * 0.1
    taps_score = (total_taps or 0) * 0.05
    vip_score = (vip_level or 0) * 1000000
    level_score = (level or 1) * 10000
    return coins_score + earned_score + taps_score + vip_score + level_score

try:
    with get_db() as db:
        # Add columns if they don't exist
        from sqlalchemy import text
        db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1"))
        db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS experience FLOAT DEFAULT 0.0"))
        db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 0.0"))
        db.commit()
        print("✅ Columns added successfully")
        
        # Update all users
        users = db.query(User).all()
        updated = 0
        for u in users:
            exp = calculate_experience(u.total_earned, u.total_taps, getattr(u, 'vip_level', 0) or 0)
            lvl = calculate_level(exp)
            rtg = calculate_rating(u.coins, u.total_earned, u.total_taps, getattr(u, 'vip_level', 0) or 0, lvl)
            
            u.level = lvl
            u.experience = exp
            u.rating = rtg
            updated += 1
        
        db.commit()
        print(f"✅ Updated {updated} users")
        print("✅ Migration completed successfully!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
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

### 8. Проверьте логи:
```bash
sudo journalctl -u quantum-nexus-web.service -n 50
sudo journalctl -u quantum-nexus.service -n 50
```

---

## 🚀 БЫСТРАЯ КОМАНДА (ВСЁ ВМЕСТЕ):

```bash
cd /root/quantum-nexus && git pull origin main && sudo -u postgres psql quantum_nexus -c "ALTER TABLE users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1;" && sudo -u postgres psql quantum_nexus -c "ALTER TABLE users ADD COLUMN IF NOT EXISTS experience FLOAT DEFAULT 0.0;" && sudo -u postgres psql quantum_nexus -c "ALTER TABLE users ADD COLUMN IF NOT EXISTS rating FLOAT DEFAULT 0.0;" && sudo -u postgres psql quantum_nexus -f ADD_LEVEL_SYSTEM.sql && sudo cp web_app.html /var/www/quantum-nexus/web_app.html && sudo systemctl restart quantum-nexus-web.service && sudo systemctl restart quantum-nexus.service
```

---

## ✅ После обновления проверьте:

1. Откройте приложение в Telegram
2. Нажмите на кнопку 🏆 ТОП ЛИДЕРЫ
3. Проверьте, что:
   - VIP пользователи вверху
   - Отображаются уровни
   - Отображается рейтинг
   - Сортировка правильная

---

## 📊 Формулы расчета:

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

VIP пользователи ВСЕГДА в топе благодаря большому множителю × 1,000,000!

---

## 🆘 Если что-то пошло не так:

### Откат миграции:
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
git push --force origin main
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service
```

---

**ГОТОВО!** 🎉

