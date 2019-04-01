import pygame

BLACK = (0, 0, 0)
RED = (125, 0, 0)
WHITE = (255,255,255)
BLUE = (0, 0, 125)

class Brick(pygame.Rect):
    def __init__(self, x, y, w, h, color, hp):
        super().__init__(x, y, w, h)
        self.color = color
        self.hpMax = hp
        self.hp = hp

    def draw(self, screen):
        if self.hp > 0:
            pygame.draw.rect(screen, self.color, self)

class Pad(pygame.Rect):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)

class Ball:
    def __init__(self, cx, cy, radius, color):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.cx, self.cy), self.radius)
