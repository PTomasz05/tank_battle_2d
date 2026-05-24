import random
import pygame

from settings import WIDTH, HEIGHT, PLAY_AREA
from src.managers.assets import AssetManager
from src.entities.wall import Wall


class GameMap:
    def __init__(self, level=1):
        self.level = level
        self.background = AssetManager.map_image(level)
        self.walls = self.create_walls(level)

        self.player_spawn = self.get_spawn_position(level)

    def get_spawn_position(self, level):
        if level % 3 == 1:
            return (160, 160)
        elif level % 3 == 2:
            return (352, 160)
        else:
            return (224, 544)

    def create_walls(self, level):
        # LEVEL 1
        if level % 3 == 1:
            return [
                Wall(64 * 6, 64 * 1, 64 * 4, 64 * 1, "concrete"),
                Wall(64 * 7, 64 * 5, 64 * 2, 64 * 1, "concrete"),
                Wall(64 * 14, 64 * 3, 64 * 1, 64 * 5, "concrete"),
                Wall(64 * 3, 64 * 3, 64 * 1, 64 * 1, "crate"),
                Wall(64 * 12, 64 * 3, 64 * 1, 64 * 1, "crate"),
                Wall(64 * 3, 64 * 7, 64 * 1, 64 * 1, "crate"),
                Wall(64 * 12, 64 * 7, 64 * 1, 64 * 1, "crate"),
            ]

        # LEVEL 2
        elif level % 3 == 2:
            return [
                Wall(64 * 1, 64 * 1, 64 * 3, 64 * 3, "concrete"),  # Lewy górny róg
                Wall(64 * 13, 64 * 1, 64 * 3, 64 * 3, "concrete"),  # Prawy górny róg
                Wall(64 * 1, 64 * 7, 64 * 3, 64 * 2, "concrete"),  # Lewy dolny róg
                Wall(64 * 13, 64 * 7, 64 * 3, 64 * 2, "concrete"),  # Prawy dolny róg
                Wall(64 * 7, 64 * 5, 64 * 3, 64 * 1, "crate"),  # Środek
            ]

        # LEVEL 3
        else:
            return [
                Wall(64 * 4, 64 * 4, 64 * 2, 64 * 3, "concrete"),
                Wall(64 * 11, 64 * 4, 64 * 2, 64 * 3, "concrete"),

                Wall(64 * 8, 64 * 5, 64 * 2, 64 * 1, "crate"),

                Wall(64 * 4, 64 * 1, 64 * 2, 64 * 1, "crate"),
                Wall(64 * 11, 64 * 1, 64 * 2, 64 * 1, "crate"),
                Wall(64 * 4, 64 * 9, 64 * 2, 64 * 1, "crate"),
                Wall(64 * 11, 64 * 9, 64 * 2, 64 * 1, "crate"),
            ]

    def wall_rects(self):
        return [wall.rect for wall in self.walls]

    def random_spawn_position(self, player_rect, min_distance_from_player=260):
        """Losuje miejsce dla przeciwnika, ale nie na ścianie i nie za blisko gracza."""
        walls = self.wall_rects()

        for _ in range(500):
            x = random.randint(PLAY_AREA.left + 60, PLAY_AREA.right - 60)
            y = random.randint(PLAY_AREA.top + 60, PLAY_AREA.bottom - 60)
            rect = pygame.Rect(x - 30, y - 30, 60, 60)

            if rect.collidelist(walls) != -1:
                continue

            distance = ((rect.centerx - player_rect.centerx) ** 2 + (rect.centery - player_rect.centery) ** 2) ** 0.5
            if distance < min_distance_from_player:
                continue

            return x, y

        # Awaryjny spawn, gdyby losowanie się nie udało.
        return WIDTH - 120, HEIGHT - 120

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        for wall in self.walls:
            wall.draw(surface)
