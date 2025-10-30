# Команды для обновления на сервере

Выполните на сервере:

```bash
cd ~/quantum-nexus
git pull origin main
sudo cp web_app.html admin.html web_server.py models.py /var/www/quantum-nexus/
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web
```

Если нужно восстановить базу данных:

```bash
# Проверка, какая база используется
cat .env || echo "Using default: quantum_nexus"

# Создание таблиц
python3 << 'EOF'
from database import engine
from models import Base
Base.metadata.create_all(engine)
print("✅ Tables created!")
EOF

# Проверка таблиц
sudo -u postgres psql quantum_nexus -c "\dt"
```

После этого всё должно работать!





