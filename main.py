import pygame, sys
from pygame.locals import *

pygame.init()
root = pygame.display.set_mode((400, 600))

GAME_LOOP = True
while GAME_LOOP:
    events = pygame.event.get()
    if pygame.event.Event(QUIT) in events:
        GAME_LOOP = False
        sys.exit()

    pygame.display.update()
