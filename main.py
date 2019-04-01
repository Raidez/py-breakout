import pygame, sys, math
from pygame.locals import *
from classes import *

BLACK = (0, 0, 0)
RED = (125, 0, 0)
BLUE = (0, 125, 255)

pygame.init()
root = pygame.display.set_mode((400, 600))

# définition d'une brique rouge
theo = Brick(0, 0, 20, 20, RED, 5)

done = False
while not done:
    # definition du fond et des contours
    root.fill(BLACK)
    Brick(0, 0, 10, 600, BLUE, math.inf).draw(root)
    Brick(390, 0, 10, 600, BLUE, math.inf).draw(root)
    Brick(0, 0, 400, 10, BLUE, math.inf).draw(root)

    for event in pygame.event.get():
        if event.type is QUIT: done = True
        if event.type is KEYDOWN:
            theo.pos.x += 5

    theo.draw(root)
    pygame.display.flip()
    # pygame.display.update()

pygame.quit()
