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

def handle_touch_movement(player, touch_pos):
    """Handle touch movement - move player towards touch position"""
    if touch_pos:
        # Calculate direction to touch point
        dx = touch_pos[0] - player.rect.centerx
        dy = touch_pos[1] - player.rect.centery
        
        # Normalize and create movement keys
        distance = max(abs(dx), abs(dy))
        if distance > 10:  # Only move if touch is far enough
            move_keys = [False, False, False, False]
            if dy < -10:  # Touch is above player
                move_keys[0] = True  # Up
            elif dy > 10:  # Touch is below player
                move_keys[1] = True  # Down
            if dx < -10:  # Touch is left of player
                move_keys[2] = True  # Left
            elif dx > 10:  # Touch is right of player
                move_keys[3] = True  # Right
            player.move(move_keys)
