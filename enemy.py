import pygame
import random
import config
import os
import math

class Enemy:
    def __init__(self, screen_width, screen_height, player_pos):
        # Load dragon sprite as a static image
        dragon_path = "assets/images/enemy/fly/Biomech Dragon Splice.png"
        if os.path.exists(dragon_path):
            image = pygame.image.load(dragon_path).convert_alpha()
            self.image = pygame.transform.smoothscale(image, (256, 256))
        else:
            self.image = pygame.Surface((128, 128))
            self.image.fill((255, 0, 0))
        # Spawn at least 400px away from player
        while True:
            x = random.randint(100, screen_width - 356)
            y = random.randint(100, screen_height - 356)
            if math.hypot(x - player_pos[0], y - player_pos[1]) > 400:
                break
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = config.ENEMY_HEALTH
        self.speed = config.ENEMY_SPEED
        # For future: projectiles
        self.projectiles = []

    def move_towards(self, target_rect):
        if self.rect.x < target_rect.x: self.rect.x += self.speed
        if self.rect.x > target_rect.x: self.rect.x -= self.speed
        if self.rect.y < target_rect.y: self.rect.y += self.speed
        if self.rect.y > target_rect.y: self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # For future: draw projectiles
        for proj in self.projectiles:
            pygame.draw.circle(surface, (255, 100, 0), proj, 12)

    def is_dead(self):
        return self.health <= 0
