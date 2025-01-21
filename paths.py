import os

# Получаем абсолютный путь к корневой директории проекта
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Пути к директориям
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SPRITES_DIR = os.path.join(IMAGES_DIR, 'sprites')
BACKGROUNDS_DIR = os.path.join(IMAGES_DIR, 'backgrounds')
ENEMIES_DIR = os.path.join(IMAGES_DIR, 'enemies')
MUSIC_DIR = os.path.join(ASSETS_DIR, 'music')
SOUNDS_DIR = os.path.join(MUSIC_DIR, 'sounds')