import pygame, sys, math
from pygame.locals import *
from classes import *

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

Bricks = []
NumberRow = 6
i = 1
while i <= NumberRow:
    hauteur = 30 * i
    couleur = WHITE
    if NumberRow + 1 -i == 1:
        couleur = GREEN
        pass
    if NumberRow + 1 -i == 2:
        couleur = ORANGE
        pass
    if NumberRow + 1 -i == 3:
        couleur = PINK
        pass
    if NumberRow + 1 -i == 4:
        couleur = YELLOW
        pass
    if NumberRow + 1 -i == 5:
        couleur = BLUE
        pass
    if NumberRow + 1 -i == 6:
        couleur = RED
        pass

    brick = Brick(30, hauteur, 40, 20, couleur, NumberRow + 1 -i)
    Bricks.append(brick) 
    print(brick)
    brick = Brick(80, hauteur, 40, 20, couleur, NumberRow + 1 -i)
    Bricks.append(brick)
    brick = Brick(130, hauteur, 40, 20, couleur, NumberRow + 1 -i)
    Bricks.append(brick) 
    brick = Brick(180, hauteur, 40, 20, couleur, NumberRow + 1 -i)
    Bricks.append(brick) 
    brick = Brick(230, hauteur, 40, 20, couleur, NumberRow + 1 -i)
    Bricks.append(brick)
    brick = Brick(280, hauteur, 40, 20, couleur, NumberRow + 1 -i)
    Bricks.append(brick)  
    brick = Brick(330, hauteur, 40, 20, couleur, NumberRow + 1 -i)
    Bricks.append(brick)  
    i = i + 1
    
    pass





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

    # gestion du mouvement de la balle
    ball.update(left_wall, top_wall, right_wall, pad)

def draw():
    top_wall.draw(root)
    right_wall.draw(root)
    left_wall.draw(root)
    pad.draw(root)
    ball.draw(root)
    for brick in Bricks:
        brick.draw(root)
    pass

done = False
while not done:
    root.fill(BLACK)

    pygame.display.update()
    update()
    draw()
    pygame.display.update()
    clock.tick(60) # permet de bloquer le framerate a 60 images par secondes

pygame.quit()
