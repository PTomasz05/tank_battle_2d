import math
import random
import heapq
import pygame

from settings import WIDTH, HEIGHT, PLAY_AREA
from settings import Settings
from src.entities.tank import Tank
from src.managers.assets import AssetManager


class EnemyTank(Tank):
    def __init__(self, x, y, level=1):
        super().__init__(x, y, AssetManager.enemy_tank(), Settings.ENEMY_MAX_HP + (level - 1) * 8)

        self.speed = Settings.ENEMY_SPEED + (level - 1) * 0.12
        self.damage_value = Settings.ENEMY_DAMAGE + (level - 1) * 2

        # Zmienne nawigacyjne AI
        self.path = []
        self.path_timer = 0
        self.tile_size = 64

    def distance_to(self, player):
        return math.hypot(player.x - self.x, player.y - self.y)

    def line_of_sight(self, player, walls):
        """Sprawdza, czy wróg widzi gracza w linii prostej (do strzału)."""
        steps = 30
        for i in range(steps):
            t = i / steps
            px = self.x + (player.x - self.x) * t
            py = self.y + (player.y - self.y) * t
            probe = pygame.Rect(px - 3, py - 3, 6, 6)

            if probe.collidelist(walls) != -1:
                return False
        return True

    def get_grid_pos(self, x, y):
        """Konwertuje piksele na współrzędne siatki (kolumna, wiersz)."""
        return int(x // self.tile_size), int(y // self.tile_size)

    def get_world_pos(self, gx, gy):
        """Konwertuje współrzędne siatki z powrotem na środek kafelka w pikselach."""
        return gx * self.tile_size + (self.tile_size // 2), gy * self.tile_size + (self.tile_size // 2)

    def is_walkable(self, gx, gy, walls):
        """Sprawdza, czy dany kafelek na siatce nie jest zablokowany ścianą."""
        rect = pygame.Rect(gx * self.tile_size + 6, gy * self.tile_size + 6, 52, 52)

        if rect.left < PLAY_AREA.left or rect.right > PLAY_AREA.right:
            return False
        if rect.top < PLAY_AREA.top or rect.bottom > PLAY_AREA.bottom:
            return False

        return rect.collidelist(walls) == -1

    def a_star(self, start, goal, walls):
        """Algorytm A* znajdujący najkrótszą ścieżkę na gridzie."""
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_node = (current[0] + dx, current[1] + dy)

                if not self.is_walkable(next_node[0], next_node[1], walls):
                    continue

                new_cost = cost_so_far[current] + 1

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + abs(goal[0] - next_node[0]) + abs(goal[1] - next_node[1])
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        if goal not in came_from:
            return []

        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def update_ai(self, player, walls, bullets):
        if not self.alive:
            return

        distance = self.distance_to(player)
        has_view = self.line_of_sight(player, walls)

        if has_view and distance < 280:
            self.angle = math.atan2(player.y - self.y, player.x - self.x)

            if distance > 150:
                self.x += math.cos(self.angle) * self.speed * 0.7
                self.y += math.sin(self.angle) * self.speed * 0.7

        else:
            self.path_timer -= 1

            if self.path_timer <= 0 or not self.path:
                start_grid = self.get_grid_pos(self.x, self.y)
                goal_grid = self.get_grid_pos(player.x, player.y)
                self.path = self.a_star(start_grid, goal_grid, walls)
                self.path_timer = 30

            if self.path:
                target_grid = self.path[0]
                target_x, target_y = self.get_world_pos(target_grid[0], target_grid[1])

                self.angle = math.atan2(target_y - self.y, target_x - self.x)
                self.x += math.cos(self.angle) * self.speed
                self.y += math.sin(self.angle) * self.speed

                if math.hypot(target_x - self.x, target_y - self.y) < self.speed * 2:
                    self.path.pop(0)

        if distance < Settings.ENEMY_VIEW_DISTANCE and has_view:
            self.angle = math.atan2(player.y - self.y, player.x - self.x)
            self.shoot(
                bullets,
                "enemy",
                self.damage_value,
                Settings.ENEMY_COOLDOWN
            )