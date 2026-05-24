import random
import pygame

from settings import YELLOW, ORANGE, RED


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.radius = random.randint(2, 6)
        self.life = random.randint(18, 34)
        self.color = random.choice([YELLOW, ORANGE, RED, (240, 220, 160)])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.radius = max(0, self.radius - 0.08)

    def draw(self, surface):
        if self.life > 0 and self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
