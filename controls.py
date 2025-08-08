import pygame

def handle_input(player, enemies):
    keys = pygame.key.get_pressed()
    # WASD and Arrow keys
    move_keys = [
        keys[pygame.K_w] or keys[pygame.K_UP],
        keys[pygame.K_s] or keys[pygame.K_DOWN],
        keys[pygame.K_a] or keys[pygame.K_LEFT],
        keys[pygame.K_d] or keys[pygame.K_RIGHT],
    ]
    player.move(move_keys)
    # Attack with spacebar
    if keys[pygame.K_SPACE]:
        player.attack(enemies)
