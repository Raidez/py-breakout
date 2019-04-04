#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, copy
from pygame.locals import *
from utils import *
from scenes import *

pygame.init()
root = pygame.display.set_mode((WIDTH, HEIGHT_WINDOW))
pygame.key.set_repeat(10, 10)

# configuration des scènes
game = GameScene(WIDTH, HEIGHT)
win = WinScene(WIDTH, HEIGHT)
lose = LoseScene(WIDTH, HEIGHT)
score = ScoreScene(WIDTH, HEIGHT_WINDOW - HEIGHT, game)
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
        if lose.restart and lose.lives > 0:
            del game
            game = GameScene(WIDTH, HEIGHT)
            current = game
            lose.restart = False
            lose.once = True
            lose.lives -= 1
            lose.text2 = lose.font2.render(f'Remaining lives : {lose.lives}', True, Color.WHITE, Color.RED)
            if lose.lives < 0:
                lose.draw_exit()

        if win.restart:
            score = game.score
            del game
            game = GameScene(WIDTH, HEIGHT)
            game.score = score
            current = game
            win.restart = False
            win.once = True

        # gestion des événements et dessin de la scène courante
        done = current.update(delta, events)
        score.update_score(game)
        score.draw()
        current.draw()

        root.blits(blit_sequence=((current, (0,0)), (score, (0,600))))

        pygame.display.update()

pygame.quit()
