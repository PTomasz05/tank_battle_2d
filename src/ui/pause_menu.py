import pygame

from settings import WIDTH, HEIGHT,WHITE,MUTED
from src.ui.button import Button

class PauseMenu:
    def __init__(self, font, font_big, font_medium):
        self.font = font
        self.font_big = font_big
        self.font_medium = font_medium
        self.font_title = pygame.font.SysFont("arial", 42, bold=True)
        self.active_tab = "main"

        center_x = WIDTH // 2

        self.resume_button = Button(center_x - 140, 250, 280, 55, "RESUME", font_medium)
        self.upgrades_button = Button(center_x - 140, 320, 280, 55, "UPGRADES", font_medium)
        self.new_game_button = Button(center_x - 140, 390, 280, 55, "NEW GAME", font_medium)
        self.quit_button = Button(center_x - 140, 460, 280, 55, "QUIT GAME", font_medium)

        self.back_button = Button(40, HEIGHT - 90, 180, 50, "BACK", font_medium)
        self.fullscreen_button = Button(center_x - 200, 300, 420, 55, "TOGGLE FULLSCREEN", font_medium)

        self.upg_damage_btn = Button(center_x - 255, 250, 510, 50, "SIŁA OGNIA (+10) | 500 PKT", font_medium)
        self.upg_hp_btn = Button(center_x - 255, 320, 510, 50, "PANCERZ MAX (+25) | 500 PKT", font_medium)
        self.upg_speed_btn = Button(center_x - 255, 390, 510, 50, "SZYBKOŚĆ RUCHU | 500 PKT", font_medium)
        self.upg_cooldown_btn = Button(center_x - 255, 460, 510, 50, "PRZEŁADOWANIE | 500 PKT", font_medium)

    def reset_to_main(self):
        self.active_tab = "main"

    def draw_background(self, surface):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 260, 100, 520, 530)
        pygame.draw.rect(surface, (18, 22, 30), panel, border_radius=22)
        pygame.draw.rect(surface, (80, 95, 120), panel, 2, border_radius=22)

    def draw_title(self, surface, title, subtitle=None):
        title_surface = self.font_title.render(title, True, WHITE)
        surface.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 150)))

        if subtitle:
            subtitle_surface = self.font.render(subtitle, True, MUTED)
            surface.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, 200)))

    def draw_main(self, surface):
        self.draw_background(surface)
        self.draw_title(surface, "PAUSE MENU", "ESC - return to game")

        self.resume_button.draw(surface)
        self.upgrades_button.draw(surface)
        self.new_game_button.draw(surface)
        self.quit_button.draw(surface)

    def draw_settings(self, surface, fullscreen):
        self.draw_background(surface)
        self.draw_title(surface, "SETTINGS")

        mode_text = "ON" if fullscreen else "OFF"
        fullscreen_text = self.font.render(f"Fullscreen: {mode_text}", True, WHITE)
        resolution_text = self.font.render("Resolution: 1100x700", True, MUTED)

        surface.blit(fullscreen_text, fullscreen_text.get_rect(center=(WIDTH // 2, 245)))
        surface.blit(resolution_text, resolution_text.get_rect(center=(WIDTH // 2, 380)))

        self.fullscreen_button.draw(surface)
        self.back_button.draw(surface)

    def draw_upgrades(self, surface, score):
        self.draw_background(surface)
        self.draw_title(surface, "ULEPSZENIA CZOŁGU", f"DOSTĘPNE PUNKTY: {score}")

        self.upg_damage_btn.draw(surface)
        self.upg_hp_btn.draw(surface)
        self.upg_speed_btn.draw(surface)
        self.upg_cooldown_btn.draw(surface)

        self.back_button.draw(surface)

    def draw(self, surface, fullscreen, score):
        if self.active_tab == "main":
            self.draw_main(surface)
        elif self.active_tab == "settings":
            self.draw_settings(surface, fullscreen)
        elif self.active_tab == "upgrades":
            self.draw_upgrades(surface, score)

    def draw(self, surface, fullscreen, upgrade_points):
        if self.active_tab == "main":
            self.draw_main(surface)
        elif self.active_tab == "settings":
            self.draw_settings(surface, fullscreen)
        elif self.active_tab == "upgrades":
            self.draw_upgrades(surface, upgrade_points)