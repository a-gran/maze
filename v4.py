# Импортируем pygame для создания игры и os для работы с путями к файлам
import pygame
import os

# Инициализируем все модули pygame
pygame.init()
# Инициализируем подсистему для работы со шрифтами

# Получаем абсолютный путь к директории, где находится текущий файл
GAME_DIR = os.path.dirname(os.path.abspath(__file__))
# Создаем пути к различным директориям с ресурсами игры
ASSETS_DIR = os.path.join(GAME_DIR, 'assets')  # Директория с ресурсами
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')  # Директория с изображениями
SPRITES_DIR = os.path.join(IMAGES_DIR, 'sprites')  # Директория со спрайтами
BACKGROUNDS_DIR = os.path.join(IMAGES_DIR, 'backgrounds')  # Директория с фонами
ENEMIES_DIR = os.path.join(IMAGES_DIR, 'enemies')  # Директория с врагами
MUSIC_DIR = os.path.join(ASSETS_DIR, 'music')  # Директория с музыкой
SOUNDS_DIR = os.path.join(MUSIC_DIR, 'sounds')  # Директория со звуками

# Создаем список всех необходимых директорий
required_dirs = [ASSETS_DIR, IMAGES_DIR, SPRITES_DIR, BACKGROUNDS_DIR, 
                ENEMIES_DIR, MUSIC_DIR, SOUNDS_DIR]
# Проверяем существование каждой директории и создаем её, если она отсутствует
for directory in required_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Создана директория: {directory}")

# Определяем константы цветов в формате RGB
WALL_WHITE = (255, 255, 255)  # Белый цвет
WALL_RED = (255, 0, 0)        # Красный цвет
WALL_GREEN = (0, 255, 0)      # Зеленый цвет
WALL_BLUE = (0, 0, 255)       # Синий цвет
WALL_BLACK = (0, 0, 0)        # Черный цвет
WIN = (255, 215, 0)           # Золотой цвет для сообщения о победе
LOSE = (180, 0, 0)            # Темно-красный цвет для сообщения о поражении

# Базовый класс для всех игровых объектов, наследуется от pygame.sprite.Sprite
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, player_x, player_y, player_speed):
        # Вызываем конструктор родительского класса
        super().__init__()
        # Масштабируем изображение до размера 65x65 пикселей
        self.image = pygame.transform.scale(image, (65, 65))
        # Сохраняем скорость объекта
        self.speed = player_speed
        # Получаем прямоугольник (область) спрайта
        self.rect = self.image.get_rect()
        # Устанавливаем начальные координаты
        self.rect.x = player_x
        self.rect.y = player_y

    # Метод для отрисовки спрайта на экране
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока, наследуется от GameSprite
class Player(GameSprite):
    def update(self):
        # Получаем словарь нажатых клавиш
        keys = pygame.key.get_pressed()
        
        # Обработка движения влево с проверкой границы
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        # Обработка движения вправо с проверкой границы
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        # Обработка движения вверх с проверкой границы
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        # Обработка движения вниз с проверкой границы
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Класс врага, наследуется от GameSprite
class Enemy(GameSprite):
    # Начальное направление движения
    direction = 'left'
    
    def update(self):
        # Сохраняем текущую позицию перед движением
        previous_x = self.rect.x
        
        # Движение в зависимости от текущего направления
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
        # Проверяем столкновения со стенами
        collision_occurred = False
        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                collision_occurred = True
                break
        
        # Обработка столкновений и изменение направления
        if collision_occurred:
            # Возвращаем врага на предыдущую позицию
            self.rect.x = previous_x
            # Меняем направление движения
            self.direction = 'right' if self.direction == 'left' else 'left'
        else:
            # Проверка и обработка достижения границ экрана
            if self.rect.x <= 50:
                self.direction = 'right'
            if self.rect.x >= win_width - 50:
                self.direction = 'left'

# Класс стены, наследуется от pygame.sprite.Sprite
class Wall(pygame.sprite.Sprite):
    def __init__(self, thickness, color, wall_x, wall_y, length, is_vertical, type_wall=None, name=None):
        super().__init__()
        # Сохраняем параметры стены
        self.thickness = thickness  # Толщина стены
        self.color = color  # Цвет стены
        self.wall_x = wall_x  # Координата X
        self.wall_y = wall_y  # Координата Y
        self.is_vertical = is_vertical  # Вертикальная или горизонтальная
        self.length = length  # Длина стены
        self.type_wall = type_wall  # Тип стены
        self.name = name  # Название стены
        
        # Определяем размеры стены в зависимости от ориентации
        if is_vertical:
            self.width = thickness
            self.height = length
        else:
            self.width = length
            self.height = thickness
            
        # Создаем поверхность стены и заполняем её цветом
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        # Получаем прямоугольник стены и устанавливаем его позицию
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    # Метод для отрисовки стены
    def draw_wall(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Функция для создания списка стен из параметров
def create_walls(walls_list):
    wall_objects = []
    for wall_params in walls_list:
        wall = Wall(
            thickness=wall_params[0],  # Толщина
            color=wall_params[1],      # Цвет
            wall_x=wall_params[2],     # Позиция X
            wall_y=wall_params[3],     # Позиция Y
            length=wall_params[4],     # Длина
            is_vertical=wall_params[5], # Ориентация
            type_wall=wall_params[6],  # Тип
            name=wall_params[7]        # Название
        )
        wall_objects.append(wall)
    return wall_objects

# Список параметров для создания стен
walls_list = [
    [10, WALL_WHITE, 200, 40, 600, True, 'barricada', 'левая стена'],
    [40, WALL_BLACK, 200, 800, 500, False, 'barricada', 'правая нижняя горизонтальная стена']
]

# Устанавливаем размеры игрового окна
win_width = 1000   # Ширина окна
win_height = 1000  # Высота окна

# Создаем игровое окно и устанавливаем заголовок
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Лабиринт')

# Загружаем все игровые изображения
player_img = pygame.image.load(os.path.join(SPRITES_DIR, 'hero.png'))
cyborg_img = pygame.image.load(os.path.join(ENEMIES_DIR, 'cyborg.png'))
treasure_img = pygame.image.load(os.path.join(SPRITES_DIR, 'treasure.png'))

# Загружаем и масштабируем фоновое изображение
background = pygame.transform.scale(
    pygame.image.load(os.path.join(BACKGROUNDS_DIR, 'background1.jpg')), 
    (win_width, win_height)
)

# Создаем игровые объекты
player = Player(player_img, 5, win_height - 80, 4)  # Игрок
monster1 = Enemy(cyborg_img, win_width - 80, 280, 2)  # Враг
final = GameSprite(treasure_img, win_width - 120, win_height - 80, 0)  # Сокровище

# Создаем списки игровых объектов
walls = create_walls(walls_list)  # Список стен
monsters = [monster1]  # Список врагов
finals = [final]  # Список целей

# Загружаем звуки игры
pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'jungles.ogg'))  # Загружаем фоновую музыку
kick = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'kick.ogg'))  # Загружаем звук поражения
money = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'money.ogg'))  # Загружаем звук победы
pygame.mixer.music.play(-1)  # Запускаем фоновую музыку в бесконечном цикле

# Создаем шрифт и текстовые сообщения
font = pygame.font.Font(None, 70)  # Шрифт размером 70
win_text = font.render('YOU WIN!', True, WIN)  # Текст победы
lose_text = font.render('YOU LOSE!', True, LOSE)  # Текст поражения

# Инициализируем игровые переменные
game_over = False  # Флаг завершения игры
clock = pygame.time.Clock()  # Создаем объект для управления временем
finish = False  # Флаг окончания раунда
FPS = 100  # Количество кадров в секунду

# Функция завершения игры
def end_game(end=None):
    global finish
    finish = True
    if end == win_text:
        # При победе проигрываем звук и выводим сообщение
        money.play()
        window.blit(win_text, (500, 500))
    elif end == lose_text:
        # При поражении проигрываем звук и выводим сообщение
        kick.play()
        window.blit(lose_text, (500, 500))

# Основной игровой цикл
while not game_over:
    # Обрабатываем события pygame
    for event in pygame.event.get():
        # Проверяем наличие события закрытия окна
        if event.type == pygame.QUIT:
            game_over = True
    
    # Если игра не закончена
    if not finish:
        # Отрисовываем фон
        window.blit(background, (0, 0))
        # Обновляем и отрисовываем игрока
        player.update()
        player.reset()

        # Отрисовываем все стены и проверяем столкновения с игроком
        for wall in walls:
            wall.draw_wall(window)
            if pygame.sprite.collide_rect(player, wall):
                end_game(lose_text)

        # Обновляем и отрисовываем всех врагов, проверяем столкновения
        for monster in monsters:
            monster.update()
            monster.reset()
            if pygame.sprite.collide_rect(player, monster):
                end_game(lose_text)

        # Отрисовываем все цели и проверяем достижение цели
        for final in finals:
            final.reset()
            if pygame.sprite.collide_rect(player, final):
                end_game(win_text)

    # Обновляем экран
    pygame.display.update()
    # Устанавливаем частоту обновления кадров
    clock.tick(FPS)

# Завершаем работу pygame
pygame.quit()