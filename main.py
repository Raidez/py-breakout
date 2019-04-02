#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, sys, math
from pygame.locals import *
from utils import *

pygame.init()
root = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(10, 10)

# définition des objets
clock = pygame.time.Clock()
left_wall = Brick(0, 0, 10, HEIGHT, math.inf)
right_wall = Brick(WIDTH-10, 0, 10, HEIGHT, math.inf)
top_wall = Brick(0, 0, WIDTH, 10, math.inf)
pad = Pad(150, 575, 100, 15, WHITE)
ball = Ball(root.get_width() // 2, root.get_height() // 2, 10, WHITE, vy=-1.2, vx=-1.8)

bricks = []
number_row = 6
for i in range(1, number_row):
    # remplissage des briques
    height = 30 * i
    bricks.append(Brick(30, height, 40, 20, number_row + 1 -i))
    bricks.append(Brick(80, height, 40, 20, number_row + 1 -i))
    bricks.append(Brick(130, height, 40, 20, number_row + 1 -i))
    bricks.append(Brick(180, height, 40, 20, number_row + 1 -i))
    bricks.append(Brick(230, height, 40, 20, number_row + 1 -i))
    bricks.append(Brick(280, height, 40, 20, number_row + 1 -i))
    bricks.append(Brick(330, height, 40, 20, number_row + 1 -i))

def update():
    global done, ball, bricks

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

def draw():
    global bricks
    top_wall.draw(root)
    right_wall.draw(root)
    left_wall.draw(root)

    pad.draw(root)
    ball.draw(root)

    for brick in bricks:
        brick.draw(root)

done = False
while not done:
    root.fill(BLACK)
    update()
    draw()
    pygame.display.update()
    clock.tick(60) # permet de bloquer le framerate à 60 images par secondes

pygame.quit()
