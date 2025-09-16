# sounds.py
import pygame
import os
from assets import Assets

# Try to initialize audio, but handle cases where it's not available (like in WSL)
try:
    pygame.mixer.init()
    audio_available = True
except pygame.error:
    audio_available = False
    print("Warning: Audio not available. Game will run without sound.")

# Create dummy sound objects that do nothing when played
class DummySound:
    def play(self):
        pass

# Create sound objects only if audio is available
if audio_available:
    # Try to load each sound file individually
    try:
        slash = pygame.mixer.Sound(Assets.SLASH_WAV)
    except (pygame.error, FileNotFoundError):
        print("Warning: Could not load slash.wav, using dummy sound")
        slash = DummySound()

    try:
        hit = pygame.mixer.Sound(Assets.HIT_WAV)
    except (pygame.error, FileNotFoundError):
        print("Warning: Could not load hit.wav, using dummy sound")
        hit = DummySound()

    try:
        death = pygame.mixer.Sound(Assets.DEATH_WAV)
    except (pygame.error, FileNotFoundError):
        print("Warning: Could not load death.wav, using dummy sound")
        death = DummySound()

    # Check for BGM files - try multiple possible names
    bgm = None
    possible_bgm_files = Assets.POSSIBLE_BGM_FILES

    for bgm_file in possible_bgm_files:
        if os.path.exists(bgm_file):
            bgm = bgm_file
            print(f"Found BGM: {bgm_file}")
            break

    if bgm is None:
        print("Warning: Could not find any BGM file")
else:
    # Create dummy sound objects that do nothing when played
    slash = DummySound()
    hit = DummySound()
    death = DummySound()
    bgm = None
