from player import Player
from enemy import Enemy
import random
import config
import math

def reset_game(screen_width, screen_height):
    # Center player
    player = Player(screen_width // 2, screen_height // 2)
    enemies = [Enemy(screen_width, screen_height, player.rect.center) for _ in range(random.randint(3, 6))]
    return player, enemies
