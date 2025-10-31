# Инструкция по обновлению майнинга

## Важно: Новая версия майнинга v6.0

### 1. Обновление кода с GitHub
```bash
cd /root/quantum-nexus
git pull origin main
```

### 2. Копирование файлов
```bash
sudo cp web_server.py /var/www/quantum-nexus/web_server.py
sudo cp web_app.html /var/www/quantum-nexus/web_app.html
sudo cp models.py /var/www/quantum-nexus/models.py
```

### 3. Миграция базы данных (опционально)
Новые поля должны добавиться автоматически при первом использовании. Если нужна ручная миграция:

```bash
cd /root/quantum-nexus
python3 migration_add_mining_levels.py
```

Или вручную через Python:
```bash
python3 <<EOF
from database import get_db
from models import User

with get_db() as db:
    users = db.query(User).all()
    for user in users:
        if not hasattr(user, 'mining_coins_levels'):
            user.mining_coins_levels = '{}'
        if not hasattr(user, 'mining_quanhash_levels'):
            user.mining_quanhash_levels = '{}'
        if not hasattr(user, 'mining_vip_levels'):
            user.mining_vip_levels = '{}'
    db.commit()
    print(f"Updated {len(users)} users")
EOF
```

### 4. Перезапуск сервисов
```bash
sudo systemctl restart quantum-nexus-web.service
sudo systemctl restart quantum-nexus
```

### 5. Проверка логов
```bash
sudo systemctl status quantum-nexus-web.service
sudo journalctl -u quantum-nexus-web.service -f
```

## Что нового в v6.0:
- ✅ Полностью переработанный майнинг с реалистичными значениями
- ✅ Красивые описания и тематические названия
- ✅ Многоуровневая система покупки машин
- ✅ Правильные тексты кнопок и доходов
- ✅ Уменьшенные VIP цены
- ✅ Интеграция с базой данных для уровней
- ✅ Группировка купленных машин (x2, x3 и т.д.)

## Категории машин:

### За коины 🪙
- CPU Майнер (5000 коинов)
- GPU Майнер (20000 коинов)
- ASIC Риг (80000 коинов)
- Quantum Майнер (300000 коинов)
- Server Ферма (1000000 коинов)
- Cloud Риг (3500000 коинов)
- Data Центр (12000000 коинов)
- Quantum Ферма (40000000 коинов)
- Neural Майнер (150000000 коинов)
- Cosmic Станция (500000000 коинов)

### За QuanHash 💎
- Quantum Ядро (10000 💎)
- Plasma Риг (50000 💎)
- Stellar Блок (250000 💎)
- Cosmic Поток (1000000 💎)
- Nova Ускоритель (4000000 💎)
- Galaxy Матрица (15000000 💎)
- Void Порталы (60000000 💎)
- Eternal Движитель (250000000 💎)
- Divine Генератор (1000000000 💎)
- Absolute Мощь (4000000000 💎)

### VIP Машины ⭐
- Quantum Prime (50 ⭐)
- Solar Core (100 ⭐)
- Black Hole (150 ⭐)
- Nebula Ферма (250 ⭐)
- Multiverse Станция (400 ⭐)
- Infinity Альянс (750 ⭐)

Все машины имеют многоуровневую систему с ростом цены и дохода!


