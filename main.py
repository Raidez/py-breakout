#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, sys, math
from pygame.locals import *
from utils import *

pygame.init()
root = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(10, 10)

# Affichage texte Win
win = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption('Winner')
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Winner', True, BLACK, WHITE)
textRect = text.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 2)

win.fill(WHITE)
win.blit(text, textRect)

no_bricks = False
done = False

# définition des objets
clock = pygame.time.Clock()
left_wall = Brick(0, 0, 10, HEIGHT, math.inf)
right_wall = Brick(WIDTH-10, 0, 10, HEIGHT, math.inf)
top_wall = Brick(0, 0, WIDTH, 10, math.inf)
pad = Pad(150, 575, 100, 15, WHITE)
ball = Ball(root.get_width() // 2, root.get_height() // 2, 10, WHITE, vy=-1.2, vx=-1.8)

bricks = generation_bricks(10)

def update():
    global done, ball, bricks, no_bricks

    # gestion des événements (bouger la barre, quitter l'appli)
    for event in pygame.event.get():
        if event.type == QUIT: done = True
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and pad.x < right_wall.x - pad.w:
                pad.x += 5
            if event.key == K_LEFT and pad.x > left_wall.w:
                pad.x -= 5
            if event.key == K_UP:
                ball.speed += 0.2
            if event.key == K_DOWN:
                ball.speed -= 0.2
        if event.type == KEYUP and event.key == K_r:
            ball = Ball(root.get_width() // 2, root.get_height() // 2, 10, WHITE, vy=-1.2, vx=-1.8)

    # gestion du mouvement de la balle
    ball.update(left_wall, top_wall, right_wall, pad)

    # on enlève 1 HP à chaque touche
    for index in ball.hitbox.collidelistall(bricks):
        ball.rebound_vertical()
        brick = bricks[index]
        brick.hp -= 1

        if brick.hp <= 0:
            del bricks[index]

    if len(bricks) == 0:
        no_bricks = True


def draw():
    global bricks, no_bricks
    top_wall.draw(root)
    right_wall.draw(root)
    left_wall.draw(root)

    pad.draw(root)
    ball.draw(root)

    for brick in bricks:
        brick.draw(root)

    if no_bricks == True:
        root.blit(win, (0,0))

while not done:
    root.fill(BLACK)
    update()
    draw()
    pygame.display.update()
    clock.tick(60) # permet de bloquer le framerate à 60 images par secondes

pygame.quit()
