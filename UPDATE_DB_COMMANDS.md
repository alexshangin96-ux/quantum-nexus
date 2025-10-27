# Команды для обновления базы данных

## PostgreSQL команды

Для добавления новых полей в таблицу users:

```bash
# Подключиться к базе данных
psql -U quantum -d quantum_nexus

# Или если нужен пароль:
sudo -u postgres psql quantum_nexus
```

Затем выполните в psql:

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_passive_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_hash_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

# Проверить изменения
\d users

# Выход
\q
```

## Альтернативный способ через Python

Если прямой доступ к psql затруднен, создайте миграцию:

```bash
python3 -c "
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS last_passive_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP'))
    conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS last_hash_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP'))
    conn.commit()
print('Migration completed')
"
```


