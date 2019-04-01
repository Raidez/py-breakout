import pygame, sys, math
from pygame.locals import *
from classes import *

BLACK = (0, 0, 0)
RED = (125, 0, 0)
WHITE = (255,255,255)
BLUE = (0, 0, 125)

pygame.init()
root = pygame.display.set_mode((400, 600))

# definition des contours
mur_gauche = Brick(0, 0, 10, 600, BLUE, math.inf)
mur_droit = Brick(390, 0, 10, 600, BLUE, math.inf)
mur_haut = Brick(0, 0, 400, 10, BLUE, math.inf)

# definition des objets
brick = Brick(0, 0, 20, 20, RED, 5)
pad = Pad(150, 575, 100, 15, WHITE)

done = False
while not done:
    # mise a jour du fond et des contours
    root.fill(BLACK)
    mur_haut.draw(root)
    mur_droit.draw(root)
    mur_gauche.draw(root)

    for event in pygame.event.get():
        if event.type == QUIT: done = True
        if event.type == KEYDOWN and event.key == K_RIGHT:
            pad.x += 5
        elif event.type == KEYDOWN and event.key == K_LEFT:
            pad.x -= 5

    brick.draw(root)
    pad.draw(root)
    pygame.display.update()

pygame.quit()
