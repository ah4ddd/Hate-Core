import pygame

def draw_ui(screen, player, screen_width, wave_number):
    font = pygame.font.SysFont("Arial", 30)
    score = font.render(f"Score: {player.score}", True, (255, 255, 255))
    health = font.render(f"Health: {player.health}", True, (255, 0, 0))
    wave = font.render(f"Wave: {wave_number}", True, (0, 255, 0))
    enemies_killed = font.render(f"Enemies Killed: {player.enemies_killed}/10", True, (255, 255, 0))
    # Centered at top
    screen.blit(score, (screen_width // 2 - score.get_width() // 2, 10))
    screen.blit(health, (screen_width // 2 - health.get_width() // 2, 50))
    screen.blit(wave, (10, 10))
    screen.blit(enemies_killed, (10, 50))

    # Add controls info
    controls_font = pygame.font.SysFont("Arial", 20)
    controls = controls_font.render("WASD/Arrows: Move | SPACE: Attack | ESC: Exit", True, (200, 200, 200))
    screen.blit(controls, (10, screen.get_height() - 30))

def draw_game_over(screen, screen_width, screen_height):
    font = pygame.font.SysFont("Arial", 50)
    over = font.render("GAME OVER - Press R to Restart", True, (200, 0, 0))
    screen.blit(over, (screen_width // 2 - over.get_width() // 2, screen_height // 2 - over.get_height() // 2))

    # Add exit instruction
    exit_font = pygame.font.SysFont("Arial", 30)
    exit_text = exit_font.render("Press ESC to Exit", True, (150, 150, 150))
    screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 50))

def draw_victory(screen, screen_width, screen_height, score):
    font = pygame.font.SysFont("Arial", 60)
    victory = font.render("VICTORY!", True, (0, 255, 0))
    screen.blit(victory, (screen_width // 2 - victory.get_width() // 2, screen_height // 2 - 100))

    score_font = pygame.font.SysFont("Arial", 40)
    score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 20))

    restart_font = pygame.font.SysFont("Arial", 30)
    restart_text = restart_font.render("Press R to Play Again", True, (200, 200, 200))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))

    exit_font = pygame.font.SysFont("Arial", 30)
    exit_text = exit_font.render("Press ESC to Exit", True, (150, 150, 150))
    screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 100))
