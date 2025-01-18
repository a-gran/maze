from sprites import GameSprite
import pygame

class Enemy(GameSprite):
    def __init__(self, image, player_x, player_y, player_speed, win_width):
        super().__init__(image, player_x, player_y, player_speed)
        self.direction = 'left'
        self.win_width = win_width
    
    def update(self, walls):  # Добавляем параметр walls
        previous_x = self.rect.x
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
        collision_occurred = False
        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                collision_occurred = True
                break
        
        if collision_occurred:
            self.rect.x = previous_x
            self.direction = 'right' if self.direction == 'left' else 'left'
        else:
            if self.rect.x <= 50:
                self.direction = 'right'
            if self.rect.x >= self.win_width - 50:
                self.direction = 'left'