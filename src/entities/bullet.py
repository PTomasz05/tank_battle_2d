import math
import pygame

from settings import PLAY_AREA, YELLOW
from settings import Settings


class Bullet:
    def __init__(self, x, y, angle, owner, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.owner = owner
        self.damage = damage
        self.speed = Settings.BULLET_SPEED
        self.radius = Settings.BULLET_RADIUS
        self.bounces_left = Settings.BULLET_BOUNCES
        self.active = True

    def rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def bounce_from_rect(self, obstacle):
        previous_x = self.x - math.cos(self.angle) * self.speed
        previous_y = self.y - math.sin(self.angle) * self.speed

        came_from_left = previous_x < obstacle.left
        came_from_right = previous_x > obstacle.right
        came_from_top = previous_y < obstacle.top
        came_from_bottom = previous_y > obstacle.bottom

        if came_from_left or came_from_right:
            self.angle = math.pi - self.angle
        elif came_from_top or came_from_bottom:
            self.angle = -self.angle
        else:
            self.angle += math.pi

        self.bounces_left -= 1
        self.x += math.cos(self.angle) * self.speed * 1.5
        self.y += math.sin(self.angle) * self.speed * 1.5

        if self.bounces_left < 0:
            self.active = False

    def update(self, walls):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        if self.x <= PLAY_AREA.left or self.x >= PLAY_AREA.right:
            self.angle = math.pi - self.angle
            self.bounces_left -= 1

        if self.y <= PLAY_AREA.top or self.y >= PLAY_AREA.bottom:
            self.angle = -self.angle
            self.bounces_left -= 1

        self.x = max(PLAY_AREA.left + 2, min(PLAY_AREA.right - 2, self.x))
        self.y = max(PLAY_AREA.top + 2, min(PLAY_AREA.bottom - 2, self.y))

        for wall in walls:
            if self.rect().colliderect(wall):
                self.bounce_from_rect(wall)
                break

        if self.bounces_left < 0:
            self.active = False

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 245, 160), (int(self.x), int(self.y)), self.radius + 2)
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), self.radius)
