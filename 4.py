# Импортируем библиотеку pygame, которая предоставляет функционал для создания игр
import pygame

# Базовый класс для всех игровых объектов (спрайтов)
class GameSprite(pygame.sprite.Sprite):
    # Конструктор класса, инициализирует основные свойства спрайта
    def __init__(self, player_image, player_x, player_y, player_speed):
        # Вызываем конструктор родительского класса Sprite
        super().__init__()
 
        # Загружаем изображение и масштабируем его до размера 65x65 пикселей
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        # Сохраняем скорость движения спрайта
        self.speed = player_speed
 
        # Создаем прямоугольник для определения границ спрайта
        self.rect = self.image.get_rect()
        # Устанавливаем начальные координаты спрайта
        self.rect.x = player_x
        self.rect.y = player_y

    # Метод для отрисовки спрайта на экране
    def reset(self):
        # Отрисовываем изображение спрайта в его текущей позиции
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока, наследуется от GameSprite
class Player(GameSprite):
    # Метод обновления позиции игрока
    def update(self):
        # Получаем словарь всех нажатых клавиш
        keys = pygame.key.get_pressed()
        # Если нажата левая стрелка и игрок не у левой границы
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        # Если нажата правая стрелка и игрок не у правой границы
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        # Если нажата стрелка вверх и игрок не у верхней границы
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        # Если нажата стрелка вниз и игрок не у нижней границы
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Класс врага с улучшенной системой столкновений
class Enemy(GameSprite):
    # Начальное направление движения врага
    direction = 'left'
    
    # Метод обновления позиции врага
    def update(self):
        # Сохраняем текущую позицию для возможного отката
        previous_x = self.rect.x
        
        # Двигаем врага в текущем направлении
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
        # Проверяем столкновения со стенами
        collision_occurred = False
        for wall in walls:  # walls должен быть доступен как глобальная переменная
            if pygame.sprite.collide_rect(self, wall):
                collision_occurred = True
                break
                
        # Если произошло столкновение со стеной
        if collision_occurred:
            # Возвращаемся на предыдущую позицию
            self.rect.x = previous_x
            # Меняем направление на противоположное
            self.direction = 'right' if self.direction == 'left' else 'left' # тернарный оператор
        # Если нет столкновения, проверяем границы экрана
        else:
            # Если враг достиг левой границы, меняем направление на правое
            if self.rect.x <= 50:
                self.direction = 'right'
            # Если враг достиг правой границы, меняем направление на левое
            if self.rect.x >= win_width - 50:
                self.direction = 'left'

# Класс стены
class Wall(pygame.sprite.Sprite):
    # Конструктор класса стены
    def __init__(self, thickness, color, start_x, start_y, length, is_vertical, type_wall=None, name=None):
        # Вызываем конструктор родительского класса
        super().__init__()
        
        # Сохраняем все параметры стены как атрибуты класса
        self.thickness = thickness  # Толщина стены
        self.color = color         # Цвет стены
        self.start_x = start_x     # Начальная X-координата
        self.start_y = start_y     # Начальная Y-координата
        self.is_vertical = is_vertical  # Ориентация стены (вертикальная/горизонтальная)
        self.length = length       # Длина стены
        self.type_wall = type_wall  # Название стены
        self.name = name           # Название стены
        
        # Определяем размеры стены в зависимости от ориентации
        if is_vertical:
            self.width = thickness   # Для вертикальной стены ширина равна толщине
            self.height = length     # А высота равна длине
        else:
            self.width = length      # Для горизонтальной стены ширина равна длине
            self.height = thickness  # А высота равна толщине
            
        # Создаём поверхность для отрисовки стены
        self.image = pygame.Surface((self.width, self.height))
        # Закрашиваем поверхность заданным цветом
        self.image.fill(color)
        
        # Создаём прямоугольник для определения границ стены
        self.rect = self.image.get_rect()
        # Устанавливаем позицию стены
        self.rect.x = start_x
        self.rect.y = start_y
    
    # Метод для отрисовки стены
    def draw_wall(self, window):
        # Отрисовываем стену на указанной поверхности
        window.blit(self.image, (self.rect.x, self.rect.y))

# Создание стен лабиринта
def create_walls(walls_list):
    """
    Создает список объектов стен на основе параметров из входного списка.
    
    Args:
        walls_list (list): Список параметров стен в формате
            [thickness, color, start_x, start_y, is_vertical, length, name, description]
    
    Returns:
        list: Список объектов класса Wall
    """
    # Создаем пустой список для хранения объектов стен
    wall_objects = []
    
    # Перебираем все элементы из списка параметров стен
    for wall_params in walls_list:
        # Создаем новый объект стены с соответствующими параметрами
        wall = Wall(
            thickness=wall_params[0],    # Толщина стены
            color=wall_params[1],        # Цвет стены
            start_x=wall_params[2],      # Начальная X-координата
            start_y=wall_params[3],      # Начальная Y-координата            
            length=wall_params[4],       # Длина стены
            is_vertical=wall_params[5],  # Ориентация стены
            type_wall=wall_params[6],    # Описание стены
            name=wall_params[7]          # Название стены (если есть)
        )
        # Добавляем созданную стену в список
        wall_objects.append(wall)
    
    return wall_objects

# Цвета стен
WALL_WHITE = (255, 255, 255)
WALL_RED = (255, 0, 0)
WALL_GREEN = (0, 255, 0)
WALL_BLUE = (0, 0, 255)
WALL_BLACK = (0, 0, 0)

walls_list = [
    [10, WALL_WHITE, 200, 40, 600, True, 'barricada','левая стена'],
    [10, WALL_RED, 700, 40, 600, False, 'barricada','левая стена'],
    [20, WALL_GREEN, 800, 40, 200, True, 'barricada','верхняя стена'],
    [10, WALL_BLUE, 400, 40, 600, True, 'barricada','левая стена'],
    [40, WALL_WHITE, 50, 400, 600, False, 'barricada','правая стена']
] 

# Создаем глобальную переменную для хранения объектов стен
walls = create_walls(walls_list)

# Определяем константы цветов
WIN = (255, 215, 0)          # Золотой цвет для сообщения о победе
LOSE = (180, 0, 0)          # Красный цвет для сообщения о поражении

# Задаём размеры игрового окна
win_width = 1000   # Ширина окна
win_height = 1000  # Высота окна

# Создаём игровое окно заданного размера
window = pygame.display.set_mode((win_width, win_height))
# Устанавливаем заголовок окна
pygame.display.set_caption('Лабиринт')

# Загружаем и масштабируем фоновое изображение
background = pygame.transform.scale(pygame.image.load('background1.jpg'), (win_width, win_height))

# Создаём игровые объекты
player = Player('hero.png', 5, win_height - 80, 4)  # Игрок
monster1 = Enemy('cyborg.png', win_width - 80, 280, 2)  # Враг
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)  # Цель

# Создаём списки игровых объектов
monsters = [monster1]  # Список врагов
finals = [final]       # Список целей

# Инициализируем игровые флаги и настройки
game_over = False  # Флаг завершения игры
clock = pygame.time.Clock()  # Объект для управления временем
finish = False  # Флаг завершения уровня
FPS = 100  # Количество кадров в секунду

# Инициализируем систему шрифтов pygame
pygame.font.init()
# Создаём шрифт размером 70 пикселей
font = pygame.font.Font(None, 70)
# Создаём текстовые сообщения
win = font.render('YOU WIN!', True, WIN)   # Сообщение о победе
lose = font.render('YOU LOSE!', True, LOSE) # Сообщение о поражении

# Инициализируем звуковую систему pygame
pygame.mixer.init()
# Загружаем и запускаем фоновую музыку
pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play()
# Загружаем звуковые эффекты
money = pygame.mixer.Sound('money.ogg')  # Звук для победы
kick = pygame.mixer.Sound('kick.ogg')   # Звук для поражения

# Функция завершения игры
def end_game(end=None):
    global finish  # Используем глобальную переменную finish
    # Устанавливаем флаг завершения
    finish = True
    # Если передано сообщение о победе
    if end == win:
        money.play()  # Проигрываем звук победы
        window.blit(win, (500, 500))  # Отображаем сообщение о победе        
    # Если передано сообщение о поражении
    elif end == lose:
        kick.play()  # Проигрываем звук поражения
        window.blit(lose, (500, 500))  # Отображаем сообщение о поражении

# Основной игровой цикл
while not game_over:
    # Обрабатываем все события pygame
    for event in pygame.event.get():
        # Если пользователь закрыл окно
        if event.type == pygame.QUIT:
            game_over = True  # Завершаем игру
    
    # Если игра не завершена
    if finish != True:
        # Отрисовываем фон
        window.blit(background,(0, 0))
        # Обновляем позицию игрока и отрисовываем его
        player.update()        
        player.reset()           

        # Обрабатываем все стены
        for wall in walls:
            wall.draw_wall(window)  # Отрисовываем стену
            # Проверяем столкновение игрока со стеной
            if pygame.sprite.collide_rect(player, wall):
                end_game(lose)  # Завершаем игру поражением

        # Обрабатываем всех врагов
        for monster in monsters:
            monster.update()  # Обновляем позицию врага
            monster.reset()   # Отрисовываем врага
            # Проверяем столкновение игрока с врагом
            if pygame.sprite.collide_rect(player, monster):
                end_game(lose)  # Завершаем игру поражением

        # Обрабатываем все цели
        for final in finals:
            final.reset()  # Отрисовываем цель
            # Проверяем достижение игроком цели
            if pygame.sprite.collide_rect(player, final):
                end_game(win)  # Завершаем игру победой

    # Обновляем экран
    pygame.display.update()
    # Устанавливаем частоту обновления
    clock.tick(FPS)