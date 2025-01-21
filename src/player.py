import pygame
from src.sprites import GameSprite

class Player(GameSprite):
    def __init__(self, image, player_x, player_y, player_speed, win_width, win_height):
        super().__init__(image, player_x, player_y, player_speed)
        self.lives = 3
        self.win_width = win_width
        self.win_height = win_height
        self.safety_margin = 3

    def get_wall_next_position(self, wall):
        """Вычисляет следующую позицию движущейся стены"""
        next_x = wall.rect.x
        next_y = wall.rect.y
        
        if wall.is_moving_horizontal:
            next_x += wall.move_speed * wall.move_direction
        if wall.is_moving_vertical:
            next_y += wall.move_speed * wall.move_direction
            
        return next_x, next_y
        # 

    def check_edge_collision(self, wall, next_x, next_y):
        """Проверяет столкновение с узкими сторонами стены с учётом её движения"""
        next_rect = pygame.Rect(next_x, next_y, self.rect.width, self.rect.height)
        
        # Получаем следующую позицию стены
        wall_next_x, wall_next_y = self.get_wall_next_position(wall)
        
        if wall.is_moving_vertical:
            # Расширенные зоны для верхней и нижней границ с учётом движения стены
            margin = self.safety_margin + abs(wall.move_speed)  # Увеличиваем отступ на скорость движения
            top_edge = pygame.Rect(
                wall_next_x - margin,
                wall_next_y - margin,
                wall.rect.width + (margin * 2),
                margin * 2
            )
            bottom_edge = pygame.Rect(
                wall_next_x - margin,
                wall_next_y + wall.rect.height - margin,
                wall.rect.width + (margin * 2),
                margin * 2
            )
            
            # Проверяем пересечение с расширенными зонами
            if next_rect.colliderect(top_edge) or next_rect.colliderect(bottom_edge):
                return True
                
        elif wall.is_moving_horizontal:
            # Расширенные зоны для левой и правой границ с учётом движения стены
            margin = self.safety_margin + abs(wall.move_speed)
            left_edge = pygame.Rect(
                wall_next_x - margin,
                wall_next_y - margin,
                margin * 2,
                wall.rect.height + (margin * 2)
            )
            right_edge = pygame.Rect(
                wall_next_x + wall.rect.width - margin,
                wall_next_y - margin,
                margin * 2,
                wall.rect.height + (margin * 2)
            )
            
            # Проверяем пересечение с расширенными зонами
            if next_rect.colliderect(left_edge) or next_rect.colliderect(right_edge):
                return True
                
        return False

    def update(self, walls=None, special_walls=None):
        previous_x = self.rect.x
        previous_y = self.rect.y

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] and self.rect.x > 2:
            dx = -self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < self.win_width - 50:
            dx = self.speed
        if keys[pygame.K_UP] and self.rect.y > 2:
            dy = -self.speed
        if keys[pygame.K_DOWN] and self.rect.y < self.win_height - 50:
            dy = self.speed

        if special_walls and (dx != 0 or dy != 0):
            for wall in special_walls:
                if not (wall.is_transparent and wall.is_currently_transparent):
                    if wall.is_moving_horizontal or wall.is_moving_vertical:
                        # Проверяем с учётом следующего положения стены
                        if self.check_edge_collision(wall, self.rect.x + dx, self.rect.y + dy):
                            return  # Отменяем движение если есть риск столкновения с узкой стороной

        # Применяем движение по горизонтали
        if dx != 0:
            self.rect.x += dx
            collision = False
            
            if walls:
                for wall in walls:
                    if pygame.sprite.collide_rect(self, wall):
                        collision = True
                        break

            if not collision and special_walls:
                for wall in special_walls:
                    if pygame.sprite.collide_rect(self, wall):
                        if wall.is_transparent and wall.is_currently_transparent:
                            continue
                        collision = True
                        break

            if collision:
                self.rect.x = previous_x

        # Применяем движение по вертикали
        if dy != 0:
            self.rect.y += dy
            collision = False
            
            if walls:
                for wall in walls:
                    if pygame.sprite.collide_rect(self, wall):
                        collision = True
                        break

            if not collision and special_walls:
                for wall in special_walls:
                    if pygame.sprite.collide_rect(self, wall):
                        if wall.is_transparent and wall.is_currently_transparent:
                            continue
                        collision = True
                        break

            if collision:
                self.rect.y = previous_y

    def lose_life(self):
        self.lives -= 1
        self.respawn()
        return self.lives <= 0