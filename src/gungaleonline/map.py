import csv

import pygame
from config import COLOR, NOT_EXISTS, TILE_SIZE, TILES_PATH
from shapely import geometry


class Tile:
    def __init__(self, image, rect):
        self.image = image
        self.rect: pygame.Rect = rect
        self.mask = pygame.mask.from_surface(self.image)
        self.corners = [
            self.rect.topleft,
            self.rect.topright,
            self.rect.bottomright,
            self.rect.bottomleft,
        ]


class Wall:
    def __init__(self, tiles, vertical=False):
        self.tiles = tiles
        self.vertical = vertical

        x = self.tiles[0].rect.x
        y = self.tiles[0].rect.y

        if self.vertical:
            width = TILE_SIZE
            height = TILE_SIZE * len(self.tiles)
        else:
            width = TILE_SIZE * len(self.tiles)
            height = TILE_SIZE

        self.distance = 0

        self.rect = pygame.Rect(x, y, width, height)
        self.corners = [
            self.rect.topleft,
            self.rect.topright,
            self.rect.bottomright,
            self.rect.bottomleft,
        ]
        self.shapely = geometry.Polygon(self.corners)

        self.image = pygame.Surface((width, height))
        for i, tile in enumerate(self.tiles):
            if vertical:
                self.image.blit(tile.image, (0, i * TILE_SIZE))
            else:
                self.image.blit(tile.image, (i * TILE_SIZE, 0))

        self.mask = pygame.mask.from_surface(self.image)


class Map:
    def __init__(self, path):
        with open(path) as file:
            csv_content = csv.reader(file, delimiter=",")
            self.map = [line for line in csv_content]

        self.image = None
        self.tiles = []
        self.walls = []
        self.inside_walls = []
        self.render_map()

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

    def render_map(self):
        surface = pygame.Surface((len(self.map[0]) * TILE_SIZE, len(self.map) * TILE_SIZE))
        surface.set_colorkey(COLOR["black"])

        found_h_wall = False
        h_wall = []

        v_walls = []

        for i, line in enumerate(self.map):
            for j, tile in enumerate(line):
                if tile != NOT_EXISTS:
                    image = pygame.image.load(
                        f"{TILES_PATH}tile_{tile}.png"
                    ).convert_alpha()
                    surface.blit(image, (j * TILE_SIZE, i * TILE_SIZE))

                    tile_object = Tile(image, pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    self.tiles.append(tile_object)

                    if tile in ["0", "1", "2"]:
                        if tile == "0":
                            found_h_wall = True

                        if found_h_wall:
                            h_wall.append(tile_object)

                        if tile == "2":
                            found_h_wall = False
                            self.walls.append(Wall(h_wall))
                            if i != 0 and i != 17:
                                self.inside_walls.append(Wall(h_wall))
                            h_wall.clear()

                    if tile in ["3", "4", "5"]:
                        if tile == "3":
                            v_walls.append([j, tile_object])

                        if tile == "4":
                            for w in v_walls:
                                if w[0] == j:
                                    w.append(tile_object)
                                    break

                        if tile == "5":
                            for w in v_walls:
                                if w[0] == j:
                                    w.append(tile_object)
                                    self.walls.append(Wall(w[1:], True))
                                    if w[0] != 0 and w[0] != 31:
                                        self.inside_walls.append(Wall(w[1:], True))
                                    v_walls.remove(w)
                                    break

                    if tile == "6":
                        self.walls.append(Wall([tile_object]))
                        if i != 0 and i != 17 and j != 0 and j != 31:
                            self.inside_walls.append(Wall([tile_object]))

        self.image = surface
