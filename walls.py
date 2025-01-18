import pygame
import time
from consts import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, thickness, color, wall_x, wall_y, length, is_vertical, type_wall=None, name=None):
        super().__init__()
        self.thickness = thickness
        self.color = color
        self.wall_x = wall_x
        self.wall_y = wall_y
        self.is_vertical = is_vertical
        self.length = length
        self.type_wall = type_wall
        self.name = name
        
        if is_vertical:
            self.width = thickness
            self.height = length
        else:
            self.width = length
            self.height = thickness
            
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def draw_wall(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class SpecialWall(Wall):
    def __init__(self, thickness, color, wall_x, wall_y, length, is_vertical, 
                 wall_type=None, name=None, is_transparent=False, is_deadly=False,
                 is_moving_vertical=False, is_moving_horizontal=False):
        super().__init__(thickness, color, wall_x, wall_y, length, is_vertical, wall_type, name)
        
        self.is_transparent = is_transparent
        self.is_deadly = is_deadly
        self.is_moving_vertical = is_moving_vertical
        self.is_moving_horizontal = is_moving_horizontal
        
        self.initial_x = wall_x
        self.initial_y = wall_y
        self.move_direction = 1
        self.move_distance = 50
        self.move_speed = 2
        
        self.transparency_timer = time.time()
        self.transparency_interval = 3.0
        self.is_currently_transparent = is_transparent
        
        if self.is_transparent:
            self.image = self.image.convert_alpha()
            self.update_transparency()

    def update_transparency(self):
        current_time = time.time()
        if current_time - self.transparency_timer >= self.transparency_interval:
            self.transparency_timer = current_time
            self.is_currently_transparent = not self.is_currently_transparent
            
            if self.is_currently_transparent:
                transparent_color = list(self.color)
                transparent_color.append(128)
                self.image.fill(transparent_color)
            else:
                self.image.fill(self.color + (255,))

    def update(self):
        if self.is_moving_vertical:
            self.rect.y += self.move_speed * self.move_direction
            if abs(self.rect.y - self.initial_y) >= self.move_distance:
                self.move_direction *= -1
                
        elif self.is_moving_horizontal:
            self.rect.x += self.move_speed * self.move_direction
            if abs(self.rect.x - self.initial_x) >= self.move_distance:
                self.move_direction *= -1

        if self.is_transparent:
            self.update_transparency()

    def check_collision(self, sprite):
        if not pygame.sprite.collide_rect(self, sprite):
            return False, False
            
        if self.is_transparent and self.is_currently_transparent:
            return False, False
            
        if self.is_deadly:
            return True, True
            
        if self.is_moving_horizontal:
            sprite.rect.x += self.move_speed * self.move_direction
        elif self.is_moving_vertical:
            sprite.rect.y += self.move_speed * self.move_direction
            
        return True, False