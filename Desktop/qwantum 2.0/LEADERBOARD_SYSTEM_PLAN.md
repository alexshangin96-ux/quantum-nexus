# 🏆 План реализации системы ТОП лидеров с уровнями

## 📋 Что нужно сделать:

### 1. Добавить поле `level` в модель User
```python
# В models.py добавить:
level = Column(Integer, default=1)  # Уровень пользователя
experience = Column(Float, default=0)  # Опыт пользователя
rating = Column(Float, default=0)  # Рейтинг (общий балл)
```

### 2. Создать миграцию для добавления поля
```sql
-- Добавить в таблицу users:
ALTER TABLE users ADD COLUMN level INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN experience FLOAT DEFAULT 0;
ALTER TABLE users ADD COLUMN rating FLOAT DEFAULT 0;
```

### 3. Реализовать расчет уровня
```python
def calculate_level(experience):
    """Рассчитывает уровень на основе опыта"""
    # Формула: level = sqrt(experience / 100) + 1
    level = int((experience / 100) ** 0.5) + 1
    return min(level, 100)  # Максимум 100 уровень

def calculate_experience(total_earned, total_taps, vip_level):
    """Рассчитывает опыт на основе активности"""
    base_exp = total_earned * 0.01  # 1% от заработанных монет
    tap_bonus = total_taps * 0.1  # За каждый тап
    vip_bonus = vip_level * 1000  # VIP бонус
    
    return base_exp + tap_bonus + vip_bonus

def calculate_rating(coins, total_earned, total_taps, vip_level, level):
    """Рассчитывает рейтинг пользователя"""
    coins_score = coins * 0.01
    earned_score = total_earned * 0.1
    taps_score = total_taps * 0.05
    vip_score = vip_level * 1000000  # VIP всегда в топе
    level_score = level * 10000
    
    rating = coins_score + earned_score + taps_score + vip_score + level_score
    return rating
```

### 4. Обновить эндпоинт top_users для сортировки
```python
@app.route('/api/top_users', methods=['POST'])
def top_users():
    """Get top users sorted by rating"""
    limit = request.json.get('limit', 100)
    
    with get_db() as db:
        users = db.query(User).all()
        
        # Рассчитываем rating для каждого пользователя
        for user in users:
            user.rating = calculate_rating(
                user.coins,
                user.total_earned,
                user.total_taps,
                user.vip_level or 0,
                user.level or 1
            )
            user.level = calculate_level(user.experience or 0)
        
        # Сортируем: VIP first, потом по rating
        sorted_users = sorted(users, key=lambda u: (
            -(u.vip_level or 0),  # VIP сначала (в обратном порядке)
            -(u.rating or 0)  # Потом по рейтингу
        ))
        
        return jsonify({
            'users': [format_user(u) for u in sorted_users[:limit]]
        })
```

### 5. Обновить UI топ лидеров
- Добавить уровень рядом с именем
- Показать рейтинг
- Добавить прогресс-бар опыта
- Показать "Вип-бейдж" для VIP пользователей
- Добавить анимацию обновления

### 6. Автоматическое обновление
- Каждые 10 секунд обновлять топ
- Показывать индикатор обновления
- Кнопка "Обновить" для ручного обновления

---

## 🚀 Команды для реализации:

### 1. Обновить модель:
```bash
cd quantum-nexus
nano models.py
# Добавить поля: level, experience, rating
```

### 2. Создать миграцию:
```bash
python3 -c "from models import *; from database import engine; Base.metadata.create_all(engine)"
```

### 3. Обновить web_server.py:
```bash
nano web_server.py
# Добавить функции расчета и обновить эндпоинт
```

### 4. Обновить frontend:
```bash
nano web_app.html
# Обновить openVIPTopLeaders()
```

### 5. Перезапустить сервисы:
```bash
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus.service
```

---

## ✅ Текущий статус:
- ✅ UI топ лидеров уже есть
- ✅ VIP система работает
- ✅ Сортировка частично работает
- ❌ Нет системы уровней
- ❌ Нет расчета рейтинга
- ❌ Нет автогенерации опыта

---

## 📊 Формула рейтинга:
```
Rating = (Coins × 0.01) + (Total_Earned × 0.1) + (Total_Taps × 0.05) + (VIP_Level × 1,000,000) + (Level × 10,000)
```

VIP пользователи ВСЕГДА в топе благодаря большому множителю.

---

**Сделайте это и система будет работать!** 🎯

