import pygame
from config import *
from player import Player
from enemy import Enemy
from ui import draw_ui, draw_game_over, draw_victory
from controls import handle_input
from sounds import slash, hit, death, bgm
from game import reset_game
import random

pygame.init()
# Set fullscreen mode and get the display size
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
# Load and scale the background image to fit the screen
bg_image = pygame.image.load("assets/images/background.png").convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hate-Core")
clock = pygame.time.Clock()
if bgm:
    pygame.mixer.music.load(bgm)
    pygame.mixer.music.play(-1)

player, enemies = reset_game(SCREEN_WIDTH, SCREEN_HEIGHT)
game_over = False
victory = False
wave_number = 1

running = True
while running:
    screen.blit(bg_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if not game_over and not victory:
        handle_input(player, enemies)
        player.update()

        # Update enemies and check collisions
        for enemy in enemies:
            enemy.move_towards(player.rect)
            enemy.draw(screen)
            # Only damage player if health > 0 and not in death state
            if player.rect.colliderect(enemy.rect) and player.health > 0 and player.state != 'death':
                player.health = max(0, player.health - 1)  # Prevent negative health
                hit.play()

        # Remove dead enemies and add score
        original_enemy_count = len(enemies)
        enemies = [enemy for enemy in enemies if enemy.health > 0]  # Keep only alive enemies
        enemies_killed = original_enemy_count - len(enemies)
        if enemies_killed > 0:
            player.score += enemies_killed * 10
            print(f"Killed {enemies_killed} enemies! Score: {player.score}")

        # Check for victory (after killing 10 enemies total)
        if player.enemies_killed >= 10:
            victory = True

        # Spawn new enemies if all are dead (but fewer enemies)
        if len(enemies) == 0 and not victory:
            wave_number += 1
            enemies = [Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, player.rect.center) for _ in range(random.randint(2, 4))]

        player.draw(screen)
        draw_ui(screen, player, SCREEN_WIDTH, wave_number)

        # Handle player death - make it much faster
        if player.health <= 0 and player.state != 'death':
            death.play()
            player.die()
        # Show game over after just 2 frames of death animation
        if player.state == 'death' and player.death_frame >= 2:  # Much faster
            game_over = True
    elif victory:
        draw_victory(screen, SCREEN_WIDTH, SCREEN_HEIGHT, player.score)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player, enemies = reset_game(SCREEN_WIDTH, SCREEN_HEIGHT)
            game_over = False
            victory = False
            wave_number = 1
    else:
        draw_game_over(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player, enemies = reset_game(SCREEN_WIDTH, SCREEN_HEIGHT)
            game_over = False
            victory = False
            wave_number = 1
    pygame.display.flip()
    clock.tick(FPS)
