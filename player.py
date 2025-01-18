from sprites import GameSprite
import pygame

class Player(GameSprite):
    def __init__(self, image, player_x, player_y, player_speed, win_width, win_height):
        super().__init__(image, player_x, player_y, player_speed)
        self.lives = 3
        self.win_width = win_width
        self.win_height = win_height

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.rect.x > 2:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < self.win_width - 50:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 2:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < self.win_height - 50:
            self.rect.y += self.speed

    def lose_life(self):
        self.lives -= 1
        self.respawn()
        return self.lives <= 0