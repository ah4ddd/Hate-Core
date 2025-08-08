# sounds.py
import pygame

# Try to initialize audio, but handle cases where it's not available (like in WSL)
try:
    pygame.mixer.init()
    audio_available = True
except pygame.error:
    audio_available = False
    print("Warning: Audio not available. Game will run without sound.")

# Create sound objects only if audio is available
if audio_available:
    slash = pygame.mixer.Sound("assets/sounds/slash.wav")
    hit = pygame.mixer.Sound("assets/sounds/hit.wav")
    death = pygame.mixer.Sound("assets/sounds/death.wav")
    bgm = "assets/sounds/bgm.mp3"
else:
    # Create dummy sound objects that do nothing when played
    class DummySound:
        def play(self):
            pass

    slash = DummySound()
    hit = DummySound()
    death = DummySound()
    bgm = None
