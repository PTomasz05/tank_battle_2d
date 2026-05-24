import pygame

from settings import WIDTH, HEIGHT, FPS
from settings import Settings
from src.ui.button import Button
from src.entities.enemy import EnemyTank
from src.core.game_map import GameMap
from src.entities.particle import Particle
from src.entities.tank import PlayerTank
from src.ui.hud import UI
from src.ui.pause_menu import PauseMenu


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tank Battle 2D")
        self.clock = pygame.time.Clock()

        self.ui = UI()
        self.fullscreen = False
        self.upgrade_points = 0
        self.font_big = pygame.font.SysFont("arial", 56, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 34, bold=True)
        self.font = pygame.font.SysFont("arial", 24)
        self.pause_menu = PauseMenu(self.font, self.font_big, self.font_medium)

        self.state = "menu"

        self.level = 1
        self.wave = 1
        self.score = 0

        self.game_map = GameMap(self.level)
        self.game_map = GameMap(self.level)

        spawn_x, spawn_y = self.game_map.player_spawn
        self.player = PlayerTank(spawn_x, spawn_y)
        self.bullets = []
        self.enemies = []
        self.particles = []

        self.start_button = Button(WIDTH // 2 - 135, HEIGHT // 2 + 45, 270, 64, "START GAME", self.font_medium)
        self.next_level_button = Button(WIDTH // 2 - 140, HEIGHT // 2 + 45, 280, 64, "NEXT LEVEL", self.font_medium)
        self.restart_button = Button(WIDTH // 2 - 140, HEIGHT // 2 + 45, 280, 64, "RESTART", self.font_medium)

    def start_new_game(self):
        self.state = "playing"
        self.level = 1
        self.wave = 1
        self.score = 0

        self.game_map = GameMap(self.level)
        self.game_map = GameMap(self.level)

        spawn_x, spawn_y = self.game_map.player_spawn
        self.player = PlayerTank(spawn_x, spawn_y)
        self.bullets.clear()
        self.particles.clear()
        self.spawn_wave()

    def start_next_level(self):
        self.state = "playing"
        self.level += 1
        self.wave = 1

        def toggle_fullscreen(self):
            self.fullscreen = not self.fullscreen

            if self.fullscreen:
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.game_map = GameMap(self.level)

        spawn_x, spawn_y = self.game_map.player_spawn
        self.player.x = spawn_x
        self.player.y = spawn_y
        self.player.heal_full()

        self.bullets.clear()
        self.particles.clear()
        self.spawn_wave()

    def spawn_wave(self):
        self.enemies.clear()

        enemy_count = min(2 + self.wave + self.level - 1, Settings.MAX_ENEMIES_PER_WAVE)

        for _ in range(enemy_count):
            x, y = self.game_map.random_spawn_position(self.player.rect())
            self.enemies.append(EnemyTank(x, y, self.level))

    def create_explosion(self, x, y, amount=22):
        for _ in range(amount):
            self.particles.append(Particle(x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.state == "playing":
                    self.state = "paused"
                    self.pause_menu.reset_to_main()
                elif self.state == "paused":
                    if self.pause_menu.active_tab == "main":
                        self.state = "playing"
                    else:
                        self.pause_menu.active_tab = "main"

            if self.state == "menu":
                if self.start_button.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    self.start_new_game()

            elif self.state == "level_completed":
                if self.next_level_button.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    self.start_next_level()

            elif self.state == "game_over":
                if self.restart_button.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    self.start_new_game()

            elif self.state == "paused":
                if self.pause_menu.active_tab == "main":
                    if self.pause_menu.resume_button.clicked(event):
                        self.state = "playing"

                    elif self.pause_menu.upgrades_button.clicked(event):
                        self.pause_menu.active_tab = "upgrades"

                    elif self.pause_menu.new_game_button.clicked(event):
                        self.start_new_game()

                    elif self.pause_menu.quit_button.clicked(event):
                        return False

                elif self.pause_menu.active_tab == "settings":
                    if self.pause_menu.back_button.clicked(event):
                        self.pause_menu.active_tab = "main"

                    elif self.pause_menu.fullscreen_button.clicked(event):
                        self.toggle_fullscreen()


                elif self.pause_menu.active_tab == "upgrades":

                    if self.pause_menu.back_button.clicked(event):

                        self.pause_menu.active_tab = "main"



                    elif self.pause_menu.upg_damage_btn.clicked(event) and self.score >= 500:

                        self.score -= 500

                        self.player.damage += 10


                    elif self.pause_menu.upg_hp_btn.clicked(event) and self.score >= 500:

                        self.score -= 500

                        self.player.max_hp += 25

                        self.player.hp += 25


                    elif self.pause_menu.upg_speed_btn.clicked(event) and self.score >= 500:

                        self.score -= 500

                        self.player.speed += 0.4


                    elif self.pause_menu.upg_cooldown_btn.clicked(event) and self.score >= 500:

                        if self.player.cooldown >= 200:
                            self.score -= 500

                            self.player.cooldown -= 100

        return True

    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        walls = self.game_map.wall_rects()

        self.player.move(keys, walls)
        self.player.update_angle()

        if keys[pygame.K_SPACE] or mouse_pressed[0]:
            self.player.shoot(self.bullets, "player", self.player.damage, self.player.cooldown)

        for enemy in self.enemies:
            enemy.update_ai(self.player, walls, self.bullets)

        for bullet in self.bullets:
            bullet.update(walls)

        self.handle_collisions()

        self.bullets = [bullet for bullet in self.bullets if bullet.active]
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]

        for particle in self.particles:
            particle.update()

        self.particles = [particle for particle in self.particles if particle.life > 0]

        if not self.player.alive:
            self.state = "game_over"

        if len(self.enemies) == 0:
            self.advance_wave_or_finish_level()

    def advance_wave_or_finish_level(self):
        if self.wave >= Settings.WAVES_PER_LEVEL:
            self.player.heal_full()
            self.state = "level_completed"
        else:
            self.wave += 1
            self.player.heal_full()
            self.spawn_wave()

    def handle_collisions(self):
        for bullet in self.bullets:
            if not bullet.active:
                continue

            if bullet.owner == "player":
                for enemy in self.enemies:
                    if enemy.alive and bullet.rect().colliderect(enemy.rect()):
                        enemy.take_damage(bullet.damage)
                        bullet.active = False
                        self.create_explosion(bullet.x, bullet.y, 14)

                        if not enemy.alive:
                            self.score += 100
                            self.create_explosion(enemy.x, enemy.y, 34)

                        break

            elif bullet.owner == "enemy":
                if self.player.alive and bullet.rect().colliderect(self.player.rect()):
                    self.player.take_damage(bullet.damage)
                    bullet.active = False
                    self.create_explosion(bullet.x, bullet.y, 14)

    def draw_world(self):
        self.game_map.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        if self.player.alive:
            self.player.draw(self.screen)

        for particle in self.particles:
            particle.draw(self.screen)

        self.ui.draw_hud(self.screen, self.player, self.score, self.level, self.wave, len(self.enemies))
        self.ui.draw_controls(self.screen)

    def draw_menu(self):
        self.game_map.draw(self.screen)

        title = self.font_big.render("TANK BATTLE 2D", True, (240, 240, 240))
        subtitle = self.font.render("Python + Pygame | OOP | enemy AI | random spawns | levels", True, (175, 184, 194))

        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 238)))

        self.start_button.draw(self.screen)

    def draw_level_completed(self):
        self.draw_world()
        self.ui.draw_overlay(
            self.screen,
            "LEVEL COMPLETED",
            f"Level {self.level} ukończony! HP odnowione. ENTER albo NEXT LEVEL"
        )
        self.next_level_button.draw(self.screen)

    def draw_game_over(self):
        self.draw_world()
        self.ui.draw_overlay(
            self.screen,
            "GAME OVER",
            f"Score: {self.score} | Level: {self.level} | Wave: {self.wave}/3"
        )
        self.restart_button.draw(self.screen)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_world()
        elif self.state == "paused":
            self.draw_world()
            self.pause_menu.draw(self.screen, self.fullscreen, self.score)
        elif self.state == "level_completed":
            self.draw_level_completed()
        elif self.state == "game_over":
            self.draw_game_over()

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

        pygame.quit()
