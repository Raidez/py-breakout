#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, math

WIDTH = 400
HEIGHT = 600
FPS_CAP = 60

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
DEFAULT_COLORS = (GREEN, ORANGE, PINK, YELLOW, BLUE, RED)

def draw_text(surface, text, size, color, x, y, align="nw"):
    font_name = pygame.font.match_font('hack')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw": text_rect.topleft = (x, y)
    if align == "ne": text_rect.topright = (x, y)
    if align == "sw": text_rect.bottomleft = (x, y)
    if align == "se": text_rect.bottomright = (x, y)
    if align == "n": text_rect.midtop = (x, y)
    if align == "s": text_rect.midbottom = (x, y)
    if align == "e": text_rect.midright = (x, y)
    if align == "w": text_rect.midleft = (x, y)
    if align == "center": text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

class Brick(pygame.Rect):
    def __init__(self, x, y, w, h, hp):
        super().__init__(x, y, w, h)
        self.hpMax = hp
        self.hp = hp

    def draw(self, screen):
        """la couleur de la brique dépend de ses points de vie
        (exception pour les murs)"""
        color = BLACK
        if self.hp == math.inf:
            color = BLUE
            pygame.draw.rect(screen, color, self)
        elif self.hp > 0 and self.hp <= len(DEFAULT_COLORS):
            color = DEFAULT_COLORS[self.hp-1]
            pygame.draw.rect(screen, color, self)
            pygame.draw.rect(screen, GREY, self, 2)
        elif self.hp > len(DEFAULT_COLORS):
            color = WHITE
            pygame.draw.rect(screen, color, self)
            pygame.draw.rect(screen, GREY, self, 2)

class Pad(pygame.Rect):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)

class Ball:
    def __init__(self, cx, cy, radius, color, vx=1.0, vy=1.0, speed=1.0):
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

    def update(self, delta):
        # déplacer la hitbox à sa nouvelle position
        self.dx += self.vx * self.speed * delta
        self.dy += self.vy * self.speed * delta

    def move(self):
        # déplacer la position de la balle en pixel
        self.cx = int(self.dx)
        self.cy = int(self.dy)

    def collide(self, rect : pygame.Rect, delta : float):
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

        # vérifier s'il y'aura collision
        has_collide = ""
        if bottom <= rect.top: has_collide = "t"
        if top >= rect.bottom: has_collide = "b"
        if left >= rect.right: has_collide += "r"
        if right <= rect.left: has_collide += "l"
        has_collide = len(has_collide) == 0

        return (has_collide, collide_dir)

    def draw(self, screen):
        position = (self.cx, self.cy)
        pygame.draw.circle(screen, self.color, position, self.radius)

    def rebound_vertical(self):
        self.vy = -self.vy

    def rebound_horizontal(self):
        self.vx = -self.vx

    def rebound(self, has_collide, collide_dir):
        if has_collide and len(collide_dir):
            if 'l' in collide_dir or 'r' in collide_dir :
                self.rebound_horizontal()
            if 't' in collide_dir or 'b' in collide_dir :
                self.rebound_vertical()

def generation_bricks(number_row):
    bricks = []
    rows = number_row +1
    col = int((WIDTH) / 50)+1
    for h in range(1, rows):
        # remplissage des briques
        height = 20 * h
        for w in range(1, col):
            width = 40 * w
            bricks.append(Brick(width, height, 40, 20, rows-h))

    return bricks
