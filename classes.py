import pygame

class Brick:
    def __init__(self, x, y, w, h, color, hp):
        self.pos = pygame.Rect(x, y, w, h)
        self.color = color
        self.hpMax = hp
        self.hp = hp

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.pos)


class Pad:
    def __init__(self, x, y, w, h, color):
        self.pos = pygame.Rect(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.pos)
