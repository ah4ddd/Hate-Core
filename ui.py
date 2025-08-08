import pygame
import config

def draw_ui(screen, player, screen_width, wave_number, high_score):
    # Create a dark, horror-themed UI
    font_large = pygame.font.SysFont("Arial", 36)
    font_medium = pygame.font.SysFont("Arial", 28)
    font_small = pygame.font.SysFont("Arial", 20)

    # Draw dark overlay at top
    overlay = pygame.Surface((screen_width, 80))
    overlay.set_alpha(180)
    overlay.fill((20, 0, 0))  # Dark red background
    screen.blit(overlay, (0, 0))

    # Score with glowing effect
    score_text = font_large.render(f"SCORE: {player.score}", True, (255, 255, 0))
    score_shadow = font_large.render(f"SCORE: {player.score}", True, (100, 100, 0))
    screen.blit(score_shadow, (screen_width // 2 - score_text.get_width() // 2 + 2, 12))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 10))

    # High score display (moved left to avoid overlap)
    high_score_text = font_medium.render(f"HIGH SCORE: {high_score}", True, (0, 255, 255))
    screen.blit(high_score_text, (screen_width - high_score_text.get_width() - 120, 10))  # Moved left

    # Kill counter with blood red color
    kill_text = font_medium.render(f"KILLS: {player.enemies_killed}", True, (255, 0, 0))
    screen.blit(kill_text, (screen_width // 2 - kill_text.get_width() // 2, 50))

    # Wave counter
    wave_text = font_small.render(f"WAVE {wave_number}", True, (0, 255, 0))
    screen.blit(wave_text, (10, 10))

    # Player health bar
    bar_width = 200
    bar_height = 20
    bar_x = 10
    bar_y = 40

    # Health bar background
    pygame.draw.rect(screen, (50, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    # Health bar fill
    health_percentage = player.health / config.PLAYER_HEALTH
    health_width = int(health_percentage * bar_width)
    if health_width > 0:
        # Color based on health
        if health_percentage > 0.6:
            health_color = (0, 255, 0)  # Green
        elif health_percentage > 0.3:
            health_color = (255, 255, 0)  # Yellow
        else:
            health_color = (255, 0, 0)  # Red
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
    # Health bar border
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    # Health text
    health_text = font_small.render(f"HEALTH: {player.health}", True, (255, 255, 255))
    screen.blit(health_text, (bar_x + bar_width + 10, bar_y + 2))

    # Controls info with dark theme
    controls_font = pygame.font.SysFont("Arial", 18)
    controls = controls_font.render("WASD/Arrows: Move | SPACE: Attack | P: Pause | ESC: Exit", True, (150, 150, 150))
    screen.blit(controls, (10, screen.get_height() - 30))

def draw_touch_controls(screen, screen_width, screen_height, attack_button_pressed):
    """Draw beautiful touch control buttons for mobile"""

    # Movement joystick area (left side) - Beautiful circular design
    joystick_center = (120, screen_height - 120)
    joystick_radius = 70

    # Draw joystick outer ring with gradient effect
    for i in range(5):
        alpha = 255 - (i * 40)
        if alpha > 0:
            ring_surface = pygame.Surface((joystick_radius * 2 + 10, joystick_radius * 2 + 10), pygame.SRCALPHA)
            pygame.draw.circle(ring_surface, (100, 100, 100, alpha), (joystick_radius + 5, joystick_radius + 5), joystick_radius + 5 - i)
            screen.blit(ring_surface, (joystick_center[0] - joystick_radius - 5, joystick_center[1] - joystick_radius - 5))

    # Draw joystick background with metallic effect
    pygame.draw.circle(screen, (80, 80, 80), joystick_center, joystick_radius)
    pygame.draw.circle(screen, (120, 120, 120), joystick_center, joystick_radius - 5)
    pygame.draw.circle(screen, (60, 60, 60), joystick_center, joystick_radius, 3)

    # Draw joystick center with highlight
    pygame.draw.circle(screen, (150, 150, 150), joystick_center, joystick_radius - 15)
    pygame.draw.circle(screen, (200, 200, 200), joystick_center, joystick_radius - 20)

    # Draw joystick label with shadow
    font = pygame.font.SysFont("Arial", 18, bold=True)
    joystick_text = font.render("MOVE", True, (255, 255, 255))
    joystick_shadow = font.render("MOVE", True, (50, 50, 50))
    screen.blit(joystick_shadow, (joystick_center[0] - joystick_text.get_width() // 2 + 1, joystick_center[1] - 8 + 1))
    screen.blit(joystick_text, (joystick_center[0] - joystick_text.get_width() // 2, joystick_center[1] - 8))

    # Attack button (right side) - Beautiful gradient design
    attack_button_rect = pygame.Rect(screen_width - 120, screen_height - 120, 90, 90)

    # Draw attack button with gradient effect
    if attack_button_pressed:
        # Pressed state - darker
        pygame.draw.rect(screen, (150, 0, 0), attack_button_rect)
        pygame.draw.rect(screen, (200, 0, 0), attack_button_rect.inflate(-10, -10))
        pygame.draw.rect(screen, (100, 0, 0), attack_button_rect, 4)
    else:
        # Normal state - bright gradient
        pygame.draw.rect(screen, (200, 0, 0), attack_button_rect)
        pygame.draw.rect(screen, (255, 50, 50), attack_button_rect.inflate(-10, -10))
        pygame.draw.rect(screen, (150, 0, 0), attack_button_rect, 4)

    # Add highlight effect
    highlight_rect = pygame.Rect(attack_button_rect.x + 5, attack_button_rect.y + 5, attack_button_rect.width - 10, 20)
    pygame.draw.rect(screen, (255, 255, 255, 100), highlight_rect)

    # Draw attack button label with shadow
    attack_text = font.render("ATTACK", True, (255, 255, 255))
    attack_shadow = font.render("ATTACK", True, (50, 50, 50))
    screen.blit(attack_shadow, (attack_button_rect.centerx - attack_text.get_width() // 2 + 1, attack_button_rect.centery - 8 + 1))
    screen.blit(attack_text, (attack_button_rect.centerx - attack_text.get_width() // 2, attack_button_rect.centery - 8))

    # Pause button (top right) - Sleek modern design
    pause_button_rect = pygame.Rect(screen_width - 90, 20, 70, 45)

    # Draw pause button with gradient
    pygame.draw.rect(screen, (60, 60, 60), pause_button_rect)
    pygame.draw.rect(screen, (100, 100, 100), pause_button_rect.inflate(-5, -5))
    pygame.draw.rect(screen, (40, 40, 40), pause_button_rect, 3)

    # Add highlight
    highlight_rect = pygame.Rect(pause_button_rect.x + 3, pause_button_rect.y + 3, pause_button_rect.width - 6, 15)
    pygame.draw.rect(screen, (255, 255, 255, 80), highlight_rect)

    # Draw pause button label
    pause_text = font.render("PAUSE", True, (255, 255, 255))
    pause_shadow = font.render("PAUSE", True, (30, 30, 30))
    screen.blit(pause_shadow, (pause_button_rect.centerx - pause_text.get_width() // 2 + 1, pause_button_rect.centery - 8 + 1))
    screen.blit(pause_text, (pause_button_rect.centerx - pause_text.get_width() // 2, pause_button_rect.centery - 8))

def draw_pause_screen(screen, screen_width, screen_height):
    """Draw pause screen overlay"""
    # Create dark overlay
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Pause text
    font = pygame.font.SysFont("Arial", 72)
    pause_text = font.render("PAUSED", True, (255, 255, 0))
    screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - 100))

    # Instructions
    instruction_font = pygame.font.SysFont("Arial", 30)
    instruction_text = instruction_font.render("Press P to Resume", True, (255, 255, 255))
    screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2))

def draw_game_over(screen, screen_width, screen_height, high_score):
    # Create dark overlay
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Blood red game over text
    font = pygame.font.SysFont("Arial", 72)
    over = font.render("GAME OVER", True, (255, 0, 0))
    over_shadow = font.render("GAME OVER", True, (100, 0, 0))
    screen.blit(over_shadow, (screen_width // 2 - over.get_width() // 2 + 3, screen_height // 2 - over.get_height() // 2 + 3))
    screen.blit(over, (screen_width // 2 - over.get_width() // 2, screen_height // 2 - over.get_height() // 2))

    # High score display
    high_score_font = pygame.font.SysFont("Arial", 36)
    high_score_text = high_score_font.render(f"High Score: {high_score}", True, (0, 255, 255))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 20))

    # Restart instruction
    restart_font = pygame.font.SysFont("Arial", 36)
    restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 70))

    # Exit instruction
    exit_font = pygame.font.SysFont("Arial", 30)
    exit_text = exit_font.render("Press ESC to Exit", True, (150, 150, 150))
    screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 120))

def draw_victory(screen, screen_width, screen_height, score):
    # Create golden overlay
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(150)
    overlay.fill((255, 215, 0))  # Gold color
    screen.blit(overlay, (0, 0))

    # Victory text with glow effect
    font = pygame.font.SysFont("Arial", 80)
    victory = font.render("VICTORY!", True, (255, 255, 0))
    victory_shadow = font.render("VICTORY!", True, (100, 100, 0))
    screen.blit(victory_shadow, (screen_width // 2 - victory.get_width() // 2 + 3, screen_height // 2 - 150 + 3))
    screen.blit(victory, (screen_width // 2 - victory.get_width() // 2, screen_height // 2 - 150))

    # Final score
    score_font = pygame.font.SysFont("Arial", 48)
    score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 50))

    # Restart instruction
    restart_font = pygame.font.SysFont("Arial", 36)
    restart_text = restart_font.render("Press R to Play Again", True, (255, 255, 255))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))

    # Exit instruction
    exit_font = pygame.font.SysFont("Arial", 30)
    exit_text = exit_font.render("Press ESC to Exit", True, (200, 200, 200))
    screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 100))
