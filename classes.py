import pygame

WIDTH = 400
HEIGHT = 600

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
    def __init__(self, cx, cy, radius, color, vx=1.0, vy=1.0, speed=1.0):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy
        self.speed = speed

    def update(self, left_wall, top_wall, right_wall, pad):
        # faire rebondir la balle contre les murs
        if (self.cx - self.radius) < (left_wall.x + left_wall.w) or (self.cx + self.radius) >= right_wall.x:
            self.rebound_horizontal()
        if (self.cy - self.radius) < (top_wall.y + top_wall.h):
            self.rebound_vertical()

        # DEBUG: a supprimer
        if self.cy >= 600:
            self.rebound_vertical()

        # faire rebondir la balle contre la barre


        # deplacer la balle a sa nouvelle position
        self.cx += self.vx * self.speed
        self.cy += self.vy * self.speed

    def draw(self, screen):
        position = (int(self.cx), int(self.cy))
        pygame.draw.circle(screen, self.color, position, self.radius)

    def rebound_vertical(self):
        self.vy = -self.vy

    def rebound_horizontal(self):
        self.vx = -self.vx
