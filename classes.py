import pygame

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
