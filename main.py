import pygame
from config import *
from player import Player
from enemy import Enemy
from ui import draw_ui, draw_game_over, draw_victory, draw_touch_controls, draw_pause_screen
from controls import handle_input, handle_touch_movement
from sounds import slash, hit, death, bgm
from game import reset_game
import random
import os

pygame.init()
# Set fullscreen mode to use the entire screen but keep title bar
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
# Load and scale the background image to fit the screen
bg_image = pygame.image.load("assets/images/background.png").convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HATE-CORE by Ahad")  # Your title bar!
clock = pygame.time.Clock()

# High score system
def load_high_score():
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))
    except:
        pass

# Try to load BGM with error handling
if bgm:
    try:
        pygame.mixer.music.load(bgm)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Warning: Could not load BGM, game will run without background music")

player, enemies = reset_game(SCREEN_WIDTH, SCREEN_HEIGHT)
game_over = False
paused = False
wave_number = 1
high_score = load_high_score()
touch_pos = None
attack_button_pressed = False

running = True
while running:
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_r and game_over:
                player, enemies = reset_game(SCREEN_WIDTH, SCREEN_HEIGHT)
                game_over = False
                wave_number = 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Touch controls for mobile
            if event.button == 1:  # Left click/touch
                touch_pos = event.pos

                # Check if touch is on pause button (updated position)
                pause_button_rect = pygame.Rect(SCREEN_WIDTH - 90, 20, 70, 45)
                if pause_button_rect.collidepoint(event.pos):
                    paused = not paused

                # Check if touch is on attack button (updated position)
                attack_button_rect = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120, 90, 90)
                if attack_button_rect.collidepoint(event.pos):
                    attack_button_pressed = True
                    if not game_over and not paused:
                        player.attack(enemies)

                # Check if touch is on restart button (when game over)
                if game_over:
                    restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 40)
                    if restart_button_rect.collidepoint(event.pos):
                        player, enemies = reset_game(SCREEN_WIDTH, SCREEN_HEIGHT)
                        game_over = False
                        wave_number = 1

        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop movement when touch ends
            touch_pos = None
            attack_button_pressed = False
        elif event.type == pygame.MOUSEMOTION:
            # Update touch position for movement
            if pygame.mouse.get_pressed()[0]:  # Left mouse button held
                touch_pos = event.pos

    if not game_over and not paused:
        # Handle keyboard input
        handle_input(player, enemies)
        # Handle touch movement
        handle_touch_movement(player, touch_pos)
        player.update()

        # Update enemies and check collisions
        for enemy in enemies:
            enemy.move_towards(player.rect)
            enemy.draw(screen)
            # Only damage player if health > 0 and not in death state
            if player.rect.colliderect(enemy.rect) and player.health > 0 and player.state != 'death':
                player.health = max(0, player.health - 2)  # More damage from tougher enemies
                hit.play()

        # Remove dead enemies and add score
        original_enemy_count = len(enemies)
        enemies = [enemy for enemy in enemies if enemy.health > 0]  # Keep only alive enemies
        enemies_killed = original_enemy_count - len(enemies)
        if enemies_killed > 0:
            player.score += enemies_killed * 10
            print(f"Killed {enemies_killed} enemies! Score: {player.score}")

        # Spawn new enemies if all are dead (unlimited game)
        if len(enemies) == 0:
            wave_number += 1
            # Increase difficulty with each wave
            enemy_count = min(2 + wave_number // 3, 8)  # More enemies, max 8
            enemies = [Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, player.rect.center) for _ in range(enemy_count)]

        player.draw(screen)
        draw_ui(screen, player, SCREEN_WIDTH, wave_number, high_score)
        draw_touch_controls(screen, SCREEN_WIDTH, SCREEN_HEIGHT, attack_button_pressed)

        # Handle player death - make it much faster
        if player.health <= 0 and player.state != 'death':
            death.play()
            player.die()
        # Show game over after just 2 frames of death animation
        if player.state == 'death' and player.death_frame >= 2:  # Much faster
            # Check for new high score
            if player.score > high_score:
                high_score = player.score
                save_high_score(high_score)
            game_over = True
    elif paused:
        draw_pause_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    else:
        draw_game_over(screen, SCREEN_WIDTH, SCREEN_HEIGHT, high_score)

    # Draw thick white border on top of everything so it's very visible
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 8)

    pygame.display.flip()
    clock.tick(FPS)
