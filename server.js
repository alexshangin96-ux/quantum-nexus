const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Путь к файлу данных
const gameDataPath = path.join(__dirname, 'gameData.json');

// Функция для загрузки данных игры
function loadGameData() {
    try {
        if (fs.existsSync(gameDataPath)) {
            const data = fs.readFileSync(gameDataPath, 'utf8');
            return JSON.parse(data);
        }
        return {};
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        return {};
    }
}

// Функция для сохранения данных игры
function saveGameData(data) {
    try {
        fs.writeFileSync(gameDataPath, JSON.stringify(data, null, 2));
        console.log('Данные сохранены:', data);
        return true;
    } catch (error) {
        console.error('Ошибка сохранения данных:', error);
        return false;
    }
}

// API для загрузки данных игры
app.get('/api/game/:userId/load', (req, res) => {
    const userId = req.params.userId;
    console.log('Запрос на загрузку данных для пользователя:', userId);
    
    try {
        const gameData = loadGameData();
        const userData = gameData[userId];
        
        if (userData) {
            console.log('Найдены данные для пользователя:', userId, userData);
            res.json({
                success: true,
                gameData: userData
            });
        } else {
            console.log('Данные не найдены для пользователя:', userId);
            res.json({
                success: true,
                gameData: {
                    totalTaps: 0,
                    coins: 0,
                    level: 1,
                    bitcoin: 0,
                    multiplier: 1,
                    energy: 100,
                    maxEnergy: 100
                }
            });
        }
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        res.status(500).json({
            success: false,
            error: 'Ошибка загрузки данных'
        });
    }
});

// API для сохранения данных игры
app.post('/api/game/:userId/save', (req, res) => {
    const userId = req.params.userId;
    const userData = req.body;
    
    console.log('Запрос на сохранение данных для пользователя:', userId, userData);
    
    try {
        const gameData = loadGameData();
        gameData[userId] = userData;
        
        if (saveGameData(gameData)) {
            console.log('Данные успешно сохранены для пользователя:', userId);
            res.json({ success: true });
        } else {
            console.error('Ошибка сохранения данных для пользователя:', userId);
            res.status(500).json({ success: false, error: 'Ошибка сохранения' });
        }
    } catch (error) {
        console.error('Ошибка сохранения данных:', error);
        res.status(500).json({
            success: false,
            error: 'Ошибка сохранения данных'
        });
    }
});

// Главная страница
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Тестовая страница
app.get('/test', (req, res) => {
    res.json({
        status: 'OK',
        message: 'Quantum Nexus Server is running!',
        timestamp: new Date().toISOString()
    });
});

// Запуск сервера
app.listen(PORT, () => {
    console.log('Quantum Nexus server running on port', PORT);
    console.log('Game available at: http://localhost:' + PORT);
    console.log('Test endpoint: http://localhost:' + PORT + '/test');
});


