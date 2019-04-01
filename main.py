import pygame, sys, math
from pygame.locals import *
from classes import *

WIDTH = 400
HEIGHT = 600

pygame.init()
root = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(10, 10)

# definition des objets
clock = pygame.time.Clock()
left_wall = Brick(0, 0, 10, HEIGHT, BLUE, math.inf)
right_wall = Brick(WIDTH-10, 0, 10, HEIGHT, BLUE, math.inf)
top_wall = Brick(0, 0, WIDTH, 10, BLUE, math.inf)
pad = Pad(150, 575, 100, 15, WHITE)
ball = Ball(root.get_width() // 2, root.get_height() // 2, 10, WHITE, vy=-1.2, vx=-1.8)

def update():
    global done

    # gestion des evenements (bouger la barre, quitter l'appli)
    for event in pygame.event.get():
        if event.type == QUIT: done = True
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                if pad.x < right_wall.x - pad.w:
                    pad.x += 5
            if event.key == K_LEFT:
                if pad.x > left_wall.w:
                    pad.x -= 5
            if event.key == K_UP: ball.speed += 0.2
            if event.key == K_DOWN: ball.speed -= 0.2

    # faire rebondir la balle (murs et barre)
    if ball.cx >= 400 or ball.cx < 0:
        ball.vx = -ball.vx
    if ball.cy < 0 or ball.cy >= 600:
        ball.vy = -ball.vy

    # gestion du mouvement de la balle
    ball.update()

def draw():
    top_wall.draw(root)
    right_wall.draw(root)
    left_wall.draw(root)
    pad.draw(root)
    ball.draw(root)

done = False
while not done:
    root.fill(BLACK)
    update()
    draw()
    pygame.display.update()
    clock.tick(60) # permet de bloquer le framerate a 60 images par secondes

pygame.quit()
