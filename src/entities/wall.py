import pygame
from settings import WALL, WALL_LIGHT


class Wall:
    def __init__(self, x, y, width, height, kind="concrete"):
        self.rect = pygame.Rect(x, y, width, height)
        self.kind = kind

    def draw(self, surface):
        if self.kind == "crate":
            base = (115, 80, 45)
            light = (170, 120, 70)
        else:
            base = WALL
            light = WALL_LIGHT

        pygame.draw.rect(surface, base, self.rect, border_radius=7)
        pygame.draw.rect(surface, light, self.rect, 2, border_radius=7)

        if self.kind == "crate":
            pygame.draw.line(surface, light, self.rect.topleft, self.rect.bottomright, 3)
            pygame.draw.line(surface, light, self.rect.topright, self.rect.bottomleft, 3)
        else:
            for offset in range(18, max(self.rect.width, self.rect.height), 52):
                start = (self.rect.x + min(offset, self.rect.width - 8), self.rect.y + 8)
                end = (self.rect.x + min(offset + 12, self.rect.width - 8), self.rect.y + self.rect.height - 8)
                pygame.draw.line(surface, (52, 57, 66), start, end, 2)
