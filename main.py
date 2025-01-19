import pygame
import os
from paths import *
from level_editor.data_walls import *
from sprites import GameSprite
from player import Player
from enemy import Enemy
from walls import Wall, SpecialWall
from utils import create_walls, create_special_walls, draw_lives, end_game

# Размеры окна
WIN_WIDTH = 1000
WIN_HEIGHT = 1000
FPS = 100

def main():
    pygame.init()

    # Создание директорий
    required_dirs = [ASSETS_DIR, IMAGES_DIR, SPRITES_DIR, BACKGROUNDS_DIR, 
                    ENEMIES_DIR, MUSIC_DIR, SOUNDS_DIR]
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Создана директория: {directory}")

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Лабиринт')

    player_img = pygame.image.load(os.path.join(SPRITES_DIR, 'hero.png'))
    cyborg_img = pygame.image.load(os.path.join(ENEMIES_DIR, 'cyborg.png'))
    treasure_img = pygame.image.load(os.path.join(SPRITES_DIR, 'treasure.png'))
    background = pygame.transform.scale(
        pygame.image.load(os.path.join(BACKGROUNDS_DIR, 'background1.jpg')), 
        (WIN_WIDTH, WIN_HEIGHT)
    )

    # Создание игровых объектов с передачей необходимых параметров
    player = Player(player_img, 5, WIN_HEIGHT - 80, 4, WIN_WIDTH, WIN_HEIGHT)
    monster1 = Enemy(cyborg_img, WIN_WIDTH - 80, 280, 2, WIN_WIDTH)
    monster2 = Enemy(cyborg_img, WIN_WIDTH - 80, 680, 2, WIN_WIDTH)
    final = GameSprite(treasure_img, WIN_WIDTH - 120, WIN_HEIGHT - 80, 0)

    # Создание стен с передачей классов
    walls = create_walls(walls_list, Wall)
    special_walls = create_special_walls(special_walls_list, SpecialWall)
    monsters = [monster1, monster2]
    finals = [final]

    pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'jungles.ogg'))
    kick = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'kick.ogg'))
    money = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'money.ogg'))
    pygame.mixer.music.play(-1)

    font = pygame.font.Font(None, 70)
    lives_font = pygame.font.Font(None, 36)

    game_over = False
    clock = pygame.time.Clock()
    finish = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        
        if not finish:
            window.blit(background, (0, 0))
            draw_lives(window, player.lives, lives_font, WALL_WHITE)
            
            player.update()
            player.reset(window)

            for wall in walls:
                wall.draw_wall(window)
                if pygame.sprite.collide_rect(player, wall):
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

            for special_wall in special_walls:
                special_wall.update()
                special_wall.draw_wall(window)
                collision, is_deadly = special_wall.check_collision(player)
                
                if collision:
                    if is_deadly:
                        if player.lose_life():
                            finish = end_game(window, finish, 'lose', font, WIN_COLOR, LOSE_COLOR, 
                                           kick_sound=kick)
                        else:
                            kick.play()

            for monster in monsters:
                monster.update(walls)
                monster.reset(window)
                
                for special_wall in special_walls:
                    collision, _ = special_wall.check_collision(monster)
                
                if pygame.sprite.collide_rect(player, monster):
                    if player.lose_life():
                        finish = end_game(window, finish, 'lose', font, WIN_COLOR, LOSE_COLOR, 
                                       kick_sound=kick)
                    else:
                        kick.play()

            for final in finals:
                final.reset(window)
                if pygame.sprite.collide_rect(player, final):
                    finish = end_game(window, finish, 'win', font, WIN_COLOR, LOSE_COLOR, 
                                   money_sound=money)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()