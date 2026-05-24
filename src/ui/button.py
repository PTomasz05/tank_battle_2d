import pygame
from settings import WHITE


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

    def draw(self, surface):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = (65, 150, 85) if hover else (48, 112, 66)

        pygame.draw.rect(surface, color, self.rect, border_radius=14)
        pygame.draw.rect(surface, (132, 230, 150), self.rect, 3, border_radius=14)

        text = self.font.render(self.text, True, WHITE)
        surface.blit(text, text.get_rect(center=self.rect.center))
