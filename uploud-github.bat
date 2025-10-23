@echo off
REM Quantum Nexus - GitHub Upload Script for Windows
echo 🚀 Quantum Nexus - GitHub Upload Script
echo ========================================

REM Проверка наличия Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git не установлен. Установите Git и попробуйте снова.
    echo 📥 Скачайте Git с https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Проверка наличия файлов
if not exist "quantum-nexus.html" (
    echo ❌ Файл quantum-nexus.html не найден.
    echo Убедитесь, что вы находитесь в правильной директории.
    pause
    exit /b 1
)

REM Запрос GitHub username
set /p GITHUB_USERNAME="📝 Введите ваш GitHub username: "
if "%GITHUB_USERNAME%"=="" (
    echo ❌ GitHub username не может быть пустым.
    pause
    exit /b 1
)

REM Запрос названия репозитория
set /p REPO_NAME="📝 Введите название репозитория (по умолчанию: quantum-nexus): "
if "%REPO_NAME%"=="" set REPO_NAME=quantum-nexus

echo.
echo 🔧 Настройка Git репозитория...

REM Инициализация Git
if not exist ".git" (
    echo 📁 Инициализация Git репозитория...
    git init
) else (
    echo ✅ Git репозиторий уже инициализирован
)

REM Добавление файлов
echo 📦 Добавление файлов в Git...
git add .

echo 📊 Статус Git репозитория:
git status

echo.
set /p CONTINUE="🤔 Продолжить с коммитом? (y/n): "
if /i not "%CONTINUE%"=="y" (
    echo ❌ Операция отменена.
    pause
    exit /b 1
)

REM Создание коммита
echo 💾 Создание коммита...
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

REM Настройка удаленного репозитория
echo 🌐 Настройка удаленного репозитория...
git remote remove origin 2>nul
git remote add origin "https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git"

REM Загрузка на GitHub
echo ⬆️ Загрузка на GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Успешно загружено на GitHub!
    echo 🔗 Репозиторий: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo.
    echo 📋 Следующие шаги:
    echo 1. Перейдите на https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo 2. Проверьте, что все файлы загружены
    echo 3. Подготовьтесь к развертыванию на Selectel
) else (
    echo.
    echo ❌ Ошибка загрузки на GitHub.
    echo 💡 Создайте репозиторий на GitHub вручную:
    echo 1. Перейдите на https://github.com/new
    echo 2. Название: %REPO_NAME%
    echo 3. Сделайте репозиторий публичным
    echo 4. НЕ инициализируйте с README
    echo 5. Запустите скрипт снова
)

echo.
echo 🎮 Quantum Nexus готов к развертыванию!
pause
