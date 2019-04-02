#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from utils import *
from scenes import *

pygame.init()
root = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(10, 10)

# configuration des scènes
game = GameScene(WIDTH, HEIGHT)
win = WinScene(WIDTH, HEIGHT)
lose = LoseScene(WIDTH, HEIGHT)
current = game

# définition des objets
clock = pygame.time.Clock()
done = False

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT: done = True

    if not done:
        # s'il n'y a plus de briques alors victoire
        if len(game.bricks) == 0:
            current = win

        if game.ball.cy > (HEIGHT + 10):
            current = lose

        done = current.update(events)
        current.draw()
        root.blit(current, (0,0))

        pygame.display.update()
        clock.tick(60) # permet de bloquer le framerate à 60 images par secondes

pygame.quit()
