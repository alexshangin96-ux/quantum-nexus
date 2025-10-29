#!/bin/bash
# Скрипт для автоматического восстановления базы данных

echo "🔧 Восстановление базы данных Quantum Nexus..."

# 1. Запускаем PostgreSQL если не запущен
echo "1. Проверка PostgreSQL..."
if ! sudo systemctl is-active --quiet postgresql; then
    echo "   PostgreSQL не запущен, запускаю..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# 2. Создаем пользователя если не существует
echo "2. Проверка пользователя..."
sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='quantum'" | grep -q 1 || sudo -u postgres psql -c "CREATE USER quantum WITH PASSWORD 'quantum123';"

# 3. Создаем базу данных если не существует
echo "3. Проверка базы данных..."
sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='quantum'" | grep -q 1 || sudo -u postgres psql -c "CREATE DATABASE quantum;"

# 4. Даем права
echo "4. Выдача прав..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE quantum TO quantum;"

# 5. Переходим в директорию проекта
cd ~/quantum-nexus || exit 1

# 6. Активируем виртуальное окружение
source venv/bin/activate || exit 1

# 7. Восстанавливаем таблицы
echo "5. Восстановление таблиц..."
python3 -c "from database import Base, engine; Base.metadata.drop_all(engine); Base.metadata.create_all(engine)"

# 8. Проверяем результат
echo "6. Проверка результата..."
python3 -c "from database import get_db; from models import User; db = next(get_db()); count = db.query(User).count(); print(f'Пользователей в базе: {count}')"

# 9. Перезапускаем сервисы
echo "7. Перезапуск сервисов..."
sudo systemctl restart quantum-nexus
sudo systemctl restart quantum-nexus-web

echo "✅ База данных восстановлена!"
echo ""
echo "Проверьте статус:"
echo "sudo systemctl status quantum-nexus"
echo "sudo systemctl status quantum-nexus-web"



