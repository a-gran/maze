import pygame
'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(pygame.sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Игровая сцена:
win_width = 1000
win_height = 1000
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Maze')
background = pygame.transform.scale(pygame.image.load('background1.jpg'), (win_width, win_height))

#Персонажи игры:
player = GameSprite('hero.png', 5, win_height - 80, 4)
monster = GameSprite('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

game_over = False
clock = pygame.time.Clock()
FPS = 100

#музыка
pygame.mixer.init()
pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    
    window.blit(background,(0, 0))
    player.reset()
    monster.reset()
    final.reset()

    pygame.display.update()
    clock.tick(FPS)