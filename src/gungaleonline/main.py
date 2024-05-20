import pygame

from config import *
from scene import *


class Game:
    def __init__(self):
        pygame.init()

        self.running = True

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_LOCATION, FONT_SIZE)
        self.screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
        self.render_surface = pygame.Surface(WINDOW_DIMENSIONS)

        self.input = []

        """mode = input('Mode: ')
        if mode == '1':
            self.main_scene = scene.HostScene('src/data/maps/map_1.csv')
            self.active_scene = self.main_scene
        elif mode == '2':
            ip = input('IP: ')
            port = int(input('Port: '))
            self.main_scene = scene.ClientScene((ip, port))
            # self.main_scene = scene.ClientScene()
            self.active_scene = self.main_scene
        elif mode == '3':
            self.active_scene = scene.MainMenuScene()"""

        self.active_scene = MainMenuScene()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_input()
            self.update_scene()
            self.render_scene()
            self.update_screen()

    def handle_input(self):
        self.input = pygame.event.get()
        for event in self.input:
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.active_scene.stop()
                self.running = False

    def update_scene(self):
        self.active_scene.update(self.render_surface, self.input)

    def render_scene(self):
        fps_text = "fps: " + str(round(self.clock.get_fps(), 2))
        self.render_surface.blit(
            self.font.render(fps_text, True, COLOR["text"]), (5, 5)
        )
        self.screen.blit(
            pygame.transform.scale(self.render_surface, WINDOW_DIMENSIONS), (0, 0)
        )
        pygame.display.update()

    def update_screen(self):
        if self.active_scene.next_scene:
            self.active_scene = self.active_scene.next_scene
            pygame.display.set_caption(
                f"{WINDOW_COPTION}: {self.active_scene.__class__.__name__}"
            )


if __name__ == "__main__":
    app = Game()
    app.run()
