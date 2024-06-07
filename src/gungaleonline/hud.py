import time

import pygame
from config import *
from player import *


class Hud:
    def __init__(self, p: Player):
        self.player = p

        self.last_weapon = self.player.active_weapon
        self.last_ammo = self.player.ammo.copy()
        self.last_hearts = self.player.hearts
        self.last_reload = 0

        self.full_reload_duration = 60
        self.full_reload_count = 0

        self.last_time = time.time()
        self.dt = 1

        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE_XS)

        self.heart_images = [
            ICONS[key] for key in ["heart", "heart_half", "heart_empty"]
        ]
        self.bullet_images = [ICONS[key] for key in ["bullet", "bullet_empty"]]
        self.weapon_images = [ICONS[key] for key in ["knife", "pistol", "rifle"]]
        self.reload_images = [
            ICONS[key]
            for key in ["reload_1", "reload_2", "reload_3", "reload_4", "reload_5"]
        ]
        self.border_20x20 = ICONS["border_20x20"]
        self.border_36x20 = ICONS["border_36x20"]

        self.heart_render = pygame.Surface(
            (
                self.heart_images[0].get_width() * self.player.max_hearts,
                self.heart_images[0].get_height(),
            )
        )
        self.heart_render.set_colorkey(COLOR["black"])

        self.bullets_render = pygame.Surface(
            (
                self.bullet_images[0].get_width() * 10,
                (self.bullet_images[0].get_height() + 5)
                * int((self.player.rifle_max_ammo / 10)),
            )
        )
        self.bullets_render.set_colorkey(COLOR["black"])

        self.weapons_render = pygame.Surface(
            (
                self.border_36x20.get_width(),
                (self.border_36x20.get_height() + 5) * len(self.weapon_images),
            )
        )
        self.weapons_render.set_colorkey(COLOR["black"])

        self.reload_render = pygame.Surface(
            (self.reload_images[0].get_width(), self.reload_images[0].get_height())
        )
        self.reload_render.set_colorkey(COLOR["black"])

        self.render_hearts()
        self.render_bullets()
        self.render_weapons()
        self.render_reload(self.last_reload)

    def update(self):
        self.dt = time.time() - self.last_time
        self.dt *= FPS
        self.last_time = time.time()

        if self.player.active_weapon != self.last_weapon:
            self.last_weapon = self.player.active_weapon
            self.render_weapons()

        if self.player.ammo != self.last_ammo:
            self.last_ammo = self.player.ammo.copy()
            self.render_bullets()

        if self.player.hearts != self.last_hearts:
            self.last_hearts = self.player.hearts
            self.render_hearts()

        if self.player.reloading:
            progress = self.player.reloading_counter / self.player.reloading_duration
            if progress > self.last_reload:
                self.render_reload(progress)
                self.last_reload = progress
        elif self.last_reload != 0:
            self.last_reload = 0
            self.render_reload(1)
            self.full_reload_count = self.full_reload_duration
        elif self.full_reload_count > 0:
            self.full_reload_count -= self.dt
        else:
            self.render_reload(self.last_reload)

    def render(self, surface: pygame.Surface):
        surface.blit(self.heart_render, (36, 36))

        surface.blit(
            self.bullets_render,
            (
                WINDOW_WIDTH - self.bullets_render.get_width() - 36,
                WINDOW_HEIGHT - self.bullets_render.get_height() - 36,
            ),
        )

        surface.blit(
            self.weapons_render,
            (WINDOW_WIDTH - self.weapons_render.get_width() - 36, 36),
        )

        if self.player.reloading or self.full_reload_count > 0:
            surface.blit(
                self.reload_render,
                (
                    WINDOW_WIDTH - self.reload_render.get_width() - 36,
                    WINDOW_HEIGHT
                    - self.bullets_render.get_height()
                    - 36
                    - 10
                    - self.reload_render.get_height(),
                ),
            )

    def render_hearts(self):
        self.heart_render.fill(COLOR["black"])

        x = 0
        for i in range(int(self.player.hearts)):
            self.heart_render.blit(
                self.heart_images[0], (i * self.heart_images[0].get_width(), 0)
            )
            x += 1

        next_x = x
        if self.player.hearts % 1 == 0.5:
            self.heart_render.blit(
                self.heart_images[1], (next_x * self.heart_images[1].get_width(), 0)
            )
            x += 1

        for i in range(self.player.max_hearts - x):
            self.heart_render.blit(
                self.heart_images[2], ((i + x) * self.heart_images[2].get_width(), 0)
            )

    def render_bullets(self):
        self.bullets_render = pygame.Surface(
            (
                self.bullet_images[0].get_width() * 10,
                (self.bullet_images[0].get_height() + 5)
                * int((self.player.ammo[0] / 10)),
            )
        )
        self.bullets_render.set_colorkey(COLOR["black"])

        self.bullets_render.fill(COLOR["black"])

        full = self.player.ammo[1]
        empty = self.player.ammo[0] - full

        x = 0
        y = 0
        for i in range(full):
            self.bullets_render.blit(
                self.bullet_images[0],
                (
                    x * self.bullet_images[0].get_width(),
                    y * (self.bullet_images[0].get_height() + 5),
                ),
            )
            x += 1
            if x == 10:
                x = 0
                y += 1

        for i in range(empty):
            self.bullets_render.blit(
                self.bullet_images[1],
                (
                    x * self.bullet_images[0].get_width(),
                    y * (self.bullet_images[0].get_height() + 5),
                ),
            )
            x += 1
            if x == 10:
                x = 0
                y += 1

    def render_weapons(self):
        self.weapons_render.fill(COLOR["black"])

        if self.player.active_weapon == "rifle":
            pygame.draw.rect(
                self.weapons_render, COLOR["selected_weapon"], (4, 4, 64, TILE_SIZE)
            )
        self.weapons_render.blit(self.border_36x20, (0, 0))
        self.weapons_render.blit(self.weapon_images[2], (4, 4))

        if self.player.active_weapon == "pistol":
            pygame.draw.rect(
                self.weapons_render,
                COLOR["selected_weapon"],
                (
                    4 + TILE_SIZE,
                    self.border_36x20.get_height() + 5 + 4,
                    TILE_SIZE,
                    TILE_SIZE,
                ),
            )
        self.weapons_render.blit(
            self.border_20x20, (TILE_SIZE, self.border_36x20.get_height() + 5)
        )
        self.weapons_render.blit(
            self.weapon_images[1],
            (4 + TILE_SIZE, self.border_36x20.get_height() + 5 + 4),
        )

        if self.player.active_weapon == "knife":
            pygame.draw.rect(
                self.weapons_render,
                COLOR["selected_weapon"],
                (
                    4 + TILE_SIZE,
                    self.border_36x20.get_height() * 2 + 5 * 2 + 4,
                    TILE_SIZE,
                    TILE_SIZE,
                ),
            )
        self.weapons_render.blit(
            self.border_20x20, (TILE_SIZE, self.border_36x20.get_height() * 2 + 5 * 2)
        )
        self.weapons_render.blit(
            self.weapon_images[0],
            (4 + TILE_SIZE, self.border_36x20.get_height() * 2 + 5 * 2 + 4),
        )

    def render_reload(self, progress):
        self.reload_render.fill(COLOR["black"])

        if progress < 0.25:
            self.reload_render.blit(self.reload_images[0], (0, 0))
        elif progress < 0.5:
            self.reload_render.blit(self.reload_images[1], (0, 0))
        elif progress < 0.75:
            self.reload_render.blit(self.reload_images[2], (0, 0))
        elif progress < 1:
            self.reload_render.blit(self.reload_images[3], (0, 0))
        else:
            self.reload_render.blit(self.reload_images[4], (0, 0))
