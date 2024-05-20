import pygame
import time

from config import FPS


animations = {}


def load_animation(path, length):
    return [
        pygame.image.load(f"{path}{i+1}.png").convert_alpha() for i in range(length)
    ]


def to_renderer_position(pos):
    new_x = (1024 * pos[0]) / 1920
    new_y = (576 * pos[1]) / 1080
    return new_x, new_y


class Bullet:
    def __init__(self, direction, center, speed, damage, map):
        self._init_attributes(direction, center, speed, damage, map)

    def _init_attributes(self, direction, center, speed, damage, map):
        self.one_direction = direction
        self.direction = (direction[0] * speed, direction[1] * speed)
        self.center = center
        self.speed = speed
        self.damage = damage
        self.map = map
        self.dead = False
        self.collided = False
        self.last_time = time.time()
        self.dt = 1
        self._load_frames()
        self.frame = 0
        self.animation_change = 10
        self.animation_count = 0
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=self.center)
        self.mask = pygame.mask.from_surface(self.image)
        self._update_frame()

    def _load_frames(self):
        if "bullet_animation" not in animations:
            self.frames = load_animation("src/data/sprites/animations/bullet_", 3)
            animations["bullet_animation"] = self.frames
        else:
            self.frames = animations["bullet_animation"]

    def _update_frame(self):
        if self.animation_count >= self.animation_change:
            self.frame += 1
            self.animation_count = 0
            if self.frame == len(self.frames):
                self.dead = True
            else:
                self.image = self.frames[self.frame]
        self.animation_count += self.dt

    def update(self):
        self.dt = time.time() - self.last_time
        self.dt *= FPS
        self.last_time = time.time()

        if not self.collided:
            self._move_bullet()
            self._check_collision()
        else:
            self._update_frame()

    def _move_bullet(self):
        self.center = (
            self.center[0] + min(self.direction[0] * self.dt, 33),
            self.center[1] + min(self.direction[1] * self.dt, 33),
        )
        self.rect.center = self.center

    def _check_collision(self):
        for wall in self.map.walls:
            if self.rect.colliderect(wall.rect):
                while wall.rect.collidepoint(self.center):
                    self.center = (
                        self.center[0] - self.one_direction[0] * self.dt,
                        self.center[1] - self.one_direction[1] * self.dt,
                    )
                self.rect.center = self.center
                self.collided = True
                break

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
