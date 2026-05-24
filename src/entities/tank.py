import math
import pygame

from settings import PLAY_AREA, BLACK
from settings import Settings
from src.entities.bullet import Bullet
from src.managers.assets import AssetManager


class Tank:
    def __init__(self, x, y, sprite, max_hp):
        self.x = x
        self.y = y
        self.size = 52
        self.angle = 0
        self.sprite = sprite
        self.max_hp = max_hp
        self.hp = max_hp
        self.last_shot = 0
        self.alive = True

    def rect(self):
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )

    def can_shoot(self, cooldown):
        return pygame.time.get_ticks() - self.last_shot >= cooldown

    def shoot(self, bullets, owner, damage, cooldown):
        if not self.can_shoot(cooldown):
            return

        self.last_shot = pygame.time.get_ticks()
        barrel = 44

        bullets.append(
            Bullet(
                self.x + math.cos(self.angle) * barrel,
                self.y + math.sin(self.angle) * barrel,
                self.angle,
                owner,
                damage
            )
        )

    def take_damage(self, amount):
        self.hp -= amount

        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def heal_full(self):
        self.hp = self.max_hp

    def draw_hp(self, surface):
        width = 58
        height = 7
        x = self.x - width / 2
        y = self.y - 45
        ratio = self.hp / self.max_hp

        pygame.draw.rect(surface, (80, 26, 26), (x, y, width, height), border_radius=4)
        pygame.draw.rect(surface, (80, 230, 105), (x, y, width * ratio, height), border_radius=4)
        pygame.draw.rect(surface, BLACK, (x, y, width, height), 1, border_radius=4)

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.sprite, -math.degrees(self.angle))
        rect = rotated.get_rect(center=(self.x, self.y))

        surface.blit(rotated, rect)
        self.draw_hp(surface)


class PlayerTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, AssetManager.player_tank(), Settings.PLAYER_MAX_HP)
        self.speed = Settings.PLAYER_SPEED

        self.damage = Settings.PLAYER_DAMAGE
        self.cooldown = Settings.PLAYER_COOLDOWN

    def update_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - self.y, mouse_x - self.x)

    def move_axis(self, dx, dy, walls):
        old_x = self.x
        old_y = self.y

        self.x += dx
        self.y += dy

        if self.rect().collidelist(walls) != -1:
            self.x = old_x
            self.y = old_y

        self.x = max(PLAY_AREA.left + 35, min(PLAY_AREA.right - 35, self.x))
        self.y = max(PLAY_AREA.top + 35, min(PLAY_AREA.bottom - 35, self.y))

    def move(self, keys, walls):
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.move_axis(dx, 0, walls)
        self.move_axis(0, dy, walls)
