import os
import random
import pygame

from settings import (
    WIDTH, HEIGHT, ASSET_DIR, PLAY_AREA,
    DARK_BG, GROUND, ROAD, GREEN, GREEN_DARK, RED, RED_DARK
)


class AssetManager:

    @staticmethod
    def load_image(filename, size=None):
        path = os.path.join(ASSET_DIR, filename)

        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            if size is not None:
                image = pygame.transform.smoothscale(image, size)
            return image

        return None

    @staticmethod
    def create_tank_sprite(body_color, dark_color):
        surf = pygame.Surface((96, 96), pygame.SRCALPHA)

        pygame.draw.ellipse(surf, (0, 0, 0, 75), (16, 62, 66, 18))

        pygame.draw.rect(surf, dark_color, (18, 20, 18, 56), border_radius=9)
        pygame.draw.rect(surf, dark_color, (60, 20, 18, 56), border_radius=9)

        for y in range(25, 72, 10):
            pygame.draw.line(surf, (12, 14, 16), (21, y), (34, y + 4), 3)
            pygame.draw.line(surf, (12, 14, 16), (63, y + 4), (76, y), 3)

        pygame.draw.rect(surf, body_color, (28, 24, 40, 48), border_radius=12)
        pygame.draw.rect(surf, dark_color, (33, 29, 30, 38), 3, border_radius=9)

        pygame.draw.rect(surf, (82, 86, 92), (48, 43, 38, 10), border_radius=5)
        pygame.draw.circle(surf, (105, 111, 120), (48, 48), 17)
        pygame.draw.circle(surf, body_color, (48, 48), 12)

        return surf

    @staticmethod
    def create_background(level=1):
        surf = pygame.Surface((WIDTH, HEIGHT))

        # Mapowanie zakrętów
        tile_map = {
            '-': 'tileGrass_roadEast.png',
            '|': 'tileGrass_roadNorth.png',
            '1': 'tileGrass_roadCornerLR.png',
            '2': 'tileGrass_roadCornerLL.png',
            '3': 'tileGrass_roadCornerUR.png',
            '4': 'tileGrass_roadCornerUL.png',
            '+': 'tileGrass_roadCrossing.png',
            'T': 'tileGrass_roadSplitN.png',
            'E': 'tileGrass_roadSplitE.png'
        }

        TILE_SIZE = 64
        loaded_tiles = {}
        for symbol, filename in tile_map.items():
            img = AssetManager.load_image(filename, (TILE_SIZE, TILE_SIZE))
            if img:
                loaded_tiles[symbol] = img

        if '-' in loaded_tiles:
            perfect_grass_color = loaded_tiles['-'].get_at((2, 2))
        else:
            perfect_grass_color = (103, 175, 50)  # Zapasowy kolor w razie błędu

        surf.fill(perfect_grass_color)

        if level % 3 == 1:
            layout = [
                "                 ",
                "                 ",
                "  1----------2   ",
                "  |          |   ",
                "  |  1----2  |   ",
                "  |  |    |  |   ",
                "  |  3----4  |   ",
                "  |          |   ",
                "  3----------4   ",
                "                 ",
                "                 "
            ]
        elif level % 3 == 2:
            layout = [
                "                 ",
                "                 ",
                "     1----2      ",
                "     |    |      ",
                "  1--+----+--2   ",
                "  |  |    |  |   ",
                "  3--+----+--4   ",
                "     |    |      ",
                "     3----4      ",
                "                 ",
                "                 "
            ]
        else:
            layout = [
                "                 ",
                "                 ",
                "  1----2  1----2 ",
                "  |    |  |    | ",
                "  |    3--4    | ",
                "  |            | ",
                "  |    1--2    | ",
                "  |    |  |    | ",
                "  3----4  3----4 ",
                "                 ",
                "                 "
            ]

        for row_idx, row_str in enumerate(layout):
            for col_idx, symbol in enumerate(row_str):
                if symbol in loaded_tiles:
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    surf.blit(loaded_tiles[symbol], (x, y))

        pygame.draw.rect(surf, (40, 50, 60), PLAY_AREA, 4, border_radius=12)

        return surf

    @staticmethod
    def player_tank():
        image = AssetManager.load_image("player_tank.png", (96, 96))
        return image if image else AssetManager.create_tank_sprite(GREEN, GREEN_DARK)

    @staticmethod
    def enemy_tank():
        image = AssetManager.load_image("enemy_tank.png", (96, 96))
        return image if image else AssetManager.create_tank_sprite(RED, RED_DARK)

    @staticmethod
    def map_image(level):
        if level == 1:
            image = AssetManager.load_image("map.png", (WIDTH, HEIGHT))
            if image:
                return image

        return AssetManager.create_background(level)
