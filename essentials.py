from pathlib import Path
import pygame

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.joinpath("assets")
MUSIC_DIR = BASE_DIR.joinpath("music")

def load_sprite(name):
    print("Loading sprite: " + name)
    path = ASSETS_DIR.glob("**/" + name + "*")
    return pygame.image.load(list(path)[0]).convert_alpha()

def load_music(name):
    path = MUSIC_DIR.glob("**/" + name + "*")
    return pygame.mixer.Sound(list(path)[0])
def game_over():
    screen = pygame.display.get_surface()
    midx = screen.get_width() / 2
    midy = screen.get_height() / 2
    font = pygame.font.Font(None, 150)
    text = font.render("Game Over", True, (0, 0, 0))
    text_rect = text.get_rect(center=(midx, midy))
    
    if screen is None:
        return
    screen.blit(text, text_rect)