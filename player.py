import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/player.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.health = 100
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
