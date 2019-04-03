#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

WIDTH = 400
HEIGHT = 400
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

class Ball:
    def __init__(self, x, y, r):
        self.color = WHITE

        # position hitbox
        self.dx = x
        self.dy = y
        self.r = r

        # position réelle (pixel)
        self.x = int(self.dx)
        self.y = int(self.dy)

        # vecteur et accélération
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 1.0

    def collide(self, rect : pygame.Rect):
        top = self.dy - self.r
        bottom = self.dy + self.r
        left = self.dx - self.r
        right = self.dx + self.r

        dir = ""
        if bottom < rect.top: dir = "t"
        if top > rect.bottom: dir = "b"
        if left > rect.right: dir += "r"
        if right < rect.left: dir += "l"
        return dir

    def update(self):
        # calcul de la nouvelle destination
        self.dx += self.vx * self.speed
        self.dy += self.vy * self.speed

        # rebond contre mur horizontal
        if self.dx + self.r > WIDTH:
            self.dx -= 1
            self.vx = -ball.vx
        if self.dx - self.r <= 0:
            self.dx += 1
            self.vx = -self.vx
        # rebond contre mur vertical
        if self.dy + self.r > HEIGHT:
            self.dy -= 1
            self.vy = -self.vy
        if self.dy - self.r <= 0:
            self.dy += 1
            self.vy = -self.vy

    def move(self):
        self.x = int(self.dx)
        self.y = int(self.dy)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)

pygame.init()
pygame.key.set_repeat(20, 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
ball = Ball(WIDTH / 4 * 3, HEIGHT / 4 * 3, 10)
ball.vx = 1.0
ball.vy = 1.0
ball.color = GREEN
ball.collisions_dir = ""
ball.has_collisions = False
rect = pygame.Rect(WIDTH / 2 - 25, HEIGHT / 2 - 25, 50, 50)

done = False
while not done:
    # UPDATE
    clock.tick(FPS_CAP) # permet de bloquer le framerate
    for event in pygame.event.get():
        if event.type == QUIT: done = True
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                ball.vx -= 0.2
            if event.key == K_RIGHT:
                ball.vx += 0.2
            if event.key == K_UP:
                ball.vy -= 0.2
            if event.key == K_DOWN:
                ball.vy += 0.2


    ball.collisions_dir = ball.collide(rect)
    ball.update() # mise à jour de la position de la ball
    ball.has_collisions = len(ball.collide(rect)) == 0
    if ball.has_collisions and len(ball.collisions_dir) > 0:
        if 'l' in ball.collisions_dir or 'r' in ball.collisions_dir :
            ball.vx = -ball.vx
            ball.color = RED
        if 't' in ball.collisions_dir  or 'b' in ball.collisions_dir :
            ball.vy = -ball.vy
            ball.color = RED
    else:
        ball.color = GREEN

    ball.move() # déplacement effectif de la balle

    # DRAW
    screen.fill(BLACK)
    ball.draw(screen) # affichage de la ball
    pygame.draw.rect(screen, BLUE, rect) # affichage du rectangle
    pygame.display.update()

pygame.quit()
