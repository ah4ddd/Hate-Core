import pygame
import config
from assets import Assets
import os

class Player:
    def __init__(self, x, y):
        # Load walk animation
        self.walk_sprites = []
        walk_dir = Assets.PLAYER_WALK_DIR
        for fname in sorted(os.listdir(walk_dir)):
            if fname.endswith('.png') and not fname.endswith('.Zone.Identifier'):
                sprite_path = os.path.join(str(walk_dir), fname)
                sprite = pygame.image.load(sprite_path).convert_alpha()
                # Ensure exact same size for all sprites
                sprite = pygame.transform.smoothscale(sprite, (128, 128))
                self.walk_sprites.append(sprite)
        # Load attack animation
        self.attack_sprites = []
        attack_dir = Assets.PLAYER_ATTACK_DIR
        for fname in sorted(os.listdir(attack_dir)):
            if fname.endswith('.png') and not fname.endswith('.Zone.Identifier'):
                sprite_path = os.path.join(str(attack_dir), fname)
                sprite = pygame.image.load(sprite_path).convert_alpha()
                # Ensure exact same size for all sprites
                sprite = pygame.transform.smoothscale(sprite, (128, 128))
                self.attack_sprites.append(sprite)
        # Load death animation
        self.death_sprites = []
        death_dir = Assets.PLAYER_DEATH_DIR
        for fname in sorted(os.listdir(death_dir)):
            if fname.endswith('.png') and not fname.endswith('.Zone.Identifier'):
                sprite_path = os.path.join(str(death_dir), fname)
                sprite = pygame.image.load(sprite_path).convert_alpha()
                # Ensure exact same size for all sprites
                sprite = pygame.transform.smoothscale(sprite, (128, 128))
                self.death_sprites.append(sprite)
        # Fallbacks
        if not self.walk_sprites:
            self.walk_sprites = [pygame.Surface((128, 128))]
            self.walk_sprites[0].fill((0, 100, 255))
        if not self.attack_sprites:
            self.attack_sprites = self.walk_sprites
        if not self.death_sprites:
            self.death_sprites = self.walk_sprites
        self.state = 'walk'  # walk, attack, death
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.animation_counter = 0
        self.image = self.walk_sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = config.PLAYER_HEALTH
        self.speed = config.PLAYER_SPEED
        self.score = 0
        self.attack_cooldown = 0
        self.attack_frame = 0
        self.death_frame = 0
        self.attack_range = 250  # Even larger attack range
        self.attack_speed = 0.8  # Much faster attack animation
        self.attack_effect_timer = 0
        self.enemies_killed = 0  # Track total enemies killed

    def move(self, move_keys):
        # Allow movement during attack, but not during death
        if self.state == 'death':
            return  # No movement during death only
        moved = False
        if move_keys[0]:
            self.rect.y -= self.speed
            moved = True
        if move_keys[1]:
            self.rect.y += self.speed
            moved = True
        if move_keys[2]:
            self.rect.x -= self.speed
            moved = True
        if move_keys[3]:
            self.rect.x += self.speed
            moved = True
        # Animate walk when moving and not attacking
        if moved and self.state == 'walk':
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.current_sprite = (self.current_sprite + 1) % len(self.walk_sprites)
                self.animation_counter = 0
                self.image = self.walk_sprites[self.current_sprite]

    def attack(self, enemies=None):
        if self.attack_cooldown == 0:  # Allow attack anytime if not on cooldown
            print("ATTACKING!")  # Debug
            self.state = 'attack'
            self.attack_frame = 0
            self.attack_counter = 0
            self.attack_effect_timer = 15  # Show attack effect
            # Damage enemies in range
            if enemies is not None:
                enemies_hit = 0
                for enemy in enemies:
                    distance = ((self.rect.centerx - enemy.rect.centerx) ** 2 +
                               (self.rect.centery - enemy.rect.centery) ** 2) ** 0.5
                    print(f"Distance to enemy: {distance}, Attack range: {self.attack_range}")  # Debug
                    if distance < self.attack_range:
                        enemy.health = 0  # kill enemy
                        enemies_hit += 1
                        self.enemies_killed += 1
                        print(f"ENEMY KILLED! Distance was {distance}")
                if enemies_hit > 0:
                    print(f"SLASH! Hit {enemies_hit} enemies!")
                else:
                    print("Attack missed!")

    def update(self):
        if self.state == 'attack':
            self.attack_counter += self.attack_speed
            if self.attack_counter >= 1:
                self.attack_frame += 1
                self.attack_counter = 0
                if self.attack_frame < len(self.attack_sprites):
                    self.image = self.attack_sprites[self.attack_frame]
                else:
                    self.state = 'walk'
                    self.current_sprite = 0
                    self.image = self.walk_sprites[0]
                    self.attack_cooldown = 5  # frames - shorter cooldown
        elif self.state == 'death':
            self.animation_counter += 1.0  # Much faster death animation
            if self.animation_counter >= 1:
                self.death_frame += 1
                self.animation_counter = 0
                if self.death_frame < len(self.death_sprites):
                    self.image = self.death_sprites[self.death_frame]
        else:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

        if self.attack_effect_timer > 0:
            self.attack_effect_timer -= 1

    def die(self):
        self.state = 'death'
        self.death_frame = 0
        self.animation_counter = 0
        self.image = self.death_sprites[0]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # Only show slash effect, no yellow circle
        if self.attack_effect_timer > 0:
            # Draw multiple slash lines for better effect
            pygame.draw.line(surface, (255, 255, 255),
                           (self.rect.centerx - 60, self.rect.centery - 60),
                           (self.rect.centerx + 60, self.rect.centery + 60), 6)
            pygame.draw.line(surface, (255, 255, 0),
                           (self.rect.centerx - 40, self.rect.centery - 40),
                           (self.rect.centerx + 40, self.rect.centery + 40), 4)

    def is_dead(self):
        return self.health <= 0 and self.state != 'death'
