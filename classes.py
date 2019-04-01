import pygame

class Brick:
    def __init__(self, x, y, w, h, color, hp):
        self.pos = pygame.Rect(x, y, w, h)
        self.color = color
        self.hpMax = hp
        self.hp = hp

    @property
    def x(self):
        return self.pos.left

    @x.setter
    def x(self, x):
        self.pos = self.pos.move(x, self.y)

    @property
    def y(self):
        return self.pos.top

    @y.setter
    def y(self, y):
        self.pos = self.pos.move(self.x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.pos)
