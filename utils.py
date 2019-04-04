#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, math

WIDTH = 400
HEIGHT_WINDOW = 650
HEIGHT = 600
FPS_CAP = 60

class Color:
    BLACK = (0, 0, 0)
    GREY = (125, 125, 125)
    RED = (255, 0, 0)
    WHITE = (255,255,255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255,255,0)
    ORANGE = (255,165,0)
    PINK = (255,20,147)

# couleurs par défaut de la coloration selon les PV d'une brique
# VERT -> 1 PV; ROUGE -> max PV
DEFAULT_COLORS = (Color.GREEN, Color.ORANGE, Color.PINK, Color.YELLOW, Color.BLUE, Color.RED)

class Brick(pygame.Rect):
    def __init__(self, x: int, y: int, w: int, h: int, hp: int):
        super().__init__(x, y, w, h)
        self.hpMax = hp
        self.hp = hp

    def draw(self, surface: pygame.Surface):
        """la couleur de la brique dépend de ses points de vie
        (exception pour les murs)"""
        color = Color.WHITE
        if self.hp == math.inf:
            pygame.draw.rect(surface, Color.BLUE, self)
        else:
            if self.hp > 0 and self.hp <= len(DEFAULT_COLORS):
                color = DEFAULT_COLORS[self.hp-1]

            pygame.draw.rect(surface, color, self)
            pygame.draw.rect(surface, Color.GREY, self, 2)

class Pad(pygame.Rect):
    def __init__(self, x: int, y: int, w: int, h: int, color: Color):
        super().__init__(x, y, w, h)
        self.color = color

    def draw(self, surface : pygame.Surface):
        pygame.draw.rect(surface, self.color, self)

class Ball:
    def __init__(self, cx: int, cy: int, radius: int, color: Color, vx: int = 1.0, vy: int = 1.0, speed: int = 1.0):
        # position hitbox
        self.dx = cx
        self.dy = cy

        # position réelle (pixel)
        self.cx = int(cx)
        self.cy = int(cy)

        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy
        self.speed = speed

    def update(self, delta: float):
        # déplacer la hitbox à sa nouvelle position
        self.dx += self.vx * self.speed * delta
        self.dy += self.vy * self.speed * delta

    def move(self):
        # déplacer la position de la balle en pixel
        self.cx = int(self.dx)
        self.cy = int(self.dy)

    def collide(self, rect: pygame.Rect, delta: float):
        # récupérer la position de la balle par rapport à l'objet
        left = self.cx - self.radius
        top = self.cy - self.radius
        right = self.cx + self.radius
        bottom = self.cy + self.radius

        collide_dir = ""
        if bottom <= rect.top: collide_dir = "t"
        if top >= rect.bottom: collide_dir = "b"
        if left >= rect.right: collide_dir += "r"
        if right <= rect.left: collide_dir += "l"

        # simuler le déplacement de la balle
        dx = self.dx + self.vx * self.speed * delta
        dy = self.dy + self.vy * self.speed * delta
        left = dx - self.radius
        top = dy - self.radius
        right = dx + self.radius
        bottom = dy + self.radius

        # prévoir s'il y'aura une collision
        has_collide = ""
        if bottom <= rect.top: has_collide = "t"
        if top >= rect.bottom: has_collide = "b"
        if left >= rect.right: has_collide += "r"
        if right <= rect.left: has_collide += "l"
        has_collide = len(has_collide) == 0

        return (has_collide, collide_dir)

    def draw(self, surface: pygame.Surface):
        position = (self.cx, self.cy)
        pygame.draw.circle(surface, self.color, position, self.radius)

    def rebound_vertical(self):
        self.vy = -self.vy

    def rebound_horizontal(self):
        self.vx = -self.vx

    def rebound(self, has_collide: bool, collide_dir: str):
        if has_collide and len(collide_dir):
            if 'l' in collide_dir or 'r' in collide_dir :
                self.rebound_horizontal()
            if 't' in collide_dir or 'b' in collide_dir :
                self.rebound_vertical()

def generation_bricks(number_row: int = 1):
    """ Génère une liste de briques sur X lignes """
    bricks = []
    rows = number_row + 1
    col = WIDTH // 40 - 1
    for h in range(1, rows):
        y = 20 * h
        hp = rows - h
        for w in range(1, col):
            x = 40 * w
            bricks.append(Brick(x, y, 40, 20, hp))

    return bricks
