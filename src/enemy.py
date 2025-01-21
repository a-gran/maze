from .sprites import GameSprite
import pygame

class Enemy(GameSprite):
    def __init__(self, image, player_x, player_y, player_speed, win_width):
        super().__init__(image, player_x, player_y, player_speed)
        self.direction = 'left'
        self.win_width = win_width
        self.safety_margin = 3  # Дополнительный запас для предотвращения столкновений

    def will_collide_with_moving_wall(self, wall, next_x):
        """
        Проверяет, произойдет ли столкновение с движущейся стеной на следующем шаге
        
        Args:
            wall: Движущаяся стена
            next_x: Следующая позиция врага по X
        
        Returns:
            bool: True если будет столкновение
        """
        # Создаем расширенный прямоугольник для проверки
        test_rect = pygame.Rect(
            next_x - self.safety_margin,
            self.rect.y - self.safety_margin,
            self.rect.width + self.safety_margin * 2,
            self.rect.height + self.safety_margin * 2
        )
        
        # Рассчитываем следующую позицию стены
        wall_next_x = wall.rect.x + (wall.move_speed * wall.move_direction if wall.is_moving_horizontal else 0)
        wall_next_y = wall.rect.y + (wall.move_speed * wall.move_direction if wall.is_moving_vertical else 0)
        wall_rect = pygame.Rect(wall_next_x, wall_next_y, wall.rect.width, wall.rect.height)
        
        # Проверяем пересечение с расширенным прямоугольником
        return test_rect.colliderect(wall_rect)

    def update(self, walls, special_walls=None):
        # Сохраняем текущую позицию
        previous_x = self.rect.x
        
        # Определяем следующую позицию
        next_x = self.rect.x - self.speed if self.direction == 'left' else self.rect.x + self.speed
        
        # Проверяем столкновения с движущимися стенами
        will_collide = False
        if special_walls:
            for wall in special_walls:
                if (wall.is_moving_horizontal or wall.is_moving_vertical) and not wall.is_transparent:
                    if self.will_collide_with_moving_wall(wall, next_x):
                        will_collide = True
                        break
        
        # Если столкновение не предвидится, двигаемся
        if not will_collide:
            if self.direction == 'left':
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            
            # Проверяем коллизии с обычными стенами
            collision = False
            for wall in walls:
                if pygame.sprite.collide_rect(self, wall):
                    collision = True
                    break
            
            # Проверяем коллизии со специальными стенами
            if not collision and special_walls:
                for wall in special_walls:
                    if pygame.sprite.collide_rect(self, wall):
                        if not (wall.is_transparent and wall.is_currently_transparent):
                            collision = True
                            break
            
            # При коллизии возвращаемся и меняем направление
            if collision:
                self.rect.x = previous_x
                self.direction = 'right' if self.direction == 'left' else 'left'
        else:
            # Если предвидится столкновение с движущейся стеной, сразу меняем направление
            self.direction = 'right' if self.direction == 'left' else 'left'
        
        # Проверка границ экрана
        if self.rect.x <= 50:
            self.rect.x = 50
            self.direction = 'right'
        elif self.rect.x >= self.win_width - 50:
            self.rect.x = self.win_width - 50
            self.direction = 'left'