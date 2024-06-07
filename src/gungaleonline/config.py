import pygame


def load_image(path):
    try:
        image = pygame.image.load(path)
        if pygame.display.get_init():
            image = image.convert_alpha()
        return image
    except pygame.error as e:
        print(f"Cannot load image {path}: {e}")
        raise


FPS = 120

WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 576
WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_COPTION = "Gun Gale Online"

ASSETS_PATH = "src/assets/"
ANIMATIONS_PATH = ASSETS_PATH + "sprites/animations/"
ICONS_PATH = ASSETS_PATH + "sprites/icons/"
TILES_PATH = ASSETS_PATH + "sprites/tiles/"
FONT_PATH = ASSETS_PATH + "font/font.ttf"
FONT_SIZE_XS, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG = 10, 15, 20, 25

COLOR = {
    "background": (125, 112, 113),
    "black": (0, 0, 0),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "selected_weapon": (223, 246, 245),
    "shadows": (48, 44, 46),
    "text": (223, 246, 245),
    "text_input": (48, 44, 46),
}

ICONS = {
    "heart": load_image(ICONS_PATH + "heart.png"),
    "heart_half": load_image(ICONS_PATH + "heart_half.png"),
    "heart_empty": load_image(ICONS_PATH + "heart_empty.png"),
    "bullet": load_image(ICONS_PATH + "bullet.png"),
    "bullet_empty": load_image(ICONS_PATH + "bullet_empty.png"),
    "knife": load_image(ICONS_PATH + "knife.png"),
    "pistol": load_image(ICONS_PATH + "pistol.png"),
    "rifle": load_image(ICONS_PATH + "rifle.png"),
    "reload_1": load_image(ICONS_PATH + "reload_1.png"),
    "reload_2": load_image(ICONS_PATH + "reload_2.png"),
    "reload_3": load_image(ICONS_PATH + "reload_3.png"),
    "reload_4": load_image(ICONS_PATH + "reload_4.png"),
    "reload_5": load_image(ICONS_PATH + "reload_5.png"),
    "border_20x20": load_image(ICONS_PATH + "border_20x20.png"),
    "border_36x20": load_image(ICONS_PATH + "border_36x20.png"),
}
