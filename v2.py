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
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока, наследующийся от GameSprite
class Player(GameSprite):
    # Метод обновления позиции игрока на основе нажатых клавиш
    def update(self):
        # Получаем список нажатых клавиш
        keys = pygame.key.get_pressed()
        # Проверяем нажатие стрелок и перемещаем игрока с учетом границ окна
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Класс врага, наследующийся от GameSprite
class Enemy(GameSprite):
    # Начальное направление движения врага
    direction = "left"
    # Метод обновления позиции врага
    def update(self):
        # Меняем направление движения при достижении границ
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        # Перемещаем врага в соответствии с текущим направлением
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# Определяем размеры игрового окна
win_width = 1000
win_height = 1000
# Создаем игровое окно заданного размера
window = pygame.display.set_mode((win_width, win_height))
# Устанавливаем заголовок окна
pygame.display.set_caption("Maze")
# Загружаем и масштабируем фоновое изображение
background = pygame.transform.scale(pygame.image.load("background1.jpg"), (win_width, win_height))

# Создаем игровые объекты: игрока, врага и цель
player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

# Флаг для завершения игры
game_over = False
# Создаем объект для управления временем
clock = pygame.time.Clock()
# Флаг для обозначения завершения уровня
finish = False
# Устанавливаем количество кадров в секунду
FPS = 100

# Инициализируем звуковую подсистему pygame
pygame.mixer.init()
# Загружаем музыкальный файл
pygame.mixer.music.load('jungles.ogg')
# Запускаем воспроизведение музыки
pygame.mixer.music.play()

# Основной игровой цикл
while not game_over:
    # Обрабатываем события pygame
    for e in pygame.event.get():
        # Если пользователь закрыл окно, завершаем игру
        if e.type == pygame.QUIT:
            game_over = True
    
    # Если уровень не завершен
    if finish != True:
        # Отрисовываем фон
        window.blit(background,(0, 0))
        # Обновляем позиции игрока и врага
        player.update()
        monster.update()        
        # Отрисовываем игровые объекты
        player.reset()
        monster.reset()
        final.reset() 

    # Обновляем экран
    pygame.display.update()
    # Устанавливаем задержку для поддержания заданного FPS
    clock.tick(FPS)