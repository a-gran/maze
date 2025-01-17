# Импортируем библиотеку pygame для создания игры
import pygame

'''Необходимые классы'''
# Определяем базовый класс для всех игровых спрайтов, наследующийся от pygame.sprite.Sprite
class GameSprite(pygame.sprite.Sprite):
    # Конструктор класса, принимающий параметры: изображение, координаты x и y, скорость
    def __init__(self, player_image, player_x, player_y, player_speed):
        # Вызываем конструктор родительского класса
        super().__init__()
 
        # Загружаем и масштабируем изображение спрайта до размера 65x65 пикселей
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        # Сохраняем скорость спрайта
        self.speed = player_speed
 
        # Создаем прямоугольник для определения границ спрайта
        self.rect = self.image.get_rect()
        # Устанавливаем начальные координаты спрайта
        self.rect.x = player_x
        self.rect.y = player_y

    # Метод для отрисовки спрайта на экране
    def reset(self):
        # Отображаем спрайт в заданной позиции
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока, наследующийся от GameSprite
class Player(GameSprite):
    # Метод обновления позиции игрока на основе нажатых клавиш
    def update(self):
        # Получаем список нажатых клавиш
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

# Класс врага, наследующийся от GameSprite
class Enemy(GameSprite):
    # Определение начального направления движения
    direction = 'left'
    
    # Метод обновления позиции врага
    def update(self):
        # Изменение направления при достижении левой границы
        if self.rect.x <= 470:
            self.direction = 'right'
        # Изменение направления при достижении правой границы
        if self.rect.x >= win_width - 85:
            self.direction = 'left'

        # Движение влево или вправо в зависимости от направления
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# Класс для создания препятствий (стен)
class Wall(pygame.sprite.Sprite):
    # Конструктор класса с параметрами цвета и размеров стены
    def __init__(self, color, wall_x, wall_y, wall_width, wall_height):
        # Инициализация родительского класса
        super().__init__()
        # Сохранение цвета стены
        self.color = color
        # Сохранение размеров стены
        self.width = wall_width
        self.height = wall_height
 
        # Создание поверхности стены заданного размера
        self.image = pygame.Surface((self.width, self.height))
        # Заполнение поверхности цветом
        self.image.fill(color)
 
        # Создание прямоугольника для коллизий
        self.rect = self.image.get_rect()
        # Установка позиции стены
        self.rect.x = wall_x
        self.rect.y = wall_y
 
    # Метод отрисовки стены
    def draw_wall(self):
        # Отрисовка поверхности стены
        window.blit(self.image, (self.rect.x, self.rect.y))
        # Отрисовка контура стены
        pygame.draw.rect(window, self.color, (self.rect.x, self.rect.y, self.width, self.height))

# Определение константы цвета стен
WALL_COLOR = (255, 255, 255)
WIN = (255, 215, 0)
LOSE = (180, 0, 0)
# Установка размеров игрового окна
win_width = 1000
win_height = 1000
# Создание игрового окна заданного размера
window = pygame.display.set_mode((win_width, win_height))
# Установка заголовка окна
pygame.display.set_caption('Лабиринт')
# Загрузка и масштабирование фонового изображения
background = pygame.transform.scale(pygame.image.load('background1.jpg'), (win_width, win_height))

# Создание игровых объектов с начальными параметрами
player = Player('hero.png', 5, win_height - 80, 4)
monster1 = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

monsters = [monster1]
finals = [final]

# Создание стен игрового лабиринта
w1 = Wall(WALL_COLOR, 100, 20, 450, 10)
w2 = Wall(WALL_COLOR, 100, 480, 350, 10)
w3 = Wall(WALL_COLOR, 100, 20, 10, 380)

# Создание списка всех стен для удобства обработки
walls = [w1, w2, w3]

# Инициализация игровых флагов и настроек
game_over = False  # Флаг завершения игры
clock = pygame.time.Clock()  # Объект для управления временем
finish = False  # Флаг завершения уровня
FPS = 100  # Частота обновления экрана

# Инициализация системы шрифтов
pygame.font.init()
# Создание шрифта заданного размера
font = pygame.font.Font(None, 70)
# Создание текстовых сообщений для победы и поражения
win = font.render('YOU WIN!', True, WIN)
lose = font.render('YOU LOSE!', True, LOSE)

# Инициализация звуковой системы
pygame.mixer.init()
# Загрузка и воспроизведение фоновой музыки
pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play()
# Загрузка звуковых эффектов
money = pygame.mixer.Sound('money.ogg')
kick = pygame.mixer.Sound('kick.ogg')

# Функция завершения игры
def end_game(end=None):
    global finish
    # Установка флага завершения
    finish = True
    # Обработка победы
    if end == win:
        money.play()
        window.blit(win, (500, 500))        
    # Обработка поражения
    elif end == lose:
        kick.play()
        window.blit(lose, (500, 500))

# Основной игровой цикл
while not game_over:
    # Обработка событий pygame
    for event in pygame.event.get():
        # Проверка события закрытия окна
        if event.type == pygame.QUIT:
            game_over = True
    
    # Проверка состояния игры
    if finish != True:
        # Отрисовка фона
        window.blit(background,(0, 0))
        # Обновление позиции игрока и его отрисовка
        player.update()        
        player.reset()            

        # Проверка столкновений со стенами и монстром
        for wall in walls:
            wall.draw_wall()
            if pygame.sprite.collide_rect(player, wall):
                end_game(lose)

        # Проверка столкновений с монстрами
        for monster in monsters:
            monster.update()
            monster.reset()                        
            if pygame.sprite.collide_rect(player, monster):
                end_game(lose)

        # Проверка достижения цели
        for final in finals:
            final.reset()
            if pygame.sprite.collide_rect(player, final):
                end_game(win)

    # Обновление экрана
    pygame.display.update()
    # Установка частоты обновления
    clock.tick(FPS)