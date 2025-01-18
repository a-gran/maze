# Импортируем pygame для создания игры и os для работы с путями к файлам
from game_sprite import GameSprite
import pygame
import random
import os
import time

# Инициализируем все модули pygame
pygame.init()

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
        # Сохраняем начальные координаты для респауна
        self.start_x = player_x
        self.start_y = player_y

    # Метод для отрисовки спрайта на экране
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # Метод для возврата на начальную позицию
    def respawn(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y

# Класс игрока, наследуется от GameSprite
class Player(GameSprite):
    def __init__(self, image, player_x, player_y, player_speed):
        super().__init__(image, player_x, player_y, player_speed)
        self.lives = 3  # Добавляем количество жизней

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

    def lose_life(self):
        # Уменьшаем количество жизней и возвращаем игрока на старт
        self.lives -= 1
        self.respawn()
        return self.lives <= 0  # Возвращаем True если жизни закончились

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

# Класс стены с расширенными возможностями
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

class SpecialWall(Wall):
    def __init__(self, thickness, color, wall_x, wall_y, length, is_vertical, 
                 wall_type=None, name=None, is_transparent=False, is_deadly=False,
                 is_moving_vertical=False, is_moving_horizontal=False):
        super().__init__(thickness, color, wall_x, wall_y, length, is_vertical, wall_type, name)
        
        # Специальные свойства стены
        self.is_transparent = is_transparent  # Прозрачная стена
        self.is_deadly = is_deadly  # Смертельная стена
        self.is_moving_vertical = is_moving_vertical  # Движение вверх-вниз
        self.is_moving_horizontal = is_moving_horizontal  # Движение влево-вправо
        
        # Параметры движения
        self.initial_x = wall_x
        self.initial_y = wall_y
        self.move_direction = 1  # 1 или -1 для определения направления движения
        self.move_distance = 50  # Расстояние движения в пикселях
        self.move_speed = 2  # Скорость движения
        
        # Параметры прозрачности
        self.transparency_timer = time.time()  # Время последнего изменения прозрачности
        self.transparency_interval = 3.0  # Интервал изменения прозрачности (в секундах)
        self.is_currently_transparent = is_transparent  # Текущее состояние прозрачности
        
        # Если стена прозрачная, делаем её полупрозрачной
        if self.is_transparent:
            self.image = self.image.convert_alpha()
            self.update_transparency()

    def update_transparency(self):
        """Обновление прозрачности стены"""
        current_time = time.time()
        if current_time - self.transparency_timer >= self.transparency_interval:
            self.transparency_timer = current_time
            self.is_currently_transparent = not self.is_currently_transparent
            
            if self.is_currently_transparent:
                transparent_color = list(self.color)
                transparent_color.append(128)  # Полупрозрачность
                self.image.fill(transparent_color)
            else:
                self.image.fill(self.color + (255,))  # Полная непрозрачность

    def update(self):
        """Обновление позиции движущейся стены"""
        if self.is_moving_vertical:
            # Движение вверх-вниз
            self.rect.y += self.move_speed * self.move_direction
            
            # Проверка достижения границ движения
            if abs(self.rect.y - self.initial_y) >= self.move_distance:
                self.move_direction *= -1  # Меняем направление
                
        elif self.is_moving_horizontal:
            # Движение влево-вправо
            self.rect.x += self.move_speed * self.move_direction
            
            # Проверка достижения границ движения
            if abs(self.rect.x - self.initial_x) >= self.move_distance:
                self.move_direction *= -1  # Меняем направление

        # Обновляем прозрачность для прозрачных стен
        if self.is_transparent:
            self.update_transparency()

    def check_collision(self, sprite):
        """Проверка столкновений с учетом специальных свойств стены"""
        if not pygame.sprite.collide_rect(self, sprite):
            return False, False
            
        # Если стена прозрачная и в данный момент прозрачна
        if self.is_transparent and self.is_currently_transparent:
            return False, False
            
        # Если стена смертельная
        if self.is_deadly:
            return True, True
            
        # Если стена движущаяся, сдвигаем спрайт
        if self.is_moving_horizontal:
            sprite.rect.x += self.move_speed * self.move_direction
        elif self.is_moving_vertical:
            sprite.rect.y += self.move_speed * self.move_direction
            
        # Обычная коллизия
        return True, False

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
    [20, WALL_WHITE, 200, 40, 600, True, 'barricada', 'левая стена'],
    [40, WALL_BLACK, 200, 800, 500, False, 'barricada', 'правая нижняя горизонтальная стена']
]

# Функция для создания специальных стен аналогично обычным стенам
def create_special_walls(special_walls_list):
    special_wall_objects = []
    for wall_params in special_walls_list:
        wall = SpecialWall(
            thickness=wall_params[0],      # Толщина
            color=wall_params[1],          # Цвет
            wall_x=wall_params[2],         # Позиция X
            wall_y=wall_params[3],         # Позиция Y
            length=wall_params[4],         # Длина
            is_vertical=wall_params[5],    # Ориентация
            wall_type=wall_params[6],      # Тип стены
            name=wall_params[7],           # Название
            is_transparent=wall_params[8],  # Прозрачность
            is_deadly=wall_params[9],      # Смертельность
            is_moving_vertical=wall_params[10],    # Движение вверх-вниз
            is_moving_horizontal=wall_params[11]   # Движение влево-вправо
        )
        special_wall_objects.append(wall)
    return special_wall_objects

# Список параметров для создания специальных стен
special_walls_list = [
    # [толщина, цвет, x, y, длина, верт?, тип, имя, прозрачность, смертельность, движ.верт, движ.гор]
    [20, WALL_BLUE, 300, 200, 100, True, 'moving_vertical', 'движущаяся вертикальная стена', 
     False, False, True, False],
    
    [20, WALL_RED, 500, 300, 200, False, 'moving_horizontal', 'движущаяся горизонтальная стена',
     False, False, False, True],
    
    [20, WALL_GREEN, 700, 400, 150, True, 'transparent', 'прозрачная стена',
     True, False, False, False],
    
    [20, WALL_RED, 0, 500, 100, False, 'deadly', 'смертельная стена',
     False, True, False, False]
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
monster2 = Enemy(cyborg_img, win_width - 80, 680, 2)  # Враг
final = GameSprite(treasure_img, win_width - 120, win_height - 80, 0)  # Сокровище

# Создаем списки игровых объектов
walls = create_walls(walls_list)  # Список стен
special_walls = create_special_walls(special_walls_list)  # Список специальных стен
monsters = [monster1, monster2]  # Список врагов
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

# Создаем шрифт для отображения жизней
lives_font = pygame.font.Font(None, 36)

# Функция для отображения количества оставшихся жизней
def draw_lives(lives):
    lives_text = lives_font.render(f'Lives: {lives}', True, WALL_WHITE)
    window.blit(lives_text, (10, 10))

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

# Инициализируем игровые переменные
game_over = False  # Флаг завершения игры
clock = pygame.time.Clock()  # Создаем объект для управления временем
finish = False  # Флаг окончания раунда
FPS = 100  # Количество кадров в секунду

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
        
        # Отображаем количество оставшихся жизней
        draw_lives(player.lives)
        
        # Обновляем и отрисовываем игрока
        player.update()
        player.reset()

        # Отрисовываем все обычные стены и проверяем столкновения с игроком
        for wall in walls:
            wall.draw_wall(window)
            if pygame.sprite.collide_rect(player, wall):
                # При столкновении с обычной стеной просто откатываем позицию
                if player.rect.y < wall.rect.y + wall.rect.height and player.rect.y + player.rect.height > wall.rect.y:
                    if player.rect.x < wall.rect.x:
                        player.rect.right = wall.rect.left
                    else:
                        player.rect.left = wall.rect.right
                else:
                    if player.rect.y < wall.rect.y:
                        player.rect.bottom = wall.rect.top
                    else:
                        player.rect.top = wall.rect.bottom

        # Обновляем и проверяем специальные стены
        for special_wall in special_walls:
            special_wall.update()
            special_wall.draw_wall(window)
            collision, is_deadly = special_wall.check_collision(player)
            
            if collision:
                if is_deadly:
                    # Если стена смертельная, отнимаем жизнь
                    if player.lose_life():
                        end_game(lose_text)
                    else:
                        kick.play()  # Проигрываем звук потери жизни

        # Обновляем и отрисовываем всех врагов, проверяем столкновения
        for monster in monsters:
            monster.update()
            monster.reset()
            
            # Проверяем столкновения врагов со специальными стенами
            for special_wall in special_walls:
                collision, _ = special_wall.check_collision(monster)
            
            if pygame.sprite.collide_rect(player, monster):
                if player.lose_life():
                    end_game(lose_text)
                else:
                    kick.play()

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