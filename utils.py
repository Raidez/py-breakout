#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, math

WIDTH = 400
HEIGHT = 600

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
        self.hitbox = pygame.Rect(cx, cy, radius, radius)
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy
        self.speed = speed

    def update(self, left_wall, top_wall, right_wall, pad):
        # déplacer la balle et sa hitbox à sa nouvelle position
        self.cx += self.vx * self.speed
        self.cy += self.vy * self.speed
        self.hitbox.x = int(self.cx)
        self.hitbox.y = int(self.cy)

        # faire rebondir la contre les murs
        if (self.cx - self.radius) < (left_wall.x + left_wall.w) or (self.cx + self.radius) >= right_wall.x:
            self.rebound_horizontal()
        if (self.cy - self.radius) < (top_wall.y + top_wall.h):
            self.rebound_vertical()

        # faire rebondir la balle contre la barre
        if self.hitbox.colliderect(pad):
            self.rebound_vertical()

    def draw(self, screen):
        position = (int(self.cx), int(self.cy))
        pygame.draw.circle(screen, self.color, position, self.radius)

    def rebound_vertical(self):
        self.vy = -self.vy

    def rebound_horizontal(self):
        self.vx = -self.vx

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
