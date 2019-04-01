import pygame, sys, math
from pygame.locals import *
from classes import *

pygame.init()
root = pygame.display.set_mode((400, 600))

# definition des objets
left_wall = Brick(0, 0, 10, 600, BLUE, math.inf)
right_wall = Brick(390, 0, 10, 600, BLUE, math.inf)
top_wall = Brick(0, 0, 400, 10, BLUE, math.inf)
pad = Pad(150, 575, 100, 15, WHITE)

def update():
    global done
    for event in pygame.event.get():
        if event.type == QUIT: done = True
        if event.type == KEYDOWN and event.key == K_RIGHT:
            pad.x += 5
        elif event.type == KEYDOWN and event.key == K_LEFT:
            pad.x -= 5

def draw():
    top_wall.draw(root)
    right_wall.draw(root)
    left_wall.draw(root)
    pad.draw(root)

done = False
while not done:
    root.fill(BLACK)
    update()
    draw()
    pygame.display.update()

pygame.quit()
