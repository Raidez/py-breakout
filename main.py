import pygame, sys
from pygame.locals import *
from classes import *

BLACK = (0, 0, 0)
RED = (125, 0, 0)

pygame.init()
root = pygame.display.set_mode((400, 600))

# définition d'une brique rouge
theo = Brick(0, 0, 20, 20, RED, 5)

done = False
while not done:
    root.fill(BLACK)
    for event in pygame.event.get():
        if event.type is QUIT: done = True
        if event.type is KEYDOWN:
            theo.x += 5

    theo.draw(root)
    pygame.display.flip()
    # pygame.display.update()

pygame.quit()
