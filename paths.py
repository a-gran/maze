# constants.py
import os

# Получаем абсолютный путь к директории
GAME_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(GAME_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SPRITES_DIR = os.path.join(IMAGES_DIR, 'sprites')
BACKGROUNDS_DIR = os.path.join(IMAGES_DIR, 'backgrounds')
ENEMIES_DIR = os.path.join(IMAGES_DIR, 'enemies')
MUSIC_DIR = os.path.join(ASSETS_DIR, 'music')
SOUNDS_DIR = os.path.join(MUSIC_DIR, 'sounds')
