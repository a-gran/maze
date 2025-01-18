import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.start_x = player_x
        self.start_y = player_y

    def reset(self, window):  # Добавляем параметр window
        window.blit(self.image, (self.rect.x, self.rect.y))

    def respawn(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y