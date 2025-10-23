#!/bin/bash

# Quantum Nexus - GitHub Upload Script
# Автоматическая загрузка проекта на GitHub

echo "🚀 Quantum Nexus - GitHub Upload Script"
echo "========================================"

# Проверка наличия Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите Git и попробуйте снова."
    exit 1
fi

# Проверка наличия файлов
if [ ! -f "quantum-nexus.html" ]; then
    echo "❌ Файл quantum-nexus.html не найден. Убедитесь, что вы находитесь в правильной директории."
    exit 1
fi

# Запрос GitHub username
read -p "📝 Введите ваш GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username не может быть пустым."
    exit 1
fi

# Запрос названия репозитория
read -p "📝 Введите название репозитория (по умолчанию: quantum-nexus): " REPO_NAME
REPO_NAME=${REPO_NAME:-quantum-nexus}

echo ""
echo "🔧 Настройка Git репозитория..."

# Инициализация Git (если еще не инициализирован)
if [ ! -d ".git" ]; then
    echo "📁 Инициализация Git репозитория..."
    git init
else
    echo "✅ Git репозиторий уже инициализирован"
fi

# Добавление всех файлов
echo "📦 Добавление файлов в Git..."
git add .

# Проверка статуса
echo "📊 Статус Git репозитория:"
git status

echo ""
read -p "🤔 Продолжить с коммитом? (y/n): " CONTINUE

if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
    echo "❌ Операция отменена."
    exit 1
fi

# Создание коммита
echo "💾 Создание коммита..."
git commit -m "🚀 Initial commit: Quantum Nexus - Ultimate Tap Revolution

✨ Features:
- Квантовое ядро с WebGL эффектами
- Telegram Stars интеграция
- Криптовалюты (Bitcoin, Ethereum)
- NFT маркетплейс
- AR/VR режим
- Социальные функции
- AI-ассистент
- Полная русская локализация

🎮 Game mechanics:
- Система энергии и регенерации
- Уровни и опыт
- Power-ups за звезды
- Достижения
- Статистика в реальном времени

💰 Monetization:
- Telegram Stars платежи
- Криптомайнинг
- NFT торговля
- VIP подписки

🛠️ Tech Stack:
- Frontend: HTML5, CSS3, JavaScript ES6+
- Backend: Node.js, Express.js
- API: Telegram Bot API
- Effects: Particle systems, Neural networks"

# Добавление удаленного репозитория
echo "🌐 Настройка удаленного репозитория..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Загрузка на GitHub
echo "⬆️ Загрузка на GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Успешно загружено на GitHub!"
    echo "🔗 Репозиторий: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo ""
    echo "📋 Следующие шаги:"
    echo "1. Перейдите на https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "2. Проверьте, что все файлы загружены"
    echo "3. Настройте GitHub Pages (опционально)"
    echo "4. Подготовьтесь к развертыванию на Selectel"
    echo ""
    echo "🚀 Готово! Теперь можно развертывать на Selectel."
else
    echo ""
    echo "❌ Ошибка загрузки на GitHub."
    echo "💡 Возможные причины:"
    echo "- Неправильный username или название репозитория"
    echo "- Репозиторий не существует на GitHub"
    echo "- Проблемы с аутентификацией"
    echo ""
    echo "🔧 Решения:"
    echo "1. Создайте репозиторий на GitHub вручную"
    echo "2. Проверьте настройки аутентификации Git"
    echo "3. Попробуйте использовать SSH вместо HTTPS"
    echo ""
    echo "📝 Для создания репозитория вручную:"
    echo "1. Перейдите на https://github.com/new"
    echo "2. Название: $REPO_NAME"
    echo "3. Описание: Ultimate Tap Revolution - The most powerful tap game"
    echo "4. Сделайте репозиторий публичным"
    echo "5. НЕ инициализируйте с README, .gitignore или лицензией"
    echo "6. Нажмите 'Create repository'"
    echo "7. Запустите этот скрипт снова"
fi

echo ""
echo "📚 Дополнительная информация:"
echo "- Документация: README.md"
echo "- Конфигурация: .env.example"
echo "- Игнорируемые файлы: .gitignore"
echo "- Основной файл: quantum-nexus.html"
echo "- Сервер: server.js"
echo ""
echo "🎮 Quantum Nexus готов к развертыванию!"
