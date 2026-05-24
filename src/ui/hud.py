import pygame

from settings import WIDTH, HEIGHT, WHITE, MUTED


class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 24)
        self.font_big = pygame.font.SysFont("arial", 56, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 34, bold=True)

    def draw_hud(self, surface, player, score, level, wave, enemies):
        pygame.draw.rect(surface, (18, 22, 28), (0, 0, WIDTH, 65))          # Górny pasek
        pygame.draw.rect(surface, (18, 22, 28), (0, HEIGHT - 85, WIDTH, 85)) # Dolny pasek

        score_text = self.font_medium.render(f"WYNIK: {score}", True, (240, 240, 240))
        level_text = self.font.render(f"POZIOM: {level}   |   FALA: {wave}/3", True, (200, 210, 220))
        enemy_text = self.font.render(f"PRZECIWNICY: {enemies}", True, (255, 100, 100))

        surface.blit(score_text, (30, 20))
        surface.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 25))
        surface.blit(enemy_text, (WIDTH - enemy_text.get_width() - 30, 25))

        hp_text = self.font.render(f"STAN PANCERZA: {player.hp}/{player.max_hp}", True, (200, 210, 220))
        surface.blit(hp_text, (30, HEIGHT - 75))

        hp_bar_x = 30
        hp_bar_y = HEIGHT - 45
        hp_bar_width = 300
        hp_bar_height = 20
        ratio = max(0, player.hp / player.max_hp)

        pygame.draw.rect(surface, (60, 20, 20), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), border_radius=6)
        pygame.draw.rect(surface, (75, 220, 100), (hp_bar_x, hp_bar_y, int(hp_bar_width * ratio), hp_bar_height), border_radius=6)
        pygame.draw.rect(surface, (100, 110, 120), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 2, border_radius=6)

    def draw_controls(self, surface):
        text = self.font.render(
            "WASD: ruch | Mysz: celowanie | LPM: strzał",
            True,
            MUTED
        )
        surface.blit(text, (WIDTH - text.get_width() - 30, HEIGHT - 40))

    def draw_overlay(self, surface, title, subtitle):
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 155))
        surface.blit(shade, (0, 0))

        title_surface = self.font_big.render(title, True, WHITE)
        subtitle_surface = self.font.render(subtitle, True, MUTED)

        surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 75)))
        surface.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 22)))
