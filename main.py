import pygame, sys
from pygame.locals import *
from classes import *

BLACK = (0, 0, 0)
RED = (125, 0, 0)
WHITE = (255,255,255)
BLUE = (0, 0, 125)

pygame.init()
root = pygame.display.set_mode((400, 600))

# definition des objets
brick = Brick(0, 0, 20, 20, RED, 5)
pad = Pad(200, 500, 20, 20, BLUE)

done = False
while not done:
    root.fill(BLACK)
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
