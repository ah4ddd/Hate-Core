from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_ROOT / "assets"


class Assets:
    # Base directories
    ROOT = ASSETS_DIR
    IMAGES_DIR = ASSETS_DIR / "images"
    SOUNDS_DIR = ASSETS_DIR / "sounds"

    # Common image files (strings)
    BACKGROUND = str(IMAGES_DIR / "background.png")
    DRAGON = str(IMAGES_DIR / "enemy" / "fly" / "Biomech_Dragon_Splice.png")

    # Player sprite directories (Path objects for iteration)
    PLAYER_WALK_DIR = IMAGES_DIR / "player" / "Walk"
    PLAYER_ATTACK_DIR = IMAGES_DIR / "player" / "Attack"
    PLAYER_DEATH_DIR = IMAGES_DIR / "player" / "Death"

    # Sound files (strings)
    SLASH_WAV = str(SOUNDS_DIR / "slash.wav")
    HIT_WAV = str(SOUNDS_DIR / "hit.wav")
    DEATH_WAV = str(SOUNDS_DIR / "death.wav")

    # Possible BGM files (strings)
    POSSIBLE_BGM_FILES = [
        str(SOUNDS_DIR / "Cris Velasco - Pandora's Song  God of War III (Original Game Soundtrack).mp3"),
        str(SOUNDS_DIR / "bgm.mp3"),
        str(SOUNDS_DIR / "music.mp3"),
        str(SOUNDS_DIR / "background.mp3"),
        str(SOUNDS_DIR / "pandora.mp3"),
    ]
