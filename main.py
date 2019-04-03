#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, copy
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
    # bloque le framerate à X ips
    # delta correspond au temps écoulé en millisecondes depuis la dernière frame
    delta = clock.tick(FPS_CAP) / 1000.0

    # gestion de l'événement pour quitter l'application
    # (ici pour ne pas avoir à le répéter dans chaque scène)
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT: done = True

    if not done:
        # s'il n'y a plus de briques alors victoire
        if len(game.bricks) == 0: current = win
        # si la balle sort de l'écran alors game over
        if game.ball.cy > (HEIGHT + 10): current = lose
        # restart
        if lose.restart:
            del game
            game = GameScene(WIDTH, HEIGHT)
            current = game
            lose.restart = False
            lose.once = True

        if win.restart:
            del game
            game = GameScene(WIDTH, HEIGHT)
            current = game
            win.restart = False
            win.once = True

        # gestion des événements et dessin de la scène courante
        done = current.update(delta, events)
        current.draw()
        root.blit(current, (0,0))

        pygame.display.update()

pygame.quit()
