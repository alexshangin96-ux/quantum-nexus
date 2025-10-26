# Исправление базы данных

Если база данных "слетела", выполните на сервере:

## 1. Проверьте статус PostgreSQL
```bash
sudo systemctl status postgresql
```

Если не запущен, запустите:
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## 2. Проверьте, существует ли база данных
```bash
sudo -u postgres psql -c "\l" | grep quantum
```

Если база не найдена, создайте её:
```bash
sudo -u postgres psql -c "CREATE DATABASE quantum;"
```

## 3. Проверьте пользователя
```bash
sudo -u postgres psql -c "\du" | grep quantum
```

Если пользователь не найден, создайте:
```bash
sudo -u postgres psql -c "CREATE USER quantum WITH PASSWORD 'quantum123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE quantum TO quantum;"
```

## 4. Восстановите таблицы
```bash
cd ~/quantum-nexus
source venv/bin/activate
python3 -c "from database import Base, engine; Base.metadata.drop_all(engine); Base.metadata.create_all(engine)"
```

## 5. Проверьте, что все работает
```bash
python3 -c "from database import get_db; from models import User; db = next(get_db()); print(f'Users in DB: {db.query(User).count()}')"
```

## 6. Перезапустите сервисы
```bash
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
```

Если проблемы остаются, проверьте логи:
```bash
sudo journalctl -u quantum-nexus -f
```
