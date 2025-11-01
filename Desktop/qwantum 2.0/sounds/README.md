# Game Sounds Directory

This directory contains sound files for the game.

## Sound Files Required:

- `tap.mp3` - Sound for tap actions (Stage 1 test sound)
- `mining.mp3` - Sound for mining actions (Stage 2 test sound)
- `purchase.mp3` - Sound for purchase actions (Stage 3 test sound)
- `level_up.mp3` - Sound for level up events
- `achievement.mp3` - Sound for achievement unlocks
- `default.mp3` - Default sound

## Usage:

Sounds are controlled via the user's profile settings. Users can toggle sounds on/off in the Profile menu.

## Integration:

Sounds are played in the web app using HTML5 Audio API. The bot sends sound event signals, and the web app handles actual playback based on user preferences.

## Test Sounds:

Three test sound buttons are available in the Profile menu:
1. Тест звука 1 - Plays tap sound
2. Тест звука 2 - Plays mining sound  
3. Тест звука 3 - Plays purchase sound

